#!/usr/bin/env python3
"""Build and qualify the day's Canadian earnings universe.

Same job as `researcher_us/scripts/edge_universe.py`, `jp_universe.py` and
`eu_universe.py`, and it writes the same shape so the shared scorer reads a Canadian
run unchanged. Three things here exist nowhere else in the repo, and all three are
answers to something measured in `researcher_canada/SOURCES.md`.

THE CALENDAR IS RECONCILED, NOT CHOSEN. Wall Street Horizon (through TMX) and
TradingView disagree on 172 of 277 forward dates. Neither is established, so the stage
does not pick one: it records both and grades the agreement.

    confirmed   WSH says CON. The issuer has told its calendar vendor the date.
    agreed      WSH says UNC and the vendor lands on the same day.
    wsh_only    WSH has a date, the vendor has nothing near it.
    vendor_only WSH has no event for this issuer at all (26% of the universe).
    disputed    both have a date and they differ. NOT HUNTED unless the issuer's own
                "we will report on X" release confirms it.

Every one of those is carried into the baseline, so after a fortnight of runs the
question "which calendar is right" is answered by the resolved files rather than by
argument. That is the cheapest of the three open tests in SOURCES.md and it runs itself.

THE EVENT SHAPE IS SCREENED. About a third of the eligible universe reports by filing
an interim financial statement on SEDAR+ with no press release at all. That is a real
reporting event and it is not the event this method assumes, so `filing_only` issuers
are kept in the file and kept out of the draw. See `ca_market.event_shape`.

THE DRAW IS RANDOM AND THE CUT IS TURNOVER, exactly as in Tokyo, for exactly the same
reason: any other cut is a second ranking the scorer cannot see, and this repo has
already paid once for one when the two highest-priority US names each got two hunters.
"""
import argparse
import json
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "researcher_us" / "scripts"))
import ca_market as M                                   # noqa: E402
import ca_sources as CA                                 # noqa: E402
from share_class import collapse                        # noqa: E402

REPO = Path(__file__).resolve().parents[2]
TV = "https://scanner.tradingview.com/canada/scan"
YQ = "https://query1.finance.yahoo.com"
TV_COLUMNS = ["name", "description", "close", "currency", "market_cap_basic",
              "average_volume_10d_calc", "earnings_release_date",
              "earnings_release_time", "earnings_release_next_date",
              "earnings_release_next_time", "exchange", "sector"]
SESSION_FLAG = {-1: "bmo", 1: "amc", 0: None}
FX_FALLBACK = 0.71


def curl_json(args, timeout=60, post=None):
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {CA.UA}"]
    if post is not None:
        cmd += ["-X", "POST", "-H", "Content-Type: application/json", "--data-binary", "@-"]
    cmd += args
    p = subprocess.run(cmd, capture_output=True,
                       input=json.dumps(post).encode() if post is not None else None)
    return json.loads(p.stdout)


