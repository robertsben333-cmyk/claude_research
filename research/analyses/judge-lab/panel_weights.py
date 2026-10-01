#!/usr/bin/env python3
"""How should a four-model panel's certainty and agreement set the size of a position?

The operator's design (2026-10-01): do not demand that all judges agree; use their
certainty and their agreement as factors in the expected move and the weight. This tests
the candidate rules on the four blind re-judges already on disk (Opus 5, Opus 5.5,
Sonnet 5.5, Fable 5.1), development names only, test set sealed.

Per name and model: the signed size z (impact_sum scaled within bucket, so models on
different scales are comparable) and the model's own certainty c = |p_up - 50| / 50,
standardised within that model (confidence scales are model-specific; CISC 2025).

Panel quantities: mu = mean z, sd = spread of z across the four (epistemic uncertainty
in the deep-ensemble sense), agree = |sum of signs| / 4, cert = mean standardised c.

Rules, each a signed score used both to RANK and to SIZE:
  mean            mu
  median          median z
  mean x agree    mu * agree
  precision       mu / (sd + tau), tau = median sd   (mean over its uncertainty)
  mean x cert     mu * (1 + cert / 2), floored at 0
  mean x agree x cert
  unanimous-min   the earlier rule: all four same sign, sized by the weakest

Scored three ways:
  1. top 15% pooled within bucket, traded equal-weight on the sign (selection);
  2. a book of ALL nonzero names each day weighted by the score (sizing): return =
     sum(w * r) / sum(|w|), per day, mean and t over days;
  3. calibration: Spearman of score with the move, and whether agreement and
     certainty predict that the panel's sign is right (hit rate by level).

  python3 panel_weights.py [--hunter opus5]
"""
import argparse, glob, json, math, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_lab as J
import ensemble as E


def judge_rows():
    """impact_sum and p_up per (model, id) from the four-model re-judge outputs."""
    key = {x['id']: x for x in json.load(open(J.KEY))}; back = {v.get('pid', k): k for k, v in key.items()}
    out = {}
    for f in glob.glob(f'{J.REJ}/out-*-*.json'):
        m = os.path.basename(f)[:-5].split('-')[-1]
        if m not in E.MEMBERS: continue
        for o in json.load(open(f)):
            i = back.get(o['id'], o['id'])
            out.setdefault(m, {})[i] = (float(o.get('impact_sum') or 0), J.num(o.get('p_up')))
    return out


def standardise(d):
    v = [x for x in d.values() if x is not None]
    mu, sd = st.mean(v), st.pstdev(v) or 1
    return {k: (0.0 if x is None else (x - mu) / sd) for k, x in d.items()}


def build(dev, JR):
    z = {m: E.scaled({i: JR[m][i][0] for i in JR[m]}, dev) for m in E.MEMBERS}
    c = {m: standardise({r['id']: (abs(JR[m][r['id']][1] - 50) / 50 if JR[m][r['id']][1] is not None else None) for r in dev})
         for m in E.MEMBERS}
    P = {}
    for r in dev:
        i = r['id']; xs = [z[m][i] for m in E.MEMBERS]
        P[i] = dict(mu=st.mean(xs), med=st.median(xs), sd=st.pstdev(xs),
                    agree=abs(sum(J.sgn(x) for x in xs)) / 4, cert=st.mean(c[m][i] for m in E.MEMBERS),
                    unan=(J.sgn(xs[0]) * min(map(abs, xs)) if all(J.sgn(x) == J.sgn(xs[0]) != 0 for x in xs) else 0.0))
    tau = st.median(p['sd'] for p in P.values()) or 1
    rules = {
        'mean': lambda p: p['mu'],
        'median': lambda p: p['med'],
        'mean x agree': lambda p: p['mu'] * p['agree'],
        'precision mu/(sd+tau)': lambda p: p['mu'] / (p['sd'] + tau),
        'mean x cert': lambda p: p['mu'] * max(0.0, 1 + p['cert'] / 2),
        'mean x agree x cert': lambda p: p['mu'] * p['agree'] * max(0.0, 1 + p['cert'] / 2),
        'unanimous-min': lambda p: p['unan'],
    }
    return P, {k: {i: f(P[i]) for i in P} for k, f in rules.items()}


