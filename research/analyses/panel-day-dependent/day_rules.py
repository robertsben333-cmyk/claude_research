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


# Score-dependent sizing (Xavier, 2026-10-14): the weight per name rises with |panel_pct|,
# never above 50% of equity; gross exposure at most 100% (scaled down pro rata). Fixed here
# before scoring. 'curve' reads the frozen expected-return curve, which was FITTED ON THESE
# SAME NAMES (backtest + October), so it is in sample by construction.
CURVE = {c['abs_pct']: c['expected'] for c in
         json.load(open(HERE.parent / 'panel-mean-pct/expected-return-2026-10-13.json'))['curve']}
SIZING = [
    ('gelijk vast80', lambda p: 0.5 if p >= 80 else 0.0, 'equal'),
    ('gelijk aanvul 2/50', None, 'fill2'),
    ('lineair 50-100', lambda p: 0.5 * max(0.0, (p - 50) / 50), 'abs'),
    ('lineair 60-100', lambda p: 0.5 * max(0.0, (p - 60) / 40), 'abs'),
    ('staffel', lambda p: 0.5 if p >= 90 else 0.33 if p >= 80 else 0.2 if p >= 70 else 0.1 if p >= 60 else 0.0, 'abs'),
    ('curve (in sample)', lambda p: 0.5 * max(0.0, ER.at([CURVE[g] for g in ER.GRID], p) - CURVE[50]) / (CURVE[100] - CURVE[50]), 'abs'),
]


def sized(rows, start=10000.0):
    by = defaultdict(list)
    for r in rows:
        by[r['date']].append(r)
    days = sorted(by)
    out, daily_all = {}, {}
    for name, f, mode in SIZING:
        eq, peak, mdd, daily, dep, ncalls = start, start, 0.0, [], [], 0
        for d in days:
            rs = by[d]
            if mode == 'equal':
                sel = [r for r in rs if abs(r['pct']) >= 80]
                w = {id(r): min(1 / len(sel), 0.5) for r in sel} if sel else {}
            elif mode == 'fill2':
                sel = select(rs, ('fill', 2, 50))
                w = {id(r): min(1 / len(sel), 0.5) for r in sel} if sel else {}
            else:
                w = {id(r): f(abs(r['pct'])) for r in rs if f(abs(r['pct'])) > 0}
                tot = sum(w.values())
                if tot > 1:
                    w = {k: v / tot for k, v in w.items()}
            ret = sum(w.get(id(r), 0) * r['ret'] / 100 for r in rs)
            ncalls += len(w)
            eq *= 1 + ret; daily.append(ret * 100); dep.append(sum(w.values()))
            peak = max(peak, eq); mdd = min(mdd, eq / peak - 1)
        daily_all[name] = daily
        dn = [min(0.0, x) for x in daily]
        sd, dsd = (st.stdev(daily) if len(daily) > 1 else 0.0), math.sqrt(sum(x * x for x in dn) / len(dn))
        gains, losses = sum(x for x in daily if x > 0), -sum(x for x in daily if x < 0)
        ann = ((eq / start) ** (252 / len(days)) - 1) * 100
        kpi = {'vol_ann_pct': sd * math.sqrt(252), 'sharpe_ann': st.mean(daily) / sd * math.sqrt(252) if sd else None,
               'sortino_ann': st.mean(daily) / dsd * math.sqrt(252) if dsd else None,
               'calmar': ann / abs(mdd * 100) if mdd else None, 'cagr_pct': ann,
               'day_hit_pct': 100 * sum(x > 0 for x in daily) / max(1, sum(x != 0 for x in daily)),
               'profit_factor': gains / losses if losses else None,
               'best_day_pct': max(daily), 'worst_day_pct': min(daily),
               'sharpe_day': st.mean(daily) / sd if sd else None}
        # net of a 1% round-trip cost on what was deployed that day (spread + borrow, a guess)
        net = [x - 1.0 * w for x, w in zip(daily, dep)]
        nsd = st.stdev(net) if len(net) > 1 else 0.0
        eqn = start
        for x in net:
            eqn *= 1 + x / 100
        kpi.update({'net1_total_pct': (eqn / start - 1) * 100, 'net1_mean_day_pct': st.mean(net),
                    'net1_sharpe_day': st.mean(net) / nsd if nsd else None,
                    'net1_sharpe_ann': st.mean(net) / nsd * math.sqrt(252) if nsd else None})
        diff = [a - b for a, b in zip(daily, daily_all['gelijk vast80'])]
        out[name] = {'end': eq, 'total_pct': (eq / start - 1) * 100, 'max_dd_pct': mdd * 100,
                     'mean_day_pct': st.mean(daily), 't_day': tstat(daily), 'calls': ncalls,
                     'deployed_pct': st.mean(dep) * 100, 'days_invested': sum(x > 0 for x in dep),
                     'kpi': kpi, 'vs_vast80_pp': st.mean(diff), 't_vs_vast80': tstat(diff) if any(diff) else float('nan')}
    return out


def print_kpi(label, res):
    print(f"\n--- kengetallen, {label} (dagrendementen, 0 rf, x252 is extrapolatie) ---")
    print(f"{'schema':20s} {'vol/dag':>7s} {'Sh/dag':>6s} {'Sh/jr':>6s} {'Sortino':>7s} {'dag+':>5s} {'PF':>5s} {'beste':>7s} {'slechtste':>9s} {'netto1%':>8s} {'Sh/jr netto':>11s}")
    for n, r in res.items():
        k = r['kpi']; f = lambda v, w=6, d=2: f"{v:{w}.{d}f}" if v is not None else ' ' * (w - 1) + '-'
        print(f"{n:20s} {k['vol_ann_pct']/math.sqrt(252):6.2f}% {f(k['sharpe_day'])} {f(k['sharpe_ann'])} {f(k['sortino_ann'],7)} "
              f"{k['day_hit_pct']:4.0f}% {f(k['profit_factor'],5)} {k['best_day_pct']:+6.1f}% {k['worst_day_pct']:+8.1f}% "
              f"{k['net1_total_pct']:+7.1f}% {f(k['net1_sharpe_ann'],11)}")


def print_sized(label, res):
    print(f"\n--- gewicht naar score, {label}, max 50% per naam, max 100% bruto, start $10.000 ---")
    print(f"{'schema':20s} {'calls':>5s} {'eind':>8s} {'max dd':>7s} {'gem/dag':>8s} {'t':>5s} {'belegd':>7s} {'vs vast80':>9s} {'t':>5s}")
    for n, r in res.items():
        print(f"{n:20s} {r['calls']:5d} {r['total_pct']:+7.1f}% {r['max_dd_pct']:6.1f}% {r['mean_day_pct']:+7.2f}% "
              f"{r['t_day']:5.2f} {r['deployed_pct']:6.0f}% {r['vs_vast80_pp']:+8.2f}pp {r['t_vs_vast80']:5.2f}")


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
    res['sizing'] = {}
    for key, rows in (('backtest_opus5', back), ('oktober_v1', v1), ('oktober_v2', v2)):
        res['sizing'][key] = sized(rows)
        print_sized(key, res['sizing'][key])
        print_kpi(key, res['sizing'][key])
    json.dump(res, open(HERE / 'day-rules.json', 'w'), indent=1, default=lambda x: None)


if __name__ == '__main__':
    main()
