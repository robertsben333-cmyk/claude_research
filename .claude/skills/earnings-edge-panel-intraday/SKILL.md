---
name: earnings-edge-panel-intraday
description: Stage E-PI. Stage E-P (Opus 5.5 searchers and a blind four-model panel) re-run from scratch at fixed New York times through the US session - 10:00, 12:00, 14:00 and 16:00 - each run saved as its own snapshot so the development of every name's call through the day can be read. Writes edge-intraday-<HHMM>/ snapshots and an edge-intraday/timeline.md, never touches stage E-P's files or its panel history, and places no orders. Use when asked to run stage E-PI, the intraday panel, or an intraday snapshot of the US panel.
---

# Stage E-PI — the intraday panel

Built 2026-10-14 on the operator's instruction: *"a routine for the US that does the same
as US-panel, but runs it independently every 1,5 hours starting from 10.00, and saves
these so we can see the development"*, moved the same day to every two hours so one
Routine covers it: 10:00, 12:00, 14:00 and 16:00 New York.

Each fire is ONE snapshot. It is stage E-P, run exactly as
`.claude/skills/earnings-edge-panel/SKILL.md` runs it (which is itself an overlay on
`.claude/skills/earnings-edge-hunt/SKILL.md`), with the differences in the table below.
Read `CLAUDE.md`, then the stage E skill, then the stage E-P skill, then come back here.

The question it can answer: **does the panel's call on a name move through the day, and
does the call nearer the print do better than the call earlier in the day?** It cannot
answer that from one day. It is never pooled with stage E-P: the provenance market is
`US-PI`, the stage version `us-panel-intraday.vN`, and stage E-P's 13:06 run is shown
beside the snapshots as a reference column only.

## The overrides on stage E-P

| Stage E-P does | Stage E-PI does instead | Why |
| --- | --- | --- |
| writes to `<RUN>/edge-panel/` | writes to **`<SNAP>` = `<RUN>/edge-intraday-<HHMM>/`**, every file, E-P's layout | One directory per snapshot, the date still its parent, so every per-run script works unchanged. `intraday.py slot` names it. |
| builds its own universe and sweep | **the first snapshot of the day builds them and freezes them** (`intraday.py freeze`); every later snapshot copies them in (`intraday.py seed`) and skips the sweep | Every snapshot answers about the same names, so the only things that move are the evidence and the clock. |
| hunts every confirmed name | **a snapshot at or after 16:00 ET hunts bmo names only** | At 16:00 tonight's amc names are releasing; a searcher reading the release is reporting the outcome. |
| scores whatever the searchers wrote | **runs `intraday.py guard` between the searchers and `edge_score.py`** | An amc hunt written at or after 16:00 ET on its event date may have read the release. The guard moves it and its baseline to `<SNAP>/_after_release/`, which nothing scores. |
| `panel_score.py --run <RUN>/edge-panel` | **`panel_score.py --run <SNAP> --dry-run --stage E-PI`** | `--dry-run` keeps `researcher_us/analysis/panel-history.json` untouched: it is the reference every judge's percentile is read against, and four snapshots a day of one day's names would swamp it. Each judge is still read against stage E-P's live range from runs dated before today. |
| stamps `provenance.py stamp --market US-P` | stamps **`--market US-PI`** on `<SNAP>` | Its own stage label and prompt version. |
| runs `edge_grounded_score.py` (step 5b) and `edge_context.py` (step 6d) | **skips both** | The V2 grounded score and the context labels describe the name, not the time of day, and stage E-P already writes them for these names. |
| run-log headings `Edge hunt (panel) — …`, publish `edge hunt panel: …` | **`Intraday panel <HH:MM> — …`** and **`intraday panel <HH:MM>: …`** | Several sessions append to one `_run-log.md`. |
| the note `<RUN>/edge-panel/edge-note.md` | a short **`<SNAP>/edge-note.md`** plus the day's **`<RUN>/edge-intraday/timeline.md`** | The timeline is the deliverable: one row per name, one column per snapshot. |

Everything else is stage E-P's: `unpriced-searcher` (with stage E's fallback), the same
sealed-baseline rules, step 5p's packs, four judges in ONE message with only the packs
file and their output path, the coverage check, the provenance `panel` block.

**YOU PLACE NO ORDERS.** No `alpaca_trade.py` call of any kind, not `mode`, not `plan`, not
`status`. No V2 shadow ledger. Never write into `<RUN>/edge/`, `<RUN>/edge-panel/` or
another snapshot's directory. Never read stage E's or E-P's files except, for the
timeline, `<RUN>/edge-panel/edge-scores-panel.json`, which `intraday.py timeline` reads
itself.

## 0. Which snapshot is this?

```bash
python3 researcher_us/scripts/intraday.py slot
```

It prints the New York time, the snapshot label (`1000`, `1200`, `1400`, `1600`;
a fire more than 45 minutes from every slot keeps its own clock and says `on_slot:
false`), `<RUN>`, `<SNAP>`, whether the day's names are frozen, whether amc names are
excluded, and the snapshot's `status`.

- `weekday` false, or `inside_hours` false: append one line to the run log saying so,
  publish, stop.
- `status: complete`: this snapshot already ran (a re-fire). Say so in one run-log line,
  rebuild the timeline (step 6), publish, stop.
