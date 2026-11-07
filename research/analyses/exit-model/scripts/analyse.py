"""Pre-registered analysis (PREREG.md). Usage: analyse.py rows.json > results.txt"""
import json, sys, math, random, statistics as st, collections
import numpy as np
from lib import rank, pearson, tt, p_from_t
R = json.load(open(sys.argv[1]))
CUT = '2026-10-20'
F = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
SIGN = dict(F1=-1, F2=1, F3=-1, F4=1, F5=-1, F6=-1, F7=1, F8=1, F9=1, F10=-1)
for r in R: r['train'] = r['day'] <= CUT
mk = [r for r in R if abs(r['gap']) >= 2]
tr = [r for r in mk if r['train']]; ho = [r for r in mk if not r['train']]
def spear(x, y, d, nperm=5000, seed=7, one_sided=True):
    P = [(a, b, c) for a, b, c in zip(x, y, d) if a is not None and b is not None]
    if len(P) < 8: return dict(n=len(P))
    x = [p[0] for p in P]; y = [p[1] for p in P]; d = [p[2] for p in P]
    rx, ry = rank(x), rank(y); rho = pearson(rx, ry)
    idx = collections.defaultdict(list)
    for i, dd in enumerate(d): idx[dd].append(i)
    rnd = random.Random(seed); ge = 0
    for _ in range(nperm):
        yy = ry[:]
        for ii in idx.values():
            v = [ry[i] for i in ii]; rnd.shuffle(v)
            for i, val in zip(ii, v): yy[i] = val
        q = pearson(rx, yy)
        ge += (q >= rho - 1e-12) if one_sided else (abs(q) >= abs(rho) - 1e-12)
    return dict(n=len(P), days=len(idx), rho=round(rho, 3), p=round((ge + 1) / (nperm + 1), 4))
# standardisation on training market sample
mu, sd = {}, {}
for k in F:
    v = [r[k] for r in tr if r[k] is not None]
    mu[k], sd[k] = st.mean(v), st.pstdev(v) or 1
def z(r, k):
    if r.get(k) is None: return 0.0
    return max(-3, min(3, (r[k] - mu[k]) / sd[k]))
for r in R:
    r['z'] = {k: z(r, k) for k in F}
    r['MA'] = sum(SIGN[k] * r['z'][k] for k in F)
# M-B: constrained OLS on training
def ols(keys):
    X = np.array([[1] + [r['z'][k] for k in keys] for r in tr]); y = np.array([r['Y1'] for r in tr])
    b, *_ = np.linalg.lstsq(X, y, rcond=None); return b
keys = F[:]; b = ols(keys)
dropped = [k for k, c in zip(keys, b[1:]) if c * SIGN[k] < 0]
keys = [k for k in keys if k not in dropped]; b = ols(keys)
for r in R: r['MB'] = float(b[0] + sum(c * r['z'][k] for k, c in zip(keys, b[1:])))
print('# Exit model, pre-registered analysis\n')
print(f'market sample |gap|>=2: train {len(tr)} events / {len(set(r["day"] for r in tr))} days, holdout {len(ho)} / {len(set(r["day"] for r in ho))} days')
print('M-B dropped (wrong sign in training):', dropped)
print('M-B coefficients:', {k: round(c, 3) for k, c in zip(['const'] + keys, b)})
print('\n## Test 1: market-wide, holdout (primary = M-A vs Y1)')
for m in ('MA', 'MB'):
    for Y in ('Y1', 'Y2', 'Y3'):
        for lab, S in (('train', tr), ('holdout', ho)):
            s = spear([r[m] for r in S], [r[Y] for r in S], [r['day'] for r in S])
            print(f'{m} {Y} {lab}: {s}')
    for sess in ('amc', 'bmo'):
        S = [r for r in ho if r['session'] == sess]
        print(f'  {m} Y1 holdout {sess}: {spear([r[m] for r in S], [r["Y1"] for r in S], [r["day"] for r in S])}')
# Y0: amc, pre-open composite (F6 not known; gap-dependent factors re-signed on the pre-market gap)
def ma_pre(r):
    if r.get('gp') is None: return None
    flip = r['gp'] * r['g']      # +1 if pm gap and open gap agree
    zz = dict(r['z']); zz['F6'] = 0
    zz['F5'] = z(dict(F5=r['F5'] * flip), 'F5') if r['F5'] is not None else 0
    zz['F7'] = z(dict(F7=r['F7'] * flip), 'F7') if r['F7'] is not None else 0
    zz['F8'] = z(dict(F8=1 if r['gp'] < 0 else 0), 'F8')
    if r.get('implied') and r.get('pmgap') is not None: zz['F1'] = z(dict(F1=abs(r['pmgap']) / r['implied']), 'F1')
    return sum(SIGN[k] * zz[k] for k in F)
a0 = [r for r in R if r['session'] == 'amc' and r.get('Y0') is not None and r.get('pmgap') is not None and abs(r['pmgap']) >= 2]
for lab, S in (('train', [r for r in a0 if r['train']]), ('holdout', [r for r in a0 if not r['train']])):
    print(f'MA-pre Y0 (amc pm->open) {lab}: {spear([ma_pre(r) for r in S], [r["Y0"] for r in S], [r["day"] for r in S])}')
print('\n## Per factor (signed by theory, so + means the theory holds), Y1')
for k in F:
    out = []
    for lab, S in (('train', tr), ('holdout', ho)):
        s = spear([SIGN[k] * r[k] if r[k] is not None else None for r in S], [r['Y1'] for r in S], [r['day'] for r in S], nperm=2000, one_sided=False)
        out.append(f"{lab} rho {s.get('rho')} p {s.get('p')} n {s['n']}")
    print(k, SIGN[k], ' | '.join(out))
