"""Pre-registered tests H1-H3 plus labelled exploratory cuts. Usage: analyse.py rows.json"""
import json, sys, math, random, statistics as st, collections
import numpy as np
sys.path.insert(0, '/mnt/project-files/exit-model/scripts')
from lib import summ, tt, p_from_t
R = json.load(open(sys.argv[1]))
DEV = lambda d: d <= '2026-10-20'
SET = float(sys.argv[2]) if len(sys.argv) > 2 else 0.30
def rk(a): return np.argsort(np.argsort(a, kind='mergesort'), kind='mergesort').astype(float)
def rho(x, y):
    if len(x) < 8: return None
    a, b = rk(np.array(x)), rk(np.array(y)); return float(np.corrcoef(a, b)[0, 1])
def perm_p(x, y, days, n=2000, seed=1):
    x, y = np.array(x), rk(np.array(y)); rx = rk(x); r0 = np.corrcoef(rx, y)[0, 1]
    rng = np.random.default_rng(seed); groups = collections.defaultdict(list)
    for i, d in enumerate(days): groups[d].append(i)
    groups = [np.array(g) for g in groups.values()]; ge = 0
    for _ in range(n):
        yy = y.copy()
        for g in groups: yy[g] = y[rng.permutation(g)]
        if abs(np.corrcoef(rx, yy)[0, 1]) >= abs(r0) - 1e-12: ge += 1
    return round((ge + 1) / (n + 1), 4)
# observation table
O = []
for r in R:
    for o in r['obs']:
        if o['F13'] is None or abs(o['M']) < 2 or o['TR'] is None or o['VW'] is None or o['DEC'] is None: continue
        O.append(dict(o, day=r['day'], s=r['session'], tk=r['ticker']))
dev = [o for o in O if DEV(o['day'])]
def wz(v, m, s): return max(-3, min(3, (v - m) / s))
mTR, sTR = st.mean(o['TR'] for o in dev), st.pstdev(o['TR'] for o in dev)
mVW, sVW = st.mean(o['VW'] for o in dev), st.pstdev(o['VW'] for o in dev)
def Dsig(o): return wz(o['TR'], mTR, sTR) + wz(o['VW'], mVW, sVW)
for o in O: o['D'] = Dsig(o); o['set'] = o['DEC'] < SET
print(f'settle threshold {SET}; obs {len(O)} (dev {len(dev)}), events {len(R)}; z TR {mTR:.2f}/{sTR:.2f} VW {mVW:.2f}/{sVW:.2f}')
def block(lab, S, Y='F13', pp=True):
    if len(S) < 8: print(f'  {lab}: n {len(S)}'); return None
    x = [o['D'] for o in S]; y = [o[Y] for o in S]; r = rho(x, y)
    p = perm_p(x, y, [o['day'] for o in S]) if pp else None
    m = summ(y, [o['day'] for o in S])
    print(f"  {lab}: n {len(S)} days {m.get('days')} | rho(D,{Y}) {r:+.3f} p {p} | mean {Y} {m['mean']:+.2f} t {m['t']} t_days {m.get('t_days')}")
    return r
def boot_gap(S, reps=1000, seed=2):
    byd = collections.defaultdict(list)
    for o in S: byd[o['day']].append(o)
    ds = list(byd); rng = random.Random(seed); out = []
    for _ in range(reps):
        smp = [o for d in (rng.choice(ds) for _ in ds) for o in byd[d]]
        u = [o for o in smp if not o['set']]; s = [o for o in smp if o['set']]
        if len(u) < 8 or len(s) < 8: continue
        out.append(abs(rho([o['D'] for o in u], [o['F13'] for o in u])) - abs(rho([o['D'] for o in s], [o['F13'] for o in s])))
    out.sort(); return round(out[int(.025 * len(out))], 3), round(out[int(.975 * len(out))], 3)