def fx_cadusd():
    """Live, with the fallback RECORDED rather than silent. The floor is the only
    non-random selection this stage makes, so the number it is applied against has to be
    reproducible from the file, and a 429 from Yahoo must not read as a live rate."""
    for i in range(5):
        try:
            d = curl_json([f"{YQ}/v8/finance/chart/CADUSD=X?range=5d&interval=1d"], 25)
            c = [x for x in d["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x]
            return round(c[-1], 5), f"{YQ}/v8/finance/chart/CADUSD=X"
        except Exception:
            pass
    return FX_FALLBACK, f"FALLBACK CONSTANT {FX_FALLBACK} -- yahoo did not answer"


def scan():
    body = {"filter": [{"left": "is_primary", "operation": "equal", "right": True},
                       {"left": "type", "operation": "equal", "right": "stock"}],
            "options": {"lang": "en"}, "columns": TV_COLUMNS,
            "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
            "range": [0, 8000]}
    d = curl_json([TV], 90, post=body)
    return [dict(zip(TV_COLUMNS, x["d"]), tv_symbol=x["s"]) for x in d.get("data", [])]


def reconcile(tv_date, wsh):
    """Grade the agreement between the two calendars. Returns (confidence, date, session)."""
    if wsh:
        if wsh["confirmed"]:
            return "confirmed", wsh["date"], wsh["session"]
        if tv_date and wsh["date"] == tv_date:
            return "agreed", wsh["date"], wsh["session"]
        if not tv_date:
            return "wsh_only", wsh["date"], wsh["session"]
        return "disputed", wsh["date"], wsh["session"]
    return "vendor_only", tv_date, None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="event date, Toronto. Default: today.")
    ap.add_argument("--cap", type=int, default=20)
    ap.add_argument("--min-turnover-usd", type=int, default=200_000,
                    help="median 20-day turnover floor in USD; the same capacity bar "
                         "stages E, J and EU screen on (default 200000)")
    ap.add_argument("--window-days", type=int, default=7,
                    help="how far either side of the target a vendor date may sit and "
                         "still be a candidate, since the two calendars disagree")
    ap.add_argument("--hunt-disputed", action="store_true",
                    help="hunt names whose two calendars disagree and whose date the "
                         "issuer has not announced. Off by default: this is how TRT "
                         "happened.")
    ap.add_argument("--validate-past", action="store_true",
                    help="build the universe from the vendor's LAST release date rather "
                         "than its next one. A VALIDATION SWITCH ONLY: it builds a day "
                         "whose outcome already exists, so the run can exercise the whole "
                         "chain and can never be a result about anything. Every file it "
                         "writes is stamped validation_only.")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    target = a.date or datetime.now(timezone.utc).astimezone(
        __import__("zoneinfo").ZoneInfo(M.TZ)).date().isoformat()
    closed = M.market_closed(target)
    fx, fx_src = fx_cadusd()

    out = {
        "market": "CA", "event_date": target, "timezone": M.TZ,
        "cap": a.cap, "min_turnover_usd": a.min_turnover_usd,
        "cadusd": fx, "fx_source": fx_src,
        "market_closed": closed,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {"calendar_vendor": TV,
                    "calendar_confirmed": "getWSHEventData via app-money.tmx.com",
                    "archive": "getNewsForSymbol via app-money.tmx.com"},
    }

    if closed:
        out["names"], out["dropped"] = [], []
        out["note"] = (f"Toronto is closed on {target} ({closed}). An empty universe here "
                       f"is the exchange being shut, not a calendar that failed to read.")
        emit(out, a.out, target)
        return

    rows = scan()
    out["scanner_rows"] = len(rows)
    out["validation_only"] = bool(a.validate_past)
    date_key = "earnings_release_date" if a.validate_past else "earnings_release_next_date"
    time_key = "earnings_release_time" if a.validate_past else "earnings_release_next_time"
    lo = (date.fromisoformat(target) - timedelta(days=a.window_days)).isoformat()
    hi = (date.fromisoformat(target) + timedelta(days=a.window_days)).isoformat()

    cand = []
    for r in rows:
        ts = r.get(date_key)
        d = datetime.fromtimestamp(ts, timezone.utc).date().isoformat() if ts else None
        if d and not (lo <= d <= hi):
            continue
        if not d:
            continue                      # WSH-only names are unreachable without a scan hit
        px, vol = r.get("close"), r.get("average_volume_10d_calc")
        turn = px * vol * fx if (px and vol) else None
        cand.append({"ticker": r["tv_symbol"].split(":")[-1],
                     "company": r.get("description") or r.get("name"),
                     "exchange": r.get("exchange"), "sector": r.get("sector"),
                     "close": px, "currency": r.get("currency"),
                     "turnover_usd": round(turn) if turn else None,
                     "tv_date": d, "tv_session": SESSION_FLAG.get(r.get(time_key)),
                     "market_cap_usd": r.get("market_cap_basic")})
    out["candidates_in_window"] = len(cand)

    def enrich(c):
        c = dict(c)
        if a.validate_past:
            # WSH only carries FORWARD events, so a past-date build has nothing to
            # reconcile against and must not pretend otherwise.
            c["wsh"] = None
            c["date_confidence"] = "validation_past"
            c["event_date"] = c["tv_date"]
            c["session"] = c["tv_session"] or "amc"
            c["session_unresolved"] = c["tv_session"] is None
            try:
                n = CA.news(c["ticker"], limit=100)
            except Exception:
                n = []
            shape, k = M.event_shape([x.get("headline") for x in n])
            c["event_shape"], c["financial_headlines"] = shape, k
            c["announced"] = M.announced_before(n, c["event_date"] or target)
            c["news_rows"] = len(n)
            return c
        try:
            ev = CA.earnings_event(c["ticker"], lo)
        except Exception as exc:
            ev, c["wsh_error"] = [], str(exc)
        w = ev[0] if ev else None
        c["wsh"] = w
        conf, dt, sess = reconcile(c["tv_date"], w)
        c["date_confidence"], c["event_date"], c["session"] = conf, dt, sess or c["tv_session"]
        c["session_unresolved"] = c["session"] is None
        if c["session"] is None:
            c["session"] = "amc"          # Canada is amc-heavy: 188 of 271 WSH rows
        try:
            n = CA.news(c["ticker"], limit=100)
        except Exception as exc:
            n, c["news_error"] = [], str(exc)
        shape, k = M.event_shape([x.get("headline") for x in n])
        c["event_shape"], c["financial_headlines"] = shape, k
        c["announced"] = M.announced_before(n, c["event_date"] or target)
        c["news_rows"] = len(n)
        return c

    with ThreadPoolExecutor(max_workers=8) as ex:
        cand = list(ex.map(enrich, cand))

    # Only names whose RECONCILED date is the target are today's.
    todays = [c for c in cand if c["event_date"] == target]
    out["scheduled_today"] = len(todays)
    out["calendar_reconciliation"] = {
        k: sum(1 for c in todays if c["date_confidence"] == k)
        for k in ("confirmed", "agreed", "wsh_only", "vendor_only", "disputed")}
    out["moved_off_target_by_wsh"] = [
        {"ticker": c["ticker"], "vendor": c["tv_date"], "wsh": c["wsh"]["date"],
         "status": c["wsh"]["status"]}
        for c in cand if c["tv_date"] == target and c["event_date"] != target]

    eligible, dropped = [], []
    for c in todays:
        t = c["turnover_usd"]
        if not t:
            c["drop_reason"] = "no tape"
        elif t < a.min_turnover_usd:
            c["drop_reason"] = f"below the turnover floor: ${t:,} < ${a.min_turnover_usd:,}"
        elif c["event_shape"] == "filing_only":
            c["drop_reason"] = (
                f"filing-only issuer: {c['financial_headlines']} financial-results "
                f"headlines in its last {c['news_rows']} releases. It reports by filing "
                f"interim statements on SEDAR+, which is a real event and not one this "
                f"method can hunt -- there is no release for the market to reprice.")
        elif c["date_confidence"] == "disputed" and not c["announced"] and not a.hunt_disputed:
            c["drop_reason"] = (
                f"disputed date: the vendor says {c['tv_date']}, Wall Street Horizon "
                f"says {c['wsh']['date']} and neither is confirmed. The issuer has not "
                f"announced a date. Hunting this is how TRT happened.")
        else:
            eligible.append(c)
            continue
        dropped.append(c)

    kept, folded = collapse(eligible)
    for f in folded:
        f["drop_reason"] = f.get("folded_because")
    dropped += folded

    seed = f"ca-{target}"
    rng = random.Random(seed)
    if len(kept) > a.cap:
        picked = sorted(rng.sample(kept, a.cap), key=lambda x: x["ticker"])
        method = f"random sample of {len(kept)} eligible, seed '{seed}'"
    else:
        picked = sorted(kept, key=lambda x: x["ticker"])
        method = f"all {len(kept)} eligible names (at or under the cap)"

    out["selection"] = {"method": method, "seed": seed, "eligible": len(kept),
                        "dropped": len(dropped), "hunted": len(picked),
                        "share_classes_folded": len(folded)}
    out["eligible_tickers"] = sorted(x["ticker"] for x in kept)
    out["sessions"] = {s: sum(1 for x in picked if x["session"] == s)
                       for s in ("amc", "bmo")}
    out["names"] = picked
    out["dropped"] = dropped
    emit(out, a.out, target)


def emit(out, path, target):
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text + "\n", encoding="utf-8")
        s = out.get("selection", {})
        print(f"{target}: {out.get('scanner_rows', '-')} scanner rows, "
              f"{out.get('scheduled_today', 0)} scheduled today "
              f"{out.get('calendar_reconciliation', {})}, "
              f"{s.get('eligible', 0)} eligible, {s.get('hunted', 0)} hunted -> {path}")
    else:
        print(text)


if __name__ == "__main__":
    main()
