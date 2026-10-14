#!/usr/bin/env python3
"""The four-model panel in each model's OWN percentiles, October only, per region.

Operator's design (2026-10-14): "10%" means the names in a model's own top 10%. The
threshold is the model's, not a shared number: Opus 5's top 10% might start at 1.8 and
Opus 5.5's at 0.9. That weighs the models fairly whatever scale each one sizes on, and a
future model joins without rescaling anyone else.

Per region and per model, the reference is every October panel name that model judged in
that region, resolved or not; no outcome is used. A name's percentile for a model is the
share of that reference with a smaller |size|, x 100 (a zero size scores 0), signed by
the model's sign. The panel's number is the mean of the four signed percentiles, so a
name every judge puts at its 95th percentile on the same side reads 95, and a name the
judges split on reads near zero. "Top X%" is every name with |mean| >= 100 - X, traded on
the sign of the mean, equal weight, gross. Each model on its own is computed the same way
for comparison.

Done twice: on `impact_sum` as the judge wrote it, and on `impact_scaled` =
(2 x p_up / 100 - 1) x abs_move_pct, recomputed from the judge's two inputs as
edge_score.py does. The US judges are told to make the two equal (config/panel-judge.md),
so there they mostly coincide; the market judges are not, and in Japan they differ.

US (operator, 2026-10-14): the strategy exit only (amc at the next opening print, bmo
at 20:00 CET, the ledger's `px.strategy`), from two entries: 19:30 CET (13:30 ET, the
ledger's half-hour price `enpx['1330']`) and the close before the print (`mv_strategy`).
Other regions have no strategy exit and no 19:30 entry: the panel the market stages run
since 2026-10-08, in each market's own resolver window. September Opus 5.5 hunts are out on the operator's instruction: every run read
here is October, after the shared core.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
"""
import bisect, glob, json, statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')
KEYS = ('impact_sum', 'impact_scaled')
TOPS = list(range(5, 101, 5))
REGIONS = {  # dir under research/<Y>/<M>/<D>/, the market resolver's file, label
    'US': ('edge-panel', None, 'Verenigde Staten (stage E-P)'),
    'EU': ('europe', 'eu-resolved.json', 'Europa (10 markten)'),
    'JP': ('japan', 'jp-resolved.json', 'Japan'),
    'AU': ('australia', 'au-resolved.json', 'Australië'),
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


def scaled(x):
    p, a = x.get('p_up'), x.get('abs_move_pct')
    return None if p is None or a is None else (2 * p / 100 - 1) * a


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
                e, x = (l.get('enpx') or {}).get('1330'), (l.get('px') or {}).get('strategy')
                moves = {'e1930': (x / e - 1) * 100 if e and x and not l.get('pending') else None,
                         'e2200': None if l.get('pending') else l.get('mv_strategy')}
            else:
                moves = {'market': mv.get(r['ticker'])}
            mem = r['members']
            names.append({'date': date, 'ticker': r['ticker'], 'selected': r['selected'],
                          'impact_sum': {m: mem[m]['impact_sum'] for m in MEMBERS},
                          'impact_scaled': {m: scaled(mem[m]) for m in MEMBERS},
                          'moves': moves})
    return names


def pct(ref_sorted, v):
    """share of the reference with a smaller |size|, x 100; a zero size scores 0."""
    if v is None or v == 0: return 0.0
    return 100.0 * bisect.bisect_left(ref_sorted, abs(v)) / len(ref_sorted)


def book(res, score, top, mk):
    v = [r for r in res if r['moves'].get(mk) is not None and score(r) and abs(score(r)) >= 100 - top]
    if not v: return None
    s = [sgn(score(r)) * r['moves'][mk] for r in v]
    return {'top': top, 'n': len(v), 'days': len({r['date'] for r in v}), 'mean': st.mean(s),
            'se': st.stdev(s) / len(s) ** .5 if len(s) > 1 else None, 'hit': sum(y > 0 for y in s) / len(s)}


def main():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    doc = {'generated_from': 'research/2026/10/*, October only', 'tops': TOPS, 'regions': {}}
    for region in REGIONS:
        names = load_region(region, led)
        mkeys = list(names[0]['moves']) if names else []
        res = [n for n in names if any(v is not None for v in n['moves'].values())]
        R = {'label': REGIONS[region][2], 'names': len(names), 'resolved': len(res),
             'days': sorted({n['date'] for n in res})}
        if len(res) < 5:
            R['note'] = 'fewer than five resolved names: nothing to read yet'
            doc['regions'][region] = R
            print(f"{region}: {len(names)} panel names, {len(res)} resolved, skipped")
            continue
        R['move_keys'] = mkeys
        R['all_names_short'], R['current_rule'] = {}, {}
        for mk in mkeys:
            v = [n for n in res if n['moves'][mk] is not None]
            sel = [sgn(sum(n['impact_sum'].values())) * n['moves'][mk] for n in v if n['selected']]
            R['all_names_short'][mk] = st.mean(-n['moves'][mk] for n in v)
            R['current_rule'][mk] = {'n': len(sel), 'mean': st.mean(sel) if sel else None}
            print(f"\n{region} [{mk}]: {len(names)} panel names (the percentile reference), {len(v)} resolved over "
                  f"{len({n['date'] for n in v})} days; short every name {R['all_names_short'][mk]:+.2f}%; 3-of-4 rule "
                  f"{len(sel)} names" + (f" {R['current_rule'][mk]['mean']:+.2f}%" if sel else ''))
        for key in KEYS:
            ref = {m: sorted(abs(n[key][m]) for n in names if n[key][m] is not None) for m in MEMBERS}
            thr = {m: {t: ref[m][min(len(ref[m]) - 1, int(len(ref[m]) * (1 - t / 100)))] for t in (10, 20, 30)}
                   for m in MEMBERS}
            for n in names:
                n.setdefault('pct', {})[key] = {m: round(sgn(n[key][m] or 0) * pct(ref[m], n[key][m]), 1) for m in MEMBERS}
                n.setdefault('panel', {})[key] = round(st.mean(n['pct'][key].values()), 1)
            K = {'threshold_at_top': thr, 'panel': {}, 'models': {}}
            for mk in mkeys:
                K['panel'][mk] = [b for t in TOPS if (b := book(res, lambda r: r['panel'][key], t, mk))]
                K['models'][mk] = {m: [b for t in TOPS if (b := book(res, lambda r, m=m: r['pct'][key][m], t, mk))]
                                   for m in MEMBERS}
            R[key] = K
            print(f"  {key}: own top-10% threshold " + ', '.join(f"{m} {thr[m][10]:.2f}" for m in MEMBERS))
            for mk in mkeys:
                for b in K['panel'][mk]:
                    if b['top'] in (10, 20, 30, 50, 100):
                        print(f"    [{mk}] top {b['top']:3d}%  n {b['n']:2d} ({b['days']} d)  {b['mean']:+6.2f}%"
                              f"  se {b['se'] or 0:4.2f}  right {b['hit']:.0%}")
        R['rows'] = [{k: n[k] for k in ('date', 'ticker', 'selected', 'impact_sum', 'impact_scaled', 'pct',
                                        'panel', 'moves')} for n in res]
        doc['regions'][region] = R
    json.dump(doc, open(OUT / 'panel-mean-pct.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
