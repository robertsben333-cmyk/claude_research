#!/usr/bin/env python3
"""From a panel percentile to an expected return on the trade (operator, 2026-10-14).

The threshold curve is not an expected return: "top 20%: +7%" is the average of every
name at or above 80, so a name AT 80 earns less than that and a name at 98 more. What a
single name needs is the conditional expectation E[side x move | |panel_pct|], the
return the call earns as a function of how far into the judges' own top it sits.

Sample: every resolved US panel name. Two sources, read on the scorebord's window (BUY
13:30 ET on the entry day; SELL amc at the next opening print, bmo at 13:00 ET on the
report day; the frozen resolved moves where the scorebord froze one):

- `backtest`: the blind four-model re-judge of the Opus 5-era hunts, 2026-08-31 to
  09-22 (September Opus 5.5 out), percentiles within that sample (panel_mean_pct.py).
- `oktober`: the live stage E-P runs, percentiles point in time against each judge's
  live range before the run (panel_score.live_reference), exactly as the scorer now
  writes them.

Model, chosen to be dull on purpose, four pieces:
1. Kernel regression of side x move on |panel_pct| (Gaussian, bandwidth 12 points),
   pooled over both sources, on a grid of |pct| = 0, 5, ..., 100.
2. Shrinkage toward ZERO (no skill), with a prior worth K_PRIOR names:
   E = sum(w r) / (sum(w) + K_PRIOR). Where few names sit near a percentile, the
   estimate falls back toward zero rather than toward a lucky neighbour.
3. Monotone: the grid is forced non-decreasing in |pct| (pool adjacent violators,
   weighted by the names near each point). That is the hypothesis the selection rests
   on, and without it the fit bends wherever a few names happened to land; the raw
   kernel bent upward below |pct| 20 on this sample, which nothing predicts.
4. A day-block bootstrap (whole days resampled, 2000 draws) of the whole procedure for
   an 80% interval, since names on one day share a market.

Checked out of sample before it is used: fitted on the backtest only, does it predict the
October names (calibration slope of the realised signed return on the prediction)?

  python3 research/analyses/panel-mean-pct/expected_return.py [--day 2026-10-13]
"""
import argparse, glob, json, math, random, statistics as st, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / 'researcher_us' / 'scripts'))
import panel_score as PS  # noqa: E402

BW, K_PRIOR, DRAWS = 12.0, 8.0, 2000


def sgn(x): return (x > 0) - (x < 0)


def sb_move(n, frozen):
    """The scorebord's resolved US move, without a network call: the frozen value, else
    13:30 ET entry, amc out at the ledger's 09:30 bar, bmo out at 13:00 ET (hr_21)."""
    if not n:
        return None
    k = f"{n['run_date']}|{n['ticker']}"
    if k in frozen:
        return frozen[k]['move']
    e = (n.get('enpx') or {}).get('1330')
    if not e or n.get('pending'):
        return None
    if n.get('session') == 'amc':
        x = (n.get('px') or {}).get('open')
    elif n.get('hr_21') is not None and n.get('entry_close'):
        x = n['entry_close'] * (1 + n['hr_21'] / 100)
    else:
        x = None
    return None if not x else (x / e - 1) * 100


def october_pcts():
    """date, ticker -> panel_pct for every live E-P run, point in time."""
    hist = json.load(open(PS.HISTORY))
    out = {}
    for f in sorted(glob.glob(str(REPO / 'research/2026/10/*/edge-panel/edge-scores-panel.json'))):
        doc = json.load(open(f))
        run = Path(f).parent
        date = run.parent.name
        rows = doc.get('ranking') or []
        present = doc.get('members_present') or list(PS.MEMBERS)
        if rows and all('panel_pct' in r for r in rows):
            for r in rows:
                out[(date, r['ticker'])] = (r['panel_pct'], r.get('n_members') == len(present))
            continue
        ids = {r['id'] for r in rows}
        refs = {m: PS.live_reference(hist, m, 200, before=date, exclude=ids,
                                     fallback=PS.fallback_rows('seed', hist))[0] for m in present}
        for r in rows:
            ps = [PS.pct_of(refs[m], r['members'][m]['impact_sum']) for m in present if m in r['members']]
            out[(date, r['ticker'])] = (sum(ps) / len(ps), len(ps) == len(present))
    return out


GRID = list(range(0, 101, 5))


def kernel(rows, x):
    w = [math.exp(-0.5 * ((abs(r['pct']) - x) / BW) ** 2) for r in rows]
    sw = sum(w)
    return sum(wi * r['ret'] for wi, r in zip(w, rows)) / (sw + K_PRIOR), sw


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


def fit(rows):
    """The monotone, shrunk curve on GRID: (expected, names nearby) per grid point."""
    raw = [kernel(rows, x) for x in GRID]
    return pav([e for e, _ in raw], [sw + K_PRIOR for _, sw in raw]), [sw for _, sw in raw]


