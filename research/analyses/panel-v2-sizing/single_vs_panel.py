import json, glob, os, random, statistics as st, math
A='/home/user/claude_research/research/analyses/rejudge-four-models'
key={r['id']:r for r in json.load(open(f'{A}/key.json'))}
pid={r.get('pid',r['id']):r['id'] for r in key.values()}
M={'opus5':'opus5','opus55':'opus','sonnet55':'sonnet','fable51':'fable'}
sc={m:{} for m in M}; pu={m:{} for m in M}; am={m:{} for m in M}
for m,tag in M.items():
    for f in glob.glob(f'{A}/out-*-{tag}.json'):
        for o in json.load(open(f)):
            i=pid.get(o['id'])
            if i is None: continue
            sc[m][i]=float(o.get('impact_sum') or 0); pu[m][i]=o.get('p_up'); am[m][i]=o.get('abs_move_pct')
ids=[i for i in key if all(i in sc[m] for m in M)]
ids=[i for i in ids if key[i]['region']!='us' or (key[i].get('dollar_vol') or 0)>=2e5]
sgn=lambda x:(x>0)-(x<0)
def bucket(i):
    r=key[i]; return (r['region']=='us', r['day']>='2026-09-23')
live={i:float(key[i]['live'] or 0) for i in ids}
# z per member: score / rms of that member over all names (panel_score uses each member's own history rms)
z={}
for m in M:
    rms=math.sqrt(st.mean(sc[m][i]**2 for i in ids)); z[m]={i:sc[m][i]/rms for i in ids}
rmsl={}
for b in {bucket(i) for i in ids}:
    v=[live[i] for i in ids if bucket(i)==b]; rmsl[b]=math.sqrt(st.mean(x*x for x in v)) or 1
z['live']={i:live[i]/rmsl[bucket(i)] for i in ids}
mem=list(M)
med=lambda v: st.median(v)
arms={'live':z['live'],**{m:z[m] for m in mem},
      'panel_median':{i:med([z[m][i] for m in mem]) for i in ids},
      'panel_mean':{i:st.mean([z[m][i] for m in mem]) for i in ids}}
# own-top-20% sets per member within bucket
def topset(score,share=0.2):
    out=set(); B={}
    for i in ids: B.setdefault(bucket(i),[]).append(i)
    for v in B.values():
        k=max(1,round(share*len(v))); r=sorted((i for i in v if score[i]!=0),key=lambda i:(-abs(score[i]),i)); out|=set(r[:k])
    return out
tops={m:topset(z[m]) for m in mem}
kk={}
for i in ids:
    side=sgn(arms['panel_median'][i]); kk[i]=sum(i in tops[m] and sgn(z[m][i])==side!=0 for m in mem)
def stats(sel,score):
    ret=[sgn(score[i])*key[i]['move'] for i in sel if sgn(score[i])]
    if not ret: return (0,0,None,None)
    n=len(ret); h=sum(x>0 for x in ret); mu=st.mean(ret); se=st.stdev(ret)/math.sqrt(n) if n>1 else float('nan')
    return (n,h,mu,mu/se if se==se and se>0 else float('nan'))
def band(score,lo,hi,sub=None):
    out=[]; B={}
    for i in (sub or ids): B.setdefault(bucket(i),[]).append(i)
    for v in B.values():
        r=sorted((i for i in v if score[i]!=0),key=lambda i:(-abs(score[i]),i)); N=len(v)
        out+= [i for j,i in enumerate(r) if lo*N<=j<hi*N]
    return out
def rank(a):
    s=sorted(range(len(a)),key=lambda i:a[i]); r=[0]*len(a); i=0
    while i<len(a):
        j=i
        while j+1<len(a) and a[s[j+1]]==a[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2
        i=j+1
    return r
def sp(x,y):
    a,b=rank(x),rank(y); ma,mb=st.mean(a),st.mean(b); d=math.sqrt(sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))
    return sum((p-ma)*(q-mb) for p,q in zip(a,b))/d if d else 0
