---
name: earnings-edge-panel-split
description: Stage E-PS, a one-day test (2026-10-22). Stage E-P's own names that day split over four fresh sessions of at most five, each with stage E-P's sweep rows and sealed baselines copied in, its own Opus 5.5 searchers and its own blind four-model panel, scored --dry-run against stage E-P's history. The sessions agree who takes which names through compare-and-swap commits on the test branch (panel_split.py claim). Writes edge-split-<k>/ shards and an edge-split/ plan, claims and comparison with stage E-P; places no orders. Use when asked to run stage E-PS, the split panel, or one shard of the split test.
---

# Stage E-PS — stage E-P's names, five to a session

Built 2026-10-22 on the operator's instruction: *"ik heb het gevoel dat bij hoog aantal
tickers het systeem het niet goed doet. dus ik wil even 4 test routines aanmaken, die
ieder max 5 stocks beoordelen, en op de een of andere manier communiceren onderling wie
welk doet"*. Four Routines fire the same afternoon with the same prompt; each session takes
one shard of at most five of stage E-P's names.

It asks one question: **does a session carrying five names produce different evidence and a
different panel call than stage E-P's one session carrying twenty, on the same names?** The
2026-10-21 run log is why it is worth asking: on 30 names one sweep left 89 of 118 universe
names unchecked, the searchers reported the session's shared WebSearch budget running out,
and the judges hit a 429 and finished after the close. Here the sweep is E-P's own (copied,
not re-run), so a shard spends its whole budget on five searchers and four judges.

This file is an overlay: follow `.claude/skills/earnings-edge-panel/SKILL.md` (itself an
overlay on `.claude/skills/earnings-edge-hunt/SKILL.md`) for how a searcher is briefed, how
the packs and judges run and how the panel is recorded, and do differently what the table
and the steps below say. Read `CLAUDE.md`, then the stage E skill, then the stage E-P
skill, then come back here.

## The overrides on stage E-P

| Stage E-P does | Stage E-PS does instead | Why |
| --- | --- | --- |
| builds its own universe, seals 100+ baselines, runs one `edge-sweep` | **no universe, no sealing, no sweep**: `panel_split.py claim` copies E-P's universe rows, sweep rows and sealed baselines for this shard's names into `<SHARD>` | The names, the sweep and the searcher's inputs are E-P's, so the load per session is what differs. |
| writes to `<RUN>/edge-panel/` | writes to **`<SHARD>` = `<RUN>/edge-split-<k>/`**, E-P's layout; the day's plan, claims and comparison live in `<RUN>/edge-split/` and only `panel_split.py` writes there | One directory per shard, the date still its parent, so every per-run script works unchanged. |
| up to twenty searchers in waves | **at most five, all in one message** | The point of the test. |
| step 3s sells, step 6b buys | **nothing: no `alpaca_trade.py` call of any kind**, not `mode`, not `plan`, not `status` | Stage E-P is the only stage connected to the account. |
| `edge_grounded_score.py` (5b), `edge_context.py` (6d) | **skips both** | They describe the name, not the session load, and stage E-P writes them for these names. |
| `panel_score.py --run <RUN>/edge-panel` | **`panel_score.py --run <SHARD> --dry-run --stage E-PS`** | `--dry-run` keeps `researcher_us/analysis/panel-history.json` untouched; each judge is read against stage E-P's live range from runs before today, so the shard's percentiles sit on E-P's scale. |
| stamps `provenance.py stamp --market US-P` | stamps **`--market US-PS`** on `<SHARD>` | Its own label and version, `us-panel-split.vN`. Never pooled with stage E-P. |
| `scripts/run_log.py` and `scripts/publish.sh` | **`panel_split.py log` and `panel_split.py publish`, never the two scripts directly** | `log` appends to the day's run log by compare-and-swap, so four sessions never meet in a rebase on `_run-log.md`; `publish` pushes to `edge_panel_split.data_branch`. A plain `publish.sh` pushes to `main` and would carry this test's code there. |
| amc names are done long before the release | **`intraday.py guard --snap <SHARD>` between the searchers and `edge_score.py`** | A shard starts about an hour after E-P; any amc hunt written at or after 16:00 ET is moved out of the scored set. |

**YOU PLACE NO ORDERS.** Never write into `<RUN>/edge-panel/`, `<RUN>/edge/` or another
shard's directory. Never open stage E-P's hunts, packs, judge files or scores: the only
thing that reads them is `panel_split.py summary`, after your own panel is scored.

