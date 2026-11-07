"""EU panel study 2: distributions, cuts, entry/exit grid, costs, strategy with a
date-split out-of-sample check. Reads dataset.json, writes report.txt and results.json."""
import json, math, random, statistics as st
from collections import defaultdict
from pathlib import Path

S = Path(__file__).resolve().parent
D = json.loads((S / 'dataset.json').read_text())
STOXX = D['stoxx']
OUT = []
RES = {}


def P(*a):
    OUT.append(' '.join(str(x) for x in a))


def tstat(xs):
    n = len(xs)
    if n < 2:
        return None, None
    m = st.mean(xs); sd = st.stdev(xs)
    if sd == 0:
        return None, None
    t = m / (sd / math.sqrt(n))
    # two-sided p from t with n-1 df (normal approx for n>30, else Student via betainc)
    return t, pval_t(t, n - 1)


def pval_t(t, df):
    x = df / (df + t * t)
    return betainc(df / 2, 0.5, x)


def betainc(a, b, x):
    # regularized incomplete beta via continued fraction (Numerical Recipes)
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b + lbeta)
    def cf(a, b, x):
        f, c, d = 1.0, 1.0, 0.0
        for i in range(200):
            m = i // 2
            if i == 0: num = 1.0
            elif i % 2 == 0: num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
            else: num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
            d = 1 + num * d; d = 1 / d if abs(d) > 1e-30 else 1e30
            c = 1 + num / c if abs(c) > 1e-30 else 1e30
            f *= c * d
            if abs(1 - c * d) < 1e-10: break
        return f
    if x < (a + 1) / (a + b + 2):
        return front * (cf(a, b, x) - 1) / a
    return 1 - betainc(b, a, 1 - x)


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(x, y):
    if len(x) < 3: return None
    rx, ry = ranks(x), ranks(y)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def within_day_rho(rows, key, ret, iters=5000, seed=3):
    """n-weighted mean of per-day Spearman, permutation p shuffling within days."""
    by = defaultdict(list)
    for r in rows:
        by[r['day']].append(r)
    groups = [(g) for g in by.values() if len(g) >= 3]
    def stat(gs):
        tot = w = 0
        for g in gs:
            rho = spearman([key(r) for r in g], [ret(r) for r in g])
            if rho is not None:
                tot += rho * len(g); w += len(g)
        return tot / w if w else None
    obs = stat(groups)
    if obs is None: return None, None, 0
    rnd = random.Random(seed); hits = 0
    for _ in range(iters):
        sh = []
        for g in groups:
            ys = [ret(r) for r in g]; rnd.shuffle(ys)
            sh.append([dict(r, _y=y) for r, y in zip(g, ys)])
        tot = w = 0
        for g in sh:
            rho = spearman([key(r) for r in g], [r['_y'] for r in g])
            if rho is not None: tot += rho * len(g); w += len(g)
        if abs(tot / w) >= abs(obs) - 1e-12: hits += 1
    return obs, (hits + 1) / (iters + 1), sum(len(g) for g in groups)


def pct(a, b):
    return None if a is None or b is None or not b else (a / b - 1) * 100


def leg(r, e, x):
    px = r['px']; a, b = px.get(e), px.get(x)
    if a is None or b is None or not a: return None
    if e == 'open_R' and x == 'open_R': return None
    return r['sd'] * (b / a - 1) * 100


# ---- the sample -------------------------------------------------------------------
rows = []
drop = defaultdict(list)
for r in D['rows']:
    px = r.get('px') or {}
    if r.get('event_occurred') is False:
        drop['no event (resolver)'].append(r['day'] + ' ' + r['ticker']); continue
    if r.get('panel_pct') is None or not r.get('side'):
        drop['no panel side'].append(r['day'] + ' ' + r['ticker']); continue
    if 'close_R' not in px:
        drop['not priced/pending'].append(r['day'] + ' ' + r['ticker'] + ' ' + str(px)[:40]); continue
    r['pp'] = float(r['panel_pct']); r['sd'] = float(r['side'])
    r['mv'] = pct(px['close_R'], px['close_Rm1'])
    r['ret'] = r['sd'] * r['mv']
    # market move over the same window
    stx = STOXX.get(px['R']); prev = None
    ks = sorted(STOXX)
    if px['R'] in ks:
        i = ks.index(px['R']); prev = STOXX[ks[i - 1]] if i else None
    r['mkt'] = pct(stx, prev)
    r['ret_x'] = r['sd'] * (r['mv'] - r['mkt']) if r['mkt'] is not None else None
    r['cs'] = px.get('cs_spread_pct')
    uk_long = (r['submarket'] == 'uk' and r['sd'] > 0)
    r['cost'] = (r['cs'] if r['cs'] is not None else 1.0) + 0.10
    r['cost_uk_stamp'] = r['cost'] + (0.5 if uk_long else 0)
    rows.append(r)

