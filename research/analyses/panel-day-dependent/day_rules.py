#!/usr/bin/env python3
"""May the panel's selection depend on the day? (operator, 2026-10-14)

Question: on a day with many candidates be stricter, on a day with few also take names
at a panel percentile of 50, 60 or 70. How would that have done?

The rules are FIXED HERE, before any of them was scored, and every one is reported:

  vast80          |pct| >= 80 (the live stage E-P rule)
  aanvul K/F      >= 80, and if the day has fewer than K such names, top up with the
                  next-highest |pct| down to a floor F. K in {2, 3}, F in {50, 60, 70}
  topK K/F        exactly the K highest names of the day, none below F (so a busy day
                  is capped, a thin day is filled). K = 3, F in {50, 60, 70}
  staffel         threshold by the number of names the panel judged that day:
                  >= 12 names: 85, 7-11: 80, 4-6: 70, <= 3: 60

Window: the scorebord's (BUY 13:30 ET on the run day; amc out at the next open, bmo out
at 13:00 ET on the report day), via panel-mean-pct/expected_return.sb_move. Gross.

Two levels, because they answer different questions:
- per call: mean side x move over all selected names, hit rate, t.
- per day (the account): every trading day's book is the equal-weight mean of what it
  selected, fully deployed, and a day with nothing selected earns 0. Mean over ALL days.
  Topping up a thin day lowers the per-call average almost by construction; the account
  number is where it could pay, because that capital was idle otherwise.

Samples are kept apart (never pooled): the blind backtest re-judge of the Opus 5-era
hunts (one version), and the live October E-P runs split by searcher version
(us-searcher.v1 to 10-09, v2 from 10-12).

  python3 research/analyses/panel-day-dependent/day_rules.py
"""
import json, math, random, statistics as st, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'panel-mean-pct'))
import expected_return as ER  # noqa: E402

RULES = [('vast80', None)] + [(f'aanvul {k}/{f}', ('fill', k, f)) for k in (2, 3) for f in (50, 60, 70)] \
        + [(f'top{3}/{f}', ('top', 3, f)) for f in (50, 60, 70)] + [('staffel', ('staffel',))]


def select(day_rows, rule):
    rs = sorted(day_rows, key=lambda r: -abs(r['pct']))
    base = [r for r in rs if abs(r['pct']) >= 80]
    if rule is None:
        return base
    if rule[0] == 'fill':
        _, k, f = rule
        if len(base) >= k:
            return base
        return [r for r in rs if abs(r['pct']) >= f][:max(k, len(base))]
    if rule[0] == 'top':
        _, k, f = rule
        return [r for r in rs if abs(r['pct']) >= f][:k]
    n = len(day_rows)
    thr = 85 if n >= 12 else 80 if n >= 7 else 70 if n >= 4 else 60
    return [r for r in rs if abs(r['pct']) >= thr]


def tstat(x):
    if len(x) < 2 or st.pstdev(x) == 0:
        return float('nan')
    return st.mean(x) / (st.stdev(x) / math.sqrt(len(x)))


def p_two(t, n):
    # normal approximation; with n < 30 read it as rough
    return math.erfc(abs(t) / math.sqrt(2)) if t == t else float('nan')


def evaluate(rows, label):
    by = defaultdict(list)
    for r in rows:
        by[r['date']].append(r)
    days = sorted(by)
    sizes = [len(by[d]) for d in days]
    print(f"\n=== {label}: {len(rows)} names over {len(days)} days "
          f"(names per day median {st.median(sizes)}, min {min(sizes)}, max {max(sizes)}) ===")
    print(f"{'regel':14s} {'calls':>5s} {'dagen':>5s} {'goed':>6s} {'per call':>9s} {'t':>5s}"
          f" {'per dag':>8s} {'t':>5s} {'vs vast80':>9s} {'t':>5s} {'p':>5s}  extra namen")
    out = {}
    base_day = None
    base_ids = None
    for name, rule in RULES:
        calls, dayret, picked = [], [], set()
        for d in days:
            sel = select(by[d], rule)
            calls += [r['ret'] for r in sel]
            picked |= {(r['date'], r['ticker']) for r in sel}
            dayret.append(st.mean(r['ret'] for r in sel) if sel else 0.0)
        if rule is None:
            base_day, base_ids = dayret, picked
        diff = [a - b for a, b in zip(dayret, base_day)]
        extra = [r['ret'] for r in rows if (r['date'], r['ticker']) in picked - base_ids]
        dropped = [r['ret'] for r in rows if (r['date'], r['ticker']) in base_ids - picked]
        hit = sum(c > 0 for c in calls) / len(calls) if calls else float('nan')
        td = tstat(diff) if any(diff) else float('nan')
        res = {'calls': len(calls), 'days_traded': sum(1 for d in days if select(by[d], rule)),
               'hit': hit, 'per_call': st.mean(calls) if calls else None, 't_call': tstat(calls),
               'per_day': st.mean(dayret), 't_day': tstat(dayret),
               'vs_fixed_per_day': st.mean(diff), 't_vs_fixed': td, 'p_vs_fixed': p_two(td, len(diff)),
               'extra_n': len(extra), 'extra_mean': st.mean(extra) if extra else None,
               'dropped_n': len(dropped), 'dropped_mean': st.mean(dropped) if dropped else None}
        out[name] = res
        ex = (f"+{len(extra)} gem {res['extra_mean']:+.2f}%" if extra else '')
        ex += (f" / -{len(dropped)} gem {res['dropped_mean']:+.2f}%" if dropped else '')
        pc = f"{res['per_call']:+.2f}%" if calls else '   -'
        print(f"{name:14s} {len(calls):5d} {res['days_traded']:5d} {hit*100:5.0f}% {pc:>9s} {res['t_call']:5.2f}"
              f" {res['per_day']:+7.2f}% {res['t_day']:5.2f} {res['vs_fixed_per_day']:+8.2f}pp {td:5.2f} {res['p_vs_fixed']:5.2f}  {ex}")
    # the mechanism: do the 50-79 names pay differently on thin and busy days?
    mid = [r for r in rows if 50 <= abs(r['pct']) < 80]
    n80 = {d: sum(abs(r['pct']) >= 80 for r in by[d]) for d in days}
    thin = [r['ret'] for r in mid if n80[r['date']] < 2]
    busy = [r['ret'] for r in mid if n80[r['date']] >= 2]
    print(f"namen op 50-79: {len(mid)}, gem {st.mean(r['ret'] for r in mid):+.2f}% (t {tstat([r['ret'] for r in mid]):.2f}); "
          f"op dagen met <2 namen >=80: n {len(thin)} gem {st.mean(thin) if thin else float('nan'):+.2f}%; "
          f"op dagen met >=2: n {len(busy)} gem {st.mean(busy) if busy else float('nan'):+.2f}%")
    out['_mid_band'] = {'n': len(mid), 'mean': st.mean(r['ret'] for r in mid) if mid else None,
                        'thin_n': len(thin), 'thin_mean': st.mean(thin) if thin else None,
                        'busy_n': len(busy), 'busy_mean': st.mean(busy) if busy else None}
    for lo in (50, 60, 70):
        b = [r['ret'] for r in rows if lo <= abs(r['pct']) < lo + 10]
        if b:
            print(f"  band {lo}-{lo+9}: n {len(b)}, gem {st.mean(b):+.2f}%, goed {sum(x>0 for x in b)/len(b)*100:.0f}%, t {tstat(b):.2f}")
    out['_sample'] = {'names': len(rows), 'days': len(days), 'sizes': sizes}
    return out


