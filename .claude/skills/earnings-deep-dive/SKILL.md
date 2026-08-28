---
name: earnings-deep-dive
description: Stage 2 of the daily earnings pipeline. Spawns one deep-research subagent per shortlisted company (Opus, high effort) to produce a fully sourced pre-earnings dossier, then ranks the results for the persona panel. Use when asked to run stage 2, run the deep dives, or research the shortlist.
---

# Stage 2 — Deep dossiers

Ten companies, ten independent deep-research subagents, one exhaustive sourced dossier
each. This is where the pipeline's research actually happens.

How many firings this takes is `deep_dive.batches`, and it is a usage decision, not an
implementation detail. **It is currently 1**: one research group of three names, run in
waves, in a single firing. The two-batch split it replaced was meant to spread the load
over two usage windows; in practice it gave the day two chances to be killed instead of
one, and the second batch took them. Split into batches again only above roughly five
researchers a day.

## 1. Load state

```bash
python3 scripts/run_paths.py --json
```

Read `01-shortlist.json` and `config/pipeline.yaml`.

**Take at most `triage.shortlist_size` names, highest `priority_score` first.** A
shortlist published before a budget change can be longer than the current cap — on
2026-08-13 a 10-name shortlist was sitting in front of a config that had been cut to 6 —
and quietly researching all of them puts back exactly the spike the cap was meant to
remove. Record in the run log any name you dropped for this reason.

Determine which batch you are: the routine prompt says `batch <k>`. Batch *k* takes
capped positions (k−1)·N+1…k·N, where N = ceil(capped_len / `deep_dive.batches`).

**At the current setting, `deep_dive.batches` is 1** — there is one stage-2 firing and
batch 1 is the entire capped shortlist. A prompt that says `batch 2` under this setting
is a Routine that should have been paused: it has nothing assigned to it, so verify the
dossiers exist, do the ranking if it is missing, and say so in the log rather than
re-researching anything.

If you are covering both halves because the other batch failed, the cap still applies to
the day as a whole: research up to `triage.shortlist_size` names total, not per batch.

Before starting, check `02-dossiers/` for dossiers that already exist. **Skip any ticker
that already has both a `.md` and a `.json`.** Routines get re-run, sessions get
retried, and re-researching a finished name is pure waste. If an earlier batch failed
entirely, a later one should notice the gap and cover both — say so in the log if you
do.

If `01-shortlist.json` does not exist, stage 1 has not published. Do not invent a
shortlist. Log the block (step 1a) and stop — but check first whether stage 1's Routine
simply has not fired yet, and if the shortlist is merely late, prefer running the
`earnings-triage` skill yourself over losing the day.

## 1a. Leave a heartbeat before spending anything

**Do this before spawning a single researcher, and publish it.**

```bash
python3 scripts/run_log.py --heading "Stage 2 — deep dive, batch <k> — STARTED" \
  --line "Shortlist: <n> names; this batch: <tickers>" \
  --line "Already on disk, skipping: <tickers or none>" \
  --line "Plan: waves of <wave_size> opus/high researchers, publish after each wave"
scripts/publish.sh "stage 2 batch <k>: started for <YYYY-MM-DD>"
```

This costs one cheap commit and it is the only reason tomorrow's you can tell a
Routine that never fired from a session that fired and died on its first researcher.
Those two have completely different fixes. Between 2026-08-08 and 2026-08-12 the deep
dive published *nothing at all* on four consecutive days, and because there was no
heartbeat, stage 3 could only record "stage 2 never ran, or ran and failed before
completing its first name" — which is not a diagnosis.

## 2. Spawn the researchers, in waves

One `earnings-deep-researcher` subagent per ticker — but **not the whole batch at
once**. Launch them in waves of `deep_dive.wave_size` (default 2), and publish after
every wave before starting the next.

Launching a batch in parallel looks faster and is strictly worse. Nothing is on disk
until the first agent returns, so a session killed during the fan-out — usage limit,
container reclaim — leaves no dossier, no log line, nothing. A wave that completes is
banked; a wave that dies costs one wave.

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

Opus/high researchers are long and heavy, and sessions do run out. A real run died
partway through batch 1 with two names still unwritten — the three that had already been
pushed survived, and they only survived because they had been pushed. A commit per
dossier costs seconds and is the difference between losing one name and losing the batch.

**If a wave returns nothing at all, stop the batch.** Two researchers that both come
back empty — or a wave that returns in a couple of minutes on an implausible token
count — is the usage limit biting, not a research failure. Starting the next wave in
that state burns the rest of the day's allowance for nothing. Record it and go to
step 5:

```bash
python3 scripts/run_log.py --heading "Stage 2 — deep dive, batch <k> — HALTED" \
  --line "Completed before halting: <tickers or none>" \
  --line "Not researched: <tickers>" \
  --line "Reason: <what the failure actually said>"
```

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

Only the **final** batch ranks — batch *k* where *k* equals `deep_dive.batches`. At the
current setting of 1, batch 1 *is* the final batch and must produce the ranking. If an
earlier batch is running, skip this step.

Stage 3 cannot run without `02-ranking.json`. A day that produces dossiers and no
ranking has paid for the research and thrown away the deliverable.

## 5. Log and publish

Append to `_run-log.md` (one section per batch, do not overwrite the other batch's):

```markdown
## Stage 2 — deep dive, batch <k> — FINISHED (<HH:MM> UTC)
- Researched: <tickers>
- Skipped (already done): <tickers or none>
- Failed: <ticker (reason) or none>
- Subagents: <n> opus/high, in <w> waves of <wave_size>
- Median evidence completeness: <n>/100
- Panel-eligible after this batch: <tickers>       # final batch only
```

Timestamp in **UTC**. Sessions have repeatedly guessed their own local time wrong and
written a CEST time that is an hour or two off, which makes the log useless for working
out what ran when. `scripts/run_log.py` stamps UTC for you.

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
