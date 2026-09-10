#!/usr/bin/env python3
"""Is the conviction result an artefact of hunter count?

Until 2026-09-09 `config/pipeline.yaml` set `double_hunt_top_n: 2`, so on every
resolved day the two names with the highest `hunt_priority` were hunted twice and
every other name once. The ranking key `impact_sum` is a SUM of signed per-finding
sizes, so a second hunter mechanically adds findings and pushes the name further
from zero. Conviction is `abs(impact_sum)`. So "high conviction predicts a correct
sign" and "the sweep's two favourite names predict a correct sign" and "two hunters
predict a correct sign" are three different claims that the published test cannot
tell apart.

This separates them, on data already on disk. Nothing is re-hunted.

  - THE COUNTERFACTUAL SINGLE HUNT: rebuild every double-hunted name's key from one
    hunter's findings only, so all 38 events sit at one hunter each and no name is
    dropped. This is the test that matters. Dropping the double-hunted names instead
    is not a clean control: they were chosen on `hunt_priority`, a sweep score
    assigned before any hunting, so the restricted sample is "the names the sweep
    rated lowest", a different population rather than the same one de-confounded
  - divide the key by hunter count, and by finding count
  - hold hunter count fixed as a control (partial rank correlation)
  - restrict to the single-hunted names, reported for completeness and read as the
    low-priority subsample it is
  - and run hunter count and `hunt_priority` as predictors in their own right

Both exposed tests are re-run: the conviction-vs-sign test of
`edge/scripts/edge_direction.py` (entry 14:00 ET, exit next open / next close) and the
ranking correlation of `edge/scripts/edge_decompose.py` (impact sum vs realised move,
pooled within days).

    python3 edge/scripts/edge_hunter_control.py
"""
import argparse
import glob
import json
import math
import os
import random
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


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
    if n < 3:
        return None
    ma, mb = st.mean(a), st.mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den if den else None


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def partial_spearman(x, y, z):
    """Rank correlation of x and y with z held fixed."""
    rxy, rxz, ryz = spearman(x, y), spearman(x, z), spearman(y, z)
    if None in (rxy, rxz, ryz):
        return None
    den = math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
    return (rxy - rxz * ryz) / den if den else None


def sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)


# ---------------------------------------------------------------- data assembly

def load_rows(rows_path, cache_path):
    """The 43 resolved names, each carrying hunter count, hunt_priority and both
    outcome measures: the close-to-close move and the 14:00 ET entry returns."""
    days = json.loads(Path(rows_path).read_text())
    cache = json.loads(Path(cache_path).read_text()) if Path(cache_path).exists() else {}
    out = []
    for d in sorted(days, key=lambda d: d[0]["run"]):
        run = d[0]["run"]
        sc = json.loads((Path(run) / "edge-scores.json").read_text())
        hunters = {}
        for n in sc["ranking"]:
            h = n.get("hunters")
            if h is None:
                h = len([p for p in glob.glob(f"{run}/hunts/*.json")
                         if os.path.basename(p).split("-")[0].split(".")[0].upper()
                         == n["ticker"].upper()])
            hunters[n["ticker"]] = h
        prio = {}
        sw = Path(run) / "sweep.json"
        if sw.exists():
            for n in json.loads(sw.read_text()).get("names", []):
                if n.get("hunt_priority") is not None:
                    prio[n["ticker"].upper()] = n["hunt_priority"]
        per_hunter = {}
        for n in sc["ranking"]:
            g = {}
            for f in n.get("findings") or []:
                g.setdefault(f["hunter"], []).append(f["expected_impact_pct"])
            per_hunter[n["ticker"]] = [round(sum(v), 3) for _, v in sorted(g.items())]
        for r in d:
            b = json.loads((Path(run) / "baselines" / f"{r['t']}.json").read_text())
            ed, sess = b.get("event_date"), b.get("session", "bmo")
            px = cache.get(f"{r['t']}|{ed}|{sess}") or {}
            out.append({
                "run": run, "day": run.split("/")[-2], "t": r["t"],
                "event": ed, "session": sess,
                "pred": r["impact_sum"], "escore": r["escore"], "nf": r["nf"],
                "hunters": hunters.get(r["t"]),
                "prio": prio.get(r["t"].upper()),
                "move": r["move"], "dv": r.get("dollar_vol"),
                "ro": px.get("ret_to_open_pct"), "rc": px.get("ret_to_close_pct"),
                # per-hunter sums, ordered by hunter label (a before b, h1 before h2).
                # The hunters run in parallel, so the label is arbitrary, not temporal.
                "hsums": per_hunter.get(r["t"]) or [r["impact_sum"]],
            })
    return out


