import json, collections
from stats import *
R = [r for r in json.load(open("rows.json")) if r["ret"] is not None]
by = collections.defaultdict(dict)
for r in R:
    by[(r["run_date"], r["ticker"])][r["arm"]] = r

def fmt(d): return f"n {d['n']}, mean {d['mean']}%, hit {d['hit']}/{d['n']}, t {d['t']}, p {d['p']}"

print("=== Q1 split (EPS) vs full (EP), same names, same day")
pairs = [(k, v["EP"], v["EPS"]) for k, v in by.items() if "EP" in v and "EPS" in v]
days = sorted(set(k[0] for k, _, _ in pairs)); print("days", days, "paired names", len(pairs))
a = [p[1]["signed"] for p in pairs]; b = [p[2]["signed"] for p in pairs]
print("rho EP vs EPS signed pct (pooled):", round(spearman(a, b), 3),
      " same side:", sum(1 for x, y in zip(a, b) if (x > 0) == (y > 0)), "/", len(a))
for arm in ("EP", "EPS"):
    g = [([p[1 if arm == 'EP' else 2]["signed"] for p in pairs if p[0][0] == d],
          [p[1]["move"] for p in pairs if p[0][0] == d]) for d in days]
    print(arm, "within-day rho vs move:", within_day_rho(g))
    sel = [p[1 if arm == 'EP' else 2]["ret"] for p in pairs if p[1 if arm == 'EP' else 2]["selected"]]
    print(arm, "selected:", fmt(summ(sel)) if sel else "none",
          [p[0] for p in pairs if p[1 if arm == 'EP' else 2]["selected"]])
    for cut in (60, 70):
        s = [p[1 if arm == 'EP' else 2]["ret"] for p in pairs if p[1 if arm == 'EP' else 2]["panel_pct"] >= cut]
        print(f"  {arm} pct>={cut}:", fmt(summ(s)) if s else "none")
    # top 3 per day
    s = []
    for d in days:
        pp = sorted([p for p in pairs if p[0][0] == d], key=lambda p: -p[1 if arm == 'EP' else 2]["panel_pct"])[:3]
        s += [p[1 if arm == 'EP' else 2]["ret"] for p in pp]
    print(f"  {arm} top3/day:", fmt(summ(s)))
print("findings EP/EPS", sum(p[1]["n_findings"] for p in pairs)/len(pairs), sum(p[2]["n_findings"] for p in pairs)/len(pairs))
print("mean |pct| EP/EPS", sum(p[1]["panel_pct"] for p in pairs)/len(pairs), sum(p[2]["panel_pct"] for p in pairs)/len(pairs))
for p in sorted(pairs, key=lambda p: -max(p[1]["panel_pct"], p[2]["panel_pct"]))[:14]:
    print(p[0], p[1]["session"], "EP", p[1]["signed"], "EPS", p[2]["signed"], "move", round(p[1]["move"], 2))
avg = [(x + y) / 2 for x, y in zip(a, b)]
g = [([ (p[1]["signed"] + p[2]["signed"]) / 2 for p in pairs if p[0][0] == d], [p[1]["move"] for p in pairs if p[0][0] == d]) for d in days]
print("avg of both within-day rho:", within_day_rho(g))

print("\n=== reproducibility per day, all paired names incl. unresolved")
ALL = json.load(open("rows.json"))
bya = collections.defaultdict(dict)
for r in ALL:
    if r["signed"] is not None: bya[(r["run_date"], r["ticker"])][r["arm"]] = r
for d in sorted({k[0] for k, v in bya.items() if "EPS" in v}):
    pr = [(v["EP"], v["EPS"]) for k, v in bya.items() if k[0] == d and "EP" in v and "EPS" in v]
    if len(pr) < 3: print(d, "pairs", len(pr)); continue
    x = [p[0]["signed"] for p in pr]; y = [p[1]["signed"] for p in pr]
    print(d, "pairs", len(pr), "rho", round(spearman(x, y), 2), "same side", sum((a > 0) == (b > 0) for a, b in zip(x, y)),
          "EP sel", sorted(p[0]["ticker"] for p in pr if p[0]["selected"]), "EPS sel", sorted(p[1]["ticker"] for p in pr if p[1]["selected"]),
          "resolved", sum(p[0]["ret"] is not None for p in pr))
    for p in sorted(pr, key=lambda p: -max(p[0]["panel_pct"], p[1]["panel_pct"]))[:8]:
        print("   ", p[0]["ticker"], p[0]["session"], "EP", p[0]["signed"], "EPS", p[1]["signed"], "move", None if p[0]["move"] is None else round(p[0]["move"], 2))

print("\n=== selected by both arms vs by one arm (resolved, each arm on its own side)")
both = [p[1]["ret"] for p in pairs if p[1]["selected"] and p[2]["selected"] and p[1]["side"] == p[2]["side"]]
only_ep = [p[1]["ret"] for p in pairs if p[1]["selected"] and not (p[2]["selected"] and p[1]["side"] == p[2]["side"])]
only_eps = [p[2]["ret"] for p in pairs if p[2]["selected"] and not (p[1]["selected"] and p[1]["side"] == p[2]["side"])]
for lab, s in (("both", both), ("E-P only", only_ep), ("split only", only_eps)):
    print(lab, fmt(summ(s)) if s else "none")
print("per day E-P sel / EPS sel mean:")
for d in days:
    for i, arm in ((1, "EP"), (2, "EPS")):
        s = [p[i]["ret"] for p in pairs if p[0][0] == d and p[i]["selected"]]
        print("  ", d, arm, len(s), round(sum(s)/len(s), 2) if s else "-")
