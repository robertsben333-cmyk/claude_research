#!/usr/bin/env python3
"""Phase 0. Every big one-day faller in the listed US market, with what happened next.

This runs BEFORE any agent exists, deliberately. The reversal stage is only worth
building if the thing it would research has a measurable base rate that a free
one-line screen does not already capture, and that question costs bars and no
tokens. `CLAUDE.md` is largely a record of what the other order costs.

WHAT A ROW IS
-------------
One (ticker, drop date) pair whose adjusted close-to-close return cleared a loose
pre-filter, carrying: how it fell (gap against intraday), how much it normally
trades, what it had done before, an estimated half-spread, and the forward return
to seven horizons. Nothing here is a prediction and nothing is ranked; the ranking
and the floors belong to rev_backtest.py, so they can be swept rather than baked in.

THE PRE-FILTER IS HALF THE REAL FLOOR IN EVERY DIMENSION
--------------------------------------------------------
Rows are kept at ret <= -4%, median 20-day dollar volume >= $100k and price >= $0.50,
against a live screen at -X%, $200k and $1. Half in each direction, so the floors
stay sweepable in both and the file does not grow to the whole market. Per-date
counts of the FULL cross-section are written beside the rows, so the part the
pre-filter removed is still countable.

    python3 researcher_reversal/scripts/rev_harvest.py --range 3y
    python3 researcher_reversal/scripts/rev_harvest.py --range 3y --limit 200 --out /tmp/x
"""
import argparse
import gzip
import json
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rev_market as M                                            # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "researcher_reversal" / "analysis"
FWD = [("open1", "open", 1), ("d1", "close", 1), ("d2", "close", 2),
       ("d3", "close", 3), ("d5", "close", 5), ("d10", "close", 10),
       ("d21", "close", 21)]
PRE_RET, PRE_DV, PRE_PX = -4.0, 100_000.0, 0.50


def pct(a, b):
    return None if not b else round((a / b - 1) * 100, 4)


def name_rows(t, b, meta):
    """Candidate rows for one name. `b` is adjusted daily bars, oldest first."""
    out, agg = [], []
    n = len(b)
    for i in range(1, n):
        prev, cur = b[i - 1], b[i]
        r = pct(cur["close"], prev["close"])
        if r is None:
            continue
        w20 = b[max(0, i - 20):i]                     # the 20 days BEFORE the drop
        dv = M.median([x["close"] * x["volume"] for x in w20]) or 0.0
        agg.append((cur["date"], r))
        if r > PRE_RET or dv < PRE_DV or cur["raw_close"] < PRE_PX:
            continue
        vol20 = M.median([x["volume"] for x in w20]) or 0.0
        gap = pct(cur["open"], prev["close"])
        row = {
            "ticker": t, "date": cur["date"],
            "sector": meta.get("sector"), "exchange": meta.get("exchange"),
            "market_cap_now": meta.get("market_cap"),
            "close": round(cur["close"], 4), "price": round(cur["raw_close"], 4),
            "ret_d_pct": r,
            "gap_pct": gap,
            "intraday_pct": pct(cur["close"], cur["open"]),
            "gap_share": (round(gap / r, 3) if (gap is not None and r) else None),
            "dollar_vol_d": round(cur["close"] * cur["volume"]),
            "dv_med20": round(dv),
            "vol_spike": (round(cur["volume"] / vol20, 2) if vol20 else None),
            "runup_5d_pct": pct(prev["close"], b[i - 6]["close"]) if i >= 6 else None,
            "runup_20d_pct": pct(prev["close"], b[i - 21]["close"]) if i >= 21 else None,
            "runup_60d_pct": pct(prev["close"], b[i - 61]["close"]) if i >= 61 else None,
            "half_spread_pct": M.half_spread_pct(b[max(0, i - 21):i]),
            "half_spread_incl_d_pct": M.half_spread_pct(b[max(0, i - 21):i + 1]),
        }
        w52 = b[max(0, i - 252):i + 1]
        hi = max(x["high"] for x in w52)
        lo = min(x["low"] for x in w52)
        row["pos_52w"] = round((cur["close"] - lo) / (hi - lo), 3) if hi > lo else None
        tr = []
        for j in range(max(1, i - 13), i + 1):
            p, c = b[j - 1], b[j]
            tr.append(max(c["high"] - c["low"], abs(c["high"] - p["close"]),
                          abs(p["close"] - c["low"])))
        row["atr14_pct"] = (round(100 * M.mean(tr) / cur["close"], 3)
                            if tr and cur["close"] else None)
        for key, field, k in FWD:
            j = i + k
            row["fwd_" + key] = pct(b[j][field], cur["close"]) if j < n else None
        row["fwd_last_date"] = b[min(n - 1, i + 21)]["date"]
        out.append(row)
    return out, agg


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--range", default="3y", help="Yahoo range: 1y, 2y, 3y, 5y")
    ap.add_argument("--limit", type=int, help="first N tickers only (a smoke run)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()

    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    uni = M.screener()
    if a.limit:
        uni = uni[:a.limit]
    meta = {u["ticker"]: u for u in uni}
    tickers = [u["ticker"] for u in uni]
    print(f"universe {len(tickers)} names, range {a.range}", file=sys.stderr)

    # Rows are streamed to disk as they are produced. Holding 400k dicts in memory
    # to sort them at the end costs the best part of a gigabyte for no gain: the
    # file is read back by date anyway, and rev_backtest.py groups it itself.
    cross, empty = defaultdict(list), []
    lock = threading.Lock()
    t0 = time.time()
    state = {"rows": 0}
    path = outdir / "drops.jsonl.gz"
    fh = gzip.open(path, "wt")

    def sink(done, total, t, b):
        with lock:
            if not b:
                empty.append(t)
            else:
                r, agg = name_rows(t, b, meta.get(t, {}))
                for row in r:
                    fh.write(json.dumps(row, separators=(",", ":")) + "\n")
                state["rows"] += len(r)
                for d, ret in agg:
                    cross[d].append(ret)
            if done % 250 == 0 or done == total:
                el = time.time() - t0
                print(f"  {done}/{total} names, {state['rows']} rows, "
                      f"{len(empty)} empty, {el:.0f}s", file=sys.stderr)

    M.bars_many(tickers, rg=a.range, workers=a.workers, on_done=sink)
    fh.close()

    days = {}
    for d, rets in cross.items():
        rets.sort()
        days[d] = {
            "n_names": len(rets),
            "median_ret_pct": round(M.median(rets), 3),
            "p01_ret_pct": round(rets[max(0, int(len(rets) * 0.01))], 3),
            "n_below_5": sum(1 for r in rets if r <= -5),
            "n_below_10": sum(1 for r in rets if r <= -10),
            "n_below_20": sum(1 for r in rets if r <= -20),
        }
    (outdir / "cross-section.json").write_text(json.dumps({
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "range": a.range, "universe": len(tickers),
        "empty_charts": len(empty),
        "pre_filter": {"ret_pct_max": PRE_RET, "dv_med20_min": PRE_DV,
                       "price_min": PRE_PX},
        "days": dict(sorted(days.items())),
    }, indent=1))
    print(f"wrote {state['rows']} rows over {len(days)} sessions -> {path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
