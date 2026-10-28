import json, collections, math
from pathlib import Path
from stats import *
ROOT = Path(__file__).resolve().parents[3]
R = [r for r in json.load(open("rows.json")) if r["ret"] is not None and r["arm"] == "EP"]
days = collections.defaultdict(list)
for r in R: days[r["run_date"]].append(r)
# priority rank within the day
for d, x in days.items():
    pr = {}
    for r in x:
        p = ROOT / f"research/2026/10/{d}/edge-panel/sweep-rows/{r['ticker']}.json"
        try: pr[r["ticker"]] = json.load(open(p)).get("hunt_priority")
        except Exception: pr[r["ticker"]] = None
    order = sorted(x, key=lambda r: -(pr[r["ticker"]] or -1))
    for i, r in enumerate(order): r["prio_rank"] = i + 1; r["prio"] = pr[r["ticker"]]
def bucket(n): return "thin" if n <= 10 else ("mid" if n <= 16 else "busy")
# day-level selected means
dm = {b: [] for b in ("thin", "mid", "busy")}
for d, x in days.items():
    s = [r["ret"] for r in x if r["selected"]]
    if s: dm[bucket(len(x))].append(sum(s) / len(s))
print({b: [round(v, 2) for v in vs] for b, vs in dm.items()})
a, b = dm["thin"], dm["busy"]
ma, mb = sum(a)/len(a), sum(b)/len(b)
va = sum((v-ma)**2 for v in a)/(len(a)-1); vb = sum((v-mb)**2 for v in b)/(len(b)-1)
t = (ma-mb)/math.sqrt(va/len(a)+vb/len(b)); df = (va/len(a)+vb/len(b))**2/((va/len(a))**2/(len(a)-1)+(vb/len(b))**2/(len(b)-1))
print("day-level thin vs busy selected: diff", round(ma-mb, 2), "Welch t", round(t, 2), "df", round(df, 1), "p", round(pval_t(t, df), 3))
# rank-sum exact on day means: thin all above busy?
print("busy days: selected by priority rank <=10 vs >10")
for lab, f in (("rank<=10", lambda r: r["prio_rank"] <= 10), ("rank>10", lambda r: r["prio_rank"] > 10)):
    s = [r["ret"] for d, x in days.items() if bucket(len(x)) == "busy" for r in x if r["selected"] and f(r)]
    al = [r["ret"] for d, x in days.items() if bucket(len(x)) == "busy" for r in x if f(r)]
    print(" ", lab, "selected", summ(s), "| all", summ(al))
print("long vs short among selected, by bucket")
for bk in ("thin", "mid", "busy"):
    for sd in (1, -1):
        s = [r["ret"] for d, x in days.items() if bucket(len(x)) == bk for r in x if r["selected"] and r["side"] == sd]
        print(" ", bk, "long" if sd == 1 else "short", summ(s))
print("session among selected, by bucket")
for bk in ("thin", "busy"):
    for ss in ("amc", "bmo"):
        s = [r["ret"] for d, x in days.items() if bucket(len(x)) == bk for r in x if r["selected"] and r["session"] == ss]
        print(" ", bk, ss, summ(s))
# excluding 10-21
s = [r["ret"] for d, x in days.items() if bucket(len(x)) == "busy" and d != "2026-10-21" for r in x if r["selected"]]
print("busy without 10-21:", summ(s))
print("pct_filled days (pre-10-14 recomputed):", sorted({r['run_date'] for r in R if r['pct_filled']}))
