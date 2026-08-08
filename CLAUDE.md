# claude_research — daily earnings pipeline

This repository runs one thing: a five-stage daily research pipeline over US companies
reporting earnings between today's close and tomorrow's open. Each stage is fired by a
scheduled Routine into a **fresh session** that knows nothing except this file and the
repo contents.

If you are a Routine session, read this whole file before doing anything.

## The stages

| # | Skill | Fires | What it does |
| --- | --- | --- | --- |
| 0 | `earnings-universe` | 07:12 | Fetch and qualify the day's earnings universe |
| 1 | `earnings-triage` | 11:08 | Screen it down to ~10 names worth researching |
| 2 | `earnings-deep-dive` | 14:22 & 16:22 | One deep Opus/high dossier per name, in two batches |
| 3 | `earnings-panel-advice` | 18:07 | Seven-persona panel on the top names → the advice note |
| 4 | `earnings-calibration` | 08:20 next day | Score yesterday's calls, update the ledger |

Times are Europe/Amsterdam. See `docs/ROUTINES.md` for the cron expressions and the
reasoning behind the spacing.

Invoke the stage skill named in your Routine prompt. Do not improvise a different
workflow — later stages read the files earlier stages wrote, in the shapes the skills
specify.

## Where things go

```
research/<YYYY>/<MM>/<YYYY-MM-DD>/
  00-universe.json  00-universe.md      stage 0
  01-shortlist.json 01-shortlist.md     stage 1
  02-dossiers/<TICKER>.md + .json       stage 2
  02-ranking.json                       stage 2, final batch only
  03-panel/<TICKER>.json                stage 3, verdicts + synthesis
  03-panel/<TICKER>-synthesis.json      stage 3, raw script output
  03-panel/<TICKER>-dossier.md          stage 3, the answer-first dossier
  04-advice.md  04-advice.json          stage 3, the day's deliverable
  05-outcome.md 05-outcome.json         stage 4
  _run-log.md                           appended by every stage
INDEX.md         rolling archive index (generated — never hand-edit)
LEDGER.md        rolling forecast accuracy ledger
PREDICTIONS.csv  every prediction ever made, one row per (day, ticker) — generated
PREDICTIONS.json same data plus a summary block — generated
```

`PREDICTIONS.csv` is the file to open when the question is "what did we call, and what
happened". It joins the triage scores, the dossier's preliminary read, the panel
synthesis, and the realised outcome into one flat table. Regenerate it with:

```bash
python3 scripts/build_predictions.py
```

Stages 3 and 4 do this as part of publishing. It is derived state — safe to delete and
rebuild.

Never invent a path. Always resolve with:

```bash
python3 scripts/run_paths.py --json
```

## Rules that apply to every stage

**Publish or it never happened.** These sessions are ephemeral containers. Work that is
not committed and pushed is destroyed when the session ends. Every stage ends with:

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage <n>: <what> for <YYYY-MM-DD>"
```

Stage 2 publishes after *each* batch, not once at the end.

**Append to `_run-log.md`, never rewrite it.** Each stage adds its own section. The run
log is how a later stage — and you, tomorrow — finds out that something upstream went
wrong.

**Resume, do not restart.** Routines get re-run and sessions get retried. Before doing
expensive work, check whether the output already exists and skip it.

**Never fabricate a number.** Every company-specific figure carries a source URL, or is
marked `unavailable`/`null`. This applies to prices, implied moves, consensus estimates,
short interest, insider transactions, and historical reactions. A missing anchor
correctly lowers confidence downstream; an invented one corrupts everything after it.

**Validate before publishing:**

```bash
python3 scripts/validate_stage.py shortlist|panel|advice <path>
```

If you change a skill, an agent definition, or `scripts/synthesize.py`, run
`python3 scripts/smoke_test.py` before pushing. It checks the whole chain against
synthetic data with no model calls.

**Respect the budget.** `config/pipeline.yaml` sets subagent caps per stage. When a
stage would exceed its cap, shed scope using `budget.degrade_order` and record what you
shed. Half a pipeline that finishes beats a full one that gets cut off.

## Independence of the persona panel

The seven personas in stage 3 must never see each other's verdicts, nor the stage 2
dossier, nor your own view. They receive only the Phase-0 anchors: ticker, company,
window, session, spot, implied move, historical realised moves.

Their disagreement is the entire signal. `scripts/synthesize.py` reads the spread of
their scores as `disparity` and lowers certainty when they diverge — so a panel that has
been allowed to converge produces a confident number that means nothing. The persona
agent definitions deliberately have no file-reading tools; do not work around that.

## Network

`WebSearch` works. `WebFetch` may be blocked for financial domains depending on the
environment's egress policy, and `curl`/`requests` from Bash may be blocked too.

When a fetch is blocked: fall back to `WebSearch` snippets, cite the source URL, mark the
datum `snippet_only`, and record the unreachable domain in the run log. Do not disable
TLS verification and do not try to route around the proxy.

If `scripts/get_earnings.py` exits 2 with `status_reason: network_blocked`, the
environment is the problem — the Routines should be pointed at an environment with full
network access. Flag it in the run log rather than quietly degrading every day.

## Conventions

- Money in USD. Moves in percent. Dates ISO `YYYY-MM-DD`. Timestamps UTC with the zone.
- `session` is `"amc"` or `"bmo"`, lowercase, everywhere.
- `direction_score` −100…+100 · `prob_up` 0…100 · `reversal_risk` 0…100, always separate
  from direction.
- Calls are exactly: `Strong Up`, `Lean Up`, `Neutral / No Edge`, `Lean Down`,
  `Strong Down`.
- Every deliverable ends with the disclaimer in `config/pipeline.yaml`.

## This is research, not advice

The output is a forecasting exercise over public information. It is not investment
advice and must not be presented as such. Keep the disclaimer on every deliverable and
keep certainty claims honest — the calibration ledger in `LEDGER.md` exists to check
exactly that.
