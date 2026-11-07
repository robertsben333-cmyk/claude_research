"""All US earnings events in the repo's universe files (amc + bmo), with E-P calls (version from
provenance), the Aug-Sep backtest calls and stage M rows attached. No prices. Run from repo root."""
import json, glob, sys, collections, datetime as dt
from pathlib import Path
OUT = sys.argv[1]
def load(p):
    try: return json.load(open(p))
    except Exception: return None
ev = {}
for f in sorted(glob.glob('research/2026/*/*/edge*/universe.json')):
    if f.split('/')[-2] not in ('edge', 'edge-panel'): continue
    for n in (load(f) or {}).get('names', []):
        if n.get('session') not in ('amc', 'bmo') or not n.get('event_date'): continue
        k = (n['ticker'], n['event_date'])
        e = ev.setdefault(k, dict(ticker=n['ticker'], event_date=n['event_date'], session=n['session'],
                                  mcap=n.get('market_cap_usd'), calls=[], implied=None, m=None))
# implied / expected move from any baseline
for f in sorted(glob.glob('research/2026/*/*/edge*/baselines/*.json')):
    if f.split('/')[-3] not in ('edge', 'edge-panel'): continue
    b = load(f) or {}
    k = (b.get('ticker'), b.get('event_date'))
    if k not in ev: continue
    o = b.get('options') or {}
    im = o.get('event_implied_move_pct')
    if im: ev[k]['implied'] = im
for f in sorted(glob.glob('research/2026/*/*/edge-panel/edge-scores-panel.json')):
    run = Path(f).parent; d = run.parent.name
    doc = load(f) or {}; prov = load(run / 'provenance.json') or {}
    ver = (prov.get('stage_version') or {}).get('id')
    U = {n['ticker']: n for n in (load(run / 'universe.json') or {}).get('names', [])}
    for r in doc.get('ranking') or []:
        n = U.get(r['ticker'], {})
        if r.get('side') not in (1, -1) or r.get('panel_pct') is None: continue
        k = (r['ticker'], n.get('event_date'))
        if k not in ev: continue
        ev[k]['calls'].append(dict(src='EP', ver=ver, run_day=d, side=r['side'], pct=r['panel_pct'],
                                   strong=r['panel_pct'] >= 80 and r.get('n_members') == 4))
an = load('research/analyses/panel-mean-pct/panel-mean-pct.json')
for r in an['datasets']['backtest']['US']['rows']:
    p = r['comb']['impact_sum']['gemiddelde']
    if not p: continue
    U = {n['ticker']: n for n in (load(f"research/{r['date'][:4]}/{r['date'][5:7]}/{r['date']}/edge/universe.json") or {}).get('names', [])}
    n = U.get(r['ticker']) or {}
    k = (r['ticker'], n.get('event_date'))
    if k not in ev: continue
    ev[k]['calls'].append(dict(src='BT', ver='backtest', run_day=r['date'], side=1 if p > 0 else -1, pct=abs(p), strong=abs(p) >= 80))
# stage M (advice + review), keyed by ticker/event_date
for d in sorted(glob.glob('research/2026/*/*/morning')):
    a = load(d + '/morning-advice.json') or {}
    for r in a.get('rows', []):
        k = (r['ticker'], r.get('event_date'))
        if k not in ev: continue
        rv = load(f"{d}/reviews/{r['ticker']}.json") or {}
        ev[k]['m'] = dict(day=a['date'], adv=r, rev=rv)
E = list(ev.values())
json.dump(E, open(OUT, 'w'))
c = collections.Counter((e['session']) for e in E)
print(len(E), c, 'implied', sum(1 for e in E if e['implied']), 'stageM', sum(1 for e in E if e['m']))
print(collections.Counter((x['ver'], x['strong']) for e in E for x in e['calls']))
print(min(e['event_date'] for e in E), max(e['event_date'] for e in E))