P('SAMPLE')
P(f'  panel-scored live names: {len(D["rows"])}; usable: {len(rows)}; days: {len({r["day"] for r in rows})}')
for k, v in drop.items():
    P(f'  dropped {k}: {len(v)}  {v[:12]}')
P('  hunter versions:', sorted({tuple(r["hunter_versions"]) for r in rows}))
P('  sessions:', dict(sorted(defaultdict(int, {s: sum(1 for r in rows if r["session"] == s) for s in {r["session"] for r in rows}}).items())))
RES['n'] = len(rows)


def block(name, rs, f=lambda r: r['ret']):
    xs = [f(r) for r in rs if f(r) is not None]
    if not xs:
        return f'{name:34s} n   0'
    t, p = tstat(xs)
    hit = sum(1 for x in xs if x > 0) / len(xs)
    return (f'{name:34s} n {len(xs):3d}  mean {st.mean(xs):+6.2f}  med {st.median(xs):+6.2f}  '
            f'hit {hit:4.0%}  t {t if t is not None else float("nan"):+5.2f}  p {p if p is not None else float("nan"):.3f}')


def stats(rs, f=lambda r: r['ret']):
    xs = [f(r) for r in rs if f(r) is not None]
    t, p = tstat(xs) if len(xs) > 1 else (None, None)
    return {'n': len(xs), 'mean': round(st.mean(xs), 3) if xs else None,
            'hit': round(sum(1 for x in xs if x > 0) / len(xs), 3) if xs else None,
            't': round(t, 2) if t else None, 'p': round(p, 3) if p else None}


# ---- 1. ranking ------------------------------------------------------------------
P('\n1. RANKING, close(R-1) -> close(R)')
for lab, key in (('panel_pct_signed', lambda r: r['pp'] * r['sd']),
                 ('hunter impact_sum', lambda r: r['hunter_impact_sum'] or 0),
                 ('control -run_up_20d', lambda r: -(r['run_up_20d'] or 0)),
                 ('control -run_up_5d', lambda r: -(r['run_up_5d'] or 0))):
    rho, p, n = within_day_rho(rows, key, lambda r: r['mv'])
    P(f'  within-day rho {lab:22s} {rho:+.3f}  perm p {p:.3f}  n {n}')
    RES.setdefault('rank', {})[lab] = {'rho': round(rho, 3), 'p': round(p, 3), 'n': n}
for m in ('opus5', 'opus55', 'sonnet55', 'fable51'):
    rr = [r for r in rows if (r['members'].get(m) or {}).get('pct_signed') is not None]
    rho, p, n = within_day_rho(rr, lambda r: r['members'][m]['pct_signed'], lambda r: r['mv'], iters=2000)
    P(f'  within-day rho judge {m:10s} {rho:+.3f}  perm p {p:.3f}  n {n}')
rho = spearman([r['pp'] for r in rows], [r['ret'] for r in rows])
P(f'  pooled rho |panel_pct| vs signed return {rho:+.3f} (does a higher score mean a better-signed trade)')
rho2 = spearman([r['pp'] for r in rows], [abs(r['mv']) for r in rows])
P(f'  pooled rho |panel_pct| vs |move|        {rho2:+.3f} (does a higher score find bigger movers)')

def day_t(rs, f=lambda r: r['ret']):
    by = defaultdict(list)
    for r in rs:
        v = f(r)
        if v is not None: by[r['day']].append(v)
    m = [st.mean(v) for v in by.values()]
    t, p = tstat(m)
    return f'day-clustered: {len(m)} days, mean of day means {st.mean(m):+.2f}, t {t:+.2f}, p {p:.3f}, days positive {sum(1 for x in m if x > 0)}/{len(m)}'


