"""EU panel study: effectiveness, entry/exit grid, and cuts. Reads dataset.json."""
import json, math, random, statistics as st, collections, sys
from pathlib import Path

S = Path(__file__).resolve().parent
REPO = Path('/home/user/claude_research')
D = json.loads((S / 'dataset.json').read_text())
MEMBERS = ['opus5', 'opus55', 'sonnet55', 'fable51']
STRONG = 70  # the scorebord's fixed benchmark for the EU panel


# ---------- uniform-scale percentile (sizes only, no outcomes) ----------
def pools():
    h = json.loads((REPO / 'researcher_europe/analysis/panel-history.json').read_text())
    live = {m: sorted(abs(x['impact_sum']) for x in h[m] if 'europe' in (x.get('source') or '')
                      and not str(x.get('source')).startswith('seed')) for m in MEMBERS}
    bt = {m: sorted(abs((r['members'].get(m) or {}).get('impact_sum') or 0) for r in D if r['src'] == 'backtest')
          for m in MEMBERS}
    # backtest pool: every EU re-judge row, also the excluded September ones (sizes only)
    rj = REPO / 'research/analyses/rejudge-four-models'
    full = {m: [] for m in MEMBERS}
    keys = {k['id'] for k in json.loads((rj / 'key.json').read_text()) if k['region'] == 'europe'}
    for pack in ('eu', 'x1', 'x2'):
        for mm, name in (('opus5', 'opus5'), ('opus', 'opus55'), ('sonnet', 'sonnet55'), ('fable', 'fable51')):
            f = rj / f'out-{pack}-{mm}.json'
            if f.exists():
                full[name] += [abs(o['impact_sum']) for o in json.loads(f.read_text()) if o['id'] in keys]
    return live, {m: sorted(v) for m, v in full.items()}


def pct(ref, v):
    if not v:
        return 0.0
    return 100.0 * sum(1 for x in ref if x < abs(v)) / len(ref) * (1 if v > 0 else -1)


LIVE_POOL, BT_POOL = pools()
for r in D:
    pool = LIVE_POOL if r['src'] == 'live' else BT_POOL
    ps = [pct(pool[m], (r['members'].get(m) or {}).get('impact_sum')) for m in MEMBERS if m in r['members']]
    r['u_signed'] = sum(ps) / len(ps) if ps else 0.0
    r['u_pct'] = abs(r['u_signed'])
    r['u_side'] = 1 if r['u_signed'] > 0 else -1 if r['u_signed'] < 0 else 0
    if r['src'] == 'backtest':  # no live panel ran: the uniform scale is the only one
        r['panel_pct_signed'] = r['u_signed']; r['panel_pct'] = r['u_pct']; r['side'] = r['u_side']
    r['m_signed'] = {m: pct((LIVE_POOL if r['src'] == 'live' else BT_POOL)[m],
                            (r['members'].get(m) or {}).get('impact_sum')) for m in MEMBERS}


# ---------- returns ----------
def ret(a, b):
    if a in (None, 0) or b is None:
        return None
    return (b / a - 1) * 100


ENTRIES = {'seal': 'entry_seal', 'close_D-1': 'close_entry_day', 'close_R-1': 'close_Rm1'}
EXITS = ['open_R', 'R_30m', 'R_60m', 'R_120m', 'R_240m', 'close_R', 'close_Rp1', 'close_Rp2', 'close_Rp5']
EXIT_LABEL = {'open_R': 'open R', 'R_30m': 'R +30m', 'R_60m': 'R +1u', 'R_120m': 'R +2u', 'R_240m': 'R +4u',
              'close_R': 'close R', 'close_Rp1': 'close R+1', 'close_Rp2': 'close R+2', 'close_Rp5': 'close R+5'}


def usable(r):
    p = r['px'] or {}
    return (r.get('event_occurred_res') is not False and p.get('close_R') and p.get('close_Rm1')
            and r.get('side'))


def move(r, entry='close_R-1', exit_='close_R'):
    p = r['px']
    return ret(p.get(ENTRIES[entry]), p.get(exit_))


# ---------- stats ----------
def tstat(xs):
    if len(xs) < 3:
        return None
    sd = st.stdev(xs)
    return st.mean(xs) / (sd / math.sqrt(len(xs))) if sd else None


def p_from_t(t, n):
    # two-sided, normal approx with a small-n correction via t-dist (Hill's approximation)
    if t is None:
        return None
    df = n - 1
    x = df / (df + t * t)
    # regularised incomplete beta via continued fraction
    return betainc(df / 2, 0.5, x)


def betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b + lbeta) / a
    f, c, d = 1.0, 1.0, 0.0
    for i in range(200):
        m = i // 2
        if i == 0: num = 1.0
        elif i % 2 == 0: num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else: num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1 + num * d; d = 1 / d if abs(d) > 1e-30 else 1e30
        c = 1 + num / c if abs(c) > 1e-30 else 1e30
        f *= c * d
        if abs(c * d - 1) < 1e-10: break
    return front * (f - 1)


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spear(x, y):
    if len(x) < 4: return None
    rx, ry = ranks(x), ranks(y)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def spear_pooled_within_day(rows, key, val, iters=4000, seed=7):
    """Spearman on within-day ranks (each day's ranks scaled to 0..1), permutation p
    shuffling moves within each day."""
    days = collections.defaultdict(list)
    for r in rows:
        days[r['day']].append(r)
    def frame(perm=None):
        xs, ys = [], []
        for d, rr in days.items():
            if len(rr) < 2: continue
            k = [key(r) for r in rr]; v = [val(r) for r in rr]
            if perm: perm.shuffle(v)
            n = len(rr) - 1
            xs += [a / n for a in ranks(k)]; ys += [b / n for b in ranks(v)]
        return xs, ys
    xs, ys = frame()
    rho = spear(xs, ys)
    if rho is None: return None, None, len(xs)
    rng = random.Random(seed); hit = 0
    for _ in range(iters):
        a, b = frame(rng)
        if abs(spear(a, b) or 0) >= abs(rho) - 1e-12: hit += 1
    return rho, (hit + 1) / (iters + 1), len(xs)


def book(rows, entry='close_R-1', exit_='close_R', side_key='side'):
    xs = [r[side_key] * m for r in rows if (m := move(r, entry, exit_)) is not None]
    if not xs: return {'n': 0}
    t = tstat(xs)
    return {'n': len(xs), 'mean': st.mean(xs), 'median': st.median(xs),
            'hit': 100 * sum(1 for x in xs if x > 0) / len(xs), 't': t,
            'p': p_from_t(t, len(xs)) if t is not None else None}


def fmt(b):
    if not b or b.get('n', 0) == 0: return 'n 0'
    s = f"n {b['n']}, gem {b['mean']:+.2f}%, med {b['median']:+.2f}%, raak {b['hit']:.0f}%"
    if b.get('t') is not None: s += f", t {b['t']:.2f}, p {b['p']:.2f}"
    return s


if __name__ == '__main__':
    U = [r for r in D if usable(r)]
    print('usable', collections.Counter(r['src'] for r in U), 'of', collections.Counter(r['src'] for r in D))
    print([(r['day'], r['ticker'], r.get('event_occurred_res')) for r in D if not usable(r)])


# Both reported on 2026-10-15 (Ericsson Q3, Nordea Q3; checked on the web 2026-10-21);
# eu_resolve.py's Nordic feed match marked them false. Kept in, flagged in the report.
OVERRIDE_OCCURRED = {('2026-10-15', 'ERIC_A'), ('2026-10-15', 'NDA_FI')}
for r in D:
    if (r['day'], r['ticker']) in OVERRIDE_OCCURRED:
        r['event_occurred_res'] = True
        r['occurred_override'] = True


def tercile(v, cuts):
    for i, c in enumerate(cuts):
        if v < c: return i
    return len(cuts)


