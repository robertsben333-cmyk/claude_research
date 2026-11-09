"""Version 2 tests (PREREG-v2.md). Usage: analyse2.py ev.json cache tq_dir"""
import json, sys, os, math, bisect, statistics as st, collections
import numpy as np
sys.path.insert(0, '/mnt/project-files/exit-model/scripts')
from lib import summ
EV, C, TQ = sys.argv[1:4]
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
def partial(x, y, z):  # rank partial correlation
    a, b, c = rk(x), rk(y), rk(z)
    def res(u, v): k = np.polyfit(v, u, 1); return u - np.polyval(k, v)
    return float(np.corrcoef(res(a, c), res(b, c))[0, 1])
TQD = {}
for f in os.listdir(TQ): TQD[f[:-5]] = json.load(open(f'{TQ}/{f}'))
rows = []
for e in E:
    rd = e.get('react_day')
    if not rd or rd not in TQD: continue
    p = f"{C}/{e['ticker']}_{e['event_date']}.json"
    if not os.path.exists(p): continue
    d = json.load(open(p)); q = d['q15']; prev = d['prev']
    pc = [x for x in q if x[0] == prev and x[1] == 945]
    if not pc: continue
    P0 = pc[-1][2]
    cl = {x[0]: x[2] for x in q if x[1] == 945}; ds = sorted(cl)
    if len(ds) < 15: continue
    lr = [math.log(cl[ds[k]] / cl[ds[k - 1]]) * 100 for k in range(1, len(ds))]
    sig = st.stdev(lr)
    dv = collections.defaultdict(float)
    for x in q: dv[x[0]] += x[2] * x[3]
    adv = st.mean(dv.values())
    B = sorted((b[1], b[2], b[5]) for b in d['m1'] if b[0] == rd)
    T = [b[0] for b in B]
    def px(t, stale=30):
        i = bisect.bisect_left(T, t) - 1
        return B[i][2] if i >= 0 and t - T[i] <= stale else None
    ob = [b for b in B if 570 <= b[0] <= 574]
    popen = ob[0][1] if ob else None
    p925, p1255, p13, pcl = px(565), px(775), px(780), px(955)
    if None in (popen, p13, pcl) or not sig: continue
    tq = TQD[rd].get(e['ticker'].replace('-', '.'), {})
    for dm, pdec, ex0, ex1, keys in (('0925', p925, popen, p13, ('dec0925', 'ref0800', 'nrm0925')),
                                    ('1255', p1255, p13, pcl, ('dec1255', 'ref0950', 'nrm1255'))):
        if dm == '1255' and e['session'] != 'bmo': continue
        if pdec is None: continue
        dec, ref, nrm = (tq.get(k) for k in keys)
        if not dec or not dec.get('spread'): continue
        M = (pdec / P0 - 1) * 100; dd = 1 if M >= 0 else -1
        F = dd * (ex1 - ex0) / P0 * 100
        r = dict(tk=e['ticker'], sess=e['session'], dm=dm, set=f"{e['session']}@{dm}", day=rd, M=M, d=dd, sig=sig, adv=adv,
                 F=F, size=abs(F) / sig, Msz=abs(M) / sig, ex0=ex0, ex1=ex1, P0=P0, calls=e['calls'],
                 abn=dec['spread'] / nrm['spread'] if nrm and nrm.get('spread') else None,
                 decay=dec['spread'] / ref['spread'] if ref and ref.get('spread') else None,
                 OI=dd * (dec['buy'] - dec['sell']) / dec['vol'] if dec['vol'] else None,
                 RI=dd * (dec['rbuy'] - dec['rsell']) / (dec['rbuy'] + dec['rsell']) if dec['rbuy'] + dec['rsell'] > 0 else None)
        rows.append(r)
