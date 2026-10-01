#!/usr/bin/env python3
"""Select the Opus 5 hunter days from the four-model re-judge and chunk them into packs.

Reads ../rejudge-four-models/packs-*.json and key.json (for the day and region only; the
packs themselves carry no outcome). Keeps every pack entry whose live hunt ran on Opus 5:
day before 2026-09-23 (the `opus` alias moved to Opus 5.5 between 18:56 and 19:09 UTC on
2026-09-22, after every run dated 09-22 had sealed). Corpus names in packs-x2 have no key
and are skipped. Writes packs-NN.json (CHUNK names each, seeded shuffle so no pack is one
day) and manifest.json with the git blob of every hunter definition, lessons file and the
core the judges will read, so the prompt version under test is pinned.

    python3 build_packs.py
"""
import glob, json, os, random, subprocess
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '..', 'rejudge-four-models')
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
CHUNK = 13
CUTOFF = '2026-09-23'

key = json.load(open(os.path.join(SRC, 'key.json')))
pid = {r.get('pid', r['id']): r for r in key}
sel = []
for f in sorted(glob.glob(os.path.join(SRC, 'packs-*.json'))):
    for p in json.load(open(f)):
        e = pid.get(p['id'])
        if e and e['day'] < CUTOFF:
            sel.append(p)
random.seed(20261001)
random.shuffle(sel)
for old in glob.glob(os.path.join(D, 'packs-*.json')):
    os.remove(old)
packs = [sel[i:i + CHUNK] for i in range(0, len(sel), CHUNK)]
for n, chunk in enumerate(packs, 1):
    json.dump(chunk, open(os.path.join(D, f'packs-{n:02d}.json'), 'w'), indent=1, ensure_ascii=False)

def blob(path):
    try:
        return subprocess.check_output(['git', 'hash-object', os.path.join(ROOT, path)], text=True).strip()
    except Exception:
        return None
files = sorted(({p.get('hunter_definition') for p in sel} | {p.get('lessons_file') for p in sel} | {'config/hunter-core.md'}) - {None})
json.dump({'cutoff_day': CUTOFF, 'names': len(sel), 'packs': len(packs), 'chunk': CHUNK,
           'by_region': {r: sum(1 for p in sel if pid[p['id']]['region'] == r) for r in sorted({pid[p['id']]['region'] for p in sel})},
           'anonymised': sum(1 for p in sel if p['id'].startswith('anon/')),
           'files_judges_read': {f: blob(f) for f in files}},
          open(os.path.join(D, 'manifest.json'), 'w'), indent=1)
print(f'{len(sel)} names in {len(packs)} packs')
