---
name: earnings-edge-panel-split
description: Stage E-PS. Stage E-P's own names split over four fresh sessions of at most five, run every weekday at the same time as stage E-P on E-P's sweep rows and sealed baselines, each with its own Opus 5.5 searchers and its own blind four-model panel, scored --dry-run against E-P's history. The session runs on main with this stage's own files laid over it, and the four agree who takes which names through compare-and-swap commits on the test branch (panel_split.py claim), where all their output lands. Places no orders. Use when asked to run stage E-PS, the split panel, or one shard of it.
---

# Stage E-PS — stage E-P's names, five to a session, beside E-P

Built 2026-10-22 on the operator's instruction: *"ik heb het gevoel dat bij hoog aantal
tickers het systeem het niet goed doet. dus ik wil even 4 test routines aanmaken, die
ieder max 5 stocks beoordelen, en op de een of andere manier communiceren onderling wie
welk doet"*. Daily since 2026-10-23 (*"zet die routines voorlopig standaard op"*) and at
the same time as stage E-P (*"laat ze gelijktijdig met e-p lopen zodat ze goed te
vergelijken zijn"*). Four Routines fire a few minutes after stage E-P with the same prompt;
each session takes one shard of at most five of E-P's names.

It asks one question: **does a session carrying five names produce different evidence and a
different panel call than stage E-P's one session carrying twenty, on the same names in the
same half hour?** The 2026-10-21 run log is why it is worth asking: on 30 names one sweep
left 89 of 118 universe names unchecked, the searchers reported the session's shared
WebSearch budget running out, and the judges hit a 429 and finished after the close. Here
the sweep is E-P's own (copied, not re-run), so a shard spends its whole budget on five
searchers and four judges.

**Your checkout is main.** Stage E-P runs on main, and so do you: the searcher, the four
judges, `edge_score.py`, `panel_packs.py`, `panel_score.py`, the panel history and the
calibration are exactly E-P's today. Only this stage's own files come from the test branch
(`overlay` in `config/edge-panel-split.yaml`), laid over the checkout and never committed.

This file is an overlay: follow `.claude/skills/earnings-edge-panel/SKILL.md` (itself an
overlay on `.claude/skills/earnings-edge-hunt/SKILL.md`) for how a searcher is briefed, how
the packs and judges run and how the panel is recorded, and do differently what the table
and the steps below say. Read `CLAUDE.md`, then the stage E skill, then the stage E-P
skill, then come back here.

## The overrides on stage E-P

| Stage E-P does | Stage E-PS does instead | Why |
| --- | --- | --- |
| builds its own universe, seals 100+ baselines, runs one `edge-sweep` | **no universe, no sealing, no sweep**: `panel_split.py claim` waits for E-P's `sweep.json` on main, then copies E-P's universe rows, sweep rows and sealed baselines for this shard's names into `<SHARD>` | The names, the sweep and the searcher's inputs are E-P's, so the load per session is what differs, and the shards search while E-P's searchers do. |
| writes to `<RUN>/edge-panel/` and publishes to `main` | writes to **`<SHARD>` = `<RUN>/edge-split-<k>/`**, E-P's layout, and publishes it to `edge_panel_split.data_branch` only; the day's plan, claims, run log and comparison live in `<RUN>/edge-split/` and only `panel_split.py` writes there | One directory per shard, the date still its parent, so every per-run script works unchanged. |
| up to twenty searchers in waves | **at most five, all in one message** | The point of the test. |
| step 3s sells, step 6b buys | **nothing: no `alpaca_trade.py` call of any kind**, not `mode`, not `plan`, not `status` | Stage E-P is the only stage connected to the account. |
| `edge_grounded_score.py` (5b), `edge_context.py` (6d) | **skips both** | They describe the name, not the session load, and stage E-P writes them for these names. |
| `panel_score.py --run <RUN>/edge-panel` | **`panel_score.py --run <SHARD> --dry-run --stage E-PS`** | `--dry-run` keeps `researcher_us/analysis/panel-history.json` untouched; each judge is read against stage E-P's live range from runs before today, so the shard's percentiles sit on E-P's scale. |
| `provenance.py stamp --market US-P` | **`panel_split.py stamp --shard <k> --orchestrator-model "<model>"`** | Market `US-PS`, version `us-panel-split.vN`, registered at run time because main's `provenance.py` does not know it. Never pooled with stage E-P. |
| `scripts/run_log.py` and `scripts/publish.sh` | **`panel_split.py log` and `panel_split.py publish`, never the two scripts directly** | Your checkout is main: a plain `publish.sh` would push your shard to `main`, and `run_log.py` would write into E-P's day log. `log` appends to `<RUN>/edge-split/_run-log.md` and `publish` mirrors `<SHARD>` onto the test branch, both by compare-and-swap, so four sessions never meet in a rebase. |
| amc names are done long before the release | **`intraday.py guard --snap <SHARD>` between the searchers and `edge_score.py`** | The safety net for a shard that starts or runs late; any amc hunt written at or after 16:00 ET is moved out of the scored set. |

**YOU PLACE NO ORDERS.** Never write into `<RUN>/edge-panel/`, `<RUN>/edge/` or another
shard's directory. Never open stage E-P's hunts, packs, judge files or scores: the only
thing that reads them is `panel_split.py summary`, after your own panel is scored.

## 0. Claim a shard

```bash
python3 researcher_us/scripts/panel_split.py claim
```

Give that Bash call a timeout of 600000 ms: one call waits up to nine minutes. It waits
until stage E-P's `edge-panel/sweep.json` is on main (E-P publishes it before its first
searcher, about fifteen minutes after it fires), then builds the day's plan once from that
sweep, confirmed names first by `hunt_priority` and cut where E-P cuts (the first session to
push it wins; every other session reads that one), and claims the lowest free shard. It
prints JSON:

