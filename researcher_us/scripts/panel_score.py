#!/usr/bin/env python3
"""Stage E-P: combine the four panel judges into one ranking, a selection and a weight.

SINCE 2026-10-14 (operator's instruction) every member is reported as a PERCENTILE of
its own range, and the US selection reads the mean of those percentiles:

- `pct` per member: the share of that member's own reference sizes with a smaller
  |impact_sum|, x 100: a STRENGTH from 0 to 100, with the member's direction beside it in
  `side` (+1 long, -1 short, 0 no view; operator, 2026-10-14: no negative percentiles on
  any report). `pct_signed` keeps side x pct for arithmetic. "Top 10%" of
  Opus 5 and "top 10%" of Opus 5.5 are then the same statement whatever scale each
  model sizes on, and a future model joins without rescaling the others.
- The reference is POINT IN TIME: the member's LIVE sizes from runs dated before this
  one (`live_reference`), the last `history_window` of them. The re-judge seed is not
  live and is left out (it judged September and Opus 5-era evidence, on another scale);
  it is only a fallback when fewer than MIN_REFERENCE live sizes exist, as is the US
  E-P history for a market panel that has not built its own yet
  (`reference_fallback`).
- `panel_pct` (0-100) = the size of the mean of the members' SIGNED percentiles, so
  members who disagree on the side pull it down; `side` is that mean's direction and
  `panel_pct_signed` the mean itself, kept for rank correlations. `panel_pct_sd` is the
  spread of the signed percentiles, recorded and deciding nothing (research/analyses/panel-mean-pct/: it did not
  help measurably as a gate or a penalty).
- `selection: mean_pct` (stage E-P): selected when every member is present and
  panel_pct >= 100 x (1 - selection_top_share), i.e. the mean is in the top 20%, on
  `side`. `selection: consensus` (the market panels, unchanged):
  3 of 4 members in their own top 20% on the panel's side. Both verdicts are written on
  every row (`selected_mean_pct`, `selected_consensus`) so each can be measured forward.
- The old score is still recorded: z, panel_score, consensus_k, in_own_top.
- `expected_return_pct` (since 2026-10-14, stage E-P only, `expected_return: calibrated`):
  the percentile leads, and each panel_pct is referenced to ONE expected return on the
  trade, the same for every name at that percentile, read off the frozen curve in
  `researcher_us/analysis/panel-calibration.json` (panel_calibrate.py, which also holds
  the out-of-sample check). With it: an 80% band for how well that expectation is known
  and `p_right`, the hit rate at that percentile. On a selected name `expected_edge_pct`
  is now that expectation as a signed move instead of the shrunk development prior. On
  the scorebord's window, gross of costs. The curve is flat at about +0.3% below
  panel_pct 50 and rises from there.

What follows is the rule as it was built on 2026-10-01, kept because every field it
describes is still written.

What the development data said (research/analyses/judge-lab/, APPROACH.md section 6) and
how each finding becomes a rule here:

- Each model sizes on its own scale, so every member's impact_sum is read against that
  member's OWN recent history (`researcher_us/analysis/panel-history.json`, seeded from
  the four-model re-judge, then extended by every run): z = impact / rms(history), and
  "in its top" = |impact| at or above the member's 80th percentile.
- Agreement on the SIGN carries nothing by itself (all four agreed on 127 of 151 names,
  right 50%). Agreement on SIZE does: `consensus_k` counts the members that put the name
  in their own top 20% on the panel's side. A name is `selected` at consensus_k >= 3 of 4
  (18/24 right, +6.7% net on development names), or all of a smaller panel.
- Inside the selection weights barely mattered (equal +6.7%, the best tilt +7.0%), so
  the live weight is EQUAL. The precision tilt, |mean z| / (sd z + tau) clamped to
  0.75..1.25, is written beside it as a frozen variant to be measured forward, not used.
- The models' own certainty (|p_up - 50|) was not monotonic in the hit rate. It is
  recorded per member and decides nothing.
- `panel_score` (the signed median z) is the ranking key for a full-day ranking; one unit
  was worth ~1.7 points of signed move across all names, against a move sd of ~10, so it
  ranks and does not forecast. `expected_edge_pct` on a selected name is the development
  prior for the selection, shrunk by half, because it was measured in sample.

  python3 researcher_us/scripts/panel_score.py --run research/<Y>/<M>/<DATE>/edge-panel

Reads <RUN>/panel/<member>.json for the members present; writes
<RUN>/edge-scores-panel.json (ranked beside the key by edge_resolve.py) and appends the
day's member sizes to the history file, once per id.
"""
import argparse, bisect, json, math, re, statistics as st, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HISTORY = REPO / 'researcher_us' / 'analysis' / 'panel-history.json'
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')
MIN_REFERENCE = 20


