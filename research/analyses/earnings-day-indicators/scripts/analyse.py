import json,math,numpy as np,collections
rng=np.random.default_rng(7)
F=json.load(open('/mnt/project-files/earnings-day-indicators/features.json'))
Fk={(f['d'],f['t']):f for f in F}
R=json.load(open('/mnt/project-files/quant-selection-score/rows.json'))
IND=[('D1','ru5',-1),('D2','ru20',-1),('D3','rsi',-1),('D4','sma50',1),('D5','prev',1),('D6','skew',-1),
     ('D7','pcr',-1),('D8','rday',1),('D9','vwap',1),('D10','abvol',1),('D11','dtc',-1)]
S1=('S1','ivrich',-1)
# within-day centred ranks over the market-wide set, for the composite
byday=collections.defaultdict(list)
for f in F: byday[f['d']].append(f)
for d,L in byday.items():
  for _,k,h in IND:
    v=[(f[k],i) for i,f in enumerate(L) if f.get(k) is not None]
    if len(v)<2: continue
    v.sort();
    for r,(_,i) in enumerate(v): L[i]['_r_'+k]=h*(r/(len(v)-1)-0.5)
for f in F:
  rs=[f['_r_'+k] for _,k,_ in IND if '_r_'+k in f]; f['comp']=sum(rs)/len(rs) if len(rs)>=6 else None
def rk(a):
  o=np.argsort(a,kind='mergesort');r=np.empty(len(a));r[o]=np.arange(len(a))
  a=np.asarray(a);
  for val in np.unique(a):
    m=a==val
    if m.sum()>1: r[m]=r[m].mean()
  return r
def sp(x,y,days,nperm=5000):
  x=np.array(x,float);y=np.array(y,float);days=np.array(days)
  m=~(np.isnan(x)|np.isnan(y));x,y,days=x[m],y[m],days[m]
  if len(x)<10: return None
  groups=[np.where(days==d)[0] for d in np.unique(days)]
  groups=[g for g in groups if len(g)>=3]
  keep=np.concatenate(groups);rx=np.zeros(len(x));ry=np.zeros(len(y))
  for g in groups:
    rx[g]=(rk(x[g])/(len(g)-1))-0.5; ry[g]=(rk(y[g])/(len(g)-1))-0.5
  x,y=x[keep],y[keep];rx,ry=rx[keep],ry[keep];days=days[keep]
  groups=[np.where(days==d)[0] for d in np.unique(days)]
  rho=float(rx@ry/math.sqrt((rx@rx)*(ry@ry)))
  P=np.tile(np.arange(len(y)),(nperm,1))
  for g in groups:
    if len(g)>1: P[:,g]=g[np.argsort(rng.random((nperm,len(g))),axis=1)]
  sims=(ry[P]@rx)/math.sqrt((rx@rx)*(ry@ry))
  p=float((np.sum(np.abs(sims)>=abs(rho)-1e-12)+1)/(nperm+1))
  return dict(rho=round(rho,3),p=round(p,4),n=int(len(x)))
def ols_pct(rows,k,h,target):
  # ret ~ day-demeaned pct + day-demeaned signed rank; day-clustered t
  D=collections.defaultdict(list)
  for r in rows:
    f=Fk[(r['d'],r['t'])]; y=target(r,f)
    if f.get(k) is None or y is None: continue
    D[r['d']].append((r['pct'],r['side']*h*f[k],y))
  X=[];Y=[];G=[]
  for d,L in D.items():
    if len(L)<2: continue
    xs=rk([l[1] for l in L]);xs=xs/(len(L)-1)-0.5
    pc=np.array([l[0] for l in L]);yy=np.array([l[2] for l in L])
    for a,b,c in zip(pc-pc.mean(),xs-xs.mean(),yy-yy.mean()): X.append([a,b]);Y.append(c);G.append(d)
  X=np.array(X);Y=np.array(Y);G=np.array(G)
  if len(Y)<20: return None
  b=np.linalg.lstsq(X,Y,rcond=None)[0];e=Y-X@b;XtX=np.linalg.inv(X.T@X)
  M=sum(np.outer(X[G==g].T@e[G==g],X[G==g].T@e[G==g]) for g in np.unique(G))
  V=XtX@M@XtX;nG=len(np.unique(G));V*=nG/(nG-1)
  return dict(b_top_vs_bottom=round(float(b[1]),2),t=round(float(b[1]/math.sqrt(V[1,1])),2),n=len(Y))
