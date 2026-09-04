#!/usr/bin/env python3
"""Every company reporting on an explicit date and session, with no size floor.

Deliberately not `get_earnings.py`. That script resolves the *actionable window*
for the daily advice pipeline and filters at a $500m cap, which is right for
advice and wrong here. `backtest/FINDINGS.md` §27 measured news coverage as a
near-monotonic function of market cap and found 20% of a random draw had no
usable news at all -- so the small names are not noise to be filtered out, they
are the part of the distribution the hunt most needs to be tested on. A hunt that
only ever runs on names with deep coverage is measuring market cap.

Nasdaq's calendar carries an explicit session for future dates. Rows stamped
`time-not-supplied` are kept and marked, because for a bmo run they may or may
not be in the window and that is a fact about the day rather than a bug.

    python3 scripts/edge_universe.py --date 2026-08-31 --session bmo
    python3 scripts/edge_universe.py --date 2026-09-01 --session amc -o universe.json
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from get_earnings import next_trading_day    # NYSE calendar, holidays included

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SESSION = {"time-pre-market": "bmo", "time-after-hours": "amc",
           "time-not-supplied": "unknown"}


def money(s):
    if not s:
        return None
    n = re.sub(r"[^0-9.]", "", str(s))
    try:
        return float(n)
    except ValueError:
        return None


def fetch(d):
    u = f"https://api.nasdaq.com/api/calendar/earnings?date={d}"
    r = urllib.request.urlopen(urllib.request.Request(
        u, headers={"User-Agent": UA, "Accept": "application/json"}), timeout=30)
    return ((json.loads(r.read()).get("data") or {}).get("rows") or [])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="event date YYYY-MM-DD")
    ap.add_argument("--session", default="bmo", choices=["bmo", "amc", "all"])
    ap.add_argument("--window", action="store_true",
                    help="the pipeline's actual window: today's amc plus the next "
                         "trading day's bmo, merged. What a daily routine wants.")
    ap.add_argument("--include-unknown", action="store_true",
                    help="also take rows Nasdaq left as time-not-supplied")
    ap.add_argument("--min-market-cap", type=float, default=0.0)
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    if a.window:
        today = date.fromisoformat(a.date) if a.date else date.today()
        # Skipping only the weekend resolved the Friday before Labor Day 2026
        # (09-04) to Monday 09-07, a closed market: 19 calendar rows, zero in
        # the window. `get_earnings.py` already knows the NYSE calendar.
        nxt = next_trading_day(today)
        plan = [(today.isoformat(), "amc"), (nxt.isoformat(), "bmo")]
    elif a.date:
        plan = [(a.date, a.session)]
    else:
        sys.exit("give --date or --window")

    rows, out = [], []
    for d, want in plan:
        day_rows = fetch(d)
        rows.extend(day_rows)
        for r in day_rows:
            sess = SESSION.get(r.get("time"), "unknown")
            cap = money(r.get("marketCap"))
            if want != "all" and sess != want:
                if not (sess == "unknown" and a.include_unknown):
                    continue
            if cap is not None and cap < a.min_market_cap:
                continue
            out.append({
                "ticker": r.get("symbol"),
                "company": (r.get("name") or "").strip(),
                "event_date": d,
                "session": sess,
                "session_source": "nasdaq calendar" if sess != "unknown" else "unresolved",
                "market_cap_usd": cap,
                "eps_forecast": r.get("epsForecast") or None,
                "n_estimates": r.get("noOfEsts") or None,
                "last_year_eps": r.get("lastYearEPS") or None,
            })
    out.sort(key=lambda x: -(x["market_cap_usd"] or 0))

    doc = {
        "event_date": a.date or plan[0][0],
        "window": [{"date": d, "session": s} for d, s in plan] if a.window else None,
        "session_filter": "window" if a.window else a.session,
        "resolved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "api.nasdaq.com/api/calendar/earnings",
        "rows_on_calendar": len(rows),
        "count": len(out),
        "unknown_session_included": a.include_unknown,
        "unknown_session_count": sum(1 for x in out if x["session"] == "unknown"),
        "note": "no market-cap floor by default. Small names are the part of the "
                "distribution the hunt most needs testing on, not noise to filter.",
        "names": out,
    }
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    label = " + ".join(f"{d} {s}" for d, s in plan)
    print(f"{label}: {len(out)} of {len(rows)} calendar rows"
          f" ({doc['unknown_session_count']} unresolved session)")
    for x in out:
        cap = f"${x['market_cap_usd']/1e9:.2f}bn" if x["market_cap_usd"] else "cap n/a"
        print(f"  {x['ticker']:8s}{x['event_date']} {x['session']:9s}{cap:>12s}  "
              f"est={x['eps_forecast'] or '-':>8s} nEst={x['n_estimates'] or '-'}  "
              f"{x['company'][:36]}")
    print(",".join(x["ticker"] for x in out))
    if a.out:
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