def dayrho(score,sub,perm=2000):
    D={}
    for i in sub: D.setdefault((key[i]['region'],key[i]['day']),[]).append(i)
    D=[v for v in D.values() if len(v)>=3]
    obs=st.mean(sp([score[i] for i in v],[key[i]['move'] for i in v]) for v in D)
    random.seed(1); c=0
    for _ in range(perm):
        t=st.mean(sp(random.sample([score[i] for i in v],len(v)),[key[i]['move'] for i in v]) for v in D)
        c+= t>=obs
    return obs,c/perm
groups={'all':ids,'us':[i for i in ids if key[i]['region']=='us'],'exus':[i for i in ids if key[i]['region']!='us'],
        'us_pre0923':[i for i in ids if key[i]['region']=='us' and key[i]['day']<'2026-09-23']}
res={}
for g,sub in groups.items():
    print(f'\n=== {g} n={len(sub)}  short-all {st.mean(-key[i]["move"] for i in sub):+.2f}')
    print(f'{"arm":13s} {"rho(p)":>14s} | {"top10":>16s} {"top20":>16s} {"20-50%":>16s} {"50-100%":>16s} | nonzero-all')
    for a,s in arms.items():
        r,p=dayrho(s,sub,500)
        cells=[]
        for lo,hi in [(0,.1),(0,.2),(.2,.5),(.5,1.0)]:
            n,h,mu,t=stats(band(s,lo,hi,sub),s); cells.append(f'{h}/{n} {mu:+.2f} t{t:.1f}' if n else '-')
        n,h,mu,t=stats([i for i in sub if s[i]!=0],s)
        print(f'{a:13s} {r:+.3f} ({p:.2f})  | '+' '.join(f'{c:>16s}' for c in cells)+f' | {h}/{n} {mu:+.2f}')
        res[(g,a)]=dict(rho=r,p=p)
    for k in [4,3,2,1,0]:
        sel=[i for i in sub if kk[i]==k]
        n,h,mu,t=stats(sel,arms['panel_median'])
        print(f'  consensus_k={k}: {h}/{n} {mu if mu is not None else float("nan"):+.2f} t{t if t else float("nan"):.1f}  mean|move| {st.mean(abs(key[i]["move"]) for i in sel) if sel else 0:.1f}')
    # among k<=1: does unanimous sign help?
    for lab,cond in [('k<=1 & 4 agree sign',lambda i:kk[i]<=1 and len({sgn(z[m][i]) for m in mem})==1 and sgn(z[mem[0]][i])!=0),
                     ('k<=1 & split sign',lambda i:kk[i]<=1 and not (len({sgn(z[m][i]) for m in mem})==1 and sgn(z[mem[0]][i])!=0))]:
        sel=[i for i in sub if cond(i)]; n,h,mu,t=stats(sel,arms['panel_median'])
        print(f'  {lab}: {h}/{n} {mu if mu is not None else float("nan"):+.2f}')
# Brier on p_up
print('\n=== Brier on P(up), all names with p_up, lower is better (0.25 = coin)')
for g,sub in groups.items():
    out=[]
    for m in mem:
        v=[(pu[m][i]/100, key[i]['move']>0) for i in sub if pu[m][i] is not None]
        out.append(f'{m} {st.mean((p-y)**2 for p,y in v):.4f}')
    v=[(st.mean(pu[m][i] for m in mem)/100, key[i]['move']>0) for i in sub if all(pu[m][i] is not None for m in mem)]
    out.append(f'mean4 {st.mean((p-y)**2 for p,y in v):.4f}')
    # extremized (a=2 on log-odds)
    def ext(p,a=2.0):
        p=min(max(p,1e-3),1-1e-3); lo=math.log(p/(1-p))*a; return 1/(1+math.exp(-lo))
    out.append(f'mean4_ext2 {st.mean((ext(p)-y)**2 for p,y in v):.4f}')
    print(g, ' | '.join(out))

