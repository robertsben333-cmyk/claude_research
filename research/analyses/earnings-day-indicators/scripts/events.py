"""All E-P baselines on the v2/v3 run days -> events.json"""
import json,glob,os
REPO='/home/user/claude_research'
R=json.load(open('/mnt/project-files/quant-selection-score/rows.json'))
days=sorted({r['d'] for r in R}); ver={r['d']:r['v'] for r in R}
E=[]
for d in days:
  for f in sorted(glob.glob(f"{REPO}/research/{d[:4]}/{d[5:7]}/{d}/edge-panel/baselines/*.json")):
    b=json.load(open(f))
    if b.get('session') not in ('amc','bmo') or not b.get('event_date'): continue
    o=b.get('options') or {}; h=b.get('history') or {}; t=b.get('tape') or {}
    mv=h.get('moves') or []
    prev=None
    for m in sorted(mv,key=lambda m:m['event_date'],reverse=True):
      if m['event_date']<d and m.get('move_pct') is not None: prev=m['move_pct']; break
    E.append(dict(d=d,v=ver[d],t=b['ticker'],ev=b['event_date'],ses=b['session'],
      skew=o.get('skew_25d_vol_points'),pcr=o.get('put_call_open_interest_ratio'),
      iv=o.get('atm_iv_pct'),imp=o.get('event_implied_move_pct'),hmed=h.get('median_abs_move_pct'),
      prev=prev,rv=t.get('realised_vol_20d_annualised_pct')))
json.dump(E,open('../events.json','w'))
print(len(E),len({e['t'] for e in E}))
