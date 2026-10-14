#!/usr/bin/env python3
"""Stage E-P: turn a name's panel percentile into an expected return on the trade.

Operator's request (2026-10-14): report, per name, what the trade is expected to earn,
not only how far into the judges' own top it sits. The threshold curve cannot answer
that (its "top 20%" is the average of everything at or above 80), so the expectation is
built from two parts that can each be estimated on more data than the curve alone:

    E[return] = E|move| x ( P(right) x k_right - (1 - P(right)) x k_wrong )

- P(right | |panel_pct|): the share of calls on the right side among names near that
  percentile (Gaussian kernel, bandwidth 12 points), shrunk toward a coin flip with a
  prior worth 8 names, then forced non-decreasing in |panel_pct| (pool adjacent
  violators). Fitted on every resolved US panel name: the blind backtest of the Opus
  5-era hunts (September Opus 5.5 out) plus the live E-P runs. The side is the sign of
  panel_pct. A logistic was tried first and lost in cross-validation (below).
- E|move| for THIS name, from its sealed baseline only: the event-implied move
  (`expected_move_pct`: the straddle net of ordinary volatility, else the median
  historical reaction), the median historical reaction and the 20-day realised
  volatility, as a log-linear regression with Duan's smearing back to points. It is a
  property of the stock and the print, not of the hunt, so it is fitted on every
  resolved US name in the ledger, not only the panel's.
- k_right, k_wrong: how the realised move compares with E|move| when the call was right
  and when it was wrong (a call that is right on bigger moves earns more than
  (2P - 1) x E|move|).

All moves are on the scorebord's window (BUY 13:30 ET on the entry day; SELL amc at the
next opening print, bmo at 13:00 ET on the report day), gross of costs. The interval is
the 10th to 90th percentile of the expectation over a day-block bootstrap of the whole
fit: it says how well the expectation is known, NOT how widely the trade can land.

The fit is checked before it is written: leave-one-day-out over the panel names, every
name predicted by a fit that never saw its day, against the flat mean and against the
pooled return curve of research/analyses/panel-mean-pct/ (expected_return.py), on
correlation, rank correlation, error and calibration slope, overall and per sample, plus
a quintile table of predicted against realised. Five variants were compared that way on
2026-10-14 (pooled curve; logistic x magnitude; logistic through 0.5 x magnitude; this
one; pooled curve x relative magnitude) and this one was best or tied on every measure;
that choice was made on the same 148 names, so the forward days are the real test. The
file records the comparison and every out-of-sample prediction; panel_score.py reads
only the frozen parameters.

  python3 researcher_us/scripts/panel_calibrate.py          # refit and write
  python3 researcher_us/scripts/panel_calibrate.py --check  # print, write nothing

Writes researcher_us/analysis/panel-calibration.json. Research only.
"""
import argparse, glob, json, math, random, statistics as st, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'researcher_us' / 'analysis' / 'panel-calibration.json'
sys.path.insert(0, str(REPO / 'researcher_us' / 'scripts'))
sys.path.insert(0, str(REPO / 'research' / 'analyses' / 'panel-mean-pct'))
DRAWS, SEED, EPS = 500, 11, 0.3


def sgn(x): return (x > 0) - (x < 0)


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


# ---------------------------------------------------------------- features

def features(b):
    """Log magnitude features from a sealed baseline, with the gaps filled from each
    other so a name missing one anchor is still priced. None without any anchor."""
    b = b or {}
    em = b.get('expected_move_pct')
    hm = (b.get('history') or {}).get('median_abs_move_pct')
    vol = (b.get('tape') or {}).get('realised_vol_20d_annualised_pct')
    em = em if em and em > 0 else (hm if hm and hm > 0 else None)
    hm = hm if hm and hm > 0 else em
    if not em and not vol:
        return None
    if not em:                      # a daily sd from the annualised vol, as a last resort
        em = hm = vol / math.sqrt(252) * 1.5
    vol = vol if vol and vol > 0 else em * math.sqrt(252) / 1.5
    return [1.0, math.log(em), math.log(hm), math.log(vol)]


def ols(X, y):
    k = len(X[0])
    A = [[sum(x[i] * x[j] for x in X) for j in range(k)] for i in range(k)]
    v = [sum(x[i] * t for x, t in zip(X, y)) for i in range(k)]
    for i in range(k):
        A[i][i] += 1e-6
    for i in range(k):                                     # Gauss-Jordan
        p = A[i][i]
        for j in range(k): A[i][j] /= p
        v[i] /= p
        for r in range(k):
            if r != i:
                f = A[r][i]
                for j in range(k): A[r][j] -= f * A[i][j]
                v[r] -= f * v[i]
    return v


