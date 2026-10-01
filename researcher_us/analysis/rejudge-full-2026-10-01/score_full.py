#!/usr/bin/env python3
"""Score the full blinded re-judge and draw the threshold chart.

Arms: live (the impact_sum the original hunt emitted, old prompt, served model of the
day), opus (Opus 5.5 re-judge under the shared core), sonnet (Sonnet 5.5 re-judge).
Return per trade = sign(impact_sum) x realised move. US names use the strategy exit and
the $200k turnover floor the book trades under; other regions use their resolver window.
Only names judged by BOTH models are scored, so the three arms share one sample.
"""
import json, glob, os, random, statistics as st
D = os.path.dirname(os.path.abspath(__file__))
key = {r['id']: r for r in json.load(open(f'{D}/key.json'))}
arms = {'opus': {}, 'sonnet': {}}
for f in glob.glob(f'{D}/out-*-*.json'):
    m = os.path.basename(f)[:-5].split('-')[-1]
    for o in json.load(open(f)):
        arms[m][o['id']] = float(o.get('impact_sum') or 0)
ids = sorted(set(arms['opus']) & set(arms['sonnet']))
arms = {'live': {i: float(key[i]['live'] or 0) for i in ids}, **{k: {i: v[i] for i in ids} for k, v in arms.items()}}
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
def rho(sc, sub):
    days = {}
    for i in sub: days.setdefault((key[i]['region'], key[i]['day']), []).append(i)
    D_ = [([sc[i] for i in v], [key[i]['move'] for i in v]) for v in days.values() if len(v) >= 3]
    if not D_: return None, None
    f = lambda D_: sum(sp(x, y)*len(x) for x, y in D_)/sum(len(x) for x, y in D_)
    o = f(D_); random.seed(1)
    p = sum(1 for _ in range(2000) if abs(f([(x, random.sample(y, len(y))) for x, y in D_])) >= abs(o)-1e-12)/2000
    return o, p
def book(sc, sub, thr):
    t = [i for i in sub if abs(sc[i]) >= thr and sc[i] != 0 and tradable(i)]
    r = [(1 if sc[i] > 0 else -1)*key[i]['move'] for i in t]
    return len(t), (sum(x > 0 for x in r) if r else 0), (st.mean(r) if r else None)
groups = {'all': ids, 'us': [i for i in ids if key[i]['region'] == 'us'],
          'ex_us': [i for i in ids if key[i]['region'] != 'us'],
          'europe': [i for i in ids if key[i]['region'] == 'europe'],
          'apac': [i for i in ids if key[i]['region'] in ('japan', 'australia')]}
thresholds = [x/2 for x in range(0, 13)]
out = {'n': len(ids), 'groups': {}}
for g, sub in groups.items():
    out['groups'][g] = {}
    for a, sc in arms.items():
        r, p = rho(sc, sub)
        out['groups'][g][a] = {'n': len(sub), 'zeros': sum(1 for i in sub if sc[i] == 0),
            'median_abs': st.median([abs(sc[i]) for i in sub]) if sub else None, 'rho': r, 'p': p,
            'curve': [dict(zip(('n', 'hits', 'mean'), book(sc, sub, t)), thr=t) for t in thresholds]}
json.dump(out, open(f'{D}/scores.json', 'w'), indent=1)
for g in groups:
    print(f"== {g}  n={len(groups[g])}")
    for a in arms:
        s = out['groups'][g][a]; c = {x['thr']: x for x in s['curve']}
        fm = lambda t: f"{c[t]['n']:3d} {c[t]['hits']:3d}/{c[t]['n']:<3d} {c[t]['mean']:+6.2f}%" if c[t]['n'] else "  0"
        rr = f"{s['rho']:+.3f} (p {s['p']:.2f})" if s['rho'] is not None else '-'
        print(f"  {a:6s} zeros {s['zeros']:3d} med|x| {s['median_abs']:.2f} rho {rr} | >=0: {fm(0)} | >=1.5: {fm(1.5)} | >=3: {fm(3.0)}")