TGT={'move':lambda r,f:r['ret'],
 'entry':lambda r,f:None if f.get('leg_entry') is None else r['side']*f['leg_entry'],
 'amc_hold':lambda r,f:None if f.get('leg_amc_hold') is None else r['side']*f['leg_amc_hold'],
 'bmo_early':lambda r,f:None if f.get('leg_bmo_early') is None else r['side']*f['leg_bmo_early'],
 'bmo_late':lambda r,f:None if f.get('leg_bmo_late') is None else r['side']*f['leg_bmo_late']}
MK={'move':'mv','entry':'leg_entry','amc_hold':'leg_amc_hold','bmo_early':'leg_bmo_early','bmo_late':'leg_bmo_late'}
res={}
allind=IND+[S1,('C','comp',1)]
for leg in TGT:
  for code,k,h in allind:
    for v in ['us-panel.v3','us-panel.v2']:
      rows=[r for r in R if r['v']==v]
      xs=[];ys=[];ds=[]
      for r in rows:
        f=Fk[(r['d'],r['t'])];y=TGT[leg](r,f)
        if code=='S1' and leg=='move': xs.append(np.nan if f.get(k) is None else h*f[k])
        else: xs.append(np.nan if f.get(k) is None else r['side']*h*f[k])
        ys.append(np.nan if y is None else y);ds.append(r['d'])
      res[(leg,code,v)]=sp(xs,ys,ds)
      if leg=='move' and code not in ('S1',): res[(leg,code,v,'ols')]=ols_pct(rows,k,h,TGT[leg])
    # market-wide (S1 not applicable: no side)
    if code!='S1':
      for v in ['us-panel.v3','us-panel.v2']:
        L=[f for f in F if f['v']==v]
        res[(leg,code,'mkt-'+v[-2:])]=sp([np.nan if f.get(k) is None else h*f[k] for f in L],
             [np.nan if f.get(MK[leg]) is None else f[MK[leg]] for f in L],[f['d'] for f in L])
# Holm per leg over the 12 (D1..D11,S1) on v3
out=[]
for leg in TGT:
  ps=sorted([(res[(leg,c,'us-panel.v3')]['p'],c) for c,_,_ in IND+[S1] if res.get((leg,c,'us-panel.v3'))])
  m=len(ps);holm={};run=0
  for i,(p,c) in enumerate(ps): run=max(run,min(1,(m-i)*p));holm[c]=round(run,4)
  for code,k,h in allind:
    a=res.get((leg,code,'us-panel.v3'));b=res.get((leg,code,'us-panel.v2'));mw=res.get((leg,code,'mkt-v3'));m2=res.get((leg,code,'mkt-v2'))
    sg=lambda z:None if not z else (z['rho']>0)-(z['rho']<0)
    verdict='nothing'
    if a and b:
      same=sg(a)==sg(b)==(sg(mw) if mw else sg(a))
      if code!='C' and holm.get(code,1)<0.05 and same: verdict='ADDS'
      elif code=='C' and a['p']<0.05 and same: verdict='ADDS'
      elif same and a['p']<0.10: verdict='lead'
    out.append(dict(leg=leg,ind=code,var=k,v3=a,holm=holm.get(code),v2=b,mkt_v3=mw,mkt_v2=m2,ols_v3=res.get((leg,code,'us-panel.v3','ols')),ols_v2=res.get((leg,code,'us-panel.v2','ols')),verdict=verdict))
json.dump(out,open('/mnt/project-files/earnings-day-indicators/results.json','w'),indent=1)
f=lambda z:'—' if not z else f"{z['rho']:+.2f} p{z['p']:.3f} n{z['n']}"
for o in out:
  print(f"{o['leg']:9s} {o['ind']:3s} {o['var']:6s} v3 {f(o['v3']):22s} holm {o['holm']}  v2 {f(o['v2']):22s} mkt3 {f(o['mkt_v3']):22s} mkt2 {f(o['mkt_v2']):22s} {o['verdict']}"+(f"  ols3 {o['ols_v3']} ols2 {o['ols_v2']}" if o['ols_v3'] else ''))
