---
name: earnings-deep-research
description: Stage D. Deep, one-by-one research on three US companies reporting earnings in the day's window, drawn at random from the names stage E hunts. One deep-question-researcher per name freezes the key questions the reaction will turn on and a quick first read, then researches each question its own way and returns stage E's finding contract plus the questions, evidence and confidence. Writes to its own edge-deep/ directory and places no orders. Use when asked to run stage D, the deep research stage, or the three-name deep dive.
---

# Stage D — three names a day, researched in depth, one by one

Stage D was added on 2026-10-07 on the operator's idea. It asks: **does researching a few
names in real depth, organised around the questions the reaction will turn on, beat
stage E's one-hunter-per-name breadth and stage E-P's panel, on the same names?**

Read the history before you believe in depth. Retired stage 2 wrote one deep dossier per
name (75 over 20 days) and went 39/75 on direction, +0.69% a trade against +1.24% for
shorting the same names blind, its ten most confident reads 4/10 (`archive/README.md`).
On 187 resolved names the names a hunter was most sure about moved LESS than the average
name (`research/analyses/judge-lab/`). So this stage carries two controls inside every
hunt, and they are the point of it: **the key questions are frozen before the research**,
so they can be scored after the print, and **a quick first read is frozen before the
depth**, so depth can be measured against no depth on the same name and model.

This file is an overlay, not a copy: follow `.claude/skills/earnings-edge-hunt/SKILL.md`
for steps 0, 1, 2, 2b, 5 and the standing rules, and do differently only what the table
and the steps below say. Read `CLAUDE.md` first, then the stage E skill in full, then come
back here.

## The overrides

| Stage E does | Stage D does instead | Why |
| --- | --- | --- |
| writes to `<RUN>/edge/` | writes to **`<RUN>/edge-deep/`**, every file, same layout, plus `pick.json` | Stage E and E-P write to their own directories the same day. |
| hunts every confirmed name | hunts **three names, drawn at random** by `deep_pick.py` | Depth costs turns. Random, seeded by date, so nobody chooses the names and each pick also has a stage E and E-P score. |
| launches `unpriced-hunter` | launches **`deep-question-researcher`** (Opus 5.5 at maximum effort, a ceiling of 400 turns, `Bash` for curl and arithmetic; it finishes when its questions are answered and ends with an investment decision) | Generated from `unpriced-hunter.md` plus `config/deep-addendum.md` by `scripts/sync_hunter_core.py`; same event check, source rule and output contract, so `impact_sum` sits on stage E's scale. |
| launches `edge-sweep` | **the same `edge-sweep`**, on the whole universe | The pool the draw comes from must be the names stage E would hunt. |
| step 0b sells, step 6b buys | **neither. No `alpaca_trade.py` call of any kind, not `mode`, not `plan`, not `status`.** | Stage E trades the one paper account. |
| runs the V2 shadow ledger (6c) and `edge_grounded_score.py` (5b) | **skips both** | The shadow ledger is stage E's to feed; V2 on three names adds nothing to read. |
| step 2b stamps `--market US` | step 2d stamps **`--market US-D`** on `<RUN>/edge-deep`, after the draw | Records `deep-question-researcher`'s prompt version (`us-deep.vN`). |
| run-log headings `Edge hunt — …`, publish `edge hunt: …` | **`Deep research — …`** and **`deep research: …`** | All stages append to one `_run-log.md`. |

Every `--run <RUN>/edge` in the stage E skill becomes `--run <RUN>/edge-deep`. Never read
stage E's or E-P's files while the research runs: the researchers must be blind to the
arms they are compared against. The one exception is step 6, at the very end.

## 1–2. Universe, baselines, sweep: as stage E

Stage E's steps 0, 1 and 2 into `<RUN>/edge-deep/`: `edge_universe.py --window`, one
`priced_in.py` per `(date, session)` group into `<RUN>/edge-deep/baselines/`, then one
`edge-sweep` agent writing `<RUN>/edge-deep/sweep.json`. Then the heartbeat:

```bash
python3 scripts/run_log.py --date <D> --heading "Deep research — <D> — STARTED" --line "<n> names in the window"
EARNINGS_DATA_BRANCH=main scripts/publish.sh "deep research: started for <D>"
```

## 2c. Draw the three names

```bash
python3 researcher_us/scripts/deep_pick.py --run <RUN>/edge-deep
```

**Everything is scored before today's US close, for every name** (operator's instruction,
2026-10-07). An amc name reports after today's close and a bmo name before tomorrow's
open, and both windows start at today's close, so both are researched and scored today.
Re-read the clock with `date -u` first. If it is past **15:00 ET**, there is no time to
research before the close: publish a run-log line and a note saying the fire was too late,
and stop. `--no-amc` is kept in the script for history and is no longer used. Never re-draw
to get "better" names, and never swap a picked name by hand; a name whose hunt fails stays
in `pick.json` and goes in the note as failed.