def dedup(rows):
    """Keep the earlier hunt of a repeated event, as edge_direction.py does."""
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: r["run"]):
        k = (r["t"], r["event"], r["session"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def by_day(rows):
    d = {}
    for r in rows:
        d.setdefault(r["day"], []).append(r)
    return [v for _, v in sorted(d.items())]


# ------------------------------------------------------- test 1: conviction/sign

def conv_sign(rows, keyf, retk):
    """Rank of |prediction| against whether the sign was right. No threshold."""
    v = [r for r in rows if keyf(r) not in (None, 0) and r.get(retk) is not None]
    if len(v) < 4:
        return None, 0, None
    a = [abs(keyf(r)) for r in v]
    b = [1.0 if sign(keyf(r)) == sign(r[retk]) else 0.0 for r in v]
    hits = int(sum(b))
    return spearman(a, b), len(v), hits


def conv_sign_p(rows, keyf, retk, trials=20000, seed=17):
    """Permute the realised return within each day and recompute."""
    obs, n, _ = conv_sign(rows, keyf, retk)
    if obs is None:
        return None, None, n
    rnd = random.Random(seed)
    days = by_day([r for r in rows if keyf(r) not in (None, 0)
                   and r.get(retk) is not None])
    hit = 0
    for _ in range(trials):
        sub = []
        for d in days:
            rets = [r[retk] for r in d]
            rnd.shuffle(rets)
            for r, x in zip(d, rets):
                q = dict(r)
                q[retk] = x
                sub.append(q)
        s, _, _ = conv_sign(sub, keyf, retk)
        if s is not None and abs(s) >= abs(obs) - 1e-12:
            hit += 1
    return obs, hit / trials, n


def conv_sign_partial(rows, keyf, retk, ctrl):
    v = [r for r in rows if keyf(r) not in (None, 0) and r.get(retk) is not None
         and r.get(ctrl) is not None]
    if len(v) < 5:
        return None, 0
    a = [abs(keyf(r)) for r in v]
    b = [1.0 if sign(keyf(r)) == sign(r[retk]) else 0.0 for r in v]
    c = [r[ctrl] for r in v]
    return partial_spearman(a, b, c), len(v)


# ----------------------------------------------------------- test 2: the ranking

def pooled_within(days, keyf, sgn=1):
    A, B = [], []
    for d in days:
        v = [r for r in d if keyf(r) is not None]
        if len(v) < 3:
            continue
        ra, rb = ranks([sgn * keyf(r) for r in v]), ranks([r["move"] for r in v])
        ma, mb = st.mean(ra), st.mean(rb)
        A += [x - ma for x in ra]
        B += [x - mb for x in rb]
    return (pearson(A, B) if len(A) >= 3 else None), len(A)


def pooled_p(days, keyf, sgn=1, trials=20000, seed=11):
    obs, n = pooled_within(days, keyf, sgn)
    if obs is None:
        return None, None, n
    rnd = random.Random(seed)
    hit = 0
    for _ in range(trials):
        sub = []
        for d in days:
            mv = [r["move"] for r in d]
            rnd.shuffle(mv)
            sub.append([dict(r, move=m) for r, m in zip(d, mv)])
        s, _ = pooled_within(sub, keyf, sgn)
        if s is not None and abs(s) >= abs(obs) - 1e-12:
            hit += 1
    return obs, hit / trials, n


def pooled_partial(days, keyf, ctrl):
    """Partial rank correlation with the control, computed on within-day ranks."""
    A, B, C = [], [], []
    for d in days:
        v = [r for r in d if keyf(r) is not None and r.get(ctrl) is not None]
        if len(v) < 3:
            continue
        for arr, xs in ((A, [keyf(r) for r in v]), (B, [r["move"] for r in v]),
                        (C, [r[ctrl] for r in v])):
            rk = ranks(xs)
            m = st.mean(rk)
            arr += [x - m for x in rk]
    if len(A) < 5:
        return None, 0
    return partial_spearman(A, B, C), len(A)


def fisher_2x2(a, b, c, d):
    """One-sided p for a 2x2 table, hypergeometric tail. Small n, exact."""
    from math import comb
    n = a + b + c + d
    row1, col1 = a + b, a + c
    lo = max(0, col1 - (n - row1))
    hi = min(row1, col1)
    tot = sum(comb(row1, i) * comb(n - row1, col1 - i) for i in range(lo, hi + 1))
    tail = sum(comb(row1, i) * comb(n - row1, col1 - i) for i in range(a, hi + 1))
    return tail / tot


def boot_mean(xs, trials=10000, seed=5):
    rnd = random.Random(seed)
    out = sorted(st.mean(rnd.choices(xs, k=len(xs))) for _ in range(trials))
    return out[int(0.025 * trials)], out[int(0.975 * trials)]


# ------------------------------------------------------------------------ report

def fmt(x, w=6, d=3):
    return f"{x:+{w}.{d}f}" if isinstance(x, float) else f"{'--':>{w}}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", default=str(REPO / "edge/analysis/edge-rows.json"))
    ap.add_argument("--cache", default=str(REPO / ".edge_direction_cache.json"))
    ap.add_argument("--out", default=str(REPO / "edge/analysis/edge-hunter-control.json"))
    ap.add_argument("--trials", type=int, default=20000)
    a = ap.parse_args()

    allrows = load_rows(a.rows, a.cache)
    ded = dedup(allrows)
    doc = {"n_rows_raw": len(allrows), "n_events_dedup": len(ded)}

    print(f"{len(allrows)} resolved names, {len(ded)} de-duplicated events\n")

    # --- who was hunted twice
    print("hunter count by name (de-duplicated events)")
    print(f"{'day':12s}{'ticker':8s}{'hunters':>8s}{'prio':>6s}{'nf':>4s}"
          f"{'impact':>9s}{'move':>8s}{'ret_c':>8s}")
    for r in sorted(ded, key=lambda r: (r["day"], -abs(r["pred"]))):
        print(f"{r['day']:12s}{r['t']:8s}{int(r['hunters']):>8d}"
              f"{(int(r['prio']) if r['prio'] is not None else -1):>6d}{r['nf']:>4d}"
              f"{r['pred']:>+9.2f}{r['move']:>+8.2f}"
              f"{(r['rc'] if r['rc'] is not None else float('nan')):>+8.2f}")

    dbl = [r for r in ded if r["hunters"] >= 2]
    sgl = [r for r in ded if r["hunters"] == 1]
    doc["counts"] = {"double": len(dbl), "single": len(sgl)}
    print(f"\n{'':22s}{'n':>4s}{'mean nf':>9s}{'mean |impact|':>15s}"
          f"{'median |impact|':>17s}{'mean prio':>11s}")
    for lab, g in (("double-hunted", dbl), ("single-hunted", sgl)):
        pr = [r["prio"] for r in g if r["prio"] is not None]
        print(f"{lab:22s}{len(g):>4d}{st.mean(r['nf'] for r in g):>9.2f}"
              f"{st.mean(abs(r['pred']) for r in g):>15.2f}"
              f"{st.median([abs(r['pred']) for r in g]):>17.2f}"
              f"{(st.mean(pr) if pr else float('nan')):>11.1f}")
    for lab, g in (("double-hunted", dbl), ("single-hunted", sgl)):
        for retk, rl in (("rc", "close"), ("ro", "open")):
            v = [r for r in g if r["pred"] and r.get(retk) is not None]
            h = sum(1 for r in v if sign(r["pred"]) == sign(r[retk]))
            doc.setdefault("sign_by_hunters", {})[f"{lab}_{rl}"] = f"{h}/{len(v)}"
    print("\nsign correct, to the next close:  "
          + "   ".join(f"{k} {v}" for k, v in doc["sign_by_hunters"].items()
                       if k.endswith("close")))

    # --- test 1
    print("\n=== conviction vs sign-correct (rank of |pred| vs sign right) ===")
    print(f"{'variant':46s}{'exit':7s}{'rho':>7s}{'perm p':>9s}{'n':>5s}{'hits':>7s}")
    variants = [
        ("published: |impact_sum|, all events", lambda r: r["pred"], ded),
        ("single-hunted names only", lambda r: r["pred"], sgl),
        ("double-hunted names only", lambda r: r["pred"], dbl),
        ("impact_sum / hunter count", lambda r: r["pred"] / r["hunters"], ded),
        ("impact_sum / finding count", lambda r: r["pred"] / r["nf"], ded),
        ("hunter count as the predictor of |pred| sign",
         lambda r: r["hunters"] * sign(r["pred"]), ded),
    ]
    t1 = {}
    for lab, kf, rows in variants:
        for retk, rl in (("rc", "close"), ("ro", "open")):
            rho, p, n = conv_sign_p(rows, kf, retk, a.trials)
            _, _, hits = conv_sign(rows, kf, retk)
            t1[f"{lab} | {rl}"] = {"rho": rho, "p": p, "n": n, "hits": hits}
            print(f"{lab:46s}{rl:7s}{fmt(rho)}"
                  f"{(f'{p:.4f}' if p is not None else '--'):>9s}{n:>5d}"
                  f"{(f'{hits}/{n}' if hits is not None else '--'):>7s}")
    for ctrl, cl in (("hunters", "hunter count"), ("nf", "finding count"),
                     ("prio", "hunt_priority")):
        for retk, rl in (("rc", "close"), ("ro", "open")):
            rho, n = conv_sign_partial(ded, lambda r: r["pred"], retk, ctrl)
            t1[f"partial, controlling {cl} | {rl}"] = {"rho": rho, "n": n}
            print(f"{'partial rho, controlling ' + cl:46s}{rl:7s}{fmt(rho)}"
                  f"{'':>9s}{n:>5d}")
    doc["conviction_vs_sign"] = t1

    # --- the threshold
    print("\n=== the |pred| >= 3 threshold, with and without the double hunt ===")
    print(f"{'sample':34s}{'n':>4s}{'sign (close)':>14s}{'ret/trade':>11s}"
          f"{'always-short':>14s}")
    thr = {}
    for lab, g in (("all events", ded), ("single-hunted only", sgl),
                   ("double-hunted only", dbl)):
        v = [r for r in g if abs(r["pred"]) >= 3 and r.get("rc") is not None]
        if not v:
            continue
        h = sum(1 for r in v if sign(r["pred"]) == sign(r["rc"]))
        tr = [sign(r["pred"]) * r["rc"] for r in v]
        thr[lab] = {"n": len(v), "hits": h, "ret": round(st.mean(tr), 2)}
        print(f"{lab:34s}{len(v):>4d}{f'{h}/{len(v)}':>14s}"
              f"{st.mean(tr):>+11.2f}{-st.mean([r['rc'] for r in v]):>+14.2f}")
    doc["threshold_3"] = thr

    # --- test 2
    print("\n=== the ranking: impact_sum vs realised move, pooled within days ===")
    d_all, d_ded = by_day(allrows), by_day(ded)
    d_sgl = by_day(sgl)
    print(f"{'variant':46s}{'sample':10s}{'rho':>7s}{'perm p':>9s}{'n':>5s}")
    t2 = {}
    combos = [
        ("impact_sum (published key)", lambda r: r["pred"], 1),
        ("impact_sum / hunter count", lambda r: r["pred"] / r["hunters"], 1),
        ("impact_sum / finding count", lambda r: r["pred"] / r["nf"], 1),
        ("hunter count alone", lambda r: float(r["hunters"]), 1),
        ("hunt_priority alone",
         lambda r: float(r["prio"]) if r["prio"] is not None else None, 1),
    ]
    for lab, kf, sgn in combos:
        for sl, days in (("43 names", d_all), ("38 dedup", d_ded),
                         ("single only", d_sgl)):
            rho, p, n = pooled_p(days, kf, sgn, a.trials)
            t2[f"{lab} | {sl}"] = {"rho": rho, "p": p, "n": n}
            print(f"{lab:46s}{sl:10s}{fmt(rho)}"
                  f"{(f'{p:.4f}' if p is not None else '--'):>9s}{n:>5d}")
    for ctrl, cl in (("hunters", "hunter count"), ("nf", "finding count"),
                     ("prio", "hunt_priority")):
        for sl, days in (("43 names", d_all), ("38 dedup", d_ded)):
            rho, n = pooled_partial(days, lambda r: r["pred"], ctrl)
            t2[f"partial, controlling {cl} | {sl}"] = {"rho": rho, "n": n}
            print(f"{'partial rho, controlling ' + cl:46s}{sl:10s}{fmt(rho)}"
                  f"{'':>9s}{n:>5d}")
    doc["ranking"] = t2

    # --- the counterfactual single hunt: one hunter for every name, nothing dropped
    print("\n=== counterfactual: rebuild the key from ONE hunter per name ===")
    print("The double-hunted names were picked on hunt_priority, before any hunting.")
    print("Dropping them changes the population; rebuilding their key from a single")
    print("hunter holds the population and removes the doubling.\n")
    pairs = [r for r in ded if len(r["hsums"]) >= 2]
    print(f"{'day':12s}{'ticker':8s}{'hunter A':>10s}{'hunter B':>10s}"
          f"{'full':>9s}{'A only':>9s}{'B only':>9s}{'move':>9s}")
    for r in sorted(pairs, key=lambda r: r["day"]):
        ha, hb = r["hsums"][0], r["hsums"][1]
        print(f"{r['day']:12s}{r['t']:8s}{ha:>+10.2f}{hb:>+10.2f}"
              f"{r['pred']:>+9.2f}{ha:>+9.2f}{hb:>+9.2f}{r['move']:>+9.2f}")
    agree = sum(1 for r in pairs if sign(r["hsums"][0]) == sign(r["hsums"][1]))
    gap = [abs(r["hsums"][0] - r["hsums"][1]) for r in pairs]
    infl = [abs(r["pred"]) - abs(r["hsums"][0]) for r in pairs]
    print(f"\n{len(pairs)} paired names. Hunters agree on sign {agree}/{len(pairs)}; "
          f"median gap {st.median(gap):.2f} points.")
    print(f"The second hunter moves |key| by a median {st.median(infl):+.2f} points "
          f"(mean {st.mean(infl):+.2f}).")
    hs_a = sum(1 for r in pairs if r["hsums"][0] and r.get("rc") is not None
               and sign(r["hsums"][0]) == sign(r["rc"]))
    hs_f = sum(1 for r in pairs if r["pred"] and r.get("rc") is not None
               and sign(r["pred"]) == sign(r["rc"]))
    print(f"Sign correct on those names: hunter A alone {hs_a}/{len(pairs)}, "
          f"both hunters summed {hs_f}/{len(pairs)}.")
    doc["counterfactual_pairs"] = {
        "n": len(pairs), "sign_agree": agree, "median_gap": round(st.median(gap), 2),
        "median_inflation": round(st.median(infl), 2),
        "sign_first_only": hs_a, "sign_full": hs_f,
        "rows": [{"day": r["day"], "t": r["t"], "a": r["hsums"][0],
                  "b": r["hsums"][1], "full": r["pred"], "move": r["move"],
                  "rc": r["rc"]} for r in pairs]}

    cf = {"first hunter only": lambda r: r["hsums"][0],
          "second hunter only": lambda r: r["hsums"][-1],
          "mean of hunters": lambda r: st.mean(r["hsums"]),
          "full sum (published)": lambda r: r["pred"]}
    print(f"\n{'key':24s}{'conviction rho':>16s}{'p':>8s}{'hits':>8s}"
          f"{'ranking rho':>14s}{'p':>8s}")
    cfd = {}
    for lab, kf in cf.items():
        rho, pp, n = conv_sign_p(ded, kf, "rc", a.trials)
        _, _, hits = conv_sign(ded, kf, "rc")
        rr, rp, rn = pooled_p(by_day(ded), kf, 1, a.trials)
        ro_, op, _ = conv_sign_p(ded, kf, "ro", a.trials)
        cfd[lab] = {"conviction_close": rho, "p_close": pp, "hits": hits, "n": n,
                    "conviction_open": ro_, "p_open": op,
                    "ranking": rr, "ranking_p": rp, "ranking_n": rn}
        print(f"{lab:24s}{fmt(rho, 16)}{(f'{pp:.4f}'):>8s}"
              f"{f'{hits}/{n}':>8s}{fmt(rr, 14)}{(f'{rp:.4f}'):>8s}")
    doc["counterfactual_keys"] = cfd

    # --- the floor, re-derived on the counterfactual single-hunt key
    print("\n=== conviction floor on the counterfactual key (one hunter, 38 events) ===")
    print(f"{'threshold':12s}{'n':>4s}{'share':>7s}{'sign (close)':>14s}"
          f"{'ret/trade':>11s}{'boot 95% CI':>22s}{'always-short':>14s}")
    kf = lambda r: r["hsums"][0]
    cfl = {}
    for th in (0, 1, 2, 3, 5, 8):
        v = [r for r in ded if abs(kf(r)) >= th and r.get("rc") is not None]
        if len(v) < 3:
            continue
        h = sum(1 for r in v if sign(kf(r)) == sign(r["rc"]))
        tr = [sign(kf(r)) * r["rc"] for r in v]
        lo, hi = boot_mean(tr)
        cfl[th] = {"n": len(v), "hits": h, "ret": round(st.mean(tr), 2),
                   "ci": [round(lo, 2), round(hi, 2)],
                   "always_short": round(-st.mean([r["rc"] for r in v]), 2)}
        print(f"{'|pred| >= ' + str(th):12s}{len(v):>4d}"
              f"{100 * len(v) / len(ded):>6.0f}%{f'{h}/{len(v)}':>14s}"
              f"{st.mean(tr):>+11.2f}{f'[{lo:+.2f}, {hi:+.2f}]':>22s}"
              f"{-st.mean([r['rc'] for r in v]):>+14.2f}")
    doc["floor_counterfactual"] = cfl

    # --- and what any of it would have paid
    print("\n=== traded: entry 14:00 ET before the print, exit next close ===")
    print("Every name at sign(key), equal weight, gross. The mean and the sum share a")
    print("sign on every name, so they can only differ where MAGNITUDE selects.\n")
    print(f"{'key':22s}{'floor':>6s}{'n':>4s}{'hits':>8s}{'ret/trade':>11s}"
          f"{'t':>6s}{'boot 95% CI':>22s}{'day book':>11s}")
    cfk = {"full sum (published)": lambda r: r["pred"],
           "mean of hunters": lambda r: st.mean(r["hsums"]),
           "hunter A only": lambda r: r["hsums"][0],
           "hunter B only": lambda r: r["hsums"][-1]}
    days = by_day(ded)
    trd = {}
    for lab, kf in cfk.items():
        book = []
        for d in days:
            if len(d) < 3:
                continue
            srt = sorted(d, key=lambda r: -kf(r))
            k = max(1, len(srt) // 3)
            book.append((st.mean(r["move"] for r in srt[:k])
                         - st.mean(r["move"] for r in srt[-k:])) / 2)
        for floor in (0, 3):
            v = [r for r in ded if abs(kf(r)) >= floor and kf(r) != 0
                 and r.get("rc") is not None]
            tr = [sign(kf(r)) * r["rc"] for r in v]
            h = sum(1 for r in v if sign(kf(r)) == sign(r["rc"]))
            lo, hi = boot_mean(tr)
            sd = st.stdev(tr) if len(tr) > 1 else 0.0
            t = st.mean(tr) / (sd / math.sqrt(len(tr))) if sd else 0.0
            trd[f"{lab}|floor{floor}"] = {
                "n": len(v), "hits": h, "ret": round(st.mean(tr), 2),
                "t": round(t, 2), "ci": [round(lo, 2), round(hi, 2)],
                "day_book_pct": round(st.mean(book), 2)}
            print(f"{lab:22s}{floor:>6}{len(v):>4d}{f'{h}/{len(v)}':>8s}"
                  f"{st.mean(tr):>+11.2f}{t:>6.2f}"
                  f"{f'[{lo:+.2f}, {hi:+.2f}]':>22s}"
                  f"{(f'{st.mean(book):+.2f}%' if floor else ''):>11s}")
    av = [r for r in ded if r.get("rc") is not None]
    print(f"{'always short (null)':22s}{'-':>6s}{len(av):>4d}{'-':>8s}"
          f"{-st.mean([r['rc'] for r in av]):>+11.2f}")
    dis = [r for r in pairs if sign(r["hsums"][0]) != sign(r["hsums"][1])]
    okc = sum(1 for r in dis if sign(r["pred"]) == sign(r["rc"]))
    print(f"\nThe two hunters disagreed on sign on {len(dis)} of {len(pairs)} paired "
          f"names ({', '.join(r['t'] for r in dis)}).")
    print(f"Summing them resolved the sign correctly on {okc} of {len(dis)}.")
    trd["disagreements"] = {"n": len(dis), "sum_correct": okc,
                            "tickers": [r["t"] for r in dis]}
    doc["traded"] = trd

    # --- is it the second hunter, or the sweep's choice of name?
    print("\n=== separating hunter count from hunt_priority ===")
    for lab, g in (("all events", ded), ("single-hunted only", sgl)):
        for retk, rl in (("rc", "close"), ("ro", "open")):
            v = [r for r in g if r["prio"] is not None and r.get(retk) is not None
                 and r["pred"]]
            b = [1.0 if sign(r["pred"]) == sign(r[retk]) else 0.0 for r in v]
            rho = spearman([r["prio"] for r in v], b)
            doc.setdefault("priority_vs_sign", {})[f"{lab}|{rl}"] = {
                "rho": rho, "n": len(v)}
            print(f"{'hunt_priority vs sign-correct, ' + lab:46s}{rl:7s}"
                  f"{fmt(rho)}{'':>9s}{len(v):>5d}")
    hd = sum(1 for r in dbl if r["pred"] and sign(r["pred"]) == sign(r["rc"]))
    hs = sum(1 for r in sgl if r["pred"] and sign(r["pred"]) == sign(r["rc"]))
    fp = fisher_2x2(hd, len(dbl) - hd, hs, len(sgl) - hs)
    doc["double_vs_single_sign"] = {"double": f"{hd}/{len(dbl)}",
                                    "single": f"{hs}/{len(sgl)}",
                                    "fisher_one_sided_p": round(fp, 3)}
    print(f"\nsign correct to the close: double {hd}/{len(dbl)}, "
          f"single {hs}/{len(sgl)}, one-sided Fisher p={fp:.3f}")

    # --- re-deriving the conviction floor on names hunted once
    print("\n=== conviction floor, single-hunted names only (the new regime) ===")
    print(f"{'threshold':12s}{'n':>4s}{'share':>7s}{'sign (close)':>14s}"
          f"{'ret/trade':>11s}{'boot 95% CI':>22s}{'always-short':>14s}")
    fl = {}
    for th in (0, 1, 2, 3, 5, 8):
        v = [r for r in sgl if abs(r["pred"]) >= th and r.get("rc") is not None]
        if len(v) < 3:
            continue
        h = sum(1 for r in v if sign(r["pred"]) == sign(r["rc"]))
        tr = [sign(r["pred"]) * r["rc"] for r in v]
        lo, hi = boot_mean(tr)
        fl[th] = {"n": len(v), "hits": h, "ret": round(st.mean(tr), 2),
                  "ci": [round(lo, 2), round(hi, 2)],
                  "always_short": round(-st.mean([r["rc"] for r in v]), 2)}
        print(f"{'|pred| >= ' + str(th):12s}{len(v):>4d}"
              f"{100 * len(v) / len(sgl):>6.0f}%{f'{h}/{len(v)}':>14s}"
              f"{st.mean(tr):>+11.2f}{f'[{lo:+.2f}, {hi:+.2f}]':>22s}"
              f"{-st.mean([r['rc'] for r in v]):>+14.2f}")
    doc["floor_single_hunted"] = fl

    # --- per-day ranking, all names against single-hunted only
    print("\n=== per-day ranking rho (impact_sum vs move) ===")
    print(f"{'day':12s}{'n all':>6s}{'rho all':>9s}{'n single':>9s}{'rho single':>11s}")
    pd = {}
    for d in by_day(ded):
        v = [r for r in d if r["hunters"] == 1]
        ra = spearman([r["pred"] for r in d], [r["move"] for r in d])
        rs = (spearman([r["pred"] for r in v], [r["move"] for r in v])
              if len(v) >= 3 else None)
        pd[d[0]["day"]] = {"n": len(d), "rho": ra, "n_single": len(v),
                           "rho_single": rs}
        print(f"{d[0]['day']:12s}{len(d):>6d}{fmt(ra, 9)}{len(v):>9d}"
              f"{fmt(rs, 11)}")
    doc["per_day_ranking"] = pd

    Path(a.out).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
