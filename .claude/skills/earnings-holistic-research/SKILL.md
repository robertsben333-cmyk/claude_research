---
name: earnings-holistic-research
description: Stage H. The self-revising holistic US earnings researcher. After stage E-P has run, one holistic-researcher per name (up to 12, from E-P's sweep) searches and judges in one loop under a versioned playbook and returns one view, with a long or short recommendation only where it is confident the market has not priced the reaction. A frozen copy of the first playbook runs on every name as the control. After the research it resolves past days, evaluates every playbook version, and lets holistic-reflector revise the playbook under fixed gates. Writes to edge-holistic/ and places no orders. Use when asked to run stage H, the holistic researcher, or the self-evolving researcher.
---

# Stage H: the self-revising holistic researcher

Stage H was built on 2026-11-05 on the operator's idea. It tests two things at once:

1. **Does one researcher that searches and judges in one loop, and gives one holistic
   view, beat breaking the evidence into point-sized findings?** (Stage E-P separates a
   searcher from four blind judges who size each finding.)
2. **Does an approach that revises itself on the last days' outcomes beat a frozen
   approach?** The operator's hypothesis is that the best predictor adapts to the market
   of the moment.

Question 2 is the dangerous one: a process that rewrites itself on small weekly samples
will chase noise unless something stops it. So the design keeps three things fixed while
the playbook moves: **the evaluation** (window, metrics, in `holistic.py`), **the gates**
(minimum evidence before any change, at most three small edits, no tickers in the
playbook, `config/pipeline.yaml` `edge_holistic.gates`), and **a frozen control**
(`playbook/control.md` = hp.v1, sha256 pinned in config, checked by the smoke test) that
researches every name beside the evolving playbook (since 2026-11-13; a random third
before, recorded per run as `control_design`), so every version has a paired comparison
on the same names. See `researcher_holistic/README.md`.

Read `CLAUDE.md` first. This skill borrows stage E's universe and sweep conventions but is
not an overlay: follow the steps below.

## Standing rules

- Write ONLY to `<RUN>/edge-holistic/`, plus, in step 6 only, `researcher_holistic/analysis/`
  and `researcher_holistic/playbook/` through `holistic.py` (never by hand).
- **No orders.** No `alpaca_trade.py` call of any kind, not `mode`, not `plan`, not
  `status`. No V2 shadow ledger.
- **The researchers are blind**: to stage E-P's hunts, scores and panel, to each other, to
  which arm they are on, and to your view. They may read their sealed baseline and their
  own sweep row, and nothing else of E-P's. You read E-P's panel only in step 5.
- Never edit `researcher_holistic/playbook/*.md` or `changes.jsonl` by hand. A playbook
  changes only through `holistic.py revise`, which applies the gates and logs every
  proposal, applied or rejected.
- `export EARNINGS_DATA_BRANCH=main` before every `scripts/publish.sh`.
- Never fabricate a number. Every company-specific figure carries a URL or is unavailable.

## 0. Clock, run, heartbeat

```bash
date -u
python3 scripts/run_paths.py --json
git pull --ff-only origin main || true
```

New York is UTC-5 in winter and UTC-4 in summer; anchor on New York time. If it is past
**15:00 ET** there is no time to research before the close: write a run-log line, skip to
step 6 (the learning step still runs), then publish.

```bash
python3 scripts/run_log.py --date <D> --heading "Holistic research — <D> — STARTED" --line "<plan>"
EARNINGS_DATA_BRANCH=main scripts/publish.sh "holistic research: started for <D>"
```

## 1. The names: stage E-P's sweep

Stage E-P fires at 13:06 ET into `<RUN>/edge-panel/` and has sealed its baselines and
finished its sweep long before 14:15. Pull main (above), then:

```bash
python3 researcher_holistic/scripts/holistic.py pick --run <RUN>
```

It takes the sweep-confirmed names by `hunt_priority` (cap `edge_holistic.max_names`,
12), freezes the current playbook as `playbook-a.md` and the control as `playbook-b.md`
into the run, puts every name on the control too (`control_share: 1.0` since 2026-11-13;
a date-seeded share below 1), records `control_design`, and writes `pick.json`. It
refuses if the control playbook's hash has moved. Never re-draw or swap a name.

If it exits 3 (no E-P sweep on main), stage E-P did not publish one today. Then run stage
E's skill steps 0 to 2 (`.claude/skills/earnings-edge-hunt/SKILL.md`: `edge_universe.py`,
`priced_in.py` per group, one `edge-sweep` agent) into `<RUN>/edge-holistic/source/`, and
call `pick --run <RUN> --source <RUN>/edge-holistic/source`. Say so in the run log.

Stamp provenance, then publish:

```bash
python3 scripts/provenance.py stamp --run <RUN>/edge-holistic --market US-H --orchestrator-model "<model>"
EARNINGS_DATA_BRANCH=main scripts/publish.sh "holistic research: names for <D>"
```

## 2. The researchers

One `holistic-researcher` per (name, arm) in `pick.json`. For each, get the brief:

