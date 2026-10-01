"""Build key.json and the re-judge packs. First pass wrote packs-us1..apac; the second
pass (packs-x1, x2) adds US hunts saved under suffixed names and the names first left out
for leakage, anonymised: ticker, company name and every URL replaced by placeholders."""
import json,glob,os,re
R='/home/user/claude_research'; os.chdir(R)
OUT='research/analyses/rejudge-four-models'
SIZE=re.compile(r'\b[Ss]ized? (at|to) [^.;]*|\bcut (it )?from [-+]?\d[^.;]*|\(lesson[^)]*\)|\blesson \d+\b[^.;]*|\bp_up\b[^.;]*|\babs_move[^.;]*',re.I)
sc=lambda s: SIZE.sub('[sizing note removed]',s) if isinstance(s,str) else s
NORDIC={'se','dk','no','fi','nordic'}
def eu_hunter(sub): return 'unpriced-hunter-nordic' if (sub or '').lower() in NORDIC else 'unpriced-hunter-'+(sub or 'uk').lower()
def trim(o,depth=0):
    if isinstance(o,dict): return {k:trim(v,depth+1) for k,v in o.items() if k not in ('headlines','raw','bars','series')}
    if isinstance(o,list): return [trim(x,depth+1) for x in o[:12]]
    if isinstance(o,str) and len(o)>600: return o[:600]+'…'
    return o
def evidence(hfiles):
    ev=[]
    for h in hfiles:
        j=json.load(open(h)); tag=os.path.basename(h)
        for f in j.get('findings') or []:
            ev.append({'kind':'filed_by_first_hunter','hunt':tag,'text':sc(f.get('finding')),'lands_on':f.get('lands_on'),'leg':f.get('leg'),'resolves_by':f.get('resolves_by'),'source':f.get('source'),'source_date':f.get('source_date'),
              'reaction_history_on_this_line':sc(f.get('reaction_history_on_this_line')),'why_not_priced':sc(f.get('why_not_priced')),'independence':sc(f.get('independence'))})
        for o in j.get('outside_window') or []:
            ev.append({'kind':'put_outside_window_by_first_hunter','hunt':tag,'text':sc(o.get('finding') if isinstance(o,dict) else o),'resolves_by':(o.get('resolves_by') if isinstance(o,dict) else None),'source':(o.get('source') if isinstance(o,dict) else None)})
        for r in j.get('rejected_candidates') or []:
            ev.append({'kind':'rejected_by_first_hunter','hunt':tag,'text':sc(r.get('candidate')),'source':r.get('source'),'first_hunter_reason':r.get('reason')})
        for s in j.get('searched_and_found_nothing') or []:
            ev.append({'kind':'listed_as_searched_and_found_nothing','hunt':tag,'text':sc(s if isinstance(s,str) else json.dumps(s))})
    for i,e in enumerate(ev): e['i']=i
    return ev
def ctx(h):
    d=json.load(open(h))
    return {'bar':sc(d.get('bar')),'positioning_check':d.get('positioning_check'),'already_public':d.get('already_public'),'new_in_release':d.get('new_in_release'),'session_check':d.get('session_check')}
rows=[]
# US
L=json.load(open('dashboard/data/ledger.json'))['names']
for r in L:
    if r.get('pending') or r.get('duplicate_event') or r.get('mv_strategy') is None: continue
    d=r['run'].rstrip('/'); t=r['ticker']
    hs=sorted(glob.glob(f'{d}/hunts/{t}.json')+glob.glob(f'{d}/hunts/{t}-*.json'))
    b=f'{d}/baselines/{t}.json'
    if not hs or not os.path.exists(b): continue
    rows.append(dict(region='us',day=r['run_date'],ticker=t,company=r.get('company'),hunter='unpriced-hunter',lessons='researcher_us/LESSONS.md',run=d,hunts=hs,baseline=b,
      move=r['mv_strategy'],move_basis='strategy exit (amc at open, bmo 20:00 CET)',live=r['impact_sum'],dollar_vol=r.get('dollar_vol')))
# foreign
for mk,fn,les in [('europe','eu-resolved.json',None),('japan','jp-resolved.json','researcher_japan/LESSONS.md'),('australia','au-resolved.json','researcher_australia/LESSONS.md'),('canada','canada-resolved.json','researcher_canada/LESSONS.md')]:
    for f in sorted(glob.glob(f'research/2026/*/*/{mk}/{fn}')):
        d=os.path.dirname(f); day=d.split('/')[3]
        if mk=='europe' and day in ('2026-09-16','2026-09-17'): continue
        j=json.load(open(f)); rs=j.get('rows') or j.get('names') or []
        for r in rs:
            mv=r.get('realised_move_pct', r.get('move_pct'))
            if mv is None or r.get('move_pending') or r.get('event_occurred') is False or r.get('rankable') is False: continue
            t=r['ticker']; hs=sorted(glob.glob(f'{d}/hunts/{t}.json')+glob.glob(f'{d}/hunts/{t}-*.json'))
            b=f'{d}/baselines/{t}.json'
            if not hs or not os.path.exists(b): continue
            hun={'europe':eu_hunter(r.get('submarket')),'japan':'unpriced-hunter-jp','australia':'unpriced-hunter-au','canada':'unpriced-hunter-ca'}[mk]
            rows.append(dict(region=mk,day=day,ticker=t,company=r.get('company'),hunter=hun,lessons=les,run=d,hunts=hs,baseline=b,move=mv,move_basis=fn,live=r.get('impact_sum'),dollar_vol=r.get('median_turnover_usd_20d')))
