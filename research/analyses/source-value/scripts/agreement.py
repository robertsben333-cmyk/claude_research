#!/usr/bin/env python3
"""Agreement between the two v1 labelling runs, and the merges it forces (no outcome read).

  python3 scripts/agreement.py     # writes codebook/agreement-v1.json, codebook/agreement-v1.md, codebook/merges-v1.json

Per subtype: Dice agreement 2|both| / (|run0| + |run1|) over the items either run gave it.
A subtype below 0.80 is merged into its parent, the group (`G:<group>`), and agreement is
recomputed on the merged scheme until every remaining code clears 0.80 or is a group code.
A group code still below 0.80 is kept and flagged: it is the coarsest level the hierarchy has.
Flags: share of items where both runs agree (bools, direction, magnitude), and for
n_independent_sources the share within 1.
"""
import json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
ROOT = f'{SV}/labels/v1'


def pairs():
    r0, r1 = {}, {}
    for k, d in ((0, r0), (1, r1)):
        for f in os.listdir(f'{ROOT}/run{k}'):
            if f.endswith('.json'):
                j = json.load(open(f'{ROOT}/run{k}/{f}'))
                for x in j['items']:
                    d[(j['pack'], x['i'])] = x
    keys = sorted(set(r0) & set(r1))
    return [(k, r0[k], r1[k]) for k in keys]


def dice(P, mp):
    a, b, both = Counter(), Counter(), Counter()
    for _, x, y in P:
        s, t = mp.get(x.get('subtype'), x.get('subtype')), mp.get(y.get('subtype'), y.get('subtype'))
        a[s] += 1
        b[t] += 1
        if s == t:
            both[s] += 1
    return {s: (2 * both[s] / (a[s] + b[s]), a[s], b[s], both[s]) for s in set(a) | set(b)}


def main():
    cb = json.load(open(f'{SV}/codebook/codebook-v1.json'))
    grp = {s['id']: s['group'] for s in cb['subtypes']}
    P = pairs()
    mp = {}
    rounds = []
    while True:
        d = dice(P, mp)
        low = [s for s, (v, *_r) in d.items() if v < 0.80 and not str(s).startswith('G:') and s in grp]
        rounds.append({'merged_this_round': sorted(low)})
        if not low:
            break
        for s in low:
            mp[s] = 'G:' + grp[s]
        for s, t in list(mp.items()):
            mp[s] = t
    d0 = dice(P, {})
    d1 = dice(P, mp)
    exact = sum(1 for _, x, y in P if x.get('subtype') == y.get('subtype')) / len(P)
    exact_m = sum(1 for _, x, y in P if mp.get(x.get('subtype'), x.get('subtype')) == mp.get(y.get('subtype'), y.get('subtype'))) / len(P)
    flags = {}
    for f in ('quantified', 'dated_in_window', 'about_focal_company', 'primary_document', 'already_widely_reported', 'contradicted_in_pack',
              'direction', 'magnitude_claim', 'language'):
        flags[f] = round(sum(1 for _, x, y in P if x.get(f) == y.get(f)) / len(P), 4)
    flags['n_independent_sources_within1'] = round(sum(1 for _, x, y in P if isinstance(x.get('n_independent_sources'), int) and isinstance(y.get('n_independent_sources'), int) and abs(x['n_independent_sources'] - y['n_independent_sources']) <= 1) / len(P), 4)
    dirs = [(x.get('direction'), y.get('direction')) for _, x, y in P if (x.get('direction') or 0) != 0 or (y.get('direction') or 0) != 0]
    flags['direction_among_nonzero'] = round(sum(a == b for a, b in dirs) / len(dirs), 4) if dirs else None
    flags['direction_opposite_signs'] = sum(1 for a, b in dirs if a and b and a != b)
    unknown = Counter(x.get('subtype') for _, x, y in P if x.get('subtype') not in grp) + Counter(y.get('subtype') for _, x, y in P if y.get('subtype') not in grp)
    out = {'n_items_both_runs': len(P), 'subtype_exact_agreement': round(exact, 4), 'after_merge_exact_agreement': round(exact_m, 4),
           'per_subtype_before': {s: {'dice': round(v[0], 3), 'run0': v[1], 'run1': v[2], 'both': v[3]} for s, v in sorted(d0.items(), key=lambda kv: -kv[1][1])},
           'per_code_after': {s: {'dice': round(v[0], 3), 'run0': v[1], 'run1': v[2], 'both': v[3]} for s, v in sorted(d1.items(), key=lambda kv: -kv[1][1])},
           'flags': flags, 'rounds': rounds, 'unknown_subtype_ids': dict(unknown)}
    json.dump(out, open(f'{SV}/codebook/agreement-v1.json', 'w'), indent=1)
    json.dump({'version': 'v1', 'rule': 'Dice agreement < 0.80 -> merged into group code G:<group>', 'map': mp}, open(f'{SV}/codebook/merges-v1.json', 'w'), indent=1)
    L = ['# Labeller agreement, codebook v1', '', f'{len(P)} items labelled by both runs. Exact subtype agreement {exact:.1%}; '
         f'after merges {exact_m:.1%}. {len(mp)} of {len(grp)} subtypes merged into their group (Dice < 0.80).', '',
         '## Flags (share of items where the two runs agree)', '', '| flag | agreement |', '|---|---|']
    L += [f'| {k} | {v} |' for k, v in flags.items()]
    L += ['', '## Subtypes before merging', '', '| subtype | run0 | run1 | both | Dice | merged into |', '|---|---|---|---|---|---|']
    for s, v in out['per_subtype_before'].items():
        L.append(f"| `{s}` | {v['run0']} | {v['run1']} | {v['both']} | {v['dice']} | {mp.get(s, '')} |")
    L += ['', '## Codes after merging', '', '| code | run0 | run1 | both | Dice |', '|---|---|---|---|---|']
    for s, v in out['per_code_after'].items():
        L.append(f"| `{s}` | {v['run0']} | {v['run1']} | {v['both']} | {v['dice']} |")
    open(f'{SV}/codebook/agreement-v1.md', 'w').write('\n'.join(L) + '\n')
    print('items', len(P), 'exact', round(exact, 3), 'merged', len(mp), 'after', round(exact_m, 3))
    print(flags)
    print('unknown ids', dict(unknown))


if __name__ == '__main__':
    main()
