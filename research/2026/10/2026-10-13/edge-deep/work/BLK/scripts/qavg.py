import csv, sys, statistics as st
def load(p):
    rows=[]
    with open(p) as f:
        r=csv.reader(f); next(r)
        for d,v in r:
            try: rows.append((d,float(v)))
            except: pass
    return rows
for s in sys.argv[1:]:
    rows=load(f'dl/fred_{s}.csv')
    def avg(a,b):
        x=[v for d,v in rows if a<=d<=b]; return (st.mean(x) if x else None, len(x))
    def last(a,b):
        x=[(d,v) for d,v in rows if a<=d<=b]; return x[-1] if x else None
    def first(a,b):
        x=[(d,v) for d,v in rows if a<=d<=b]; return x[0] if x else None
    q2=avg('2026-04-01','2026-06-30'); q3=avg('2026-07-01','2026-09-30')
    m7=avg('2026-07-01','2026-07-31'); m8=avg('2026-08-01','2026-08-31'); m9=avg('2026-09-01','2026-09-30')
    e2=last('2026-04-01','2026-06-30'); e3=last('2026-07-01','2026-09-30'); lt=rows[-1]
    print(s, 'Q2avg %.2f n%d'%q2, 'Q3avg %.2f n%d'%q3, 'chg %.2f%%'%((q3[0]/q2[0]-1)*100),
          '| Jul %.1f Aug %.1f Sep %.1f'%(m7[0],m8[0],m9[0]), '| end Q2',e2,'end Q3',e3,'chg %.2f%%'%((e3[1]/e2[1]-1)*100), '| latest',lt)
    hi=max(rows,key=lambda x:x[1]); lo=min([r for r in rows if r[0]>='2026-07-01'],key=lambda x:x[1])
    print('   max since Mar',hi,' min since Jul',lo)
