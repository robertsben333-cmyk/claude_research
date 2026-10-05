#!/usr/bin/env python3
"""Build the SkillOpt split for the US judge, from the judge-lab's frozen split.

Three roles, all US, all whole days, none drawn here:
  train (SkillOpt "train", the optimizer reads these outcomes): judge-lab TRAIN days that
        researcher_us/LESSONS.md was written from. The hunter already learned from them,
        so they were never clean evidence anyway.
  val   (SkillOpt "val", the gate): every other judge-lab TRAIN day. The optimizer never
        reads these trajectories; only their mean score decides accept or reject.
  test  (SkillOpt "test", the readout): judge-lab VALIDATION days. Neither the optimizer
        nor the gate sees them.
The judge-lab TEST days are not written at all. They stay sealed.

Each item carries the blinded pack the four-model re-judge used (no sizes in it) and,
separately, the outcome fields the reward needs. Only the rollout reads the outcome.
"""
import glob, json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '..', 'judge-lab'))
import judge_lab as J  # noqa: E402

ROLE = {'train': 'train', 'val': 'val', 'test': 'test'}


def role(r, S):
    s = J.split_of(r, S)
    if s == 'train':
        return 'train' if r['day'] in J.LESSON_DAYS['us'] else 'val'
    if s == 'val':
        return 'test'
    return None  # judge-lab test: sealed, never written


def main():
    rows = [r for r in J.load() if r['region'] == 'us']
    S = json.load(open(J.SPLIT))
    key = {x['id']: x for x in json.load(open(J.KEY))}
    pid = {x.get('pid', x['id']): x['id'] for x in key.values()}
    packs = {}
    for f in sorted(glob.glob(f'{J.REJ}/packs-*.json')):
        for p in json.load(open(f)):
            rid = pid.get(p['id'], p['id'])
            # prefer the named pack over an anonymised one when both exist
            if rid not in packs or packs[rid]['id'].startswith('anon/'):
                packs[rid] = p
    out = {k: [] for k in ROLE}
    for r in rows:
        k = role(r, S)
        if k is None or r['id'] not in packs:
            continue
        E = J.z(r['implied']) or J.z(r['hist']) or 5.0
        out[k].append({
            'id': r['id'].replace('/', '__'),
            'name_id': r['id'],
            'task_type': f"us_{r['hunter_model']}",
            'pack': packs[r['id']],
            'outcome': {'move_pct': r['move'], 'priced_move_pct': max(E, 1.0),
                        'priced_basis': 'option-implied' if J.z(r['implied']) else ('median past reaction' if J.z(r['hist']) else 'default 5'),
                        'dollar_vol': r['dv'], 'tradable': J.tradable(r), 'day': r['day']},
        })
    for k, v in out.items():
        os.makedirs(f'{D}/data/{k}', exist_ok=True)
        json.dump(v, open(f'{D}/data/{k}/items.json', 'w'), ensure_ascii=False)
        print(k, len(v), 'names over', len({x['outcome']['day'] for x in v}), 'days')


if __name__ == '__main__':
    main()
