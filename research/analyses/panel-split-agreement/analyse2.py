import json, collections
from stats import *
R = [r for r in json.load(open("rows.json")) if r["ret"] is not None]
def fmt(d): return f"n {d['n']}, mean {d['mean']}%, hit {d['hit']}/{d['n']}, t {d['t']}, p {d['p']}" if d['n'] else "n 0"
EP = [r for r in R if r["arm"] == "EP"]
days = collections.defaultdict(list)
for r in EP: days[r["run_date"]].append(r)
print("=== Q2 day size, live E-P", len(EP), "names", len(days), "days")
for d in sorted(days):
    rs = days[d]; s = [r for r in rs if r["selected"]]
    print(d, "n", len(rs), "sel", len(s), "sel mean", round(sum(r["ret"] for r in s)/len(s),2) if s else "-",
          "all-short", round(-sum(r["move"] for r in rs)/len(rs),2))
def bucket(n): return "thin<=10" if n <= 10 else ("mid 11-16" if n <= 16 else "busy>=19")
for b in ("thin<=10", "mid 11-16", "busy>=19"):
    rs = [r for d, x in days.items() if bucket(len(x)) == b for r in x]
    nd = sum(1 for d, x in days.items() if bucket(len(x)) == b)
    sel = [r["ret"] for r in rs if r["selected"]]
    g = [([r["signed"] for r in x], [r["move"] for r in x]) for d, x in days.items() if bucket(len(x)) == b]
    print(b, "days", nd, "names", len(rs), "share>=80", round(sum(1 for r in rs if r["selected"])/len(rs),2),
          "| selected:", fmt(summ(sel)), "| within-day rho", tuple(round(v,3) for v in within_day_rho(g)[:2]))
    for cut in (60, 70, 90):
        s = [r["ret"] for r in rs if r["panel_pct"] >= cut and r["n_members"] == 4]
        print("   pct>=", cut, fmt(summ(s)))
# rank of selected within day on busy days: top1, top2, rest of selected
print("-- busy days: top-1 / top-2 per day vs the other >=80 names")
for b in ("thin<=10", "mid 11-16", "busy>=19"):
    t1, t2, rest = [], [], []
    for d, x in days.items():
        if bucket(len(x)) != b: continue
        s = sorted([r for r in x if r["selected"]], key=lambda r: -r["panel_pct"])
        t1 += [r["ret"] for r in s[:1]]; t2 += [r["ret"] for r in s[:2]]; rest += [r["ret"] for r in s[2:]]
    print(b, "top1:", fmt(summ(t1)), "| top2:", fmt(summ(t2)), "| rank 3+:", fmt(summ(rest)))
# relative cut: top 10% of the day by panel_pct (at least 1)
print("-- top 10% / top 20% of each day (rank), not the absolute 80")
for b in ("thin<=10", "mid 11-16", "busy>=19"):
    for q in (0.1, 0.2):
        s = []
        for d, x in days.items():
            if bucket(len(x)) != b: continue
            k = max(1, round(q * len(x)))
            s += [r["ret"] for r in sorted(x, key=lambda r: -r["panel_pct"])[:k]]
        print(b, q, fmt(summ(s)))
# pooled: day size vs selected return (spearman across selected names)
sel = [r for r in EP if r["selected"]]
print("rho(day size, selected ret):", round(spearman([r["day_n"] for r in sel], [r["ret"] for r in sel]), 3), "n", len(sel))
print("rho(day size, ret) all names:", round(spearman([r["day_n"] for r in EP], [r["ret"] for r in EP]), 3), "n", len(EP))
