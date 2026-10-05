#!/usr/bin/env python3
"""Fourth layer: is the no-anchor / low-sufficiency edge drift, luck or one day?

  python3 checks.py [--unseal]     # writes results/checks.json
"""
import argparse, json, os, random, statistics as st, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402
J = A.J


def r(x, n=3):
    return None if x is None else round(x, n)


def book(g, pred):
    rows = [{'id': e['id'], 'region': 'us', 'day': e['day'], 'move': e['move'], 'dv': e['dollar_vol'] or 0} for e in g]
    return J.top_metrics(rows, pred, 0.2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unseal', action='store_true')
    ap.add_argument('--perms', type=int, default=2000)
    a = ap.parse_args()
    events, _ = A.load(a.unseal)
    names = [e for e in events if not e['duplicate_hunt'] and e['lab']]
    ms = 42.5  # the discovery median, frozen
    for e in names:
        e['suf_lo'] = e['lab']['pack_sufficiency'] < ms
        e['no_anchor'] = e['implied_move'] is None
    calls = ('live', 'median4', 'sonnet', 'opus5', 'opus', 'fable', 'rated')
    O = {}
    # 1. drift: direction of moves and of calls, per group; free controls
    O['1_drift'] = {}
    for lab, f in (('no_anchor', lambda e: e['no_anchor']), ('anchor', lambda e: not e['no_anchor']),
                   ('suf_lo', lambda e: e['suf_lo']), ('suf_hi', lambda e: not e['suf_lo'])):
        g = [e for e in names if f(e)]
        row = {'n': len(g), 'share_moves_up': r(st.mean(int(e['move'] > 0) for e in g)),
               'mean_move': r(st.mean(e['move'] for e in g), 2),
               'short_all_hits': f"{sum(e['move'] < 0 for e in g)}/{len(g)}",
               'neg_runup20_hits': f"{sum(A.sgn(-(e['runup_20d'] or 0)) == A.sgn(e['move']) for e in g if e['runup_20d'])}/{sum(1 for e in g if e['runup_20d'])}"}
        for c in calls:
            gg = [e for e in g if c in e['call'] and A.sgn(e['call'][c])]
            row[f'{c}_share_calls_up'] = r(st.mean(int(e['call'][c] > 0) for e in gg)) if gg else None
            row[f'{c}_hits'] = f"{sum(A.sgn(e['call'][c]) == A.sgn(e['move']) for e in gg)}/{len(gg)}"
            # hits when the call goes AGAINST the group's majority move direction
            maj = 1 if st.mean(int(e['move'] > 0) for e in g) >= .5 else -1
            ag = [e for e in gg if A.sgn(e['call'][c]) != maj]
            row[f'{c}_hits_against_majority'] = f"{sum(A.sgn(e['call'][c]) == A.sgn(e['move']) for e in ag)}/{len(ag)}"
        O['1_drift'][lab] = row
    # 2. permutation: within-day shuffle of moves; contrasts in hit rate and in the top-20% book
    days = defaultdict(list)
    for e in names:
        days[e['perm_day']].append(e)
    rnd = random.Random(A.SEED)

    def stat(mv):
        out = {}
        for c in ('median4', 'live', 'sonnet', 'rated'):
            g = [e for e in names if c in e['call'] and A.sgn(e['call'][c])]
            h = lambda grp: st.mean(int(A.sgn(e['call'][c]) == A.sgn(mv[e['id']])) for e in grp) if grp else 0
            out[f'{c}:hit_no_anchor_minus_anchor'] = h([e for e in g if e['no_anchor']]) - h([e for e in g if not e['no_anchor']])
            out[f'{c}:hit_suflo_minus_sufhi'] = h([e for e in g if e['suf_lo']]) - h([e for e in g if not e['suf_lo']])
            bl = book([{**e, 'move': mv[e['id']]} for e in names if e['suf_lo'] and c in e['call']], {e['id']: e['call'][c] for e in names if e['suf_lo'] and c in e['call']})['net']
            bh = book([{**e, 'move': mv[e['id']]} for e in names if not e['suf_lo'] and c in e['call']], {e['id']: e['call'][c] for e in names if not e['suf_lo'] and c in e['call']})['net']
            out[f'{c}:book_suflo_minus_sufhi'] = (bl or 0) - (bh or 0)
        return out
    obs = stat({e['id']: e['move'] for e in names})
    null = defaultdict(list)
    for _ in range(a.perms):
        mv = {}
        for g in days.values():
            sh = [e['move'] for e in g]
            rnd.shuffle(sh)
            mv.update({e['id']: m for e, m in zip(g, sh)})
        for k, v in stat(mv).items():
            null[k].append(v)
    O['2_permutation'] = {k: {'obs': r(v), 'p_one_sided': r((1 + sum(x >= v for x in null[k])) / (1 + a.perms))} for k, v in obs.items()}
    # 3. stability: by hunter model and leave-one-day-out of the median4 suf_lo book
    O['3_by_hunter_model'] = {}
    for m in ('Opus 5', 'Opus 5.5'):
        for half in (True, False):
            g = [e for e in names if e['hunter_model'] == m and e['suf_lo'] == half and 'median4' in e['call']]
            gg = [e for e in g if A.sgn(e['call']['median4'])]
            O['3_by_hunter_model'][f"{m}/{'suf_lo' if half else 'suf_hi'}"] = {
                'n': len(g), 'median4_hits': f"{sum(A.sgn(e['call']['median4']) == A.sgn(e['move']) for e in gg)}/{len(gg)}",
                'no_anchor_share': r(st.mean(int(e['no_anchor']) for e in g)) if g else None}
    lo = [e for e in names if e['suf_lo'] and 'median4' in e['call']]
    full = book(lo, {e['id']: e['call']['median4'] for e in lo})
    O['3_lodo_median4_suf_lo'] = {'full': {k: r(full[k]) if isinstance(full[k], float) else full[k] for k in ('n', 'hits', 'net')}}
    for d in sorted({e['perm_day'] for e in lo}):
        g = [e for e in lo if e['perm_day'] != d]
        m = book(g, {e['id']: e['call']['median4'] for e in g})
        O['3_lodo_median4_suf_lo'][f'without {d}'] = {'n': m['n'], 'hits': m['hits'], 'net': r(m['net'])}
    O['3_picks'] = [{'id': e['id'], 'suf': e['lab']['pack_sufficiency'], 'no_anchor': e['no_anchor'], 'call': r(e['call']['median4'], 2),
                     'move': r(e['move'], 2), 'turnover_m': r((e['dollar_vol'] or 0) / 1e6, 2)} for e in lo if e['id'] in set(full['ids'])]
    out = f"{HERE}/results/checks{'-unsealed' if a.unseal else ''}.json"
    json.dump(O, open(out, 'w'), indent=1)
    print(json.dumps(O, indent=1))


if __name__ == '__main__':
    main()
