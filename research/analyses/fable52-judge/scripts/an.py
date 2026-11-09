import json,math,random,collections
import numpy as np
random.seed(7); rng=np.random.default_rng(7)
R=[x for x in json.load(open('rows.json')) if x['move'] is not None]
def rank(a):
    a=np.asarray(a,float); o=a.argsort(); r=np.empty(len(a)); r[o]=np.arange(len(a))
    for v in np.unique(a):
        m=a==v; r[m]=r[m].mean()
    return r
def sp(x,y):
    if len(x)<3: return float('nan')
    rx,ry=rank(x),rank(y)
    if rx.std()==0 or ry.std()==0: return float('nan')
    return float(np.corrcoef(rx,ry)[0,1])
def within(rows,key,n=4000):
    # within-day: demean ranks per day -> pooled corr; permutation within day
    days=collections.defaultdict(list)
    for r in rows:
        if r.get(key) is not None: days[r['date']].append(r)
    xs=[];ys=[];idx=[]
    for d,v in days.items():
        if len(v)<3: continue
        x=rank([r[key] for r in v]); y=rank([r['move'] for r in v])
        x=(x-x.mean())/len(v); y=(y-y.mean())/len(v)
        idx.append((len(xs),len(xs)+len(v))); xs+=list(x); ys+=list(y)
    xs=np.array(xs);ys=np.array(ys)
    obs=float(np.corrcoef(xs,ys)[0,1]); c=0
    for _ in range(n):
        yp=ys.copy()
        for a,b in idx: yp[a:b]=rng.permutation(yp[a:b])
        if abs(np.corrcoef(xs,yp)[0,1])>=abs(obs): c+=1
    return obs,(c+1)/(n+1),len(xs)
def tstat(v):
    v=np.asarray(v,float)
    if len(v)<2: return float('nan')
    return float(v.mean()/(v.std(ddof=1)/math.sqrt(len(v)))) if v.std(ddof=1)>0 else float('nan')
def dayt(rows,retf):
    d=collections.defaultdict(list)
    for r in rows: d[r['date']].append(retf(r))
    m=[np.mean(v) for v in d.values()]
    return tstat(m),len(m)
def summ(rows,retf,label):
    v=[retf(r) for r in rows]
    if not v: print(f'  {label:28s} n 0'); return
    td,nd=dayt(rows,retf)
    print(f'  {label:28s} n {len(v):3d}  mean {np.mean(v):+6.2f}%  hit {100*np.mean(np.array(v)>0):4.0f}%  t {tstat(v):+5.2f}  day-t {td:+5.2f} ({nd} days)')
KEYS=['f52','fable51','opus5','opus55','sonnet55','panel_pct_signed']
print('N resolved',len(R))
f=np.array([r['f52'] for r in R])
print('Fable 5.2 impact_sum: median |x| %.2f  p80 |x| %.2f  p90 %.2f  max %.2f ; share long %.0f%% ; zero %d'%(np.median(abs(f)),np.quantile(abs(f),.8),np.quantile(abs(f),.9),abs(f).max(),100*np.mean(f>0),int((f==0).sum())))
pu=np.array([r['f52_p_up'] for r in R]); print('p_up: min %d max %d, |p_up-50| median %.0f p80 %.0f'%(pu.min(),pu.max(),np.median(abs(pu-50)),np.quantile(abs(pu-50),.8)))
for k in ['fable51','opus5','opus55','sonnet55']:
    a=np.array([abs(r[k]) for r in R if r.get(k) is not None]); print(f'  {k}: median |x| {np.median(a):.2f} p80 {np.quantile(a,.8):.2f}')
print('\nAgreement with original judges (Spearman over all names, signed score):')
for k in KEYS[1:]:
    rr=[r for r in R if r.get(k) is not None]
    print(f'  f52 vs {k:18s} rho {sp([r["f52"] for r in rr],[r[k] for r in rr]):+.2f}  same sign {100*np.mean([np.sign(r["f52"])==np.sign(r[k]) for r in rr if r["f52"]!=0 and r[k]!=0]):.0f}%  n {len(rr)}')
print('  (for scale) fable51 vs opus55 rho %+.2f, opus5 vs sonnet55 %+.2f'%(sp([r['fable51'] for r in R],[r['opus55'] for r in R]),sp([r['opus5'] for r in R],[r['sonnet55'] for r in R])))
for ver in ['us-panel.v3','us-panel.v2','all']:
    rows=[r for r in R if ver=='all' or r['version']==ver]
    print(f'\n=== {ver}: n {len(rows)}, days {len(set(r["date"] for r in rows))} ===')
    print(' Ranking: within-day Spearman of signed score vs stock move (permutation p)')
    for k in KEYS:
        o,p,n=within(rows,k); print(f'  {k:18s} rho {o:+.3f}  p {p:.3f}  n {n}')
    o,p,n=within(rows,'f52_p_up'); print(f'  {"f52 p_up":18s} rho {o:+.3f}  p {p:.3f}  n {n}')
    print(' Trading the sign (return = side x move, gross):')
    for k in KEYS:
        rr=[r for r in rows if r.get(k)]
        summ(rr,lambda r,k=k: math.copysign(1,r[k])*r['move'],k+' all non-zero')
    summ(rows,lambda r:-r['move'],'short everything')
    summ(rows,lambda r:r['move'],'long everything')
json.dump(R,open('rows_resolved.json','w'))
