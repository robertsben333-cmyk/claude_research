#!/usr/bin/env python3
"""The four-model panel in %, October only: do the highest average expected moves pay?

Operator's question (2026-10-14): drop the 3-of-4 rule for this read and ask the usual
thing, whether the HIGHEST scores pay, with every number in % so that it reads directly
and a future model can be added without re-scaling the others.

What a judge returns is already a percentage: impact_sum = (2 x p_up / 100 - 1) x
abs_move_pct, the expected signed move in % of spot (config/panel-judge.md). The four are
averaged per name as stated (`pct_stated`), with no fitting and no history, so a new model
adds its own number without changing anyone else's.

Two diagnostics are written per region, neither used to rank:
- `k_magnitude` = median |realised move| / the model's median abs_move_pct. It tests
  whether the models disagree about how BIG a move is. In October they do not (US 7-8%
  for all four, Japan 3.5-4.5%), so this calibration moves every model alike and cannot
  balance them: the difference between the models is in p_up, how sure they are.
- `kappa` = realised move per stated point, a through-origin slope on the signed outcome.
  This is the only per-model % calibration that would balance them, and it needs the sign
  of the outcome, so on a few dozen names it is in sample and noisy. Measure it forward;
  use it only once a region has enough resolved names to freeze it.

For every threshold x: every resolved name with |average| >= x, traded on the sign of the
average, equal weight, gross. US: stage E-P runs, the dashboard ledger's close-to-close
move (`mv_close`) and strategy exit. Other regions: the four-model panel the market stages
run since 2026-10-08, each market's own resolver window. September Opus 5.5 hunts are out
on the operator's instruction; every run read here is October, after the shared core.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
"""
import glob, json, statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')
REGIONS = {  # dir under research/<Y>/<M>/<D>/, the market resolver's file, label
    'US': ('edge-panel', None, 'United States (stage E-P)'),
    'EU': ('europe', 'eu-resolved.json', 'Europe (10 markets)'),
    'JP': ('japan', 'jp-resolved.json', 'Japan'),
    'AU': ('australia', 'au-resolved.json', 'Australia'),
    'CA': ('canada', 'canada-resolved.json', 'Canada'),
}


def sgn(x): return (x > 0) - (x < 0)


def move_of(row):
    for k in ('realised_move_pct', 'move_pct', 'realised_move'):
        if row.get(k) is not None:
            return row[k]
    return None


def market_moves(run, fname, region, date):
    """ticker -> realised move from the market's resolver: the day's own file, else the
    copy resolved for this analysis (resolved/<id>-<date>.json), never a pending row."""
    for f in (Path(run) / fname, OUT / 'resolved' / f"{region.lower()}-{date}.json"):
        if f.exists():
            rows = json.load(open(f)).get('rows') or []
            return {r['ticker']: move_of(r) for r in rows
                    if move_of(r) is not None and not r.get('move_pending')
                    and r.get('event_occurred') is not False and r.get('rankable') is not False}
    return {}


def load_region(region, led):
    sub, fname, _ = REGIONS[region]
    names = []
    for run in sorted(glob.glob(str(REPO / f'research/2026/10/*/{sub}'))):
        pf = Path(run) / 'edge-scores-panel.json'
        if not pf.exists(): continue
        date = Path(run).parent.name
        mv = {} if region == 'US' else market_moves(run, fname, region, date)
        for r in json.load(open(pf))['ranking']:
            if not all(m in r['members'] for m in MEMBERS): continue
            if region == 'US':
                l = led.get((date, r['ticker'])) or {}
                move, strat = l.get('mv_close'), l.get('mv_strategy')
            else:
                move, strat = mv.get(r['ticker']), None
            names.append({'date': date, 'ticker': r['ticker'], 'selected': r['selected'],
                          'stated': {m: r['members'][m]['impact_sum'] for m in MEMBERS},
                          'abs_move': {m: r['members'][m].get('abs_move_pct') for m in MEMBERS},
                          'move': move, 'move_strategy': strat})
    return names


def curve_of(res, key):
    out = []
    for x in sorted({abs(r[key]) for r in res}):
        v = [r for r in res if abs(r[key]) >= x]
        s = [sgn(r[key]) * r['move'] for r in v]
        s2 = [sgn(r[key]) * r['move_strategy'] for r in v if r['move_strategy'] is not None]
        out.append({'x': round(x, 3), 'n': len(v), 'days': len({r['date'] for r in v}),
                    'mean': st.mean(s), 'se': st.stdev(s) / len(s) ** .5 if len(s) > 1 else None,
                    'hit': sum(y > 0 for y in s) / len(s),
                    'mean_strategy': st.mean(s2) if s2 else None})
    return out


def main():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    doc = {'generated_from': 'research/2026/10/*, October only', 'regions': {}}
    for region in REGIONS:
        names = load_region(region, led)
        res = [n for n in names if n['move'] is not None]
        R = {'label': REGIONS[region][2], 'names': len(names), 'resolved': len(res),
             'days': sorted({n['date'] for n in res})}
        if len(res) < 5:
            R['note'] = 'fewer than five resolved names: nothing to read yet'
            doc['regions'][region] = R
            print(f"{region}: {len(names)} panel names, {len(res)} resolved, skipped")
            continue
        real = st.median(abs(n['move']) for n in res)
        k = {}
        for m in MEMBERS:
            am = [n['abs_move'][m] for n in res if n['abs_move'][m]]
            k[m] = real / st.median(am) if am else None
        for n in names:
            n['pct_stated'] = round(st.mean(n['stated'].values()), 3)
        res = [n for n in res if n['pct_stated'] != 0]
        kappa = {m: sum(n['stated'][m] * n['move'] for n in res) / (sum(n['stated'][m] ** 2 for n in res) or 1)
                 for m in MEMBERS}
        sel = [sgn(n['pct_stated']) * n['move'] for n in res if n['selected']]
        R.update({'median_abs_realised_move': real,
                  'model_median_abs_move_pct': {m: st.median(n['abs_move'][m] for n in res if n['abs_move'][m]) for m in MEMBERS},
                  'k_magnitude': k, 'kappa': kappa,
                  'model_median_abs_stated': {m: st.median(abs(n['stated'][m]) for n in res) for m in MEMBERS},
                  'all_names_short': st.mean(-n['move'] for n in res),
                  'current_rule': {'n': len(sel), 'mean': st.mean(sel) if sel else None},
                  'curve': curve_of(res, 'pct_stated'),
                  'rows': [{kk: n[kk] for kk in ('date', 'ticker', 'selected', 'stated', 'abs_move',
                                                  'pct_stated', 'move', 'move_strategy')} for n in res]})
        doc['regions'][region] = R
        print(f"\n{region}: {len(names)} panel names, {len(res)} resolved over {len(R['days'])} days; "
              f"median |move| {real:.2f}%; kappa " + ', '.join(f"{m} {v:.2f}" for m, v in kappa.items())
              + f"; short every name {R['all_names_short']:+.2f}%; 3-of-4 rule n {len(sel)}"
              + (f" {R['current_rule']['mean']:+.2f}%" if sel else ''))
        for p in R['curve']:
            if p['n'] == len(res) or p['n'] % 5 == 0 or p['n'] <= 3:
                print(f"    |avg| >= {p['x']:5.2f}%  n {p['n']:2d} ({p['days']} d)  {p['mean']:+6.2f}%"
                      f"  se {p['se'] or 0:4.2f}  right {p['hit']:.0%}")
    json.dump(doc, open(OUT / 'panel-mean-pct.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
