#!/usr/bin/env python3
"""Refresh the registry with forward days, never over v1.

  python3 scripts/label_forward.py && python3 scripts/update_registry.py

Reads data/forward/ and labels/forward/ (codebook v1, frozen), computes each cell's raw DV*
on the forward prints alone (the residual uses stratum A's band means and run-up slope, which
are fixed), writes registry/forward-cells.json, then rebuilds the registry with those cells as
the forward column into registry/registry-forward.json. registry-v1.json is never touched. A
verdict is called CONFIRMED only where the forward data agree with v1's sign on >= 5 votes.
"""
import json, os, statistics as st, subprocess, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402

BANDS = ['micro', 'small', 'mid', 'large']


def main():
    if not os.path.exists(f'{SV}/data/forward/events.json'):
        sys.exit('run label_forward.py first')
    FE = [e for e in json.load(open(f'{SV}/data/forward/events.json')) if not e['duplicate_hunt']]
    FI = json.load(open(f'{SV}/data/forward/items.json'))
    if not FE:
        json.dump({}, open(f'{SV}/registry/forward-cells.json', 'w'))
        print('no forward prints yet')
        return
    E, _ = core.load()
    A = [e for e in E if e['stratum'] == 'A']
    mu = {b: st.mean([e['y']['strategy'] for e in A if e['cap_band'] == b]) for b in BANDS}
    cb = core.codebook()
    grp = {s['id']: s['group'] for s in cb['subtypes']}
    mm = core.merge_map()
    L = core.load_labels(root=f'{SV}/labels/forward')
    ev = {}
    for e in FE:
        y = core.wins(e['move'] / e['priced_move'])
        e['res_f'] = y - mu.get(e['cap_band'], 0.0)
        ev[e['id']] = e
    acc = defaultdict(lambda: [0.0, 0.0])
    for it in FI:
        e = ev.get(it['event'])
        runs = [r[it['i']] for r in L.get(it['pack_id'], []) if it['i'] in r]
        if not e or not runs:
            continue
        lab = core.merged_label(runs, mm, grp)
        if not lab['vote']:
            continue
        for c, w in lab['subtype_w'].items():
            g = c[2:] if c.startswith('G:') else grp.get(c)
            for key in (f'{c}|None', f"{c}|{e['cap_band']}", f'GROUP:{g}|None', f"GROUP:{g}|{e['cap_band']}"):
                acc[key][0] += w * lab['vote'] * e['res_f']
                acc[key][1] += w
    cells = {k: {'DVstar_raw': a / n, 'n_vote': n} for k, (a, n) in acc.items() if n}
    json.dump(cells, open(f'{SV}/registry/forward-cells.json', 'w'), indent=1)
    subprocess.run([sys.executable, f'{HERE}/registry.py', '--forward', f'{SV}/registry/forward-cells.json'], check=True)


if __name__ == '__main__':
    main()
