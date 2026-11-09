import json,glob,os,sys
R='/home/user/claude_research'
S=os.path.dirname(os.path.abspath(__file__))
sb=json.load(open(R+'/dashboard/data/scorebord.json'))
ret={}
for r in sb['week']:
    if r['stage'] in('US · E-P panel','Europa · panel') and r['state']=='opgelost' and r['move'] is not None:
        ret[('us' if r['stage'].startswith('US') else 'eu',r['run_date'],r['ticker'])]=r
rows=[];miss=[]
for d in sorted(glob.glob(S+'/work/*')):
    name=os.path.basename(d); mk=name[:2]; date=name[3:13]
    if not os.path.exists(d+'/out.json'): continue
    out={o['id']:o for o in json.load(open(d+'/out.json'))}
    run=f"{R}/research/{date[:4]}/{date[5:7]}/{date}/"+('edge-panel' if mk=='us' else 'europe')
    ps=json.load(open(run+'/edge-scores-panel.json'))
    rk={x['id']:x for x in ps['ranking']}
    ver=(json.load(open(run+'/provenance.json')).get('stage_version') or {}).get('id')
    for p in json.load(open(d+'/packs.json')):
        i=p['id']; t=i.split('/')[-1]; o=out.get(i)
        if not o: miss.append(i); continue
        x=rk.get(i); rr=ret.get((mk,date,t))
        b=p['baseline']
        em=b.get('expected_move_pct'); 
        if isinstance(b.get('expected_move'),dict): em=b['expected_move'].get('pct') or b['expected_move'].get('expected_move_pct')
        row=dict(id=i,market=mk,date=date,ticker=t,version=ver,session=b.get('session'),exp_move=em,
                 f52=o['impact_sum'],f52_p_up=o['p_up'],f52_abs=o['abs_move_pct'],f52_nf=len(o.get('findings',[])),
                 move=rr['move'] if rr else None, panel_pct_signed=None)
        if x:
            row['panel_pct_signed']=x.get('panel_pct_signed'); row['n_members']=x.get('n_members')
            for m,v in x['members'].items(): row[m]=v['impact_sum']; row[m+'_pct']=v.get('pct_signed')
        rows.append(row)
json.dump(rows,open(S+'/rows.json','w'),indent=0)
import collections
print(len(rows),'rows; resolved',sum(r['move'] is not None for r in rows),'missing ids',miss[:5],len(miss))
print(collections.Counter((r['market'],r['version']) for r in rows if r['move'] is not None))
