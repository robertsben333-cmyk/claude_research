#!/usr/bin/env python3
"""Stage E-P: one expected return for every panel percentile.

Operator's design (2026-10-14): the panel percentile leads. Each |panel_pct| is
referenced to ONE expected return on the trade, the same for every name at that
percentile, so "this name sits at 85" and "a name at 85 has earned about X" are the same
statement. Nothing name-specific enters (a version that scaled by each name's expected
move size was built and withdrawn the same day on the operator's instruction).

Why not just read the threshold curve: "top 20%: +7%" is the average of everything AT OR
ABOVE 80, so a name at exactly 80 earns less than that and a name at 98 more. The number a
single name needs is the conditional expectation E[side x move | |panel_pct|]:

1. Kernel regression of the signed return on |panel_pct| (Gaussian, bandwidth 12
   points) on a grid of 0, 5, ..., 100, over every resolved US panel name: the blind
   backtest of the Opus 5-era hunts (2026-08-31 to 09-22, September Opus 5.5 out) and the
   live E-P runs, each at its own percentile (point in time for the live runs).
2. Shrunk toward zero (no skill) with a prior worth 8 names, so a stretch with few names
   falls back toward zero rather than toward a lucky neighbour.
3. Forced non-decreasing in |panel_pct| (pool adjacent violators): the selection rests on
   higher being better, and without it the curve bends wherever a few names landed.
4. An 80% band from a day-block bootstrap of the whole fit: how well the expectation at
   that percentile is known, NOT where a trade can land (that spread is ten times wider).

The same is done for the share of calls on the right side (`p_right`), shrunk to a coin
flip, so each percentile also reads as a hit rate.

All moves are on the scorebord's window (BUY 13:30 ET on the entry day; SELL amc at the
next opening print, bmo at 13:00 ET on the report day), gross of costs.

Checked before it is written: leave one panel day out, every name predicted by a curve
that never saw its day, against the flat mean, overall and per sample; and per 10-point
band of |panel_pct| the realised average beside the curve, backtest and October apart.
panel_score.py reads only the frozen curve.

  python3 researcher_us/scripts/panel_calibrate.py          # refit and write
  python3 researcher_us/scripts/panel_calibrate.py --check  # print, write nothing

Writes researcher_us/analysis/panel-calibration.json. Research only.
"""
import argparse, json, math, random, statistics as st, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'researcher_us' / 'analysis' / 'panel-calibration.json'
sys.path.insert(0, str(REPO / 'researcher_us' / 'scripts'))
sys.path.insert(0, str(REPO / 'research' / 'analyses' / 'panel-mean-pct'))
DRAWS, SEED = 1000, 11
BW, PRIOR = 12.0, 8.0
GRID = list(range(0, 101, 5))


def sgn(x): return (x > 0) - (x < 0)


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


# ---------------------------------------------------------------- the curve

