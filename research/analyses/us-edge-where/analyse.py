"""Where does the US panel (stage E-P) work? Every cut is computed per prompt version
(us-panel.v2 and us-panel.v3 are never pooled) at three levels: all names, panel_pct
>= 60 and >= 80. Per cell: n, hit rate, mean return on the panel's side (gross,
operator's window), t, and a two-sided sign-flip p. Standard library only.
Run: python3 research/analyses/us-edge-where/analyse.py > results.txt"""
import json, math, random, statistics as st
from pathlib import Path
from collections import defaultdict
R = json.load(open(Path(__file__).with_name("rows.json")))
random.seed(20261113)
VERS = ["us-panel.v2", "us-panel.v3"]

def cell(xs, flips=4000):
    n = len(xs)
    if n == 0: return None
    m = sum(xs) / n
    hit = 100 * sum(1 for x in xs if x > 0) / n
    if n < 3: return (n, hit, m, None, None)
    sd = st.stdev(xs)
    t = m / (sd / math.sqrt(n)) if sd else 0
    k = 0
    for _ in range(flips):
        s = sum(x if random.random() < .5 else -x for x in xs) / n
        if abs(s) >= abs(m) - 1e-12: k += 1
    return (n, hit, m, t, (k + 1) / (flips + 1))

def fmt(c):
    if not c: return f"{'-':>30}"
    n, hit, m, t, p = c
    if t is None: return f"n{n:>4} {hit:5.0f}% {m:+6.2f}%{'':13}"
    star = '*' if p < .05 else ' '
    return f"n{n:>4} {hit:5.0f}% {m:+6.2f}% t{t:+5.2f} p{p:.3f}{star}"

def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r

def pooled_rho(rows, xf, yf, perms=3000):
    """Spearman within days, pooled: ranks demeaned per day, one correlation; the
    permutation shuffles y within each day."""
    days = defaultdict(list)
    for r in rows:
        if xf(r) is not None and yf(r) is not None: days[r["run_date"]].append(r)
    X, Y, blocks = [], [], []
    for d, g in days.items():
        if len(g) < 3: continue
        rx, ry = rank([xf(r) for r in g]), rank([yf(r) for r in g])
        mx, my = sum(rx) / len(g), sum(ry) / len(g)
        s = len(X); X += [a - mx for a in rx]; Y += [b - my for b in ry]
        blocks.append((s, len(X)))
    if len(X) < 8: return None
    def corr(Y):
        sxy = sum(a * b for a, b in zip(X, Y)); sxx = sum(a * a for a in X); syy = sum(b * b for b in Y)
        return sxy / math.sqrt(sxx * syy) if sxx and syy else 0
    r0 = corr(Y); k = 0
    for _ in range(perms):
        Yp = Y[:]
        for s, e in blocks:
            seg = Yp[s:e]; random.shuffle(seg); Yp[s:e] = seg
        if abs(corr(Yp)) >= abs(r0) - 1e-12: k += 1
    return (len(X), len(blocks), r0, (k + 1) / (perms + 1))