- **exit 3**, `retry`: run the same command again, as often as it says. It stops itself at
  14:30 ET.
- **exit 2**, `stop`: no E-P sweep on main by 14:30 ET (E-P did not run, or a holiday). Run
  `panel_split.py log --heading "stopped" --line "<reason>"` and end.
- **exit 4**: every shard is taken (a re-fire, or a fifth session). Log it the same way and end.
- **exit 0**: `shard`, `snap` (= `<SHARD>`), `names` (ticker, company, session, event date,
  hunt priority), `names_basis`. `resumed: true` means this container claimed it before:
  keep what `<SHARD>` already holds and relaunch only the searchers whose hunts are missing.

A shard with no names (a day with fewer names than shards): log it, run
`panel_split.py done --shard <k>`, end.

Then the heartbeat, before anything is spent:

```bash
python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "STARTED" --line "<names>, E-P's sweep and baselines from <source_commit>, <names_basis>"
python3 researcher_us/scripts/panel_split.py stamp --shard <k> --orchestrator-model "<model>"
python3 researcher_us/scripts/panel_split.py publish --shard <k> "split panel <k>: seeded for <D>"
```

## 1. Search — all of the shard's names in ONE message

One `unpriced-searcher` per name, every one in the same message, amc names first in the
message. Give each exactly what stage E-P gives it: ticker, company, event date and session,
the absolute path to `<SHARD>/baselines/<TICKER>.json`, its output path
`<SHARD>/hunts/<TICKER>.json`, and its sweep row (`<SHARD>/sweep-rows/<TICKER>.json`).
Where that row says `baseline_history_trustworthy: false`, or the baseline carries
`cadence_implausible`, tell that searcher so, as stage E does. A name the sweep left
unconfirmed gets what E-P tells such a searcher: settle the event and session yourself.
Nothing else: not stage E-P's hunt for the name, not the other shards, not your view. If
`unpriced-searcher` is not found, use stage E-P's fallback (`general-purpose`, its body
pasted in, `model: opus`) and record which form ran.

When the last one returns:

```bash
python3 researcher_us/scripts/intraday.py guard --snap <SHARD>
python3 researcher_us/scripts/edge_score.py --run <SHARD>
python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "searchers done" --line "<n> of <n> returned at <UTC>; guard moved <names or nothing>; any searcher that reported its search budget running out"
python3 researcher_us/scripts/panel_split.py publish --shard <k> "split panel <k>: hunts for <D>"
```

The guard reads each hunt file's write time, so run it in this session, never after a
fresh checkout. Whether a searcher said its WebSearch budget ran out is the most useful
thing this shard can report: copy each such line into the log.

## 2. The panel

Stage E-P's step 5p on `<SHARD>`, unchanged except the combine:

```bash
python3 researcher_us/scripts/panel_packs.py --run <SHARD>
# four judges in ONE message, each given only the packs path and its output path
python3 researcher_us/scripts/panel_score.py --run <SHARD> --dry-run --stage E-PS
```

`--dry-run` is not optional. The same four judges (`panel-judge-opus5`, `-opus55`,
`-sonnet55`, `-fable51`) with stage E-P's fallbacks, the coverage check, and the `panel`
block in `<SHARD>/provenance.json`. A judge that is refused or rate-limited gets one
relaunch; after that it is missing for the day and the note says so.

## 3. The shard note, done, the comparison

`<SHARD>/edge-note.md`, short: this is stage E-PS, shard `<k>` of four, run beside stage
E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and
baselines, no orders; which judges ran; what the guard moved; claim-to-done minutes; then
the panel table exactly as `panel_score.py` printed it. One day is an anecdote. End with the
disclaimer in `config/pipeline.yaml`.

```bash
python3 researcher_us/scripts/panel_split.py publish --shard <k> "split panel <k>: <n> names, <m> selected for <D>"
python3 researcher_us/scripts/panel_split.py done --shard <k>
python3 researcher_us/scripts/panel_split.py summary
```

`summary` rebuilds `<RUN>/edge-split/summary.{json,md}` from every finished shard and stage
E-P's own `edge-scores-panel.json` and hunts on main: per name, E-P's call beside the
shard's, both searchers' `impact_sum`, findings and sources, then the overlap of the
selected sets, the Spearman rho between the two signed `panel_pct` columns, and any name E-P
hunted outside the plan. Every session runs it last, and E-P may still be judging when you
do: a cell E-P has not scored yet reads `·`, and the last session to finish writes the most
complete version. If E-P has not scored by then, say so; do not wait.

**The closing reply**: the panel table as `panel_score.py` printed it, then the summary
table as `summary` printed it, which judges ran and on which model, what the guard moved,
any searcher that ran out of search budget, and anything that failed.

## 4. Resolve

Each shard resolves as its own run, `edge_resolve.py --run <SHARD>`, beside
`edge_resolve.py --run <RUN>/edge-panel`. The question is whether the shards' selected names
and E-P's selected names on the same day differ and which set paid. It is judged pooled over
days, never one day at a time.

## 5. Changing this stage

The three overlay files live on `edge_panel_split.data_branch`. After any change run
`python3 researcher_us/scripts/panel_split_check.py` (throwaway repositories, no network,
no model calls), then commit and push them to that branch. Never put them on main from a
fired session.

This is research, not investment advice.