```bash
python3 researcher_holistic/scripts/holistic.py brief --run <RUN> --ticker <T> --arm evolving|control
```

and pass that text as the whole prompt, nothing else. Not your view, not the arm, not the
other names, not any E-P file.

- **Launch a name's two arms in the same wave**, so the control never gets less time than
  the evolving researcher on the same name. Order the waves amc first, then bmo.
- At most **8 launches per orchestrator turn** and about 8 in flight: the search budget is
  shared per turn (stage E-P, 2026-10-28). End your turn and launch the next wave when a
  notification wakes you.
- **If `holistic-researcher` comes back "not found"** (a definition added on a branch is
  invisible until main carries it), launch `general-purpose` with
  `.claude/agents/holistic-researcher.md`'s body pasted above the brief and `model: opus`.
  Record which form ran in the run log.
- A hand-back that reports a refused search, or a file with `search_complete: false`, is
  unfinished. Relaunch it once in a later turn if it can still finish before 15:35 ET;
  otherwise it stays unfinished and is never scored.
- Publish after each wave lands.

## 3. Collect, before the close

At 15:45 ET at the latest, whether or not every researcher has returned:

```bash
python3 researcher_holistic/scripts/holistic.py collect --run <RUN>
```

It validates each hunt (an unfinished, contaminated, inconsistent or late file is never
scored; a recommendation that contradicts its own `p_up` is dropped), writes
`recommendations.json` and `note.md`. Then:

```bash
python3 scripts/update_index.py
EARNINGS_DATA_BRANCH=main scripts/publish.sh "holistic research: recommendations for <D>"
```

This publish must land before 16:00 ET: a recommendation written after the entry is not a
forecast.

## 4. The note

`note.md` is written by `collect`. Add to its top, by hand, three lines: that this is
stage H (holistic, self-revising, experiment, no orders), the playbook version, and that
one day is an anecdote.

## 5. Compare with stage E-P, after the publish

Only now read `<RUN>/edge-panel/edge-scores-panel.json` if it exists, and append to
`note.md` a table: per name, stage H `p_up` and action (evolving and, where run, control),
and E-P `panel_pct_signed` and `selected`. One line for each name where H and E-P disagree
in sign. Publish.

## 6. Learn: resolve, evaluate, and maybe revise

This runs on every fire, after the research is published (it may run after the close).

```bash
python3 researcher_holistic/scripts/holistic.py resolve
python3 researcher_holistic/scripts/holistic.py evaluate
```

`evaluate` prints the per-version scores, the frozen control, the paired comparison, E-P
on the same names and the **gate**. Then:

- **Gate closed and no drift alarm**: do not launch the reflector. Write one run-log line
  with the gate numbers (for example "gate closed: 14/30 names, 2/3 days on hp.v1").
- **Gate open, or drift alarm**: launch ONE `holistic-reflector` with exactly this prompt
  (fill in the paths):

  > Follow your definition. Evaluation: `researcher_holistic/analysis/evaluation.json`
  > and `.md`. Outcomes: `researcher_holistic/analysis/outcomes.json`. Playbook:
  > `researcher_holistic/playbook/current.md`; control: `researcher_holistic/playbook/control.md`;
  > change log: `researcher_holistic/playbook/changes.jsonl`. At most <max_ops> operations,
  > each citing at least <min_evidence_names_per_op> resolved names. <If drift alarm: "The
  > drift alarm is on: only revert_to is accepted.">
  > Write your proposal to `<RUN>/edge-holistic/reflection/proposal.json`.

  If it is not found, use `general-purpose` with its body pasted in and `model: opus`.
  Then apply it, whatever it says:

  ```bash
  python3 researcher_holistic/scripts/holistic.py revise --proposal <RUN>/edge-holistic/reflection/proposal.json --run <RUN>
  ```

  It applies the proposal only if every gate passes, writes the new version
  (`playbook/versions/hp.vN.md` and `current.md`) and logs it in `changes.jsonl` and
  `CHANGELOG.md`. A rejected proposal is logged with its reasons and changes nothing. Do
  not repair a rejected proposal yourself and do not re-run the reflector to get a
  different answer. Copy `evaluation.md` into `<RUN>/edge-holistic/reflection/`.

Then register the new version if one was written (it is data, not a definition, so
`provenance.py registry` is not needed: the run's `pick.json` and `provenance.json` record
the playbook version and its blob), and publish:

```bash
python3 scripts/run_log.py --date <D> --heading "Holistic research — learning step" --line "<gate, decision, version>"
EARNINGS_DATA_BRANCH=main scripts/publish.sh "holistic research: learning step for <D>"
git fetch origin main && git log --oneline -1 origin/main
```

## The closing reply

First the recommendations table from `note.md` (or "no recommendations today"), then
every name's p_up on one line, then the comparison with E-P, then the learning step: the
gate numbers, the reflector's decision and diagnosis in two lines, and the version that
tomorrow's run will use. Judge a playbook version only on its own resolved names; the
lineage row against the control tests the process, never a version. Say when a sample is
too small. This is a forecasting exercise over public information, not investment advice.
