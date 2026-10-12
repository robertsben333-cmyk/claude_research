"""Why is impact_sum smaller in Europe? |impact_sum| = findings x size per finding x coherence,
where coherence = |sum f| / sum |f| (1 = all findings point one way, 0 = they cancel).
One unit is one hunt file. Validation runs (synthetic findings) and non-events are left out."""
import json, glob, statistics as st, collections, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]
DIRS = {'edge': 'US', 'edge-panel': 'US searcher', 'europe': 'EU', 'japan': 'JP', 'australia': 'AU', 'canada': 'CA'}
def era(day):
    if day <= '2026-09-22': return '1 Opus 5'
    if day <= '2026-09-30': return '2 Sept Opus 5.5'
    return '3 core (Oct)'
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None
rows = []
for d, mk in DIRS.items():
    for run in glob.glob(str(R / f'research/2026/*/*/{d}')):
        day = Path(run).parent.name
        u = Path(run) / 'universe.json'
        if u.exists():
            try:
                if json.load(open(u)).get('validation_only'): continue
            except Exception: pass
        sc = Path(run) / 'edge-scores.json'
        rank = {}
        if sc.exists():
            for r in json.load(open(sc)).get('ranking', []): rank[r['ticker']] = r
        for h in glob.glob(run + '/hunts/*.json'):
            try: H = json.load(open(h))
            except Exception: continue
            if not isinstance(H, dict): continue
            t = H.get('ticker') or Path(h).stem
            r = rank.get(t, {})
            if H.get('event_confirmed') is False or r.get('rankable') is False: continue
            b = Path(run) / 'baselines' / f'{t}.json'
            hist = None; sub = None
            if b.exists():
                try:
                    B = json.load(open(b)); hist = num((B.get('history') or {}).get('median_abs_move_pct'))
                    sub = B.get('submarket')
                except Exception: pass
            f = [num(x.get('expected_impact_pct')) for x in H.get('findings') or []]
            f = [x for x in f if x is not None]
            rows.append(dict(mk=mk, sub=(sub or (H.get('market') or '')).lower() if mk == 'EU' else None, day=day, era=era(day),
                             n=len(f), f=f, s=sum(f), abs_move=num(H.get('abs_move_pct')), p_up=num(H.get('p_up')),
                             rej=len(H.get('rejected_candidates') or []), srcs=num(H.get('sources_used')),
                             nothing=len(H.get('searched_and_found_nothing') or []), outside=len(H.get('outside_window') or []),
                             hist=hist))
md = lambda v: round(st.median(v), 2) if v else None
mn = lambda v: round(st.mean(v), 2) if v else None
def summary(g):
    allf = [abs(x) for r in g for x in r['f']]
    withf = [r for r in g if r['n']]
    coh = [abs(r['s']) / sum(abs(x) for x in r['f']) for r in withf if sum(abs(x) for x in r['f'])]
    rel = [abs(x) / r['hist'] for r in g for x in r['f'] if r['hist']]
    am = [r['abs_move'] for r in g if r['abs_move'] is not None]
    cert = [abs(2 * r['p_up'] / 100 - 1) for r in g if r['p_up'] is not None]
    return dict(hunts=len(g), zero=f"{100*sum(r['n']==0 for r in g)/len(g):.0f}%", findings=mn([r['n'] for r in g]),
                size_med=md(allf), size_mean=mn(allf), coherence=mn(coh), abs_sum_med=md([abs(r['s']) for r in g]),
                abs_sum_mean=mn([abs(r['s']) for r in g]), hist_move=md([r['hist'] for r in g if r['hist']]),
                size_per_hist=md(rel), abs_move=md(am), certainty=mn(cert), rejected=mn([r['rej'] for r in g]),
                nothing=mn([r['nothing'] for r in g]), outside=mn([r['outside'] for r in g]), sources=md([r['srcs'] for r in g if r['srcs']]))
cols = ['hunts','zero','findings','size_med','size_mean','coherence','abs_sum_med','abs_sum_mean','hist_move','size_per_hist','abs_move','certainty','rejected','nothing','outside','sources']
def table(groups, title):
    print('\n## ' + title); print(f"{'group':28s}" + ''.join(f'{c[:9]:>10s}' for c in cols))
    out = {}
    for k in sorted(groups):
        if len(groups[k]) < 3: continue
        s = summary(groups[k]); out[' / '.join(k)] = s
        print(f"{' / '.join(k):28s}" + ''.join(f"{str(s[c]):>10s}" for c in cols))
    return out
by = collections.defaultdict(list); bysub = collections.defaultdict(list)
for r in rows:
    by[(r['era'], r['mk'])].append(r)
    if r['mk'] == 'EU': bysub[(r['era'], r['sub'])].append(r)
