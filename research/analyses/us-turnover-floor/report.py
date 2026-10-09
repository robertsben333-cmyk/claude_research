#!/usr/bin/env python3
"""Tables for README.md, from event-liquidity.json (written by measure.py).

    python3 research/analyses/us-turnover-floor/report.py
"""
import json
import math
import statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = json.loads((HERE / "event-liquidity.json").read_text())
EQUITY = 11_200          # paper account equity on 2026-10-09
BANDS = [(0, 2e5, "<200k"), (2e5, 1e6, "200k-1m"), (1e6, 5e6, "1-5m"),
         (5e6, 25e6, "5-25m"), (25e6, 1e13, ">25m")]


def q(v, p):
    v = sorted(v)
    return v[int(p * (len(v) - 1))]


def corr(x, y):
    mx, my = st.mean(x), st.mean(y)
    return (sum((a - mx) * (b - my) for a, b in zip(x, y))
            / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)))


def sgn(x):
    return (x > 0) - (x < 0)


print(f"{len(rows)} hunted US events, 20-day average turnover as alpaca_trade.py reads it\n")
print(f"{'band':9}{'n':>4}{'react x':>9}{'p25':>6}{'p75':>6}{'entry x':>9}"
      f"{'next x':>8}{'CS half %':>10}{'|move| %':>10}")
for lo, hi, lab in BANDS:
    b = [r for r in rows if lo <= r["adv20_avg"] < hi]
    rx = [r["react_x_avg"] for r in b]
    ax = [r["after_x_avg"] for r in b if r["after_x_avg"]]
    cs = [r["cs_half_spread_pre_pct"] for r in b if r["cs_half_spread_pre_pct"] is not None]
    mv = [r["abs_move_close"] for r in b if r["abs_move_close"] is not None]
    print(f"{lab:9}{len(b):>4}{st.median(rx):>9.1f}{q(rx, .25):>6.1f}{q(rx, .75):>6.1f}"
          f"{st.median(r['entry_x_avg'] for r in b):>9.2f}{st.median(ax):>8.2f}"
          f"{st.median(cs):>10.2f}{st.median(mv):>10.2f}")
for s in ("amc", "bmo"):
    b = [r for r in rows if r["session"] == s]
    print(f"  {s}: n {len(b)}, reaction day x{st.median(r['react_x_avg'] for r in b):.2f}, "
          f"entry day x{st.median(r['entry_x_avg'] for r in b):.2f}")

lx = [math.log(r["adv20_avg"]) for r in rows]
print(f"\ncorr(log ADV, log reaction-day turnover)  {corr(lx, [math.log(r['react_dv']) for r in rows]):+.3f}")
print(f"corr(log ADV, log reaction multiple)       {corr(lx, [math.log(r['react_x_avg']) for r in rows]):+.3f}")
b = [r for r in rows if r["abs_move_close"]]
print(f"corr(log reaction multiple, |move|)        "
      f"{corr([math.log(r['react_x_avg']) for r in b], [r['abs_move_close'] for r in b]):+.3f}")

print("\nnames kept by a floor on each measure")
for lab, key in (("20d average (live)", "adv20_avg"), ("20d median", "adv20_med"),
                 ("entry day", "entry_dv"), ("reaction day", "react_dv")):
    print(f"  {lab:20} >=$200k {sum(r[key] >= 2e5 for r in rows):>3}/{len(rows)}   "
          f">=$1m {sum(r[key] >= 1e6 for r in rows):>3}")
for f in (5e4, 1e5, 2e5, 5e5, 1e6):
    print(f"  20d average >= ${f/1e3:>5.0f}k keeps {sum(r['adv20_avg'] >= f for r in rows)}")

low = [r for r in rows if r["adv20_avg"] < 2e5]
print(f"\nbelow the floor ({len(low)}): entry day >= $200k {sum(r['entry_dv'] >= 2e5 for r in low)}, "
      f"reaction day >= $200k {sum(r['react_dv'] >= 2e5 for r in low)}")
for lab, b in (("<200k", low), ("200k-1m", [r for r in rows if 2e5 <= r["adv20_avg"] < 1e6])):
    for cap in (0.33, 0.50):
        pos = cap * EQUITY
        pe = [100 * pos / (0.5 * r["entry_dv"]) for r in b]   # ~half the day gone by 13:30 ET
        pr = [100 * pos / r["react_dv"] for r in b]
        print(f"  {lab:8} position ${pos:,.0f}: share of entry-day volume to 13:30 ET "
              f"median {st.median(pe):.1f}% (max {max(pe):.0f}%), of reaction day {st.median(pr):.1f}%")
for cap in (0.33, 0.50):
    thr = cap * EQUITY / 0.01
    print(f"  1%-of-ADV cap at a {cap:.0%} equity cap binds below ${thr/1e3:.0f}k: "
          f"{sum(2e5 <= r['adv20_avg'] < thr for r in rows)} names above the floor sized down")

print("\n|impact_sum| >= 2.8, signed return at the strategy exit")
for lo, hi, lab in BANDS + [(2e5, 1e13, ">=200k")]:
    b = [r for r in rows if lo <= r["adv20_avg"] < hi and (r["conviction"] or 0) >= 2.8
         and r["ret_strategy"] is not None and r["impact_sum"]]
    s = [sgn(r["impact_sum"]) * r["ret_strategy"] for r in b]
    t = st.mean(s) / (st.stdev(s) / math.sqrt(len(s)))
    print(f"  {lab:8} n {len(s):>3}  right {sum(x > 0 for x in s):>2}/{len(s):<3} "
          f"mean {st.mean(s):+6.2f}%  median {st.median(s):+6.2f}%  t {t:+.2f}")
