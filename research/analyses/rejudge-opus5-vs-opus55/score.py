import json,sys,random,statistics as st
sys.path.insert(0,'/tmp/claude-0/-home-user-claude-research/6dc1c6c2-fdc8-5fd8-97a8-16311f29aa9a/scratchpad')
L={r['run_date']+'/'+r['ticker']:r for r in json.load(open('dashboard/data/ledger.json'))['names']}
arms={'live_5.5':{k:L[k]['impact_sum'] for k in L if '2026-09-23'<=k[:10]<='2026-09-29' and not L[k].get('pending')}}
for nm,p in [a.split('=') for a in sys.argv[1:]]:
    arms[nm]={o['id']:o['impact_sum'] for o in json.load(open(p))}
ids=sorted(arms['live_5.5'])
def rk(a):
    s=sorted(range(len(a)),key=lambda i:a[i]);r=[0]*len(a);i=0
    while i<len(a):
        j=i
        while j+1<len(a) and a[s[j+1]]==a[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2
        i=j+1
    return r
def sp(x,y):
    a,b=rk(x),rk(y);ma,mb=st.mean(a),st.mean(b);d=(sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))**.5
    return sum((p-ma)*(q-mb) for p,q in zip(a,b))/d if d else 0
def pooled(sc,ky,perm=False):
    days={}
    for i in ids: days.setdefault(i[:10],[]).append(i)
    D=[([sc[i] for i in v],[L[i][ky] for i in v]) for v in days.values() if len(v)>=3]
    f=lambda D: sum(sp(x,y)*len(x) for x,y in D)/sum(len(x) for x,y in D)
    o=f(D)
    if not perm: return o
    random.seed(1);c=sum(1 for _ in range(4000) if abs(f([(x,random.sample(y,len(y))) for x,y in D]))>=abs(o)-1e-12)
    return o,c/4000
ky='mv_strategy'
print(f"{'arm':10s} {'zeros':>5s} {'med|x|':>6s} {'rho_close':>9s} {'rho_strat (p)':>15s} | book |x|>=3 ($0.2m floor): n, hit, mean/name | |x|>=1.5 | sign-all mean")
for nm,sc in arms.items():
    x=[sc.get(i,0) or 0 for i in ids]; sc={i:(sc.get(i,0) or 0) for i in ids}
    r1=pooled(sc,'mv_close'); r2,p=pooled(sc,ky,True)
    out=[]
    for thr in (3,1.5):
        B=[i for i in ids if abs(sc[i])>=thr and (L[i].get('dollar_vol') or 0)>=2e5]
        rets=[(1 if sc[i]>0 else -1)*L[i][ky] for i in B]
        out.append(f"{len(B)}, {sum(r>0 for r in rets)}/{len(B)}, {st.mean(rets):+.2f}%" if B else "0")
    nz=[i for i in ids if sc[i]]
    sa=st.mean([(1 if sc[i]>0 else -1)*L[i][ky] for i in nz]) if nz else 0
    print(f"{nm:10s} {sum(1 for v in x if v==0):5d} {st.median([abs(v) for v in x]):6.2f} {r1:+9.3f} {r2:+8.3f} ({p:.2f}) | {out[0]} | {out[1]} | {sa:+.2f}% on {len(nz)}")