If the pool is empty, publish the run log line and the note saying so, and stop.

## 2d. Stamp provenance (after the draw, before the researchers)

```bash
python3 scripts/provenance.py stamp --run <RUN>/edge-deep --market US-D --orchestrator-model "<model>"
```

## 3. Three deep researchers, in ONE message, in parallel

Launch one `deep-question-researcher` per picked name. Give each exactly: ticker,
company, event date and session, the absolute path to its `baselines/<TICKER>.json`, its
output path `<RUN>/edge-deep/hunts/<TICKER>.json`, its own work directory
`<RUN>/edge-deep/work/<TICKER>/` (create all three before launching) with the line **"Write
drafts, freezes and downloads only in your work directory; never use /tmp or a shared
scratch folder, and never read another ticker's files"**, its row from `sweep.json`, and for
EVERY name, amc and bmo alike, the line **"Your research stops at 15:30 ET today (run
`date -u`); emit what you have by then."** Nothing else: not your view, not the other names, not stage E's or E-P's
files.

**If `deep-question-researcher` comes back "not found"** (an agent definition added on a
branch is invisible until main carries it, and a definition written in this session is
invisible to it), launch `general-purpose` with `.claude/agents/deep-question-researcher.md`'s
body pasted in and `model: opus`. Record which form ran in the run log.

Check each hunt as it lands: it must carry `questions_frozen`, `pre_research`,
`key_questions`, `premortem`, `pre_lessons` and `investment_decision`. A hunt missing `questions_frozen` or
`pre_research` is scored like any other, flagged in the run log, and never repaired by
hand: a reconstructed freeze is not a freeze. Publish after each hunt lands.

## 5. Score, before 16:00 ET

Score as soon as the last hunt lands and in any case before the 16:00 ET close: a score
written after the close of the day the window starts is not a forecast. If a hunt is still
running at 15:40 ET, score without it and say so in the note.

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>/edge-deep
python3 researcher_us/scripts/edge_context.py --run <RUN>/edge-deep || true
```

Three names are not a ranking. `edge_score.py` writes the same files as for stage E so
the scorers, `edge_resolve.py` and the comparison read them unchanged; nothing about a
three-name order is evidence.

## 6. The note

`<RUN>/edge-deep/edge-note.md`, answer first:

1. Three lines at the top: **this is stage D: three names drawn at random, one deep
   Opus 5.5 researcher each, no orders**; which names; that three names on one day are an
   anecdote.
2. One section per name: the frozen key questions in a table (question, priced answer,
   our answer, confidence, impact), then `p_up`, `abs_move_pct`, `impact_sum` and the
   quick first read beside them (how far did depth move the number?), the premortem in
   two lines, and the **investment decision** (action, conviction, reason, what would
   change it). The decision is research output for the operator; this stage places no
   orders.
3. **Only now** read `<RUN>/edge/edge-scores.json` and `<RUN>/edge-panel/edge-scores-panel.json`
   if they exist, and add a table: per name, stage D `impact_sum`, stage E `impact_sum`,
   E-P `panel_score` and `selected`. Where the signs disagree, one line each. If either
   file is not there yet, say so; do not wait for it.
4. What the numbers are not: no hit rate exists until names resolve, and the pooled
   comparison needs weeks of days before it can tell anything.

**The closing chat reply** starts with the verbatim output of
`python3 scripts/score_report.py --run <RUN>/edge-deep --label "Stage D (deep)"`, then the
comparison table from the note. Finish with `python3 scripts/update_index.py` and
`EARNINGS_DATA_BRANCH=main scripts/publish.sh "deep research: <what> for <D>"`.

## 7. Resolve and score the questions, once the window closes

```bash
python3 researcher_us/scripts/deep_compare.py --questions-template --run <RUN>/edge-deep
```

writes `question-verdicts.json`, one row per frozen question. Fill it from the release,
the call and the reaction, never before them: `was_the_line` (did the reaction turn on
this question), `answered_right` (did the release answer it the way stage D said), and
per name `missed_line` (what the stock did trade on, when no question named it), each
with the evidence. Then the pooled comparison:

```bash
python3 researcher_us/scripts/deep_compare.py -o researcher_us/analysis/deep-compare.json
```

It pools names over every `edge-deep` run and reports, per arm (deep, deep scaled, the
quick first read, stage E, E-P panel, minus the 20-day run-up): sign hits with a binomial
p, the return of trading the sign with t, Spearman ρ with a permutation p; and paired on
the same names, McNemar on sign for deep against the quick read, stage E and E-P. Below
20 resolved names it prints counts only and says the sample is too small. **Never pool
two prompt versions of `deep-question-researcher`** (`provenance.json`), and judge this
stage only on its own resolved runs.

This is research, not investment advice.