def at(curve, x):
    i = min(int(x // 5), len(GRID) - 2)
    f = (x - GRID[i]) / 5
    return curve[i] * (1 - f) + curve[i + 1] * f


def boot(rows, seed=7):
    """80% interval per grid point, the whole fit redone on day-block resamples."""
    rnd = random.Random(seed)
    days = sorted({r['date'] for r in rows})
    by = {d: [r for r in rows if r['date'] == d] for d in days}
    draws = []
    for _ in range(DRAWS):
        sample = [r for d in (rnd.choice(days) for _ in days) for r in by[d]]
        draws.append(fit(sample)[0])
    lo = [sorted(d[i] for d in draws)[int(.1 * DRAWS)] for i in range(len(GRID))]
    hi = [sorted(d[i] for d in draws)[int(.9 * DRAWS)] for i in range(len(GRID))]
    return lo, hi


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--day', default='2026-10-13'); a = ap.parse_args()
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    frozen = json.load(open(REPO / 'dashboard/data/scorebord-frozen.json'))
    rows = []
    bt = json.load(open(OUT / 'panel-mean-pct.json'))['datasets']['backtest']['US']['rows']
    for r in bt:
        mv = sb_move(led.get((r['date'], r['ticker'])), frozen)
        p = r['comb']['impact_sum']['gemiddelde']
        if mv is not None and p:
            rows.append({'src': 'backtest', 'date': r['date'], 'ticker': r['ticker'], 'pct': p, 'ret': sgn(p) * mv})
    octo = october_pcts()
    for (d, t), (p, full) in octo.items():
        mv = sb_move(led.get((d, t)), frozen)
        if mv is not None and p and full:
            rows.append({'src': 'oktober', 'date': d, 'ticker': t, 'pct': p, 'ret': sgn(p) * mv})
    bt_rows = [r for r in rows if r['src'] == 'backtest']; oc_rows = [r for r in rows if r['src'] == 'oktober']
    print(f"calibration sample: {len(bt_rows)} backtest + {len(oc_rows)} October = {len(rows)} names, "
          f"{len({r['date'] for r in rows})} days; mean signed return {st.mean(r['ret'] for r in rows):+.2f}%")

    # out of sample: fit on the backtest, predict October
    bt_curve = fit(bt_rows)[0]
    pred = [at(bt_curve, abs(r['pct'])) for r in oc_rows]
    real = [r['ret'] for r in oc_rows]
    mp, mr = st.mean(pred), st.mean(real)
    slope = sum((p - mp) * (q - mr) for p, q in zip(pred, real)) / (sum((p - mp) ** 2 for p in pred) or 1)
    corr = slope * (st.pstdev(pred) / (st.pstdev(real) or 1))
    print(f"out of sample (fit on backtest, predict October, n={len(oc_rows)}): mean predicted {mp:+.2f}%, "
          f"mean realised {mr:+.2f}%, slope {slope:+.2f}, corr {corr:+.2f}")

    est, sws = fit(rows)
    raw = [kernel(rows, x)[0] for x in GRID]
    lo, hi = boot(rows)
    curve = [{'abs_pct': x, 'expected': round(e, 2), 'kernel_before_monotone': round(r_, 2),
              'lo80': round(l, 2), 'hi80': round(h, 2), 'weight_names': round(w, 1)}
             for x, e, r_, l, h, w in zip(GRID, est, raw, lo, hi, sws)]
    print('\n|pct|  expected  80% interval      raw kernel  names nearby')
    for c in curve:
        if c['abs_pct'] % 10 == 0:
            print(f"{c['abs_pct']:5d}  {c['expected']:+6.2f}%  [{c['lo80']:+6.2f}, {c['hi80']:+6.2f}]  "
                  f"{c['kernel_before_monotone']:+6.2f}%  {c['weight_names']:6.1f}")

    day = []
    for (d, t), (p, full) in sorted(octo.items(), key=lambda kv: -abs(kv[1][0])):
        if d != a.day: continue
        n = led.get((d, t)) or {}
        e, sw = at(est, abs(p)), kernel(rows, abs(p))[1]
        l_, h_ = at(lo, abs(p)), at(hi, abs(p))
        mv = sb_move(n, frozen)
        day.append({'ticker': t, 'session': n.get('session'), 'panel_pct': round(p, 1), 'side': 'long' if p > 0 else 'short' if p < 0 else '-',
                    'selected': full and abs(p) >= 80, 'expected_return': round(e, 2), 'lo80': round(l_, 2), 'hi80': round(h_, 2),
                    'expected_move': round(sgn(p) * e, 2), 'names_nearby': round(sw, 1),
                    'realised_return': None if mv is None else round(sgn(p) * mv, 2)})
    print(f"\n{a.day}: expected return per trade on the scorebord window")
    for r in day:
        print(f"  {r['ticker']:6s} {r['session'] or '?':4s} pct {r['panel_pct']:+6.1f}  {r['side']:5s} "
              f"E {r['expected_return']:+5.2f}% [{r['lo80']:+5.2f}, {r['hi80']:+5.2f}]  "
              f"{'selected' if r['selected'] else ''}  realised {r['realised_return'] if r['realised_return'] is not None else 'open'}")
    json.dump({'method': {'bandwidth': BW, 'prior_names_at_zero': K_PRIOR, 'monotone': 'PAV on the grid',
                          'bootstrap': f'{DRAWS} day-block draws of the whole fit',
                          'window': 'scorebord: 13:30 ET in; amc out next open, bmo out 13:00 ET'},
               'sample': {'backtest': len(bt_rows), 'oktober': len(oc_rows)},
               'out_of_sample': {'n': len(oc_rows), 'mean_pred': mp, 'mean_real': mr, 'slope': slope, 'corr': corr},
               'curve': curve, 'day': a.day, 'names': day},
              open(OUT / f'expected-return-{a.day}.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
