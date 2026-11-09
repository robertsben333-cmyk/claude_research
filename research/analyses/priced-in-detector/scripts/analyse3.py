"""Version 3 (PREREG-v3.md): targets (B), options (C), combined. Usage: analyse3.py ev.json cache tq opt main_repo"""
import json, sys, os, math, bisect, glob, statistics as st, collections
import numpy as np
sys.path.insert(0, '/mnt/project-files/exit-model/scripts')
from lib import summ
EV, C, TQ, OPT, MAIN = sys.argv[1:6]
E = json.load(open(EV)); DEV = lambda d: d <= '2026-10-20'
def rk(a): return np.argsort(np.argsort(np.array(a), kind='mergesort'), kind='mergesort').astype(float)
def rho(x, y): return float(np.corrcoef(rk(x), rk(y))[0, 1]) if len(x) >= 8 else None
def perm_p(x, y, days, n=2000, seed=1):
    rx, ry = rk(x), rk(y); r0 = np.corrcoef(rx, ry)[0, 1]; rng = np.random.default_rng(seed)
    g = collections.defaultdict(list)
    for i, d in enumerate(days): g[d].append(i)
    g = [np.array(v) for v in g.values()]; ge = 0
    for _ in range(n):
        yy = ry.copy()
        for v in g: yy[v] = ry[rng.permutation(v)]
        ge += abs(np.corrcoef(rx, yy)[0, 1]) >= abs(r0) - 1e-12
    return round((ge + 1) / (n + 1), 4)
def partial(x, y, z):
    a, b, c = rk(x), rk(y), rk(z)
    def res(u, v): k = np.polyfit(v, u, 1); return u - np.polyval(k, v)
    return float(np.corrcoef(res(a, c), res(b, c))[0, 1])
TQD = {f[:-5]: json.load(open(f'{TQ}/{f}')) for f in os.listdir(TQ)}
OPD = {f[:-5]: json.load(open(f'{OPT}/{f}')) for f in os.listdir(OPT)}
# panel expected moves, keyed (run_day, ticker)
EXP = {}
for f in glob.glob(f'{MAIN}/research/2026/*/*/edge-panel/edge-scores-panel.json'):
    d = f.split('/')[-3]
    for r in json.load(open(f)).get('ranking') or []:
        if r.get('expected_move_pct') is not None: EXP[(d, r['ticker'])] = r['expected_move_pct']
# stage M rows keyed (ticker, date)
SM = {}
for f in glob.glob(f'{MAIN}/research/2026/*/*/morning/morning-resolved.json'):
    for r in json.load(open(f)).get('rows') or []:
        if r.get('release_read_move_pct') is not None and r.get('premarket_ref_pct') is not None:
            SM[(r['ticker'], f.split('/')[-3])] = r
def straddle(oc, day, T, S, exp):
    by = collections.defaultdict(dict)
    for c in oc:
        if c['x'] != exp: continue
        b = [z for z in c['b'] if z[0] == day and T - 120 <= z[1] <= T]
        if b: by[c['k']][c['t']] = b[-1][2]
    ks = sorted((k for k in by if 'C' in by[k] and 'P' in by[k]), key=lambda k: abs(k - S))
    if not ks or abs(ks[0] / S - 1) > 0.05: return None
    return by[ks[0]]['C'] + by[ks[0]]['P']
