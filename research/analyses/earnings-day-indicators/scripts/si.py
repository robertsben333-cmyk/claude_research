import json,os,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
C='/mnt/project-files/earnings-day-indicators/cache_si';os.makedirs(C,exist_ok=True)
E_=json.load(open('/mnt/project-files/earnings-day-indicators/events_si_order.json'))
def one(t):
  p=f'{C}/{t}.json'
  if os.path.exists(p): return
  url=f'https://api.nasdaq.com/api/quote/{t}/short-interest?assetClass=stocks'
  for a in range(4):
    try:
      with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'}),timeout=20) as r:
        d=json.load(r);break
    except Exception: time.sleep(2**a)
  else: d={'error':1}
  json.dump(d,open(p,'w'))
with ThreadPoolExecutor(8) as ex: list(ex.map(one,list(dict.fromkeys(e['t'] for e in E_))))
print('done',len(os.listdir(C)))