print('rows', len(rows), collections.Counter(r['set'] for r in rows))
MW = [r for r in rows if abs(r['M']) >= 2]
medadv = st.median(r['adv'] for r in MW)
def test(lab, S, x, y, pp=True, part=None):
    S = [r for r in S if r[x] is not None and r[y] is not None]
    if len(S) < 10: return print(f'   {lab}: n {len(S)}')
    X = [r[x] for r in S]; Y = [r[y] for r in S]; rr = rho(X, Y)
    p = perm_p(X, Y, [r['day'] for r in S]) if pp else None
    extra = f" | partial|Msz {partial(X, Y, [r['Msz'] for r in S]):+.3f}" if part else ''
    print(f"   {lab}: n {len(S)} days {len({r['day'] for r in S})} rho({x},{y}) {rr:+.3f} p {p}{extra}")
    return rr
sgn = {}
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    S = [r for r in MW if f(r['day'])]
    print(f'\n== {per} (|move| >= 2%: {len(S)} rows) ==')
    print(' HA size: abnormal spread vs |F|/sigma')
    test('pooled', S, 'abn', 'size', part=True)
    for s in ('amc@0925', 'bmo@0925', 'bmo@1255'): test(s, [r for r in S if r['set'] == s], 'abn', 'size', pp=False, part=True)
    print(' [exploratory] size: spread decay, move so far')
    test('decay pooled', S, 'decay', 'size', pp=False, part=True)
    test('Msz pooled', S, 'Msz', 'size', pp=False)
    print(' HB direction')
    for x in ('OI', 'RI'):
        rr = test(f'{x} pooled', S, x, 'F')
        if per == 'DEV': sgn[x] = 1 if rr > 0 else -1
        for s in ('amc@0925', 'bmo@0925', 'bmo@1255'): test(f'{x} {s}', [r for r in S if r['set'] == s], x, 'F', pp=False)
    print(' [exploratory] direction by liquidity (above/below median $vol)')
    for x in ('OI', 'RI'):
        test(f'{x} liquid', [r for r in S if r['adv'] >= medadv], x, 'F', pp=False)
        test(f'{x} illiquid', [r for r in S if r['adv'] < medadv], x, 'F', pp=False)
    print(' [exploratory] mean F by set:', {s: summ([r['F'] for r in S if r['set'] == s], [r['day'] for r in S if r['set'] == s]) for s in ('amc@0925', 'bmo@0925', 'bmo@1255')})
print('\n== HC exit rule (signals oriented by development sign:', sgn, ') ==')
def gain(r, side, x):
    v = r[x]
    if v is None: return 0.0
    fav = sgn[x] * v * side * r['d'] > 0      # signal favours our position
    if r['set'] == 'amc@0925':   # current: open (ex0); hold to 13:00 if favourable
        return side * (r['ex1'] - r['ex0']) / r['P0'] * 100 if fav else 0.0
    if r['set'] == 'bmo@0925':   # current: 13:00 (ex1); sell at open if against
        return side * (r['ex0'] - r['ex1']) / r['P0'] * 100 if not fav else 0.0
    return side * (r['ex1'] - r['ex0']) / r['P0'] * 100 if fav else 0.0   # bmo@1255: hold to close if favourable
for x in ('OI', 'RI'):
    for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
        print(f' -- {x} {per}')
        for s in ('amc@0925', 'bmo@0925', 'bmo@1255'):
            S = [r for r in MW if f(r['day']) and r['set'] == s and r[x] is not None]
            print(f'   market {s}:', summ([(gain(r, 1, x) + gain(r, -1, x)) / 2 for r in S], [r['day'] for r in S]))
        for ver in ('us-panel.v2', 'us-panel.v3', 'backtest'):
            for strong in (False, True):
                g, dd = [], []
                for r in rows:
                    if not f(r['day']): continue
                    for c in r['calls']:
                        if c['ver'] == ver and (c['strong'] or not strong): g.append(gain(r, c['side'], x)); dd.append(r['day'])
                if g: print(f"   calls {ver}{' strong' if strong else ''} (all sets):", summ(g, dd))
