"""Build the self-contained bundle Codex (ChatGPT app) judges in, for two OpenAI models.

Question (operator, 2026-10-14): would GPT-6 Astra and GPT-5.6 Sol, judging the same blind
packs as the four Claude judges, have sized the evidence usefully, and do they add anything
to the panel? First the resolved packs, before any daily use.

Two parts, each judged with the definitions the Claude judges read at the time:

  A-backtest  the four-model re-judge (../rejudge-four-models/), filtered to the names the
              panel-mean-pct backtest uses: the September Opus 5.5 hunts are left out
              (operator: `sept_opus55`, ledger.json / markets.json). US 119, EU 18, JP 3.
              Same pack files as the Claude run, minus those names, so each judge sees the
              same neighbours. Definitions as of 2a817d14, the commit the brief ran on.
  B-oktober   stage E-P's own packs, 2026-10-05 onwards, judged under config/panel-judge.md.
              Definitions as of today's main (the live judges read the version of their
              own day; the drift is in the core's wording, not its sizing rule).

Nothing in the bundle carries an outcome: no key.json, no ledger, no resolved file, no
other judge's output. The bundle is meant to be opened by Codex as a folder of its own,
NOT inside this repository, where every outcome is a file away.

  python3 research/analyses/rejudge-codex/build_bundle.py      # writes bundle/ and the zip
"""
import json, shutil, subprocess, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
REJ = REPO / 'research/analyses/rejudge-four-models'
OUT = HERE / 'bundle'
REJUDGE_COMMIT = '2a817d14'           # brief.md and the outputs were written on this tree
PACKS_A = ('us1', 'us2', 'us3', 'eu', 'apac', 'x1', 'x2')
OCT_FROM = '2026-10-05'               # first E-P day with a packs file on disk


def git_show(commit, path):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{commit}:{path}'],
                          check=True, capture_output=True).stdout


def keep_ids():
    L = json.load(open(REPO / 'dashboard/data/ledger.json'))
    led = {(n['run_date'], n['ticker']): n for n in L['names']}
    mk = {}
    for v in json.load(open(REPO / 'dashboard/data/markets.json'))['markets'].values():
        for r in v['names']:
            mk[(r.get('run_date'), r['ticker'])] = r
    keep = set()
    for k in json.load(open(REJ / 'key.json')):
        row = (led if k['region'] == 'us' else mk).get((k['day'], k['ticker']))
        if row is not None and not row.get('sept_opus55'):
            keep.add(k.get('pid', k['id']))
    return keep


def part_a(files):
    keep, n, defs = keep_ids(), {}, set()
    for p in PACKS_A:
        packs = [x for x in json.load(open(REJ / f'packs-{p}.json')) if x['id'] in keep]
        if not packs:
            continue
        files[f'A-backtest/packs/{p}.json'] = json.dumps(packs, ensure_ascii=False, indent=1).encode()
        n[p] = len(packs)
        for x in packs:
            defs |= {d for d in (x.get('hunter_definition'), x.get('lessons_file')) if d}
    for d in sorted(defs | {'config/hunter-core.md'}):
        files[f'A-backtest/{d}'] = git_show(REJUDGE_COMMIT, d)
    return n


def part_b(files):
    n, defs = {}, set()
    for f in sorted(REPO.glob('research/2026/1[0-2]/*/edge-panel/panel/packs.json')):
        day = f.parents[2].name
        if day < OCT_FROM:
            continue
        packs = json.load(open(f))
        files[f'B-oktober/packs/{day}.json'] = json.dumps(packs, ensure_ascii=False, indent=1).encode()
        n[day] = len(packs)
        for x in packs:
            defs |= {d for d in (x.get('hunter_definition'), x.get('lessons_file')) if d}
    for d in sorted(defs | {'config/hunter-core.md'}):
        files[f'B-oktober/{d}'] = (REPO / d).read_bytes()
    return n


def main():
    files = {}
    na, nb = part_a(files), part_b(files)
    for name in ('AGENTS.md', 'PROMPT.md'):
        files[name] = (HERE / name).read_bytes()
    if OUT.exists():
        shutil.rmtree(OUT)
    for rel, data in files.items():
        p = OUT / 'codex-panel-rejudge' / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    (OUT / 'codex-panel-rejudge' / 'out').mkdir(exist_ok=True)
    (OUT / 'codex-panel-rejudge' / 'out' / '.keep').write_text('')
    manifest = {'rejudge_commit': REJUDGE_COMMIT, 'part_a_names': na, 'part_b_names': nb,
                'total_a': sum(na.values()), 'total_b': sum(nb.values())}
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    z = HERE / 'codex-panel-rejudge.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in sorted((OUT / 'codex-panel-rejudge').rglob('*')):
            if p.is_file():
                zf.write(p, p.relative_to(OUT))
    shutil.rmtree(OUT)
    print(json.dumps(manifest, indent=1))
    print(f'{z.relative_to(REPO)}: {z.stat().st_size // 1024} kB')


if __name__ == '__main__':
    main()
