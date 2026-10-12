"""Per country: is the shared 'top 20%' line (panel) and the 2.8 floor (hunter) on the right scale?"""
import json, glob, math, statistics as st, sys, collections
from pathlib import Path
R = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(R/'researcher_us/scripts')); import panel_score as PS
med = lambda v: round(st.median(v), 2) if v else None
def q(v, p): v = sorted(v); return round(v[min(len(v)-1, int(p*len(v)))], 2) if v else None

# ---------- 1. scale per country: expected (baseline history) and realised
exp = collections.defaultdict(list)   # country -> baseline median abs move per hunted name
for mk, d in [('us','edge'),('eu','europe'),('jp','japan'),('au','australia'),('ca','canada')]:
    for run in glob.glob(str(R/f'research/*/*/*/{d}')):
        u = Path(run)/'universe.json'
        if u.exists():
            try:
                if json.load(open(u)).get('validation_only'): continue
            except Exception: pass
        for b in glob.glob(run+'/baselines/*.json'):
            try: B = json.load(open(b))
            except Exception: continue
            h = (B.get('history') or {}).get('median_abs_move_pct')
            sub = B.get('submarket') or (B.get('identity') or {}).get('submarket')
            key = f'eu-{sub}' if mk=='eu' and sub else mk
            if isinstance(h,(int,float)) and h>0: exp[key].append(h)
            if mk=='eu' and isinstance(h,(int,float)) and h>0: exp['eu (all)'].append(h)

M = json.load(open(R/'dashboard/data/markets.json'))['markets']
val = {r['run'] for m in M.values() for r in m['runs'] if r.get('validation_only')}
real = collections.defaultdict(list); vol = collections.defaultdict(list); live = collections.defaultdict(list)
for mk, m in M.items():
    for n in m['names']:
        if n['run'] in val: continue
        key = mk.lower() if mk!='EU' else f"eu-{n.get('submarket')}"
        keys = [key] + (['eu (all)'] if mk=='EU' else [])
        for k in keys:
            if n.get('realised_vol_20d_pct'): vol[k].append(n['realised_vol_20d_pct'])
            if n.get('realised_move_pct') is not None and not n.get('move_pending') and n.get('event_occurred') is not False and n.get('rankable') is not False:
                real[k].append(abs(n['realised_move_pct']))
            if n.get('rankable') is not False and not n.get('sept_opus55') and (n.get('run_date') or '') >= '2026-10-01':
                live[k].append(abs(n.get('impact_sum') or 0))
L = json.load(open(R/'dashboard/data/ledger.json'))
for n in L['names']:
    if n.get('duplicate_event'): continue
    if n.get('mv_close') is not None: real['us'].append(abs(n['mv_close']))
    if n.get('realised_vol_20d'): vol['us'].append(n['realised_vol_20d'])
    if not n.get('sept_opus55') and (n.get('run_date') or '') >= '2026-10-01': live['us'].append(abs(n.get('impact_sum') or 0))

print('\n## 1. Scale per country (median %)')
print(f"{'country':10s} {'n_exp':>5s} {'exp|mv|':>7s} {'n_real':>6s} {'real|mv|':>8s} {'vol20d':>6s} {'n_live':>6s} {'live|imp|':>9s} {'>=2.8':>6s}")
order = ['us','eu (all)','eu-uk','eu-fr','eu-de','eu-se','eu-dk','eu-no','eu-fi','eu-it','eu-es','eu-pl','jp','au','ca']
out1 = {}
for k in order:
    lv = live.get(k, [])
    share = round(100*sum(x>=2.8 for x in lv)/len(lv)) if lv else None
    out1[k] = dict(n_exp=len(exp.get(k,[])), exp=med(exp.get(k,[])), n_real=len(real.get(k,[])), real=med(real.get(k,[])),
                   vol=med(vol.get(k,[])), n_live=len(lv), live=med(lv), share_ge_28=share)
    o = out1[k]
    print(f"{k:10s} {o['n_exp']:5d} {str(o['exp']):>7s} {o['n_real']:6d} {str(o['real']):>8s} {str(o['vol']):>6s} {o['n_live']:6d} {str(o['live']):>9s} {str(share)+'%' if share is not None else '-':>6s}")