- `status: partial`: a killed earlier attempt. Resume: keep its baselines (they were
  sealed before any of its hunts), relaunch only the searchers whose hunts are missing.
  If the baselines themselves are missing, archive the directory to `<SNAP>/_attempt1/`
  as stage E's step 0 describes and start clean.
- An exchange holiday: `edge_universe.py` comes back empty. Log it and stop.

Then the heartbeat, before anything is spent:
`python3 scripts/run_log.py --date <D> --heading "Intraday panel <HH:MM> — STARTED" --line "<plan>"`
and `scripts/publish.sh "intraday panel <HH:MM>: started for <D>"`.

## 1. Names: freeze them once, then seed

**If `names_frozen` is false**, this snapshot builds the day's set:

```bash
python3 researcher_us/scripts/edge_universe.py --window -o <SNAP>/universe.json
python3 researcher_us/scripts/intraday.py prefilter --snap <SNAP>   # only when amc_excluded is true
```

then run stage E's step 1 checks and one `edge-sweep` agent into `<SNAP>/sweep.json`
exactly as stage E-P does, and freeze:

```bash
python3 researcher_us/scripts/intraday.py freeze --snap <SNAP>
```

Publish straight away, so a later snapshot finds the set. A snapshot that excludes amc
names never freezes (the script refuses): it would freeze a set without tonight's names.

**If `names_frozen` is true**, do not build a universe and do not launch a sweep:

```bash
python3 researcher_us/scripts/intraday.py seed --snap <SNAP>
```

It writes `<SNAP>/universe.json`, `<SNAP>/sweep.json` and `<SNAP>/intraday.json`, whose
`hunt` list is the names this snapshot hunts and `excluded` says what it left out and why.

## 2. Seal, stamp, hunt

Seal **this snapshot's own** baselines with `priced_in.py` into `<SNAP>/baselines/` for the
`hunt` names, one call per `(date, session)` group, before any searcher launches. Every
snapshot re-seals: the spot, the tape and the option chain at this hour are part of what
the snapshot measures. Commit and publish the baselines. Then:

```bash
python3 scripts/provenance.py stamp --run <SNAP> --market US-PI --orchestrator-model "<model>"
```

**At most 19 names a snapshot** (`edge_panel_intraday.hunted_names`): stage E-P hunts up
to 30 since 2026-10-21, the snapshots do not, because 30 do not finish inside a two-hour
slot reliably. Shed by `budget.edge_degrade_order` at 19.

Launch one `unpriced-searcher` per name in stage E's waves, each with exactly what stage
E-P gives it (ticker, company, event date and session, its baseline path, its output path
`<SNAP>/hunts/<TICKER>.json`, its sweep row). Nothing about earlier snapshots, ever: a
searcher that sees the 10:00 call is no longer independent of it.

**amc names first.** An amc name must be hunted before 16:00 ET or the guard drops it.
On the 14:00 snapshot start every amc searcher in the first wave.

## 3. The guard, then score

As soon as the last searcher returns, before anything reads the hunts:

```bash
python3 researcher_us/scripts/intraday.py guard --snap <SNAP>
python3 researcher_us/scripts/edge_score.py --run <SNAP>
```

The guard reads each hunt file's write time, so run it in the same session that wrote
them, never after a fresh checkout. Every name it moves goes in the run log.

## 4. The panel

Stage E-P's step 5p, on `<SNAP>`, with two changes in the combine step:

```bash
python3 researcher_us/scripts/panel_packs.py --run <SNAP>
# four judges, one message, packs path + output path only
python3 researcher_us/scripts/panel_score.py --run <SNAP> --dry-run --stage E-PI
```

`--dry-run` is not optional. Record the `panel` block in `<SNAP>/provenance.json` as stage
E-P does.

## 5. The snapshot note

`<SNAP>/edge-note.md`, short: this is stage E-PI, snapshot `<HH:MM>` New York, Opus 5.5
searchers and a blind four-model panel, no orders; which judges ran; what was excluded or
guarded and why; then the panel table exactly as `panel_score.py` printed it. One day is
an anecdote, and the snapshots of one day share names and a market, so they are not
independent evidence. End with the disclaimer.

## 6. The timeline — the deliverable

```bash
python3 researcher_us/scripts/intraday.py timeline --run <RUN>
```

It rebuilds `<RUN>/edge-intraday/timeline.{json,md}` from every snapshot written so far:
per name, `panel_pct` with its side at each snapshot (`*` = selected), stage E-P's 13:06
run beside them for reference, the number of side flips and how often the name was
selected. Rebuild it on every fire, also on a re-fire.

Then `python3 scripts/update_index.py` and
`scripts/publish.sh "intraday panel <HH:MM>: <n> names for <D>"`, with
`EARNINGS_DATA_BRANCH=main` exported, and check `git log --oneline -1 origin/main`.

**The closing reply**: the panel table, then the timeline table as `timeline` printed it,
then which judges ran, what was excluded or guarded, and anything that failed.

## 7. Resolve

Each snapshot resolves as its own run: `edge_resolve.py --run <SNAP>`. The question is
pooled, never one day: per slot, over many days, do the selected names move and pay, and
is the later call better than the earlier one on the same names? Judge each
`us-panel-intraday` version on its own resolved runs and never pool it with stage E-P.

This is research, not investment advice.
