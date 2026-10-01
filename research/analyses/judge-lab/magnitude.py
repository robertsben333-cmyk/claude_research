#!/usr/bin/env python3
"""Do the names a judge is surest about actually move the most? Sign ignored.

The operator's question (2026-10-01): not whether the direction is right, but whether the
highest-conviction names are the ones that really move, and whether aggregating several
judges sharpens that. So every arm here is ranked on |score| alone and scored on the
realised |move|.

The trap is volatility: a judge that puts the jumpiest names on top 'predicts' size
without knowing anything the market does not. So two free controls rank on what was
known before the print: the event-implied move (or, without an option chain, the median
past reaction), and the 20-day realised volatility. A judge earns something only where
it beats those, and the cleanest test is the move scaled by what the market expected
(`|move| / expected`), where a vol-picker scores nothing.

Per arm, pooled within bucket (US or not x before/after 09-23), development names only:
  top15_abs     mean |move| of the top 15% by |score|
  lift          that divided by the bucket's mean |move| (1.0 = no better than random)
  big_hit       share of those picks that are among the bucket's top 15% movers
  rho_abs       within-day Spearman of |score| against |move|
  rho_surprise  within-day Spearman of |score| against |move| / expected

  python3 magnitude.py [--hunter opus5|opus55]
"""
import argparse, json, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_lab as J
import ensemble as E
import sonnet_x5 as S

SHARE = 0.15


def expected(r):
    return r['implied'] or r['hist'] or None


def day_rho(rows, score, target):
    days = {}
    for r in rows:
        t = target(r)
        if t is not None: days.setdefault((r['region'], r['day']), []).append((abs(score[r['id']]), t))
    num, den = 0, 0
    for v in days.values():
        if len(v) < 3: continue
        a, b = J.rank([x for x, _ in v]), J.rank([y for _, y in v])
        ma, mb = st.mean(a), st.mean(b); d = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** .5
        if d: num += len(v) * sum((x - ma) * (y - mb) for x, y in zip(a, b)) / d; den += len(v)
    return num / den if den else None


def top_stats(rows, score, share=SHARE):
    B = {}
    for r in rows:
        if J.tradable(r): B.setdefault(J.bucket(r), []).append(r)
    picks, base, big = [], [], 0
    for v in B.values():
        k = max(1, round(share * len(v)))
        top = sorted(v, key=lambda r: (-abs(score[r['id']]), r['id']))[:k]
        movers = {r['id'] for r in sorted(v, key=lambda r: -abs(r['move']))[:k]}
        picks += top; base += v; big += sum(r['id'] in movers for r in top)
    m = st.mean(abs(r['move']) for r in picks); b = st.mean(abs(r['move']) for r in base)
    sp = [abs(r['move']) / expected(r) for r in picks if expected(r)]
    sb = [abs(r['move']) / expected(r) for r in base if expected(r)]
    return {'n': len(picks), 'top15_abs': m, 'all_abs': b, 'lift': m / b, 'big_hit': big / len(picks),
            'surprise_lift': (st.mean(sp) / st.mean(sb)) if sp and sb else None}


def perm_lift(rows, score, n=500):
    """Within-day shuffles of |score|: how often a random top 15% lifts as much."""
    o = top_stats(rows, score)['lift']; days = {}
    for r in rows: days.setdefault((r['region'], r['day']), []).append(r['id'])
    rnd = J.random.Random(J.SEED); hit = 0
    for _ in range(n):
        p = {}
        for ids in days.values():
            v = [score[i] for i in ids]; rnd.shuffle(v); p.update(zip(ids, v))
        hit += top_stats(rows, p)['lift'] >= o
    return hit / n


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--hunter', choices=['opus5', 'opus55']); a = ap.parse_args()
    rows = J.load(); F = J.make_folds(rows, json.load(open(J.SPLIT)))
    rej = J.rejudge_arms(); R = S.runs()
    dev = [r for r in rows if J.fold_of(r, F) is not None and (not a.hunter or r['hunter_model'] == a.hunter)
           and all(r['id'] in rej.get(m, {}) for m in E.MEMBERS)]
    if R and a.hunter == 'opus5':   # the five Sonnet runs cover the Opus 5-hunted names
        dev = [r for r in dev if all(r['id'] in R[k] for k in R)]
    with_x5 = bool(R) and all(all(r['id'] in R[k] for r in dev) for k in R)
    arms = {m: rej[m] for m in E.MEMBERS}; arms['live'] = {r['id']: r['live'] for r in dev}
    if with_x5:
        for k in R: arms[k] = R[k]
    z = {m: E.scaled(arms[m], dev) for m in arms}
    absz = lambda ms: {r['id']: [abs(z[m][r['id']]) for m in ms] for r in dev}
    cand = {
        'control: implied move': {r['id']: expected(r) or 0 for r in dev},
        'control: 20d volatility': {r['id']: r['vol'] or 0 for r in dev},
        'live |impact_sum|': arms['live'],
        **{f'single {m}': arms[m] for m in E.MEMBERS},
        'four models: mean |x|': {i: st.mean(v) for i, v in absz(E.MEMBERS).items()},
        'four models: median |x|': {i: st.median(v) for i, v in absz(E.MEMBERS).items()},
        'four models: weakest |x|': {i: min(v) for i, v in absz(E.MEMBERS).items()},
        'four models + live: mean |x|': {i: st.mean(v) for i, v in absz(E.MEMBERS + ['live']).items()},
    }
    if with_x5:
        ks = sorted(R)
        for k in ks: cand[f'sonnet {k}'] = arms[k]
        cand['sonnet x5: mean |x|'] = {i: st.mean(v) for i, v in absz(ks).items()}
        cand['sonnet x5: weakest |x|'] = {i: min(v) for i, v in absz(ks).items()}
        cand['all nine judges: mean |x|'] = {i: st.mean(v) for i, v in absz(E.MEMBERS + ks).items()}
    out = {'n': len(dev), 'hunter': a.hunter or 'all', 'share': SHARE, 'arms': {}}
    print(f"{len(dev)} development names{' hunted by ' + a.hunter if a.hunter else ''}; ranked on |score| only")
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us')]:
        sub = [r for r in dev if f(r)]
        print(f"== {g} ({len(sub)})   top-15% mean|move|  lift  p     big-mover hit  surprise-lift  rho|move|  rho|move|/expected")
        for name, sc in cand.items():
            sc = {r['id']: sc.get(r['id'], 0) or 0 for r in sub}
            t = top_stats(sub, sc); p = perm_lift(sub, sc)
            ra = day_rho(sub, sc, lambda r: abs(r['move']))
            rs = day_rho(sub, sc, lambda r: abs(r['move']) / expected(r) if expected(r) else None)
            out['arms'].setdefault(name, {})[g] = {**t, 'lift_perm_p': p, 'rho_abs': ra, 'rho_surprise': rs}
            f2 = lambda x: '   -' if x is None else f'{x:+.2f}'
            print(f"  {name:30s} {t['top15_abs']:6.2f}% (all {t['all_abs']:5.2f})  {t['lift']:.2f}  {p:.2f}   {t['big_hit']:5.0%}          {t['surprise_lift'] or 0:.2f}       {f2(ra)}      {f2(rs)}")
    json.dump(out, open(os.path.join(J.D, f"magnitude{'-' + a.hunter if a.hunter else ''}.json"), 'w'), indent=1)


if __name__ == '__main__':
    main()
