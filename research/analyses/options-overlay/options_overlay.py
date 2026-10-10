#!/usr/bin/env python3
"""Would options have paid on the most confident US names?

Prices four ways of expressing each confident call against the stock itself:
  stock     sign x the realised move to the strategy exit (gross)
  option    an at-the-money call (predicted up) or put (predicted down)
  binary    a cash-or-nothing digital on the predicted side (an up/down bet)
  straddle  a long ATM straddle; where the judge gave abs_move_pct, also a
            conditional straddle: long when abs_move_pct > the event-implied
            move, short when below

PRICES ARE ESTIMATES. The sealed baseline stored one quote of the front expiry
covering the event (ATM implied vol, straddle mid, worst-leg spread / mid). No
option was ever bought and no chain was stored for the exit, so:
  - entry: Black-Scholes at the entry close, K = entry close, with the sealed
    event variance kept and the ordinary variance (20d realised vol) rolled to
    the entry time; a half spread paid on each leg;
  - exit: Black-Scholes at the strategy-exit spot (amc at the next open, bmo
    20:00 CET), post-event vol = 20d realised vol (full IV crush), the same
    dollar half spread paid again;
  - no commissions, no early-exercise, no skew (ATM vol for both legs).
Run: python3 options_overlay.py   (writes results.json, prints the tables)
"""
import json, math, os, random, statistics, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LEDGER = os.path.join(ROOT, 'dashboard/data/ledger.json')
REJUDGE = os.path.join(ROOT, 'research/analyses/rejudge-four-models')
FLOOR = {'Opus 5': 3.0, 'Opus 5.5': 2.8}       # the floor each model's book was cut at
SCALED_FLOOR = 1.76                              # book key since 2026-10-02
MIN_DV = 200_000
YEAR_H = 365 * 24.0

# ---------------------------------------------------------------- pricing
N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs(S, K, T, v):
    """call, put, digital-call, digital-put (r = 0). T in years, v annualised."""
    if T <= 1e-9 or v <= 1e-9:
        c, p = max(S - K, 0), max(K - S, 0)
        return c, p, float(S > K), float(S < K)
    sd = v * math.sqrt(T)
    d1 = (math.log(S / K) + 0.5 * sd * sd) / sd
    d2 = d1 - sd
    c = S * N(d1) - K * N(d2)
    return c, c - S + K, N(d2), N(-d2)

def et(ts_utc):
    """UTC iso -> naive New York time (EDT; every run here is Aug-Oct 2026)."""
    t = dt.datetime.fromisoformat(ts_utc.replace('Z', '+00:00'))
    return (t - dt.timedelta(hours=4)).replace(tzinfo=None)

def at(date, hh, mm=0):
    return dt.datetime.fromisoformat(date).replace(hour=hh, minute=mm)

def hours(a, b):
    return (b - a).total_seconds() / 3600.0

