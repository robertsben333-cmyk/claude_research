"""Alpaca SIP bars, multi-symbol. Keys from env, never printed.
daily: 2026-04-01..2026-11-14 for all tickers. m5: run day 09:30-13:30 ET; bmo report day 09:30-13:00 ET."""
import json,os,time,datetime as dt,urllib.request,urllib.parse,urllib.error,collections
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
NY=ZoneInfo('America/New_York');UTC=dt.timezone.utc
H={'APCA-API-KEY-ID':os.environ['ALPACA_API_KEY_ID'],'APCA-API-SECRET-KEY':os.environ['ALPACA_API_SECRET_KEY']}
C='/mnt/project-files/earnings-day-indicators/cache';os.makedirs(C,exist_ok=True)
def iso(day,hh,mm): return dt.datetime.combine(dt.date.fromisoformat(day),dt.time(hh,mm),NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def get(syms,tf,start,end):
  out=collections.defaultdict(list);tok=None
  while True:
    q=dict(symbols=','.join(syms),timeframe=tf,start=start,end=end,feed='sip',adjustment='split',limit=10000)
    if tok:q['page_token']=tok
    url='https://data.alpaca.markets/v2/stocks/bars?'+urllib.parse.urlencode(q)
    for a in range(7):
      try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=60) as r: d=json.load(r);break
      except urllib.error.HTTPError as e:
        if e.code==429: time.sleep(2**a);continue
        if e.code in (400,422): return dict(out)
        time.sleep(2**a)
      except Exception: time.sleep(2**a)
    else: raise RuntimeError('retries')
    for s,b in (d.get('bars') or {}).items(): out[s]+=b
    tok=d.get('next_page_token')
    if not tok: return dict(out)
E_=json.load(open('/mnt/project-files/earnings-day-indicators/events.json'))
sym=lambda t:t.replace('-','.')
def chunks(l,n): return [l[i:i+n] for i in range(0,len(l),n)]
jobs=[]
allt=sorted({sym(e['t']) for e in E_})
for i,c in enumerate(chunks(allt,50)): jobs.append((f'daily_{i}',c,'1Day',iso('2026-04-01',0,0),iso('2026-11-14',23,0)))
byd=collections.defaultdict(set);byev=collections.defaultdict(set)
for e in E_:
  byd[e['d']].add(sym(e['t']))
  if e['ses']=='bmo': byev[e['ev']].add(sym(e['t']))
for d,s in byd.items():
  for i,c in enumerate(chunks(sorted(s),50)): jobs.append((f'run_{d}_{i}',c,'5Min',iso(d,9,30),iso(d,13,30)))
for d,s in byev.items():
  for i,c in enumerate(chunks(sorted(s),50)): jobs.append((f'bmo_{d}_{i}',c,'5Min',iso(d,9,30),iso(d,13,0)))
def run(j):
  p=f'{C}/{j[0]}.json'
  if os.path.exists(p): return
  try: json.dump(get(*j[1:]),open(p,'w'))
  except Exception as ex: print(j[0],ex)
with ThreadPoolExecutor(4) as ex: list(ex.map(run,jobs))
print('jobs',len(jobs),'cached',len(os.listdir(C)))
