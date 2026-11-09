import json,glob,os,subprocess,sys
S='/tmp/claude-0/-home-user-claude-research/45f9f26a-8708-5e3a-b08c-1a1d70c8a4f2/scratchpad/fj'
def sh(*a): return subprocess.run(a,capture_output=True,text=True)
def show(c,p):
    r=sh('git','show',f'{c}:{p}'); return r.stdout if r.returncode==0 else None
jobs=[]
def job(market,date,packfile,part,judge_src):
    c=sh('git','log','--diff-filter=A','--format=%H %cI','--',packfile).stdout.strip().split('\n')[-1].split()
    commit,when=c[0],c[1]
    packs=json.load(open(packfile))
    name=f'{market}-{date}'+(f'-{part}' if part else '')
    d=f'{S}/work/{name}'; os.makedirs(d,exist_ok=True)
    json.dump(packs,open(d+'/packs.json','w'),ensure_ascii=False,indent=1)
    files={'config/hunter-core.md'}
    for p in packs:
        files.add(p.get('hunter_definition','.claude/agents/unpriced-hunter.md')); files.add(p.get('lessons_file','researcher_us/LESSONS.md'))
    for f in files:
        t=show(commit,f)
        if t is None: print('MISSING',name,f); continue
        os.makedirs(os.path.dirname(d+'/'+f),exist_ok=True); open(d+'/'+f,'w').write(t)
    j=show(commit,judge_src)
    open(d+'/JUDGE.md','w').write(j)
    jobs.append(dict(name=name,market=market,date=date,n=len(packs),kb=os.path.getsize(d+'/packs.json')//1000,commit=commit[:8],when=when,dir=d))
for d in sorted(glob.glob('research/2026/1*/*/edge-panel')):
    date=d.split('/')[3]
    if not ('2026-10-12'<=date<='2026-11-06'): continue
    parts=sorted(glob.glob(d+'/panel/packs-p*.json'))
    if parts:
        for f in parts: job('us',date,f,os.path.basename(f)[6:-5],'config/panel-judge.md')
    else: job('us',date,d+'/panel/packs.json','', 'config/panel-judge.md')
for d in sorted(glob.glob('research/2026/1*/*/europe')):
    date=d.split('/')[3]
    f=d+'/panel/packs.json'
    if not os.path.exists(f) or not ('2026-10-12'<=date<='2026-11-06'): continue
    job('eu',date,f,'','config/panel-judge-intl.md')
json.dump(jobs,open(S+'/jobs.json','w'),indent=1)
for j in jobs: print(j['name'],j['n'],j['kb'],j['commit'],j['when'])
print(len(jobs),sum(j['n'] for j in jobs))