def price_name(n, opt, tape, seal_utc, side, abs_pred=None, p_up=None,
               cost=0.5, crush=1.0):
    """Returns a dict of per-strategy returns on premium (%), or None + reason."""
    S0 = n['entry_close']; mv = n['mv_strategy']
    if S0 is None or mv is None:
        return None, 'unresolved'
    iv = (opt.get('atm_iv_pct') or 0) / 100
    rv = (tape.get('realised_vol_20d_annualised_pct') or n.get('realised_vol_20d') or 0) / 100
    if iv <= 0 or rv <= 0:
        return None, 'no vol'
    expiry = at(opt['expiry'], 16)
    entry = at(n['entry_date'], 16)
    exit_ = at(n['reaction_date'], 9, 30) if n['session'] == 'amc' else at(n['event_date'], 14)
    if expiry < exit_:
        return None, 'expiry before exit'
    seal = et(seal_utc)
    Ts = max(hours(seal, expiry), 1) / YEAR_H
    ev = max(iv * iv * Ts - rv * rv * Ts, 0.0)            # event variance the chain carried
    Te = hours(entry, expiry) / YEAR_H
    ve = math.sqrt((ev + rv * rv * Te) / Te)
    Tx = max(hours(exit_, expiry), 0) / YEAR_H
    vx = rv * crush
    S1 = S0 * (1 + mv / 100)
    K = S0
    c0, p0, dc0, dp0 = bs(S0, K, Te, ve)
    c1, p1, dc1, dp1 = bs(S1, K, Tx, vx)
    f = opt.get('atm_spread_frac_of_mid')
    f_assumed = f is None
    if f is None:
        f = 0.25
    h = cost * f      # 0.5 = cross the quoted spread, 0.25 = fill halfway, 0 = mid

    def rt(buy_mid, sell_mid):                 # long: pay mid+h, sell at mid-h (dollar h fixed)
        hs = h * buy_mid
        cost = buy_mid + hs
        return (max(sell_mid - hs, 0) - cost) / cost * 100

    out = {'stock': side * mv,
           'implied_move': opt.get('event_implied_move_pct'),
           'straddle_move': opt.get('straddle_implied_move_pct'),
           'spread_frac': f, 'spread_assumed': f_assumed,
           'dte': round(Te * 365, 1)}
    if side > 0:
        out['option'] = rt(c0, c1); out['binary'] = rt(dc0, dc1); q = dc0
    else:
        out['option'] = rt(p0, p1); out['binary'] = rt(dp0, dp1); q = dp0
    # vertical spread (bull call / bear put): buy ATM, sell the strike one or two
    # event-implied moves away. The short leg pays the same DOLLAR half spread as
    # the ATM leg (adjacent strikes quote similar widths), so both legs cost.
    w = (opt.get('event_implied_move_pct') or opt.get('straddle_implied_move_pct') or 0) / 100
    hs_atm = h * (c0 if side > 0 else p0)
    for mult in (1, 2):
        K2 = S0 * (1 + side * mult * w)
        a0, b0, _, _ = bs(S0, K2, Te, ve)
        a1, b1, _, _ = bs(S1, K2, Tx, vx)
        if side > 0:
            long0, long1, sh0, sh1 = c0, c1, a0, a1
        else:
            long0, long1, sh0, sh1 = p0, p1, b0, b1
        debit = (long0 + hs_atm) - max(sh0 - hs_atm, 0)
        exitv = max(max(long1 - hs_atm, 0) - (sh1 + hs_atm), 0)   # never pay to close: let it lapse
        out[f'vertical_{mult}x'] = (exitv - debit) / debit * 100 if debit > 0 else None
        out[f'vertical_{mult}x_max_gain'] = (mult * w * S0 - debit) / debit * 100 if debit > 0 else None
    st0, st1 = c0 + p0, c1 + p1
    out['straddle'] = rt(st0, st1)
    # option P&L expressed per unit of stock notional, to compare leverage-free
    prem = (c0 if side > 0 else p0) * (1 + h)
    out['option_pnl_pct_of_spot'] = out['option'] / 100 * prem / S0 * 100
    out['binary_price'] = q * (1 + h)
    if abs_pred is not None and out['implied_move'] is not None:
        if abs_pred > out['implied_move']:
            out['straddle_cond'] = out['straddle']; out['straddle_cond_side'] = 'long'
        else:                                   # short: receive mid-h, buy back at mid+h
            hs = h * st0
            got = st0 - hs
            out['straddle_cond'] = (got - (st1 + hs)) / got * 100
            out['straddle_cond_side'] = 'short'
    if p_up is not None:
        p_side = p_up / 100 if side > 0 else 1 - p_up / 100
        out['p_side'] = p_side
        out['binary_edge'] = p_side - q * (1 + h)   # judge's probability minus the price paid
    return out, None