P('\n2. SCORE BANDS (signed, gross)')
P('  ' + block('control: all long', rows, lambda r: r['mv']))
P('  ' + block('all names, panel side', rows))
bands = [(0, 30), (30, 50), (50, 60), (60, 70), (70, 80), (80, 101)]
for lo, hi in bands:
    rs = [r for r in rows if lo <= r['pp'] < hi]
    P('  ' + block(f'panel_pct {lo}-{hi}', rs) + f'  med|move| {st.median([abs(r["mv"]) for r in rs]) if rs else 0:.1f}')
    RES.setdefault('bands', {})[f'{lo}-{hi}'] = stats(rs)
for th in (50, 60, 70, 80):
    rs = [r for r in rows if r['pp'] >= th]
    P('  ' + block(f'>= {th}', rs))
    P('  ' + block(f'>= {th} vs STOXX', rs, lambda r: r['ret_x']))
    RES.setdefault('thresh', {})[th] = stats(rs)
for th in (0, 60, 70, 80):
    P(f'  >= {th} ' + day_t([r for r in rows if r['pp'] >= th]))
P('  distribution of panel_pct:', {f'{lo}-{hi}': sum(1 for r in rows if lo <= r['pp'] < hi) for lo, hi in bands})
P('  distribution of signed return >=70 (sorted):', [round(r['ret'], 1) for r in sorted([r for r in rows if r['pp'] >= 70], key=lambda r: r['ret'])])

# ---- 3. cuts -------------------------------------------------------------------
STRONG = [r for r in rows if r['pp'] >= 70]


def turn_band(r):
    t = r['turnover_usd'] or 0
    return '<$1m' if t < 1e6 else '$1-5m' if t < 5e6 else '$5-25m' if t < 25e6 else '>$25m'


def vol_band(r):
    v = r['vol20']
    return 'unknown' if v is None else '<25%' if v < 25 else '25-40%' if v < 40 else '>=40%'


def ana(r):
    a = r['analyst_count']
    return 'unknown' if a is None else '0-2' if a <= 2 else '3-7' if a <= 7 else '8+'


def week(r):
    return r['day'][:8] + ('1-15' if int(r['day'][8:]) <= 15 else '16-31') if False else (
        'A 10-12..10-23' if r['day'] <= '2026-10-23' else 'B 10-26..11-05')


CUTS = [('country', lambda r: r['submarket']),
        ('sector', lambda r: r['industry'] or '?'),
        ('side', lambda r: 'long' if r['sd'] > 0 else 'short'),
        ('session', lambda r: r['session']),
        ('turnover', turn_band),
        ('anchor (short register names it)', lambda r: str(bool(r['anchor_covered']))),
        ('analysts', ana),
        ('20d vol', vol_band),
        ('judges agree on sign', lambda r: f"{r['sign_agree']} of 4"),
        ('judge spread', lambda r: 'low (sd<12)' if (r['panel_pct_sd'] or 0) < 12 else 'high'),
        ('hunter agrees with panel side', lambda r: str((r['hunter_impact_sum'] or 0) * r['sd'] > 0)),
        ('day size', lambda r: '1-9' if day_n[r['day']] < 10 else '10-17' if day_n[r['day']] < 18 else '18+'),
        ('period', week)]
day_n = defaultdict(int)
for r in rows: day_n[r['day']] += 1
for title, rs in (('ALL NAMES', rows), ('STRONG >= 70', STRONG), ('>= 60', [r for r in rows if r['pp'] >= 60])):
    P(f'\n3. CUTS, {title} (signed, gross, close->close)')
    for cname, f in CUTS:
        groups = defaultdict(list)
        for r in rs: groups[f(r)].append(r)
        P(f'  -- {cname}')
        for g in sorted(groups, key=lambda g: -len(groups[g])):
            if len(groups[g]) < 2 and title == 'ALL NAMES': continue
            P('    ' + block(str(g)[:30], groups[g]))
            RES.setdefault('cuts', {}).setdefault(title, {}).setdefault(cname, {})[str(g)] = stats(groups[g])

