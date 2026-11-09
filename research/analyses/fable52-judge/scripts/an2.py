import json,math,collections,numpy as np
exec(open('an.py').read().split("KEYS=")[0])
ret=lambda r,k='f52': math.copysign(1,r[k])*r['move'] if r[k] else 0.0
print('\n== Bands of |Fable 5.2 impact_sum| (all 194; side from sign) ==')
for lo,hi in [(0,1),(1,2),(2,3),(3,99)]:
    summ([r for r in R if lo<=abs(r['f52'])<hi and r['f52']],ret,f'|f52| {lo}-{hi}')
print('== cumulative thresholds, per version ==')
for ver in ['us-panel.v3','us-panel.v2']:
    rows=[r for r in R if r['version']==ver]; print(ver)
    for t in [1,1.5,2,2.5,3]:
        summ([r for r in rows if abs(r['f52'])>=t],ret,f'|f52| >= {t}')
    for t in [5,8,10,12]:
        summ([r for r in rows if abs(r['f52_p_up']-50)>=t],lambda r: math.copysign(1,r['f52_p_up']-50)*r['move'],f'|p_up-50| >= {t}')
    print('  -- live panel on the same names --')
    for t in [60,70,80,90]:
        summ([r for r in rows if abs(r['panel_pct_signed'])>=t and r.get('n_members')==4],lambda r: math.copysign(1,r['panel_pct_signed'])*r['move'],f'panel_pct >= {t}')
    for k in ['fable51','opus55','opus5']:
        q=np.quantile([abs(r[k]) for r in R],.8)
        summ([r for r in rows if abs(r[k])>=q],lambda r,k=k: math.copysign(1,r[k])*r['move'],f'{k} own top 20% (>= {q:.2f})')
    q=np.quantile([abs(r['f52']) for r in R],.8)
    summ([r for r in rows if abs(r['f52'])>=q],ret,f'f52 own top 20% (>= {q:.2f})')
# conviction: does |f52| predict being right
x=[abs(r['f52']) for r in R if r['f52']]; y=[ret(r) for r in R if r['f52']]
print('\nconviction: Spearman |f52| vs signed return %.3f (n %d); long/short split:'%(sp(x,y),len(x)))
summ([r for r in R if r['f52']>=2],ret,'f52 >= +2 (long)'); summ([r for r in R if r['f52']<=-2],ret,'f52 <= -2 (short)')
summ([r for r in R if 0<r['f52']<2],ret,'0<f52<2'); summ([r for r in R if -2<r['f52']<0],ret,'-2<f52<0')
# dev/holdout on v3
v3=[r for r in R if r['version']=='us-panel.v3']
dev=[r for r in v3 if r['date']<='2026-11-03']; ho=[r for r in v3 if r['date']>'2026-11-03']
print('\n== v3 boundary: chosen on development (29 Oct-3 Nov, n %d), tested on holdout (4-6 Nov, n %d) =='%(len(dev),len(ho)))
best=None
for t in [0.5,1,1.5,2,2.5,3]:
    s=[ret(r) for r in dev if abs(r['f52'])>=t]
    if len(s)>=8:
        ts=tstat(s); print(f'  dev |f52|>={t}: n {len(s)} mean {np.mean(s):+.2f} t {ts:+.2f}')
        if best is None or ts>best[1]: best=(t,ts)
print('  chosen threshold',best)
summ([r for r in ho if abs(r['f52'])>=best[0]],ret,f'holdout |f52|>={best[0]}')
summ([r for r in ho if abs(r['f52'])<best[0] and r['f52']],ret,f'holdout below')
# agreement with panel strong calls
print('\n== live strong calls (panel>=80, 4 judges) split by Fable 5.2 ==')
st=[r for r in R if abs(r['panel_pct_signed'])>=80 and r.get('n_members')==4]
pr=lambda r: math.copysign(1,r['panel_pct_signed'])*r['move']
summ(st,pr,'all strong')
summ([r for r in st if r['f52']*r['panel_pct_signed']>0 and abs(r['f52'])>=2],pr,'f52 agrees, |f52|>=2')
summ([r for r in st if r['f52']*r['panel_pct_signed']>0 and abs(r['f52'])<2],pr,'f52 agrees, |f52|<2')
summ([r for r in st if r['f52']*r['panel_pct_signed']<=0],pr,'f52 disagrees/zero')
print('strong Fable calls (|f52|>=2.2) not strong in panel:')
summ([r for r in R if abs(r['f52'])>=2.2 and not(abs(r['panel_pct_signed'])>=80 and r.get('n_members')==4)],ret,'f52 only')
# leak check: tickers named in project notes
named={'AEYE','LIFE','TREE','CRCT','IBTA','MVIS','CHGG','HRTG','CYH','KALU','TTMI','LRCX','CRS'}
print('named-in-notes tickers in sample:',[(r['id'],r['f52'],r['move']) for r in R if r['ticker'] in named])