## 0. Claim a shard

```bash
python3 researcher_us/scripts/panel_split.py claim
```

Give that Bash call a timeout of 600000 ms: one call waits up to nine minutes. It waits
until stage E-P has reached its buy (`edge-panel/alpaca-plan.json` on `main`) or, failing
that, until 14:30 ET, then builds the day's plan once (the first session to push it wins;
every other session reads that one) and claims the lowest free shard. It prints JSON:

- **exit 3**, `retry`: run the same command again, as often as it says. It stops itself at
  14:30 ET.
- **exit 2**, `stop`: no E-P sweep on `main` by 14:30 ET. Run
  `panel_split.py log --heading "stopped" --line "<reason>"` and end.
- **exit 4**: every shard is taken (a re-fire, or a fifth session). Log it the same way and end.
- **exit 0**: `shard`, `snap` (= `<SHARD>`), `names` (ticker, company, session, event date,
  hunt priority), `names_basis`. `resumed: true` means this container claimed it before:
  keep what `<SHARD>` already holds and relaunch only the searchers whose hunts are missing.

A shard with no names (a day E-P hunted fewer than four): log it, run
`panel_split.py done --shard <k>`, end.

Then the heartbeat, before anything is spent:

```bash
python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "STARTED" --line "<names>, E-P's sweep and baselines from <source_commit>, <names_basis>"
python3 researcher_us/scripts/panel_split.py publish "split panel <k>: seeded for <D>"
python3 scripts/provenance.py stamp --run <SHARD> --market US-PS --orchestrator-model "<model>"
```

## 1. Search — all of the shard's names in ONE message

One `unpriced-searcher` per name, every one in the same message, amc names first in the
message. Give each exactly what stage E-P gives it: ticker, company, event date and session,
the absolute path to `<SHARD>/baselines/<TICKER>.json`, its output path
`<SHARD>/hunts/<TICKER>.json`, and its sweep row (`<SHARD>/sweep-rows/<TICKER>.json`).
Where that row says `baseline_history_trustworthy: false`, or the baseline carries
`cadence_implausible`, tell that searcher so, as stage E does. Nothing else: not stage E-P's
hunt for the name, not the other shards, not your view. If `unpriced-searcher` is not found,
use stage E-P's fallback (`general-purpose`, its body pasted in, `model: opus`) and record
which form ran.

When the last one returns:

```bash
python3 researcher_us/scripts/intraday.py guard --snap <SHARD>
python3 researcher_us/scripts/edge_score.py --run <SHARD>
python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "searchers done" --line "<n> of <n> returned at <UTC>; guard moved <names or nothing>; any searcher that reported its search budget running out"
python3 researcher_us/scripts/panel_split.py publish "split panel <k>: hunts for <D>"
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

`<SHARD>/edge-note.md`, short: this is stage E-PS, shard `<k>` of four, Opus 5.5 searchers
and a blind four-model panel on stage E-P's own names, sweep and baselines, no orders; which
judges ran; what the guard moved; claim-to-done minutes; then the panel table exactly as
`panel_score.py` printed it. One day is an anecdote. End with the disclaimer in
`config/pipeline.yaml`.

```bash
python3 researcher_us/scripts/panel_split.py publish "split panel <k>: <n> names, <m> selected for <D>"
python3 researcher_us/scripts/panel_split.py done --shard <k>
python3 researcher_us/scripts/panel_split.py summary
```

`summary` rebuilds `<RUN>/edge-split/summary.{json,md}` from every finished shard and stage
E-P's own `edge-scores-panel.json` and hunts on `main`: per name, E-P's call beside the
shard's, both searchers' `impact_sum`, findings and sources, then the overlap of the
selected sets and the Spearman rho between the two signed `panel_pct` columns. Every
session runs it last; the last to finish writes the complete one.

**The closing reply**: the panel table as `panel_score.py` printed it, then the summary
table as `summary` printed it, which judges ran and on which model, what the guard moved,
any searcher that ran out of search budget, and anything that failed.

## 4. Resolve

Each shard resolves as its own run, `edge_resolve.py --run <SHARD>`, beside
`edge_resolve.py --run <RUN>/edge-panel`. The question is whether the shards' selected names
and E-P's selected names on the same day differ and which set paid. One day cannot answer
it; it can only show whether the evidence and the calls differ enough to be worth a
second day.

This is research, not investment advice.
