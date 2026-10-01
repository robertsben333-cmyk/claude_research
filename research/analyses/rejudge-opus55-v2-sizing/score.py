#!/usr/bin/env python3
"""Score the Opus 5.5 two-measurement re-judge on the Opus 5 days, against four arms.

Arms (gross returns, sign(score) x realised move, US on the strategy exit and the $200k
turnover floor, Europe on its resolver window; the same conventions as
../rejudge-four-models/score_full.py, whose helpers are copied here unchanged):

  live           the impact_sum the Opus 5 hunt emitted live (version 2 sizing)
  opus5_v3       Opus 5 re-judge of the same evidence under the morning's core (v3)
  opus55_v3      Opus 5.5 re-judge under the morning's core (v3): the collapse case
  opus55_v2      THIS RUN: Opus 5.5, findings sized on their own, their sum
  opus55_scaled  THIS RUN: (2 * p_up / 100 - 1) * abs_move_pct, recomputed here

The question: does Opus 5.5 with findings sized on their own get back to the live Opus 5
scale and signal, and does its separate scaled number add anything? Only names every
arm covers are scored, so all arms share one sample.

    python3 score.py      # reads out-NN.json, writes scores.json, prints the table
"""
import glob, json, os, random, statistics as st
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '..', 'rejudge-four-models')
key = {r['id']: r for r in json.load(open(os.path.join(SRC, 'key.json')))}
pid = {r.get('pid', r['id']): r['id'] for r in key.values()}

def load_old(model):
    out = {}
    for f in glob.glob(os.path.join(SRC, f'out-*-{model}.json')):
        for o in json.load(open(f)):
            if o['id'] in pid:
                out[pid[o['id']]] = float(o.get('impact_sum') or 0)
    return out

new_sum, new_scaled, nfind, bad = {}, {}, {}, []
for f in sorted(glob.glob(os.path.join(D, 'out-*.json'))):
    for o in json.load(open(f)):
        i = pid.get(o.get('id'))
        if i is None:
            bad.append(o.get('id')); continue
        fs = o.get('findings') or []
        s = round(sum(float(x.get('expected_impact_pct') or 0) for x in fs), 3)
        if abs(s - float(o.get('impact_sum') or 0)) > 0.05:
            bad.append(f"{o['id']}: impact_sum {o.get('impact_sum')} != findings {s}")
        new_sum[i] = s
        nfind[i] = sum(1 for x in fs if float(x.get('expected_impact_pct') or 0) != 0)
        a, p = o.get('abs_move_pct'), o.get('p_up')
        if isinstance(a, (int, float)) and isinstance(p, (int, float)):
            new_scaled[i] = (2 * p / 100 - 1) * a

packs = [p['id'] for f in glob.glob(os.path.join(D, 'packs-*.json')) for p in json.load(open(f))]
expected = {pid[x] for x in packs if x in pid}
missing = sorted(expected - set(new_sum))

arms_all = {'live': {i: float(key[i]['live'] or 0) for i in key},
            'opus5_v3': load_old('opus5'), 'opus55_v3': load_old('opus'),
            'opus55_v2': new_sum, 'opus55_scaled': new_scaled}
ids = sorted(set.intersection(*(set(v) for v in arms_all.values())) & expected)
arms = {a: {i: v[i] for i in ids} for a, v in arms_all.items()}

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
def rets(sc, sub, thr, mv):
    t = [i for i in sub if abs(sc[i]) >= thr and sc[i] != 0 and tradable(i)]
    return [(1 if sc[i] > 0 else -1)*mv[i] for i in t]
def summ(r):
    if not r: return {'n': 0, 'hits': 0, 'mean': None, 't': None}
    sd = st.stdev(r) if len(r) > 1 else 0
    return {'n': len(r), 'hits': sum(x > 0 for x in r), 'mean': st.mean(r),
            't': st.mean(r)/(sd/len(r)**.5) if sd else None}
thresholds = [x/4 for x in range(0, 25)]
MIN_N = 8
def cut_at_share(sc, sub, share):
    t = sorted((abs(sc[i]) for i in sub if sc[i] != 0 and tradable(i)), reverse=True)
    return t[max(1, round(len(t)*share))-1] if t else None
def tstat(r):
    return st.mean(r)/(st.stdev(r)/len(r)**.5) if len(r) >= MIN_N and st.stdev(r) > 0 else None