# Test 2: rule on our calls
thr = sorted(abs(r['MA']) for r in tr)[int(0.67 * len(tr))]
print(f'\n## Test 2: rule on our calls (|M-A| > {thr:.2f}, the training 67th percentile)')
def calls(S, ver, strong=None):
    out = []
    for r in S:
        seen = set()
        for c in r['calls']:
            if c['ver'] != ver or c['ver'] in seen: continue
            if strong is not None and c['strong'] != strong: continue
            seen.add(c['ver']); out.append((r, c))
    return out
def gain(r, side, pred):
    a = side * r['g']
    if abs(pred) <= thr: return 0.0, False
    if r['session'] == 'amc':
        return (a * r['Y1'], True) if a * pred > 0 else (0.0, False)
    return (-a * r['Y1'], True) if a * pred < 0 else (0.0, False)
def summ(v, days):
    by = collections.defaultdict(list)
    for x, d in zip(v, days): by[d].append(x)
    dm = [st.mean(x) for x in by.values()]
    t = tt(v); td = tt(dm)
    return f"n {len(v)} mean {st.mean(v):+.2f} t {t if t is None else round(t,2)} p {None if t is None else round(p_from_t(t,len(v)),3)} | days {len(dm)} t_days {None if td is None else round(td,2)} pos_days {sum(x>0 for x in dm)}"
for ver, period in (('us-panel.v2', 'holdout'), ('us-panel.v3', 'holdout'), ('us-panel.v2', 'train'), ('backtest', 'train')):
    S = ho if period == 'holdout' else tr
    S = [r for r in R if (not r['train']) == (period == 'holdout')]   # all gaps, not only >=2%
    for st_ in (None, True):
        C = calls(S, ver, st_)
        if not C: continue
        G = [gain(r, c['side'], r['MA']) for r, c in C]
        acted = [g for g, a in G if a]
        lab = f"{ver} {'strong' if st_ else 'all'} ({period})"
        print(f"{lab}: {summ([g for g, _ in G], [r['day'] for r, _ in C])}; acted on {len(acted)}" + (f", mean when acted {st.mean(acted):+.2f}" if acted else ''))
        for sess in ('amc', 'bmo'):
            CC = [(r, c) for r, c in C if r['session'] == sess]
            if len(CC) >= 3:
                GG = [gain(r, c['side'], r['MA'])[0] for r, c in CC]
                print(f"    {sess}: {summ(GG, [r['day'] for r, _ in CC])}")
        # does M-A rank the position's gain from holding to 13:00?
        x = [r['MA'] * c['side'] * r['g'] for r, c in C]; y = [c['side'] * r['g'] * r['Y1'] for r, c in C]
        print(f"    rank: a*M-A vs a*Y1 {spear(x, y, [r['day'] for r, _ in C], nperm=2000)}")
# Test 3: stage M
print('\n## Test 3: stage M add-on (analyst prompt v2, reviews from 21 Oct)')
M = [r for r in R if r.get('m') and r['m']['day'] >= '2026-10-21' and r['m']['action'] != 'none' and r['m'].get('side')]
def sig(r):
    m = r['m']; s = m['side']; a = s * r['g']
    S1 = s * m['exp_oc'] if m['exp_oc'] is not None else None
    S2 = -a * (m['p_fade'] - 50) if m['p_fade'] is not None else None
    S3 = s * (m['read'] - m['pmref_pct']) if (m['read'] is not None and m['pmref_pct'] is not None) else None
    S4 = (s * (m['verdict'] or 0) / 100) + s * m['guid'] + a * m['tape']
    return [S1, S2, S3, S4]
sigs = [sig(r) for r in M]
cols = list(zip(*sigs))
zs = []
for col in cols:
    v = [x for x in col if x is not None]; m_, s_ = st.mean(v), st.pstdev(v) or 1
    zs.append([0 if x is None else (x - m_) / s_ for x in col])
Sc = [sum(z_[i] for z_ in zs) / 4 for i in range(len(M))]
yh = [r['m']['side'] * r['g'] * r['Y1'] for r in M]        # position gain open -> 13:00
yc = [r['m']['side'] * (r['x1300_to_close']) for r in M]    # position gain 13:00 -> close
dd = [r['day'] for r in M]
print(f'n {len(M)} names, {len(set(dd))} mornings')
for nm, col in zip(['S1', 'S2', 'S3', 'S4'], zs):
    print(nm, 'vs open->13:00', spear(col, yh, dd, nperm=2000), '| vs 13:00->close', spear(col, yc, dd, nperm=2000))
print('S composite vs open->13:00', spear(Sc, yh, dd), '| vs 13:00->close', spear(Sc, yc, dd))
for sess in ('amc', 'bmo'):
    ii = [i for i, r in enumerate(M) if r['session'] == sess]
    print(f'  {sess}: S vs open->13:00', spear([Sc[i] for i in ii], [yh[i] for i in ii], [dd[i] for i in ii], nperm=2000))
xa = [r['MA'] * r['m']['side'] * r['g'] for r in M]
print('M-A (position-signed) on the same names vs open->13:00', spear(xa, yh, dd))
comb = [a / (st.pstdev(xa) or 1) + b for a, b in zip(xa, Sc)]
print('M-A + S vs open->13:00', spear(comb, yh, dd))
json.dump([dict(ticker=r['ticker'], day=r['day'], session=r['session'], gap=r['gap'], MA=round(r['MA'], 3), MB=round(r['MB'], 4),
                Y0=r.get('Y0'), Y1=r['Y1'], Y2=r['Y2'], Y3=r['Y3'], train=r['train'],
                calls=[(c['ver'], c['side'], c['strong']) for c in r['calls']]) for r in R], open('scored.json', 'w'))