rows = []
for e in E:
    rd = e.get('react_day')
    if not rd or rd not in TQD: continue
    key = f"{e['ticker']}_{e['event_date']}"; p = f'{C}/{key}.json'
    if not os.path.exists(p): continue
    d = json.load(open(p)); q = d['q15']; prev = d['prev']
    pc = [x for x in q if x[0] == prev and x[1] == 945]
    if not pc: continue
    P0 = pc[-1][2]; cl = {x[0]: x[2] for x in q if x[1] == 945}; ds = sorted(cl)
    if len(ds) < 15: continue
    sig = st.stdev([math.log(cl[ds[k]] / cl[ds[k - 1]]) * 100 for k in range(1, len(ds))])
    B = sorted((b[1], b[2], b[5]) for b in d['m1'] if b[0] == rd); T = [b[0] for b in B]
    def px(t, stale=30):
        i = bisect.bisect_left(T, t) - 1
        return B[i][2] if i >= 0 and t - T[i] <= stale else None
    ob = [b for b in B if 570 <= b[0] <= 574]; popen = ob[0][1] if ob else None
    p925, p945, p1255, p13, pcl = px(565), px(585), px(775), px(780), px(955)
    if None in (popen, p13, pcl) or not sig: continue
    tq = TQD[rd].get(e['ticker'].replace('-', '.'), {})
    oc = OPD.get(rd, {}).get(key, [])
    exps = sorted({c['x'] for c in oc if any(z[0] == rd for z in c['b'])})
    exp = exps[0] if exps else None
    spre = straddle(oc, prev, 945, P0, exp) if exp else None
    for dm, pdec, ex0, ex1, tqk, optT in (('0925', p925, popen, p13, ('dec0925', 'ref0800'), None),
                                         ('0945', p945, p945, p13, ('dec0925', 'ref0800'), 570),
                                         ('1255', p1255, p13, pcl, ('dec1255', 'ref0950'), 750)):
        if dm == '1255' and e['session'] != 'bmo': continue
        if pdec is None: continue
        dec, ref = tq.get(tqk[0]), tq.get(tqk[1])
        M = (pdec / P0 - 1) * 100; dd = 1 if M >= 0 else -1
        r = dict(tk=e['ticker'], sess=e['session'], dm=dm, set=f"{e['session']}@{dm}", day=rd, M=M, d=dd, sig=sig,
                 F=dd * (ex1 - ex0) / P0 * 100, Msz=abs(M) / sig, P0=P0, popen=popen, pdec=pdec, ex0=ex0, ex1=ex1, calls=e['calls'],
                 B3=abs(M) / e['implied'] if e.get('implied') else None,
                 OI=dd * (dec['buy'] - dec['sell']) / dec['vol'] if dec and dec.get('vol') else None,
                 decay=dec['spread'] / ref['spread'] if dec and ref and dec.get('spread') and ref.get('spread') else None,
                 remain=None, crush=None, C2=None, sm=SM.get((e['ticker'], rd)))
        r['size'] = abs(r['F']) / sig
        if optT is not None and exp:
            s1 = straddle(oc, rd, optT + 15, pdec, exp)
            if s1: r['remain'] = s1 / pdec * 100; r['crush'] = s1 / spre if spre else None
            cv = sum(z[3] for c in oc if c['x'] == exp and c['t'] == 'C' for z in c['b'] if z[0] == rd and z[1] == optT)
            pv = sum(z[3] for c in oc if c['x'] == exp and c['t'] == 'P' for z in c['b'] if z[0] == rd and z[1] == optT)
            if cv + pv >= 20: r['C2'] = dd * (cv - pv) / (cv + pv)
        rows.append(r)
print('rows', len(rows), collections.Counter(r['set'] for r in rows))
print('with remaining straddle', sum(r['remain'] is not None for r in rows), 'C2', sum(r['C2'] is not None for r in rows))
MW = [r for r in rows if abs(r['M']) >= 2]
def test(lab, S, x, y, pp=True, part=False):
    S = [r for r in S if r.get(x) is not None and r.get(y) is not None]
    if len(S) < 10: print(f'   {lab}: n {len(S)}'); return None
    X = [r[x] for r in S]; Y = [r[y] for r in S]; rr = rho(X, Y)
    p = perm_p(X, Y, [r['day'] for r in S]) if pp else None
    ex = f" | partial|Msz {partial(X, Y, [r['Msz'] for r in S]):+.3f}" if part else ''
    print(f"   {lab}: n {len(S)} days {len({r['day'] for r in S})} rho({x},{y}) {rr:+.3f} p {p}{ex}"); return rr
SG = {}
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    S = [r for r in MW if f(r['day'])]; So = [r for r in S if r['dm'] in ('0945', '1255')]
    print(f'\n== {per} ==')
    print(' C1 size: remaining straddle % vs remaining |move|/sigma (09:45 and 12:55 rows)')
    test('pooled', So, 'remain', 'size', part=True)
    for s in ('amc@0945', 'bmo@0945', 'bmo@1255'): test(s, [r for r in So if r['set'] == s], 'remain', 'size', pp=False, part=True)
    test('[expl] crush ratio', So, 'crush', 'size', pp=False, part=True)
    print(' C2 direction: call-put volume imbalance vs F')
    rr = test('pooled', So, 'C2', 'F')
    if per == 'DEV': SG['C2'] = 1 if (rr or 0) > 0 else -1
    for s in ('amc@0945', 'bmo@0945', 'bmo@1255'): test(s, [r for r in So if r['set'] == s], 'C2', 'F', pp=False)
    print(' B3 market: |move| / implied vs F (sign predicted negative)')
    test('pooled all sets', S, 'B3', 'F')
    for s in ('amc@0925', 'bmo@0925', 'amc@0945', 'bmo@0945', 'bmo@1255'): test(s, [r for r in S if r['set'] == s], 'B3', 'F', pp=False)
    rr = test('[for sign] OI 09:45/12:55 rows', So, 'OI', 'F', pp=False)
    if per == 'DEV': SG['OI'] = 1 if (rr or 0) > 0 else -1