# ---------------------------------------------------------------- stats
def summarise(vals):
    v = [x for x in vals if x is not None]
    n = len(v)
    if n == 0:
        return {'n': 0}
    m = statistics.mean(v)
    sd = statistics.stdev(v) if n > 1 else float('nan')
    t = m / (sd / math.sqrt(n)) if n > 1 and sd > 0 else float('nan')
    # sign-flip randomisation p, two-sided (exact up to n = 16)
    if n <= 16:
        cnt = tot = 0
        for mask in range(1 << n):
            s = sum(x if (mask >> i) & 1 else -x for i, x in enumerate(v))
            tot += 1; cnt += abs(s) >= abs(sum(v)) - 1e-12
    else:
        rnd = random.Random(7); tot = 20000; cnt = 0
        for _ in range(tot):
            s = sum(x if rnd.random() < .5 else -x for x in v)
            cnt += abs(s) >= abs(sum(v)) - 1e-12
    return {'n': n, 'mean': round(m, 2), 'median': round(statistics.median(v), 2),
            'hit': round(sum(x > 0 for x in v) / n * 100), 't': round(t, 2),
            'p': round(cnt / tot, 3), 'worst': round(min(v), 1), 'best': round(max(v), 1)}

# ---------------------------------------------------------------- data
def load_json(p):
    try:
        return json.load(open(p))
    except Exception:
        return None

def baseline(run, tkr):
    return load_json(os.path.join(ROOT, run, 'baselines', f'{tkr}.json'))

def scaled_map(run):
    d = load_json(os.path.join(ROOT, run, 'edge-scores-scaled.json')) or {}
    return {r['ticker']: r for r in d.get('ranking', [])}

def usable(n, b):
    if b is None:
        return 'no baseline'
    o = b.get('options') or {}
    if o.get('status') != 'ok' or not o.get('expiry') or not o.get('atm_iv_pct'):
        return f"options {o.get('status')}"
    if (o.get('atm_spread_frac_of_mid') or 0) >= 1:
        return 'quote spread >= 100% of mid'
    return None

STRATS = ['stock', 'option', 'vertical_1x', 'vertical_2x', 'binary', 'straddle', 'straddle_cond']

def evaluate(group, members, **kw):
    """members: list of (ledger_row, side, abs_pred, p_up)."""
    rows, skipped = [], defaultdict(int)
    for n, side, A, P in members:
        if n.get('pending') or n.get('mv_strategy') is None:
            skipped['unresolved'] += 1; continue
        if (n.get('dollar_vol') or 0) < MIN_DV:
            skipped['under $200k turnover'] += 1; continue
        b = baseline(n['run'], n['ticker'])
        why = usable(n, b)
        if why:
            skipped[why] += 1; continue
        r, why = price_name(n, b['options'], b.get('tape') or {}, b['as_of_utc'], side, A, P, **kw)
        if why:
            skipped[why] += 1; continue
        r.update(ticker=n['ticker'], run_date=n['run_date'], session=n['session'], side=side,
                 move=n['mv_strategy'], abs_pred=A, p_up=P)
        rows.append(r)
    summ = {s: summarise([r.get(s) for r in rows]) for s in STRATS}
    summ['option_pnl_pct_of_spot'] = summarise([r['option_pnl_pct_of_spot'] for r in rows])
    gated = [r['binary'] for r in rows if r.get('binary_edge') is not None and r['binary_edge'] > 0]
    summ['binary_if_judge_beats_price'] = summarise(gated)
    return {'group': group, 'summary': summ, 'skipped': dict(skipped), 'rows': rows}