def portfolio(rows, cap, start=10000.0):
    """The portfolio simulator's rule (../portfolio-simulator): per day, equity split
    equally over the picks with at most `cap` per name, the rest in cash, compounding."""
    by = defaultdict(list)
    for r in rows:
        by[r['date']].append(r)
    days = sorted(by)
    out = {}
    for name, rule in RULES:
        eq, peak, mdd, daily, dep = start, start, 0.0, [], []
        for d in days:
            sel = select(by[d], rule)
            w = min(1 / len(sel), cap) if sel else 0.0
            ret = sum(w * r['ret'] / 100 for r in sel)
            eq *= 1 + ret; daily.append(ret * 100); dep.append(w * len(sel))
            peak = max(peak, eq); mdd = min(mdd, eq / peak - 1)
        out[name] = {'end': eq, 'total_pct': (eq / start - 1) * 100, 'max_dd_pct': mdd * 100,
                     'mean_day_pct': st.mean(daily), 't_day': tstat(daily),
                     'deployed_pct': st.mean(dep) * 100, 'days_invested': sum(x > 0 for x in dep)}
    return out


def print_portfolio(label, res, cap):
    print(f"\n--- portefeuille {label}, cap {cap*100:.0f}% per naam, start $10.000, bruto ---")
    print(f"{'regel':14s} {'eind':>9s} {'totaal':>8s} {'max dd':>7s} {'gem/dag':>8s} {'t':>5s} {'belegd':>7s} {'dagen':>5s}")
    for n, r in res.items():
        print(f"{n:14s} {r['end']:9.0f} {r['total_pct']:+7.1f}% {r['max_dd_pct']:6.1f}% {r['mean_day_pct']:+7.2f}% "
              f"{r['t_day']:5.2f} {r['deployed_pct']:6.0f}% {r['days_invested']:5d}")


def main():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    frozen = json.load(open(REPO / 'dashboard/data/scorebord-frozen.json'))
    bt = json.load(open(HERE.parent / 'panel-mean-pct/panel-mean-pct.json'))['datasets']['backtest']['US']['rows']
    back = []
    for r in bt:
        mv = ER.sb_move(led.get((r['date'], r['ticker'])), frozen)
        p = r['comb']['impact_sum']['gemiddelde']
        if mv is not None and p:
            back.append({'date': r['date'], 'ticker': r['ticker'], 'pct': p, 'ret': ER.sgn(p) * mv})
    v1, v2 = [], []
    for (d, t), (p, full) in ER.october_pcts().items():
        mv = ER.sb_move(led.get((d, t)), frozen)
        if mv is not None and p and full:
            (v1 if d <= '2026-10-09' else v2).append({'date': d, 'ticker': t, 'pct': p, 'ret': ER.sgn(p) * mv})
    res = {'rules': [n for n, _ in RULES],
           'backtest_opus5': evaluate(back, 'Backtest (blinde herbeoordeling, Opus 5-hunters, aug-sep)'),
           'oktober_v1': evaluate(v1, 'Oktober live E-P, us-searcher.v1 (10-02 t/m 10-09)'),
           'oktober_v2': evaluate(v2, 'Oktober live E-P, us-searcher.v2 (10-12, 10-13)')}
    res['portfolio'] = {}
    for key, rows in (('backtest_opus5', back), ('oktober_v1', v1), ('oktober_v2', v2)):
        for cap in (0.5, 0.33):
            pr = portfolio(rows, cap)
            print_portfolio(key, pr, cap)
            res['portfolio'][f'{key}_cap{int(cap*100)}'] = pr
    json.dump(res, open(HERE / 'day-rules.json', 'w'), indent=1, default=lambda x: None)


if __name__ == '__main__':
    main()
