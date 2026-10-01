#!/usr/bin/env python3
"""Stage E-P: turn the day's searcher hunts into blind packs for the four-model panel.

One pack per rankable name: the sealed baseline (trimmed), the context the searcher wrote
(bar, positioning), and every item it surfaced, numbered, tagged with how the searcher
classified it, with its sizes, verdicts and final numbers removed. This is the exact
format the four-model re-judge was measured on (research/analyses/rejudge-four-models/,
research/analyses/judge-lab/), so the live panel judges what the measurement judged.

  python3 researcher_us/scripts/panel_packs.py --run research/<Y>/<M>/<DATE>/edge-panel

Writes <RUN>/panel/packs.json, pretty-printed one field per line so a Read-only judge can
page through it. Names that edge-scores.json marks not rankable (killed, folded share
class, no event) are left out, because the panel ranks what the stage ranks.
"""
import argparse, json, os, re, sys
from pathlib import Path

# sizing language the searcher writes into prose: removed so a judge cannot anchor on it
SIZE = re.compile(r'\b[Ss]ized? (at|to) [^.;]*|\bcut (it )?from [-+]?\d[^.;]*|\(lesson[^)]*\)|'
                  r'\blesson \d+\b[^.;]*|\bp_up\b[^.;]*|\babs_move[^.;]*|\bimpact_sum\b[^.;]*|'
                  r'\bexpected_impact[^.;]*', re.I)
DROP_KEYS = ('headlines', 'raw', 'bars', 'series')


def scrub(s):
    return SIZE.sub('[sizing note removed]', s) if isinstance(s, str) else s


def trim(o):
    if isinstance(o, dict): return {k: trim(v) for k, v in o.items() if k not in DROP_KEYS}
    if isinstance(o, list): return [trim(x) for x in o[:12]]
    if isinstance(o, str) and len(o) > 600: return o[:600] + '…'
    return o


def evidence(hunt_files):
    ev = []
    for h in hunt_files:
        j = json.load(open(h)); tag = os.path.basename(h)
        for f in j.get('findings') or []:
            ev.append({'kind': 'filed_by_first_hunter', 'hunt': tag, 'text': scrub(f.get('finding')),
                       'lands_on': f.get('lands_on'), 'leg': f.get('leg'), 'resolves_by': f.get('resolves_by'),
                       'source': f.get('source'), 'source_date': f.get('source_date'),
                       'reaction_history_on_this_line': scrub(f.get('reaction_history_on_this_line')),
                       'why_not_priced': scrub(f.get('why_not_priced')), 'independence': scrub(f.get('independence'))})
        for o in j.get('outside_window') or []:
            d = o if isinstance(o, dict) else {'finding': o}
            ev.append({'kind': 'put_outside_window_by_first_hunter', 'hunt': tag, 'text': scrub(d.get('finding')),
                       'resolves_by': d.get('resolves_by'), 'source': d.get('source')})
        for r in j.get('rejected_candidates') or []:
            ev.append({'kind': 'rejected_by_first_hunter', 'hunt': tag, 'text': scrub(r.get('candidate')),
                       'source': r.get('source'), 'first_hunter_reason': scrub(r.get('reason'))})
        for s in j.get('searched_and_found_nothing') or []:
            ev.append({'kind': 'listed_as_searched_and_found_nothing', 'hunt': tag,
                       'text': scrub(s if isinstance(s, str) else json.dumps(s))})
    for i, e in enumerate(ev): e['i'] = i
    return ev


def context(hunt_file):
    d = json.load(open(hunt_file))
    return {'bar': scrub(d.get('bar')), 'positioning_check': d.get('positioning_check'),
            'already_public': d.get('already_public'), 'new_in_release': d.get('new_in_release'),
            'session_check': d.get('session_check')}


def build(run):
    run = Path(run)
    day = next((p for p in run.parts if re.fullmatch(r'\d{4}-\d{2}-\d{2}', p)), None)
    if not day: sys.exit(f'cannot read the run date from {run}')
    rankable = None
    sf = run / 'edge-scores.json'
    if sf.exists():
        rankable = {r['ticker'] for r in json.load(open(sf)).get('ranking', []) if r.get('rankable')}
    packs = []
    for b in sorted((run / 'baselines').glob('*.json')):
        t = json.load(open(b)).get('ticker') or b.stem
        if rankable is not None and t not in rankable: continue
        hs = sorted(list((run / 'hunts').glob(f'{t}.json')) + list((run / 'hunts').glob(f'{t}-*.json')))
        if not hs: continue
        packs.append({'id': f'us/{day}/{t}', 'hunter_definition': '.claude/agents/unpriced-hunter.md',
                      'lessons_file': 'researcher_us/LESSONS.md', 'baseline': trim(json.load(open(b))),
                      'first_hunter_context': context(hs[0]), 'evidence': evidence(hs)})
    return packs


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True)
    a = ap.parse_args()
    packs = build(a.run)
    out = Path(a.run) / 'panel'; out.mkdir(exist_ok=True)
    json.dump(packs, open(out / 'packs.json', 'w'), ensure_ascii=False, indent=1)
    lines = (out / 'packs.json').read_text().count('\n')
    print(f"{len(packs)} packs -> {out / 'packs.json'} ({lines} lines)")


if __name__ == '__main__':
    main()
