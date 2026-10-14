#!/usr/bin/env python3
"""The four-model panel in each model's OWN percentiles, per region, on two samples,
with and without a penalty for disagreement.

Operator's design (2026-10-14): "10%" means the names in a model's own top 10%. The
threshold is the model's, not a shared number: Opus 5's top 10% might start at 1.8 and
Opus 5.5's at 0.9. That weighs the models fairly whatever scale each one sizes on, and a
future model joins without rescaling anyone else.

Two samples:

- `oktober`: the live panels. US stage E-P, and the panel the market stages run since
  2026-10-08. Every run read is October, after the shared core.
- `backtest`: the blind four-model re-judge of every resolved hunt to 2026-09-30
  (research/analyses/rejudge-four-models/), the same four models judging the evidence the
  live hunters collected, without web access. The September Opus 5.5 hunts are left out
  (operator's instruction; the ledger's and markets.json's `sept_opus55` flag), which
  leaves the Opus 5-era hunts of 2026-08-31 to 2026-09-22. 42 names quoted in CLAUDE.md
  or an agent file were judged anonymised (`leak`); they are kept and flagged.

Per sample, region and model, the reference is every name that model judged there; no
outcome is used. A name's percentile for a model is the share of that reference with a
smaller |size|, x 100 (a zero size scores 0), signed by the model's sign. Four ways to
combine the four signed percentiles, all read on the same scale so "top X%" is always
|score| >= 100 - X:

- `gemiddelde`: the mean. The rule the operator asked for.
- `eensgezind`: the mean, but 0 unless all four give the same nonzero sign.
- `zwakste`: if all four agree on the sign, the smallest |percentile|; else 0. "Top 10%"
  is then: every model puts the name in its own top 10%, the consensus rule taken to 4/4.
- `gem_min_spreiding`: the mean shrunk toward zero by the spread (population sd) of the
  four percentiles: sign(mean) x max(0, |mean| - sd).

Done on `impact_sum` as the judge wrote it and on `impact_scaled` = (2 x p_up / 100 - 1)
x abs_move_pct. In the backtest and for the US judges the two are equal by the judges'
contract; for the market judges they are not.

Return per name: traded on the sign of the score, equal weight, gross. US: the strategy
exit only (amc at the next opening print, bmo at 20:00 CET, the ledger's `px.strategy`),
entered at 19:30 CET (13:30 ET, `enpx['1330']`) and at the close (`mv_strategy`). Other
regions: each market's own resolver window; there is no strategy exit there.

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
"""
import bisect, glob, json, statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
REJ = REPO / 'research/analyses/rejudge-four-models'
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')
REJ_MODEL = {'opus5': 'opus5', 'opus': 'opus55', 'sonnet': 'sonnet55', 'fable': 'fable51'}
KEYS = ('impact_sum', 'impact_scaled')
TOPS = list(range(5, 101, 5))
LABEL = {'US': 'Verenigde Staten', 'EU': 'Europa', 'JP': 'Japan', 'AU': 'Australië', 'CA': 'Canada'}
LIVE = {  # dir under research/<Y>/<M>/<D>/, the market resolver's file
    'US': ('edge-panel', None), 'EU': ('europe', 'eu-resolved.json'), 'JP': ('japan', 'jp-resolved.json'),
    'AU': ('australia', 'au-resolved.json'), 'CA': ('canada', 'canada-resolved.json')}
REJ_REGION = {'us': 'US', 'europe': 'EU', 'japan': 'JP', 'australia': 'AU'}


def sgn(x): return (x > 0) - (x < 0)


def move_of(row):
    for k in ('realised_move_pct', 'move_pct', 'realised_move'):
        if row.get(k) is not None:
            return row[k]
    return None


def scaled(p, a):
    return None if p is None or a is None else (2 * p / 100 - 1) * a


def us_moves(l):
    if not l or l.get('pending'): return {'e1930': None, 'e2200': None}
    e, x = (l.get('enpx') or {}).get('1330'), (l.get('px') or {}).get('strategy')
    return {'e1930': (x / e - 1) * 100 if e and x else None, 'e2200': l.get('mv_strategy')}


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