# leakage: ticker or company name in any context file
ctxfiles=['CLAUDE.md','config/hunter-core.md']+sorted(set('.claude/agents/%s.md'%r['hunter'] for r in rows))+sorted(set(r['lessons'] for r in rows if r['lessons']))
ctxt='\n'.join(open(p).read() for p in ctxfiles if os.path.exists(p))
def leaked(r):
    if re.search(r'(?<![A-Za-z0-9])'+re.escape(r['ticker'])+r'(?![A-Za-z0-9])',ctxt): return 'ticker'
    c=(r.get('company') or '').replace(',',' ')
    words=[w for w in re.split(r'\s+',c) if w and w.lower() not in ('inc','inc.','plc','ltd','ltd.','corp','corporation','company','co','sa','se','ag','nv','ab','asa','oyj','spa','s.p.a.','the','group','holdings','limited','a/s')]
    if words and len(' '.join(words[:2]))>=6 and ' '.join(words[:2]) in ctxt: return 'company'
    return None
for r in rows: r['leak']=leaked(r)
# ---- extension 2026-10-01 (second pass) ----
# The sealed backtest corpus is deliberately left out (operator's instruction).
for r in rows:
    r['leak']=leaked(r); r['id']=f"{r['region']}/{r['day']}/{r['ticker']}"
# 2. anonymise the names whose ticker or company appears in the context every judge sees
STOP={'inc','inc.','plc','ltd','ltd.','corp','corp.','corporation','company','co','co.','sa','se','ag','nv','ab','asa','oyj','spa','s.p.a.','the','group','holdings','holding','limited','a/s','&','and','of','international','technologies','plc.','n.v.','s.a.'}
URL=re.compile(r'(https?://|www\.)\S+|\b[\w-]+\.(com|net|org|co\.uk|de|fr|it|se|no|dk|fi|pl|es|jp|com\.au|ca|io|ai)\b[/\S]*',re.I)
def scrubber(r):
    pats=[re.escape(r['ticker'])]
    c=(r.get('company') or '').replace(',',' ')
    if c.strip(): pats.append(re.escape(c.strip()))
    ws=[w for w in re.split(r'\s+',c) if w and w.lower() not in STOP]
    if ws:
        if len(' '.join(ws[:2]))>=4: pats.append(re.escape(' '.join(ws[:2])))
        if len(ws[0])>=4: pats.append(re.escape(ws[0]))
    rx=re.compile(r'(?<![A-Za-z0-9])(' + '|'.join(sorted(set(pats),key=len,reverse=True)) + r')(?![A-Za-z0-9])',re.I)
    def f(o):
        if isinstance(o,dict): return {k:f(v) for k,v in o.items()}
        if isinstance(o,list): return [f(x) for x in o]
        if isinstance(o,str): return rx.sub('[THE COMPANY]',URL.sub('[url removed]',o))
        return o
    return f,rx
done=set(x['id'] for f in glob.glob(f'{OUT}/out-*-*.json') for x in json.load(open(f)))
new=[r for r in rows if r['id'] not in done]
packs=[];k=0
for r in new:
    p={'hunter_definition':'.claude/agents/%s.md'%r['hunter'],'lessons_file':r['lessons'],'baseline':trim(json.load(open(r['baseline']))),'first_hunter_context':ctx(r['hunts'][0]),'evidence':evidence(r['hunts'])}
    if r['leak']:
        k+=1; f,rx=scrubber(r); p=f(p); r['anon']=True
        p['baseline']['ticker']='[REDACTED]'; p['baseline']['company']='[REDACTED]'
        p['id']=r['pid']=f"anon/{r['region']}/{k:03d}"
        left=rx.findall(json.dumps(p,ensure_ascii=False)); assert not left,(r['id'],left[:3])
    else:
        p['id']=r['pid']=r['id']
    packs.append(p)
import collections
print('all rows',len(rows),collections.Counter(r['region'] for r in rows))
print('new to judge',len(new),collections.Counter((r['region'],bool(r['leak'])) for r in new))
json.dump([{k:v for k,v in r.items() if k!='hunts'} for r in rows],open('/tmp/rejudge-key2.json','w'),indent=0)
json.dump(packs,open('/tmp/rejudge-packs_new.json','w'))
