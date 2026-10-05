#!/usr/bin/env python3
"""Third layer: why low-sufficiency names get the sign right more often, and whether it pays.

  python3 mechanism.py [--unseal]     # writes results/mechanism.json

Splits by turnover tercile, by whether an option chain priced the move, and by what the
realised move was against what was priced; and runs each judge's top-20% book inside the
low- and high-sufficiency halves, net of judge-lab's cost table.
"""
import argparse, json, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402
J = A.J


def r(x, n=3):
    return None if x is None else round(x, n)


def hits(g, c):
    g = [e for e in g if c in e['call'] and A.sgn(e['call'][c])]
    return f"{sum(A.sgn(e['call'][c]) == A.sgn(e['move']) for e in g)}/{len(g)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unseal', action='store_true')
    a = ap.parse_args()
    events, _ = A.load(a.unseal)
    names = [e for e in events if not e['duplicate_hunt'] and e['lab']]
    ms = st.median(e['lab']['pack_sufficiency'] for e in names)
    for e in names:
        e['suf_lo'] = e['lab']['pack_sufficiency'] < ms
    dv = sorted(e['dollar_vol'] or 0 for e in names)
    t1, t2 = dv[len(dv) // 3], dv[2 * len(dv) // 3]
    calls = ('live', 'median4', 'sonnet', 'opus5', 'opus', 'fable', 'rated')
    O = {'_cuts': {'suf_median': ms, 'turnover_terciles_usd': [t1, t2]}}
    # 1. turnover tercile x sufficiency
    O['1_turnover_x_suf'] = {}
    for lab, f in (('dv_low', lambda e: (e['dollar_vol'] or 0) < t1), ('dv_mid', lambda e: t1 <= (e['dollar_vol'] or 0) < t2), ('dv_high', lambda e: (e['dollar_vol'] or 0) >= t2)):
        for half in (True, False):
            g = [e for e in names if f(e) and e['suf_lo'] == half]
            O['1_turnover_x_suf'][f"{lab}/{'suf_lo' if half else 'suf_hi'}"] = {'n': len(g), **{c: hits(g, c) for c in calls}}
    # 2. option chain or not
    O['2_anchor'] = {}
    for lab, f in (('option_implied', lambda e: e['implied_move'] is not None), ('no_option_anchor', lambda e: e['implied_move'] is None)):
        for half in (True, False):
            g = [e for e in names if f(e) and e['suf_lo'] == half]
            O['2_anchor'][f"{lab}/{'suf_lo' if half else 'suf_hi'}"] = {
                'n': len(g), 'mean_abs_move_over_priced': r(st.mean(abs(e['move_n']) for e in g)) if g else None,
                'median_abs_move_over_priced': r(st.median(abs(e['move_n']) for e in g)) if g else None, **{c: hits(g, c) for c in calls}}
    # 3. was the move bigger than priced? (ex post, descriptive only)
    O['3_move_vs_priced'] = {}
    for lab, f in (('inside_priced', lambda e: abs(e['move_n']) <= 1), ('beyond_priced', lambda e: abs(e['move_n']) > 1)):
        for half in (True, False):
            g = [e for e in names if f(e) and e['suf_lo'] == half]
            O['3_move_vs_priced'][f"{lab}/{'suf_lo' if half else 'suf_hi'}"] = {'n': len(g), **{c: hits(g, c) for c in calls}}
    # 4. each judge's top-20% book inside each half, net of cost (judge-lab cost table)
    O['4_books_by_half'] = {}
    for c in calls:
        for half in (True, False):
            g = [e for e in names if e['suf_lo'] == half and c in e['call']]
            rows = [{'id': e['id'], 'region': 'us', 'day': e['day'], 'move': e['move'], 'dv': e['dollar_vol'] or 0} for e in g]
            m = J.top_metrics(rows, {e['id']: e['call'][c] for e in g}, 0.2)
            O['4_books_by_half'][f"{c}/{'suf_lo' if half else 'suf_hi'}"] = {k: r(m[k]) if isinstance(m[k], float) else m[k] for k in ('n', 'hits', 'mean', 'net', 't')}
    # 5. the low-sufficiency half: what share is even tradable, and at what turnover
    lo = [e for e in names if e['suf_lo']]
    hi = [e for e in names if not e['suf_lo']]
    O['5_capacity'] = {h: {'n': len(g), 'tradable_200k': sum(e['tradable'] for e in g), 'over_1m': sum((e['dollar_vol'] or 0) >= 1e6 for e in g),
                           'over_5m': sum((e['dollar_vol'] or 0) >= 5e6 for e in g), 'median_turnover_m': r(st.median((e['dollar_vol'] or 0) / 1e6 for e in g), 2),
                           'option_chain': sum(e['implied_move'] is not None for e in g)} for h, g in (('suf_lo', lo), ('suf_hi', hi))}
    out = f"{HERE}/results/mechanism{'-unsealed' if a.unseal else ''}.json"
    json.dump(O, open(out, 'w'), indent=1)
    print(json.dumps(O, indent=1))


if __name__ == '__main__':
    main()
