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
