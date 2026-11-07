"""Per-event features (known at 09:30) and outcomes. Usage: build.py ev.json bars_dir rows.json"""
import json, sys, math, statistics as st, collections, os
EV, B, OUT = sys.argv[1:4]
E = json.load(open(EV))
nday = collections.Counter(e.get('react_day') for e in E if e.get('react_day'))
def px_at(m1, minute):          # close of last bar starting at or before minute-1 (i.e. price at `minute`)
    c = [b for b in m1 if 570 <= b[0] < minute]
    return c[-1][4] if c else None
rows = []
for e in E:
    rd = e.get('react_day')
    if not rd: continue
    p = f"{B}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p))
    if 'error' in d or not d.get('d') or not d.get('m1'): continue
    daily = [x for x in d['d'] if x[0] < rd]
    if len(daily) < 21: continue
    prev = daily[-1][4]
    m1 = d['m1']
    ob = [b for b in m1 if 570 <= b[0] <= 574]
    if not ob or not prev: continue
    popen = ob[0][1]
    p1000, p1300, pclose = px_at(m1, 600), px_at(m1, 780), px_at(m1, 960)
    if not (p1000 and p1300 and pclose): continue
    if sum(1 for b in m1 if 570 <= b[0] < 960) < 60: continue
    pm = [b for b in m1 if 240 <= b[0] < 570]
    pmref = st.median([b[4] for b in pm[-5:]]) if pm else None
    p08 = [b for b in pm if b[0] <= 480]
    p08 = p08[-1][4] if p08 else (pm[0][1] if pm else None)
    pmdv = sum(b[4] * b[5] for b in pm)
    adv = st.mean([x[4] * x[5] for x in daily[-20:]])
    lr = [math.log(daily[i][4] / daily[i - 1][4]) for i in range(len(daily) - 20, len(daily))]
    rv = st.stdev(lr) * 100
    runup = (prev / daily[-21][4] - 1) * 100
    gap = (popen / prev - 1) * 100
    g = 1 if gap > 0 else -1
    f = lambda x: None if x is None else round(x, 4)
    r = dict(ticker=e['ticker'], event_date=e['event_date'], session=e['session'], day=rd, gap=f(gap), g=g,
             prev=prev, open=popen, pmref=pmref,
             pmgap=f((pmref / prev - 1) * 100) if pmref else None,
             # outcomes, gap side
             Y1=f(g * (p1300 - popen) / prev * 100), Y2=f(g * (p1000 - popen) / prev * 100),
             Y3=f(g * (pclose - p1300) / prev * 100),
             # raw position-free moves for call evaluation
             open_to_1300=f((p1300 - popen) / prev * 100), open_to_1000=f((p1000 - popen) / prev * 100),
             x1300_to_close=f((pclose - p1300) / prev * 100),
             pm_to_open=f((popen - pmref) / prev * 100) if pmref else None,
             # factors (raw)
             F1=f(abs(gap) / e['implied']) if e.get('implied') else None,
             F2=f(math.log(1 + nday[rd])),
             F3=f(math.log(max(pmdv, 1) / adv)) if adv > 0 else None,
             F4=f(math.log(adv)) if adv > 0 else None,
             F5=f(g * runup),
             F6=f(g * (popen - pmref) / prev * 100) if pmref else None,
             F7=f(g * (pmref - p08) / prev * 100) if (pmref and p08) else None,
             F8=1 if g < 0 else 0, F9=1 if e['session'] == 'bmo' else 0, F10=f(rv),
             implied=e.get('implied'), calls=e['calls'], m=None)
    # Y0: amc earlier exit, pm reference to open in the pm gap direction
    if pmref and r['pmgap']:
        gp = 1 if r['pmgap'] > 0 else -1
        r['Y0'] = f(gp * (popen - pmref) / prev * 100); r['gp'] = gp
    if e.get('m'):
        a, rv_ = e['m']['adv'], e['m']['rev']
        rel = rv_.get('release') or {}
        gd = str((rel.get('guidance') or {}).get('direction') or '')
        tr = (rv_.get('tape_read') or {}).get('read')
        r['m'] = dict(day=e['m']['day'], action=a.get('action'), side=a.get('side'),
                      exp_oc=a.get('expected_open_to_close_pct'), p_fade=a.get('p_fade_by_1000'),
                      read=a.get('release_read_move_pct'),
                      pmref_pct=a.get('premarket_ref_pct_at_compile', a.get('premarket_pct_at_compile')),
                      verdict=rel.get('verdict_vs_bar'),
                      guid=1 if gd.startswith('raised') else (-1 if gd.startswith(('lowered', 'cut')) else 0),
                      tape=1 if tr == 'undershoot' else (-1 if tr == 'overshoot' else 0),
                      limit=a.get('limit_price'))
    rows.append(r)
json.dump(rows, open(OUT, 'w'))
print(len(rows), 'rows;', sum(1 for r in rows if abs(r['gap']) >= 2), 'with |gap|>=2')
