#!/usr/bin/env python3
"""Stage E-P: combine the four panel judges into one ranking, a selection and a weight.

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
import argparse, json, math, statistics as st, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HISTORY = REPO / 'researcher_us' / 'analysis' / 'panel-history.json'
MEMBERS = ('opus5', 'opus55', 'sonnet55', 'fable51')


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
    rows = []
    for i in ids:
        mem = {}
        for m in present:
            o = verdicts[m].get(i)
            if o is None: continue
            imp = num(o.get('impact_sum')) or 0.0
            mem[m] = {'impact_sum': imp, 'p_up': num(o.get('p_up')), 'abs_move_pct': num(o.get('abs_move_pct')),
                      'z': imp / stats[m]['rms'], 'in_own_top': abs(imp) >= stats[m]['q80'] and imp != 0,
                      'note': o.get('note')}
        zs = [x['z'] for x in mem.values()]
        mu = st.mean(zs) if zs else 0.0; side = sgn(mu)
        rows.append({'id': i, 'ticker': i.split('/')[-1], 'members': mem, 'n_members': len(mem),
                     'panel_score': st.median(zs) if zs else 0.0, 'panel_mean_z': mu,
                     'panel_sd_z': st.pstdev(zs) if len(zs) > 1 else 0.0, 'side': side,
                     'sign_agree': sum(sgn(x['z']) == side != 0 for x in mem.values()),
                     'consensus_k': sum(x['in_own_top'] and sgn(x['z']) == side != 0 for x in mem.values())})
    tau = (st.median([r['panel_sd_z'] for r in rows]) or 1.0) if rows else 1.0
    prior = C.get('selected_prior_net_pct', 6.7) * C.get('prior_shrink', 0.5)
    for r in rows:
        r['selected'] = r['side'] != 0 and r['n_members'] == len(present) and r['consensus_k'] >= k_min
        prec = abs(r['panel_mean_z']) / (r['panel_sd_z'] + tau)
        r['precision'] = prec
        r['weight_equal'] = 1.0 if r['selected'] else 0.0
        r['expected_edge_pct'] = round(r['side'] * prior, 2) if r['selected'] else None
    sel = [r for r in rows if r['selected']]
    ref = st.median([r['precision'] for r in sel]) if sel else 1.0
    for r in rows:
        r['weight_precision_tilt'] = (max(0.75, min(1.25, r['precision'] / ref)) if r['selected'] and ref else 0.0)
    rows.sort(key=lambda r: (not r['selected'], -r['consensus_k'], -abs(r['panel_score']), r['id']))
    for n, r in enumerate(rows, 1): r['rank'] = n
    out = {'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'run': str(run),
           'stage': stage, 'members_present': present, 'members_missing': [m for m in MEMBERS if m not in present],
           'ranking_key': 'panel_score', 'selection': f'consensus_k >= {k_min} of {len(present)}',
           'live_weight': 'weight_equal', 'frozen_variant_weights': ['weight_precision_tilt'],
           'member_reference': {m: stats[m] for m in present}, 'tau': tau,
           'note': ('panel_score is the signed median of the members\' sizes, each read against its own '
                    'recent history. consensus_k counts members that put the name in their own top 20% '
                    'on the panel\'s side; that, not sign agreement, is what selected well on the '
                    'development names. Certainty (p_up) is recorded and decides nothing. '
                    'expected_edge_pct is a shrunk in-sample prior, not a forecast. Research only.'),
           'ranking': rows}
    # ticker-keyed copy for edge_resolve.py, which ranks this beside the key
    out['ranking_by_ticker'] = [{'ticker': r['ticker'], 'panel_score': r['panel_score'],
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
    sess = SR.session_labels(a.run)
    print(f"{'rank':>4s} {'ticker':8s} {'session':7s} {'sel':3s} {'k':>2s} {'agree':>5s} {'score':>6s} {'sd':>5s}  members (z)")
    for r in out['ranking']:
        zz = ' '.join(f"{m}:{x['z']:+.2f}{'*' if x['in_own_top'] else ''}" for m, x in r['members'].items())
        print(f"{r['rank']:4d} {r['ticker']:8s} {sess.get(r['ticker'], 'n/a'):7s} {'yes' if r['selected'] else '':3s} {r['consensus_k']:2d} "
              f"{r['sign_agree']:2d}/{r['n_members']}  {r['panel_score']:+6.2f} {r['panel_sd_z']:5.2f}  {zz}")


if __name__ == '__main__':
    main()
