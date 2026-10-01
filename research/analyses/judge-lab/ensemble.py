#!/usr/bin/env python3
"""Ensembles of the judges that already exist, scored on the development names only.

The forecasting literature's most robust result is that aggregating several independent
forecasters beats picking the best single one (Schoenegger et al. 2024, Halawi et al.
2024), that agreement between samples is a better confidence signal than a model's own
stated confidence, and that a learned linear aggregator can beat a plain average when the
members' errors differ. This tests all three on judgements already on disk, at no model
cost: four blind re-judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) and the live hunt.

Every member is scaled within its bucket (US or not x before/after 09-23) before it is
combined, because the members size on different scales. The test set stays sealed.

  python3 ensemble.py
"""
import json, math, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_lab as J

MEMBERS = ['opus5', 'opus', 'sonnet', 'fable']


def scaled(arm, rows):
    """Score divided by the bucket's root-mean-square, so a 1 means 'typical size here'."""
    out, by = {}, {}
    for r in rows: by.setdefault(J.bucket(r), []).append(r)
    for v in by.values():
        q = (sum(arm[r['id']] ** 2 for r in v) / len(v)) ** .5 or 1
        for r in v: out[r['id']] = arm[r['id']] / q
    return out


def ensembles(rows, arms):
    z = {m: scaled(arms[m], rows) for m in arms}
    E = {}
    for r in rows:
        i = r['id']; xs = [z[m][i] for m in MEMBERS]; s = [J.sgn(x) for x in xs]
        E.setdefault('mean_4', {})[i] = st.mean(xs)
        E.setdefault('median_4', {})[i] = st.median(xs)
        E.setdefault('mean_4_plus_live', {})[i] = st.mean(xs + [z['live'][i]])
        # agreement as the confidence: how many of four point the same way, then size
        net = sum(s)
        E.setdefault('vote_then_size', {})[i] = net + (st.median(xs) / 100 if net else 0)
        # unanimous only: all four nonzero and the same sign, sized by the weakest of them
        E.setdefault('unanimous_min', {})[i] = (s[0] * min(abs(x) for x in xs)
                                                 if all(v == s[0] != 0 for v in s) else 0.0)
        # unanimous four AND the live hunt agrees
        lv = J.sgn(z['live'][i])
        E.setdefault('unanimous_5_min', {})[i] = (s[0] * min(abs(x) for x in xs + [z['live'][i]])
                                                   if all(v == s[0] != 0 for v in s) and lv == s[0] else 0.0)
    return E, z


class Stacked:
    """Learned linear aggregator (logistic on the sign of the move, ridge-penalised),
    refit on every training fold. Five weights on ~150 names: expect it to overfit."""
    def __init__(self, z, lam=20.0): self.z, self.lam, self.name = z, lam, 'stacked_logit'
    def feats(self, r): return [self.z[m][r['id']] for m in MEMBERS + ['live']]
    def fit(self, train):
        self.w = J.logistic([self.feats(r) for r in train], [1.0 if r['move'] > 0 else 0.0 for r in train], self.lam)
        return self
    def score(self, r): return 1 / (1 + math.exp(-J.dot(self.w, self.feats(r)))) - 0.5


def main():
    rows = J.load(); F = J.make_folds(rows, json.load(open(J.SPLIT)))
    rej = J.rejudge_arms()
    dev = [r for r in rows if J.fold_of(r, F) is not None and all(r['id'] in rej.get(m, {}) for m in MEMBERS)]
    arms = {m: rej[m] for m in MEMBERS}; arms['live'] = {r['id']: r['live'] for r in dev}
    E, z = ensembles(dev, arms)
    cand = {'live': arms['live'], **{f'single_{m}': arms[m] for m in MEMBERS}, **E}
    st_pred = J.lodo(Stacked(z), dev); cand['stacked_logit (lodo)'] = st_pred
    for j in ('rubric', 'casebook', 'learned'):
        cand[f'judge_{j}'] = J.load_judge(j)
    out = {'n': len(dev), 'members': MEMBERS, 'rows': {}}
    print(f"{len(dev)} development names, every member present; pooled top share within bucket, net of assumed cost")
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us'), ('ex_us', lambda r: r['region'] != 'us')]:
        sub = [r for r in dev if f(r)]
        print(f"== {g} ({len(sub)})       {'top 10%':>18s} {'top 15%':>22s} {'top 20%':>18s}   picks at 15%")
        for name, sc in cand.items():
            p = {r['id']: sc.get(r['id'], 0) or 0 for r in sub}; cells = []; res = {}
            for q in J.SHARES_REPORTED:
                m = J.top_metrics(sub, p, q); res[f'{q:.2f}'] = {k: v for k, v in m.items() if k != 'ids'}
                cells.append(f"{m['hits']:2d}/{m['n']:<2d} {m['net']:+6.2f}%" if m['n'] else '   -  ')
            J.TOP = 0.15; pp = J.perm_p(sub, p); res['perm_p_15'] = pp
            out['rows'].setdefault(name, {})[g] = res
            print(f"  {name:22s} {cells[0]:>14s} {cells[1]:>16s} p {pp if pp is None else round(pp, 2)!s:>4s} {cells[2]:>14s}")
    json.dump(out, open(os.path.join(J.D, 'ensemble.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
