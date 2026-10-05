#!/usr/bin/env python3
"""Run the blind evidence labeler over every pack, n times.

  python3 label.py --runs 2 [--model claude-sonnet-5-5] [--workers 8]

Each call is the isolated judge call of ../skillopt-judge (no tools, no MCP, no setting
sources, no CLAUDE.md) with labeler.md as the whole system prompt and one pack, carrying
an opaque id, as the user message. Nothing about outcomes is in either. Results land in
labels/run<k>/<pack id>.json; existing files are skipped, so a rerun resumes.
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'skillopt-judge'))
from us_judge import judge_call  # noqa: E402


def one(p, k, model, system):
    out = f'{HERE}/labels/run{k}/{p["id"]}.json'
    if os.path.exists(out):
        return 'skip'
    user = 'Label this pack. Reply with the JSON object only.\n\nPACK:\n' + json.dumps(p, ensure_ascii=False, indent=1)
    for attempt in range(2):
        try:
            text, meta = judge_call.call(system, user, model, timeout=1200)
        except RuntimeError as e:
            text, meta = f'[failed: {e}]', {}
        j = judge_call.parse(text)
        if j and isinstance(j.get('items'), list) and len(j['items']) == len(p['evidence']):
            j['_meta'] = meta
            json.dump(j, open(out, 'w'), ensure_ascii=False)
            return 'ok'
    json.dump({'_failed': True, '_raw': text[:2000], '_meta': meta}, open(out + '.failed', 'w'))
    return 'failed'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=2)
    ap.add_argument('--model', default='claude-sonnet-5-5')
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    system = open(f'{HERE}/labeler.md').read()
    packs = json.load(open(f'{HERE}/data/packs.json'))
    jobs = []
    for k in range(a.runs):
        os.makedirs(f'{HERE}/labels/run{k}', exist_ok=True)
        jobs += [(p, k) for p in packs]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(lambda pk: one(pk[0], pk[1], a.model, system), jobs))
    from collections import Counter
    print(Counter(res))


if __name__ == '__main__':
    main()