BW, PRIOR = 12.0, 8.0
GRID = list(range(0, 101, 5))


def pav(vals, wts):
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


def hit_curve(pan):
    """P(right) on GRID: kernel share of right calls, shrunk to 0.5, monotone."""
    vals, wts = [], []
    for x in GRID:
        w = [math.exp(-0.5 * ((abs(r['pct']) - x) / BW) ** 2) for r in pan]
        sw = sum(w)
        vals.append((sum(wi * (r['ret'] > 0) for wi, r in zip(w, pan)) + PRIOR * 0.5) / (sw + PRIOR))
        wts.append(sw + PRIOR)
    return pav(vals, wts)


def on_grid(curve, x):
    i = min(int(x // 5), len(GRID) - 2)
    f = (x - GRID[i]) / 5
    return curve[i] * (1 - f) + curve[i + 1] * f


def logistic(xs, ys, iters=50):
    a, b = 0.0, 0.0
    for _ in range(iters):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = 1 / (1 + math.exp(-(a + b * x)))
            w = p * (1 - p)
            g0 += y - p; g1 += (y - p) * x
            h00 += w; h01 += w * x; h11 += w * x * x
        h00 += 1e-6; h11 += 1e-6
        det = h00 * h11 - h01 * h01
        a += (h11 * g0 - h01 * g1) / det
        b += (h00 * g1 - h01 * g0) / det
    return a, b


# ---------------------------------------------------------------- samples

def magnitude_sample():
    """Every resolved US ledger name with a sealed baseline: (features, |move|, day)."""
    import expected_return as ER
    L = load(REPO / 'dashboard/data/ledger.json') or {'names': []}
    fr = load(REPO / 'dashboard/data/scorebord-frozen.json') or {}
    out = []
    for n in L['names']:
        if n.get('duplicate_event') or n.get('rankable') is False:
            continue
        mv = ER.sb_move(n, fr)
        b = load(REPO / n['run'] / 'baselines' / f"{n['ticker']}.json")
        if mv is None or not b or b.get('event_occurred') is False:
            continue
        f = features(b)
        if f:
            out.append({'f': f, 'abs': abs(mv), 'date': n['run_date'], 'key': (n['run_date'], n['ticker'])})
    return out


def panel_sample():
    """Every resolved US panel name: |pct|, signed return, features, day."""
    import expected_return as ER
    L = load(REPO / 'dashboard/data/ledger.json') or {'names': []}
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    fr = load(REPO / 'dashboard/data/scorebord-frozen.json') or {}
    rows = []
    an = load(REPO / 'research/analyses/panel-mean-pct/panel-mean-pct.json')
    key = {x['id']: x for x in load(REPO / 'research/analyses/rejudge-four-models/key.json')}
    for r in an['datasets']['backtest']['US']['rows']:
        p = r['comb']['impact_sum']['gemiddelde']
        n = led.get((r['date'], r['ticker']))
        mv = ER.sb_move(n, fr)
        k = key.get(f"us/{r['date']}/{r['ticker']}") or {}
        f = features(load(REPO / k['baseline'])) if k.get('baseline') else None
        if p and mv is not None and f:
            rows.append({'src': 'backtest', 'date': r['date'], 'ticker': r['ticker'], 'pct': p,
                         'ret': sgn(p) * mv, 'abs': abs(mv), 'f': f})
    for (d, t), (p, full) in ER.october_pcts().items():
        mv = ER.sb_move(led.get((d, t)), fr)
        f = features(load(REPO / f'research/{d[:4]}/{d[5:7]}/{d}/edge-panel/baselines/{t}.json'))
        if p and full and mv is not None and f:
            rows.append({'src': 'oktober', 'date': d, 'ticker': t, 'pct': p,
                         'ret': sgn(p) * mv, 'abs': abs(mv), 'f': f})
    return rows


# ---------------------------------------------------------------- the model

def fit(mag, pan):
    """Parameters from a magnitude sample and a panel sample."""
    beta = ols([r['f'] for r in mag], [math.log(r['abs'] + EPS) for r in mag])
    res = [math.log(r['abs'] + EPS) - sum(b * x for b, x in zip(beta, r['f'])) for r in mag]
    smear = st.mean(math.exp(e) for e in res)
    hc = hit_curve(pan)
    em = lambda f: max(0.1, math.exp(sum(bb * x for bb, x in zip(beta, f))) * smear - EPS)  # noqa: E731
    right = [r['abs'] / em(r['f']) for r in pan if r['ret'] > 0]
    wrong = [r['abs'] / em(r['f']) for r in pan if r['ret'] <= 0]
    return {'beta': beta, 'smear': smear, 'p_right_grid': [round(x, 4) for x in hc],
            'k_right': st.mean(right) if right else 1.0, 'k_wrong': st.mean(wrong) if wrong else 1.0}


def predict(P, abs_pct, f):
    em = max(0.1, math.exp(sum(b * x for b, x in zip(P['beta'], f))) * P['smear'] - EPS)
    p = on_grid(P['p_right_grid'], abs_pct)
    return {'p_right': p, 'expected_abs_move_pct': em,
            'expected_return_pct': em * (p * P['k_right'] - (1 - p) * P['k_wrong'])}


def expected(cal, panel_pct, baseline):
    """What panel_score.py calls: the expectation and its 80% band for one name, or None
    when the name cannot be priced (no baseline anchor)."""
    f = features(baseline)
    if f is None or not panel_pct:
        return None
    pt = predict(cal['fit'], abs(panel_pct), f)
    draws = sorted(predict(d, abs(panel_pct), f)['expected_return_pct'] for d in cal['draws'])
    n = len(draws)
    return {'expected_return_pct': round(pt['expected_return_pct'], 2),
            'expected_return_lo80': round(draws[int(.1 * n)], 2) if n else None,
            'expected_return_hi80': round(draws[int(.9 * n)], 2) if n else None,
            'p_right': round(pt['p_right'], 3),
            'expected_abs_move_pct': round(pt['expected_abs_move_pct'], 2),
            'expected_move_pct': round(sgn(panel_pct) * pt['expected_return_pct'], 2)}


def load_calibration():
    return load(OUT)


# ---------------------------------------------------------------- validation

def _ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o): r[i] = k
    return r


def score_of(pr, real):
    if len(pr) < 3:
        return None
    mp, mr = st.mean(pr), st.mean(real)
    cov = sum((p - mp) * (q - mr) for p, q in zip(pr, real))
    vp = sum((p - mp) ** 2 for p in pr)
    vr = sum((q - mr) ** 2 for q in real)
    a, b = _ranks(pr), _ranks(real); ma = st.mean(a)
    top = sorted(zip(pr, real), key=lambda z: -z[0])[:max(5, len(pr) // 5)]
    return {'n': len(pr), 'corr': round(cov / math.sqrt(vp * vr), 3) if vp and vr else None,
            'spearman': round(sum((x - ma) * (y - ma) for x, y in zip(a, b)) / sum((x - ma) ** 2 for x in a), 3),
            'slope': round(cov / vp, 2) if vp else None,
            'rmse': round(math.sqrt(st.mean((p - q) ** 2 for p, q in zip(pr, real))), 2),
            'mean_predicted': round(mp, 2), 'mean_realised': round(mr, 2),
            'top20pct_predicted': round(st.mean(p for p, _ in top), 2),
            'top20pct_realised': round(st.mean(q for _, q in top), 2)}


def quintiles(rows):
    rows = sorted(rows, key=lambda r: r['pred'])
    k = len(rows)
    out = []
    for q in range(5):
        g = rows[q * k // 5:(q + 1) * k // 5]
        if g:
            rr = [r['real'] for r in g]
            out.append({'q': q + 1, 'n': len(g), 'predicted': round(st.mean(r['pred'] for r in g), 2),
                        'realised': round(st.mean(rr), 2),
                        'se': round(st.stdev(rr) / len(rr) ** .5, 2) if len(rr) > 1 else None,
                        'hit': round(sum(x > 0 for x in rr) / len(rr), 2)})
    return out


def cv(mag, pan):
    """Leave one panel day out: every name predicted by fits that never saw its day (the
    magnitude fit drops that day's names too). Returns the comparison, the rows and the
    quintile table."""
    import expected_return as ER
    preds = {'flat': [], 'pooled_curve': [], 'model': []}
    rows = []
    for d in sorted({r['date'] for r in pan}):
        tr = [r for r in pan if r['date'] != d]
        te = [r for r in pan if r['date'] == d]
        P = fit([m for m in mag if m['date'] != d], tr)
        kc = ER.fit(tr)[0]
        mu = st.mean(r['ret'] for r in tr)
        for r in te:
            m = predict(P, abs(r['pct']), r['f'])
            preds['flat'].append(mu)
            preds['pooled_curve'].append(ER.at(kc, abs(r['pct'])))
            preds['model'].append(m['expected_return_pct'])
            rows.append({'date': r['date'], 'ticker': r['ticker'], 'src': r['src'], 'pct': round(r['pct'], 1),
                         'pred': round(m['expected_return_pct'], 3), 'p_right': round(m['p_right'], 3),
                         'expected_abs_move_pct': round(m['expected_abs_move_pct'], 2), 'real': round(r['ret'], 3)})
    real = [r['real'] for r in rows]
    res = {}
    for k, pr in preds.items():
        res[k] = {'all': score_of(pr, real)}
        for s_ in ('backtest', 'oktober'):
            idx = [i for i, r in enumerate(rows) if r['src'] == s_]
            res[k][s_] = score_of([pr[i] for i in idx], [real[i] for i in idx])
    cal = {'all': quintiles(rows), 'backtest': quintiles([r for r in rows if r['src'] == 'backtest']),
           'oktober': quintiles([r for r in rows if r['src'] == 'oktober'])}
    return res, rows, cal


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    mag, pan = magnitude_sample(), panel_sample()
    print(f"magnitude sample {len(mag)} US names; panel sample {len(pan)} names "
          f"({sum(r['src'] == 'backtest' for r in pan)} backtest, {sum(r['src'] == 'oktober' for r in pan)} October), "
          f"{len({r['date'] for r in pan})} days")
    P = fit(mag, pan)
    print('P(right) by |pct|: ' + ', '.join(f"{x}% {on_grid(P['p_right_grid'], x):.2f}" for x in (0, 30, 50, 70, 80, 90, 100)))
    print(f"E|move| log-linear on [1, log implied, log history, log vol]: {[round(b, 3) for b in P['beta']]}, "
          f"smear {P['smear']:.3f}; k_right {P['k_right']:.2f}, k_wrong {P['k_wrong']:.2f}")
    res, rows, cal = cv(mag, pan)
    print(f"leave-one-day-out over {len(rows)} panel names (each predicted without its own day):")
    for k, v in res.items():
        for s_, x in v.items():
            if x:
                print(f"  {k:12s} {s_:8s} n {x['n']:3d}  corr {x['corr']:+.3f}  spearman {x['spearman']:+.3f}  "
                      f"slope {x['slope']:+.2f}  rmse {x['rmse']:5.2f}  mean pred {x['mean_predicted']:+.2f} "
                      f"real {x['mean_realised']:+.2f}  top fifth pred {x['top20pct_predicted']:+.2f} "
                      f"real {x['top20pct_realised']:+.2f}")
    for s_, qs in cal.items():
        print(f"  quintiles of the prediction, {s_}: " + '; '.join(
            f"Q{q['q']} n{q['n']} pred {q['predicted']:+.2f} real {q['realised']:+.2f}" for q in qs))
    rnd = random.Random(SEED)
    pdays = sorted({r['date'] for r in pan}); mdays = sorted({r['date'] for r in mag})
    pby = {d: [r for r in pan if r['date'] == d] for d in pdays}
    mby = {d: [r for r in mag if r['date'] == d] for d in mdays}
    draws = []
    for _ in range(DRAWS):
        ps = [r for d in (rnd.choice(pdays) for _ in pdays) for r in pby[d]]
        ms = [r for d in (rnd.choice(mdays) for _ in mdays) for r in mby[d]]
        draws.append(fit(ms, ps))
    doc = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
           'formula': 'E[return] = E|move| x (P(right) x k_right - (1 - P(right)) x k_wrong); '
                      'P(right) = monotone kernel share of right calls on |panel_pct| (bw 12, shrunk to 0.5 with 8 names), 5-point grid; '
                      'log(E|move| + 0.3) = beta . [1, log expected_move_pct, log history median, log realised vol 20d], smeared',
           'window': 'scorebord: BUY 13:30 ET on the entry day; SELL amc at the next open, bmo at 13:00 ET on the report day; gross',
           'sample': {'magnitude_names': len(mag), 'panel_names': len(pan),
                      'panel_backtest': sum(r['src'] == 'backtest' for r in pan),
                      'panel_october': sum(r['src'] == 'oktober' for r in pan), 'panel_days': len(pdays),
                      'last_panel_day': max(pdays)},
           'cross_validation': {'scheme': 'leave one panel day out', 'n': len(rows), 'models': res,
                                'quintiles': cal, 'rows': rows},
           'interval': f'10th-90th percentile of the expectation over {DRAWS} day-block bootstrap fits; '
                       'how well the expectation is known, not where the trade lands',
           'fit': P, 'draws': draws}
    if a.check:
        print('--check: nothing written'); return
    json.dump(doc, open(OUT, 'w'), indent=1)
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == '__main__':
    main()
