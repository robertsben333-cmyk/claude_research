import json, datetime as dt
def load(t):
    j=json.load(open(f'dl/yh_{t}.json'))['chart']['result'][0]
    return [(dt.datetime.utcfromtimestamp(a).strftime('%Y-%m-%d'),b) for a,b in zip(j['timestamp'],j['indicators']['quote'][0]['close']) if b is not None]
def at(r,d): return [v for dd,v in r if dd<=d][-1]
mes=['2026-03-31','2026-04-30','2026-05-29','2026-06-30','2026-07-31','2026-08-31','2026-09-30']
for t in ['SPY','EFA','EEM','AGG','IBIT','GLD','BLK']:
    r=load(t); v=[at(r,d) for d in mes]
    base=v[3]
    print(t, ' '.join(f'{d[5:]}:{x/base*100:6.2f}' for d,x in zip(mes,v)), ' Q2me-avg/Jun30 %.2f'%(sum(v[0:4])/4/base*100), ' Q3me-avg/Jun30 %.2f'%(sum(v[3:7])/4/base*100))