# ---------- 2. re-judge: effective top share at the thresholds in use, per region
RJ = R/'research/analyses/rejudge-four-models'
key = {x['id']: x for x in json.load(open(RJ/'key.json'))}
ARM = {'opus5':'opus5','opus':'opus55','sonnet':'sonnet55','fable':'fable51'}
J = {m:{} for m in ARM.values()}
for f in glob.glob(str(RJ/'out-*.json')):
    arm = Path(f).stem.split('-')[-1]
    for o in json.load(open(f)): J[ARM[arm]][o['id']] = o
hist = {'us':'researcher_us','europe':'researcher_europe','japan':'researcher_japan','australia':'researcher_australia'}
thr = {}
for reg, d in hist.items():
    H = json.load(open(R/d/'analysis/panel-history.json'))
    thr[reg] = {m: PS.member_stats(H[m], 200)['q80'] for m in PS.MEMBERS}
def region_of(i):
    k = key[i]; r = k['region']
    if r=='europe':
        h = k['hunter'].split('-')[-1]; return r, f'eu-{h}'
    return r, r
print('\n## 2. Re-judge (231 resolved names): share of each region\'s names in each judge\'s CURRENT top-20% line')
print('   (if the line were on the right scale, ~20% everywhere)')
groups = collections.defaultdict(list)
for i,k in key.items():
    if k.get('anon') or all(i not in J[m] for m in PS.MEMBERS) or k['move'] is None: continue
    reg, sub = region_of(i); groups[reg].append(i)
    if reg=='europe': groups[sub].append(i)
def book(rows):
    if not rows: return '0'
    m = st.mean(rows); h = sum(r>0 for r in rows)
    t = m/(st.stdev(rows)/math.sqrt(len(rows))) if len(rows)>1 and st.stdev(rows)>0 else float('nan')
    return f"{len(rows)} names, {h} right, {m:+.2f}% (t {t:.2f})"
out2 = {}
for g in ['us','europe','eu-uk','eu-fr','eu-de','japan','australia']:
    ids = groups[g]; reg = g if g in thr else 'europe'
    shares = {}; meds = {}
    for m in PS.MEMBERS:
        v = [abs(J[m][i]['impact_sum']) for i in ids if i in J[m]]
        shares[m] = round(100*sum(x>=thr[reg][m] for x in v)/len(v)) if v else None
        meds[m] = med(v)
    # 3-of-4 selection at the current lines, and at a line re-read on this region's own sizes
    sel_cur, sel_own = [], []
    own_q = {m: q([abs(J[m][i]['impact_sum']) for i in ids if i in J[m]], 0.8) for m in PS.MEMBERS}
    for i in ids:
        mem = {m: J[m][i]['impact_sum'] for m in PS.MEMBERS if i in J[m]}
        if len(mem) < 4: continue
        side = (sum(mem.values())>0) - (sum(mem.values())<0)
        if not side: continue
        for lines, bucket in [(thr[reg], sel_cur), (own_q, sel_own)]:
            k_ = sum(abs(v)>=lines[m] and v!=0 and ((v>0)-(v<0))==side for m,v in mem.items())
            if k_>=3: bucket.append(side*key[i]['move'])
    allsign = []
    for i in ids:
        mem = [J[m][i]['impact_sum'] for m in PS.MEMBERS if i in J[m]]
        s = (sum(mem)>0)-(sum(mem)<0)
        if s: allsign.append(s*key[i]['move'])
    out2[g] = dict(n=len(ids), median_abs_move=med([abs(key[i]['move']) for i in ids]), judge_median_abs_impact=meds,
                   share_in_current_top=shares, own_q80=own_q, sel_current=book(sel_cur), sel_own=book(sel_own), all_names=book(allsign))
    print(f"\n{g}: n={len(ids)}, median |move| {out2[g]['median_abs_move']}%")
    print('   judge median |impact|   ', meds)
    print('   share >= current line    ', {m: f'{s}%' for m,s in shares.items()})
    print('   current line             ', {m: round(v,2) for m,v in thr[reg].items()})
    print('   own p80 on this region   ', own_q)
    print('   3/4 at current lines     ', out2[g]['sel_current'])
    print('   3/4 at own-region p80    ', out2[g]['sel_own'])
    print('   panel sign, every name   ', out2[g]['all_names'])