res = {'by_market': table(by, 'per era and market'), 'eu_by_country': table(bysub, 'Europe per country')}
# a decomposition of the US/EU gap in log terms, per era: findings x size x coherence (means)
print('\n## Share of the gap in mean |impact_sum| (US / EU), log decomposition, hunts with >=1 finding')
for e in sorted({r['era'] for r in rows}):
    parts = {}
    for mk in ('US', 'EU'):
        g = [r for r in rows if r['era'] == e and r['mk'] == mk and r['n']]
        if len(g) < 5: break
        n = st.mean(r['n'] for r in g); sz = st.mean(abs(x) for r in g for x in r['f'])
        tot = st.mean(abs(r['s']) for r in g); parts[mk] = (n, sz, tot / (n * sz), tot)
    if len(parts) < 2: continue
    import math
    L = {k: math.log(parts['US'][i] / parts['EU'][i]) for i, k in enumerate(['findings', 'size', 'coherence'])}
    tot = sum(L.values())
    print(f"{e}: US/EU = {parts['US'][3]/parts['EU'][3]:.2f}x  " + '  '.join(f"{k} {math.exp(v):.2f}x ({100*v/tot:.0f}%)" for k, v in L.items())
          + f"  | zero-finding hunts not included")
    res.setdefault('gap', {})[e] = {k: round(math.exp(v), 2) for k, v in L.items()}
json.dump(res, open(Path(__file__).with_name('decomposition.json'), 'w'), indent=1)

# ---------- the judges: |impact| = abs_move_pct x |2 p_up/100 - 1|, per region
print('\n## Judges: |impact| = abs_move x certainty, re-judge (231 names) and live panels (Oct)')
RJ = R / 'research/analyses/rejudge-four-models'
key = {x['id']: x for x in json.load(open(RJ / 'key.json'))}
ARM = {'opus5': 'opus5', 'opus': 'opus55', 'sonnet': 'sonnet55', 'fable': 'fable51'}
jr = collections.defaultdict(list)
for f in glob.glob(str(RJ / 'out-*.json')):
    m = ARM[Path(f).stem.split('-')[-1]]
    for o in json.load(open(f)):
        k = key.get(o['id'])
        if not k or k.get('anon'): continue
        base = R / k['baseline'] if k.get('baseline') else None
        hist = None
        if base and base.exists():
            try: hist = num((json.load(open(base)).get('history') or {}).get('median_abs_move_pct'))
            except Exception: pass
        nf = None
        jr[('rejudge', k['region'], m)].append(dict(am=num(o.get('abs_move_pct')), p=num(o.get('p_up')), imp=num(o.get('impact_sum')), hist=hist, mv=abs(k['move'])))
for d, mk in [('edge-panel', 'us'), ('europe', 'europe'), ('japan', 'japan'), ('canada', 'canada')]:
    for run in glob.glob(str(R / f'research/2026/10/*/{d}/panel')):
        for m in ('opus5', 'opus55', 'sonnet55', 'fable51'):
            f = Path(run) / f'{m}.json'
            if not f.exists(): continue
            for o in json.load(open(f)):
                jr[('live', mk, m)].append(dict(am=num(o.get('abs_move_pct')), p=num(o.get('p_up')), imp=num(o.get('impact_sum')), hist=None, mv=None))
print(f"{'set / region / judge':34s}{'n':>5s}{'abs_move':>9s}{'certain':>9s}{'|imp|':>8s}{'hist':>7s}{'am/hist':>8s}{'real|mv|':>9s}")
jout = {}
for k in sorted(jr):
    g = jr[k]
    am = [x['am'] for x in g if x['am'] is not None]; ce = [abs(2 * x['p'] / 100 - 1) for x in g if x['p'] is not None]
    im = [abs(x['imp']) for x in g if x['imp'] is not None]; hi = [x['hist'] for x in g if x['hist']]
    ah = [x['am'] / x['hist'] for x in g if x['hist'] and x['am'] is not None]; mv = [x['mv'] for x in g if x['mv'] is not None]
    s = dict(n=len(g), abs_move=md(am), certainty=mn(ce), abs_impact=mn(im), hist=md(hi), am_per_hist=md(ah), real_move=md(mv))
    jout[' / '.join(k)] = s
    print(f"{' / '.join(k):34s}{s['n']:5d}{str(s['abs_move']):>9s}{str(s['certainty']):>9s}{str(s['abs_impact']):>8s}{str(s['hist']):>7s}{str(s['am_per_hist']):>8s}{str(s['real_move']):>9s}")
res['judges'] = jout
json.dump(res, open(Path(__file__).with_name('decomposition.json'), 'w'), indent=1)
