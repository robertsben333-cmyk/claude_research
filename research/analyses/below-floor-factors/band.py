#!/usr/bin/env python3
"""Do retail tilt, lean agreement and a quiet search spike rescue names with 1 <= |impact_sum| < 2.8?

Run from the repo root: python3 research/analyses/below-floor-factors/band.py [strategy|close]
Reads dashboard/data/ledger.json only. Factor definitions are those of dashboard/scripts/weighting.py
(retail_tilt >= 50, sign(priced_lean_pct) == sign(impact_sum), search_spike < 1.0 where measured)."""
import json, statistics as st, random, math, sys
d=json.load(open('dashboard/data/ledger.json'))
EXIT=sys.argv[1] if len(sys.argv)>1 else 'strategy'
N=[r for r in d['names'] if not r.get('duplicate_event') and r.get('impact_sum')
   and r.get('ret_'+EXIT) is not None and r.get('event_occurred',True) is not False]
def sgn(x): return 1 if x>0 else -1
def fac(r):
    imp=r['impact_sum']; lean=r.get('priced_lean_pct'); rt=r.get('retail_tilt')
    f={}
    f['retail']=None if rt is None else (1 if rt>=50 else 0)
    f['lean']=None if lean is None or lean==0 else (1 if sgn(lean)==sgn(imp) else 0)
    if r.get('search_state')=='measured' and r.get('search_spike') is not None:
        f['quiet']=1 if r['search_spike']<1.0 else 0
    else: f['quiet']=None
    return f
def stats(g,key=None):
    key=key or (lambda r:r['ret_'+EXIT])
    v=[key(r) for r in g]
    if not v: return dict(n=0)
    m=st.fmean(v); sd=st.stdev(v) if len(v)>1 else 0
    return dict(n=len(v),hit=100*sum(x>0 for x in v)/len(v),mean=m,t=m/(sd/math.sqrt(len(v))) if sd else 0,
                days=len({r['run_date'] for r in g}))
def fmt(s,lab):
    if not s['n']: return f'{lab:42s} n=0'
    return f"{lab:42s} n={s['n']:3d} d={s['days']:2d} raak {s['hit']:5.1f}%  {s['mean']:+6.2f}%  t {s['t']:+5.2f}"
def band(r):
    a=abs(r['impact_sum']); return '<1' if a<1 else ('1-2.8' if a<2.8 else '>=2.8')
for era,flt in [('ALL',lambda r:True),('Opus 5',lambda r:r.get('model_short')=='Opus 5')]:
    E=[r for r in N if flt(r)]
    print(f'\n===== {era}  exit={EXIT}  n={len(E)}')
    for b in ['<1','1-2.8','>=2.8']:
        print(fmt(stats([r for r in E if band(r)==b]),'band '+b))
    B=[r for r in E if band(r)=='1-2.8']
    print('-- within band 1-2.8, per factor')
    for k in ['retail','lean','quiet']:
        hi=[r for r in B if fac(r)[k]==1]; lo=[r for r in B if fac(r)[k]==0]
        print(fmt(stats(hi),f'  {k}=gunstig')); print(fmt(stats(lo),f'  {k}=ongunstig'))
    print('-- within band: count of favourable among retail+lean (search mostly missing)')
    for c in [0,1,2]:
        g=[r for r in B if fac(r)['retail'] is not None and fac(r)['lean'] is not None and fac(r)['retail']+fac(r)['lean']==c]
        print(fmt(stats(g),f'  retail+lean = {c}'))
    print('-- including search where measured: all available factors favourable')
    def allfav(r):
        f=fac(r); v=[x for x in f.values() if x is not None]; return len(v)>=2 and all(v)
    print(fmt(stats([r for r in B if allfav(r)]),'  all available favourable (>=2 known)'))
    print('-- controls in band')
    print(fmt(stats(B,lambda r:-r['mv_'+EXIT]),'  short everything'))
    L=[r for r in B if r.get('priced_lean_pct')]
    print(fmt(stats(L,lambda r:sgn(r['priced_lean_pct'])*r['mv_'+EXIT]),'  follow the lean alone'))
    dis=[r for r in L if fac(r)['lean']==0]
    print(fmt(stats(dis),'  lean disagrees: follow hunt'))
    print(fmt(stats(dis,lambda r:sgn(r['priced_lean_pct'])*r['mv_'+EXIT]),'  lean disagrees: follow lean'))
    # same in book
    A=[r for r in E if band(r)=='>=2.8']
    print('-- above floor, for comparison')
    for k in ['retail','lean','quiet']:
        hi=[r for r in A if fac(r)[k]==1]; lo=[r for r in A if fac(r)[k]==0]
        print(fmt(stats(hi),f'  {k}=gunstig')); print(fmt(stats(lo),f'  {k}=ongunstig'))
    La=[r for r in A if r.get('priced_lean_pct')]
    print(fmt(stats(La,lambda r:sgn(r['priced_lean_pct'])*r['mv_'+EXIT]),'  follow the lean alone (book names)'))
    print(fmt(stats(E and [r for r in E if r.get('priced_lean_pct')],lambda r:sgn(r['priced_lean_pct'])*r['mv_'+EXIT]),'  follow the lean alone (ALL names)'))
