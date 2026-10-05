#!/usr/bin/env python3
"""Score CONFIRM-PREREG.md's four contrasts on the judge-lab TEST days only, once.

  python3 confirm.py     # writes results/confirm.json and appends to ../judge-lab/TEST-LOG.md
"""
import json, os, statistics as st, sys
from datetime import datetime, timezone
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402

SUF, REL = 42.5, 68


def verdict(gap, tol):
    return 'holds' if gap > tol else ('flips' if gap < -tol else 'flat')


def rate(g, c):
    g = [e for e in g if c in e['call'] and A.sgn(e['call'][c])]
    k = sum(A.sgn(e['call'][c]) == A.sgn(e['move']) for e in g)
    return k, len(g), (k / len(g) if g else None)


def main():
    events, items = A.load(unseal=True)
    test = [e for e in events if e['role'] == 'test' and not e['duplicate_hunt']]
    tkeys = {e['event_key'] for e in test}
    titems = [it for it in items if it['event_key'] in tkeys]
    O = {'n_names': len(test), 'n_items': len(titems), 'no_anchor': sum(e['implied_move'] is None for e in test)}
    calls = ('median4', 'live', 'opus5', 'opus', 'sonnet', 'fable', 'labeler')
    rows = {}
    for c in calls:
        lo, hi = rate([e for e in test if e['lab']['pack_sufficiency'] < SUF], c), rate([e for e in test if e['lab']['pack_sufficiency'] >= SUF], c)
        na, an = rate([e for e in test if e['implied_move'] is None], c), rate([e for e in test if e['implied_move'] is not None], c)
        rows[c] = {'suf_lo': f'{lo[0]}/{lo[1]}', 'suf_hi': f'{hi[0]}/{hi[1]}', 'no_anchor': f'{na[0]}/{na[1]}', 'anchor': f'{an[0]}/{an[1]}',
                   'gap_suf': None if lo[2] is None or hi[2] is None else round(lo[2] - hi[2], 3),
                   'gap_anchor': None if na[2] is None or an[2] is None else round(na[2] - an[2], 3)}
    O['by_judge'] = rows
    m = rows['median4']
    O['C1'] = {**{k: m[k] for k in ('suf_lo', 'suf_hi', 'gap_suf')}, 'verdict': verdict(m['gap_suf'], 0.05) if m['gap_suf'] is not None else 'n/a'}
    O['C2'] = {**{k: m[k] for k in ('no_anchor', 'anchor', 'gap_anchor')}, 'verdict': verdict(m['gap_anchor'], 0.05) if m['gap_anchor'] is not None else 'n/a'}
    na = {e['event_key'] for e in test if e['implied_move'] is None}
    mv = {e['event_key']: e['move_n'] for e in test}
    f = [it for it in titems if it['event_key'] in na and it['claim_type'] == 'focal_primary' and A.sgn(it['direction'])]
    s = [A.sgn(it['direction']) * mv[it['event_key']] for it in f]
    O['C3'] = {'n_items': len(f), 'events': len({it['event_key'] for it in f}),
               'hits': f"{sum(x > 0 for x in s)}/{len(s)}", 'mean_signed_move_n': round(st.mean(s), 3) if s else None,
               'verdict': verdict(st.mean(s), 0.10) if s else 'n/a'}
    lr = [it for it in titems if it['reliability'] is not None and it['reliability'] < REL and A.sgn(it['direction'])]
    s4 = [A.sgn(it['direction']) * mv[it['event_key']] for it in lr]
    O['C4'] = {'n_items': len(lr), 'events': len({it['event_key'] for it in lr}),
               'hits': f"{sum(x > 0 for x in s4)}/{len(s4)}", 'mean_signed_move_n': round(st.mean(s4), 3) if s4 else None,
               'verdict': verdict(-st.mean(s4), 0.10) if s4 else 'n/a'}
    json.dump(O, open(f'{HERE}/results/confirm.json', 'w'), indent=1)
    log = os.path.join(HERE, '..', 'judge-lab', 'TEST-LOG.md')
    new = not os.path.exists(log)
    with open(log, 'a') as fh:
        if new:
            fh.write('# Test-set unseal log\n\nEvery read of the judge-lab TEST days is appended here.\n\n')
        fh.write(f"- {datetime.now(timezone.utc).isoformat(timespec='seconds')}: opened by `../source-types/confirm.py` for the four "
                 f"contrasts pre-registered in `../source-types/CONFIRM-PREREG.md` (US only, {len(test)} names). Not used to choose "
                 f"any judge-lab variant. Verdicts: C1 {O['C1']['verdict']}, C2 {O['C2']['verdict']}, C3 {O['C3']['verdict']}, C4 {O['C4']['verdict']}.\n")
    print(json.dumps(O, indent=1))


if __name__ == '__main__':
    main()
