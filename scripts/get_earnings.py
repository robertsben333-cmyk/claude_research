#!/usr/bin/env python3
"""
Build the daily US earnings universe for the actionable event window:

    companies reporting AFTER the close on the reference date
  + companies reporting BEFORE the open on the next NYSE trading day

Writes a machine-readable JSON universe that the downstream stages consume.

Sources are tried in order until one returns rows:

  1. nasdaq   - https://api.nasdaq.com/api/calendar/earnings   (no key)
  2. fmp      - Financial Modeling Prep                        (FMP_API_KEY)
  3. finnhub  - Finnhub earnings calendar                      (FINNHUB_API_KEY)

If every source fails the script still writes a valid universe file with
status "unavailable" and a machine-readable reason, so the calling agent can
fall back to WebSearch/WebFetch instead of guessing. Network egress that is
blocked by a proxy is reported as reason "network_blocked" specifically —
that means the environment, not the source, is the problem.

Usage:
    python3 scripts/get_earnings.py                       # today, default paths
    python3 scripts/get_earnings.py --date 2026-08-10
    python3 scripts/get_earnings.py --probe                # connectivity only
"""

import argparse
import calendar
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("requests is required: pip install requests")


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MIN_MARKET_CAP = 500_000_000


# ── NYSE calendar ─────────────────────────────────────────────────────────────