# ---------- 3. live panel days so far: selection rate per market
print('\n## 3. Live panel days (non-US since 2026-10-08, US E-P since 2026-10-02)')
for d in ['edge-panel','europe','japan','australia','canada']:
    tot = sel = 0; ins = collections.Counter(); nm = 0
    for f in glob.glob(str(R/f'research/*/*/*/{d}/edge-scores-panel.json')):
        P = json.load(open(f))
        for r in P['ranking']:
            tot += 1; sel += r['selected']
            for m,x in r['members'].items(): ins[m] += x['in_own_top']; 
            nm += 1
    if tot: print(f"{d:11s} names {tot:3d}  selected {sel:2d} ({100*sel/tot:.0f}%)  in own top per judge: " +
                  ', '.join(f"{m} {100*ins[m]/nm:.0f}%" for m in PS.MEMBERS))
json.dump({'scale': out1, 'rejudge': out2}, open(Path(__file__).with_name('country_thresholds.json'),'w'), indent=1)

# ---------- 4. the US history mixes in non-US re-judge sizes, which lowers the US line
print('\n## 4. US panel history: non-US rows in the 200-name window, and the line without them')
H = json.load(open(R/'researcher_us/analysis/panel-history.json'))
us_rows = lambda m: [x for x in H[m] if x['id'].startswith('us/') or 'edge-panel' in x['source']]
lines_us = {m: PS.member_stats(us_rows(m), 200)['q80'] for m in PS.MEMBERS}
for m in PS.MEMBERS:
    nonus = sum(not (x['id'].startswith('us/') or 'edge-panel' in x['source']) for x in H[m][-200:])
    print(f"{m:9s} non-US {nonus}/200, line now {PS.member_stats(H[m],200)['q80']}, US-only line {lines_us[m]}")
tot = sel = 0; ins = collections.Counter()
for f in glob.glob(str(R/'research/*/*/*/edge-panel/edge-scores-panel.json')):
    for r in json.load(open(f))['ranking']:
        tot += 1; k_ = 0
        for m, x in r['members'].items():
            t = abs(x['impact_sum']) >= lines_us[m] and x['impact_sum'] != 0; ins[m] += t
            k_ += t and ((x['z'] > 0) - (x['z'] < 0)) == r['side'] != 0
        sel += k_ >= 3
print(f"live E-P at the US-only line: {sel}/{tot} selected; in own top " + ', '.join(f"{m} {100*ins[m]/tot:.0f}%" for m in PS.MEMBERS))

# ---------- 5. the hunter gates, live, October: is 2.8 (impact_sum) / 1.76 (impact_scaled) a top 20%?
print('\n## 5. Hunter gates on live October runs (both were set as p80 of an Opus 5.5 reference)')
for d in ['edge', 'europe', 'japan', 'canada', 'australia']:
    s, sc = [], []
    for f in glob.glob(str(R/f'research/2026/10/*/{d}/edge-scores.json')):
        s += [abs(r.get('impact_sum') or 0) for r in json.load(open(f)).get('ranking', []) if r.get('rankable') is not False]
    for f in glob.glob(str(R/f'research/2026/10/*/{d}/edge-scores-scaled.json')):
        D = json.load(open(f))
        sc += [abs(r['impact_scaled']) for r in (D.get('ranking') or D.get('rows') or []) if isinstance(r.get('impact_scaled'), (int, float))]
    print(f"{d:10s} n {len(s):3d}  p80 |impact_sum| {q(s,.8)}  >=2.8: {sum(x>=2.8 for x in s)}   "
          f"n {len(sc):3d}  p80 |impact_scaled| {q(sc,.8)}  >=1.76: {sum(x>=1.76 for x in sc)}")
