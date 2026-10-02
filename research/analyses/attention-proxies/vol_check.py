#!/usr/bin/env python3
"""Is retail tilt an attention measure or a volatility measure? Run after collect.py.

    python3 research/analyses/attention-proxies/vol_check.py [strategy|close]
"""
import sys
import statistics as st
sys.argv = sys.argv[:2]
import evaluate as E  # noqa: E402

rs, floor = E.rows()
for label, g in (("BOOK", [r for r in rs if r["book"]]), ("ALL", rs)):
    g = [r for r in g if r.get("realised_vol_20d") is not None and r.get("retail_tilt") is not None]
    vol, rt = E.rank([r["realised_vol_20d"] for r in g]), E.rank([r["retail_tilt"] for r in g])
    hit, ret = E.rank([r["hit"] for r in g]), E.rank([r["ret"] for r in g])
    print(f"\n{label} n={len(g)}")
    print(f"  rho(volatility, hit) {E.pearson(vol, hit):+.3f}   rho(volatility, ret) {E.pearson(vol, ret):+.3f}")
    print(f"  rho(retail tilt, hit) {E.pearson(rt, hit):+.3f}   rho(retail tilt, ret) {E.pearson(rt, ret):+.3f}")
    # retail tilt with volatility regressed out of its rank
    b = sum((a - st.fmean(vol)) * (c - st.fmean(rt)) for a, c in zip(vol, rt)) / sum((a - st.fmean(vol)) ** 2 for a in vol)
    resid = [c - b * a for a, c in zip(vol, rt)]
    print(f"  retail tilt net of volatility: rho hit {E.pearson(E.rank(resid), hit):+.3f}, ret {E.pearson(E.rank(resid), ret):+.3f}")
    # the four parts one at a time
    for part in ("churn", "small_cap", "low_price", "volatility"):
        pass
    med = sorted(r["realised_vol_20d"] for r in g)[len(g) // 2]
    for name, sub in (("vol high", [r for r in g if r["realised_vol_20d"] >= med]),
                      ("vol low", [r for r in g if r["realised_vol_20d"] < med])):
        print(f"  {name:9s} n={len(sub):3d} hit {100*st.fmean(r['hit'] for r in sub):5.1f}%  ret {st.fmean(r['ret'] for r in sub):+.2f}%")