def date_of(path):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', str(path or ''))
    return m.group(1) if m else None


def is_live(x):
    return not str(x.get('source') or '').startswith('seed')


def live_reference(hist, member, window, before=None, exclude=(), fallback=None):
    """|impact_sum| of `member`'s live sizes from runs dated before `before` (all when
    None), never an id in `exclude`, the last `window` of them, sorted. Below
    MIN_REFERENCE it is topped up from `fallback` (a callable member -> rows, oldest
    first). Returns (sorted sizes, basis)."""
    def ok(x):
        d = date_of(x.get('source'))
        return x['id'] not in exclude and (before is None or (d is not None and d < before))
    rows = [x for x in hist.get(member, []) if is_live(x) and ok(x)]
    basis = 'live'
    if len(rows) < MIN_REFERENCE and fallback:
        have = {x['id'] for x in rows}
        extra = [x for x in fallback(member) if x['id'] not in have and x['id'] not in exclude
                 and (not is_live(x) or ok(x))]
        took = extra[-(MIN_REFERENCE - len(rows)):]
        rows = took + rows
        basis = f'live+{len(took)} fallback' if took else 'live'
    rows = rows[-window:]
    return sorted(abs(x['impact_sum']) for x in rows), basis


def pct_of(ref_sorted, v):
    """Signed percentile of `v` in a member's own reference: the share with a smaller
    |size|, x 100; a zero size is 0."""
    if not ref_sorted or not v:
        return 0.0
    return sgn(v) * 100.0 * bisect.bisect_left(ref_sorted, abs(v)) / len(ref_sorted)


def cfg():
    import yaml
    c = yaml.safe_load(open(REPO / 'config' / 'pipeline.yaml'))
    return c.get('edge_panel') or {}


def sgn(x): return (x > 0) - (x < 0)


def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None


def member_stats(hist, window):
    v = [abs(x['impact_sum']) for x in hist[-window:]]
    if len(v) < 20: return None
    v_sorted = sorted(v)
    return {'n': len(v), 'rms': (sum(a * a for a in v) / len(v)) ** .5 or 1.0,
            'q80': v_sorted[int(0.8 * len(v_sorted))]}


def fallback_rows(kind, hist):
    """Rows to top a thin live reference up with: the history's own seed, or stage E-P's
    live sizes (for a market panel that has not built its own yet)."""
    if kind == 'seed':
        return lambda m: [x for x in hist.get(m, []) if not is_live(x)]
    if kind == 'us_live':
        us = json.load(open(HISTORY)) if HISTORY.exists() else {}
        return lambda m: [x for x in us.get(m, []) if is_live(x)]
    return None


