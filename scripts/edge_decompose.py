#!/usr/bin/env python3
"""Which of the numbers stage E computes actually ranks the day?

`edge_resolve.py` answers "did edge_score rank" and nothing else. This answers the
prior question: of every quantity the run already wrote to disk -- the hunters' raw
impact sizes, the residuals after the adversary, the volunteered expected_move_pct,
the sealed baseline's own price lean, the 20-day run-up -- which ones order a day's
realised moves, and does the scorer's aggregation add to them or subtract from them.

Pooling is done WITHIN days. Each day is converted to within-day ranks, centred, and
the centred ranks are correlated across days, so no market-wide drift can enter the
rank structure and no assumption is made that two days' edge_score are on one scale.
`edge_resolve.py --pool` concatenates raw pairs instead and understates every ranker.
p-values permute the realised moves within each day.

    python3 scripts/edge_decompose.py --pool 'research/2026/*/*/edge'

Findings as of 43 resolved names live in docs/EDGE_ANALYSIS.md.
"""
import argparse
import glob
import importlib.util
import json
import math
import os
import random
import statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(mod):
    s = importlib.util.spec_from_file_location(mod, HERE / f"{mod}.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def ranks(x):
    s = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for m in range(i, j + 1):
            r[s[m]] = avg
        i = j + 1
    return r


def pearson(a, b):
    n = len(a)
    ma, mb = st.mean(a), st.mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den if den else 0.0


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def pooled_within(days, key, sign=1):
    """Day-fixed-effect rank correlation. Only within-day ordering contributes."""
    A, B = [], []
    for d in days:
        v = [sign * r[key] for r in d if r.get(key) is not None]
        m = [r["move"] for r in d if r.get(key) is not None]
        if len(v) < 3:
            continue
        ra, rb = ranks(v), ranks(m)
        ma, mb = st.mean(ra), st.mean(rb)
        A += [x - ma for x in ra]
        B += [x - mb for x in rb]
    return (pearson(A, B) if A else 0.0), len(A)


def perm_p(days, key, sign=1, n=20000, seed=11):
    obs, _ = pooled_within(days, key, sign)
    random.seed(seed)
    sub = [[dict(r) for r in d] for d in days]
    c = 0
    for _ in range(n):
        for d in sub:
            mv = [r["move"] for r in d]
            random.shuffle(mv)
            for r, m in zip(d, mv):
                r["move"] = m
        s, _ = pooled_within(sub, key, sign)
        if abs(s) >= abs(obs) - 1e-12:
            c += 1
    return obs, c / n


def boot_diff(days, k1, s1, k2, s2, n=5000, seed=3):
    random.seed(seed)
    out = []
    for _ in range(n):
        ds = [random.choice(days) for _ in days]
        a, _ = pooled_within(ds, k1, s1)
        b, _ = pooled_within(ds, k2, s2)
        out.append(a - b)
    out.sort()
    return (st.mean(out), out[int(0.025 * len(out))], out[int(0.975 * len(out))],
            sum(1 for x in out if x <= 0) / len(out))


def build(runs, cache_path):
    er = _load("edge_resolve")
    cache = json.loads(Path(cache_path).read_text()) if Path(cache_path).exists() else {}
    days = []
    for run in runs:
        sf = Path(run) / "edge-scores.json"
        if not sf.exists():
            continue
        sc = json.loads(sf.read_text())
        if sc.get("legacy_rescore"):
            continue                      # midpoints, not measurements
        hunts = {}
        for p in glob.glob(f"{run}/hunts/*.json"):
            h = json.loads(Path(p).read_text())
            t = h.get("ticker") or os.path.basename(p).split("-")[0]
            hunts.setdefault(t, []).append(h)
        rows = []
        for n in sc["ranking"]:
            if not n.get("rankable"):
                continue
            t = n["ticker"]
            bp = Path(run) / "baselines" / f"{t}.json"
            b = json.loads(bp.read_text()) if bp.exists() else {}
            key = f"{run}|{t}"
            if key not in cache:
                res, err = er.realised(t, b.get("event_date"), b.get("session", "bmo"))
                cache[key] = {"res": res, "err": err}
                Path(cache_path).write_text(json.dumps(cache))
            c = cache[key]
            if c["err"] or not c["res"]:
                continue
            fs = n["findings"]
            clusters = {}
            for x in fs:
                clusters.setdefault(x["cluster"], []).append(x["residual_pct"])
            per = [max(v, key=abs) for v in clusters.values()]
            k = len(per)
            hm = [h.get("expected_move_pct") for h in hunts.get(t, [])
                  if h.get("expected_move_pct") is not None]
            rows.append({
                "run": run, "t": t, "move": c["res"]["move_pct"],
                "escore": n["edge_score"], "edge_pct": n["edge_pct"],
                "conf": n["confidence"], "qual": n["baseline_quality"],
                "lean": n["priced_lean_pct"],
                "resid_sum": sum(x["residual_pct"] for x in fs),
                "resid_cluster": sum(per),
                "resid_norm": (sum(per) / math.sqrt(k)) if k else 0.0,
                "impact_sum": sum(x["expected_impact_pct"] for x in fs),
                "mean_priced": st.mean([x["priced_in_pct"] for x in fs]) if fs else None,
                "hunter_move": st.mean(hm) if hm else None,
                "runup": (b.get("tape") or {}).get("run_up_20d_pct"),
                "implied": (b.get("options") or {}).get("event_implied_move_pct"),
                "nf": len(fs),
            })
        if len(rows) >= 3:
            days.append(rows)
    return days


CANDIDATES = [
    ("impact_sum", 1, "impact sum, pre-adversary"),
    ("resid_sum", 1, "residual sum, no multipliers"),
    ("hunter_move", 1, "hunt expected_move_pct (unused by scorer)"),
    ("lean", 1, "priced_lean_pct (baseline only)"),
    ("runup", -1, "minus 20d run-up (free)"),
    ("resid_cluster", 1, "residual sum by cluster"),
    ("resid_norm", 1, "cluster sum / sqrt(k)"),
    ("edge_pct", 1, "edge_pct"),
    ("escore", 1, "edge_score as shipped"),
    ("qual", 1, "baseline_quality"),
    ("mean_priced", 1, "mean priced_in_pct"),
    ("conf", 1, "confidence"),
    ("nf", 1, "n findings"),
]

PAIRS = [("impact_sum", 1, "escore", 1), ("resid_sum", 1, "escore", 1),
         ("impact_sum", 1, "runup", -1), ("impact_sum", 1, "lean", 1),
         ("hunter_move", 1, "runup", -1)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", nargs="*", default=["research/2026/*/*/edge"])
    ap.add_argument("--cache", default=".edge_decompose_cache.json",
                    help="realised-move cache, so a re-run costs no network")
    ap.add_argument("--out", default="docs/edge-decompose.json")
    a = ap.parse_args()

    runs = []
    for pat in a.pool:
        runs.extend(sorted(glob.glob(pat)))
    days = build(runs, a.cache)
    n = sum(len(d) for d in days)
    print(f"{len(days)} resolvable days, {n} names\n")

    print(f"{'ranking key':44s}{'rho':>9s}{'p':>9s}")
    table = []
    for key, sign, label in CANDIDATES:
        rho, p = perm_p(days, key, sign)
        table.append({"key": key, "label": label, "rho": round(rho, 3), "p": round(p, 4)})
    for r in sorted(table, key=lambda r: -r["rho"]):
        print(f"{r['label']:44s}{r['rho']:>+9.3f}{r['p']:>9.4f}")

    print("\npaired bootstrap over days")
    pairs = []
    for k1, s1, k2, s2 in PAIRS:
        m, lo, hi, pl = boot_diff(days, k1, s1, k2, s2)
        pairs.append({"a": k1, "b": k2, "delta_rho": round(m, 3),
                      "ci95": [round(lo, 3), round(hi, 3)], "p_le_0": round(pl, 3)})
        print(f"  {k1:12s} - {k2:12s} delta={m:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]"
              f"  P(<=0)={pl:.3f}")

    print("\nlong top third / short bottom third, mean over days")
    spreads = {}
    for key, sign, label in [("escore", 1, "edge_score"), ("impact_sum", 1, "impact sum"),
                             ("runup", -1, "minus run-up")]:
        vals = []
        for d in days:
            s = sorted([r for r in d if r.get(key) is not None],
                       key=lambda r: -sign * r[key])
            k = max(1, len(s) // 3)
            vals.append(st.mean([r["move"] for r in s[:k]])
                        - st.mean([r["move"] for r in s[-k:]]))
        spreads[key] = {"per_day": [round(v, 2) for v in vals],
                        "mean_pp": round(st.mean(vals), 2),
                        "positive_days": sum(1 for v in vals if v > 0), "days": len(vals)}
        print(f"  {label:14s}{st.mean(vals):+7.2f}pp   positive on "
              f"{spreads[key]['positive_days']}/{len(vals)} days")

    doc = {"runs": [d[0]["run"] for d in days], "n_names": n,
           "pooling": "within-day ranks, centred, correlated across days",
           "candidates": table, "paired_bootstrap": pairs, "long_short": spreads}
    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