# ---- 3b. the first study's leads, tested on the days it never saw ---------------
NEW = [r for r in rows if r['day'] >= '2026-10-21']
P(f'\n3b. LEADS FROM THE FIRST STUDY (written 2026-10-21 on event days 10-12..10-20), on the {len(NEW)} names of event days 10-21..11-05 only')
for nm, f in (('20d vol >= 40%', lambda r: (r['vol20'] or 0) >= 40), ('20d vol < 40%', lambda r: (r['vol20'] or 0) < 40),
              ('low judge spread (sd<12)', lambda r: (r['panel_pct_sd'] or 0) < 12), ('high judge spread', lambda r: (r['panel_pct_sd'] or 0) >= 12),
              ('4 of 4 agree', lambda r: r['sign_agree'] == 4), ('3 or fewer agree', lambda r: r['sign_agree'] != 4),
              ('anchor covered', lambda r: bool(r['anchor_covered'])), ('no anchor', lambda r: not r['anchor_covered']),
              ('0-2 analysts', lambda r: r['analyst_count'] is not None and r['analyst_count'] <= 2),
              ('>= 70', lambda r: r['pp'] >= 70), ('< 70', lambda r: r['pp'] < 70), ('all', lambda r: True)):
    P('  ' + block(nm, [r for r in NEW if f(r)]))
rho, p, n = within_day_rho(NEW, lambda r: r['pp'] * r['sd'], lambda r: r['mv'])
P(f'  within-day rho panel on these days {rho:+.3f}, perm p {p:.3f}, n {n}')
P('  overlap: share of no-anchor names among vol>=40%:',
  f"{sum(1 for r in rows if (r['vol20'] or 0) >= 40 and not r['anchor_covered'])}/{sum(1 for r in rows if (r['vol20'] or 0) >= 40)}",
  '; no-anchor by country:', {c: f"{sum(1 for r in rows if r['submarket']==c and not r['anchor_covered'])}/{sum(1 for r in rows if r['submarket']==c)}" for c in sorted({r['submarket'] for r in rows})})
for nm, f in (('no anchor & vol<40', lambda r: not r['anchor_covered'] and (r['vol20'] or 0) < 40),
              ('anchor & vol<40', lambda r: r['anchor_covered'] and (r['vol20'] or 0) < 40),
              ('no anchor & vol>=40', lambda r: not r['anchor_covered'] and (r['vol20'] or 0) >= 40),
              ('anchor & vol>=40', lambda r: r['anchor_covered'] and (r['vol20'] or 0) >= 40)):
    P('  all days ' + block(nm, [r for r in rows if f(r)]))

# session split of the legs
P('\n3c. LEGS BY SESSION (all names, entry close R-1)')
for ss in ('bmo', 'amc'):
    rs = [r for r in rows if r['session'] == ss]
    for nm, a, b in (('gap', 'close_Rm1', 'open_R'), ('open -> close R', 'open_R', 'close_R'), ('close R -> R+1', 'close_R', 'close_Rp1')):
        P(f'  {ss} ' + block(nm, rs, lambda r, a=a, b=b: leg(r, a, b)))

# ---- 4. entry / exit grid -------------------------------------------------------
ENTRIES = [('panel time D-1', 'entry_panel'), ('last 60m D-1', 'entry_last60'),
           ('last 30m D-1', 'entry_last30'), ('close D-1', 'close_entry_day'),
           ('close R-1', 'close_Rm1'), ('open R', 'open_R')]
EXITS = [('open R', 'open_R'), ('+15m', 'R_15m'), ('+30m', 'R_30m'), ('+1h', 'R_60m'),
         ('+2h', 'R_120m'), ('+4h', 'R_240m'), ('+6h', 'R_360m'), ('close R', 'close_R'),
         ('close R+1', 'close_Rp1'), ('close R+2', 'close_Rp2'), ('close R+5', 'close_Rp5')]


