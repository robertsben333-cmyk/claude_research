import json, sys, datetime as dt, statistics as st
def load(t):
    j=json.load(open(f'dl/yh_{t}.json'))['chart']['result'][0]
    ts=j['timestamp']; c=j['indicators']['quote'][0]['close']
    out=[]
    for a,b in zip(ts,c):
        if b is None: continue
        d=dt.datetime.utcfromtimestamp(a).strftime('%Y-%m-%d'); out.append((d,b))
    return out
def at(rows,d):
    x=[v for dd,v in rows if dd<=d]; return x[-1]
def avg(rows,a,b):
    x=[v for d,v in rows if a<=d<=b]; return st.mean(x)
print('tkr  Q3avg/Q2avg  endQ3/endQ2  Oct12/endQ3  Oct12/Jul15  Oct12/Sep01  52wk-ish max(date) last')
for t in sys.argv[1:]:
    r=load(t)
    q2=avg(r,'2026-04-01','2026-06-30'); q3=avg(r,'2026-07-01','2026-09-30')
    e2=at(r,'2026-06-30'); e3=at(r,'2026-09-30'); l=r[-1]
    j15=at(r,'2026-07-14'); s1=at(r,'2026-08-31')
    mx=max(r,key=lambda x:x[1])
    print(f"{t:5s} {100*(q3/q2-1):+7.2f}% {100*(e3/e2-1):+8.2f}% {100*(l[1]/e3-1):+8.2f}% {100*(l[1]/j15-1):+8.2f}% {100*(l[1]/s1-1):+8.2f}%  {mx[0]} {mx[1]:.2f}  {l[0]} {l[1]:.2f}")
