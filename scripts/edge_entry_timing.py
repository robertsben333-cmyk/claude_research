#!/usr/bin/env python3
"""Does it matter whether the book is bought at the close or three hours earlier?

`open` sends market-on-close orders, which is the entry `edge_resolve.py` scores and
the entry every headline number in `docs/EDGE_ANALYSIS.md` was measured at. A plain
market order the moment the hunt finishes -- about 13:00 New York on a 16:04 Amsterdam
run -- is simpler: no cutoff to beat, nothing left pending into the auction.

Both entries have already been measured on the same events, which is the only reason
this question has an answer rather than an opinion:

  close  ->  next close   docs/edge-rows.json, the `move` edge_resolve.py computes
  14:00  ->  next close   docs/edge-direction.json, the scheme claude_naive priced

14:00 is an hour later than the hunt typically finishes, so it flatters the market
order slightly. Both are the same exit.

    python3 scripts/edge_entry_timing.py
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
MIN_DV = float(_ex["benchmark"]["min_dollar_volume_usd"])


def binom_ge(k, n):
    return sum(comb(n, i) * 0.5 ** n for i in range(k, n + 1))


def block(label, rets):
    hits = sum(1 for x in rets if x > 0)
    m = st.mean(rets)
    sd = st.stdev(rets) if len(rets) > 1 else 0.0
    t = m / (sd / math.sqrt(len(rets))) if sd else float("nan")
    print(f"{label:28s}{f'{hits}/{len(rets)}':>10s}"
          f"{binom_ge(hits, len(rets)):>9.3f}{m:>+11.2f}{sd:>8.2f}{t:>6.2f}")
    return m


# close-to-close, de-duplicated by (ticker, event_date, session)
seen, cc = set(), {}
for day in sorted(json.loads(Path("docs/edge-rows.json").read_text()),
                  key=lambda d: d[0]["run"]):
    for r in day:
        b = json.loads((Path(r["run"]) / "baselines" / f"{r['t']}.json").read_text())
        key = (r["t"], b.get("event_date"), b.get("session"))
        if key in seen:
            continue
        seen.add(key)
        cc[key] = {"move": r["move"], "pred": r["impact_sum"],
                   "dv": r.get("dollar_vol") or 0}

# 14:00 ET entry, same events
mkt = {(r["t"], r["event"], r["sess"]): r
       for r in json.loads(Path("docs/edge-direction.json").read_text())["rows"]}

both = [(k, cc[k], mkt[k]) for k in cc if k in mkt]
sel = [(k, c, m) for k, c, m in both
       if abs(c["pred"]) >= FLOOR and c["dv"] >= MIN_DV]
print(f"{len(both)} events measured both ways, {len(sel)} of them traded at "
      f"|impact_sum| >= {FLOOR} and turnover >= ${MIN_DV/1e6:.2f}m\n")

print(f"{'entry':28s}{'direction':>10s}{'binom p':>9s}{'ret/trade':>11s}"
      f"{'sd':>8s}{'t':>6s}")
a = block("market-on-close", [(1 if c["pred"] > 0 else -1) * c["move"] for _, c, _ in sel])
b = block("market at 14:00 ET", [(1 if c["pred"] > 0 else -1) * m["rc"]
                                 for _, c, m in sel])
print(f"\nthe market order gives up {a - b:+.2f} points per trade against the close.")

drift = [(1 if c["pred"] > 0 else -1) * (m["rc"] - c["move"]) for _, c, m in sel]
print(f"per-event difference: median {st.median(drift):+.2f}, "
      f"mean {st.mean(drift):+.2f}, worst {min(drift):+.2f} / {max(drift):+.2f}")
flips = [(k[0], k[1]) for (k, c, m), d in zip(sel, drift)
         if ((1 if c['pred'] > 0 else -1) * c['move'] > 0) !=
            ((1 if c['pred'] > 0 else -1) * m['rc'] > 0)]
print(f"events whose sign flips between the two entries: {len(flips)}"
      + (f" — {', '.join(t + ' ' + d for t, d in flips)}" if flips else ""))
