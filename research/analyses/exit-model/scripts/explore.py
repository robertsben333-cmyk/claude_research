"""Exploratory, written AFTER the pre-registered results: (1) size of the down-gap effect,
(2) stage M 'read beyond price' as a contrarian signal, split by period (earlier 36-name check
covered 21-27 Oct). Usage: explore.py rows.json"""
import json, sys, statistics as st, collections
from lib import tt, p_from_t
R = json.load(open(sys.argv[1]))
def s(v, d):
    by = collections.defaultdict(list)
    for x, dd in zip(v, d): by[dd].append(x)
    dm = [st.mean(x) for x in by.values()]; t = tt(v); td = tt(dm)
    return f"n {len(v)} mean {st.mean(v):+.2f} t {None if t is None else round(t,2)} p {None if t is None else round(p_from_t(t,len(v)),3)} | days {len(dm)} t_days {None if td is None else round(td,2)} pos {sum(x>0 for x in dm)}"
mk = [r for r in R if abs(r['gap']) >= 2]
print('## 1. Gap-side move open->13:00 (Y1) and open->10:00 (Y2) by gap direction')
for per, S in (('train', [r for r in mk if r['day'] <= '2026-10-20']), ('holdout', [r for r in mk if r['day'] > '2026-10-20'])):
    for g in (1, -1):
        for sess in ('amc', 'bmo'):
            T = [r for r in S if r['g'] == g and r['session'] == sess]
            if len(T) > 3:
                print(per, 'up ' if g > 0 else 'down', sess, 'Y1', s([r['Y1'] for r in T], [r['day'] for r in T]))
print('\n## 1b. Rule on our calls: down gap -> sell longs at the open (bmo) / hold shorts to 13:00 (amc); else default')
for ver in ('us-panel.v2', 'us-panel.v3', 'backtest'):
    for strong in (False, True):
        G, D = [], []
        for r in R:
            for c in r['calls']:
                if c['ver'] != ver or (strong and not c['strong']): continue
                a = c['side'] * r['g']; gain = 0.0
                if r['g'] < 0 and abs(r['gap']) >= 2:
                    if r['session'] == 'amc' and a > 0: gain = a * r['Y1']
                    if r['session'] == 'bmo' and a < 0: gain = -a * r['Y1']
                G.append(gain); D.append(r['day']); break
        if len(G) > 3: print(ver, 'strong' if strong else 'all', s(G, D))
print('\n## 2. Stage M: release read minus pre-market, on our side (S3), vs position gain open->13:00')
M = [r for r in R if r.get('m') and r['m']['day'] >= '2026-10-21' and r['m']['action'] != 'none' and r['m'].get('side')
     and r['m']['read'] is not None and r['m']['pmref_pct'] is not None]
for lab, f in (('21-27 Oct (earlier check)', lambda r: r['m']['day'] <= '2026-10-27'), ('28 Oct - 6 Nov (new)', lambda r: r['m']['day'] > '2026-10-27')):
    T = [r for r in M if f(r)]
    hi = [r for r in T if r['m']['side'] * (r['m']['read'] - r['m']['pmref_pct']) > 3]
    lo = [r for r in T if r['m']['side'] * (r['m']['read'] - r['m']['pmref_pct']) <= 3]
    for nm, U in (('read >3 beyond pre-market on our side', hi), ('rest', lo)):
        if len(U) > 2:
            print(lab, nm, 'open->13:00', s([r['m']['side'] * r['open_to_1300'] for r in U], [r['day'] for r in U]),
                  '| 13:00->close', s([r['m']['side'] * r['x1300_to_close'] for r in U], [r['day'] for r in U]))