def _easter(year):
    """Easter Sunday via the Anonymous Gregorian algorithm."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    dy = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, mo, dy)


def _observed(d):
    """Saturday holiday -> observed Friday; Sunday holiday -> observed Monday."""
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def _nth_weekday(year, month, n, wd):
    """n-th weekday wd of month (1-indexed). n=-1 means last."""
    if n > 0:
        first = date(year, month, 1)
        offset = (wd - first.weekday()) % 7
        return first + timedelta(days=offset + 7 * (n - 1))
    last_day = calendar.monthrange(year, month)[1]
    last = date(year, month, last_day)
    offset = (last.weekday() - wd) % 7
    return last - timedelta(days=offset)


def nyse_holidays(year):
    """NYSE market holidays for *year*. Ad-hoc closures are not covered."""
    MON, THU = 0, 3
    h = {
        _observed(date(year, 1, 1)),        # New Year's Day
        _nth_weekday(year, 1, 3, MON),      # MLK Day
        _nth_weekday(year, 2, 3, MON),      # Presidents' Day
        _easter(year) - timedelta(days=2),  # Good Friday
        _nth_weekday(year, 5, -1, MON),     # Memorial Day
        _observed(date(year, 7, 4)),        # Independence Day
        _nth_weekday(year, 9, 1, MON),      # Labor Day
        _nth_weekday(year, 11, 4, THU),     # Thanksgiving
        _observed(date(year, 12, 25)),      # Christmas
    }
    if year >= 2022:
        h.add(_observed(date(year, 6, 19)))  # Juneteenth
    return h


def is_trading_day(d):
    return d.weekday() < 5 and d not in nyse_holidays(d.year)


def next_trading_day(d):
    """First NYSE trading day strictly after *d*."""
    nxt = d + timedelta(days=1)
    while not is_trading_day(nxt):
        nxt += timedelta(days=1)
    return nxt


# ── Source adapters ───────────────────────────────────────────────────────────

_UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nasdaq.com/",
}


class SourceError(Exception):
    """A source could not be used. `.reason` is machine-readable."""

    def __init__(self, reason, detail):
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


def _get(url, **kw):
    try:
        r = requests.get(url, timeout=25, **kw)
    except requests.exceptions.ProxyError as exc:
        raise SourceError("network_blocked", str(exc)) from exc
    except requests.exceptions.SSLError as exc:
        raise SourceError("tls_error", str(exc)) from exc
    except requests.exceptions.RequestException as exc:
        raise SourceError("network_error", str(exc)) from exc
    if r.status_code in (401, 403, 407):
        raise SourceError("forbidden", f"HTTP {r.status_code} from {url.split('?')[0]}")
    if r.status_code >= 400:
        raise SourceError("http_error", f"HTTP {r.status_code} from {url.split('?')[0]}")
    return r


def _norm(symbol, name, market_cap, session, eps_est=None, quarter=None,
          n_ests=None, source=None):
    return {
        "symbol": (symbol or "").strip().upper(),
        "name": (name or "").strip(),
        "market_cap_usd": market_cap,
        "session": session,                # "amc" | "bmo" | "unknown"
        "eps_estimate": eps_est,
        "fiscal_quarter_ending": quarter,
        "analyst_count": n_ests,
        "source": source,
    }


def _parse_money(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return int(s) if s else None
    try:
        return int(float(str(s).replace("$", "").replace(",", "").strip()))
    except (TypeError, ValueError):
        return None


def fetch_nasdaq(d):
    r = _get(
        "https://api.nasdaq.com/api/calendar/earnings",
        params={"date": d.strftime("%Y-%m-%d"), "offset": 0, "size": 500},
        headers=_UA,
    )
    rows = ((r.json() or {}).get("data") or {}).get("rows") or []
    session_map = {"time-after-hours": "amc", "time-pre-market": "bmo"}
    out = []
    for row in rows:
        out.append(_norm(
            row.get("symbol"),
            row.get("name"),
            _parse_money(row.get("marketCap")),
            session_map.get(row.get("time"), "unknown"),
            eps_est=row.get("epsForecast"),
            quarter=row.get("fiscalQuarterEnding"),
            n_ests=row.get("noOfEsts"),
            source="nasdaq",
        ))
    return out


def fetch_fmp(d):
    key = os.environ.get("FMP_API_KEY")
    if not key:
        raise SourceError("no_api_key", "FMP_API_KEY is not set")
    iso = d.strftime("%Y-%m-%d")
    r = _get(
        "https://financialmodelingprep.com/api/v3/earning_calendar",
        params={"from": iso, "to": iso, "apikey": key},
    )
    session_map = {"amc": "amc", "bmo": "bmo"}
    out = []
    for row in r.json() or []:
        out.append(_norm(
            row.get("symbol"),
            row.get("name") or row.get("symbol"),
            None,
            session_map.get((row.get("time") or "").lower(), "unknown"),
            eps_est=row.get("epsEstimated"),
            quarter=row.get("fiscalDateEnding"),
            source="fmp",
        ))
    return out


def fetch_finnhub(d):
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        raise SourceError("no_api_key", "FINNHUB_API_KEY is not set")
    iso = d.strftime("%Y-%m-%d")
    r = _get(
        "https://finnhub.io/api/v1/calendar/earnings",
        params={"from": iso, "to": iso, "token": key},
    )
    session_map = {"amc": "amc", "bmo": "bmo", "dmh": "unknown"}
    out = []
    for row in (r.json() or {}).get("earningsCalendar") or []:
        out.append(_norm(
            row.get("symbol"),
            row.get("symbol"),
            None,
            session_map.get((row.get("hour") or "").lower(), "unknown"),
            eps_est=row.get("epsEstimate"),
            quarter=row.get("quarter"),
            source="finnhub",
        ))
    return out


SOURCES = {"nasdaq": fetch_nasdaq, "fmp": fetch_fmp, "finnhub": fetch_finnhub}
SOURCE_ORDER = ["nasdaq", "fmp", "finnhub"]


def fetch_day(d, order):
    """Try each source in turn. Returns (rows, source_name, attempts)."""
    attempts = []
    for name in order:
        try:
            rows = SOURCES[name](d)
        except SourceError as exc:
            attempts.append({"source": name, "ok": False,
                             "reason": exc.reason, "detail": exc.detail[:300]})
            continue
        except Exception as exc:  # unexpected shape change, keep going
            attempts.append({"source": name, "ok": False,
                             "reason": "parse_error", "detail": str(exc)[:300]})
            continue
        attempts.append({"source": name, "ok": True, "rows": len(rows)})
        if rows:
            return rows, name, attempts
    return [], None, attempts


# ── Assembly ──────────────────────────────────────────────────────────────────

def build_universe(ref_date, order, min_market_cap):
    nxt = next_trading_day(ref_date)

    after_rows, after_src, after_attempts = fetch_day(ref_date, order)
    before_rows, before_src, before_attempts = fetch_day(nxt, order)

    after_close = [r for r in after_rows if r["session"] == "amc"]
    before_open = [r for r in before_rows if r["session"] == "bmo"]

    for r in after_close:
        r["event_date"] = ref_date.isoformat()
    for r in before_open:
        r["event_date"] = nxt.isoformat()

    combined = after_close + before_open
    for r in combined:
        mc = r.get("market_cap_usd")
        r["passes_market_cap_floor"] = bool(mc and mc >= min_market_cap)
        r["market_cap_known"] = mc is not None

    combined.sort(key=lambda r: (r.get("market_cap_usd") or 0), reverse=True)

    ok = bool(combined)
    reasons = [a.get("reason") for a in after_attempts + before_attempts
               if not a.get("ok")]
    if ok:
        status, status_reason = "ok", None
    elif "network_blocked" in reasons:
        status, status_reason = "unavailable", "network_blocked"
    elif reasons:
        status, status_reason = "unavailable", reasons[0]
    else:
        status, status_reason = "ok", None  # sources reachable, genuinely empty day

    eligible = [r for r in combined if r["passes_market_cap_floor"]]

    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "status_reason": status_reason,
        "reference_date": ref_date.isoformat(),
        "reference_is_trading_day": is_trading_day(ref_date),
        "next_trading_day": nxt.isoformat(),
        "window_covered": (
            f"After the US close on {ref_date:%A %d %B %Y} through before the US open "
            f"on {nxt:%A %d %B %Y}"
        ),
        "min_market_cap_usd": min_market_cap,
        "sources_used": {"after_close": after_src, "before_open": before_src},
        "source_attempts": {"after_close": after_attempts, "before_open": before_attempts},
        "counts": {
            "after_close": len(after_close),
            "before_open": len(before_open),
            "total": len(combined),
            "above_market_cap_floor": len(eligible),
        },
        "companies": combined,
    }


def to_markdown(u):
    lines = [
        f"# Earnings universe — {u['reference_date']}",
        "",
        f"**Window:** {u['window_covered']}",
        f"**Generated:** {u['generated_at_utc']} UTC",
        f"**Status:** `{u['status']}`"
        + (f" (`{u['status_reason']}`)" if u["status_reason"] else ""),
        f"**Source:** after-close `{u['sources_used']['after_close']}` · "
        f"before-open `{u['sources_used']['before_open']}`",
        "",
        f"**Counts:** {u['counts']['after_close']} after-close + "
        f"{u['counts']['before_open']} before-open = **{u['counts']['total']}** total; "
        f"{u['counts']['above_market_cap_floor']} above the "
        f"${u['min_market_cap_usd']:,} market-cap floor.",
        "",
    ]
    if u["status"] != "ok":
        lines += [
            "> The automated feed did not return data. The universe below is empty and",
            "> must be rebuilt by the agent using WebSearch/WebFetch before triage runs.",
            "",
        ]
    if u["companies"]:
        lines += [
            "| Ticker | Company | Session | Event date | Market cap | EPS est. | Quarter |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
        for c in u["companies"]:
            mc = c.get("market_cap_usd")
            mc_s = f"${mc/1e9:.2f}B" if mc else "n/a"
            lines.append(
                f"| `{c['symbol']}` | {c['name']} | {c['session'].upper()} | "
                f"{c.get('event_date','')} | {mc_s} | {c.get('eps_estimate') or 'n/a'} | "
                f"{c.get('fiscal_quarter_ending') or 'n/a'} |"
            )
        lines.append("")
    return "\n".join(lines)


def probe(order):
    """Connectivity check only. Exit 0 if at least one source works."""
    today = date.today()
    any_ok = False
    for name in order:
        try:
            rows = SOURCES[name](today)
            print(f"  ok        {name:8s} ({len(rows)} rows for {today})")
            any_ok = True
        except SourceError as exc:
            print(f"  FAIL      {name:8s} {exc.reason}: {exc.detail[:120]}")
        except Exception as exc:
            print(f"  FAIL      {name:8s} unexpected: {exc}")
    return 0 if any_ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", metavar="YYYY-MM-DD",
                   help="Reference date (default: today)")
    p.add_argument("--out-dir", metavar="DIR",
                   help="Directory for 00-universe.{json,md} "
                        "(default: research/<YYYY>/<MM>/<YYYY-MM-DD>)")
    p.add_argument("--source", default="auto",
                   choices=["auto"] + SOURCE_ORDER,
                   help="Force one source instead of trying all (default: auto)")
    p.add_argument("--min-market-cap", type=int, default=DEFAULT_MIN_MARKET_CAP,
                   help=f"Market-cap floor in USD (default: {DEFAULT_MIN_MARKET_CAP})")
    p.add_argument("--probe", action="store_true",
                   help="Test source connectivity and exit")
    args = p.parse_args()

    order = SOURCE_ORDER if args.source == "auto" else [args.source]

    if args.probe:
        sys.exit(probe(order))

    if args.date:
        try:
            ref = date.fromisoformat(args.date)
        except ValueError:
            sys.exit(f"Invalid --date '{args.date}'. Use YYYY-MM-DD.")
    else:
        ref = date.today()

    universe = build_universe(ref, order, args.min_market_cap)

    out_dir = args.out_dir or os.path.join(
        REPO_ROOT, "research", f"{ref:%Y}", f"{ref:%m}", ref.isoformat()
    )
    os.makedirs(out_dir, exist_ok=True)

    json_path = os.path.join(out_dir, "00-universe.json")
    md_path = os.path.join(out_dir, "00-universe.md")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(universe, fh, indent=2)
        fh.write("\n")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(to_markdown(universe))

    c = universe["counts"]
    print(f"status         : {universe['status']}"
          + (f" ({universe['status_reason']})" if universe["status_reason"] else ""))
    print(f"window         : {universe['window_covered']}")
    print(f"after close    : {c['after_close']}")
    print(f"before open    : {c['before_open']}")
    print(f"above floor    : {c['above_market_cap_floor']}")
    print(f"wrote          : {json_path}")
    print(f"wrote          : {md_path}")

    # Exit 2 signals "no data, fall back to web research" without looking like a crash.
    sys.exit(0 if universe["status"] == "ok" else 2)


if __name__ == "__main__":
    main()