def main():
    L = json.load(open(LEDGER))
    names = [n for n in L['names'] if not n.get('duplicate_event')]
    by_key = {(n['run'], n['ticker']): n for n in names}
    out = []

    # A. live stage E, per prompt version and model, September Opus 5.5 out
    groups = defaultdict(list)
    for n in names:
        if n.get('sept_opus55'):
            continue
        groups[n['prov_key']].append(n)
    scaled = {}
    for key, ns in sorted(groups.items()):
        model = ns[0]['model_short']
        fl = FLOOR.get(model, 3.0)
        side = lambda n: 1 if n['impact_sum'] > 0 else -1
        conf = [(n, side(n), None, None) for n in ns if abs(n['impact_sum'] or 0) >= fl]
        allnz = [(n, side(n), None, None) for n in ns if (n['impact_sum'] or 0) != 0]
        if model == 'Opus 5.5':      # v9 carries abs_move_pct and p_up
            def ap(n):
                if n['run'] not in scaled:
                    scaled[n['run']] = scaled_map(n['run'])
                s = scaled[n['run']].get(n['ticker']) or {}
                return s.get('abs_move_pct'), s.get('p_up'), s.get('impact_scaled')
            conf = [(n, s, *ap(n)[:2]) for n, s, _, _ in conf]
            allnz = [(n, s, *ap(n)[:2]) for n, s, _, _ in allnz]
            book = [(n, 1 if ap(n)[2] > 0 else -1, *ap(n)[:2]) for n in ns
                    if ap(n)[2] is not None and abs(ap(n)[2]) >= SCALED_FLOOR]
            out.append(evaluate(f'E live {key} | impact_scaled >= {SCALED_FLOOR} (book key)', book))
        out.append(evaluate(f'E live {key} | |impact_sum| >= {fl}', conf))
        out.append(evaluate(f'E live {key} | every nonzero name (context)', allnz))

    # B. live stage E-P, selected names (3 of 4 judges in their own top 20%)
    ep = []
    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, 'research/2026/*/*/edge-panel/edge-scores-panel.json'))):
        d = load_json(f)
        run_e = os.path.relpath(os.path.dirname(os.path.dirname(f)), ROOT) + '/edge'
        for r in d.get('ranking', []):
            if r.get('selected'):
                n = by_key.get((run_e, r['ticker']))
                if n:
                    ab = [m.get('abs_move_pct') for m in r['members'].values() if m.get('abs_move_pct')]
                    pu = [m.get('p_up') for m in r['members'].values() if m.get('p_up')]
                    ep.append((n, r['side'], statistics.mean(ab) if ab else None,
                               statistics.mean(pu) if pu else None))
    out.append(evaluate('E-P live | panel-selected (3 of 4)', ep))

    # C. four-model blind re-judge (2026-10-01), US names. RETROSPECTIVE and the
    #    selection rule was chosen on these names: an in-sample check, not evidence.
    key = {k['id']: k for k in load_json(os.path.join(REJUDGE, 'key.json')) if k['region'] == 'us'}
    models = {'opus5': 'opus5', 'opus55': 'opus', 'sonnet55': 'sonnet', 'fable51': 'fable'}
    judged = defaultdict(dict)
    for m, tag in models.items():
        for pack in ('us1', 'us2', 'us3', 'x1', 'x2'):
            for r in load_json(os.path.join(REJUDGE, f'out-{pack}-{tag}.json')) or []:
                if r['id'] in key:
                    judged[r['id']][m] = r
    ids = []
    for i, k in key.items():
        n = by_key.get((k['run'], k['ticker']))
        if n is None or n.get('sept_opus55') or len(judged[i]) < 4:
            continue
        ids.append((i, n))
    # per-model top 20% by |impact_sum| over the sample (in-sample percentile)
    top = {}
    for m in models:
        vals = sorted(abs(judged[i][m]['impact_sum']) for i, _ in ids)
        top[m] = vals[int(0.8 * len(vals))] if vals else 1e9
    sel, o55 = [], []
    for i, n in ids:
        J = judged[i]
        side = 1 if sum(J[m]['impact_sum'] for m in models) > 0 else -1
        k_top = sum(1 for m in models if abs(J[m]['impact_sum']) >= top[m] and J[m]['impact_sum'] * side > 0)
        A = statistics.mean(J[m]['abs_move_pct'] for m in models)
        P = statistics.mean(J[m]['p_up'] for m in models)
        if k_top >= 3:
            sel.append((n, side, A, P))
        j = J['opus55']
        if abs(j['impact_sum']) >= top['opus55']:
            o55.append((n, 1 if j['impact_sum'] > 0 else -1, j['abs_move_pct'], j['p_up']))
    out.append(evaluate('Re-judge (in-sample) | 3 of 4 models in own top 20%', sel))
    out.append(evaluate('Re-judge (in-sample) | Opus 5.5 own top 20%', o55))
    allj = []
    for i, n in ids:
        j = judged[i]['opus55']
        if j['impact_sum'] != 0:
            allj.append((n, 1 if j['impact_sum'] > 0 else -1, j['abs_move_pct'], j['p_up']))
    out.append(evaluate('Re-judge (in-sample) | Opus 5.5 every nonzero name (context)', allj))

    # D. market-level checks, every version pooled on purpose: these describe the
    #    options market on these names, not any prompt version's skill
    pool = [n for n in names if not n.get('sept_opus55')]
    out.append(evaluate('Every resolved name | short straddle (market check, not a hunt signal)',
                        [(n, 1, -1.0, None) for n in pool]))
    ratio, wi, wo = [], [], []
    for n in pool:
        if n.get('pending') or n.get('mv_strategy') is None:
            continue
        b = baseline(n['run'], n['ticker'])
        ok = b is not None and usable(n, b) is None
        fl = FLOOR.get(n['model_short'], 3.0)
        if abs(n['impact_sum'] or 0) >= fl and (n.get('dollar_vol') or 0) >= MIN_DV:
            (wi if ok else wo).append((1 if n['impact_sum'] > 0 else -1) * n['mv_strategy'])
        if ok and b['options'].get('event_implied_move_pct'):
            ratio.append(abs(n['mv_strategy']) / b['options']['event_implied_move_pct'])
    market = {'realised_over_event_implied': {'n': len(ratio), 'median': round(statistics.median(ratio), 2),
                                              'share_above_1': round(sum(x > 1 for x in ratio) / len(ratio), 2)},
              'confident_stock_with_usable_options': summarise(wi),
              'confident_stock_without_usable_options': summarise(wo)}
    print('\n# market', json.dumps(market))

    # sensitivity on the main confident groups
    sens = []
    for g in out:
        if 'context' in g['group']:
            continue
        members = [(by_key[(f"research/{r['run_date'][:4]}/{r['run_date'][5:7]}/{r['run_date']}/edge", r['ticker'])],
                    r['side'], r['abs_pred'], r['p_up']) for r in g['rows']]
        for label, kw in (('at mid, no spread', {'cost': 0}),
                          ('filled halfway inside the spread', {'cost': 0.25}),
                          ('IV only half crushed (post vol 1.5x realised)', {'crush': 1.5})):
            e = evaluate(g['group'], members, **kw)
            sens.append({'group': g['group'], 'variant': label,
                         'summary': {s: e['summary'][s] for s in ('option', 'vertical_1x', 'vertical_2x', 'binary', 'straddle')}})
    # the vertical on the long side only (the 'big positive move' case)
    for g in out:
        up = [r for r in g['rows'] if r['side'] > 0]
        g['summary']['vertical_1x_longs_only'] = summarise([r.get('vertical_1x') for r in up])
        g['summary']['vertical_2x_longs_only'] = summarise([r.get('vertical_2x') for r in up])
        g['summary']['stock_longs_only'] = summarise([r['stock'] for r in up])
    json.dump({'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'note': __doc__,
               'groups': out, 'sensitivity': sens, 'market': market},
              open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=str)
    for g in out:
        print(f"\n## {g['group']}   skipped: {g['skipped']}")
        for s, v in g['summary'].items():
            if v.get('n'):
                print(f"  {s:28s} n={v['n']:3d} mean={v['mean']:+8.2f} med={v['median']:+8.2f} "
                      f"hit={v['hit']:3d}% t={v['t']:+.2f} p={v['p']:.3f}")
    print('\n# sensitivity')
    for s in sens:
        print(s['group'], '|', s['variant'], {k: (v.get('n'), v.get('mean'), v.get('p')) for k, v in s['summary'].items()})

if __name__ == '__main__':
    main()