def tercile(rows, key):
    v = sorted(r[key] for r in rows if r.get(key) is not None)
    if len(v) < 9: return None
    return v[len(v) // 3], v[2 * len(v) // 3]

def mcap_band(r):
    m = r.get("mcap")
    if m is None: return None
    return "1 micro <$300m" if m < 3e8 else "2 small $0.3-2b" if m < 2e9 else "3 mid $2-10b" if m < 1e10 else "4 large >$10b"
def adv_band(r):
    a = r.get("adv")
    if a is None: return None
    return "1 <$1m/day" if a < 1e6 else "2 $1-5m" if a < 5e6 else "3 $5-25m" if a < 25e6 else "4 >$25m"
def b(key, thr, lo, hi):
    return lambda r: None if r.get(key) is None else (hi if r[key] >= thr else lo)

CUTS = {
 "session": lambda r: r["session"],
 "side": lambda r: "long" if r["side"] > 0 else "short",
 "session x side": lambda r: r["session"] + " " + ("long" if r["side"] > 0 else "short"),
 "sector": lambda r: r.get("sector"),
 "market cap": mcap_band,
 "turnover": adv_band,
 "weekday of run": lambda r: {"Mon":"1 Mon","Tue":"2 Tue","Wed":"3 Wed","Thu":"4 Thu","Fri":"5 Fri"}[r["weekday"]],
 "20d realised vol (frozen line 58)": b("vol20", 58, "vol <58", "vol >=58"),
 "retail tilt (line 50)": b("retail_tilt", 50, "tilt <50", "tilt >=50"),
 "panel side vs sealed price lean": lambda r: None if r.get("lean_agree") is None else ("agrees with lean" if r["lean_agree"] else "against lean"),
 "findings filed": lambda r: None if r.get("n_findings") is None else ("findings >=5" if r["n_findings"] >= 5 else "findings <5"),
 "option chain": lambda r: "options ok" if r.get("opt_ok") else "no usable chain",
 "implied move": lambda r: None if r.get("implied") is None else ("implied <6%" if r["implied"] < 6 else "implied 6-10%" if r["implied"] < 10 else "implied >=10%"),
 "20d run-up vs side": lambda r: None if not r.get("runup_20d") else ("with the run-up" if (r["runup_20d"] > 0) == (r["side"] > 0) else "against the run-up"),
 "5d run-up vs side": lambda r: None if not r.get("runup_5d") else ("with the 5d move" if (r["runup_5d"] > 0) == (r["side"] > 0) else "against the 5d move"),
 "distance from 52w high": lambda r: None if r.get("from_high") is None else ("within 10% of high" if r["from_high"] > -10 else "10-30% below" if r["from_high"] > -30 else ">30% below high"),
 "side x near high": lambda r: None if r.get("from_high") is None else (("long" if r["side"]>0 else "short") + (" near high" if r["from_high"] > -10 else " off high")),
 "share price": lambda r: None if not r.get("spot") else ("price <$10" if r["spot"] < 10 else "price $10-50" if r["spot"] < 50 else "price >=$50"),
 "judge spread (sd of pct)": lambda r: None if r.get("sd") is None else ("judges close (sd<15)" if r["sd"] < 15 else "judges apart (sd>=15)"),
 "past prints mostly up": lambda r: None if r.get("hist_up") is None or (r.get("hist_n") or 0) < 4 else ("history >=60% up" if r["hist_up"] >= .6 else "history <60% up"),
 "side x past prints": lambda r: None if r.get("hist_up") is None or (r.get("hist_n") or 0) < 4 else (("long" if r["side"]>0 else "short") + (" hist up" if r["hist_up"] >= .6 else " hist not up")),
}
LEVELS = [("all", 0), (">=60", 60), (">=80", 80)]

for v in VERS:
    rows = [r for r in R if r["version"] == v]
    days = sorted({r["run_date"] for r in rows})
    print(f"\n=== {v}: {len(rows)} names, {len(days)} run days {days[0]} to {days[-1]} ===")
    print("within-day rho, signed panel_pct vs move:", pooled_rho(rows, lambda r: r["signed"], lambda r: r["move"]))
    print("within-day rho, searcher impact_sum vs move:", pooled_rho(rows, lambda r: r["searcher_sum"], lambda r: r["move"]))
    print("within-day rho, -runup_20d (free control) vs move:", pooled_rho(rows, lambda r: None if r.get("runup_20d") is None else -r["runup_20d"], lambda r: r["move"]))
    print("within-day rho, panel_pct vs sign right:", pooled_rho(rows, lambda r: r["pct"], lambda r: 1.0 if r["ret"] > 0 else 0.0))
    print("controls: short everything", fmt(cell([-r["move"] for r in rows])), "| long everything", fmt(cell([r["move"] for r in rows])))
    print("bands of panel_pct:")
    for lo, hi in [(0, 40), (40, 60), (60, 70), (70, 80), (80, 90), (90, 101)]:
        print(f"  {lo:>3}-{hi:<3}", fmt(cell([r["ret"] for r in rows if lo <= r["pct"] < hi])))
    for lab, t in LEVELS:
        g = [r for r in rows if r["pct"] >= t]
        byday = defaultdict(list)
        for r in g: byday[r["run_date"]].append(r["ret"])
        print(f"  {lab:>5} per name", fmt(cell([r['ret'] for r in g])), "| per day (equal weight)", fmt(cell([sum(x)/len(x) for x in byday.values()])))

print("\n\n=== CUTS: v2 | v3 side by side, at each level ===")
for name, f in CUTS.items():
    for lab, t in LEVELS:
        print(f"\n-- {name} [{lab}]")
        keys = sorted({f(r) for r in R if f(r) is not None})
        for k in keys:
            cs = []
            for v in VERS:
                g = [r["ret"] for r in R if r["version"] == v and r["pct"] >= t and f(r) == k]
                cs.append(cell(g))
            if max((c[0] if c else 0) for c in cs) < 4: continue
            print(f"  {str(k):<24} {fmt(cs[0])} | {fmt(cs[1])}")
