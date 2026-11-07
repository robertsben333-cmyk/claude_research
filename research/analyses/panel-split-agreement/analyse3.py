import json, collections
from stats import *
R = [r for r in json.load(open("rows.json")) if r["ret"] is not None and r["signed"] is not None]
by = collections.defaultdict(dict)
for r in R: by[(r["run_date"], r["ticker"])][r["arm"]] = r
multi = {k: v for k, v in by.items() if "EP" in v and len(v) >= 2}
print("names with E-P plus >=1 other run:", len(multi), "days", sorted({k[0] for k in multi}))
print("arm combos:", collections.Counter(tuple(sorted(v)) for v in multi.values()))
def fmt(d): return f"n {d['n']} mean {d['mean']}% hit {d['hit']}/{d['n']} t {d['t']} p {d['p']}" if d['n'] else 'n 0'
# per name: E-P side, how many other runs agree on side, mean signed across all runs, number of runs selecting
for k, v in multi.items():
    ep = v["EP"]; others = [x for a, x in v.items() if a != "EP"]
    v["_agree_all"] = all((o["signed"] > 0) == (ep["signed"] > 0) for o in others)
    v["_mean"] = sum(x["signed"] for x in v.values() if isinstance(x, dict) and "signed" in x) / len([x for x in v.values() if isinstance(x, dict) and "signed" in x])
    v["_nsel"] = sum(1 for a, x in v.items() if isinstance(x, dict) and x.get("selected") and (x["signed"] > 0) == (ep["signed"] > 0))
    v["_nruns"] = len([a for a in v if not a.startswith("_")])
    v["_minabs"] = min(abs(x["signed"]) if (x["signed"] > 0) == (ep["signed"] > 0) else 0 for a, x in v.items() if not a.startswith("_"))
print("\n(a) E-P names with panel_pct >= T: other runs all on the same side vs not")
for T in (60, 70, 80):
    ag = [v["EP"]["ret"] for v in multi.values() if v["EP"]["panel_pct"] >= T and v["_agree_all"]]
    dis = [v["EP"]["ret"] for v in multi.values() if v["EP"]["panel_pct"] >= T and not v["_agree_all"]]
    print(f" T={T} agree: {fmt(summ(ag))} | disagree: {fmt(summ(dis))}")
print("\n(b) all multi-run names: E-P side return by whether all runs agree on side")
ag = [v["EP"]["ret"] for v in multi.values() if v["_agree_all"]]; dis = [v["EP"]["ret"] for v in multi.values() if not v["_agree_all"]]
print(" agree", fmt(summ(ag)), "| disagree", fmt(summ(dis)))
print("\n(c) within-day rho vs move: E-P alone vs mean over its runs vs weakest-link (same names)")
days = sorted({k[0] for k in multi})
for lab, f in (("E-P alone", lambda v: v["EP"]["signed"]), ("mean of runs", lambda v: v["_mean"]),
               ("weakest link", lambda v: (1 if v["EP"]["signed"] > 0 else -1) * v["_minabs"])):
    g = [([f(v) for k, v in multi.items() if k[0] == d], [v["EP"]["move"] for k, v in multi.items() if k[0] == d]) for d in days]
    o, p, n = within_day_rho(g); print(f" {lab}: rho {o:+.3f} p {p:.3f} n {n}")
print("\n(d) selected in E-P: by how many runs (same side) selected it")
for k_ in (1, 2, 3, 4):
    s = [v["EP"]["ret"] for v in multi.values() if v["EP"]["selected"] and v["_nsel"] == k_]
    print(f" selected by {k_} run(s):", fmt(summ(s)))
s = [ (v["EP"]["signed"] > 0 and 1 or -1) * v["EP"]["move"] for v in multi.values() if v["_nsel"] >= 2]
print(" any name selected by >=2 runs:", fmt(summ(s)))
s = [ (v["EP"]["signed"] > 0 and 1 or -1) * v["EP"]["move"] for v in multi.values() if abs(v["_mean"]) >= 80]
print(" mean over runs >= 80:", fmt(summ(s)))
# reproducibility between runs: pairwise rho of signed pct and selection overlap
print("\n(e) run-to-run reproducibility (same names, same day)")
for a in ("EPI-1000", "EPI-1200", "EPF", "EPS"):
    pr = [(v["EP"], v[a]) for v in multi.values() if a in v]
    if not pr: continue
    x = [p[0]["signed"] for p in pr]; y = [p[1]["signed"] for p in pr]
    ss = sum(1 for p in pr if (p[0]["signed"] > 0) == (p[1]["signed"] > 0))
    se = [p for p in pr if p[0]["selected"] or p[1]["selected"]]
    both = sum(1 for p in pr if p[0]["selected"] and p[1]["selected"] and (p[0]["signed"]>0)==(p[1]["signed"]>0))
    print(f" E-P vs {a}: n {len(pr)}, rho {spearman(x, y):+.2f}, same side {ss}/{len(pr)}, selected by either {len(se)}, by both {both}")
    for arm_i in (0, 1):
        g = [([p[arm_i]["signed"] for p in pr if p[0]["run_date"] == d], [p[0]["move"] for p in pr if p[0]["run_date"] == d]) for d in sorted({p[0]["run_date"] for p in pr})]
        o, pv, n = within_day_rho(g); print(f"    {'E-P' if arm_i==0 else a} rho vs move {o:+.3f} p {pv:.3f}")
# within-panel judge agreement, E-P live, all names with 4 members
print("\n(f) inside one panel: the four judges' sign agreement and spread (E-P live)")
EP = [r for r in R if r["arm"] == "EP" and r["n_members"] == 4]
for T in (0, 60, 80):
    for k_ in (4, 3, 2):
        s = [r["ret"] for r in EP if r["panel_pct"] >= T and r["sign_agree"] == k_]
        print(f" pct>={T} sign_agree {k_}/4:", fmt(summ(s)))
for T in (60, 80):
    xs = [r for r in EP if r["panel_pct"] >= T]
    med = sorted(r["sd"] for r in xs)[len(xs)//2]
    lo = [r["ret"] for r in xs if r["sd"] <= med]; hi = [r["ret"] for r in xs if r["sd"] > med]
    print(f" pct>={T} spread <= median {med}: {fmt(summ(lo))} | above: {fmt(summ(hi))}")
print("\n(g) differences, Welch")
for T in (0, 60, 70):
    ag = [v["EP"]["ret"] for v in multi.values() if v["EP"]["panel_pct"] >= T and v["_agree_all"]]
    dis = [v["EP"]["ret"] for v in multi.values() if v["EP"]["panel_pct"] >= T and not v["_agree_all"]]
    print(f" T={T}: agree minus disagree", welch(ag, dis), len(ag), len(dis))
xs = [r for r in EP if r["panel_pct"] >= 80]; med = sorted(r["sd"] for r in xs)[len(xs)//2]
print(" >=80 low minus high spread", welch([r["ret"] for r in xs if r["sd"] <= med], [r["ret"] for r in xs if r["sd"] > med]))
print(" sign_agree 4 minus 2 (all)", welch([r["ret"] for r in EP if r["sign_agree"] == 4], [r["ret"] for r in EP if r["sign_agree"] == 2]))