def weighted_book(rows, w):
    days = {}
    for r in rows:
        if J.tradable(r) and w[r['id']] != 0: days.setdefault((r['region'], r['day']), []).append(r)
    per = []
    for v in days.values():
        g = sum(abs(w[r['id']]) for r in v)
        per.append(sum(w[r['id']] * r['move'] - abs(w[r['id']]) * J.cost(r) for r in v) / g)
    if len(per) < 3: return None
    return {'days': len(per), 'mean': st.mean(per), 't': st.mean(per) / (st.stdev(per) / len(per) ** .5)}


def hit_by(rows, P, key, cuts):
    out = []
    for lo, hi, lab in cuts:
        v = [r for r in rows if J.tradable(r) and P[r['id']]['mu'] != 0 and lo <= P[r['id']][key] < hi]
        if v:
            h = sum(J.sgn(P[r['id']]['mu']) * r['move'] > 0 for r in v)
            out.append((lab, len(v), h / len(v), st.mean(J.sgn(P[r['id']]['mu']) * r['move'] for r in v)))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--hunter', choices=['opus5', 'opus55']); a = ap.parse_args()
    rows = J.load(); F = J.make_folds(rows, json.load(open(J.SPLIT))); JR = judge_rows()
    dev = [r for r in rows if J.fold_of(r, F) is not None and (not a.hunter or r['hunter_model'] == a.hunter)
           and all(r['id'] in JR[m] for m in E.MEMBERS)]
    P, S = build(dev, JR)
    out = {'n': len(dev), 'hunter': a.hunter or 'all', 'rules': {}}
    print(f"{len(dev)} development names{' hunted by ' + a.hunter if a.hunter else ''}")
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us')]:
        sub = [r for r in dev if f(r)]
        print(f"== {g} ({len(sub)})        top-15% select       weighted book of all names    rho(score, move)")
        for name, sc in S.items():
            m = J.top_metrics(sub, sc, 0.15); b = weighted_book(sub, sc); rho = J.rho(sub, sc)
            out['rules'].setdefault(name, {})[g] = {'top15': {k: v for k, v in m.items() if k != 'ids'}, 'book': b, 'rho': rho}
            bb = f"{b['mean']:+.2f}%/day t {b['t']:+.2f} ({b['days']} d)" if b else '-'
            print(f"  {name:24s} {m['hits']:2d}/{m['n']:<2d} {m['net']:+6.2f}%     {bb:30s} {rho:+.3f}")
        print("  does agreement predict the panel's sign? (hit rate, mean signed move)")
        for lab, n, h, mv in hit_by(sub, P, 'agree', [(0.99, 2, '4 of 4 agree'), (0.49, 0.99, '3 of 4'), (0, 0.49, 'split')]):
            print(f"     {lab:14s} n {n:3d}  hit {h:.0%}  mean signed move {mv:+.2f}%")
        cs = sorted(P[r['id']]['cert'] for r in sub); t1, t2 = cs[len(cs) // 3], cs[2 * len(cs) // 3]
        print("  does the models' own certainty predict it?")
        for lab, n, h, mv in hit_by(sub, P, 'cert', [(t2, 99, 'high certainty'), (t1, t2, 'middle'), (-99, t1, 'low')]):
            print(f"     {lab:14s} n {n:3d}  hit {h:.0%}  mean signed move {mv:+.2f}%")
        ss = sorted(P[r['id']]['sd'] / (abs(P[r['id']]['mu']) + 1e-9) for r in sub if P[r['id']]['mu']); s1, s2 = ss[len(ss) // 3], ss[2 * len(ss) // 3]
        print("  does relative spread (sd / |mean|) predict it? (low spread = models agree on size too)")
        for r in sub: P[r['id']]['rel'] = P[r['id']]['sd'] / (abs(P[r['id']]['mu']) + 1e-9)
        for lab, n, h, mv in hit_by(sub, P, 'rel', [(-1, s1, 'low spread'), (s1, s2, 'middle'), (s2, 1e9, 'high spread')]):
            print(f"     {lab:14s} n {n:3d}  hit {h:.0%}  mean signed move {mv:+.2f}%")
    json.dump(out, open(os.path.join(J.D, f"panel-weights{'-' + a.hunter if a.hunter else ''}.json"), 'w'), indent=1)


if __name__ == '__main__':
    main()
