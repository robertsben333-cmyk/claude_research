"""Exploratory, after the pre-registered tests: magnitudes of the leads."""
import json,statistics as st,collections,math
F=json.load(open('../features.json'));Fk={(f['d'],f['t']):f for f in F}
R=json.load(open('/mnt/project-files/quant-selection-score/rows.json'))
def terc(rows,xf,yf,label):
  byd=collections.defaultdict(list)
  for r in rows:
    x,y=xf(r),yf(r)
    if x is None or y is None: continue
    byd[r['d']].append((x,y))
  g={0:[],1:[],2:[]}
  for d,L in byd.items():
    if len(L)<3: continue
    L.sort()
    for i,(x,y) in enumerate(L): g[min(2,int(3*i/len(L)))].append(y)
  m=lambda v:f"{st.mean(v):+.2f} (n{len(v)})"
  d=[*g[2]];a=g[0]
  diff=st.mean(d)-st.mean(a);se=math.sqrt(st.variance(d)/len(d)+st.variance(a)/len(a))
  print(f"{label:55s} low {m(g[0])}  mid {m(g[1])}  high {m(g[2])}  high-low {diff:+.2f} t {diff/se:.2f}")
for v in ['us-panel.v3','us-panel.v2']:
  rows=[r for r in R if r['v']==v]
  f=lambda r:Fk[(r['d'],r['t'])]
  terc(rows,lambda r:None if f(r).get('vwap') is None else r['side']*f(r)['vwap'],lambda r:r['ret'],v+' ret by price-vs-VWAP on our side')
  terc(rows,lambda r:None if f(r).get('rday') is None else r['side']*f(r)['rday'],lambda r:r['ret'],v+' ret by run-day move on our side')
  terc(rows,lambda r:r['side']*f(r)['ru5'],lambda r:r['ret'],v+' ret by 5d run-up on our side')
  terc(rows,lambda r:None if f(r).get('prev') is None else r['side']*f(r)['prev'],lambda r:r['ret'],v+' ret by prev reaction on our side')
  terc(rows,lambda r:f(r).get('ivrich'),lambda r:r['ret'],v+' ret by implied/hist move')
  # strong only
  s=[r for r in rows if r['pct']>=60]
  terc(s,lambda r:None if f(r).get('vwap') is None else r['side']*f(r)['vwap'],lambda r:r['ret'],v+' pct>=60: ret by VWAP')
for v in ['us-panel.v3','us-panel.v2']:
  L=[x for x in F if x['v']==v]
  terc(L,lambda x:x.get('abvol') if x['ses']=='amc' else None,lambda x:x.get('leg_amc_hold'),v+' MKT amc next open->close by abnormal volume')
  terc(L,lambda x:x.get('ru5') if x['ses']=='bmo' else None,lambda x:x.get('leg_bmo_early'),v+' MKT bmo open->13:00 by 5d run-up')
  terc(L,lambda x:x.get('abvol'),lambda x:x.get('mv'),v+' MKT move by abnormal volume')