def load_october(led):
    out = {}
    for region, (sub, fname) in LIVE.items():
        names = []
        for run in sorted(glob.glob(str(REPO / f'research/2026/10/*/{sub}'))):
            pf = Path(run) / 'edge-scores-panel.json'
            if not pf.exists(): continue
            date = Path(run).parent.name
            mv = {} if region == 'US' else market_moves(run, fname, region, date)
            for r in json.load(open(pf))['ranking']:
                mem = r['members']
                if not all(m in mem for m in MEMBERS): continue
                names.append({'date': date, 'ticker': r['ticker'], 'selected': r['selected'], 'leak': None,
                              'impact_sum': {m: mem[m]['impact_sum'] for m in MEMBERS},
                              'impact_scaled': {m: scaled(mem[m].get('p_up'), mem[m].get('abs_move_pct')) for m in MEMBERS},
                              'moves': us_moves(led.get((date, r['ticker']))) if region == 'US'
                              else {'market': mv.get(r['ticker'])}})
        out[region] = names
    return out


def load_backtest(led, mk_idx):
    key = {x['id']: x for x in json.load(open(REJ / 'key.json'))}
    back = {v.get('pid', k): k for k, v in key.items()}
    judged = {}
    for f in glob.glob(str(REJ / 'out-*-*.json')):
        m = REJ_MODEL.get(Path(f).stem.split('-')[-1])
        if not m: continue
        for o in json.load(open(f)):
            judged.setdefault(back.get(o['id'], o['id']), {})[m] = o
    out = {}
    for i, k in key.items():
        region = REJ_REGION.get(k['region'])
        j = judged.get(i, {})
        if not region or not all(m in j for m in MEMBERS): continue
        row = led.get((k['day'], k['ticker'])) if region == 'US' else mk_idx.get((k['day'], k['ticker']))
        if row is None or row.get('sept_opus55'): continue
        out.setdefault(region, []).append({
            'date': k['day'], 'ticker': k['ticker'], 'selected': None, 'leak': k.get('leak'),
            'impact_sum': {m: float(j[m].get('impact_sum') or 0) for m in MEMBERS},
            'impact_scaled': {m: scaled(j[m].get('p_up'), j[m].get('abs_move_pct')) for m in MEMBERS},
            'moves': us_moves(row) if region == 'US' else {'market': k.get('move')}})
    return out


def pct(ref_sorted, v):
    """share of the reference with a smaller |size|, x 100; a zero size scores 0."""
    if v is None or v == 0: return 0.0
    return 100.0 * bisect.bisect_left(ref_sorted, abs(v)) / len(ref_sorted)


def combine(p):
    v = list(p.values())
    mu, sd = st.mean(v), st.pstdev(v)
    unan = len({sgn(x) for x in v}) == 1 and sgn(v[0]) != 0
    return {'gemiddelde': mu, 'eensgezind': mu if unan else 0.0,
            'zwakste': sgn(v[0]) * min(abs(x) for x in v) if unan else 0.0,
            'gem_min_spreiding': sgn(mu) * max(0.0, abs(mu) - sd), 'spreiding': sd}


VARIANTS = ('gemiddelde', 'eensgezind', 'zwakste', 'gem_min_spreiding')


def book(res, score, top, mk):
    v = [r for r in res if r['moves'].get(mk) is not None and score(r) and abs(score(r)) >= 100 - top]
    if not v: return None
    s = [sgn(score(r)) * r['moves'][mk] for r in v]
    return {'top': top, 'n': len(v), 'days': len({r['date'] for r in v}), 'mean': st.mean(s),
            'se': st.stdev(s) / len(s) ** .5 if len(s) > 1 else None, 'hit': sum(y > 0 for y in s) / len(s)}


def split(res, key, mk, top):
    """Inside the mean's top X%: the half that agrees most against the half that agrees least."""
    v = [r for r in res if r['moves'].get(mk) is not None and abs(r['comb'][key]['gemiddelde']) >= 100 - top
         and r['comb'][key]['gemiddelde']]
    if len(v) < 6: return None
    med = st.median(r['comb'][key]['spreiding'] for r in v)
    out = {'top': top, 'median_spread': med}
    for lab, g in (('weinig_spreiding', [r for r in v if r['comb'][key]['spreiding'] <= med]),
                   ('veel_spreiding', [r for r in v if r['comb'][key]['spreiding'] > med])):
        s = [sgn(r['comb'][key]['gemiddelde']) * r['moves'][mk] for r in g]
        out[lab] = {'n': len(s), 'mean': st.mean(s) if s else None, 'hit': sum(y > 0 for y in s) / len(s) if s else None,
                    'se': st.stdev(s) / len(s) ** .5 if len(s) > 1 else None}
    return out


