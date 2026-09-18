#!/usr/bin/env python3
"""The day's European earnings universe, across the UK, France and Germany.

WHY THREE MARKETS IN ONE UNIVERSE, AND NOT THREE STAGES
-------------------------------------------------------
None of the three is a daily market on its own. Measured in Phase 1
(`researcher_europe/SUBMARKET.md`):

  UK       17 results announcements a day ex funds at the median, but 3 on
           2026-03-06 and 4 on 2026-01-16, and 7 a day above a $200k turnover floor
           with a floor of ONE.
  Germany  60% of issuers report quarterly -- Prime Standard still owes quarterly
           statements where the Transparency Directive floor is annual-plus-half-year
           -- but 153 of 259 forward events sit in November and June carries one.
  France   semi-annual, median gap 204 days, with 94 of 161 forward events in
           February and March.

They peak in different months, so pooling three seasonal calendars is what produces
one stream. Pooled above $1m/day of turnover that is roughly 8 to 12 names on a median
day. It is NOT 8 to 12 every day: Fridays, August, late December and the German
June-July gap will produce two- and three-name days. A thin day is a weak day and not
a broken stage; the response to one is to hunt the names there are, never to drop the
turnover floor, because below $1m/day the short register that substitutes for the
missing option anchor resolves on 12% of names and nothing can be traded anyway.

EUROPE REPORTS BEFORE THE OPEN
------------------------------
339 of 379 UK results announcements with a parseable RNS timestamp landed before 08:00
London; 31 in session and 9 after the close. The vendor calendar agrees (662 of 799 UK
rows pre-market). France has the largest after-close share of the three, because French
issuers publish quarterly revenue after the 17:35 close.

So the window this stage ranks is `close(D-1) -> close(D)` for a `bmo` name and
`close(D) -> close(D+1)` for an `amc` one, and the baseline for a bmo name has to be
sealed the EVENING BEFORE the print. That is a scheduling constraint neither the US nor
the Japanese stage has, and it is why `--date` defaults to the next session rather than
to today.

THE CALENDAR IS A VENDOR CALENDAR AND ITS ERROR RATE WAS MEASURED
-----------------------------------------------------------------
TradingView's public scanner carries, per primary listing, the last and next scheduled
release date and a session flag. Against the actual RNS record over 20 scraped days,
90 of its UK rows fell on a scraped day and 88 had a same-day results announcement from
the same issuer: a 2.2% phantom rate. The US stage's `time-not-supplied` rows were 20 of
20 phantom on 2026-09-17, so this is a different object -- but TRT was ranked, traded and
never reported, and a 2.2% rate on a 10-name day is one phantom every five days. The
confirmation pass in `eu_resolve.py` and `event_occurred: false` are not optional.

SELECTION, AND WHY IT IS RANDOM
-------------------------------
Two steps, and the second is deliberately not a judgement:

  1. Drop everything below `--min-turnover-usd` on median 20-session turnover,
     currency-normalised to USD with a live rate that is written into the output.
     $1m/day rather than the $200k the US and Japanese stages use, and the reason is
     measured rather than borrowed: below $1m the FCA short register resolves on 22 of
     190 UK names (12%) against 41 of 46 (89%) in the $1-5m band, so the cheap half of
     the universe is the half where the substitute anchor stops working.
  2. If more than `--cap` survive, take a RANDOM sample seeded by the date.

Random, because any other cut is a second ranking the scorer cannot see, and the US run
has already paid for that once. It also matters here for a reason specific to this
stage: Phase 1 found sell-side coverage runs 1-2 analysts below $1m/day, 5-7 at $1-5m,
11-13 at $5-25m and 16-19 above, so a cut to the "under-read" band would bake the
stage's own thesis into its universe and make it unfalsifiable. The floor is for
capacity and anchor coverage; the draw is random; `median_turnover_usd_20d` and the
analyst count ride in the baseline so `eu_resolve.py` can rank performance BY band
instead of assuming it.
"""
import argparse
import json
import random
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_market import MARKETS, exchange_holidays, half_session, yahoo_symbol  # noqa: E402

UTC = ZoneInfo("UTC")
REPO = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
YQ = "https://query1.finance.yahoo.com"
TV = "https://scanner.tradingview.com/{scanner}/scan"
GOVUK = "https://www.gov.uk/bank-holidays.json"
HOLIDAY_CACHE = REPO / "researcher_europe" / "analysis" / "eu-holidays.json"

