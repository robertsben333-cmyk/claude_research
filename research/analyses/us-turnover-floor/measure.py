#!/usr/bin/env python3
"""Event-day liquidity against the 20-day average the $200k floor reads."""
import json, sys, statistics as st, time
from pathlib import Path

sys.path.insert(0, "researcher_us/scripts")
sys.path.insert(0, "researcher_reversal/scripts")
import priced_in as p
from rev_market import corwin_schultz

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
L = json.load(open("dashboard/data/ledger.json"))
names = [n for n in L["names"] if not n.get("duplicate_event")]
cache_f = OUT / "bars.json"
cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}

for t in sorted({n["ticker"] for n in names}):
    if t in cache:
        continue
    try:
        j = p.get_json(f"{p.YQ}/v8/finance/chart/{p.yahoo_symbol(t)}?range=250d&interval=1d")
        r = j["chart"]["result"][0]; q = r["indicators"]["quote"][0]
        rows = []
        for i, ts in enumerate(r["timestamp"]):
            if q["close"][i] is None:
                continue
            rows.append({"date":
                         time.strftime("%Y-%m-%d", time.gmtime(ts)),
                         "open": q["open"][i], "high": q["high"][i], "low": q["low"][i],
                         "close": q["close"][i], "volume": q["volume"][i] or 0})
        cache[t] = rows
    except Exception as e:
        cache[t] = {"error": repr(e)[:200]}
    time.sleep(0.15)
cache_f.write_text(json.dumps(cache))   # bars.json is not checked in (6 MB)

out = []
for n in names:
    bars = cache.get(n["ticker"])
    if not isinstance(bars, list):
        continue
    idx = {b["date"]: i for i, b in enumerate(bars)}
    ed, rd = n.get("entry_date"), n.get("reaction_date")
    if ed not in idx or rd not in idx:
        continue
    ie, ir = idx[ed], idx[rd]
    pre = bars[max(0, ie - 20):ie]            # 20 sessions before the entry day
    if len(pre) < 15:
        continue
    dv = lambda b: b["close"] * b["volume"]
    adv_avg = pre[-1]["close"] * st.mean(b["volume"] for b in pre)   # alpaca_trade's definition
    adv_med = st.median(dv(b) for b in pre)
    react = dv(bars[ir])
    after = dv(bars[ir + 1]) if ir + 1 < len(bars) else None
    cs_pre = corwin_schultz(pre)
    out.append({
        "ticker": n["ticker"], "run_date": n["run_date"], "session": n["session"],
        "conviction": n.get("conviction"), "impact_sum": n.get("impact_sum"),
        "ret_strategy": n.get("ret_strategy"), "ret_close": n.get("ret_close"),
        "traded": n.get("traded"), "pending": n.get("pending"),
        "adv20_avg": adv_avg, "adv20_med": adv_med,
        "entry_dv": dv(bars[ie]), "react_dv": react, "after_dv": after,
        "react_x_avg": react / adv_avg if adv_avg else None,
        "react_x_med": react / adv_med if adv_med else None,
        "entry_x_avg": dv(bars[ie]) / adv_avg if adv_avg else None,
        "after_x_avg": after / adv_avg if (after and adv_avg) else None,
        "zero_vol_days_pre": sum(1 for b in pre if b["volume"] == 0),
        "cs_half_spread_pre_pct": None if cs_pre is None else cs_pre * 50,
        "abs_move_close": abs(n["ret_close"]) if n.get("ret_close") is not None else None,
    })
(OUT / "event-liquidity.json").write_text(json.dumps(out, indent=1))
print(len(names), "names,", len(out), "measured,",
      sum(1 for v in cache.values() if not isinstance(v, list)), "fetch errors")