def report():
    out = []
    P = out.append
    U = [r for r in D if usable(r)]
    L = [r for r in U if r['src'] == 'live']
    B = [r for r in U if r['src'] == 'backtest']
    P(f"usable live {len(L)} of {sum(1 for r in D if r['src']=='live')}, backtest {len(B)} of {sum(1 for r in D if r['src']=='backtest')}")
    P('dropped: ' + ', '.join(f"{r['day']} {r['ticker']} ({'no event' if r.get('event_occurred_res') is False else 'pending' if (r['px'] or {}).get('pending') else 'side 0' if not r.get('side') else 'no price'})" for r in D if not usable(r)))
    # concentration
    P('\n## Concentration per live day')
    for d in sorted({r['day'] for r in D if r['src'] == 'live'}):
        rr = [r for r in D if r['day'] == d]
        c = collections.Counter(r['submarket'] for r in rr)
        P(f"{d}: {len(rr)} names, " + ', '.join(f'{k} {v}' for k, v in c.most_common()))
    P('live overall: ' + str(collections.Counter(r['submarket'] for r in L).most_common()))

    for name, rows in (('LIVE (okt 12-20, v7)', L), ('BACKTEST (re-judge, 22-23 sep, Opus 5 hunts)', B)):
        P(f'\n## Effectiveness — {name}, window close(R-1) -> close(R)')
        for key, lab in (('panel_pct_signed', 'panel_pct live scale'), ('u_signed', 'panel_pct uniform scale'),
                         ('hunter_impact_sum', 'hunter impact_sum')):
            rr = [r for r in rows if r.get(key) is not None]
            rho, p, n = spear_pooled_within_day(rr, lambda r: r[key], lambda r: move(r))
            rho2 = spear([r[key] for r in rr], [move(r) for r in rr])
            P(f"{lab}: within-day rho {rho if rho is None else round(rho,3)} (perm p {p if p is None else round(p,3)}, n {n}); pooled rho {rho2 if rho2 is None else round(rho2,3)}")
        for m in MEMBERS:
            rr = [r for r in rows if (r['members'].get(m) or {}).get('impact_sum') is not None]
            rho, p, n = spear_pooled_within_day(rr, lambda r: r['members'][m]['impact_sum'], lambda r: move(r), iters=2000)
            hits = [1 if (r['members'][m]['impact_sum'] or 0) * move(r) > 0 else 0 for r in rr if r['members'][m]['impact_sum']]
            P(f"  judge {m}: within-day rho {rho if rho is None else round(rho,3)} (p {p if p is None else round(p,3)}, n {n}); sign right {sum(hits)}/{len(hits)}")
        fc = [r for r in rows if r.get('run_up_20d') is not None]
        rho, p, n = spear_pooled_within_day(fc, lambda r: -r['run_up_20d'], lambda r: move(r), iters=2000)
        P(f"free control -run_up_20d: within-day rho {rho if rho is None else round(rho,3)} (p {p if p is None else round(p,3)}, n {n})")
        P('books (signed by panel side):')
        P('  all names:            ' + fmt(book(rows)))
        P('  long-all control:     ' + fmt(book(rows, side_key='_one')) if False else '  long-all control:     ' + fmt({**book([dict(r, _one=1) for r in rows], side_key='_one')}))
        for lo, hi in ((0, 50), (50, 70), (70, 101), (60, 101), (80, 101)):
            rr = [r for r in rows if lo <= r['panel_pct'] < hi]
            P(f'  panel_pct {lo}-{hi if hi<101 else 100}:      ' + fmt(book(rr)))
        rr = [r for r in rows if r.get('selected_consensus')]
        P('  consensus 3 of 4:     ' + fmt(book(rr)))
        for lo, hi in ((0, 50), (50, 70), (70, 101)):
            rr = [r for r in rows if lo <= r['u_pct'] < hi]
            P(f'  uniform pct {lo}-{hi if hi<101 else 100}:   ' + fmt(book([dict(r, side=r['u_side']) for r in rr])))
        # per-day
        P('  per day (all names / pct>=70):')
        for d in sorted({r['day'] for r in rows}):
            rr = [r for r in rows if r['day'] == d]
            P(f"    {d}: {fmt(book(rr))} | >=70: {fmt(book([r for r in rr if r['panel_pct']>=STRONG]))}")

    # entry/exit grid
    for name, rows in (('LIVE', L), ('BACKTEST', B)):
        for subset, sel in (('all names', lambda r: True), ('panel_pct >= 70', lambda r: r['panel_pct'] >= STRONG),
                            ('panel_pct >= 50', lambda r: r['panel_pct'] >= 50)):
            rr = [r for r in rows if sel(r)]
            P(f'\n## Entry x exit — {name}, {subset} (n {len(rr)}), mean signed % / hit % / t')
            P('entry \\ exit | ' + ' | '.join(EXIT_LABEL[e] for e in EXITS))
            for en in ENTRIES:
                cells = []
                for ex in EXITS:
                    b = book(rr, en, ex)
                    cells.append('—' if b['n'] == 0 else f"{b['mean']:+.2f} / {b['hit']:.0f} / {b['t']:.1f} (n{b['n']})" if b.get('t') is not None else f"{b['mean']:+.2f} (n{b['n']})")
                P(f'{en} | ' + ' | '.join(cells))
        # legs
        P(f'\n## Legs — {name} (signed, all names / >=70)')
        legs = [('seal -> close D-1 (rest of seal day)', 'entry_seal', 'close_entry_day'),
                ('close R-1 -> open R (gap)', 'close_Rm1', 'open_R'),
                ('open R -> close R (session)', 'open_R', 'close_R'),
                ('close R -> close R+1 (drift day 2)', 'close_R', 'close_Rp1'),
                ('close R -> close R+5 (drift week)', 'close_R', 'close_Rp5')]
        for lab, a, b in legs:
            def lb(rows_):
                xs = [r['side'] * x for r in rows_ if (x := ret(r['px'].get(a), r['px'].get(b))) is not None]
                if len(xs) < 2: return 'n<2'
                t = tstat(xs)
                return f"n {len(xs)}, {st.mean(xs):+.2f}%, hit {100*sum(x>0 for x in xs)/len(xs):.0f}%, t {t:.2f}" if t else f"n {len(xs)}, {st.mean(xs):+.2f}%"
            P(f'{lab}: {lb(rows)} | >=70: {lb([r for r in rows if r["panel_pct"]>=STRONG])}')
        # how much of the absolute move is in the gap
        sh = [abs(ret(r['px']['close_Rm1'], r['px']['open_R'])) / abs(move(r)) for r in rows
              if r['px'].get('open_R') and move(r) and abs(move(r)) > 1]
        if sh: P(f'median |gap| / |close-to-close move| (moves > 1%): {st.median(sh):.2f} over {len(sh)} names')

    # cuts (live + backtest kept apart; cuts on live only, backtest too small)
    P('\n## Cuts — LIVE, close(R-1) -> close(R), signed by panel side')
    def cut(label, keyf):
        groups = collections.defaultdict(list)
        for r in L:
            groups[keyf(r)].append(r)
        P(f'\n### {label}')
        for g in sorted(groups, key=lambda x: str(x)):
            rr = groups[g]
            rho = spear([r['panel_pct_signed'] for r in rr], [move(r) for r in rr])
            P(f"{g}: {fmt(book(rr))}; rho {'—' if rho is None else f'{rho:+.2f}'}; >=70: {fmt(book([r for r in rr if r['panel_pct']>=STRONG]))}")
    cut('market', lambda r: r['submarket'])
    cut('market group', lambda r: 'Nordics' if r['submarket'] in ('se', 'dk', 'no', 'fi') else 'UK' if r['submarket'] == 'uk' else 'Continent (de/fr/it/es/pl)')
    cut('turnover (median 20d, USD)', lambda r: '<1m' if (r['turnover_usd'] or 0) < 1e6 else '1-5m' if r['turnover_usd'] < 5e6 else '5-25m' if r['turnover_usd'] < 25e6 else '>25m')
    cut('analyst band', lambda r: r['analyst_band'])
    cut('anchor covered (short register)', lambda r: r['anchor_covered'])
    cut('history basis', lambda r: r['history_basis'])
    cut('session', lambda r: r['session'])
    cut('sector (industry)', lambda r: r['industry'])
    cut('panel side', lambda r: 'long' if r['side'] > 0 else 'short')
    cut('judges agree on sign (sign_agree)', lambda r: r.get('sign_agree'))
    sds = sorted(r['panel_pct_sd'] for r in L if r.get('panel_pct_sd') is not None)
    med = st.median(sds)
    cut(f'judge spread panel_pct_sd (median {med:.1f})', lambda r: 'low spread' if (r.get('panel_pct_sd') or 0) <= med else 'high spread')
    cut('realised vol 20d', lambda r: 'vol<25' if (r['vol20'] or 0) < 25 else 'vol 25-40' if r['vol20'] < 40 else 'vol>=40')
    cut('day size (names on panel that day)', lambda r: (lambda n: '1-5' if n <= 5 else '6-11' if n <= 11 else '12+')(sum(1 for x in D if x['day'] == r['day'])))
    # abs move by size
    P('\n### |move| by panel_pct band (is a high score a bigger mover?)')
    for lo, hi in ((0, 50), (50, 70), (70, 101)):
        rr = [abs(move(r)) for r in L if lo <= r['panel_pct'] < hi]
        if rr: P(f'{lo}-{min(hi,100)}: n {len(rr)}, median |move| {st.median(rr):.2f}%')
    # names table
    P('\n## Name table (live + backtest)')
    P('src | day | ticker | mkt | sess | turnover $m | panel_pct | side | uniform | hunter | move c2c % | gap % | signed c2c')
    for r in sorted(U, key=lambda r: (r['src'], r['day'], -r['panel_pct'])):
        mv = move(r); gp = ret(r['px']['close_Rm1'], r['px'].get('open_R'))
        P(f"{r['src']} | {r['day']} | {r['ticker']}{' *' if r.get('occurred_override') else ''} | {r['submarket']} | {r['session']} | {(r['turnover_usd'] or 0)/1e6:.1f} | {r['panel_pct']:.0f} | {'L' if r['side']>0 else 'S'} | {r['u_signed']:+.0f} | {r.get('hunter_impact_sum')} | {mv:+.2f} | {'' if gp is None else f'{gp:+.2f}'} | {r['side']*mv:+.2f}")
    return '\n'.join(out)


if __name__ == '__main__':
    txt = report()
    (S / 'report.txt').write_text(txt)
    print(txt)
