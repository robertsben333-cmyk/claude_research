#!/usr/bin/env python3
"""Score the reliability / sufficiency ratings exactly as RATINGS-PREREG.md fixed them.

  python3 ratings.py            # reads runs/rated-{train,val,test}-{0,1}/, writes results/ratings.json
"""
import json, math, os, re, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'judge-lab'))
import judge_lab as J  # noqa: E402

SPLITS = ('train', 'val', 'test')
ROLE = {'train': 'train days', 'val': 'gate days', 'test': 'readout days'}
T_SUPPORT = 2.4


def parse(r):
    try:
        return json.loads(r.get('predicted_answer') or '')
    except (TypeError, ValueError):
        return {}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def spearman(a, b):
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(p) < 4:
        return None
    ra, rb = J.rank([x for x, _ in p]), J.rank([y for _, y in p])
    ma, mb = st.mean(ra), st.mean(rb)
    d = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / d if d else None


def welch(a, b):
    if len(a) < 2 or len(b) < 2:
        return None
    se = (st.variance(a) / len(a) + st.variance(b) / len(b)) ** .5
    return (st.mean(a) - st.mean(b)) / se if se else None


def load():
    names = {}
    for sp in SPLITS:
        items = {i['id']: i for i in json.load(open(f'{HERE}/data/{sp}/items.json'))}
        for k in (0, 1):
            f = f'{HERE}/runs/rated-{sp}-{k}/rollouts.json'
            for r in json.load(open(f)):
                it = items[r['id']]
                n = names.setdefault(it['name_id'], {'split': sp, 'item': it, 'runs': []})
                j = parse(r)
                n['runs'].append({'impact': r['impact_sum'], 'p_up': num(j.get('p_up')),
                                  'rel': num(j.get('evidence_reliability')),
                                  'suf': num(j.get('evidence_sufficiency')), 'gap': j.get('key_gap')})
    rows = []
    for nid, n in names.items():
        it, R = n['item'], n['runs']
        o, pack = it['outcome'], it['pack']
        mean = lambda k: st.mean([x[k] for x in R if x[k] is not None]) if any(x[k] is not None for x in R) else None
        ev = pack.get('evidence') or []
        srcs = [e.get('source') or '' for e in ev]
        rows.append({
            'id': nid, 'region': 'us', 'day': o['day'], 'move': o['move_pct'], 'dv': o['dollar_vol'],
            'split': n['split'], 'impact': mean('impact') or 0.0, 'p_up': mean('p_up'),
            'rel': mean('rel'), 'suf': mean('suf'),
            'rel_ab': [x['rel'] for x in R], 'suf_ab': [x['suf'] for x in R], 'impact_ab': [x['impact'] for x in R],
            'gaps': [x['gap'] for x in R],
            'n_items': len(ev), 'sec_share': (sum('sec.gov' in s for s in srcs) / len(srcs)) if srcs else 0.0,
            'vol': num(((pack.get('baseline') or {}).get('tape') or {}).get('realised_vol_20d_annualised_pct')),
            'log_dv': math.log10(max(o['dollar_vol'], 1e4)),
        })
    return rows


def book_split(rows, key, med):
    pred = {r['id']: r['impact'] for r in rows}
    m = J.top_metrics(rows, pred, 0.20)
    by = {r['id']: r for r in rows}
    hi, lo = [], []
    for i in m['ids']:
        r = by[i]
        net = J.sgn(r['impact']) * r['move'] - J.cost(r)
        (hi if r[key] is not None and r[key] >= med else lo).append(net)
    t = welch(hi, lo)
    return {'picks': m['n'], 'book_net': m['net'],
            'above': {'n': len(hi), 'net': st.mean(hi) if hi else None},
            'below': {'n': len(lo), 'net': st.mean(lo) if lo else None},
            'gap': (st.mean(hi) - st.mean(lo)) if hi and lo else None, 't': t}


def sign_split(rows, key, med):
    v = [r for r in rows if r['impact']]
    hi = [int(J.sgn(r['impact']) == J.sgn(r['move'])) for r in v if r[key] is not None and r[key] >= med]
    lo = [int(J.sgn(r['impact']) == J.sgn(r['move'])) for r in v if r[key] is None or r[key] < med]
    p1, p2 = (st.mean(hi) if hi else None), (st.mean(lo) if lo else None)
    t = None
    if hi and lo:
        p = (sum(hi) + sum(lo)) / (len(hi) + len(lo))
        se = (p * (1 - p) * (1 / len(hi) + 1 / len(lo))) ** .5
        t = (p1 - p2) / se if se else None
    return {'above': f'{sum(hi)}/{len(hi)}', 'below': f'{sum(lo)}/{len(lo)}',
            'gap_pts': (p1 - p2) * 100 if hi and lo else None, 't': t}


