"""Event list: every bmo earnings event in the repo's universe files, with E-P panel calls
and the Aug-Sep backtest calls attached. Run from the repo root."""
import json, glob, sys
from pathlib import Path
OUT = sys.argv[1]
def load(p):
    try: return json.load(open(p))
    except Exception: return None
ev = {}
for f in sorted(glob.glob('research/2026/*/*/edge*/universe.json')):
    if not (f.split('/')[-2] in ('edge', 'edge-panel')): continue
    for n in (load(f) or {}).get('names', []):
        if n.get('session') != 'bmo' or not n.get('event_date'): continue
        if n['event_date'] > '2026-11-04': continue
        ev.setdefault((n['ticker'], n['event_date']), dict(ticker=n['ticker'], event_date=n['event_date'], calls=[]))
for f in sorted(glob.glob('research/2026/*/*/edge-panel/edge-scores-panel.json')):
    run = Path(f).parent; d = run.parent.name
    doc = load(f) or {}; prov = load(run / 'provenance.json') or {}
    ver = (prov.get('stage_version') or {}).get('id')
    U = {n['ticker']: n for n in (load(run / 'universe.json') or {}).get('names', [])}
    for r in doc.get('ranking') or []:
        n = U.get(r['ticker'], {})
        if n.get('session') != 'bmo' or r.get('side') not in (1, -1) or r.get('panel_pct') is None: continue
        k = (r['ticker'], n['event_date'])
        if k not in ev: continue
        ev[k]['calls'].append(dict(src='EP', ver=ver, run_day=d, side=r['side'], pct=r['panel_pct'],
                                   strong=r['panel_pct'] >= 80 and r.get('n_members') == 4))
an = load('research/analyses/panel-mean-pct/panel-mean-pct.json')
for r in an['datasets']['backtest']['US']['rows']:
    p = r['comb']['impact_sum']['gemiddelde']
    if not p: continue
    U = {n['ticker']: n for n in (load(f"research/{r['date'][:4]}/{r['date'][5:7]}/{r['date']}/edge/universe.json") or {}).get('names', [])}
    n = U.get(r['ticker']) or {}
    if n.get('session') != 'bmo': continue
    k = (r['ticker'], n['event_date'])
    ev.setdefault(k, dict(ticker=r['ticker'], event_date=n['event_date'], calls=[]))
    ev[k]['calls'].append(dict(src='BT', ver='backtest', run_day=r['date'], side=1 if p > 0 else -1, pct=abs(p), strong=abs(p) >= 80))
json.dump(list(ev.values()), open(OUT, 'w'))
import collections
c = collections.Counter((x['ver'], x['strong']) for e in ev.values() for x in e['calls'])
print(len(ev), 'bmo events;', sorted(c.items(), key=str))
