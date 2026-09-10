# Stage E — the edge hunt

One question, asked once per company reporting today: **is there anything here the market
has missed, and how does that rank against the other names reporting today?** Not "what
will this stock do". The stage emits one signed number per company — `impact_sum`, in
points of spot, unbounded — with no call, no threshold and no direction label, because a
ranking is only answerable at every cut if nothing was rounded into a bucket upstream.

Nothing downstream reads it. It is not part of the daily advice pipeline (stages 0–4) and
it must not be merged with stage N (`claude_naive/`), which forecasts every name it looks
at rather than scoring what is unpriced. If E's ranking turns out to carry no information
that N's does not, that is a result worth having cheaply.

## What is here

```
edge/
  EDGE_ANALYSIS.md      what the resolved runs establish, and what they do not
  EXECUTION.md          the Alpaca path: what it refuses to do, and what it cannot see
  scripts/              the stage's own tools (see below)
  analysis/             everything the analysis scripts generate — JSON and HTML
  ledger/               every finding ever made, flat — CSV and SQLite, generated
  routine-prompts/      the text pasted into the Routines, kept in step by hand
```

## What cannot live here, and where it is instead

| | where | why |
| --- | --- | --- |
| the skill | `.claude/skills/earnings-edge-hunt/` | the harness discovers skills only there |
| the agents | `.claude/agents/{edge-sweep,unpriced-hunter,priced-in-adversary}.md` | same |
| the `execution` block | `config/pipeline.yaml` | one config file for the whole repo |
| each day's run | `research/<YYYY>/<MM>/<date>/edge/` | the run archive is keyed by day, not by stage |
| the corpus backtest of this stage | `backtest/runs/edge-corpus/` | it is an arm of the backtest, scored by `backtest/scripts/edge_corpus_report.py` |
| `run_paths.py`, `publish.sh`, `run_log.py`, `get_earnings.py` | `scripts/` | shared with the pipeline stages |

## The four shims in `scripts/`

`scripts/edge_score.py`, `scripts/edge_universe.py`, `scripts/priced_in.py` and
`scripts/alpaca_trade.py` are three-line forwarders to the real scripts here. Stage E's
Routine holds a prompt that was pasted in by hand, names those paths, and verifies two of
them exist before doing anything else. An agent session cannot edit that prompt —
`update_trigger` refuses any Routine an agent did not create — so removing the old paths
would have stopped the next unattended run at step 0, **before step 0b sold the previous
day's book**.

Delete them once `routine-prompts/edge-hunt.md` has been re-pasted with the new paths and
the Routine's `updated_at` confirms it. Nothing else keeps the two in step.

## Running it

The stage runs itself: invoke the `earnings-edge-hunt` skill and follow it. It is the
authority on the output contract, not this file and not the Routine prompt. By hand, the
spine is:

```bash
python3 scripts/run_paths.py --json                                    # never invent a path
python3 edge/scripts/edge_universe.py --window -o <RUN>/edge/universe.json
python3 edge/scripts/priced_in.py --tickers <T,...> --date <D> --session <s> \
        -o <RUN>/edge/baselines/                                       # seal BEFORE hunting
#   ... one edge-sweep agent, then one unpriced-hunter per confirmed name ...
python3 edge/scripts/edge_score.py --run <RUN>/edge
python3 edge/scripts/edge_ledger.py                                    # rebuild the ledger
scripts/publish.sh "stage E: edge hunt for <date>"
```

Scoring a day after the fact, and the analyses built on those rows:

```bash
python3 edge/scripts/edge_resolve.py --pool          # realised moves vs the ranking
python3 edge/scripts/edge_decompose.py               # writes analysis/edge-rows.json
python3 edge/scripts/edge_direction.py               # can the sum call direction
python3 edge/scripts/edge_trade.py                   # the ranking traded as a book
python3 edge/scripts/edge_exit.py                    # when to sell
python3 edge/scripts/edge_hunter_control.py          # how much of it is the double hunt
python3 edge/scripts/edge_turnover_floor.py          # what capacity costs
python3 edge/scripts/edge_entry_timing.py            # market vs the closing auction
```

`edge_adversary_brief.py`, `edge_brief.py` and `.claude/agents/priced-in-adversary.md` are
the removed adversary pass. They are kept unused so it can be re-run deliberately; the
stage does not call them.

## The finding ledger

Every analysis above works on one row per *company*. The ledger works on one row per
*finding*, which is the grain the hunt actually produces and the only grain at which the
question "what sort of finding was ever worth anything" can be asked.

```bash
python3 edge/scripts/edge_ledger.py --report
```

It writes `ledger/findings.csv`, `ledger/names.csv` and `ledger/edge.sqlite` from files
that already exist — no subagent, no model call, one price fetch per newly resolved name,
cached. Rebuilt from scratch every time, so it is safe to delete.

Each finding row carries what the hunter wrote (`claim`, `kind`, `evidence`, the size,
the band, `why_not_priced`, `independence`), what is derivable for free (source domain,
how old the source was on the day of the print, the finding's share of its name's
`impact_sum`), and what the name did.

**The one thing it cannot give you is a per-finding outcome.** You observe one move per
company; a name carries three to eight findings that were never separately priced. So
`sign_agreed` means "the name this finding belonged to moved the way this finding
pointed", and every finding of that name shares the value. Two rules follow: never read a
single row, and weight by `share_of_impact` when grouping — a finding that was 90% of its
name's key really was the call, one that was 5% of it is a passenger. The `sole_finding`
column marks the rows where the problem does not arise; there is currently one of them.

`edge_calibration.py` is the first thing built on it: it asks whether `impact_sum` means
what it says, rather than whether it orders the day. Over 68 de-duplicated events the
answer is no — the regression slope on the realised move is −0.021 with an R² of zero,
and the number loses to predicting no move at all. What survives is the ordering by
`|impact_sum|`, at about half the strength it was fitted at. Read
`EDGE_ANALYSIS.md`, "The number is a confidence flag, not a magnitude".

`kind` and `evidence` are null for every run before 2026-09-10 because the hunter contract
had no such fields. 349 of the 399 findings resolve, over 76 names and 9 days, and nothing
in the grouped table is close to significant. It is a table to watch as runs pool.

## What it has established

Read `EDGE_ANALYSIS.md` before quoting any number about this stage, including the ones in
`CLAUDE.md`. In one line: the ordering problem is fixed, the scorer is subtractive against
its own raw inputs, the direction lives only in the large predictions, and the stage has
not yet beaten a free control that costs nothing to compute. Money placed on the shipped
ranking would have lost to doing nothing.

`EXECUTION.md` is the whole contract for the Alpaca path, which is live and unattended on
the paper account. Setting `execution.enabled` back to `false` in `config/pipeline.yaml`
is the only thing that stops it.

This is research, not investment advice.
