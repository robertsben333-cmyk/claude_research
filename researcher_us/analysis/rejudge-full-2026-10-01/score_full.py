#!/usr/bin/env python3
"""Score the full blinded re-judge and feed the threshold chart.

Arms: live (the impact_sum the original hunt emitted, old prompt, served model of the
day), opus (Opus 5.5 re-judge under the shared core), sonnet (Sonnet 5.5 re-judge).
Return per trade = sign(impact_sum) x realised move, gross and net of an assumed cost.
US names use the strategy exit and the $200k turnover floor the book trades under; other
regions use their resolver window. Only names judged by BOTH models are scored, so the
three arms share one sample. Anonymised packs (ids starting `anon/`) map back through
key.json's `pid`.

Three additions over the first pass:
- cost: an assumed round trip by turnover band (COST below), because the spreads the
  ledger measured on real fills are too noisy to fit (17-30% on three of fourteen);
- family-wise p: the best threshold of the grid, tested against the same maximum under
  a within-day shuffle of the moves, so picking the best of 25 cuts is paid for;
- the floor re-derived two ways: the cut at the same share of names that 3.0 selected
  for the live hunt on its Opus 5 days, and a leave-one-day-out choice.
"""
import json, glob, os, random, statistics as st
D = os.path.dirname(os.path.abspath(__file__))
key = {r['id']: r for r in json.load(open(f'{D}/key.json'))}
pid = {r.get('pid', r['id']): r['id'] for r in key.values()}
# file suffix -> arm; the order is the chart's fixed series order
ARMS = {'opus5': 'Opus 5', 'opus': 'Opus 5.5', 'sonnet': 'Sonnet 5.5', 'fable': 'Fable 5.1'}
arms = {k: {} for k in ARMS}
for f in glob.glob(f'{D}/out-*-*.json'):
    m = os.path.basename(f)[:-5].split('-')[-1]
    for o in json.load(open(f)):
        if o['id'] in pid:
            arms[m][pid[o['id']]] = float(o.get('impact_sum') or 0)
arms = {k: v for k, v in arms.items() if v}
# score only names every present re-judge covered, so all arms share one sample
ids = sorted(set.intersection(*(set(v) for v in arms.values())))
arms = {'live': {i: float(key[i]['live'] or 0) for i in ids}, **{k: {i: v[i] for i in ids} for k, v in arms.items()}}
LABEL = {'live': 'Live hunt', **ARMS}

# Assumed round-trip cost in % of notional, by 20-day median turnover. An assumption,
# not a measurement: it is the same order as a quoted half-spread twice over.
COST = [(1e6, 2.0), (5e6, 1.0), (25e6, 0.5), (float('inf'), 0.2)]
def cost(i):
    dv = key[i].get('dollar_vol') or 0
    return next(c for lim, c in COST if dv < lim)
def tradable(i):
    r = key[i]
    return r['region'] != 'us' or (r.get('dollar_vol') or 0) >= 2e5
def rk(a):
    s = sorted(range(len(a)), key=lambda i: a[i]); r = [0]*len(a); i = 0
    while i < len(a):
        j = i
        while j+1 < len(a) and a[s[j+1]] == a[s[i]]: j += 1
        for k in range(i, j+1): r[s[k]] = (i+j)/2
        i = j+1
    return r
def sp(x, y):
    a, b = rk(x), rk(y); ma, mb = st.mean(a), st.mean(b)
    d = (sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))**.5
    return sum((p-ma)*(q-mb) for p, q in zip(a, b))/d if d else 0
def days_of(sub):
    d = {}
    for i in sub: d.setdefault((key[i]['region'], key[i]['day']), []).append(i)
    return d
def rho(sc, sub):
    D_ = [([sc[i] for i in v], [key[i]['move'] for i in v]) for v in days_of(sub).values() if len(v) >= 3]
    if not D_: return None, None
    f = lambda D_: sum(sp(x, y)*len(x) for x, y in D_)/sum(len(x) for x, y in D_)
    o = f(D_); random.seed(1)
    p = sum(1 for _ in range(2000) if abs(f([(x, random.sample(y, len(y))) for x, y in D_])) >= abs(o)-1e-12)/2000
    return o, p
def rets(sc, sub, thr, mv, net):
    t = [i for i in sub if abs(sc[i]) >= thr and sc[i] != 0 and tradable(i)]
    return [(1 if sc[i] > 0 else -1)*mv[i] - (cost(i) if net else 0) for i in t]
def summ(r):
    if not r: return {'n': 0, 'hits': 0, 'mean': None, 'se': None}
    return {'n': len(r), 'hits': sum(x > 0 for x in r), 'mean': st.mean(r),
            'se': st.stdev(r)/len(r)**.5 if len(r) > 1 else None}
thresholds = [x/4 for x in range(0, 25)]          # family-wise and leave-one-day-out
fine = [round(x/10, 1) for x in range(0, 61)]      # the drawn curves
pcts = list(range(0, 100, 10))
MIN_N = 8
def cut_at_share(sc, sub, share):
    t = sorted((abs(sc[i]) for i in sub if sc[i] != 0 and tradable(i)), reverse=True)
    return t[max(1, round(len(t)*share))-1] if t else None
def tstat(r):
    return st.mean(r)/(st.stdev(r)/len(r)**.5) if len(r) >= MIN_N and st.stdev(r) > 0 else None
def best_t(sc, sub, mv):
    ts = [tstat(rets(sc, sub, t, mv, True)) for t in thresholds]
    ts = [t for t in ts if t is not None]
    return max(ts) if ts else None
