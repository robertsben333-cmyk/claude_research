"""Features (known by 13:30 ET run day) + raw move on the scorebord window, every baseline name."""
import json,glob,os,math,datetime as dt,statistics as st,collections
from zoneinfo import ZoneInfo
NY=ZoneInfo('America/New_York')
C='/mnt/project-files/earnings-day-indicators/cache'
E_=json.load(open('/mnt/project-files/earnings-day-indicators/events.json'))
daily=collections.defaultdict(list)
for f in glob.glob(f'{C}/daily_*.json'):
  for s,b in json.load(open(f)).items(): daily[s]+=b
for s in daily: daily[s]=sorted({b['t'][:10]:b for b in daily[s]}.values(),key=lambda b:b['t'])
def m5(prefix):
  out=collections.defaultdict(list)
  for f in glob.glob(f'{C}/{prefix}_*.json'):
    key=f.split('/')[-1].rsplit('_',1)[0].split('_',1)[1]
    for s,b in json.load(open(f)).items(): out[(key,s)]+=b
  return out
RUN=m5('run');BMO=m5('bmo')
def et_min(t):
  x=dt.datetime.fromisoformat(t.replace('Z','+00:00')).astimezone(NY);return x.hour*60+x.minute
# short interest
def si(t,d):
  p=f'/mnt/project-files/earnings-day-indicators/cache_si/{t}.json'
  if not os.path.exists(p): return None,None
  try: rows=json.load(open(p))['data']['shortInterestTable']['rows']
  except Exception: return None,None
  ok=[]
  for r in rows:
    m,dd,y=r['settlementDate'].split('/');sd=dt.date(int(y),int(m),int(dd))
    if sd+dt.timedelta(days=11)<=dt.date.fromisoformat(d):
      try: ok.append((sd,float(r['daysToCover']),float(r['interest'].replace(',',''))))
      except Exception: pass
  ok.sort(reverse=True)
  if not ok: return None,None
  ch=math.log(ok[0][2]/ok[1][2]) if len(ok)>1 and ok[1][2]>0 and ok[0][2]>0 else None
  return ok[0][1],ch
def rsi(c,n=14):
  g=[max(c[i]-c[i-1],0) for i in range(1,len(c))];l=[max(c[i-1]-c[i],0) for i in range(1,len(c))]
  if len(g)<n: return None
  ag=sum(g[:n])/n;al=sum(l[:n])/n
  for i in range(n,len(g)): ag=(ag*(n-1)+g[i])/n;al=(al*(n-1)+l[i])/n
  return 100.0 if al==0 else 100-100/(1+ag/al)
out=[]
for e in E_:
  s=e['t'].replace('-','.');D=daily.get(s,[]);d=e['d']
  pre=[b for b in D if b['t'][:10]<d]
  x=dict(e)
  if len(pre)>=21:
    c=[b['c'] for b in pre];v=[b['v'] for b in pre];pc=c[-1]
    x['ru5']=100*(pc/c[-6]-1);x['ru20']=100*(pc/c[-21]-1);x['rsi']=rsi(c[-120:])
    x['sma50']=100*(pc/st.mean(c[-50:])-1) if len(c)>=50 else None
    x['abvol']=math.log((st.mean(v[-5:])+1)/(st.mean(v[-65:-5])+1)) if len(v)>=65 else None
    x['dvol']=st.median([a*b for a,b in zip(c[-20:],v[-20:])])
  else: pc=None
  # run day bars
  rb=sorted(RUN.get((d,s),[]),key=lambda b:b['t'])
  rb=[b for b in rb if et_min(b['t'])<13*60+30]
  entry=None
  if rb and pc and et_min(rb[-1]['t'])>=12*60+30:
    entry=rb[-1]['c'];x['rday']=100*(entry/pc-1)
    vw=sum(b['vw']*b['v'] for b in rb)/max(sum(b['v'] for b in rb),1)
    x['vwap']=100*(entry/vw-1) if vw else None
  # exit
  ex=None
  if e['ses']=='amc':
    nx=[b for b in D if b['t'][:10]>d]
    if nx: ex=nx[0]['o'];x['exit_day']=nx[0]['t'][:10]
  else:
    eb=sorted(BMO.get((e['ev'],s),[]),key=lambda b:b['t'])
    eb=[b for b in eb if et_min(b['t'])<13*60]
    if eb and et_min(eb[-1]['t'])>=12*60: ex=eb[-1]['c']
  if entry and ex: x['mv']=100*(ex/entry-1)
  dd={b['t'][:10]:b for b in D}
  if entry and d in dd: x['leg_entry']=100*(dd[d]['c']/entry-1)
  if e['ses']=='amc':
    nx=[b for b in D if b['t'][:10]>d]
    if nx: x['leg_amc_hold']=100*(nx[0]['c']/nx[0]['o']-1)
  else:
    eb2=[b for b in D if b['t'][:10]==e['ev']]
    if eb2 and ex:
      x['leg_bmo_early']=100*(ex/eb2[0]['o']-1); x['leg_bmo_late']=100*(eb2[0]['c']/ex-1)
  x['dtc'],x['sich']=si(e['t'],d)
  x['ivrich']=e['imp']/e['hmed'] if e.get('imp') and e.get('hmed') else None
  out.append(x)
json.dump(out,open('/mnt/project-files/earnings-day-indicators/features.json','w'))
n=len(out);print('n',n)
for k in ['ru5','ru20','rsi','sma50','abvol','prev','skew','pcr','rday','vwap','dtc','ivrich','mv']:
  print(k,sum(o.get(k) is not None for o in out))
