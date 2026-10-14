import json, glob, os, sys, random, re
from datetime import datetime, timedelta, timezone
M=sys.argv[1]; sys.path.insert(0, M+'/researcher_japan/scripts')
from jp_priced_in import lean_components
regs=json.load(open(sys.argv[2])); files=sorted(regs)
JST=timezone(timedelta(hours=9))
def rank(x):
    o=sorted(range(len(x)),key=lambda i:x[i]); r=[0]*len(x); i=0
    while i<len(o):
        j=i
        while j+1<len(o) and x[o[j+1]]==x[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2
        i=j+1
    return r
def sp(a,b):
    if len(a)<3: return None
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); den=(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5
    return num/den if den else None
def perm(a,b,n=5000):
    r0=sp(a,b); 
    if r0 is None: return None,None
    rng=random.Random(1); c=0; bb=list(b)
    for _ in range(n):
        rng.shuffle(bb); r=sp(a,bb)
        if r is not None and abs(r)>=abs(r0)-1e-12: c+=1
    return r0,(c+1)/(n+1)
rows=[]; cited=[]
for run in sorted(glob.glob(M+'/research/2026/10/*/japan')):
    day=run.split('/')[-2]
    res={}
    if os.path.exists(run+'/jp-resolved.json'):
        for r in json.load(open(run+'/jp-resolved.json'))['rows']: res[r['ticker']]=r
    for bp in sorted(glob.glob(run+'/baselines/*.json')):
        b=json.load(open(bp)); t=b['ticker']; pos=b.get('positioning') or {}
        seal=datetime.fromisoformat(b['sealed_utc']).astimezone(JST).strftime('%Y%m%d')
        right=max([f for f in files if f<seal], default=None)
        reg=regs[right].get(t, {}) if right else {}
        newpos={'short_ratio_pct':reg.get('short_ratio_pct',0.0),'short_change_pct_pts':reg.get('short_change_pct_pts',0.0)}
        lc_old=b.get('lean_components') or {}
        new=lean_components(newpos, pos.get('margin_ratio'), (b.get('tape') or {}).get('run_up_20d_pct'))
        lean_new=round(sum(v for v in new.values() if v is not None),3)
        r=res.get(t,{})
        mv=r.get('realised_move_pct') if r.get('rankable',True) and r.get('event_occurred',True) is not False else None
        rows.append(dict(day=day,t=t,used=pos.get('as_of'),right=right,sr_old=pos.get('short_ratio_pct'),sr_new=newpos['short_ratio_pct'],
            sc_old=pos.get('short_change_pct_pts'),sc_new=newpos['short_change_pct_pts'],lean_old=b.get('priced_lean_pct'),lean_new=lean_new,
            sq_old=lc_old.get('short_squeeze'),sq_new=new['short_squeeze'],sb_old=lc_old.get('short_building'),sb_new=new['short_building'],
            impact=r.get('impact_sum'),move=mv))
    # hunts citing short register
    for hp in glob.glob(run+'/hunts/*.json'):
        txt=open(hp,encoding='utf-8').read()
        t=os.path.basename(hp).split('.')[0].split('-')[0]
        if re.search(r'空売り|short (register|position|ratio|interest)|JPX register|disclosed short',txt,re.I):
            cited.append((day,t))
json.dump(rows,open(os.path.dirname(sys.argv[2])+'/rows.json','w'),indent=1)
stale=[r for r in rows if r['used']!=r['right']]
print('baselines',len(rows),'sealed on wrong file',len(stale))
diff=[r for r in rows if abs((r['sr_old'] or 0)-r['sr_new'])>=0.01 or abs((r['sc_old'] or 0)-r['sc_new'])>=0.01]
print('names whose register inputs differ',len(diff))
for r in diff: print(f"  {r['day']} {r['t']:5s} level {r['sr_old']}->{r['sr_new']}  chg {r['sc_old']}->{r['sc_new']}  lean {r['lean_old']}->{r['lean_new']}  impact {r['impact']} move {r['move']}")
ld=[abs((r['lean_old'] or 0)-r['lean_new']) for r in rows]; print('lean |delta| mean %.3f max %.3f, >0.25pt on %d'%(sum(ld)/len(ld),max(ld),sum(x>0.25 for x in ld)))
R=[r for r in rows if r['move'] is not None]
print('resolved names',len(R),'days',sorted({r['day'] for r in R}))
for k in ['lean_old','lean_new','sq_old','sq_new','sb_old','sb_new','impact']:
    a=[(r[k] or 0) for r in R]; m=[r['move'] for r in R]; rho,p=perm(a,m); print(f'  rho {k:9s} {rho:+.3f} p={p:.3f}' if rho is not None else f'  {k} n/a')
Rs=[r for r in R if r in diff]; print('resolved AND inputs differ',len(Rs))
def sign_hit(key): 
    z=[r for r in R if (r[key] or 0)!=0]; return sum((r[key]>0)==(r['move']>0) for z1 in [0] for r in z), len(z)
print('sign hit lean_old',sign_hit('lean_old'),'lean_new',sign_hit('lean_new'))
print('hunts mentioning short positions',len(cited),cited)
