#!/usr/bin/env python3
"""Stage E-P, October only: the panel's average size in %, each model put on one scale,
against what trading every name above a threshold would have returned.

Operator's question (2026-10-14): drop the 3-of-4 rule for this read and ask the usual
thing, whether the HIGHEST scores pay. Per name the four judges' impact_sum are rescaled
so that every model's median |size| lands on the same number (the mean of the four
medians), then averaged: `avg_pct`. The scale is read from October E-P sizes only, on
every name including unresolved ones, and never from an outcome. The September Opus 5.5
hunts and the re-judges seeded from them are left out on the operator's instruction, so
panel-history.json is NOT used here.

For each threshold x: every resolved name with |avg_pct| >= x, traded on the sign of
avg_pct, equal weight, gross. Two exits from the dashboard ledger: close to close
(`mv_close`, the window edge_resolve.py scores) and the strategy exit (`mv_strategy`).

  python3 research/analyses/panel-mean-pct/panel_mean_pct.py
"""
import glob, json, os, statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')


def sgn(x): return (x > 0) - (x < 0)


def main():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    names = []
    for run in sorted(glob.glob(str(REPO / 'research/2026/10/*/edge-panel'))):
        f = Path(run) / 'edge-scores-panel.json'
        if not f.exists(): continue
        d = Path(run).parent.name
        for r in json.load(open(f))['ranking']:
            if all(m in r['members'] for m in MEMBERS):
                names.append({'date': d, 'ticker': r['ticker'], 'selected': r['selected'],
                              'sizes': {m: r['members'][m]['impact_sum'] for m in MEMBERS}})
    med = {m: st.median(abs(n['sizes'][m]) for n in names) for m in MEMBERS}
    common = st.mean(med.values())
    factor = {m: common / med[m] for m in MEMBERS}
    rows = []
    for n in names:
        sc = {m: n['sizes'][m] * factor[m] for m in MEMBERS}
        l = led.get((n['date'], n['ticker'])) or {}
        rows.append({**n, 'scaled': {m: round(v, 3) for m, v in sc.items()}, 'avg_pct': round(st.mean(sc.values()), 3),
                     'mv_close': l.get('mv_close'), 'mv_strategy': l.get('mv_strategy'), 'session': l.get('session'),
                     'raw_avg': round(st.mean(n['sizes'].values()), 3)})
    res = [r for r in rows if r['mv_close'] is not None and r['avg_pct'] != 0]
    xs = sorted({abs(r['avg_pct']) for r in res})
    curve = []
    for x in xs:
        v = [r for r in res if abs(r['avg_pct']) >= x]
        if not v: continue
        pt = {'x': x, 'n': len(v), 'days': len({r['date'] for r in v})}
        for k in ('mv_close', 'mv_strategy'):
            s = [sgn(r['avg_pct']) * r[k] for r in v if r[k] is not None]
            pt[k] = {'n': len(s), 'mean': st.mean(s) if s else None,
                     'se': st.stdev(s) / len(s) ** .5 if len(s) > 1 else None,
                     'hit': sum(y > 0 for y in s) / len(s) if s else None}
        curve.append(pt)
    short_all = st.mean(-r['mv_close'] for r in res)
    sel = [sgn(r['avg_pct']) * r['mv_close'] for r in res if r['selected']]
    out = {'scope': 'stage E-P, October 2026, US, four judges present', 'names': len(rows), 'resolved': len(res),
           'model_median_abs_size': med, 'common_scale': common, 'factor': factor,
           'short_every_name_mv_close': short_all,
           'current_rule_selected': {'n': len(sel), 'mean_mv_close': st.mean(sel) if sel else None},
           'curve': curve, 'rows': rows}
    json.dump(out, open(OUT / 'panel-mean-pct.json', 'w'), indent=1)
    print(f"short every name {short_all:+.2f}%; current 3-of-4 rule {len(sel)} names {out['current_rule_selected']['mean_mv_close']:+.2f}%")
    print(f"{len(rows)} names, {len(res)} resolved; medians {med}; factors { {m: round(f, 2) for m, f in factor.items()} }")
    for p in curve:
        c, s = p['mv_close'], p['mv_strategy']
        print(f"|avg| >= {p['x']:5.2f}  n {p['n']:2d} ({p['days']} d)  close {c['mean']:+6.2f}% se {c['se'] or 0:4.2f} hit {c['hit']:.0%}"
              f"   strategy {s['mean'] if s['mean'] is not None else float('nan'):+6.2f}% (n {s['n']})")


if __name__ == '__main__':
    main()
