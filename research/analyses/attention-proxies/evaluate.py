#!/usr/bin/env python3
"""Do better attention proxies predict where the hunt is right?

Run from the repo root after collect.py:

    python3 research/analyses/attention-proxies/evaluate.py [strategy|close]

THE DESIGN WAS FIXED BEFORE ANY RESULT WAS READ (2026-10-02):
  * every proxy is oriented so that HIGHER = MORE ATTENTION;
  * the theory says the hunt finds what the price has not taken in, so it should do
    better where attention is LOW: the predicted sign of rho(attention, outcome) is
    negative;
  * three outcomes, as on the dashboard: hit (sign right), the signed return, and
    |move|. A proxy that only predicts |move| is a volatility measure;
  * two populations: the book (|impact_sum| >= floor) and every name;
  * Spearman rho with a permutation p that shuffles outcomes WITHIN days, 4000 times,
    and a family-wise p from the max |rho| over all proxies under the same shuffles;
  * two composites declared up front, as the mean percentile of their parts:
      structural  n_estimates, market cap, dollar volume, option OI/volume,
                  Wikipedia median views (no article = lowest), StockTwits watchers
      momentary   abnormal volume 5d, Wikipedia 3-day spike, Google search spike,
                  |5-day run-up|
"""
import json
import math
import random
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXIT = sys.argv[1] if len(sys.argv) > 1 else "strategy"
PERMS = 4000
random.seed(20261002)

# (key, label, orientation: +1 when a larger value means more attention)
PROXIES = [
    ("n_estimates", "analyst estimates (count)", +1),
    ("market_cap_usd", "market cap", +1),
    ("dollar_vol", "dollar volume 20d", +1),
    ("has_options", "has a usable option chain", +1),
    ("oi_to_volume", "option open interest / share volume", +1),
    ("option_spread", "ATM option spread (wide = less)", -1),
    ("pct_from_52w_high", "closeness to 52-week high", +1),
    ("abs_runup_5d", "|5-day run-up|", +1),
    ("abnormal_volume_5d", "abnormal volume, 5d vs 60d", +1),
    ("has_wikipedia", "has an English Wikipedia article", +1),
    ("wiki_views_median", "Wikipedia views, 90d median", +1),
    ("wiki_spike_3d", "Wikipedia 3-day spike", +1),
    ("stocktwits_watchers_now", "StockTwits watchers (today's snapshot)", +1),
    ("search_spike", "Google search spike (existing)", +1),
    ("retail_tilt", "retail tilt (existing, high = less institutional)", -1),
    ("hunt_sources", "sources the hunter cited", +1),
    ("structural", "COMPOSITE structural attention", +1),
    ("momentary", "COMPOSITE momentary attention", +1),
]
STRUCTURAL = ["n_estimates", "market_cap_usd", "dollar_vol", "oi_to_volume",
              "wiki_views_median_or_zero", "stocktwits_watchers_now"]
MOMENTARY = ["abnormal_volume_5d", "wiki_spike_3d", "search_spike", "abs_runup_5d"]


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def rows():
    led = load(REPO / "dashboard" / "data" / "ledger.json")
    floor = led.get("conviction_floor", 2.8)
    prox = {(p["run"], p["ticker"]): p for p in load(HERE / "proxies.json")}
    out = []
    for r in led["names"]:
        if r.get("duplicate_event") or not r.get("impact_sum") or r.get("ret_" + EXIT) is None:
            continue
        p = dict(prox.get((r["run"], r["ticker"]), {}))
        for k in ("market_cap_usd", "dollar_vol", "retail_tilt", "realised_vol_20d"):
            p[k] = r.get(k)
        p["search_spike"] = r.get("search_spike") if r.get("search_state") == "measured" else None
        p["wiki_views_median_or_zero"] = (p.get("wiki_views_median")
                                          if p.get("wiki_views_median") is not None
                                          else (0.0 if p.get("has_wikipedia") is False else None))
        for k in ("has_options", "has_wikipedia"):
            if p.get(k) is not None:
                p[k] = 1.0 if p[k] else 0.0
        mv = r["mv_" + EXIT]
        out.append({**p, "day": r["run"], "ticker": r["ticker"],
                    "book": abs(r["impact_sum"]) >= floor,
                    "hit": 1.0 if (r["impact_sum"] > 0) == (mv > 0) else 0.0,
                    "ret": r["ret_" + EXIT], "absmv": abs(mv)})
    composite(out, "structural", STRUCTURAL)
    composite(out, "momentary", MOMENTARY)
    return out, floor