grid = {}
for title, rs in (('ALL', rows), ('>=60', [r for r in rows if r['pp'] >= 60]), ('>=70', STRONG), ('>=80', [r for r in rows if r['pp'] >= 80])):
    full = [r for r in rs if all(r['px'].get(k) is not None for k in
            ('entry_panel', 'entry_last60', 'entry_last30', 'close_entry_day', 'open_R', 'R_15m', 'R_30m', 'R_60m', 'R_120m', 'R_240m', 'R_360m'))]
    P(f'\n4. ENTRY x EXIT, {title}: mean signed gross %, intraday columns on the {len(full)} of {len(rs)} names with a full 5m tape; R+k columns on names with that close')
    P('  ' + 'entry \\ exit'.ljust(16) + ''.join(x[0].rjust(10) for x in EXITS))
    for en, ek in ENTRIES:
        line = '  ' + en.ljust(16)
        for xn, xk in EXITS:
            base = rs if xk.startswith('close_Rp') else full
            v = [leg(r, ek, xk) for r in base]; v = [y for y in v if y is not None]
            if ek == 'open_R' and xk == 'open_R' or len(v) < 2:
                line += '         -'; continue
            line += f'{st.mean(v):+.2f}'.rjust(10)
            grid[(title, en, xn)] = stats([r for r in rs], lambda r, ek=ek, xk=xk: leg(r, ek, xk))
        P(line)
    # paired: close R vs open R exit, entry close R-1
    pr = [(leg(r, 'close_Rm1', 'close_R'), leg(r, 'close_Rm1', 'open_R')) for r in rs]
    pr = [(a - b) for a, b in pr if a is not None and b is not None]
    t, p = tstat(pr)
    P(f'  paired close R minus open R exit: {st.mean(pr):+.2f} pt, n {len(pr)}, t {t:+.2f}, p {p:.3f}')
    pr = [(leg(r, 'entry_panel', 'close_R'), leg(r, 'close_Rm1', 'close_R')) for r in rs]
    pr = [(a - b) for a, b in pr if a is not None and b is not None]
    t, p = tstat(pr)
    P(f'  paired entry at panel time minus at close R-1: {st.mean(pr):+.2f} pt, n {len(pr)}, t {t:+.2f}, p {p:.3f}')
    for nm, a, b in (('gap  close R-1 -> open R', 'close_Rm1', 'open_R'), ('session open R -> close R', 'open_R', 'close_R'),
                     ('first hour open -> +1h', 'open_R', 'R_60m'), ('+1h -> close R', 'R_60m', 'close_R'),
                     ('day 2 close R -> close R+1', 'close_R', 'close_Rp1'), ('close R -> close R+5', 'close_R', 'close_Rp5')):
        P('  ' + block(nm, rs, lambda r, a=a, b=b: leg(r, a, b)))
RES['grid'] = {' | '.join(k): v for k, v in grid.items()}

# ---- 5. costs ------------------------------------------------------------------
P('\n5. COSTS')
cs = [r['cs'] for r in rows if r['cs'] is not None]
P(f'  Corwin-Schultz full spread (round trip), median {st.median(cs):.2f}%, by turnover band:')
for b in ('<$1m', '$1-5m', '$5-25m', '>$25m'):
    v = [r['cs'] for r in rows if turn_band(r) == b and r['cs'] is not None]
    if v: P(f'    {b:8s} n {len(v):3d} median {st.median(v):.2f}%  mean {st.mean(v):.2f}%')
for title, rs in (('all', rows), ('>=60', [r for r in rows if r['pp'] >= 60]), ('>=70', STRONG), ('>=80', [r for r in rows if r['pp'] >= 80])):
    P('  ' + block(f'{title} gross', rs))
    P('  ' + block(f'{title} net CS+0.10', rs, lambda r: r['ret'] - r['cost']))
    P('  ' + block(f'{title} net CS+0.10+UK stamp', rs, lambda r: r['ret'] - r['cost_uk_stamp']))
    P('  ' + block(f'{title} net flat 0.40', rs, lambda r: r['ret'] - 0.40))

# ---- 6. strategy search, out of sample -------------------------------------------
P('\n6. STRATEGY: chosen on period A (10-12..10-23), tested on period B (10-26..11-05)')
A = [r for r in rows if r['day'] <= '2026-10-23']; B = [r for r in rows if r['day'] > '2026-10-23']
P(f'  A: {len(A)} names over {len({r["day"] for r in A})} days; B: {len(B)} names over {len({r["day"] for r in B})} days')
FILTERS = {'none': lambda r: True,
           '4 of 4 agree': lambda r: r['sign_agree'] == 4,
           'low spread': lambda r: (r['panel_pct_sd'] or 0) < 12,
           'turnover >$1m': lambda r: (r['turnover_usd'] or 0) >= 1e6,
           'short only': lambda r: r['sd'] < 0, 'long only': lambda r: r['sd'] > 0,
           'hunter agrees': lambda r: (r['hunter_impact_sum'] or 0) * r['sd'] > 0}
