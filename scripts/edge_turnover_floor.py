#!/usr/bin/env python3
"""What `execution.benchmark.min_dollar_volume_usd` does to the trade it screens.

Takes every event with |impact_sum| >= the conviction floor, trades its sign
close-before to close-after -- the window edge_resolve.py scores and the window
alpaca_trade.py places -- and reports the result at a range of turnover floors.
De-duplicated by (ticker, event_date, session), so 09-07's re-hunt of 09-04's prints
is not counted twice.

Read the table with the max-statistic warning in mind. Higher floors look better on
this sample and n is 38; choosing the floor that maximises the in-sample return is
the same move that put the ranking's own p at 0.056. Spread and events-per-day are
the arguments that do not come out of this table.

    python3 scripts/edge_turnover_floor.py
"""
import json
import math
import statistics as st
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alpaca_trade import config, execution_config       # noqa: E402

_ex = execution_config(config())
FLOOR = float(_ex["benchmark"]["min_conviction"])
EQUITY = float(_ex.get("assumed_equity_usd") or 100_000)
EQ_FRAC = float(_ex["sizing"]["max_position_pct_of_equity"]) / 100.0
ADV_FRAC = float(_ex["sizing"]["max_position_pct_of_adv"]) / 100.0
print(f"conviction floor {FLOOR}, equity ${EQUITY:,.0f}, "
      f"config floor now ${float(_ex['benchmark']['min_dollar_volume_usd'])/1e6:.2f}m")
days = json.loads(Path("docs/edge-rows.json").read_text())

seen, rows = set(), []
for d in sorted(days, key=lambda d: d[0]["run"]):
    for r in d:
        b = json.loads((Path(r["run"]) / "baselines" / f"{r['t']}.json").read_text())
        key = (r["t"], b.get("event_date"), b.get("session"))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"t": r["t"], "day": r["run"].split("/")[-2], "move": r["move"],
                     "pred": r["impact_sum"], "dv": r.get("dollar_vol") or 0,
                     "spot": r.get("spot")})

print(f"{len(rows)} de-duplicated events over "
      f"{len({r['day'] for r in rows})} days\n")


def binom_ge(k, n):
    return sum(comb(n, i) * 0.5 ** n for i in range(k, n + 1))


print(f"{'turnover floor':>15s}{'trades':>8s}{'names left':>12s}{'hits':>10s}"
      f"{'binom p':>9s}{'ret/trade':>11s}{'t':>6s}{'cum':>9s}{'always-short':>14s}")
for floor in (0, 200e3, 500e3, 1e6, 2e6, 5e6, 10e6):
    kept = [r for r in rows if r["dv"] >= floor]
    tr = [r for r in kept if abs(r["pred"]) >= FLOOR]
    if not tr:
        print(f"{floor/1e6:>14.2f}m{0:>8d}")
        continue
    rets = [(1 if r["pred"] > 0 else -1) * r["move"] for r in tr]
    hits = sum(1 for x in rets if x > 0)
    m = st.mean(rets)
    sd = st.stdev(rets) if len(rets) > 1 else 0.0
    t = m / (sd / math.sqrt(len(rets))) if sd else float("nan")
    cum = 1.0
    for x in rets:
        cum *= 1 + x / 100 * EQ_FRAC       # per-name weight from the config cap
    short_all = -st.mean([r["move"] for r in kept])
    print(f"{floor/1e6:>14.2f}m{len(tr):>8d}{len(kept):>12d}"
          f"{f'{hits}/{len(tr)}':>10s}{binom_ge(hits, len(tr)):>9.3f}"
          f"{m:>+11.2f}{t:>6.2f}{(cum-1)*100:>+8.1f}%{short_all:>+14.2f}")

print(f"\nwhat the {ADV_FRAC*100:.0f}%-of-turnover cap does to position size at "
      f"${EQUITY:,.0f} of equity")
print(f"(the {EQ_FRAC*100:.0f}% equity cap is ${EQ_FRAC*EQUITY:,.0f}, so anything "
      f"under ${EQ_FRAC*EQUITY/ADV_FRAC/1e3:,.0f}k/day of turnover is capacity-bound)")
for floor in (200e3, 500e3, 1e6, 5e6):
    print(f"  ${floor/1e6:>5.2f}m/day  ->  position capped at "
          f"${min(ADV_FRAC*floor, EQ_FRAC*EQUITY):>7,.0f}")

print("\nthe trades a $200k floor adds that a $5m floor refuses")
add = [r for r in rows if abs(r["pred"]) >= FLOOR and 200e3 <= r["dv"] < 5e6]
add.sort(key=lambda r: -abs(r["pred"]))
for r in add:
    side = "long " if r["pred"] > 0 else "short"
    got = (1 if r["pred"] > 0 else -1) * r["move"]
    print(f"  {r['day']}  {r['t']:6s}{side}  pred {r['pred']:+6.2f}  "
          f"move {r['move']:+7.2f}%  trade {got:+7.2f}%  "
          f"turnover ${r['dv']/1e6:.2f}m")
if add:
    g = [(1 if r["pred"] > 0 else -1) * r["move"] for r in add]
    print(f"  -> {sum(1 for x in g if x > 0)}/{len(g)} right, "
          f"mean {st.mean(g):+.2f}% per trade")