def composite(rs, name, parts):
    ranks = {}
    for k in parts:
        vals = sorted(r[k] for r in rs if r.get(k) is not None)
        for r in rs:
            if r.get(k) is not None:
                ranks.setdefault(id(r), []).append(
                    100 * sum(1 for v in vals if v < r[k]) / max(1, len(vals) - 1))
    for r in rs:
        v = ranks.get(id(r), [])
        r[name] = st.fmean(v) if len(v) >= max(2, len(parts) // 2) else None


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def pearson(a, b):
    ma, mb = st.fmean(a), st.fmean(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return 0.0 if not sa or not sb else sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def within_day_shuffles(rs):
    idx_by_day = {}
    for i, r in enumerate(rs):
        idx_by_day.setdefault(r["day"], []).append(i)
    out = []
    for _ in range(PERMS):
        perm = list(range(len(rs)))
        for ids in idx_by_day.values():
            sh = ids[:]
            random.shuffle(sh)
            for a, b in zip(ids, sh):
                perm[a] = b
        out.append(perm)
    return out


def evaluate(rs, label):
    shuffles = within_day_shuffles(rs)
    res, null_max = [], [0.0] * PERMS
    for key, name, orient in PROXIES:
        ids = [i for i, r in enumerate(rs) if r.get(key) is not None]
        if len(ids) < 20:
            res.append({"key": key, "name": name, "n": len(ids)})
            continue
        x = rank([orient * rs[i][key] for i in ids])
        row = {"key": key, "name": name, "n": len(ids)}
        for out in ("hit", "ret", "absmv"):
            y_all = [r[out] for r in rs]
            obs = pearson(x, rank([y_all[i] for i in ids]))
            pos = {i: k for k, i in enumerate(ids)}
            ge = 0
            for pi, perm in enumerate(shuffles):
                # outcomes shuffled within day over ALL rows, then read at the proxy's rows
                yp = [y_all[perm[i]] for i in ids]
                rho = pearson(x, rank(yp))
                if abs(rho) >= abs(obs) - 1e-12:
                    ge += 1
                if out == "ret" and abs(rho) > null_max[pi]:
                    null_max[pi] = abs(rho)
            row[f"rho_{out}"], row[f"p_{out}"] = obs, (ge + 1) / (PERMS + 1)
        # median split: low attention against high attention
        vals = sorted(orient * rs[i][key] for i in ids)
        med = vals[len(vals) // 2]
        lo = [rs[i] for i in ids if orient * rs[i][key] < med]
        hi = [rs[i] for i in ids if orient * rs[i][key] >= med]
        if len(lo) < 5:   # a binary proxy: split at the value itself
            lo = [rs[i] for i in ids if orient * rs[i][key] <= vals[0]]
            hi = [rs[i] for i in ids if orient * rs[i][key] > vals[0]]
        row["lo"], row["hi"] = summary(lo), summary(hi)
        g = row["lo"]["mean"] - row["hi"]["mean"] if lo and hi else None
        se = (math.sqrt(row["lo"]["sd"] ** 2 / len(lo) + row["hi"]["sd"] ** 2 / len(hi))
              if len(lo) > 1 and len(hi) > 1 else None)
        row["gap_ret"], row["gap_t"] = g, (g / se if g is not None and se else None)
        res.append(row)
    for row in res:
        if "rho_ret" in row:
            row["p_fwer_ret"] = (sum(1 for m in null_max if m >= abs(row["rho_ret"]) - 1e-12)
                                 + 1) / (PERMS + 1)
    print(f"\n===== {label}: n={len(rs)}, {len({r['day'] for r in rs})} days, exit={EXIT}")
    print("rho is Spearman of ATTENTION against the outcome; the theory predicts it is "
          "NEGATIVE for hit and return.")
    print(f"{'proxy':46s}{'n':>4s}{'ρ hit':>8s}{'p':>6s}{'ρ ret':>8s}{'p':>6s}{'fwer':>6s}"
          f"{'ρ|mv|':>8s}{'p':>6s}   low-att  vs  high-att (hit%, ret)   gap t")
    for row in res:
        if "rho_ret" not in row:
            print(f"{row['name']:46s}{row['n']:>4d}   too few")
            continue
        lo, hi = row["lo"], row["hi"]
        print(f"{row['name'][:45]:46s}{row['n']:>4d}{row['rho_hit']:>+8.3f}{row['p_hit']:>6.3f}"
              f"{row['rho_ret']:>+8.3f}{row['p_ret']:>6.3f}{row['p_fwer_ret']:>6.3f}"
              f"{row['rho_absmv']:>+8.3f}{row['p_absmv']:>6.3f}   "
              f"{lo['n']:>3d} {lo['hit']:>4.0f}% {lo['mean']:>+6.2f}  {hi['n']:>3d} "
              f"{hi['hit']:>4.0f}% {hi['mean']:>+6.2f}   {row['gap_t'] if row['gap_t'] is None else round(row['gap_t'], 2)}")
    return res


def summary(g):
    v = [r["ret"] for r in g]
    if not v:
        return {"n": 0, "hit": float("nan"), "mean": float("nan"), "sd": 0}
    return {"n": len(v), "hit": 100 * st.fmean(r["hit"] for r in g), "mean": st.fmean(v),
            "sd": st.stdev(v) if len(v) > 1 else 0}


def main():
    rs, floor = rows()
    out = {"exit": EXIT, "floor": floor,
           "book": evaluate([r for r in rs if r["book"]], f"BOOK |impact_sum| >= {floor}"),
           "all": evaluate(rs, "ALL NAMES")}
    # how much of each proxy is just volatility
    print("\nSpearman of each proxy with 20-day realised volatility (all names):")
    for key, name, orient in PROXIES:
        g = [r for r in rs if r.get(key) is not None and r.get("realised_vol_20d") is not None]
        if len(g) >= 20:
            print(f"  {name[:45]:46s}{pearson(rank([orient*r[key] for r in g]), rank([r['realised_vol_20d'] for r in g])):+.2f}")
    (HERE / f"results-{EXIT}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")


if __name__ == "__main__":
    main()