def verdict(gap, t, practical):
    if gap is None or t is None:
        return 'n/a'
    if gap > 0 and t >= T_SUPPORT:
        return 'supported'
    if gap > 0 and gap >= practical:
        return 'possible, more data'
    return 'not supported'


def main():
    rows = load()
    med = {k: st.median([r[k] for r in rows if r[k] is not None]) for k in ('suf', 'rel')}
    out = {'n_names': len(rows), 'medians': med}
    h1, h2, h3 = book_split(rows, 'suf', med['suf']), book_split(rows, 'rel', med['rel']), sign_split(rows, 'suf', med['suf'])
    h1['verdict'] = verdict(h1['gap'], h1['t'], 3.0)
    h2['verdict'] = verdict(h2['gap'], h2['t'], 3.0)
    h3['verdict'] = verdict(h3['gap_pts'], h3['t'], 10.0)
    out['H1_sufficiency_book'], out['H2_reliability_book'], out['H3_sufficiency_sign'] = h1, h2, h3
    out['H3b_reliability_sign'] = sign_split(rows, 'rel', med['rel'])

    out['reproducibility'] = {k: spearman([r[f'{k}_ab'][0] for r in rows], [r[f'{k}_ab'][1] for r in rows])
                              for k in ('suf', 'rel', 'impact')}
    feats = {'abs_impact': [abs(r['impact']) for r in rows],
             'conviction': [abs(r['p_up'] - 50) if r['p_up'] is not None else None for r in rows],
             'n_items': [r['n_items'] for r in rows], 'sec_share': [r['sec_share'] for r in rows],
             'vol_20d': [r['vol'] for r in rows], 'log_turnover': [r['log_dv'] for r in rows]}
    out['redundancy'] = {k: {f: spearman([r[k] for r in rows], v) for f, v in feats.items()} for k in ('suf', 'rel')}
    out['redundancy']['suf_vs_rel'] = spearman([r['suf'] for r in rows], [r['rel'] for r in rows])
    out['views'] = sum(1 for r in rows if r['impact'])
    out['book_all'] = {k: J.top_metrics(rows, {r['id']: r['impact'] for r in rows}, 0.20)[k] for k in ('n', 'hits', 'net', 't')}

    # combined filter
    pred = {r['id']: r['impact'] for r in rows}
    ids = set(J.top_metrics(rows, pred, 0.20)['ids'])
    both = [r for r in rows if r['id'] in ids and r['suf'] >= med['suf'] and r['rel'] >= med['rel']]
    out['combined_filter'] = {'n': len(both), 'hits': sum(J.sgn(r['impact']) == J.sgn(r['move']) for r in both),
                              'net': st.mean(J.sgn(r['impact']) * r['move'] - J.cost(r) for r in both) if both else None}

    # per role
    out['by_role'] = {}
    for sp in SPLITS:
        rr = [r for r in rows if r['split'] == sp]
        out['by_role'][ROLE[sp]] = {'n': len(rr), 'H1': book_split(rr, 'suf', med['suf']),
                                    'H2': book_split(rr, 'rel', med['rel']), 'H3': sign_split(rr, 'suf', med['suf'])}

    # does asking change the sizing? (gate + readout names, where seed runs exist)
    seed = {}
    for sp in ('val', 'test'):
        items = {i['id']: i['name_id'] for i in json.load(open(f'{HERE}/data/{sp}/items.json'))}
        for k in (0, 1):
            for r in json.load(open(f'{HERE}/runs/seed-{sp}-{k}/rollouts.json')):
                seed.setdefault(items[r['id']], []).append(r['impact_sum'] or 0.0)
    common = [r for r in rows if r['id'] in seed]
    sp_pred = {r['id']: st.mean(seed[r['id']]) for r in common}
    out['vs_seed'] = {'n': len(common),
                      'spearman_impact': spearman([r['impact'] for r in common], [sp_pred[r['id']] for r in common]),
                      'views_rated': sum(1 for r in common if r['impact']),
                      'views_seed': sum(1 for r in common if sp_pred[r['id']]),
                      'book_rated': {k: J.top_metrics(common, {r['id']: r['impact'] for r in common}, 0.2)[k] for k in ('n', 'hits', 'net')},
                      'book_seed': {k: J.top_metrics(common, sp_pred, 0.2)[k] for k in ('n', 'hits', 'net')}}
    out['example_gaps'] = [g for r in rows[:12] for g in r['gaps'][:1]]
    os.makedirs(f'{HERE}/results', exist_ok=True)
    json.dump(out, open(f'{HERE}/results/ratings.json', 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ('by_role', 'example_gaps')}, indent=1, default=str))
    for k, v in out['by_role'].items():
        print(k, json.dumps(v, default=str))


if __name__ == '__main__':
    main()
