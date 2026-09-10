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