XS = [('open R', 'close_Rm1', 'open_R'), ('+1h', 'close_Rm1', 'R_60m'), ('close R', 'close_Rm1', 'close_R'),
      ('close R+1', 'close_Rm1', 'close_Rp1'), ('open->close R', 'open_R', 'close_R')]
cands = []
for th in (50, 60, 70, 80):
    for fn, ff in FILTERS.items():
        for xn, ek, xk in XS:
            def f(r, ek=ek, xk=xk):
                v = leg(r, ek, xk)
                return None if v is None else v - r['cost']
            sa = [f(r) for r in A if r['pp'] >= th and ff(r)]; sa = [v for v in sa if v is not None]
            sb = [f(r) for r in B if r['pp'] >= th and ff(r)]; sb = [v for v in sb if v is not None]
            if len(sa) < 5: continue
            ta, pa = tstat(sa)
            tb, pb = tstat(sb) if len(sb) > 1 else (None, None)
            cands.append({'th': th, 'filter': fn, 'exit': xn, 'nA': len(sa), 'meanA': st.mean(sa), 'tA': ta or 0,
                          'nB': len(sb), 'meanB': st.mean(sb) if sb else None, 'tB': tb, 'pB': pb,
                          'hitB': (sum(1 for v in sb if v > 0) / len(sb)) if sb else None})
cands.sort(key=lambda c: -c['tA'])
P(f'  {len(cands)} candidates (threshold x filter x exit), net of CS spread + 0.10. Top 12 by t in A:')
for c in cands[:12]:
    P(f"   >={c['th']} {c['filter']:14s} {c['exit']:13s} A n {c['nA']:3d} {c['meanA']:+6.2f} t {c['tA']:+5.2f} | "
      f"B n {c['nB']:3d} {c['meanB'] if c['meanB'] is not None else float('nan'):+6.2f} hit {c['hitB'] or 0:4.0%} t {c['tB'] or float('nan'):+5.2f} p {c['pB'] or float('nan'):.3f}")
ra = [c['meanA'] for c in cands if c['meanB'] is not None]; rb = [c['meanB'] for c in cands if c['meanB'] is not None]
P(f'  rank correlation of candidate means A vs B over {len(ra)} candidates: {spearman(ra, rb):+.3f}  (near zero = in-sample choice does not carry)')
top = cands[:10]
P(f"  mean B return of A's top 10: {st.mean([c['meanB'] for c in top if c['meanB'] is not None]):+.2f}; of all candidates: {st.mean(rb):+.2f}")
RES['oos'] = {'top': cands[:12], 'rho_AB': spearman(ra, rb)}

# the pre-registered default, both halves
P('\n  The standing rule (>=70, entry close R-1, exit close R), net of CS+0.10, per half:')
for nm, rs in (('A', A), ('B', B), ('all', rows)):
    P('   ' + block(f'{nm} >=70 net', [r for r in rs if r['pp'] >= 70], lambda r: r['ret'] - r['cost']))
    P('   ' + block(f'{nm} >=70 gross', [r for r in rs if r['pp'] >= 70]))

# day-level book: equal weight within each day over >=th names, net
P('\n7. DAY-LEVEL BOOK (equal weight within day, net CS+0.10, close R-1 -> close R)')
for th in (60, 70, 80):
    for xn, ek, xk in (('close R', 'close_Rm1', 'close_R'), ('open R', 'close_Rm1', 'open_R')):
        by = defaultdict(list)
        for r in rows:
            if r['pp'] >= th:
                v = leg(r, ek, xk)
                if v is not None: by[r['day']].append(v - r['cost'])
        days = [st.mean(v) for v in by.values()]
        t, p = tstat(days)
        cum = 1
        for d in sorted(by): cum *= 1 + st.mean(by[d]) / 100
        P(f'  >={th} exit {xn:8s}: {len(days)} days with a call, mean/day {st.mean(days):+.2f}, '
          f'days up {sum(1 for d in days if d > 0)}/{len(days)}, t {t if t else float("nan"):+.2f}, p {p if p else float("nan"):.3f}, compounded fully invested {100 * (cum - 1):+.1f}%')

(S / 'report.txt').write_text('\n'.join(OUT) + '\n')
(S / 'results.json').write_text(json.dumps(RES, indent=1, default=str))
print('\n'.join(OUT))
