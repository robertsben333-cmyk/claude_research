"""Difference tests, per version: mean return inside a group minus outside it, Welch
t and a two-sided permutation p (labels shuffled). The same list is run on v2 and v3,
so a cut read off one version is tested out of sample on the other."""
import json, math, random, statistics as st
from pathlib import Path
from collections import defaultdict
R = json.load(open(Path(__file__).with_name("rows.json")))
random.seed(7)
def diff(a, b, perms=5000):
    if len(a) < 3 or len(b) < 3: return f"n {len(a)}/{len(b)} too small"
    d = st.mean(a) - st.mean(b)
    se = math.sqrt(st.variance(a)/len(a) + st.variance(b)/len(b))
    pool = a + b; k = 0
    for _ in range(perms):
        random.shuffle(pool)
        if abs(st.mean(pool[:len(a)]) - st.mean(pool[len(a):])) >= abs(d): k += 1
    return f"in n{len(a):>3} {st.mean(a):+6.2f}% | out n{len(b):>3} {st.mean(b):+6.2f}% | diff {d:+6.2f} t{d/se:+5.2f} p{(k+1)/(perms+1):.3f}"
mid = lambda r: r.get("mcap") and 3e8 <= r["mcap"] < 1e10
T = [
 ("pct>=60: market cap $0.3-10b vs rest", lambda r: r["pct"]>=60, mid),
 ("all: market cap $0.3-10b vs rest", lambda r: True, mid),
 ("all: market cap >$10b vs rest", lambda r: True, lambda r: r.get("mcap") and r["mcap"]>=1e10),
 ("pct>=60: price $10-50 vs rest", lambda r: r["pct"]>=60 and r.get("spot"), lambda r: 10<=r["spot"]<50),
 ("pct>=60: side with the 5d move vs against", lambda r: r["pct"]>=60 and r.get("runup_5d"), lambda r: (r["runup_5d"]>0)==(r["side"]>0)),
 ("all: side with the 5d move vs against", lambda r: bool(r.get("runup_5d")), lambda r: (r["runup_5d"]>0)==(r["side"]>0)),
 ("pct>=60: agrees with sealed lean vs against  [old stage E hypothesis]", lambda r: r["pct"]>=60 and r.get("lean_agree") is not None, lambda r: r["lean_agree"]),
 ("pct>=80: agrees with sealed lean vs against  [old]", lambda r: r["pct"]>=80 and r.get("lean_agree") is not None, lambda r: r["lean_agree"]),
 ("pct>=60: retail tilt >=50 vs <50  [old]", lambda r: r["pct"]>=60 and r.get("retail_tilt") is not None, lambda r: r["retail_tilt"]>=50),
 ("pct>=80: retail tilt >=50 vs <50  [old]", lambda r: r["pct"]>=80 and r.get("retail_tilt") is not None, lambda r: r["retail_tilt"]>=50),
 ("all: Technology vs rest  [old: tech weak]", lambda r: True, lambda r: r.get("sector")=="Technology"),
 ("all: Consumer Cyclical vs rest  [old: strong]", lambda r: True, lambda r: r.get("sector")=="Consumer Cyclical"),
 ("all: pct>=80 vs <80  [old: the floor]", lambda r: True, lambda r: r["pct"]>=80),
 ("all: pct>=60 vs <60", lambda r: True, lambda r: r["pct"]>=60),
 ("pct>=60: bmo vs amc  [old: bmo better]", lambda r: r["pct"]>=60, lambda r: r["session"]=="bmo"),
 ("pct>=80: long vs short  [Fable 5.2 trial: shorts fail]", lambda r: r["pct"]>=80, lambda r: r["side"]>0),
 ("pct>=60: long vs short", lambda r: r["pct"]>=60, lambda r: r["side"]>0),
 ("all: vol20 >=58 vs <58  [frozen forward test]", lambda r: r.get("vol20") is not None, lambda r: r["vol20"]>=58),
 ("pct>=60: implied move >=10% vs lower", lambda r: r["pct"]>=60 and r.get("implied") is not None, lambda r: r["implied"]>=10),
 ("all: usable option chain vs none", lambda r: True, lambda r: r.get("opt_ok")),
 ("pct 60-80 vs pct>=80", lambda r: r["pct"]>=60, lambda r: r["pct"]<80),
]
for name, base, grp in T:
    print("\n" + name)
    for v in ("us-panel.v2", "us-panel.v3"):
        g = [r for r in R if r["version"]==v and base(r)]
        print(f"  {v[-2:]}: " + diff([r["ret"] for r in g if grp(r)], [r["ret"] for r in g if not grp(r)]))

print("\n\nCandidate rule, per day (equal weight within the day): pct>=60 and market cap $0.3-10b")
for v in ("us-panel.v2", "us-panel.v3"):
    for lab, f in (("rule", lambda r: r["pct"]>=60 and mid(r)), ("live rule pct>=80", lambda r: r["pct"]>=80),
                   ("pct>=60", lambda r: r["pct"]>=60)):
        d = defaultdict(list)
        for r in R:
            if r["version"]==v and f(r): d[r["run_date"]].append(r["ret"])
        xs = [st.mean(x) for x in d.values()]
        n = sum(len(x) for x in d.values())
        t = st.mean(xs)/(st.stdev(xs)/math.sqrt(len(xs)))
        print(f"  {v[-2:]} {lab:<18} {n:>3} names on {len(xs):>2} days, mean day {st.mean(xs):+5.2f}%, t {t:+.2f}, days up {sum(1 for x in xs if x>0)}/{len(xs)}")