TV_COLUMNS = ["name", "description", "close", "currency", "market_cap_basic",
              "average_volume_10d_calc", "earnings_release_date",
              "earnings_release_time", "earnings_release_next_date",
              "earnings_release_next_time", "exchange", "sector", "country"]

# The vendor's session flag. 0 is an admission of ignorance and is treated as one.
SESSION_FLAG = {-1: "bmo", 1: "amc", 0: None}


def fetch(url, timeout=45, post=None, referer=None):
    """curl, not urllib: this container reaches the internet through a proxy that
    urllib does not pick up, and a silent URLError here would look like an empty
    calendar rather than a broken fetch. The same reason jp_universe.py gives."""
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {UA}"]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    if post is not None:
        cmd += ["-X", "POST", "-H", "Content-Type: application/json",
                "--data-binary", "@-"]
    cmd += ["-w", "\n%{http_code}", url]
    p = subprocess.run(cmd, capture_output=True,
                       input=json.dumps(post).encode() if post is not None else None)
    out = p.stdout
    tail = out[-4:].decode("ascii", "replace").strip()
    body = out[: -len(tail) - 1] if tail.isdigit() else out
    code = int(tail) if tail.isdigit() else 0
    if code != 200:
        raise RuntimeError(f"HTTP {code} for {url}")
    return body.decode("utf-8", "replace")


