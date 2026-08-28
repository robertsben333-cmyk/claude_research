---
name: earnings-panel-advice
description: Stage 3 of the daily earnings pipeline. Runs the seven-persona independent panel on the top-ranked names, synthesises each into a calibrated call, and writes the answer-first advice note delivered in the early evening. Use when asked to run stage 3, run the persona panel, or produce the day's earnings advice.
---

# Stage 3 — Persona panel, synthesis, and the advice note

The day's deliverable. For each of the top-ranked names: seven analysts research the
name independently through different lenses, a synthesis step aggregates their verdicts
into a calibrated call, and a dossier presents it answer-first.

Three things make this stage work, and all three are easy to break:

1. **The personas are independent.** They never see each other's verdicts, and they
   never see the stage 2 dossier. Their disagreement is the signal — a panel that has
   been allowed to converge tells you nothing.
2. **The synthesis is arithmetic, not vibes.** `scripts/synthesize.py` does the maths.
3. **The conviction gate is real.** Sometimes the honest answer is that there is no edge.

Two supporting references, read them when you reach the relevant step:
- `references/synthesis-chair.md` — aggregation rules and what the chair may override
- `references/dossier-format.md` — the exact output format

## 1. Load state

```bash
python3 scripts/run_paths.py --json
```

Read `02-ranking.json`, `01-shortlist.json`, and `config/pipeline.yaml`.

Take the top `panel.names` (currently **1**) **panel-eligible** names from the ranking. If
fewer are eligible, run fewer — never promote an ineligible name to fill a slot.

If nothing is eligible, skip to step 6 and write an advice note that says so, with the
ranked dossier summaries as the day's output. That is a legitimate result.

**If there is no `02-ranking.json` at all, you still publish.** Stage 2 dying is the
pipeline's most common failure — it happened on four consecutive days in August 2026 —
and on every one of those days stage 3 wrote a run-log entry and no deliverable, so the
archive records the outage only in prose. Instead:

- If some dossiers exist but no ranking, **build the ranking yourself** from
  `02-dossiers/*.json` using `panel.rank_by`; that is cheap and unblocks the panel.
- If there are no dossiers either, write `04-advice.md` and `04-advice.json` with
  `"status": "blocked"` and a `status_reason` naming the stage that failed, an empty
  `ranked_names`, and the shortlist as "researched: none". The validator accepts this;
  it does **not** accept invented rows.

Then say so plainly at the top of the note. A day the pipeline could not produce a call
is information, and it belongs in the archive alongside the days it could.

## 2. Build the Phase-0 anchor packet

For each name, extract from its stage 2 dossier JSON **only**:

- ticker, company name, sector
- event window in plain language, session, event date
- spot price and its as-of timestamp
- event-implied move percent, and its source
- historical realised one-day moves: the list, plus mean, median and max

That is the entire shared context. It is deliberately thin.

**Refresh the price-sensitive anchors before you pass them on.** Stage 2 runs several
hours earlier, often before the US open, so its `spot` and `event_implied_move_pct` are
usually from the prior close. Re-source both now, with a fresh as-of timestamp, and use
the refreshed values. A panel sizing a move against a stale implied move will be
confidently wrong about how much is priced in. If you cannot refresh a value, keep the
stage 2 figure but carry its original timestamp so the staleness is visible rather than
silently inherited.

**Do not pass on** the dossier's `preliminary_direction_score`, its bull/bear cases, its
prose, or anything you have concluded. If a persona is handed a directional read, it
will anchor on it, and seven anchored analysts produce one opinion wearing seven hats.

## 3. Run the panel

For each name, spawn all seven personas in parallel — one panel at a time
(`panel.max_concurrent_subagents`, default 7):

`persona-fundamental`, `persona-options-positioning`, `persona-sentiment`,
`persona-base-rates`, `persona-macro-peers`, `persona-red-team`, `persona-forensics`

Each gets the anchor packet and nothing else. Each returns one JSON verdict.

Handle failures: retry a failed persona once. If it fails twice, run the synthesis on
the remaining six and record which seat was empty — `synthesize.py` accepts three or
more verdicts. A six-analyst panel is worth reporting; a fabricated seventh verdict is
not, so never write one.

If a returned verdict is malformed, ask that persona to re-emit it as valid JSON rather
than repairing the numbers yourself.

## 4. Synthesise

For each name, write the verdicts and anchors to a temporary input file and run:

```bash
python3 scripts/synthesize.py <tmp>.json -o <run_dir>/03-panel/<TICKER>-synthesis.json
```