def region_doc(names, label):
    mkeys = list(names[0]['moves']) if names else []
    res = [n for n in names if any(v is not None for v in n['moves'].values())]
    R = {'label': label, 'names': len(names), 'resolved': len(res), 'days': sorted({n['date'] for n in res}),
         'leaked': sum(1 for n in res if n['leak'])}
    if len(res) < 5:
        R['note'] = 'fewer than five resolved names: nothing to read yet'
        return R
    R['move_keys'] = mkeys
    R['all_names_short'] = {mk: st.mean(-n['moves'][mk] for n in res if n['moves'][mk] is not None) for mk in mkeys}
    if any(n['selected'] is not None for n in res):
        R['current_rule'] = {}
        for mk in mkeys:
            s = [sgn(sum(n['impact_sum'].values())) * n['moves'][mk] for n in res if n['selected'] and n['moves'][mk] is not None]
            R['current_rule'][mk] = {'n': len(s), 'mean': st.mean(s) if s else None}
    for key in KEYS:
        ref = {m: sorted(abs(n[key][m]) for n in names if n[key][m] is not None) for m in MEMBERS}
        thr = {m: {t: ref[m][min(len(ref[m]) - 1, int(len(ref[m]) * (1 - t / 100)))] for t in (10, 20, 30)} for m in MEMBERS}
        for n in names:
            p = {m: round(sgn(n[key][m] or 0) * pct(ref[m], n[key][m]), 1) for m in MEMBERS}
            n.setdefault('pct', {})[key] = p
            n.setdefault('comb', {})[key] = {k: round(v, 1) for k, v in combine(p).items()}
        R[key] = {'threshold_at_top': thr,
                  'variants': {var: {mk: [b for t in TOPS if (b := book(res, lambda r, var=var: r['comb'][key][var], t, mk))]
                                     for mk in mkeys} for var in VARIANTS},
                  'models': {m: [b for t in TOPS if (b := book(res, lambda r, m=m: r['pct'][key][m], t, mkeys[0]))]
                             for m in MEMBERS},
                  'split': {mk: [s for t in (20, 30, 50) if (s := split(res, key, mk, t))] for mk in mkeys}}
    R['rows'] = [{k: n[k] for k in ('date', 'ticker', 'selected', 'leak', 'impact_sum', 'impact_scaled', 'pct',
                                    'comb', 'moves')} for n in res]
    return R


def main():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    mk_idx = {}
    for v in json.load(open(REPO / 'dashboard/data/markets.json'))['markets'].values():
        for r in v['names']:
            mk_idx[(r.get('run_date'), r['ticker'])] = r
    doc = {'tops': TOPS, 'variants': VARIANTS, 'datasets': {}}
    for ds, data in (('oktober', load_october(led)), ('backtest', load_backtest(led, mk_idx))):
        doc['datasets'][ds] = {}
        for region in LABEL:
            R = region_doc(data.get(region, []), LABEL[region])
            doc['datasets'][ds][region] = R
            if 'note' in R:
                print(f"{ds} {region}: {R['names']} names, {R['resolved']} resolved, skipped"); continue
            mk = R['move_keys'][0]
            print(f"\n{ds} {region} [{mk}]: {R['resolved']} names over {len(R['days'])} days; "
                  f"short every name {R['all_names_short'][mk]:+.2f}%")
            for var in VARIANTS:
                cells = []
                for t in (10, 20, 30, 50, 100):
                    b = next((x for x in R['impact_sum']['variants'][var][mk] if x['top'] == t), None)
                    cells.append(f"top{t:3d} " + (f"{b['n']:3d} {b['mean']:+6.2f}%" if b else '  -        '))
                print(f"  {var:18s} " + ' | '.join(cells))
            for s in R['impact_sum']['split'][mk]:
                a, b = s['weinig_spreiding'], s['veel_spreiding']
                print(f"  top {s['top']}% split by spread: low {a['n']} {a['mean']:+.2f}% ({a['hit']:.0%})"
                      f"  high {b['n']} {b['mean']:+.2f}% ({b['hit']:.0%})")
    json.dump(doc, open(OUT / 'panel-mean-pct.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