# z from dev
dev = [r for r in MW if DEV(r['day'])]
def zf(x):
    v = [r[x] for r in dev if r.get(x) is not None]; m, s = st.mean(v), st.pstdev(v)
    return lambda r: 0.0 if r.get(x) is None else max(-3, min(3, (r[x] - m) / s))
zC2, zOI, zB3, zdec, zrem, zM = (zf(x) for x in ('C2', 'OI', 'B3', 'decay', 'remain', 'Msz'))
for r in rows:
    r['dirs'] = SG['C2'] * zC2(r) + SG['OI'] * zOI(r) - zB3(r)
    r['sizes'] = zdec(r) + zrem(r) + zM(r)
print('\n== Combined (signs from dev:', SG, ') ==')
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    S = [r for r in MW if f(r['day']) and r['dm'] in ('0945', '1255')]
    print(f' -- {per}')
    test('direction score vs F', S, 'dirs', 'F')
    for s in ('amc@0945', 'bmo@0945', 'bmo@1255'): test(s, [r for r in S if r['set'] == s], 'dirs', 'F', pp=False)
    test('size score vs |F|/sigma', S, 'sizes', 'size')
    test('[ref] Msz alone vs |F|/sigma', S, 'Msz', 'size', pp=False)
def gain(r, side):
    fav = r['dirs'] * side * r['d'] > 0
    if r['set'] == 'amc@0945': ex = r['ex1'] if fav else r['pdec']; return side * (ex - r['popen']) / r['P0'] * 100
    if r['set'] == 'bmo@0945': return side * (r['pdec'] - r['ex1']) / r['P0'] * 100 if not fav else 0.0
    return side * (r['ex1'] - r['ex0']) / r['P0'] * 100 if fav else 0.0
print('\n== Combined exit rule vs static (amc open, bmo 13:00) ==')
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    print(f' -- {per}')
    for s in ('amc@0945', 'bmo@0945', 'bmo@1255'):
        S = [r for r in MW if f(r['day']) and r['set'] == s]
        print(f'   market {s}:', summ([(gain(r, 1) + gain(r, -1)) / 2 for r in S], [r['day'] for r in S]))
    for ver in ('us-panel.v2', 'us-panel.v3', 'backtest'):
        for strong in (False, True):
            for s in ('amc@0945', 'bmo@0945', 'bmo@1255'):
                g, dd = [], []
                for r in rows:
                    if not f(r['day']) or r['set'] != s: continue
                    for c in r['calls']:
                        if c['ver'] == ver and (c['strong'] or not strong): g.append(gain(r, c['side'])); dd.append(r['day'])
                if len(g) >= 5: print(f"   calls {ver}{' strong' if strong else ''} {s}:", summ(g, dd))
# B1: our calls, progress vs panel expected move
print('\n== B1 our calls: progress = move so far / panel expected move (sign predicted negative) ==')
for ver in ('us-panel.v2', 'us-panel.v3'):
    for s in ('amc@0925', 'bmo@0925', 'amc@0945', 'bmo@0945', 'bmo@1255', 'all'):
        X, Y, D = [], [], []
        for r in rows:
            if s != 'all' and r['set'] != s: continue
            if s == 'all' and r['dm'] == '0945': continue
            for c in r['calls']:
                em = EXP.get((c['run_day'], r['tk']))
                if c['ver'] != ver or not em: continue
                X.append(r['M'] / em); Y.append(c['side'] * (r['ex1'] - r['ex0']) / r['P0'] * 100); D.append(r['day'])
        if len(X) >= 10:
            rr = rho(X, Y); p = perm_p(X, Y, D) if s == 'all' else None
            hi = [y for x, y in zip(X, Y) if x >= 1]; lo = [y for x, y in zip(X, Y) if x < 1]
            print(f"  {ver} {s}: n {len(X)} rho {rr:+.3f} p {p} | progress>=1: {summ(hi)} | <1: {summ(lo)}")
print('\n== B2 stage M: side x (release read - pre-market) vs our-side open->13:00 (sign fixed negative) ==')
X, Y, D = [], [], []
for r in rows:
    if r['dm'] != '0925' or not r['sm']: continue
    sm = r['sm']; side = 1 if sm['position'] == 'long' else -1
    X.append(side * (sm['release_read_move_pct'] - sm['premarket_ref_pct'])); Y.append(side * (r['p13' if False else 'ex1'] - r['popen']) / r['P0'] * 100); D.append(r['day'])
if len(X) >= 10:
    print(f'  all mornings: n {len(X)} days {len(set(D))} rho {rho(X, Y):+.3f} p {perm_p(X, Y, D)}')
    nw = [(x, y) for x, y, d in zip(X, Y, D) if d > '2026-11-06']
    print('  after 6 Nov: n', len(nw))
