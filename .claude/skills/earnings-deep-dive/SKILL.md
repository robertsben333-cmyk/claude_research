---
name: earnings-deep-dive
description: Stage 2 of the daily earnings pipeline. Spawns one deep-research subagent per shortlisted company (Opus, high effort) to produce a fully sourced pre-earnings dossier, then ranks the results for the persona panel. Runs in two batches per day. Use when asked to run stage 2, run the deep dives, or research the shortlist.
---

# Stage 2 — Deep dossiers

Ten companies, ten independent deep-research subagents, one exhaustive sourced dossier
each. This is where the pipeline's research actually happens.

It runs as **two batches at different times of day**. That is not an implementation
detail — it is the main reason the pipeline fits inside a usage plan. Five Opus/high
research agents in one firing is a large but survivable spike; ten is not.

## 1. Load state

```bash
python3 scripts/run_paths.py --json
```

Read `01-shortlist.json` and `config/pipeline.yaml`.

Determine which batch you are: the routine prompt says `batch 1` or `batch 2`. Batch 1
takes shortlist positions 1…N, batch 2 takes N+1…end, where N = ceil(len(shortlist) /
`deep_dive.batches`).

Before starting, check `02-dossiers/` for dossiers that already exist. **Skip any ticker
that already has both a `.md` and a `.json`.** Routines get re-run, sessions get
retried, and re-researching a finished name is pure waste. If batch 1 failed entirely,
batch 2 should notice the gap and cover both batches — say so in the log if you do.

## 2. Spawn the researchers

One `earnings-deep-researcher` subagent per ticker, up to
`deep_dive.max_concurrent_subagents` at a time (default 6; the platform cap is 20 but
crowding it makes every agent slower and the failure mode is a hard error). Launch them
in parallel within a batch.

Give each subagent exactly:

- ticker and company name
- session (BMO/AMC) and event date
- the plain-language event window
- the absolute path of the run directory to write into
- the triage `selection_rationale`, as a starting hint only — the researcher is
  explicitly free to conclude the triage read was wrong, and should say so if it was

Do **not** give a researcher another company's dossier, another researcher's findings,
or your own view of the name. Each dossier must stand on its own evidence.

**Publish after each dossier completes, not once at the end of the batch.** As soon as
a researcher returns and its `.md` and `.json` are both on disk, commit and push that
one name:

```bash
scripts/publish.sh "stage 2 batch <k>: dossier for <YYYY-MM-DD> (<TICKER>) [in progress]"
```

Five Opus/high researchers is a long, heavy session, and sessions do run out. A real run
died partway through batch 1 with two names still unwritten — the three that had already
been pushed survived, and they only survived because they had been pushed. A commit per
dossier costs seconds and is the difference between losing one name and losing five.

## 3. Handle failures

A subagent that returns without writing both files has failed. Retry it **once**. If it
fails again, record the ticker in the run log with the reason and move on — nine solid
dossiers beat eight solid ones plus an hour spent on a name whose data does not exist.

A dossier with `event_confirmed: false` is not a failure, but it is disqualified from
the panel. Keep it and mark it.

## 4. Rank for the panel

After the last batch completes, read every `02-dossiers/*.json` from the day and compute
a panel-priority score using `panel.rank_by` from the config:

```
panel_priority = 0.45 * |preliminary_direction_score|
               + 0.35 * evidence_completeness
               + 0.20 * change_expectation        (from the shortlist)
```

Weighting `evidence_completeness` this heavily is deliberate. Seven personas researching
a name whose anchors could not be found will produce seven confident-looking verdicts
built on nothing, and the synthesis will launder that into a number. A thin dossier is
a reason to *not* run the panel.

Exclude from panel eligibility any name with:

- `event_confirmed: false`
- `evidence_completeness < 50`
- no `event_implied_move_pct` **and** no historical move history — with neither anchor
  the synthesis has nothing to size a move against

Write `02-ranking.json` with every name's scores, its panel eligibility, and — for the
excluded ones — the reason. Stage 3 reads this file and does not re-derive it.

If batch 1 is running, skip this step; only the final batch ranks.

## 5. Log and publish

Append to `_run-log.md` (one section per batch, do not overwrite the other batch's):

```markdown
## Stage 2 — deep dive, batch <k> (<HH:MM> CET)
- Researched: <tickers>
- Skipped (already done): <tickers or none>
- Failed: <ticker (reason) or none>
- Subagents: <n> opus/high
- Median evidence completeness: <n>/100
- Panel-eligible after this batch: <tickers>       # final batch only
```

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage 2 batch <k>: dossiers for <YYYY-MM-DD> (<tickers>)"
```

This is the batch's closing commit; the per-dossier pushes in step 2 have already
saved the research itself. A session that dies holding unpublished dossiers has burned
the most expensive stage in the pipeline for nothing.

## 6. Report

Per ticker, one line: implied move, preliminary direction score, evidence completeness,
biggest gap. Then the panel-eligible names in rank order, and anything stage 3 should
know — a name excluded for thin evidence, a failed researcher, an unconfirmed event.