res = {}
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    S = [o for o in O if f(o['day'])]
    print(f'\n== {per} ==')
    print(' H1 unsettled:'); ru = block('all', [o for o in S if not o['set']])
    print(' H2 settled:'); rs = block('all', [o for o in S if o['set']])
    print('  gap |rho_u|-|rho_s| day-bootstrap 95%:', boot_gap(S))
    res[per] = (ru, rs)
    for sess in ('amc', 'bmo'):
        print(f' [exploratory] {sess}:')
        block('unsettled', [o for o in S if not o['set'] and o['s'] == sess], pp=False)
        block('settled', [o for o in S if o['set'] and o['s'] == sess], pp=False)
    print(' [exploratory] F1 (to next checkpoint):')
    block('unsettled F1', [o for o in S if not o['set'] and o.get('F1') is not None], 'F1', pp=False)
    block('settled F1', [o for o in S if o['set'] and o.get('F1') is not None], 'F1', pp=False)
    print(' [exploratory] by checkpoint (unsettled+settled), rho(D,F13), share settled:')
    for t in sorted({o['t'] for o in S if o['t'] < 780}):
        ss = [o for o in S if o['t'] == t]
        if len(ss) < 20: continue
        r = rho([o['D'] for o in ss], [o['F13'] for o in ss])
        print(f"   t {t:5d} n {len(ss):4d} settled {sum(o['set'] for o in ss)/len(ss):.2f} rho {r:+.3f} meanF13 {st.mean(o['F13'] for o in ss):+.2f}")
# ---- H3 dynamic exit
s_h1 = 1 if (res['DEV'][0] or 0) > 0 else -1
print(f'\n== H3 dynamic exit (rule follows {"continuation" if s_h1 > 0 else "reversal"}) ==')
DEC_CP = {'amc': [565, 575, 585, 600, 630, 660, 720, 750, 780, 810, 840, 870, 900, 930], 'bmo': [600, 630, 660, 720, 750, 780, 810, 840, 870, 900, 930]}
def rule_gain(r, side):
    ob = {o['t']: o for o in r['obs']}
    static = r['open'] if r['session'] == 'amc' else r['p13']
    ex = r['pclose']; first = True
    for t in DEC_CP[r['session']]:
        o = ob.get(t)
        if o is None or o['TR'] is None or o['VW'] is None or o['DEC'] is None: continue
        D = Dsig(o); settled = o['DEC'] < SET
        if settled or o['d'] * D * side * s_h1 < 0:
            ex = r['open'] if t == 565 else o['P']; break
    return side * (ex - static) / r['P0'] * 100
def first_obs(r):
    t0 = DEC_CP[r['session']][0]; return next((o for o in r['obs'] if o['t'] == t0), None)
for per, f in (('DEV', DEV), ('HOLDOUT', lambda d: not DEV(d))):
    print(f'-- {per}')
    for sess in ('amc', 'bmo', 'all'):
        g, dd = [], []
        for r in R:
            if not f(r['day']) or (sess != 'all' and r['session'] != sess): continue
            o = first_obs(r)
            if not o or abs(o['M']) < 2: continue
            g.append((rule_gain(r, 1) + rule_gain(r, -1)) / 2); dd.append(r['day'])
        print(f'  market {sess}:', summ(g, dd))
    for ver in ('us-panel.v2', 'us-panel.v3', 'backtest'):
        for strong in (False, True):
            g, dd = [], []
            for r in R:
                if not f(r['day']): continue
                for c in r['calls']:
                    if c['ver'] != ver or (strong and not c['strong']): continue
                    g.append(rule_gain(r, c['side'])); dd.append(r['day'])
            if g: print(f"  calls {ver}{' strong' if strong else ''}:", summ(g, dd))
# ---- descriptive: share of the close-to-close move present at each checkpoint
print('\n== [exploratory] share of the reaction-day close move already present (|close move| >= 4%) ==')
for sess in ('amc', 'bmo'):
    rows = [r for r in R if r['session'] == sess and abs(r['close_move']) >= 4]
    line = []
    for t in (DEC_CP['amc'] if False else ([-450, -390, -300, 420, 510, 565] if sess == 'amc' else [420, 510, 565]) + [575, 600, 660, 780, 930]):
        sh = [o['M'] / r['close_move'] for r in rows for o in r['obs'] if o['t'] == t]
        if len(sh) >= 10:
            q = sorted(sh); line.append(f"{t}:{st.median(sh):.2f}[{q[len(q)//4]:.2f},{q[3*len(q)//4]:.2f}] n{len(sh)}")
    print(f' {sess} (n events {len(rows)}):', ' | '.join(line))
