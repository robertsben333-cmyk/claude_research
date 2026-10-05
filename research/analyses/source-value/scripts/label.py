#!/usr/bin/env python3
"""Phase 1, layer 3: label every item of every pack with the frozen codebook, n runs.

  python3 scripts/label.py --strata A,B,C --runs 2 [--model claude-sonnet-5-5] [--workers 8]
  python3 scripts/label.py --forward <packs.json> --out-dir <dir>      # used by label_forward.py

The system prompt is codebook/labeler-v1.md (built from codebook-v1.json by
scripts/freeze_codebook.py); the user message is one pack with an opaque id and no
outcome. Each call is isolated (scripts/llm.py). Results: labels/v1/run<k>/<pack id>.json;
existing files are skipped, so a rerun resumes. Large packs (more than CHUNK items) are
labelled in chunks of CHUNK items, each chunk carrying the whole baseline and context,
so one call never has to emit hundreds of rows.
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import llm  # noqa: E402

CHUNK = 40
VERSION = 'v1'


def valid(j, n, ids):
    if not j or not isinstance(j.get('items'), list) or len(j['items']) != n:
        return False
    return [x.get('i') for x in j['items']] == ids


def label_pack(p, out, model, system, arm):
    if os.path.exists(out):
        return 'skip'
    ev = p['evidence']
    chunks = [ev[k:k + CHUNK] for k in range(0, len(ev), CHUNK)] or [[]]
    rows, metas = [], []
    for c in chunks:
        q = dict(p)
        q['evidence'] = c
        ids = [e['i'] for e in c]
        user = ('Label every evidence item in this pack. Reply with the JSON object only.\n\nPACK:\n' +
                json.dumps(q, ensure_ascii=False, indent=1))
        ok = False
        for attempt in range(3):
            try:
                text, meta = llm.call(system, user, model, arm, p['id'], timeout=1800)
            except llm.BudgetExceeded:
                raise
            except RuntimeError as e:
                text, meta = f'[failed: {e}]', {}
            j = llm.parse(text)
            metas.append(meta)
            if valid(j, len(c), ids):
                rows += j['items']
                ok = True
                break
        if not ok:
            json.dump({'_failed': True, '_raw': text[:3000], '_meta': metas}, open(out + '.failed', 'w'))
            return 'failed'
    json.dump({'pack': p['id'], 'codebook': VERSION, 'items': rows, '_meta': metas}, open(out, 'w'), ensure_ascii=False)
    return 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strata', default='A,B,C')
    ap.add_argument('--runs', type=int, default=2)
    ap.add_argument('--model', default='claude-sonnet-5-5')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--forward')
    ap.add_argument('--out-dir')
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    system = open(f'{SV}/codebook/labeler-{VERSION}.md').read()
    jobs = []
    if a.forward:
        packs = json.load(open(a.forward))
        for k in range(a.runs):
            d = f'{a.out_dir}/run{k}'
            os.makedirs(d, exist_ok=True)
            jobs += [(p, f'{d}/{p["id"]}.json') for p in packs]
        arm = 'forward_labels'
    else:
        packs = []
        for s in a.strata.split(','):
            packs += json.load(open(f'{SV}/data/packs-{s}.json'))
        if a.limit:
            packs = packs[:a.limit]
        for k in range(a.runs):
            d = f'{SV}/labels/{VERSION}/run{k}'
            os.makedirs(d, exist_ok=True)
            jobs += [(p, f'{d}/{p["id"]}.json') for p in packs]
        arm = 'labels'
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(lambda j: label_pack(j[0], j[1], a.model, system, arm), jobs))
    from collections import Counter
    print(Counter(res), llm.spent())


if __name__ == '__main__':
    main()
