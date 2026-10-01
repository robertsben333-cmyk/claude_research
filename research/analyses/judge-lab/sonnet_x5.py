#!/usr/bin/env python3
"""Five independent Sonnet 5.5 re-judges of the same Opus 5-hunted evidence: does
self-consistency help?

Same brief as the four-model re-judge (`../rejudge-four-models/brief.md`), same packs,
five separate sessions per chunk (`sonnet-x5/out/s<k>-c<c>.json`). The question is
whether agreement WITHIN one model picks the top better than a single run, and how that
compares with agreement ACROSS four models (`ensemble.py`).

Arms, all scored on the 127 Opus 5-hunted development names, pooled top share within
bucket, net of the assumed cost:
- each single run s1..s5, and their spread (how much one run's luck matters);
- the original Sonnet re-judge from the four-model set (a sixth, earlier run);
- mean of five, and unanimous five sized by the weakest (self-consistency);
- the four-model unanimous ensemble, and that ensemble with Sonnet replaced by the
  five-run consensus.

  python3 sonnet_x5.py            (SONNET_RUNS=s1,s2,s3 for an interim read; writes nothing)
"""
import glob, json, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_lab as J
import ensemble as E

OUT = os.path.join(J.D, 'sonnet-x5', 'out')


def runs():
    key = {x['id']: x for x in json.load(open(J.KEY))}; back = {v.get('pid', k): k for k, v in key.items()}
    R = {}
    for f in sorted(glob.glob(f'{OUT}/s*-c*.json')):
        k = os.path.basename(f).split('-')[0]
        for o in json.load(open(f)):
            R.setdefault(k, {})[back.get(o['id'], o['id'])] = float(o.get('impact_sum') or 0)
    return R


def unanimous_min(vals):
    s = [J.sgn(v) for v in vals]
    return s[0] * min(abs(v) for v in vals) if all(x == s[0] != 0 for x in s) else 0.0


def main():
    rows = J.load(); F = J.make_folds(rows, json.load(open(J.SPLIT)))
    R = runs(); rej = J.rejudge_arms()
    only = [x for x in os.environ.get('SONNET_RUNS', '').split(',') if x]
    if only: R = {k: v for k, v in R.items() if k in only}
    if not R: sys.exit('no runs in sonnet-x5/out yet')
    have = [k for k in sorted(R)]
    dev = [r for r in rows if J.fold_of(r, F) is not None and r['hunter_model'] == 'opus5'
           and all(r['id'] in R[k] for k in have) and all(r['id'] in rej.get(m, {}) for m in E.MEMBERS)]
    arms = {m: rej[m] for m in E.MEMBERS}; arms['live'] = {r['id']: r['live'] for r in dev}
    for k in have: arms[k] = R[k]
    z = {m: E.scaled(arms[m], dev) for m in arms}
    cand = {'live': arms['live'], 'sonnet_original': arms['sonnet']}
    for k in have: cand[f'sonnet_{k}'] = arms[k]
    cand[f'sonnet_mean_{len(have)}'] = {r['id']: st.mean(z[k][r['id']] for k in have) for r in dev}
    cand[f'sonnet_unanimous_{len(have)}'] = {r['id']: unanimous_min([z[k][r['id']] for k in have]) for r in dev}
    cand['four_models_unanimous'] = {r['id']: unanimous_min([z[m][r['id']] for m in E.MEMBERS]) for r in dev}
    # four models, with Sonnet's single run replaced by the mean of its five runs
    for r in dev: z.setdefault('sonnet_mean', {})[r['id']] = cand[f'sonnet_mean_{len(have)}'][r['id']]
    cand['four_models_unanimous_sonnet_x5'] = {
        r['id']: unanimous_min([z[m][r['id']] for m in ('opus5', 'opus', 'fable', 'sonnet_mean')]) for r in dev}
    out = {'n': len(dev), 'runs': have, 'arms': {}}
    print(f"{len(dev)} Opus 5-hunted development names judged by all {len(have)} Sonnet runs and the four models")
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us')]:
        sub = [r for r in dev if f(r)]
        print(f"== {g} ({len(sub)})        {'top 10%':>16s} {'top 15%':>20s} {'top 20%':>16s}")
        singles = []
        for name, sc in cand.items():
            p = {r['id']: sc.get(r['id'], 0) or 0 for r in sub}; cells = []; res = {}
            for q in J.SHARES_REPORTED:
                m = J.top_metrics(sub, p, q); res[f'{q:.2f}'] = {k: v for k, v in m.items() if k != 'ids'}
                cells.append(f"{m['hits']:2d}/{m['n']:<2d} {m['net']:+6.2f}%" if m['n'] else '   -  ')
            J.TOP = 0.15; pp = J.perm_p(sub, p); res['perm_p_15'] = pp
            out['arms'].setdefault(name, {})[g] = res
            if name.startswith('sonnet_s'): singles.append(res['0.15']['net'])
            print(f"  {name:32s} {cells[0]:>14s} {cells[1]:>14s} p {pp:.2f} {cells[2]:>14s}")
        if len(singles) > 1:
            print(f"  single runs at 15%: mean {st.mean(singles):+.2f}%, range {min(singles):+.2f} to {max(singles):+.2f}")
            out['arms'].setdefault('_single_run_spread', {})[g] = {'mean': st.mean(singles), 'min': min(singles), 'max': max(singles)}
        # sign agreement between runs: how often two runs of the same model agree
    pairs = [(a, b) for i, a in enumerate(have) for b in have[i + 1:]]
    agree = [st.mean([J.sgn(R[a][r['id']]) == J.sgn(R[b][r['id']]) for r in dev]) for a, b in pairs]
    if agree:
        print(f"sign agreement between two Sonnet runs: mean {st.mean(agree):.0%} (range {min(agree):.0%}-{max(agree):.0%})")
        out['sign_agreement_between_runs'] = {'mean': st.mean(agree), 'min': min(agree), 'max': max(agree)}
    if not only: json.dump(out, open(os.path.join(J.D, 'sonnet-x5.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
