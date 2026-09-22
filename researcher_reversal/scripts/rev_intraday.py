#!/usr/bin/env python3
"""What a 15:00 ET screen costs against the 16:00 close screen phase 0 measured.

WHY THIS HAD TO BE MEASURED BEFORE THE CLOCK MOVED
---------------------------------------------------
Stage R was built on close-to-close falls: `rev_harvest.py` ranks the day by the
adjusted close-to-close return and `rev_backtest.py`'s whole base-rate table enters at
the drop-day close. Firing at 21:00 CET means screening at **15:00 ET, one hour before
that close**, so two things change and neither was in phase 0:

  churn   the worst K at 15:00 is not the worst K at 16:00. Every name that swaps is a
          name the stage hunted for nothing, or missed.
  entry   the position goes on near 15:00 rather than at the close, so it carries the
          last hour of the drop day, which phase 0 never priced.

Both are measurable from 15-minute bars, which Yahoo serves for 60 days. Neither is
guessable, and a stage that moved its clock without measuring them would be asserting
that its own base rates still applied.

    python3 researcher_reversal/scripts/rev_intraday.py --drops <dir> --days 45 --k 15
"""
import argparse
import gzip
import json
import statistics
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_market as M                                            # noqa: E402

ET = ZoneInfo("America/New_York")
CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/{t}"
         "?interval=15m&range=60d")
CUT_HHMM = (15, 0)          # the screen instant the 21:00 CET fire implies


def intraday(ticker):
    """{date: {"at_cut": px, "close": px, "prev_close": px}} from 15-minute bars.

    Regular session only. `prev_close` is the last regular bar of the previous session
    in the same series, so the fall measured here is on one consistent price source and
    is directly comparable with the daily-bar fall the harvest recorded.
    """
    try:
        raw = M.get(CHART.format(t=M.yahoo_symbol(ticker)), tries=2)
        d = json.loads(raw)
    except Exception:                                             # noqa: BLE001
        return {}
    res = ((d.get("chart") or {}).get("result") or [None])[0]
    if not res:
        return {}
    ts = res.get("timestamp") or []
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    closes = q.get("close") or []
    by_day = defaultdict(list)
    for i, t in enumerate(ts):
        c = closes[i] if i < len(closes) else None
        if c is None:
            continue
        dt = datetime.fromtimestamp(t, ET)
        if (dt.hour, dt.minute) < (9, 30) or (dt.hour, dt.minute) >= (16, 0):
            continue
        by_day[dt.date().isoformat()].append((dt.hour, dt.minute, c))
    out, days = {}, sorted(by_day)
    for n, day in enumerate(days):
        rows = sorted(by_day[day])
        at_cut = None
        for h, m, c in rows:
            if (h, m) <= CUT_HHMM:
                at_cut = c
        prev = None
        if n:
            pr = sorted(by_day[days[n - 1]])
            prev = pr[-1][2] if pr else None
        out[day] = {"at_cut": at_cut, "close": rows[-1][2], "prev_close": prev,
                    "bars": len(rows)}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drops", required=True)
    ap.add_argument("--days", type=int, default=45, help="most recent sessions to use")
    ap.add_argument("--k", type=int, default=15)
    ap.add_argument("--dv", type=float, default=200_000)
    ap.add_argument("--price", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("-o", "--out",
                    default="researcher_reversal/analysis/intraday-cut.json")
    a = ap.parse_args()

    # Candidates: every row that could have made the worst K, on the recent sessions.
    rows = []
    with gzip.open(Path(a.drops) / "drops.jsonl.gz", "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if r["dv_med20"] >= a.dv and r["price"] >= a.price:
                rows.append(r)
    dates = sorted({r["date"] for r in rows})[-a.days:]
    keep = set(dates)
    rows = [r for r in rows if r["date"] in keep]
    tickers = sorted({r["ticker"] for r in rows})
    print(f"{len(rows)} candidate rows over {len(dates)} sessions, "
          f"{len(tickers)} unique tickers", file=sys.stderr)

    bars, lock = {}, __import__("threading").Lock()
    idx = [0]

    def work():
        while True:
            with lock:
                if idx[0] >= len(tickers):
                    return
                t = tickers[idx[0]]; idx[0] += 1
            b = intraday(t)
            time.sleep(0.05)
            with lock:
                bars[t] = b
                if len(bars) % 200 == 0:
                    print(f"  {len(bars)}/{len(tickers)}", file=sys.stderr)

    ths = [__import__("threading").Thread(target=work, daemon=True)
           for _ in range(a.workers)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()

    per_day, entry_moves, churn = {}, [], []
    for d in dates:
        day_rows = [r for r in rows if r["date"] == d]
        cut, fin = [], []
        for r in day_rows:
            b = (bars.get(r["ticker"]) or {}).get(d) or {}
            if not b.get("at_cut") or not b.get("close") or not b.get("prev_close"):
                continue
            fall_cut = (b["at_cut"] / b["prev_close"] - 1) * 100
            fall_close = (b["close"] / b["prev_close"] - 1) * 100
            cut.append((fall_cut, r["ticker"]))
            fin.append((fall_close, r["ticker"]))
        if len(cut) < a.k + 3:
            continue
        cut.sort(); fin.sort()
        top_cut = [t for _, t in cut[:a.k]]
        top_fin = [t for _, t in fin[:a.k]]
        overlap = len(set(top_cut) & set(top_fin))
        churn.append(overlap)
        for t in top_cut:
            b = bars[t][d]
            entry_moves.append(round((b["close"] / b["at_cut"] - 1) * 100, 4))
        per_day[d] = {"candidates": len(cut), "overlap_of_k": overlap,
                      "kept_pct": round(100 * overlap / a.k, 1)}

    em = [x for x in entry_moves if x is not None]
    doc = {
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cut_et": f"{CUT_HHMM[0]:02d}:{CUT_HHMM[1]:02d}",
        "sessions_measured": len(per_day),
        "k": a.k,
        "churn": {
            "note": "how many of the worst K at 15:00 ET are still the worst K at the "
                    "close. Every name that swaps is one the stage hunted for nothing, "
                    "or missed",
            "mean_kept": round(M.mean(churn), 2) if churn else None,
            "mean_kept_pct": round(100 * M.mean(churn) / a.k, 1) if churn else None,
            "min_kept": min(churn) if churn else None,
            "max_kept": max(churn) if churn else None,
        },
        "last_hour_move_of_the_screened_names": {
            "note": "15:00 ET to the close, on the names the 15:00 screen picks. A "
                    "SHORT entered at 15:00 earns minus this; a long earns it",
            "n": len(em),
            "mean_pct": round(M.mean(em), 3) if em else None,
            "median_pct": round(statistics.median(em), 3) if em else None,
            "stdev_pct": round(M.stdev(em), 3) if em else None,
            "share_falling_further_pct": (round(100 * sum(1 for x in em if x < 0) / len(em), 1)
                                          if em else None),
        },
        "per_day": per_day,
    }
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(json.dumps({k: doc[k] for k in
                      ("sessions_measured", "churn",
                       "last_hour_move_of_the_screened_names")}, indent=1))


if __name__ == "__main__":
    main()