def familywise(sc, sub, n=1000):
    mv = {i: key[i]['move'] for i in sub}
    o = best_t(sc, sub, mv)
    if o is None: return None, None
    random.seed(2); hits = 0; dd = list(days_of(sub).values())
    for _ in range(n):
        m2 = {}
        for v in dd:
            s = random.sample([mv[i] for i in v], len(v)); m2.update(zip(v, s))
        b = best_t(sc, sub, m2)
        hits += b is not None and b >= o
    return o, hits/n
def loo_floor(sc, sub):
    """Leave one day out: pick the threshold with the best net mean on the other days
    (at least MIN_N trades), trade the held-out day at it. Returns the pooled
    out-of-sample trades and the thresholds chosen."""
    mv = {i: key[i]['move'] for i in sub}; out = []; chosen = []
    for d, v in days_of(sub).items():
        rest = [i for i in sub if i not in set(v)]
        cand = [(st.mean(r), t) for t in thresholds for r in [rets(sc, rest, t, mv, True)] if len(r) >= MIN_N]
        if not cand: continue
        t = max(cand)[1]; chosen.append(t)
        out += rets(sc, v, t, mv, True)
    return summ(out), chosen
G = {'all': ids, 'us': [i for i in ids if key[i]['region'] == 'us'],
     'ex_us': [i for i in ids if key[i]['region'] != 'us'],
     'europe': [i for i in ids if key[i]['region'] == 'europe'],
     'apac': [i for i in ids if key[i]['region'] in ('japan', 'australia')],
     # the hunter model moved to Opus 5.5 between stage E's 09-22 run and its 09-23 run
     'us_opus5_era': [i for i in ids if key[i]['region'] == 'us' and key[i]['day'] < '2026-09-23'],
     'us_opus55_era': [i for i in ids if key[i]['region'] == 'us' and key[i]['day'] >= '2026-09-23'],
     # the names once excluded for leakage, judged from anonymised packs
     'anonymised': [i for i in ids if key[i].get('anon')]}
# share of the live hunt's nonzero tradable US names that 3.0 selected on its Opus 5 days
e5 = G['us_opus5_era']; nz = [i for i in e5 if arms['live'][i] != 0 and tradable(i)]
SHARE = sum(abs(arms['live'][i]) >= 3 for i in nz)/len(nz)
out = {'n': len(ids), 'arms': {a: LABEL[a] for a in arms}, 'cost_assumption': COST, 'floor_share': SHARE, 'groups': {}}
for g, sub in G.items():
    if not sub: continue
    mv = {i: key[i]['move'] for i in sub}
    tr = [i for i in sub if tradable(i)]
    gg = out['groups'][g] = {'short_all': st.mean([-mv[i] for i in tr]) if tr else None,
                             'short_all_net': st.mean([-mv[i]-cost(i) for i in tr]) if tr else None}
    for a, sc in arms.items():
        r, p = rho(sc, sub)
        fw = familywise(sc, sub) if g in ('all', 'us', 'ex_us') else (None, None)
        cut = cut_at_share(sc, sub, SHARE)
        loo, chosen = loo_floor(sc, sub) if g in ('all', 'us', 'ex_us') else ({}, [])
        gg[a] = {'n': len(sub), 'zeros': sum(1 for i in sub if sc[i] == 0),
            'median_abs': st.median([abs(sc[i]) for i in sub]), 'rho': r, 'p': p,
            'best_t_net': fw[0], 'familywise_p': fw[1],
            'floor_same_share': cut, 'book_same_share_net': summ(rets(sc, sub, cut, mv, True)) if cut else None,
            'loo_net': loo, 'loo_thresholds': sorted(set(chosen)),
            'curve': [dict(thr=t, **summ(rets(sc, sub, t, mv, False)),
                           net=summ(rets(sc, sub, t, mv, True))['mean']) for t in fine],
            'pct_curve': [dict(pct=q, **summ(rets(sc, sub, cut_at_share(sc, sub, (100-q)/100) or 1e9, mv, False)),
                               net=summ(rets(sc, sub, cut_at_share(sc, sub, (100-q)/100) or 1e9, mv, True))['mean'])
                          for q in pcts]}
json.dump(out, open(f'{D}/scores.json', 'w'), indent=1)
f2 = lambda x: '-' if x is None else f'{x:+.2f}'
print(f"n={len(ids)}  3.0 selected {SHARE:.0%} of live's nonzero tradable US names on its Opus 5 days")
for g in out['groups']:
    gg = out['groups'][g]
    print(f"== {g}  n={len(G[g])}  short all {f2(gg['short_all'])}% gross, {f2(gg['short_all_net'])}% net")
    for a in arms:
        s = gg[a]; c = {round(x['thr'], 1): x for x in s['curve']}
        fm = lambda t: f"{c[t]['n']:3d} {c[t]['hits']:3d}/{c[t]['n']:<3d} {c[t]['mean']:+6.2f}% net {c[t]['net']:+6.2f}%" if c[t]['n'] else "  0"
        rr = f"{s['rho']:+.3f} (p {s['p']:.2f})" if s['rho'] is not None else '-'
        b = s['book_same_share_net'] or {}
        print(f"  {a:6s} zeros {s['zeros']:3d} med|x| {s['median_abs']:.2f} rho {rr} | >=0: {fm(0)} | >=3: {fm(3.0)}")
        extra = f"         floor at same share {f2(s['floor_same_share'])} -> {b.get('n',0)} names net {f2(b.get('mean'))}%"
        if s['familywise_p'] is not None:
            l = s['loo_net']
            extra += f" | best net t {s['best_t_net']:.2f} familywise p {s['familywise_p']:.2f} | leave-one-day-out {l.get('n',0)} trades net {f2(l.get('mean'))}% (thr {s['loo_thresholds']})"
        print(extra)