def score(run, C, dry_run=False, history=None, stage='E-P'):
    # `history` and `stage` exist for scripts/market_panel.py (the non-US stages), which
    # keep one history file per market; the defaults are stage E-P's, unchanged.
    run = Path(run)
    HIST = Path(history) if history else HISTORY
    hist = json.load(open(HIST)) if HIST.exists() else {}
    window = int(C.get('history_window', 200)); share_q = C.get('member_top_share', 0.2)
    present, verdicts = [], {}
    for m in MEMBERS:
        f = run / 'panel' / f'{m}.json'
        if f.exists():
            present.append(m); verdicts[m] = {o['id']: o for o in json.load(open(f))}
    if not present: sys.exit('no panel verdicts in ' + str(run / 'panel'))
    ids = sorted(set().union(*[set(v) for v in verdicts.values()]))
    today = set(ids)
    stats = {}
    for m in present:
        h = [x for x in hist.get(m, []) if x['id'] not in today]
        stats[m] = member_stats(h, window)
        if stats[m] is None: sys.exit(f'too little history for {m}: seed panel-history.json first')
    k_min = math.ceil(C.get('consensus_fraction', 0.75) * len(present))
    rule = C.get('selection', 'consensus')
    top_share = C.get('selection_top_share', share_q)
    pct_min = 100.0 * (1 - top_share)
    run_date = date_of(run.resolve().parent.name)      # research/<Y>/<M>/<DATE>/<stage>
    fb = fallback_rows(C.get('reference_fallback', 'seed'), hist)
    pref = {}
    for m in present:
        pref[m] = live_reference(hist, m, window, before=run_date, exclude=today, fallback=fb)
    rows = []
    for i in ids:
        mem = {}
        for m in present:
            o = verdicts[m].get(i)
            if o is None: continue
            imp = num(o.get('impact_sum')) or 0.0
            mem[m] = {'impact_sum': imp, 'p_up': num(o.get('p_up')), 'abs_move_pct': num(o.get('abs_move_pct')),
                      'pct_signed': round(pct_of(pref[m][0], imp), 1),
                      'z': imp / stats[m]['rms'], 'in_own_top': abs(imp) >= stats[m]['q80'] and imp != 0,
                      'note': o.get('note')}
        zs = [x['z'] for x in mem.values()]
        for x in mem.values():
            x['pct'], x['side'] = abs(x['pct_signed']), sgn(x['pct_signed'])
        ps = [x['pct_signed'] for x in mem.values()]
        mu = st.mean(zs) if zs else 0.0; side = sgn(mu)
        ppct = st.mean(ps) if ps else 0.0
        rows.append({'id': i, 'ticker': i.split('/')[-1], 'members': mem, 'n_members': len(mem),
                     'panel_pct': round(abs(ppct), 1), 'panel_pct_signed': round(ppct, 1), 'panel_pct_sd': round(st.pstdev(ps), 1) if len(ps) > 1 else 0.0,
                     'panel_score': st.median(zs) if zs else 0.0, 'panel_mean_z': mu,
                     'panel_sd_z': st.pstdev(zs) if len(zs) > 1 else 0.0, 'side_z': side,
                     'side_pct': sgn(ppct),
                     'sign_agree': sum(sgn(x['z']) == side != 0 for x in mem.values()),
                     'consensus_k': sum(x['in_own_top'] and sgn(x['z']) == side != 0 for x in mem.values())})
    tau = (st.median([r['panel_sd_z'] for r in rows]) or 1.0) if rows else 1.0
    prior = C.get('selected_prior_net_pct', 6.7) * C.get('prior_shrink', 0.5)
    for r in rows:
        full = r['n_members'] == len(present)
        r['selected_consensus'] = r['side_z'] != 0 and full and r['consensus_k'] >= k_min
        r['selected_mean_pct'] = r['side_pct'] != 0 and full and r['panel_pct'] >= pct_min
        r['selected'] = r['selected_mean_pct'] if rule == 'mean_pct' else r['selected_consensus']
        r['side'] = r['side_pct'] if rule == 'mean_pct' else r['side_z']
        prec = abs(r['panel_mean_z']) / (r['panel_sd_z'] + tau)
        r['precision'] = prec
        r['weight_equal'] = 1.0 if r['selected'] else 0.0
        r['expected_edge_pct'] = round(r['side'] * prior, 2) if r['selected'] else None
    cal_kind = C.get('expected_return')
    cal = None
    if cal_kind == 'calibrated':
        import panel_calibrate as PC
        cal = PC.load_calibration()
    for r in rows:
        er = PC.expected(cal, r['panel_pct_signed']) if cal else None
        r.update(er or {'expected_return_pct': None, 'expected_return_lo80': None, 'expected_return_hi80': None,
                        'p_right': None, 'expected_move_pct': None})
        if cal and r['selected']:
            r['expected_edge_pct'] = r['expected_move_pct']
    sel = [r for r in rows if r['selected']]
    ref = st.median([r['precision'] for r in sel]) if sel else 1.0
    for r in rows:
        r['weight_precision_tilt'] = (max(0.75, min(1.25, r['precision'] / ref)) if r['selected'] and ref else 0.0)
    if rule == 'mean_pct':
        rows.sort(key=lambda r: (not r['selected'], -r['panel_pct'], r['id']))
    else:
        rows.sort(key=lambda r: (not r['selected'], -r['consensus_k'], -abs(r['panel_score']), r['id']))
    for n, r in enumerate(rows, 1): r['rank'] = n
    out = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'run': str(run),
           'stage': stage, 'members_present': present, 'members_missing': [m for m in MEMBERS if m not in present],
           'ranking_key': 'panel_pct' if rule == 'mean_pct' else 'panel_score',
           'selection_rule': rule,
           'selection': (f'panel_pct >= {pct_min:.0f}, all {len(present)} members present' if rule == 'mean_pct'
                         else f'consensus_k >= {k_min} of {len(present)}'),
           'expected_return': ({'basis': 'researcher_us/analysis/panel-calibration.json',
                                'fitted_utc': cal.get('generated_utc'), 'sample': cal.get('sample'),
                                'window': cal.get('window')} if cal else None),
           'member_pct_reference': {m: {'n': len(pref[m][0]), 'basis': pref[m][1], 'before': run_date,
                                        **{f'top{t}': (pref[m][0][min(len(pref[m][0]) - 1, int(len(pref[m][0]) * (1 - t / 100)))]
                                                       if pref[m][0] else None) for t in (10, 20, 30)}}
                                    for m in present},
           'live_weight': 'weight_equal', 'frozen_variant_weights': ['weight_precision_tilt'],
           'member_reference': {m: stats[m] for m in present}, 'tau': tau,
           'note': ('Each member is reported as a percentile of its own live range, 0-100 (pct), with '
                    'its direction in side; panel_pct (0-100) is the size of the mean of the signed '
                    'percentiles and side its direction; panel_pct_sd their spread. '
                    + ('The selection is panel_pct in the top 20%. ' if rule == 'mean_pct' else
                       'The selection is 3 of 4 members in their own top 20% (consensus_k). ')
                    + 'panel_score is the signed median of the members\' sizes, each read against its own '
                    'recent history. consensus_k counts members that put the name in their own top 20% '
                    'on the panel\'s side; that, not sign agreement, is what selected well on the '
                    'development names. Certainty (p_up) is recorded and decides nothing. '
                    'expected_edge_pct is a shrunk in-sample prior, not a forecast. Research only.'),
           'ranking': rows}
    # ticker-keyed copy for edge_resolve.py, which ranks this beside the key
    out['ranking_by_ticker'] = [{'ticker': r['ticker'], 'panel_score': r['panel_score'], 'panel_pct': r['panel_pct'],
                                 'panel_pct_signed': r['panel_pct_signed'], 'side': r['side'],
                                 'panel_selected': r['selected'], 'consensus_k': r['consensus_k']} for r in rows]
    json.dump(out, open(run / 'edge-scores-panel.json', 'w'), indent=1)
    added = 0
    if dry_run: return out, 0
    for m in present:
        seen = {x['id'] for x in hist.get(m, [])}
        for i, o in verdicts[m].items():
            if i not in seen:
                hist.setdefault(m, []).append({'id': i, 'impact_sum': num(o.get('impact_sum')) or 0.0, 'source': str(run)})
                added += 1
    json.dump(hist, open(HIST, 'w'), indent=1)
    return out, added


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True)
    ap.add_argument('--dry-run', action='store_true', help='score without appending to the history')
    a = ap.parse_args()
    out, added = score(a.run, cfg(), a.dry_run)
    print(f"members {', '.join(out['members_present'])}"
          + (f" (MISSING {', '.join(out['members_missing'])})" if out['members_missing'] else '')
          + f"; selection {out['selection']}; {added} sizes added to the history")
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
    import score_report as SR
    print_table(out, SR.session_labels(a.run))


