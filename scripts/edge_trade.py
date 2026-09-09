#!/usr/bin/env python3
"""What would have happened to money placed on stage E's rankings.

Reads docs/edge-rows.json (written by edge_decompose.py) and runs the day's ranking
as a book. Entry is the close before the print and exit the close after the first
full session, the same window edge_resolve.py scores, so the print is held through.
The edge hunt fires at 16:04 CET, before that entry, so nothing here is look-ahead.

Every strategy is one unit of capital. The long/short books therefore split the
capital in half, and a day return is mean(long) / 2 - mean(short) / 2 rather than
the raw spread, which is 2x gross and flatters by exactly a factor of two.

Three things are reported beside the return, because on six days the return alone
says nothing:

  the null        `always short` needs no research at all, and this sample skewed
                  down (23 of 43 names fell, mean move -1.77%)
  costs           a flat charge per unit of capital per day, applied to every
                  strategy alike; these are small caps and 1.5% is not pessimistic
  capacity        spot x 20-day average volume for every position taken. A return
                  earned in a name that turns over $170k a day is not a return

    python3 scripts/edge_trade.py
    python3 scripts/edge_trade.py --cost 1.5 --min-dollar-vol 5e6
"""
import argparse
import json
import math
import random
import statistics as st
from math import comb
from pathlib import Path


def ls_third(day, key, sign=1):
    s = sorted([r for r in day if r.get(key) is not None], key=lambda r: -sign * r[key])
    k = max(1, len(s) // 3)
    long, short = s[:k], s[-k:]
    ret = (st.mean([r["move"] for r in long]) - st.mean([r["move"] for r in short])) / 2
    return ret, long, short


def ls_sign(day, key, sign=1):
    v = [r for r in day if r.get(key) is not None and sign * r[key] != 0]
    if not v:
        return 0.0, [], []
    long = [r for r in v if sign * r[key] > 0]
    short = [r for r in v if sign * r[key] < 0]
    ret = (sum(r["move"] for r in long) - sum(r["move"] for r in short)) / len(v)
    return ret, long, short


def always_short(day, *_):
    return -st.mean([r["move"] for r in day]), [], list(day)


def top1(day, key, sign=1):
    s = sorted([r for r in day if r.get(key) is not None], key=lambda r: -sign * r[key])
    return s[0]["move"], [s[0]], []


STRATEGIES = [
    ("edge_score L/S top-third", lambda d: ls_third(d, "escore")),
    ("impact sum L/S top-third", lambda d: ls_third(d, "impact_sum")),
    ("minus run-up L/S top-third", lambda d: ls_third(d, "runup", -1)),
    ("edge_score L/S on sign", lambda d: ls_sign(d, "escore")),
    ("always short (the null)", always_short),
    ("edge_score long the #1", lambda d: top1(d, "escore")),
]


def sign_test(k, n):
    p = [comb(n, i) / 2 ** n for i in range(n + 1)]
    return sum(x for x in p if x <= p[k] + 1e-12)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", default="docs/edge-rows.json")
    ap.add_argument("--cost", type=float, default=0.0,
                    help="percent per unit of capital per day, charged to every strategy")
    ap.add_argument("--min-dollar-vol", type=float, default=0.0,
                    help="drop names turning over less than this per day")
    ap.add_argument("--out")
    a = ap.parse_args()

    days = json.loads(Path(a.rows).read_text())
    if a.min_dollar_vol:
        days = [[r for r in d if (r.get("dollar_vol") or 0) >= a.min_dollar_vol]
                for d in days]
        days = [d for d in days if len(d) >= 3]
    flat = [r for d in days for r in d]
    print(f"{len(days)} days, {len(flat)} names, cost {a.cost:.2f}%/day, "
          f"min turnover ${a.min_dollar_vol/1e6:.1f}m")
    print(f"the sample itself: {sum(1 for r in flat if r['move'] > 0)} up, "
          f"{sum(1 for r in flat if r['move'] <= 0)} down, "
          f"mean move {st.mean([r['move'] for r in flat]):+.2f}%\n")

    print(f"{'strategy':30s}{'mean/day':>10s}{'sd':>7s}{'t':>6s}"
          f"{'bootstrap 95% CI':>20s}{'cumul':>8s}{'up days':>10s}")
    out = []
    for name, fn in STRATEGIES:
        rs, pos = [], []
        for d in days:
            r, long, short = fn(d)
            rs.append(r - a.cost)
            pos += long + short
        m, sd = st.mean(rs), (st.stdev(rs) if len(rs) > 1 else 0.0)
        t = m / (sd / math.sqrt(len(rs))) if sd else float("nan")
        random.seed(5)
        bs = sorted(st.mean([random.choice(rs) for _ in rs]) for _ in range(20000))
        lo, hi = bs[500], bs[19500]
        cum = 1.0
        for r in rs:
            cum *= 1 + r / 100
        up = sum(1 for x in rs if x > 0)
        dv = sorted((r.get("dollar_vol") or 0) for r in pos)
        row = {"strategy": name, "mean_pct_per_day": round(m, 2), "sd": round(sd, 2),
               "t": round(t, 2), "ci95": [round(lo, 2), round(hi, 2)],
               "cumulative_pct": round((cum - 1) * 100, 1),
               "up_days": up, "days": len(rs),
               "sign_test_p": round(sign_test(up, len(rs)), 3),
               "positions": len(pos),
               "median_turnover_usd": (round(st.median(dv)) if dv else None),
               "min_turnover_usd": (min(dv) if dv else None),
               "positions_under_1m": sum(1 for x in dv if x < 1e6)}
        out.append(row)
        print(f"{name:30s}{m:>+10.2f}{sd:>7.2f}{t:>6.2f}"
              f"{f'[{lo:+.2f}, {hi:+.2f}]':>20s}{(cum-1)*100:>+8.1f}"
              f"{f'{up}/{len(rs)} p={sign_test(up, len(rs)):.3f}':>10s}")

    print("\ncapacity of the positions each strategy actually took")
    for r in out:
        if r["median_turnover_usd"] is None:
            continue
        print(f"  {r['strategy']:30s}{r['positions']:>4d} positions, median "
              f"${r['median_turnover_usd']/1e6:>7.1f}m/day, smallest "
              f"${r['min_turnover_usd']/1e3:>7.0f}k/day, "
              f"{r['positions_under_1m']} under $1m")

    if a.out:
        Path(a.out).write_text(json.dumps(
            {"cost_pct_per_day": a.cost, "min_dollar_vol": a.min_dollar_vol,
             "days": len(days), "names": len(flat), "results": out}, indent=1) + "\n")
        print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
