#!/usr/bin/env python3
"""Second layer: what IS a low-sufficiency pack, and is the reliability effect an inverted U?

  python3 deep.py [--unseal]      # writes results/deep.json

1. What pack sufficiency and reliability track (coverage, volatility, turnover, size of
   the evidence, its source mix, the live conviction).
2. Hit rate by sufficiency WITHIN volatility halves and coverage groups, per judge: is
   the low-sufficiency edge more than "thin, volatile name"?
3. The source mix of each sufficiency x reliability quadrant.
4. Reliability and novelty as a dose-response curve (quintiles), item level, plus the
   same curve inside the focal-company items only.
5. The judges together: how many of the six calls (live, four re-judges, rated) got the
   sign, by quadrant.
"""
import argparse, json, os, statistics as st, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402


def r(x, n=3):
    return None if x is None else round(x, n)


def hit(e, c):
    return int(A.sgn(e['call'][c]) == A.sgn(e['move']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unseal', action='store_true')
    ap.add_argument('--perms', type=int, default=1000)
    a = ap.parse_args()
    events, items = A.load(a.unseal)
    names = [e for e in events if not e['duplicate_hunt'] and e['lab']]
    perm = A.Perm(events, a.perms)
    O = {}
    by_ev = defaultdict(list)
    for it in items:
        by_ev[it['event']].append(it)
    for e in names:
        its = by_ev[e['id']]
        src = [it for it in its if it['kind'] != 'listed_as_searched_and_found_nothing']
        e['n_items_src'] = len(src)
        e['share'] = {c: (sum(it['domain_class'] == c for it in src) / len(src)) if src else 0 for c in
                      ('sec_filing', 'newswire', 'retail_finance', 'company_site', 'major_press', 'trade_press', 'government_data', 'market_data')}
        e['share_claim'] = {c: (sum(it['claim_type'] == c for it in its) / len(its)) if its else 0 for c in
                            ('focal_primary', 'arithmetic', 'opinion_or_estimate', 'other_company_primary', 'macro_or_industry', 'absence', 'positioning_or_price')}
        e['mean_item_rel'] = st.mean([it['reliability'] for it in its if it['reliability'] is not None] or [0])
        e['suf'] = e['lab']['pack_sufficiency']
        e['rel'] = e['lab']['pack_reliability']
    ms, mr = st.median(e['suf'] for e in names), st.median(e['rel'] for e in names)
    for e in names:
        e['quad'] = f"suf_{'hi' if e['suf'] >= ms else 'lo'}/rel_{'hi' if e['rel'] >= mr else 'lo'}"

    # 1. what sufficiency / reliability track
    feats = {'coverage_thin': [int(e['lab']['coverage'] == 'thinly_covered') for e in names],
             'vol20': [e['vol20'] for e in names], 'log_turnover': [A.math.log10(max(e['dollar_vol'] or 1e4, 1e4)) for e in names],
             'n_items_with_source': [e['n_items_src'] for e in names], 'n_findings': [e['n_findings'] for e in names],
             'abs_live_impact': [abs(e['live_impact'] or 0) for e in names], 'implied_move': [e['implied_move'] for e in names],
             'bar_present': [int(e['bar_present']) for e in names], 'abs_move_over_priced': [abs(e['move_n']) for e in names]}
    feats.update({f'share_{k}': [e['share'][k] for e in names] for k in names[0]['share']})
    feats.update({f'claim_{k}': [e['share_claim'][k] for e in names] for k in names[0]['share_claim']})
    O['1_tracks'] = {lab: {f: r(A.spearman([e[lab] for e in names], v)) for f, v in feats.items()} for lab in ('suf', 'rel')}

    # 2. sufficiency within strata, per judge
    vcut = st.median(e['vol20'] for e in names if e['vol20'])
    strata = {'vol_hi': lambda e: e['vol20'] and e['vol20'] >= vcut, 'vol_lo': lambda e: e['vol20'] and e['vol20'] < vcut,
              'thin': lambda e: e['lab']['coverage'] == 'thinly_covered', 'not_thin': lambda e: e['lab']['coverage'] != 'thinly_covered'}
    O['2_suf_within_strata'] = {}
    for c in ('live', 'median4', 'sonnet', 'opus5', 'rated'):
        row = {}
        for s, f in strata.items():
            for half in ('lo', 'hi'):
                g = [e for e in names if f(e) and c in e['call'] and A.sgn(e['call'][c]) and ((e['suf'] < ms) == (half == 'lo'))]
                row[f'{s}/suf_{half}'] = f"{sum(hit(e, c) for e in g)}/{len(g)}"
        O['2_suf_within_strata'][c] = row

    # 3. source mix per quadrant
    O['3_quadrant_mix'] = {}
    for q in sorted({e['quad'] for e in names}):
        g = [e for e in names if e['quad'] == q]
        O['3_quadrant_mix'][q] = {'n': len(g), 'thin_share': r(st.mean(int(e['lab']['coverage'] == 'thinly_covered') for e in g)),
                                  'median_turnover_m': r(st.median((e['dollar_vol'] or 0) / 1e6 for e in g), 1),
                                  'median_vol20': r(st.median(e['vol20'] for e in g if e['vol20']), 1),
                                  'mean_items_with_source': r(st.mean(e['n_items_src'] for e in g), 1),
                                  'bar_present_share': r(st.mean(int(e['bar_present']) for e in g)),
                                  'mean_abs_move_over_priced': r(st.mean(abs(e['move_n']) for e in g)),
                                  **{f'share_{k}': r(st.mean(e['share'][k] for e in g)) for k in names[0]['share']},
                                  **{f'claim_{k}': r(st.mean(e['share_claim'][k] for e in g)) for k in names[0]['share_claim']}}

    # 4. dose-response over quintiles, item level
    def quint(vals):
        v = sorted(x for x in vals if x is not None)
        return [v[int(len(v) * k / 5)] for k in (1, 2, 3, 4)]

    def qof(x, cuts):
        return None if x is None else sum(x >= c for c in cuts)
    O['4_dose_response'] = {}
    directional = [it for it in items if A.sgn(it['direction'])]
    for k in ('reliability', 'novelty', 'obscurity', 'specificity', 'relevance', 'strength'):
        cuts = quint([it[k] for it in directional])
        for subset, pred in (('all', lambda it: True), ('focal_only', lambda it: it['focal']),
                             ('filed_findings', lambda it: it['kind'] == 'filed_by_first_hunter')):
            cells = A.item_cells([it for it in items if pred(it)], (lambda kk, cc: lambda it: f'Q{qof(it[kk], cc) + 1}' if it[kk] is not None else None)(k, cuts))
            fam = A.family(perm, cells)
            O['4_dose_response'][f'{k}/{subset}'] = {'cuts': cuts, **{q: {'n': v['n'], 'hit': r(v['hit_rate']), 'm': r(v.get('mean_signed_move_n')), 'z': r(v.get('z'))}
                                                                     for q, v in sorted(fam.items())}}
    # inverted U: mid (Q2-Q4) against the two tails, as one pre-specifiable contrast
    for k in ('reliability', 'novelty'):
        cuts = quint([it[k] for it in directional])
        mid = A.item_cells(items, lambda it: (None if it[k] is None else ('mid' if 1 <= qof(it[k], cuts) <= 3 else 'tails')))
        O['4_dose_response'][f'{k}/mid_vs_tails'] = {kk: {'n': v['n'], 'hit': r(v['hit_rate']), 'm': r(v.get('mean_signed_move_n')), 'z': r(v.get('z')), 'p': r(v.get('p'))}
                                                     for kk, v in A.family(perm, mid).items()}

    # 5. judges together
    calls = ('live', 'opus5', 'opus', 'sonnet', 'fable', 'rated')
    O['5_judges_together'] = {}
    for q in sorted({e['quad'] for e in names}):
        g = [e for e in names if e['quad'] == q and all(c in e['call'] for c in calls)]
        tot = [sum(hit(e, c) for c in calls if A.sgn(e['call'][c])) / max(1, sum(1 for c in calls if A.sgn(e['call'][c]))) for e in g]
        O['5_judges_together'][q] = {'n': len(g), 'mean_share_of_judges_right': r(st.mean(tot)) if tot else None}
    O['_medians'] = {'suf': ms, 'rel': mr, 'vol20': vcut}
    out = f"{HERE}/results/deep{'-unsealed' if a.unseal else ''}.json"
    json.dump(O, open(out, 'w'), indent=1, default=str)
    print(json.dumps(O, indent=1, default=str)[:20000])


if __name__ == '__main__':
    main()
