import json, math, random, statistics as st
def sgn(x): return (x > 0) - (x < 0)
def mean(x): x=[v for v in x if v is not None]; return st.mean(x) if x else None
def tt(x):
    x=[v for v in x if v is not None]
    if len(x)<3: return None
    s=st.stdev(x); return None if s==0 else st.mean(x)/(s/math.sqrt(len(x)))
def p_from_t(t, n):
    if t is None: return None
    # normal approx two-sided; fine for n>=20, note for small
    return math.erfc(abs(t)/math.sqrt(2))
def rank(v):
    o=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
    while i<len(v):
        j=i
        while j+1<len(v) and v[o[j+1]]==v[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2
        i=j+1
    return r
def pearson(a,b):
    ma,mb=st.mean(a),st.mean(b); c=sum((x-ma)*(y-mb) for x,y in zip(a,b))
    va=sum((x-ma)**2 for x in a); vb=sum((y-mb)**2 for y in b)
    return c/math.sqrt(va*vb) if va and vb else 0
def spearman(a,b,days=None,nperm=2000,seed=1):
    pairs=[(x,y,d) for x,y,d in zip(a,b,days or [0]*len(a)) if x is not None and y is not None]
    if len(pairs)<8: return None
    x=[p[0] for p in pairs]; y=[p[1] for p in pairs]; d=[p[2] for p in pairs]
    rx,ry=rank(x),rank(y); rho=pearson(rx,ry)
    # permutation within day
    rnd=random.Random(seed); idx={}
    for i,dd in enumerate(d): idx.setdefault(dd,[]).append(i)
    ge=0
    for _ in range(nperm):
        yy=ry[:]
        for ii in idx.values():
            v=[ry[i] for i in ii]; rnd.shuffle(v)
            for i,val in zip(ii,v): yy[i]=val
        if abs(pearson(rx,yy))>=abs(rho)-1e-12: ge+=1
    return dict(rho=round(rho,3), p=round((ge+1)/(nperm+1),4), n=len(pairs))
def day_t(vals, days):
    by={}
    for v,d in zip(vals,days):
        if v is not None: by.setdefault(d,[]).append(v)
    m=[st.mean(v) for v in by.values()]
    return dict(days=len(m), mean_of_days=round(st.mean(m),2) if m else None, t_days=round(tt(m),2) if tt(m) is not None else None, pos_days=sum(x>0 for x in m))
def summ(vals, days=None):
    v=[x for x in vals if x is not None]
    out=dict(n=len(v), mean=round(mean(v),2) if v else None, t=round(tt(v),2) if tt(v) is not None else None)
    if out['t'] is not None: out['p']=round(p_from_t(out['t'],len(v)),3)
    if days: out.update(day_t(vals,days))
    return out