Then read `references/synthesis-chair.md` and review the result as chair. You may
override `call`, `certainty_tier`, or `signed_estimated_move` — but every override goes
in `chair_override_note` with its reasoning, and overrides should be rare. If you find
yourself overriding most days, the formula is wrong and should be fixed in the script
where the change is visible, not silently in prose each morning.

Assemble the full panel file `03-panel/<TICKER>.json`:

```json
{
  "ticker": "TTWO",
  "company": "Take-Two Interactive",
  "anchors": { ... the Phase-0 packet ... },
  "panel_verdicts": [ ... seven verdicts ... ],
  "synthesis": { ... the synthesis packet ... },
  "personas_missing": [],
  "independence_note": "Seven isolated subagents; each received only the Phase-0 anchors."
}
```

Validate every one:

```bash
python3 scripts/validate_stage.py panel <run_dir>/03-panel/<TICKER>.json
```

## 5. Write one dossier per panelled name

`03-panel/<TICKER>-dossier.md`, following `references/dossier-format.md` exactly:
the answer-first header, the `Prediction first` line, then the eleven sections.

The prediction goes at the top. Someone reading only the first screen must come away
with the call, the direction, the size, the probability, the certainty, and the main
caveat. Everything after that is justification.

Company-specific claims carry a citation. Draw them from the stage 2 dossier and the
personas' `key_sources` — at this point you may and should use the stage 2 research for
context and prose, because the panel has already voted and can no longer be contaminated.

## 6. Write the advice note

`04-advice.md` is the file the user actually opens. Structure:

1. **Header** — date, window, how many names were researched, how many panelled.
2. **The calls** — one compact block per panelled name: ticker, call, signed move or
   unsigned band, P(direction), certainty, one-line reason, one-line caveat, and a link
   to its dossier.
3. **Ranked field** — a table of every deep-researched name with implied move,
   preliminary read, evidence completeness, and whether it was panelled. This is what
   makes the other seven dossiers worth having.
4. **What would change these calls** — the reversal drivers that cut across names.
5. **Coverage and caveats** — thin evidence, unreachable sources, empty panel seats,
   any degradation applied for budget.
6. **The disclaimer** from `config/pipeline.yaml`, verbatim, as the last line.

Also write `04-advice.json`:

```json
{
  "schema_version": 1,
  "run_date": "2026-08-10",
  "status": "ok",
  "window_covered": "...",
  "names_researched": 6,
  "names_panelled": 1,
  "ranked_names": [
    {"ticker": "TTWO", "panelled": true, "call": "Lean Up", "signed_estimated_move": 4.2,
     "prob_direction": 63.0, "certainty_tier": "Med", "reversal_risk_tier": "Med",
     "unsigned_expected_move": 8.6, "evidence_completeness": 82}
  ],
  "degradations_applied": []
}
```

`status` is `"ok"`, `"no_names"` (ranking existed, nothing cleared eligibility), or
`"blocked"` (an upstream stage produced nothing). The latter two require a
`status_reason` and permit an empty `ranked_names`; `"ok"` requires a non-empty one.

```bash
python3 scripts/validate_stage.py advice <run_dir>/04-advice.json
```

## 7. Budget guard

Before starting, read the earlier `_run-log.md` sections. If stage 2 already shed scope
or ran long, apply `budget.degrade_order` from the config and record what you shed in
`degradations_applied` and in the run log.

At `panel.names: 1` there is no second panel to drop, so the budget guard has one job
left: **do not let the single panel become two.** Seven personas on one name, finished
and published, is the day's deliverable. A stage that runs wide and gets cut off
mid-panel means the day produces nothing at all.

## 8. Log and publish

```markdown
## Stage 3 — panel & advice (<HH:MM> CET)
- Panelled: <tickers>
- Calls: <TICKER Lean Up +4.2% (Med)>, ...
- Panel seats filled: <21/21 or note the gaps>
- Chair overrides: <none | ticker + reason>
- Degradations: <none | what was shed and why>
```

```bash
python3 scripts/update_index.py
python3 scripts/build_predictions.py
scripts/publish.sh "stage 3: advice for <YYYY-MM-DD> (<tickers>)"
```

`build_predictions.py` folds today's calls into `PREDICTIONS.csv`/`.json`, the flat
table of every prediction the pipeline has ever made. Today's rows land with
`outcome_status: pending` until stage 4 scores them tomorrow.

Publish before you write your reply. The note in the repo is the deliverable; the chat
message is a summary of it.

## 9. Report

Lead with the calls — same answer-first discipline as the dossier. One block per
panelled name, then a one-line pointer to the ranked field and the archive path. Do not
paste whole dossiers into the reply.
