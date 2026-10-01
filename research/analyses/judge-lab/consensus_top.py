#!/usr/bin/env python3
"""Consensus at the top: names that EVERY member of a group puts in its own top 20%.

The operator's question (2026-10-01): what if we only take the names all five judges
rank in their top 20%? Each member ranks the names on |score| within its bucket (US or
not x before/after 09-23) and keeps its top 20%; a name is selected when at least k of
the n members kept it (k = n is full consensus). The side is the sign of the members'
mean scaled score, and the table also reports how often they agreed on it.

Groups, on the Opus 5-hunted development names (the five Sonnet runs cover those):
  sonnet x5       the five Sonnet 5.5 runs (same model, five samples)
  four models     Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1 (one run each)
  four + live     the four models and the live hunt's impact_sum
For each selection: names, sign agreement, hits / net return per pick, mean |move|,
lift over the bucket's mean |move|, and the share that are real top-15% movers.

  python3 consensus_top.py
"""
import json, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_lab as J
import ensemble as E
import sonnet_x5 as S
import magnitude as M

TOP = 0.20


def top_sets(rows, z, members):
    """Per member, the ids in its own top 20% by |score| within each bucket (zeros never)."""
    B = {}
    for r in rows:
        if J.tradable(r): B.setdefault(J.bucket(r), []).append(r)
    sets = {m: set() for m in members}
    for v in B.values():
        k = max(1, round(TOP * len(v)))
        for m in members:
            ranked = sorted((r for r in v if z[m][r['id']] != 0), key=lambda r: (-abs(z[m][r['id']]), r['id']))
            sets[m] |= {r['id'] for r in ranked[:k]}
    return sets


def evaluate(rows, picks, z, members):
    if not picks: return None
    B = {}
    for r in rows:
        if J.tradable(r): B.setdefault(J.bucket(r), []).append(r)
    movers, base = set(), []
    for v in B.values():
        k = max(1, round(0.15 * len(v)))
        movers |= {r['id'] for r in sorted(v, key=lambda r: -abs(r['move']))[:k]}; base += v
    by = {r['id']: r for r in rows}; P = [by[i] for i in picks]
    side = {i: J.sgn(st.mean(z[m][i] for m in members)) for i in picks}
    agree = sum(len({J.sgn(z[m][i]) for m in members}) == 1 for i in picks)
    ret = [side[r['id']] * r['move'] - J.cost(r) for r in P if side[r['id']]]
    mabs = st.mean(abs(r['move']) for r in P); babs = st.mean(abs(r['move']) for r in base)
    return {'n': len(P), 'sign_unanimous': agree, 'hits': sum(x > 0 for x in ret), 'traded': len(ret),
            'net': st.mean(ret) if ret else None, 'mean_abs_move': mabs, 'lift': mabs / babs,
            'big_movers': sum(r['id'] in movers for r in P) / len(P), 'ids': sorted(picks)}


def main():
    rows = J.load(); F = J.make_folds(rows, json.load(open(J.SPLIT)))
    rej = J.rejudge_arms(); R = S.runs(); ks = sorted(R)
    dev = [r for r in rows if J.fold_of(r, F) is not None and r['hunter_model'] == 'opus5'
           and all(r['id'] in rej.get(m, {}) for m in E.MEMBERS) and all(r['id'] in R[k] for k in ks)]
    arms = {m: rej[m] for m in E.MEMBERS}; arms['live'] = {r['id']: r['live'] for r in dev}
    for k in ks: arms[k] = R[k]
    z = {m: E.scaled(arms[m], dev) for m in arms}
    groups = {'sonnet x5': ks, 'four models': E.MEMBERS, 'four + live': E.MEMBERS + ['live']}
    out = {'n': len(dev), 'top_share_per_member': TOP, 'groups': {}}
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us')]:
        sub = [r for r in dev if f(r)]
        print(f"== {g} ({len(sub)} Opus 5-hunted development names; each member keeps its own top {TOP:.0%})")
        print(f"  {'group':12s} {'in top20 of':>11s} {'names':>5s} {'same sign':>9s} {'hits':>7s} {'net/pick':>9s} {'mean|move|':>10s} {'lift':>5s} {'big movers':>10s}")
        for name, members in groups.items():
            sets = top_sets(sub, z, members)
            for k in range(len(members), 0, -1):
                picks = {i for i in set().union(*sets.values()) if sum(i in s for s in sets.values()) >= k}
                e = evaluate(sub, picks, z, members)
                out['groups'].setdefault(name, {}).setdefault(g, {})[f'{k}_of_{len(members)}'] = e
                if not e: print(f"  {name:12s} {f'>={k} of {len(members)}':>11s}     0"); continue
                net = '-' if e['net'] is None else f"{e['net']:+.2f}%"
                print(f"  {name:12s} {f'>={k} of {len(members)}':>11s} {e['n']:5d} {e['sign_unanimous']:5d}/{e['n']:<3d} {e['hits']:3d}/{e['traded']:<3d} {net:>9s} {e['mean_abs_move']:9.2f}% {e['lift']:5.2f} {e['big_movers']:9.0%}")
    json.dump(out, open(os.path.join(J.D, 'consensus-top.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
