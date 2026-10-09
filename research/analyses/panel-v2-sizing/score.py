#!/usr/bin/env python3
"""Would the four-model panel do better on impact_sum (v2) than on impact_scaled (v3)?

Four judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) each judged the same 128 Opus
5-era names under ONE brief (`../rejudge-opus55-v2-sizing/brief.md`) that asks for both
measurements in one session: every finding sized on its own (sum = impact_sum, v2) and,
separately, abs_move_pct and p_up (impact_scaled, v3). Opus 5.5's outputs are the ones
already in `../rejudge-opus55-v2-sizing/out-NN.json`; the other three are `out-NN-<m>.json`
here. So the only thing that differs between the two panels is which of the two numbers
each member hands in.

Arms, all gross, sign(score) x realised move, US on the strategy exit and the $200k
turnover floor, Europe on its resolver window (helpers as in ../rejudge-four-models):

  live            the Opus 5 hunt's own impact_sum
  <m>_sum         member m, v2
  <m>_scaled      member m, v3
  panel_sum       signed median of the members' v2 sizes, each over its own rms
  panel_scaled    the same on v3
  panel_v3_old    the live E-P recipe on the earlier four-model re-judge (v3 core only)

Selection as stage E-P runs it: consensus_k = members putting the name in their own top
20% (by |size|, within region) on the panel's side; selected at k >= 3.

    python3 score.py      # writes scores.json, prints the tables
"""
import glob, json, math, os, random, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(D, '..', 'rejudge-opus55-v2-sizing')
OLD = os.path.join(D, '..', 'rejudge-four-models')
key = {r['id']: r for r in json.load(open(os.path.join(OLD, 'key.json')))}
pid = {r.get('pid', r['id']): r['id'] for r in key.values()}
MEM = ['opus5', 'opus55', 'sonnet55', 'fable51']
OLD_TAG = {'opus5': 'opus5', 'opus55': 'opus', 'sonnet55': 'sonnet', 'fable51': 'fable'}
sgn = lambda x: (x > 0) - (x < 0)


def load_member(m):
    files = (sorted(glob.glob(os.path.join(V2, 'out-[0-9][0-9].json'))) if m == 'opus55'
             else sorted(glob.glob(os.path.join(D, f'out-[0-9][0-9]-{m}.json'))))
    s, sc, nf, bad = {}, {}, {}, []
    for f in files:
        for o in json.load(open(f)):
            i = pid.get(o.get('id'))
            if i is None:
                bad.append(f'{m}: unknown id {o.get("id")}'); continue
            fs = o.get('findings') or []
            tot = round(sum(float(x.get('expected_impact_pct') or 0) for x in fs), 3)
            if abs(tot - float(o.get('impact_sum') or 0)) > 0.05:
                bad.append(f'{m} {o["id"]}: impact_sum {o.get("impact_sum")} != findings {tot}')
            s[i] = tot
            nf[i] = sum(1 for x in fs if float(x.get('expected_impact_pct') or 0) != 0)
            a, p = o.get('abs_move_pct'), o.get('p_up')
            if isinstance(a, (int, float)) and isinstance(p, (int, float)):
                sc[i] = (2 * p / 100 - 1) * a
    return s, sc, nf, bad


def load_old(m):
    out = {}
    for f in glob.glob(os.path.join(OLD, f'out-*-{OLD_TAG[m]}.json')):
        for o in json.load(open(f)):
            if o['id'] in pid:
                out[pid[o['id']]] = float(o.get('impact_sum') or 0)
    return out


packs = [p['id'] for f in glob.glob(os.path.join(V2, 'packs-*.json')) for p in json.load(open(f))]
expected = {pid[x] for x in packs if x in pid}
SUM, SCA, NF, BAD = {}, {}, {}, []
for m in MEM:
    SUM[m], SCA[m], NF[m], b = load_member(m)
    BAD += b
OLDV3 = {m: load_old(m) for m in MEM}
ids = sorted(expected.intersection(*[set(SUM[m]) for m in MEM], *[set(SCA[m]) for m in MEM],
                                   *[set(OLDV3[m]) for m in MEM]))
ids = [i for i in ids if key[i]['region'] != 'us' or (key[i].get('dollar_vol') or 0) >= 2e5]
missing = {m: sorted(expected - set(SUM[m])) for m in MEM}


def zed(d):
    rms = math.sqrt(st.mean(d[i] ** 2 for i in ids)) or 1
    return {i: d[i] / rms for i in ids}


def region(i): return key[i]['region'] == 'us'


def topset(score, share=0.2):
    out, B = set(), {}
    for i in ids: B.setdefault(region(i), []).append(i)
    for v in B.values():
        k = max(1, round(share * len(v)))
        r = sorted((i for i in v if score[i] != 0), key=lambda i: (-abs(score[i]), i))
        out |= set(r[:k])
    return out


def panel(members):
    z = {m: zed(d) for m, d in members.items()}
    med = {i: st.median(z[m][i] for m in z) for i in ids}
    tops = {m: topset(z[m]) for m in z}
    k = {i: sum(i in tops[m] and sgn(z[m][i]) == sgn(med[i]) != 0 for m in z) for i in ids}
    return med, k, z


arms = {'live': {i: float(key[i]['live'] or 0) for i in ids}}
for m in MEM:
    arms[f'{m}_sum'] = {i: SUM[m][i] for i in ids}
    arms[f'{m}_scaled'] = {i: SCA[m][i] for i in ids}