def pav(vals, wts):
    """Weighted pool-adjacent-violators: the closest non-decreasing sequence."""
    blocks = []
    for v, w in zip(vals, wts):
        blocks.append([v * w, w, 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            a, b = blocks.pop(), blocks.pop()
            blocks.append([a[0] + b[0], a[1] + b[1], a[2] + b[2]])
    out = []
    for s_, w, k in blocks:
        out += [s_ / w] * k
    return out


def curve(rows, value, prior_at):
    """Monotone, shrunk kernel curve of `value(row)` on |pct| over GRID, and the names
    near each grid point."""
    vals, wts, near = [], [], []
    for x in GRID:
        w = [math.exp(-0.5 * ((abs(r['pct']) - x) / BW) ** 2) for r in rows]
        sw = sum(w)
        vals.append((sum(wi * value(r) for wi, r in zip(w, rows)) + PRIOR * prior_at) / (sw + PRIOR))
        wts.append(sw + PRIOR)
        near.append(sw)
    return pav(vals, wts), near


def fit(rows):
    ret, near = curve(rows, lambda r: r['ret'], 0.0)
    hit, _ = curve(rows, lambda r: 1.0 if r['ret'] > 0 else 0.0, 0.5)
    return {'expected_return': [round(x, 4) for x in ret], 'p_right': [round(x, 4) for x in hit],
            'names_near': [round(x, 1) for x in near]}


def on_grid(c, x):
    x = max(0.0, min(100.0, x))
    i = min(int(x // 5), len(GRID) - 2)
    f = (x - GRID[i]) / 5
    return c[i] * (1 - f) + c[i + 1] * f


def expected(cal, panel_pct, baseline=None):
    """What panel_score.py calls: the expected return for a percentile, its 80% band and
    the hit rate, or None for a zero percentile. Pass the SIGNED value (panel_pct_signed)
    so expected_move_pct carries the side; the 0-100 strength alone gives the same return.
    `baseline` is accepted and ignored: the percentile alone decides."""
    if not cal or not panel_pct:
        return None
    x = abs(panel_pct)
    e = on_grid(cal['fit']['expected_return'], x)
    return {'expected_return_pct': round(e, 2),
            'expected_return_lo80': round(on_grid(cal['band']['lo80'], x), 2),
            'expected_return_hi80': round(on_grid(cal['band']['hi80'], x), 2),
            'p_right': round(on_grid(cal['fit']['p_right'], x), 3),
            'expected_move_pct': round(sgn(panel_pct) * e, 2)}


def load_calibration():
    return load(OUT)


# ---------------------------------------------------------------- the sample

def panel_sample():
    """Every resolved US panel name: date, ticker, source, |pct| and the signed return."""
    import expected_return as ER
    L = load(REPO / 'dashboard/data/ledger.json') or {'names': []}
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    fr = load(REPO / 'dashboard/data/scorebord-frozen.json') or {}
    rows = []
    an = load(REPO / 'research/analyses/panel-mean-pct/panel-mean-pct.json')
    for r in an['datasets']['backtest']['US']['rows']:
        p = r['comb']['impact_sum']['gemiddelde']
        mv = ER.sb_move(led.get((r['date'], r['ticker'])), fr)
        if p and mv is not None:
            rows.append({'src': 'backtest', 'date': r['date'], 'ticker': r['ticker'], 'pct': p, 'ret': sgn(p) * mv})
    for (d, t), (p, full) in ER.october_pcts().items():
        mv = ER.sb_move(led.get((d, t)), fr)
        if p and full and mv is not None:
            rows.append({'src': 'oktober', 'date': d, 'ticker': t, 'pct': p, 'ret': sgn(p) * mv})
    return rows


# ---------------------------------------------------------------- the check

def score_of(pr, real):
    if len(pr) < 3:
        return None
    mp, mr = st.mean(pr), st.mean(real)
    cov = sum((p - mp) * (q - mr) for p, q in zip(pr, real))
    vp = sum((p - mp) ** 2 for p in pr)
    vr = sum((q - mr) ** 2 for q in real)
    top = sorted(zip(pr, real), key=lambda z: -z[0])[:max(5, len(pr) // 5)]
    return {'n': len(pr), 'corr': round(cov / math.sqrt(vp * vr), 3) if vp and vr else None,
            'slope': round(cov / vp, 2) if vp else None,
            'rmse': round(math.sqrt(st.mean((p - q) ** 2 for p, q in zip(pr, real))), 2),
            'mean_predicted': round(mp, 2), 'mean_realised': round(mr, 2),
            'top20pct_predicted': round(st.mean(p for p, _ in top), 2),
            'top20pct_realised': round(st.mean(q for _, q in top), 2)}


def bands(rows):
    """Realised against predicted per 10-point band of |pct| (the last band takes 90-100)."""
    out = []
    for lo in range(0, 100, 10):
        g = [r for r in rows if lo <= abs(r['pct']) < lo + 10 or (lo == 90 and abs(r['pct']) >= 100)]
        if not g:
            continue
        rr = [r['real'] for r in g]
        out.append({'from': lo, 'to': lo + 10, 'n': len(g), 'predicted': round(st.mean(r['pred'] for r in g), 2),
                    'realised': round(st.mean(rr), 2),
                    'se': round(st.stdev(rr) / len(rr) ** .5, 2) if len(rr) > 1 else None,
                    'hit': round(sum(x > 0 for x in rr) / len(rr), 2)})
    return out


def cv(rows):
    """Leave one panel day out: every name predicted by a curve that never saw its day."""
    out, flat = [], []
    for d in sorted({r['date'] for r in rows}):
        tr = [r for r in rows if r['date'] != d]
        F = fit(tr)
        mu = st.mean(r['ret'] for r in tr)
        for r in (r for r in rows if r['date'] == d):
            out.append({'date': r['date'], 'ticker': r['ticker'], 'src': r['src'], 'pct': round(r['pct'], 1),
                        'pred': round(on_grid(F['expected_return'], abs(r['pct'])), 3), 'real': round(r['ret'], 3)})
            flat.append(mu)
    real = [r['real'] for r in out]
    res = {'curve': {'all': score_of([r['pred'] for r in out], real)},
           'flat': {'all': score_of(flat, real)}}
    for s_ in ('backtest', 'oktober'):
        idx = [i for i, r in enumerate(out) if r['src'] == s_]
        res['curve'][s_] = score_of([out[i]['pred'] for i in idx], [real[i] for i in idx])
        res['flat'][s_] = score_of([flat[i] for i in idx], [real[i] for i in idx])
    by_band = {'all': bands(out), 'backtest': bands([r for r in out if r['src'] == 'backtest']),
               'oktober': bands([r for r in out if r['src'] == 'oktober'])}
    return res, out, by_band


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    rows = panel_sample()
    days = sorted({r['date'] for r in rows})
    print(f"panel sample {len(rows)} names ({sum(r['src'] == 'backtest' for r in rows)} backtest, "
          f"{sum(r['src'] == 'oktober' for r in rows)} October), {len(days)} days")
    F = fit(rows)
    rnd = random.Random(SEED)
    by = {d: [r for r in rows if r['date'] == d] for d in days}
    draws = [fit([r for d in (rnd.choice(days) for _ in days) for r in by[d]])['expected_return'] for _ in range(DRAWS)]
    lo = [round(sorted(dr[i] for dr in draws)[int(.1 * DRAWS)], 4) for i in range(len(GRID))]
    hi = [round(sorted(dr[i] for dr in draws)[int(.9 * DRAWS)], 4) for i in range(len(GRID))]
    print('|pct|  expected  80% band          P(right)  names near')
    for i, x in enumerate(GRID):
        if x % 10 == 0:
            print(f"{x:5d}  {F['expected_return'][i]:+6.2f}%  [{lo[i]:+6.2f}, {hi[i]:+6.2f}]  {F['p_right'][i]:.2f}      {F['names_near'][i]:5.1f}")
    res, out, by_band = cv(rows)
    print(f"leave-one-day-out over {len(out)} names:")
    for k, v in res.items():
        for s_, x in v.items():
            if x:
                print(f"  {k:6s} {s_:8s} n {x['n']:3d}  corr {x['corr']:+.3f}  slope {x['slope']:+.2f}  rmse {x['rmse']:5.2f}  "
                      f"top fifth pred {x['top20pct_predicted']:+.2f} real {x['top20pct_realised']:+.2f}")
    for s_, bs in by_band.items():
        print(f"  {s_:8s} " + '; '.join(f"{b['from']}-{b['to']} n{b['n']} pred {b['predicted']:+.1f} real {b['realised']:+.1f}" for b in bs))
    doc = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'leads': 'the panel percentile: one expected return per |panel_pct|, the same for every name',
           'method': f'monotone kernel curve of the signed return on |panel_pct| (bandwidth {BW}, shrunk to 0 '
                     f'with {PRIOR} names), grid 0..100 by 5; p_right the same, shrunk to 0.5',
           'window': 'scorebord: BUY 13:30 ET on the entry day; SELL amc at the next open, bmo at 13:00 ET on the report day; gross',
           'sample': {'panel_names': len(rows), 'panel_backtest': sum(r['src'] == 'backtest' for r in rows),
                      'panel_october': sum(r['src'] == 'oktober' for r in rows), 'panel_days': len(days),
                      'last_panel_day': days[-1]},
           'grid': GRID, 'fit': F,
           'band': {'lo80': lo, 'hi80': hi, 'note': f'10th-90th percentile over {DRAWS} day-block bootstrap fits; '
                                                   'how well the expectation is known, not where a trade lands'},
           'cross_validation': {'scheme': 'leave one panel day out', 'n': len(out), 'models': res,
                                'by_band': by_band, 'rows': out}}
    if a.check:
        print('--check: nothing written'); return
    json.dump(doc, open(OUT, 'w'), indent=1)
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == '__main__':
    main()
