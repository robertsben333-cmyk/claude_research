#!/usr/bin/env python3
"""Freeze codebook v1: codebook/codebook-v1.json, codebook/codebook.md, codebook/labeler-v1.md.

  python3 scripts/freeze_codebook.py

The subtypes, groups and precedence rules are the Opus design call's (codebook/design-raw.json),
unedited. The item flags are the prompt's list, defined here. Refuses to overwrite an existing
v1 once labels exist (a change after that is v2).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)

FLAGS = [
    ('quantified', 'bool', 'The item states a number about the claim (a figure, a percentage, a count, a date-bound amount). A number that is only a date or a page reference does not count.'),
    ('dated_in_window', 'bool', "The item's source or event is dated after the company's PREVIOUS quarterly results and on or before the baseline's seal (`sealed_utc` / `as_of`), i.e. it is new since the last print. False when it is older, or undated."),
    ('about_focal_company', 'bool', 'The claim is about the company being researched itself (not a peer, the sector or the macro).'),
    ('primary_document', 'bool', 'The item quotes or reads the ORIGINAL document or data (the filing, the release, the docket, the register, the data series itself), not an article or portal ABOUT it.'),
    ('already_widely_reported', 'bool', 'Headline news, the public guide, consensus, or something any reader of the company would already know before the seal. Your judgement from the text; obscure filings, niche data and fresh items are false.'),
    ('contradicted_in_pack', 'bool', 'Another item in THIS pack contradicts it (a different figure, the opposite fact, a correction).'),
    ('n_independent_sources', 'int', 'How many independent sources the item itself cites or the pack shows for the same fact (1 if one source; 0 for a search note with no source). Republications of one document count once.'),
    ('language', 'str', 'Two-letter code of the source language (en, de, fr, ja, sv, ...). Use the language of the cited source when visible, else of the item text.'),
    ('direction', 'int', "What the item, taken alone, implies for the stock's reaction to THIS print: +1 up, -1 down, 0 neither or unclear. A search note is 0 unless it states a directional absence (e.g. 'no warning found despite a weak quarter'). Use the item's own content; do not forecast."),
    ('magnitude_claim', 'str', "none / small / large: does the item claim something big RELATIVE TO THE MOVE THE BASELINE PRICES (the option-implied move, else the past reactions)? 'large' = could by itself move the stock by as much as is priced or more; 'small' = a fraction of it; 'none' = no size claim."),
]


def main():
    out = f'{SV}/codebook/codebook-v1.json'
    if os.path.exists(out) and os.path.isdir(f'{SV}/labels/v1') and '--force' not in sys.argv:
        sys.exit('codebook v1 exists and labels exist: make v2 instead')
    d = json.load(open(f'{SV}/codebook/design-raw.json'))
    j = d['parsed']
    cb = {'version': 'v1', 'frozen_utc': '2026-10-05', 'designed_by': d['meta'].get('model_usage'), 'design_cost_usd': d['meta'].get('cost_usd'),
          'groups': j['groups'], 'subtypes': j['subtypes'], 'precedence': j['precedence'], 'design_notes': j.get('notes'),
          'flags': [{'name': n, 'type': t, 'definition': df} for n, t, df in FLAGS]}
    json.dump(cb, open(out, 'w'), indent=1, ensure_ascii=False)
    # human-readable
    L = ['# Codebook v1: source subtypes and item flags', '',
         'Frozen 2026-10-05, before any outcome was joined to a v1 label. Designed by one Opus 5.5 call',
         '(`scripts/codebook_design.py`) on every item of a seeded random 15% of the packs (41 packs, 674',
         'items) with the mechanical fields, and no outcome; the subtypes, groups and precedence rules are',
         'that call\'s, unedited. The flags are the study prompt\'s list, defined in `scripts/freeze_codebook.py`.',
         'Never edited after outcomes are joined: a change is v2, reported beside v1.', '', '## Groups', '']
    for g, t in j['groups'].items():
        L.append(f'- **{g}**: {t}')
    L += ['', '## Subtypes', '', '| id | group | name | definition | decision rule |', '|---|---|---|---|---|']
    for s in j['subtypes']:
        L.append(f"| `{s['id']}` | {s['group']} | {s['name']} | {s['definition']} | {s['decision_rule']} |")
    L += ['', '## Precedence', ''] + [f'- {p}' for p in j['precedence']] + ['', '## Item flags', '']
    for n, t, df in FLAGS:
        L.append(f'- `{n}` ({t}): {df}')
    L += ['', f"Design notes: {j.get('notes')}", '']
    open(f'{SV}/codebook/codebook.md', 'w').write('\n'.join(L))
    # labeller prompt
    sub = '\n'.join(f"- `{s['id']}` ({s['group']}): {s['name']}. {s['definition']} Rule: {s['decision_rule']}" for s in j['subtypes'])
    flags = '\n'.join(f'- `{n}` ({t}): {df}' for n, t, df in FLAGS)
    prec = '\n'.join(f'{p}' for p in j['precedence'])
    P = f"""# Evidence labeller (codebook v1)

You label the evidence that an earlier researcher collected about one listed company shortly
before it reported results. You never see what happened after. Do not use anything you may
know about what happened to the company after the baseline's seal time. You are not asked to
forecast; you describe each piece of evidence with a fixed codebook, the same way for every
company.

The user message holds one pack: a `baseline` (what the market had priced: an option-implied
move where one exists, past reactions, run-ups, positioning), the researcher's
`first_hunter_context`, and a numbered list of `evidence` items. Each item has a `kind`:

- `filed_by_first_hunter`: the researcher filed it as a finding;
- `put_outside_window_by_first_hunter`: judged real but landing after this print;
- `rejected_by_first_hunter`: considered and dropped;
- `listed_as_searched_and_found_nothing`: a place the researcher searched and found nothing;
- `dossier_claim`: one cited claim from a research dossier (its `section` says where it sat).

Some packs are anonymised: the company is `[THE COMPANY]` and URLs are removed. Label them the
same way from the text. A pack may hold only part of a company's items (large packs are sent
in chunks); label exactly the items you are given.

## Subtype: exactly one per item, from this closed list

{sub}

### Precedence (apply in order when two subtypes fit)

{prec}

## Flags: every item

{flags}

## Output

Reply with ONE JSON object and nothing else:

{{"items": [{{"i": <index>, "subtype": "<id>", "quantified": true|false, "dated_in_window": true|false,
"about_focal_company": true|false, "primary_document": true|false, "already_widely_reported": true|false,
"contradicted_in_pack": true|false, "n_independent_sources": <int>, "language": "<xx>",
"direction": -1|0|1, "magnitude_claim": "none"|"small"|"large"}}, ...]}}

One entry per evidence item, in the order given, with its `i`. Use only subtype ids from the list.
"""
    open(f'{SV}/codebook/labeler-v1.md', 'w').write(P)
    print('subtypes', len(j['subtypes']), 'prompt chars', len(P))


if __name__ == '__main__':
    main()