def print_table(out, sess):
    """The panel table every stage pastes: each member as a signed percentile of its own
    range (* where in its own top 20%), the mean and spread, then the old score."""
    ref = out.get('member_pct_reference') or {}
    print('own top 20% starts at: ' + ', '.join(f"{m} |{v['top20']:.2f}|" if v.get('top20') is not None else f"{m} -"
                                               for m, v in ref.items())
          + f"  (live sizes before {next(iter(ref.values()), {}).get('before')}, "
          + ', '.join(f"{m} n={v['n']} {v['basis']}" for m, v in ref.items()) + ')')
    er = out.get('expected_return')
    print(f"{'rank':>4s} {'ticker':8s} {'session':7s} {'sel':3s} {'pct':>3s} {'side':5s} {'sd':>4s}  {'members (own percentile, L/S)':44s} "
          f"{'k':>2s} {'score':>6s}" + ('  E[return] at this pct (80% band)  P(right)' if er else ''))
    for r in out['ranking']:
        pp = ' '.join(f"{m}:{x['pct']:3.0f}{'L' if x['side'] > 0 else 'S' if x['side'] < 0 else '-'}"
                      f"{'*' if x['pct'] >= 80 else ' '}" for m, x in r['members'].items())
        e = ''
        if er and r.get('expected_return_pct') is not None:
            e = (f"  {r['expected_return_pct']:+5.2f}% [{r['expected_return_lo80']:+.2f}, {r['expected_return_hi80']:+.2f}]"
                 f"           {r['p_right']:.2f}")
        print(f"{r['rank']:4d} {r['ticker']:8s} {sess.get(r['ticker'], 'n/a'):7s} {'yes' if r['selected'] else '':3s} "
              f"{r['panel_pct']:3.0f} {'long' if r['side'] > 0 else 'short' if r['side'] < 0 else '-':5s} {r['panel_pct_sd']:4.0f}  {pp:44s} {r['consensus_k']:2d} {r['panel_score']:+6.2f}{e}")
    if er:
        print(f"E[return]: what a name at this panel_pct has earned on the panel's side (one number per "
              f"percentile, scorebord window, gross); curve fitted {er['fitted_utc']} on "
              f"{er['sample']['panel_names']} resolved panel names.")


if __name__ == '__main__':
    main()
