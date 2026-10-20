#!/usr/bin/env python3
"""Does the panel do better on days with fewer names? (Xavier, 2026-10-20)

For every resolved panel name: the number of names the panel judged that day (n_day),
the signed return on the scorebord window (side x move) and |panel_pct|. Tests, per
sample, never pooled:
  - Spearman(n_day, signed return) over names, all and for |pct| >= 70 / >= 80;
    p from a DAY-BLOCK permutation (whole days' sizes shuffled), because names on one
    day share a market and a size.
  - thin (n_day <= median) against busy, Welch t, same subsets.
  - Spearman(n_day, |move|), to see whether thin days are simply different names.
"""
import json, math, random, statistics as st, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import day_rules as D  # noqa: E402
ER = D.ER


def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[o[j + 1]] == x[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spear(a, b):
    if len(a) < 3: return float('nan')
    ra, rb = rank(a), rank(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float('nan')


def perm_p(rows, key, draws=5000, seed=3):
    days = sorted({r['date'] for r in rows}); size = {d: rows_n[d] for d in days}
    obs = spear([size[r['date']] for r in rows], [r[key] for r in rows])
    rnd = random.Random(seed); k = 0; vals = list(size.values())
    for _ in range(draws):
        sh = vals[:]; rnd.shuffle(sh); m = dict(zip(days, sh))
        if abs(spear([m[r['date']] for r in rows], [r[key] for r in rows])) >= abs(obs) - 1e-12: k += 1
    return obs, (k + 1) / (draws + 1)


def welch(a, b):
    if len(a) < 2 or len(b) < 2: return float('nan')
    return (st.mean(a) - st.mean(b)) / math.sqrt(st.variance(a) / len(a) + st.variance(b) / len(b))


def report(rows, label):
    global rows_n
    by = defaultdict(list)
    for r in rows: by[r['date']].append(r)
    rows_n = {d: len(v) for d, v in by.items()}
    med = st.median(rows_n.values())
    for r in rows: r['absmove'] = abs(r['ret'])
    print(f"\n=== {label}: {len(rows)} names, {len(by)} days, names per day {sorted(rows_n.values())}, median {med} ===")
    out = {}
    for lab, sub in (('all', rows), ('|pct|>=70', [r for r in rows if abs(r['pct']) >= 70]),
                     ('|pct|>=80', [r for r in rows if abs(r['pct']) >= 80])):
        if len(sub) < 4:
            print(f"  {lab:10s} n {len(sub)}: too few"); continue
        rho, p = perm_p(sub, 'ret')
        thin = [r['ret'] for r in sub if rows_n[r['date']] <= med]; busy = [r['ret'] for r in sub if rows_n[r['date']] > med]
        ht = lambda x: 100 * sum(v > 0 for v in x) / len(x) if x else float('nan')
        print(f"  {lab:10s} n {len(sub):3d}  rho(n_day, return) {rho:+.2f} p {p:.2f}  | thin n {len(thin)} {st.mean(thin) if thin else float('nan'):+.2f}% "
              f"hit {ht(thin):.0f}%  busy n {len(busy)} {st.mean(busy) if busy else float('nan'):+.2f}% hit {ht(busy):.0f}%  t {welch(thin, busy):+.2f}")
        out[lab] = {'n': len(sub), 'rho': rho, 'p': p, 'thin_n': len(thin), 'busy_n': len(busy),
                    'thin_mean': st.mean(thin) if thin else None, 'busy_mean': st.mean(busy) if busy else None,
                    'thin_hit': ht(thin), 'busy_hit': ht(busy), 't': welch(thin, busy)}
    rho, p = perm_p(rows, 'absmove')
    print(f"  size of move: rho(n_day, |move|) {rho:+.2f} p {p:.2f}")
    out['abs_move'] = {'rho': rho, 'p': p}
    out['sizes'] = rows_n
    return out


def main():
    L = json.load(open(D.REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    frozen = json.load(open(D.REPO / 'dashboard/data/scorebord-frozen.json'))
    bt = json.load(open(HERE.parent / 'panel-mean-pct/panel-mean-pct.json'))['datasets']['backtest']['US']['rows']
    back = []
    for r in bt:
        mv = ER.sb_move(led.get((r['date'], r['ticker'])), frozen); p = r['comb']['impact_sum']['gemiddelde']
        if mv is not None and p: back.append({'date': r['date'], 'pct': p, 'ret': ER.sgn(p) * mv})
    v1, v2 = [], []
    for (d, t), (p, full) in ER.october_pcts().items():
        mv = ER.sb_move(led.get((d, t)), frozen)
        if mv is not None and p and full:
            (v1 if d <= '2026-10-09' else v2).append({'date': d, 'pct': p, 'ret': ER.sgn(p) * mv})
    res = {'backtest_opus5': report(back, 'Backtest re-judge (Opus 5 hunters; judges saw ~50 names per pack, not per day)'),
           'oktober_v1': report(v1, 'Live E-P us-searcher.v1'),
           'oktober_v2': report(v2, 'Live E-P us-searcher.v2')}
    json.dump(res, open(HERE / 'day-size.json', 'w'), indent=1, default=lambda x: None)


if __name__ == '__main__':
    main()