P = {'panel_sum': panel({m: SUM[m] for m in MEM}),
     'panel_scaled': panel({m: SCA[m] for m in MEM}),
     'panel_v3_old': panel({m: OLDV3[m] for m in MEM})}
for a, (med, k, z) in P.items():
    arms[a] = med


def rank(a):
    s = sorted(range(len(a)), key=lambda i: a[i]); r = [0] * len(a); i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[s[j + 1]] == a[s[i]]: j += 1
        for q in range(i, j + 1): r[s[q]] = (i + j) / 2
        i = j + 1
    return r


def sp(x, y):
    a, b = rank(x), rank(y); ma, mb = st.mean(a), st.mean(b)
    d = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))
    return sum((p - ma) * (q - mb) for p, q in zip(a, b)) / d if d else 0


def dayrho(score, sub, perm=2000):
    Dd = {}
    for i in sub: Dd.setdefault((key[i]['region'], key[i]['day']), []).append(i)
    Dd = [v for v in Dd.values() if len(v) >= 3]
    obs = st.mean(sp([score[i] for i in v], [key[i]['move'] for i in v]) for v in Dd)
    random.seed(3); c = 0
    for _ in range(perm):
        c += st.mean(sp(random.sample([score[i] for i in v], len(v)), [key[i]['move'] for i in v]) for v in Dd) >= obs
    return round(obs, 3), round(c / perm, 3)


def book(sel, score):
    ret = [sgn(score[i]) * key[i]['move'] for i in sel if sgn(score[i])]
    if not ret: return {'n': 0}
    n = len(ret); mu = st.mean(ret)
    t = mu / (st.stdev(ret) / math.sqrt(n)) if n > 2 and st.stdev(ret) > 0 else None
    return {'n': n, 'hits': sum(x > 0 for x in ret), 'mean': round(mu, 2), 't': round(t, 2) if t else None}


def band(score, lo, hi, sub):
    out, B = [], {}
    for i in sub: B.setdefault(region(i), []).append(i)
    for v in B.values():
        r = sorted((i for i in v if score[i] != 0), key=lambda i: (-abs(score[i]), i)); N = len(v)
        out += [i for j, i in enumerate(r) if lo * N <= j < hi * N]
    return out


def fmt(b):
    if not b.get('n'): return '-'
    return f"{b['hits']}/{b['n']} {b['mean']:+.2f}" + (f" t{b['t']:.1f}" if b.get('t') is not None else '')


groups = {'all': ids, 'us': [i for i in ids if region(i)],
          'us_clean': [i for i in ids if region(i) and not key[i].get('leak') and not i.startswith('anon/')]}
out = {'n': len(ids), 'problems': BAD, 'missing': missing, 'groups': {}}
for g, sub in groups.items():
    G = out['groups'][g] = {'n': len(sub), 'short_all': round(st.mean(-key[i]['move'] for i in sub), 2), 'arms': {}, 'consensus': {}}
    print(f"\n=== {g}  n={len(sub)}  short-all {G['short_all']:+.2f}")
    print(f"{'arm':16s} {'rho (p)':>15s} | {'top10%':>16s} {'top20%':>16s} {'20-50%':>16s} {'50-100%':>16s}")
    for a, s in arms.items():
        r = dayrho(s, sub)
        cells = {f'{lo}-{hi}': book(band(s, lo, hi, sub), s) for lo, hi in [(0, .1), (0, .2), (.2, .5), (.5, 1)]}
        G['arms'][a] = {'rho': r, **cells}
        print(f"{a:16s} {r[0]:+.3f} ({r[1]:.2f})  | " + ' '.join(f'{fmt(c):>16s}' for c in cells.values()))
    for a, (med, k, z) in P.items():
        row = {}
        for lab, cond in [('k>=3 (selected)', lambda i: k[i] >= 3), ('k=2', lambda i: k[i] == 2), ('k<=1', lambda i: k[i] <= 1)]:
            row[lab] = book([i for i in sub if cond(i)], med)
        G['consensus'][a] = row
        print(f"  {a:14s} " + '  '.join(f'{lab}: {fmt(b)}' for lab, b in row.items()))

# scale and agreement between the two measurements, per member
print('\n=== per member: v2 against v3 (all names)')
out['members'] = {}
for m in MEM:
    a = [SUM[m][i] for i in ids]; b = [SCA[m][i] for i in ids]
    row = {'median_abs_sum': round(st.median(abs(x) for x in a), 2), 'median_abs_scaled': round(st.median(abs(x) for x in b), 2),
           'findings_per_name': round(st.mean(NF[m][i] for i in ids), 2), 'rho_sum_scaled': round(sp(a, b), 3),
           'sign_agree': round(sum(sgn(x) == sgn(y) for x, y in zip(a, b)) / len(a), 3),
           'zeros_sum': sum(x == 0 for x in a), 'zeros_scaled': sum(x == 0 for x in b)}
    out['members'][m] = row
    print(m, row)
ps, pc = P['panel_sum'][1], P['panel_scaled'][1]
sel_s = {i for i in ids if ps[i] >= 3}; sel_c = {i for i in ids if pc[i] >= 3}
out['overlap'] = {'selected_sum': len(sel_s), 'selected_scaled': len(sel_c), 'both': len(sel_s & sel_c)}
print('\nselected by panel_sum', len(sel_s), ' by panel_scaled', len(sel_c), ' both', len(sel_s & sel_c))
print('problems:', len(BAD), BAD[:5], ' missing:', {m: len(v) for m, v in missing.items()})
json.dump(out, open(os.path.join(D, 'scores.json'), 'w'), indent=1)