def best_t(sc, sub, mv):
    ts = [tstat(rets(sc, sub, t, mv)) for t in thresholds]
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
def loo(sc, sub):
    mv = {i: key[i]['move'] for i in sub}; out = []; chosen = []
    for d, v in days_of(sub).items():
        rest = [i for i in sub if i not in set(v)]
        cand = [(st.mean(r), t) for t in thresholds for r in [rets(sc, rest, t, mv)] if len(r) >= MIN_N]
        if not cand: continue
        t = max(cand)[1]; chosen.append(t); out += rets(sc, v, t, mv)
    return summ(out), sorted(set(chosen))

G = {'us': [i for i in ids if key[i]['region'] == 'us'],
     'us_clean': [i for i in ids if key[i]['region'] == 'us' and not key[i].get('anon')],
     'europe': [i for i in ids if key[i]['region'] == 'europe'],
     'all': ids}
nz = [i for i in G['us'] if arms['live'][i] != 0 and tradable(i)]
SHARE = sum(abs(arms['live'][i]) >= 3 for i in nz)/len(nz) if nz else None

res = {}
for g, sub in G.items():
    if not sub: continue
    mv = {i: key[i]['move'] for i in sub}
    tr = [i for i in sub if tradable(i)]
    gg = res[g] = {'n': len(sub), 'short_all': st.mean([-mv[i] for i in tr]) if tr else None}
    for a, sc in arms.items():
        r, p = rho(sc, sub)
        fw = familywise(sc, sub) if g != 'europe' else (None, None)
        cut = cut_at_share(sc, sub, SHARE) if SHARE else None
        l, ch = loo(sc, sub) if g != 'europe' else ({}, [])
        gg[a] = {'zeros': sum(1 for i in sub if sc[i] == 0),
                 'median_abs': st.median([abs(sc[i]) for i in sub]),
                 'share_ge3': sum(1 for i in sub if abs(sc[i]) >= 3)/len(sub),
                 'rho': r, 'p': p, 'ge3': summ(rets(sc, sub, 3.0, mv)),
                 'all_nonzero': summ(rets(sc, sub, 1e-9, mv)),
                 'best_t': fw[0], 'familywise_p': fw[1],
                 'floor_same_share': cut, 'book_same_share': summ(rets(sc, sub, cut, mv)) if cut else None,
                 'loo': l, 'loo_thresholds': ch}
us = G['us']
agree = [i for i in us if new_sum[i] and new_scaled[i]]
out = {'n': len(ids), 'expected': len(expected), 'missing': missing, 'problems': bad,
       'floor_share_live_us': SHARE,
       'findings_per_name_us': st.mean(nfind[i] for i in us) if us else None,
       'sum_vs_scaled_sign_agree_us': (sum((new_sum[i] > 0) == (new_scaled[i] > 0) for i in agree)/len(agree)) if agree else None,
       'sum_vs_scaled_rho_us': sp([new_sum[i] for i in us], [new_scaled[i] for i in us]) if len(us) > 2 else None,
       'groups': res}
json.dump(out, open(os.path.join(D, 'scores.json'), 'w'), indent=1)

f2 = lambda x, k='+.2f': '-' if x is None else format(x, k)
print(f"scored {len(ids)} of {len(expected)} names; missing {len(missing)}; problems {len(bad)}")
for b in bad[:10]: print('  problem:', b)
print(f"3.0 selected {f2(SHARE, '.0%')} of live's nonzero tradable US names")
print(f"US: Opus 5.5 v2 findings per name {f2(out['findings_per_name_us'], '.2f')}; "
      f"impact_sum vs impact_scaled: sign agree {f2(out['sum_vs_scaled_sign_agree_us'], '.0%')}, "
      f"rho {f2(out['sum_vs_scaled_rho_us'], '+.2f')}")
for g, gg in res.items():
    print(f"\n== {g}  n={gg['n']}  short all {f2(gg['short_all'])}%")
    print(f"  {'arm':14s}{'zeros':>6s}{'med|x|':>8s}{'>=3':>6s}{'rho (p)':>16s}   {'>=3 book':>24s}   {'fw p':>6s}   {'LOO':>18s}")
    for a in arms:
        s = gg[a]; b = s['ge3']; l = s['loo'] or {}
        rr = f"{s['rho']:+.3f} ({s['p']:.2f})" if s['rho'] is not None else '-'
        bk = f"{b['hits']}/{b['n']} {f2(b['mean'])}% t {f2(b['t'])}" if b['n'] else '0'
        lo = f"{l.get('n', 0)} {f2(l.get('mean'))}%" if l else '-'
        print(f"  {a:14s}{s['zeros']:6d}{s['median_abs']:8.2f}{s['share_ge3']:6.0%}{rr:>16s}   {bk:>24s}   {f2(s['familywise_p'], '.2f'):>6s}   {lo:>18s}")
