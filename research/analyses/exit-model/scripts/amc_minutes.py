"""amc: exit at the open vs 1, 2, 3, 5 minutes later. Price at 09:3x = close of the 1-min bar ending then.
Usage: amc_minutes.py rows.json bars_dir"""
import json, sys, statistics as st, collections
from lib import tt, p_from_t
R = json.load(open(sys.argv[1])); B = sys.argv[2]
MIN = [1, 2, 3, 5]
def px(m1, k):   # price at 09:30+k
    c = [b for b in m1 if 570 <= b[0] < 570 + k]
    return c[-1][4] if c and c[-1][0] == 570 + k - 1 else None
def s(v, d):
    if len(v) < 3: return f"n {len(v)}"
    by = collections.defaultdict(list)
    for x, dd in zip(v, d): by[dd].append(x)
    dm = [st.mean(x) for x in by.values()]; t = tt(v); td = tt(dm)
    return f"n {len(v)} {st.mean(v):+.2f} t {round(t,2) if t else None} p {round(p_from_t(t,len(v)),3) if t else None} beter {sum(x>0 for x in v)} | dagen {len(dm)} t {round(td,2) if td else None}"
rows = []
for r in R:
    if r['session'] != 'amc': continue
    d = json.load(open(f"{B}/{r['ticker']}_{r['event_date']}.json"))
    p = {k: px(d['m1'], k) for k in MIN}
    if any(v is None for v in p.values()): continue
    r['dk'] = {k: (p[k] - r['open']) / r['prev'] * 100 for k in MIN}   # raw move from open, % of prev close
    rows.append(r)
def report(lab, items):   # items: (row, side)
    print(f"\n### {lab}")
    for k in MIN:
        print(f"  09:3{k}: " + s([sd * r['dk'][k] for r, sd in items], [r['day'] for r, _ in items]))
    for nm, f in (('winst op opening', lambda r, sd: sd * r['gap'] > 0), ('verlies op opening', lambda r, sd: sd * r['gap'] <= 0)):
        sub = [(r, sd) for r, sd in items if f(r, sd)]
        print(f"  {nm}: " + ' | '.join(f"09:3{k} " + s([sd * r['dk'][k] for r, sd in sub], [r['day'] for r, _ in sub]).split(' |')[0] for k in (1, 2)))
for per, f in (('t/m 27 okt', lambda r: r['day'] <= '2026-10-27'), ('28 okt - 6 nov (nieuw)', lambda r: r['day'] > '2026-10-27')):
    mk = [(r, r['g']) for r in rows if abs(r['gap']) >= 2 and f(r)]
    report(f'Markt, alle amc-gaps >=2%, aan de kant van de gap, {per}', mk)
for ver in ('us-panel.v2', 'us-panel.v3'):
    for strong in (False, True):
        it = []
        for r in rows:
            c = next((c for c in r['calls'] if c['ver'] == ver and (c['strong'] or not strong)), None)
            if c: it.append((r, c['side']))
        report(f"Onze calls {ver} {'sterk' if strong else 'alle'}", it)
