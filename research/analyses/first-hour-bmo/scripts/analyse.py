"""Pre-registered tests (PREREG.md). Usage: analyse.py events.json cache_dir > results.txt"""
import json, sys, os, math, statistics as st
sys.path.insert(0, os.path.dirname(__file__))
from lib import spearman, summ, sgn
E = json.load(open(sys.argv[1])); C = sys.argv[2]
def px(m1, T):
    b = [x for x in m1 if x[0] < T]
    return b[-1][4] if b else None
def bars(e):
    p = f"{C}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): return None
    d = json.load(open(p))
    if 'error' in d: return None
    m1 = [x for x in d['m1'] if 570 <= x[0] < 960]
    fh = [x for x in m1 if x[0] < 630]
    if not m1 or m1[0][0] > 575 or len(fh) < 20: return None
    reg = [x for x in d['m30'] if 570 <= x[1] < 960 and x[0] < e['event_date']]
    if not reg: return None
    pc = reg[-1][2]
    by = {}
    for x in reg:
        if x[1] in (570, 600): by[x[0]] = by.get(x[0], 0) + x[3]
    prior = [by[k] for k in sorted(by)[-20:]]
    fv = sum(x[5] for x in fh)
    vw = sum((x[6] or x[4]) * x[5] for x in fh) / fv if fv else None
    o = m1[0][1]; p1030 = px(m1, 630); p13 = px(m1, 780); cl = px(m1, 960)
    orh = max(x[2] for x in m1 if x[0] < 600); orl = min(x[3] for x in m1 if x[0] < 600)
    H = max(x[2] for x in fh); L = min(x[3] for x in fh)
    return dict(pc=pc, o=o, p1030=p1030, p13=p13, cl=cl, orh=orh, orl=orl, H=H, L=L, vw=vw,
                rvol=fv / st.mean(prior) if len(prior) >= 10 and st.mean(prior) > 0 else None)
def feats(b, s):
    r = lambda a, c: s * (a / c - 1) * 100
    gap = (b['o'] / b['pc'] - 1) * 100
    orb = s if b['p1030'] > b['orh'] else (-s if b['p1030'] < b['orl'] else 0)
    clv = (b['p1030'] - b['L']) / (b['H'] - b['L']) if b['H'] > b['L'] else 0.5
    if s < 0: clv = 1 - clv
    gs = None
    if abs(gap) >= 1:
        ret = (b['p1030'] - b['pc']) / (b['o'] - b['pc'])
        withus = sgn(gap) == s
        if ret >= 0.5: gs = 1 if withus else -1
        elif ret <= 0: gs = -1 if withus else 1
        else: gs = 0
    f = dict(fh_ret=r(b['p1030'], b['o']), orb=orb, vwap=r(b['p1030'], b['vw']) if b['vw'] else None,
             gap_state=gs, clv=clv, rvol=b['rvol'], gap_s=s * gap,
             R1=r(b['p13'], b['p1030']), R2=r(b['cl'], b['p1030']), R3=r(b['cl'], b['p13']))
    c = 1 if clv > 2 / 3 else (-1 if clv < 1 / 3 else 0)
    f['trend'] = sgn(f['fh_ret']) + orb + sgn(f['vwap'] or 0) + c
    return f
tiers = {}
for e in E:
    b = bars(e)
    if not b: continue
    gap = (b['o'] / b['pc'] - 1) * 100
    if abs(gap) >= 2:
        tiers.setdefault('T3 all bmo gaps>=2%, gap side', []).append(dict(day=e['event_date'], t=e['ticker'], **feats(b, sgn(gap))))
    for c in e['calls']:
        row = dict(day=e['event_date'], t=e['ticker'], **feats(b, c['side']))
        tiers.setdefault(f"T2 all calls {c['ver']}", []).append(row)
        if c['strong']: tiers.setdefault(f"T1 strong {c['ver']}", []).append(row)
IND = ['trend', 'fh_ret', 'orb', 'vwap', 'gap_state', 'clv']
out = {}
for name in sorted(tiers):
    R = tiers[name]; days = [x['day'] for x in R]
    print(f"\n=== {name}: n {len(R)}, days {len(set(days))}")
    res = {}
    for o in ('R1', 'R2', 'R3'):
        print(f"  {o} mean: {summ([x[o] for x in R], days)}")
        for i in IND:
            sub = [x for x in R if x[i] is not None]
            sp = spearman([x[i] for x in sub], [x[o] for x in sub], [x['day'] for x in sub])
            res[(o, i)] = sp; print(f"    {o} ~ {i}: {sp}")
        sub = [x for x in R if x['rvol'] is not None]
        if len(sub) >= 16:
            med = st.median(x['rvol'] for x in sub)
            for lab, part in (('high rvol', [x for x in sub if x['rvol'] >= med]), ('low rvol', [x for x in sub if x['rvol'] < med])):
                print(f"    {o} ~ fh_ret, {lab}: {spearman([x['fh_ret'] for x in part], [x[o] for x in part], [x['day'] for x in part])}")
    # trend buckets
    for lo, hi, lab in ((-4, -2, 'trend<=-2'), (-1, 1, '-1..+1'), (2, 4, 'trend>=+2')):
        part = [x for x in R if lo <= x['trend'] <= hi]
        print(f"  {lab}: n {len(part)}  R1 {summ([x['R1'] for x in part])}  R3 {summ([x['R3'] for x in part])}")
    a = [(-x['R1'] if x['trend'] <= -2 else 0) for x in R]
    bb = [(x['R3'] if x['trend'] >= 2 else 0) for x in R]
    print(f"  Rule A (exit 10:30 if trend<=-2) vs hold to 13:00, per call: {summ(a, days)}")
    print(f"  Rule B (hold to close if trend>=+2) vs exit 13:00, per call: {summ(bb, days)}")
    json.dump(R, open(f"rows_{name.split()[0]}_{name.split()[-1].replace('%','').replace(',','')}.json", 'w'))