# --- FX ---------------------------------------------------------------------------
def fx_rates():
    """GBP and EUR against USD, live, with the source carried into the output.

    A constant would be simpler and would silently move the turnover floor by 10% a
    year. The floor is the only selection this stage makes that is not random, so the
    number it is applied against has to be reproducible from the file.
    """
    out = {"USD": 1.0, "source": f"{YQ}/v8/finance/chart/<pair>=X",
           "as_of": datetime.now(UTC).isoformat(timespec="seconds")}
    for pair, code in (("GBPUSD", "GBP"), ("EURUSD", "EUR")):
        try:
            d = json.loads(fetch(f"{YQ}/v8/finance/chart/{pair}=X?range=5d&interval=1d",
                                 timeout=25))
            closes = [c for c in d["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                      if c is not None]
            out[code] = round(closes[-1], 5)
        except Exception as exc:
            out[code] = None
            out.setdefault("errors", {})[code] = str(exc)
    out["GBp"] = round(out["GBP"] / 100.0, 7) if out.get("GBP") else None
    out["GBX"] = out["GBp"]
    return out


def to_usd(amount, currency, fx):
    r = fx.get(currency)
    return None if (amount is None or r is None) else amount * r


# --- calendar ---------------------------------------------------------------------
def scan(market):
    cfg = MARKETS[market]
    body = {"filter": [{"left": "is_primary", "operation": "equal", "right": True},
                       {"left": "type", "operation": "equal", "right": "stock"}],
            "options": {"lang": "en"}, "columns": TV_COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
            "range": [0, 5000]}
    d = json.loads(fetch(TV.format(scanner=cfg["scanner"]), post=body, timeout=90))
    rows = []
    for x in d.get("data", []):
        r = dict(zip(TV_COLUMNS, x["d"]))
        r["tv_symbol"] = x["s"]
        rows.append(r)
    return rows, d.get("totalCount")


def scheduled_on(rows, target, past=False):
    """Rows whose NEXT scheduled release is `target`, with the session resolved.

    `past=True` reads the vendor's LAST release date instead. That is a VALIDATION
    switch and nothing else: it builds a universe for a date whose outcome already
    exists, so a run built with it can exercise the whole chain against a real day but
    can never be a result about anything. Every file it produces is stamped
    `validation_only: true` for exactly that reason.
    """
    key = "earnings_release_date" if past else "earnings_release_next_date"
    tkey = "earnings_release_time" if past else "earnings_release_next_time"
    out = []
    for r in rows:
        ts = r.get(key)
        if not ts:
            continue
        d = datetime.fromtimestamp(ts, UTC).date().isoformat()
        if d != target:
            continue
        sess = SESSION_FLAG.get(r.get(tkey))
        out.append({**r, "scheduled_date": d, "session": sess or "bmo",
                    "session_unresolved": sess is None,
                    "session_basis": ("vendor flag " + str(r.get(tkey))
                                      if sess else
                                      "vendor says unknown; defaulted to bmo because "
                                      "339 of 379 measured UK results announcements "
                                      "landed before 08:00 -- the resolver measures "
                                      "BOTH windows for this row")})
    return out


# --- holidays ---------------------------------------------------------------------
def closed_reason(market, day):
    d = date.fromisoformat(day)
    if d.weekday() >= 5:
        return "weekend"
    hol = exchange_holidays(market, d.year)
    if market == "uk":
        cache = {}
        if HOLIDAY_CACHE.exists():
            try:
                cache = json.loads(HOLIDAY_CACHE.read_text(encoding="utf-8"))
            except Exception:
                cache = {}
        if "uk" not in cache:
            try:
                j = json.loads(fetch(GOVUK, timeout=25))
                cache["uk"] = {e["date"]: e["title"]
                               for e in j["england-and-wales"]["events"]}
                HOLIDAY_CACHE.parent.mkdir(parents=True, exist_ok=True)
                HOLIDAY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
            except Exception:
                cache["uk"] = {}          # an unreachable list is not a reason to stop
        name = (cache.get("uk") or {}).get(day)
        if name:
            return f"UK bank holiday: {name}"
    if day in hol:
        return "exchange holiday"
    return None


# --- tape -------------------------------------------------------------------------
def tape(symbol, days=40):
    """Spot, the 20- and 5-session run-ups and median 20-session turnover.

    Turnover rather than market cap, for the reason the US and Japanese stages give:
    what binds is what can be traded in a day. Median rather than mean because one
    earnings day inside the window would otherwise set the level.
    """
    try:
        d = json.loads(fetch(f"{YQ}/v8/finance/chart/{symbol}?range={days}d&interval=1d",
                             timeout=30))
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        closes = [c for c in q["close"] if c is not None]
        if len(closes) < 5:
            return {"error": "too few bars"}
        pairs = [(c, v) for c, v in zip(q["close"], q.get("volume") or [])
                 if c is not None and v is not None]
        turn = sorted(c * v for c, v in pairs[-20:]) or [0]
        w20, w5 = closes[-21:], closes[-6:]
        return {
            "spot": round(closes[-1], 4),
            "currency": res["meta"].get("currency"),
            "run_up_20d_pct": round((w20[-1] / w20[0] - 1) * 100, 2) if len(w20) >= 2 else None,
            "run_up_5d_pct": round((w5[-1] / w5[0] - 1) * 100, 2) if len(w5) >= 2 else None,
            "median_turnover_native_20d": int(turn[len(turn) // 2]),
            "bars": len(closes),
        }
    except Exception as exc:
        return {"error": str(exc)}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="event date. Default: the NEXT calendar day, "
                                   "because Europe reports before the open and the "
                                   "baseline is sealed the evening before.")
    ap.add_argument("--markets", default="uk,de,fr",
                    help="comma-separated subset of uk,de,fr (default all three)")
    ap.add_argument("--cap", type=int, default=12,
                    help="most names to hunt in a day (default 12)")
    ap.add_argument("--min-turnover-usd", type=float, default=1_000_000,
                    help="median 20-session turnover floor in USD (default 1e6). "
                         "Below it the short register resolves on 12%% of names and "
                         "nothing is tradeable; see SUBMARKET.md section 4.")
    ap.add_argument("--use-last-release", action="store_true",
                    help="VALIDATION ONLY. Build the universe from the vendor's LAST "
                         "release date instead of its next one, so the whole chain can "
                         "be exercised against a real past day. The outcome already "
                         "exists, so nothing built this way is a result about anything "
                         "and every file is stamped validation_only.")
    ap.add_argument("--no-tape", action="store_true",
                    help="skip Yahoo entirely: emits the raw calendar with no screen "
                         "and no draw, for inspecting what the vendor is publishing")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    markets = [m.strip() for m in a.markets.split(",") if m.strip()]
    bad = [m for m in markets if m not in MARKETS]
    if bad:
        raise SystemExit(f"unknown market(s): {bad}; known: {sorted(MARKETS)}")

    target = a.date or (datetime.now(UTC).date() + timedelta(days=1)).isoformat()
    fx = fx_rates()

    out = {
        "market": "EU",
        "markets": markets,
        "event_date": target,
        "window": (f"{target} close of the PREVIOUS session -> {target} close, for a "
                   f"`bmo` name; {target} close -> next close for an `amc` one. "
                   f"Europe reports before the open: 339 of 379 measured UK results "
                   f"announcements landed before 08:00 London."),
        "fx": fx,
        "cap": a.cap,
        "min_turnover_usd": a.min_turnover_usd,
        "calendar_source": "TradingView public scanner (vendor). Measured phantom rate "
                           "on the UK: 2 of 90 rows over 20 sampled days. Confirmation "
                           "is eu_resolve.py's job and event_occurred: false is "
                           "reachable.",
        "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "validation_only": bool(a.use_last_release),
        "per_market": {},
    }

    todays, closed_all = [], {}
    for m in markets:
        try:
            rows, total = scan(m)
        except Exception as exc:
            out["per_market"][m] = {"error": str(exc)}
            continue
        closed = closed_reason(m, target)
        closed_all[m] = closed
        got = [] if closed else scheduled_on(rows, target, a.use_last_release)
        for r in got:
            r["_market"] = m
        todays.extend(got)
        out["per_market"][m] = {
            "universe_size": len(rows), "vendor_total": total,
            "scheduled_today": len(got),
            "market_closed": closed,
            "half_session": half_session(m, target),
            "confirmation_source": MARKETS[m]["confirm_name"],
            "short_register": MARKETS[m]["short_register"],
        }

    out["scheduled_today"] = len(todays)
    if all(closed_all.get(m) for m in markets):
        out["names"] = []
        out["note"] = (f"Every market in {markets} is shut on {target} "
                       f"({closed_all}). An empty universe here is the exchanges being "
                       f"closed, not a calendar that has yet to publish.")
        _write(out, a.out, target)
        return

    if a.no_tape:
        out["names"] = todays
        out["note"] = "--no-tape: no screen, no draw"
        _write(out, a.out, target)
        return

    eligible, dropped = [], []
    for r in todays:
        m = r["_market"]
        sym = yahoo_symbol(m, r["tv_symbol"])
        r = dict(r)
        r["yahoo_symbol"] = sym
        r["tape"] = tape(sym)
        t = r["tape"]
        native = t.get("median_turnover_native_20d")
        usd = to_usd(native, t.get("currency"), fx)
        r["median_turnover_usd_20d"] = int(usd) if usd is not None else None
        if t.get("error") or usd is None:
            r["drop_reason"] = f"no tape ({t.get('error', 'no fx for ' + str(t.get('currency')))})"
            dropped.append(r)
        elif usd < a.min_turnover_usd:
            r["drop_reason"] = (f"below the turnover floor: ${usd:,.0f} < "
                                f"${a.min_turnover_usd:,.0f} a day")
            dropped.append(r)
        else:
            eligible.append(r)

    seed = f"eu-{target}"
    rng = random.Random(seed)
    if len(eligible) > a.cap:
        picked = sorted(rng.sample(eligible, a.cap),
                        key=lambda x: (x["_market"], x["name"]))
        method = f"random sample of {len(eligible)} eligible, seed '{seed}'"
    else:
        picked = sorted(eligible, key=lambda x: (x["_market"], x["name"]))
        method = f"all {len(eligible)} eligible names (at or under the cap)"

    out["selection"] = {
        "method": method, "seed": seed,
        "eligible": len(eligible), "dropped": len(dropped), "hunted": len(picked),
        "by_market": {m: sum(1 for x in picked if x["_market"] == m) for m in markets},
        "basis": "Turnover floor for capacity and anchor coverage, then a seeded random "
                 "draw. The floor is NOT a size-band cut: Phase 1 found coverage runs "
                 "5-7 analysts at $1-5m of turnover against 16-19 above $25m, and "
                 "selecting on that band would bake this stage's own thesis into its "
                 "universe. Turnover rides in every baseline so the resolver can rank "
                 "performance by band instead of assuming it.",
    }
    out["eligible_symbols"] = sorted(f'{x["_market"]}:{x["name"]}' for x in eligible)
    out["names"] = picked
    out["dropped"] = dropped
    _write(out, a.out, target)


def _write(out, dest, target):
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if dest:
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_text(text + "\n", encoding="utf-8")
        s = out.get("selection", {})
        print(f"{target}: {out.get('scheduled_today', 0)} scheduled, "
              f"{s.get('eligible', '-')} eligible, {s.get('hunted', '-')} hunted "
              f"{s.get('by_market', '')} -> {dest}")
    else:
        print(text)


if __name__ == "__main__":
    main()
