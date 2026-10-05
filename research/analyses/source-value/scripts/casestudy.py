#!/usr/bin/env python3
"""Phase 5: where the hunt gets large caps right.

  python3 scripts/casestudy.py hits     # step 1: lists ONLY the right calls (casestudy/hits.json + per-print evidence digests)
  python3 scripts/casestudy.py test     # step 4: scores the frozen rules (casestudy/rules.json) on every print not used
                                        #         to derive them: the large-cap misses, the no-view large caps, the mid caps

Step 1 deliberately prints nothing about the misses, so the descriptions in casestudy/HITS.md
(step 2) and the rules in casestudy/rules.json (step 3) are written, and committed, before
the misses are looked at.

A "view" is a non-zero live impact_sum or four-model median. A print is a HIT for a caller
when the sign is right AND |move| > half the priced move.
"""
import json, os, statistics as st, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402

OUT = f'{SV}/casestudy'


def callers(e):
    out = {}
    if e.get('live_impact'):
        out['live'] = e['live_impact']
    rj = e.get('rejudge') or {}
    four = [rj[k]['impact_sum'] for k in ('opus5', 'opus', 'sonnet', 'fable') if k in rj and rj[k].get('impact_sum') is not None]
    if len(four) == 4 and st.median(four) != 0:
        out['median4'] = st.median(four)
    return out


def is_hit(e, v):
    return core.sgn(v) * e['move'] > 0 and abs(e['move']) > 0.5 * e['priced_move']


def digest(e, items):
    its = [x for x in items if x['ev']['id'] == e['id'] and x['kind'] != 'listed_as_searched_and_found_nothing']
    return [{'i': x['i'], 'kind': x['kind'], 'subtype': x['subtype'], 'vote': x['vote'], 'quantified': x['quantified'],
             'dated_in_window': x['dated_in_window'], 'primary_document': x['primary_document'],
             'already_widely_reported': x['already_widely_reported'], 'magnitude_claim': x['magnitude_claim'],
             'live_size': x.get('live_size'), 'text': (x.get('text') or '')[:400]} for x in its]


def cmd_hits():
    E, I = core.load()
    A = [e for e in E if e['stratum'] == 'A']
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for band in ('large', 'mid'):
        hits = []
        for e in A:
            if e['cap_band'] != band:
                continue
            cs = callers(e)
            hc = [c for c, v in cs.items() if is_hit(e, v)]
            if hc:
                hits.append({'id': e['id'], 'ticker': e['ticker'], 'company': e['company'], 'sector': e['sector'], 'session': e['session'],
                             'day': e['day'], 'market_cap': e['market_cap'], 'move': e['move'], 'priced_move': e['priced_move'],
                             'option_anchor': e['option_anchor'], 'right_callers': hc, 'calls': cs, 'evidence': digest(e, I)})
        res[band] = hits
        # only the count of prints with a view is shown, not which ones missed
        res[band + '_n_with_view'] = sum(1 for e in A if e['cap_band'] == band and callers(e))
    json.dump(res, open(f'{OUT}/hits.json', 'w'), indent=1, ensure_ascii=False, default=str)
    for band in ('large', 'mid'):
        print(band, 'hits', len(res[band]), 'of', res[band + '_n_with_view'], 'with a view')
        for h in res[band]:
            print(' ', h['ticker'], h['day'], h['session'], round(h['move'], 1), '/', round(h['priced_move'], 1), h['right_callers'],
                  Counter(x['subtype'] for x in h['evidence'] if x['vote']).most_common(4))


def rule_fires(rule, e, items):
    """A rule is {id, when: {item filter}, min_items, call: 'vote'|'+'|'-'}; returns a sign or 0."""
    import questions as QQ
    its = [x for x in items if x['ev']['id'] == e['id'] and QQ.match(x, rule['when'])]
    if len(its) < rule.get('min_items', 1):
        return 0
    if rule.get('call') in ('+', '-'):
        return 1 if rule['call'] == '+' else -1
    net = sum(x['vote'] for x in its)
    return core.sgn(net)


def cmd_test():
    E, I = core.load()
    rules = json.load(open(f'{OUT}/rules.json'))
    used = set(rules['derived_from'])
    A = [e for e in E if e['stratum'] == 'A']
    out = {'rules': []}
    for r in rules['rules']:
        rows = {}
        for scope, sel in (('large_not_used', [e for e in A if e['cap_band'] == 'large' and e['id'] not in used]),
                           ('mid_not_used', [e for e in A if e['cap_band'] == 'mid' and e['id'] not in used]),
                           ('small_micro', [e for e in A if e['cap_band'] in ('small', 'micro')]),
                           ('used_for_derivation', [e for e in A if e['id'] in used])):
            calls = [(e, rule_fires(r, e, I)) for e in sel]
            calls = [(e, c) for e, c in calls if c]
            rows[scope] = {'fires': len(calls), 'of': len(sel), 'right': sum(c * e['move'] > 0 for e, c in calls),
                           'mean_signed_move_n': st.mean([c * e['y']['strategy'] for e, c in calls]) if calls else None,
                           'mean_signed_res_n': st.mean([c * e['res']['strategy'] for e, c in calls]) if calls else None,
                           'tickers': [f"{e['ticker']}:{'+' if c * e['move'] > 0 else '-'}" for e, c in calls]}
        out['rules'].append({'id': r['id'], 'text': r['text'], 'scores': rows})
    json.dump(out, open(f'{OUT}/rules-test.json', 'w'), indent=1)
    for r in out['rules']:
        print(r['id'], {k: (v['fires'], v['right'], None if v['mean_signed_res_n'] is None else round(v['mean_signed_res_n'], 2)) for k, v in r['scores'].items()})


if __name__ == '__main__':
    {'hits': cmd_hits, 'test': cmd_test}[sys.argv[1]]()
