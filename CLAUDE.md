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
| 4 | `earnings-calibration` | 08:20 | Score *yesterday's* calls, update the ledger |
| 1 | `earnings-triage` | 08:38 | Screen it down to ~6 names worth researching |
| 2 | `earnings-deep-dive` | 10:22 & 12:22 | One deep Opus/high dossier per name, in two batches |
| 3 | `earnings-panel-advice` | 17:52 | Seven-persona panel on the top names → the advice note |
| C | `earnings-capture` | 17:03 | Track B: capture the run-in to *upcoming* prints, before the outcome exists |
| N | `earnings-naive-forecast` | 19:30 | `claude_naive` — the backtest-winning naive method, run live |
| E | `earnings-edge-hunt` | 16:04 | Seal what the market priced, hunt for what it did not, rank the day on one signed number |

Stage N is not part of the daily advice pipeline. It is `backtest/` arm A promoted to
production: the method that scored 72% direction and +0.90% per trade over 37 events
while the pipeline's own stage-2 method (arm C) scored 55% and lost money. It writes to
`claude_naive/` and reads nothing from `research/`. Its Routine is
`trig_01XmfJNU2CM7q5uvdb5r4ydF` and **it was disabled on 2026-09-09 at 16:16 UTC**,
alongside stage C, by someone outside this repo — observed in `list_triggers`, reason not
recorded anywhere. It had a run due at 17:35 that day and did not take it. Check
`list_triggers` before concluding a missing `claude_naive/<date>/` is a failure. See `claude_naive/README.md` for what
that result does and does not establish — in short, the direction ranking is a lead and
the magnitude finding is the part worth acting on.

Stage E is a second experiment alongside it, and nothing downstream reads it either. It
asks a narrower question than stage N: not "what will this stock do" but **"is there
anything here the market has missed, and how does that rank against the other names
reporting today."** It emits one signed number per company — `impact_sum`, in points of
spot, unbounded — with no call, no threshold and no direction label, because the question being tested is whether the day's
companies can be **ranked** — and that is only answerable at every cut if nothing was
rounded into a bucket upstream. Falsifiable by `scripts/edge_resolve.py`, which reports
Spearman rank correlation against the realised move with a permutation p-value. Until
many days have pooled, it is not better than anything.

Seven runs exist: two on 2026-08-31 and one on each of 09-01, 09-02, 09-03, 09-04,
09-07 and 09-08. Six are resolved — **43 names, 249 findings, 65 hunts**; 09-08's eight
names need the 09-09 close. The 08-31 pair is archived separately,
`research/2026/08/2026-08-31/edge/_run1-bmo/` and `edge/`. Run 1 (that day's `bmo`, with
`--include-unknown`) found eight of twelve calendar rows had no earnings event at all and
produced no ranking worth the name: every judged finding fell into one of two verdict
buckets and twelve names collapsed to one non-zero score and eleven zeros. The categories
the stage has since dropped are why, and its `edge-scores.json` carries
`legacy_rescore: true` — midpoints, never evidence about that day.

**The ordering problem is fixed; the scorer is now the problem.** `docs/EDGE_ANALYSIS.md`
decomposes all six resolved runs, pooling *within* days (`scripts/edge_decompose.py`).
The shipped `edge_score` ranks at ρ=0.243, p=0.156 — not significant. The hunters' raw
impact sum, before the cluster-max, the √k discount, the agreement discount and the
quality multiplier, ranks at ρ=0.407, p=0.017. A paired bootstrap over days puts that
gap at +0.165 with a 95% CI of [+0.082, +0.244], so the aggregation in
`scripts/edge_score.py` is subtractive, not small-sample noise. Traded as a long
top-third / short bottom-third, the shipped ranking returns +2.17pp per day against
+11.45pp for its own raw inputs.

**Money placed on it would have lost to doing nothing.** `scripts/edge_trade.py` runs
each day's ranking as a book, entry at the close before the print and exit after the
first full session. Gross of costs the shipped ranking returns +1.09% per day (t=0.51,
95% CI [−2.72, +4.80]) against **+1.49% for shorting every name and doing no research at
all**; at a 1.5%/day cost it goes negative. The one strategy with a defensible p-value is
minus the 20-day run-up, positive on 6 of 6 days (sign test p=0.031). And the single best
trade in the sample, DLTH +23.20%, turns over $170k a day: six of the ranking's 22
positions traded under $1m a day, and screening to names above $5m of turnover drops 14
of 43 names. Nothing in the budget or the scorer notices capacity.

**Five of the 43 rows are duplicates** — ABM, UNFI, WDH, CAN and GMHS were hunted on
both 09-04 and 09-07 for the same 09-08 prints — so `edge_resolve.py --pool` double-counts
five events and the real sample is 38 events over 5 independent days. De-duplicated,
`edge_score`'s trading return goes to +0.09%/day and −0.1% cumulative: its entire positive
result came from the repeated day. The raw impact sum survives at +5.66%/day (CI
[−0.21, +9.79]) and at +6.05%/day on names above $5m turnover, but a max-statistic test
over the thirteen candidates it was chosen from puts its ranking p at 0.056 — a lead to run
forward, not a finding.

**The direction lives in the large predictions, and only in the impact sum.** The
threshold-free test — does the rank of `|impact sum|` predict whether its sign was right —
gives ρ=+0.514, permutation p=0.0015 to the next close (ρ=+0.331, p=0.046 to the open).
Above the median prediction the sign is right on 74% of events; below it, 53%. As a
threshold, `|pred| >= 3` gives 16/21 with +6.37% per trade (t=2.74, CI [+1.80, +10.72],
+4.87% after a 1.5% cost), and the best of seven thresholds still clears family-wise
correction at p=0.034. It is not one day (spread over five), not the microcaps (median
turnover $7.5m in the top bucket against $69.9m in the bottom), and not a volatility proxy
(the top bucket has the *smallest* median realised move). Run the same test on
`|edge_score|` and it returns +0.077 and −0.003: the scorer destroys the conviction signal
too. See `docs/EDGE_ANALYSIS.md`, "Conviction is where the direction lives" — the
sign of the impact sum over all 38 events is a coin flip (53%), so the conviction floor is
the whole finding.

**The double hunt inflates both of those numbers by about a third, and neither dies without
it.** Until 2026-09-09 `double_hunt_top_n: 2` gave two hunters to the day's two
highest-`hunt_priority` names and one to everything else. The key is a sum, so those ten of 38
events carry 2.6× the conviction of the rest by construction (mean \|impact\| 9.13 against
3.53, 8.0 findings against 3.7). `scripts/edge_hunter_control.py` measures it. **Do not test
this by dropping the double-hunted names**: `hunt_priority` is assigned by the sweep before
any hunting, so the survivors are the names the sweep rated lowest (mean priority 59.9 against
77.2), and the collapse there (conviction +0.270 p=0.29, ranking +0.042) describes that
population rather than a de-confounded effect. The right control keeps all 38 events and
rebuilds each double-hunted name's key from **one hunter's findings**, which is also how the
stage now runs: conviction **+0.361 (p=0.045)** against +0.514, ranking **+0.303 (p=0.099)**
against +0.360 on the same de-duplicated events. `conviction_floor: 3.0` re-derived on that
counterfactual gives 15/21 = 71% at +5.53% per trade, CI [+1.02, +9.90] — still clear of zero,
still half the day, so the floor stands with a haircut rather than a reversal. Two further
things: averaging the two hunters ranks better than either alone (+0.442 against +0.361 and
+0.299), the signature of noise reduction, which argues against having removed the double
hunt; and the second hunter bought no direction on those names (7/10 sign-correct either way)
while the pair disagreed on sign 4 times in 10. Nothing here separates "a second opinion
helps" from "the sweep picked well" — they were assigned together — and only days under the
new config, or a deliberate double-hunt week, will.

**`impact_sum` sums the HUNTER's sizes, since 2026-09-09.** The 09-09 run caught that
`edge_score.py` was re-sizing every finding to the mean of the hunter's number and the
adversary's `size_check_pct`, so the ρ=0.407 above was measured on the average and every
description of the key as "the hunters' sizes" named the wrong number. Measured both ways
on the same 43 names: the average ranks at ρ=0.407 (p=0.014), the hunter's own number at
**ρ=0.453 (p=0.006)**. They differ by a median 0.80 points per name and reorder the day on
4 of 6 days, so the key now sums the hunter and keeps the adversary's estimate beside it.
`diagnostics.edge_score_legacy` still reads the averaged value and reproduces the old key
exactly. **It is not a return forecast**: regression slope 0.72–0.76 (0.86–0.93 above the
conviction floor), pearson 0.41–0.46, median absolute error 6–7 points against a realised
standard deviation near 11, and it double-counts findings that rest on one document.

**The adversary and the double hunt are both gone (2026-09-09); the day hunts 19 names
with one hunter each.** The adversary returned two numbers and both were subtractive over
215 findings on six days. `size_check_pct`: the hunter's own size ranks at ρ=0.453 against
0.407 for the mean of the two. `priced_in_pct`: every way of letting it touch the ranking
makes it worse, monotonically in how much it removes — the haircut 0.325, dropping
findings at priced_in ≥ 90 gives 0.407, ≥ 80 gives 0.328, ≥ 70 gives 0.221, keeping only
≤ 50 gives 0.305; mean priced_in per name ranks +0.046. Once `impact_sum` became the key
neither number reached the output at all: 8 of 20 subagents changing nothing ranked. The
double hunt went for the same reason — over twelve paired names the gap between two
hunters predicted neither the error (+0.203) nor whether the sign was right (+0.028).

**Two things were knowingly given up, and both belong in every note.** Nothing now checks
a finding for being factually wrong; the adversary was the only thing that did, and on
09-09 it caught a covenant amendment misread by a year and a short-interest claim
contradicted by its own source. And nothing measures the key's reproducibility: while the
double hunt ran, twelve pairs came back with a median gap of 2.40 points and **four of the
twelve had opposite signs**, on a key whose typical size is about 5. Re-run a double-hunt
week occasionally rather than letting that number rot.
`.claude/agents/priced-in-adversary.md` and the brief scripts stay in the tree, unused, so
either pass can be re-run deliberately.

**And the stage has not yet beaten a free control.** `-run_up_20d_pct`, one number from
the sealed baseline available before any subagent is spawned, ranks at ρ=0.335 and is
positive on 6 of 6 days when traded (+10.97pp). The hunt's raw evidence leads it by 0.080
with a CI spanning zero. Note also that `edge_resolve.py --pool` concatenates days and
understates every ranker (0.189 vs 0.243 for `edge_score`), that `confidence` and
`baseline_quality` rank at −0.090 and +0.074 and must not be read as reader guidance, and
that `spearman_vs_move_over_implied` normalises 18 of 43 names on a median historical
reaction rather than an option-implied move. Fix the scorer before spending another day
on hunts.

Run 2's own failures are written into the skill and the agent definitions rather than
left in the run log: a same-directory collision between the two runs that would have
pooled twelve stale zeros into run 2's ranking, a cadence heuristic in `priced_in.py`
that flagged four company-confirmed reporters as non-events, an adversary agent with no
`Write` tool, and two entries of `budget.edge_degrade_order` that each contradicted a
hard rule stated elsewhere. All four are fixed.

Stage N and stage E overlap deliberately and must not be merged. N forecasts every name
it looks at; E scores whether the market has missed something. If E's ranking turns out
to carry no information that N's does not, that is a result worth having cheaply.

Stage C is not part of the daily advice pipeline and nothing downstream reads it. It
builds the forward corpus the backtest needs, and it is the only stage whose work cannot
be redone tomorrow — the day will have moved. See `backtest/scripts/capture.py`.

Stage E's Routine is `trig_01CvGQJWoKeNLXWCxiffM3ED`, cron `4 14 * * 1-5`, enabled, and
the only one of the three still running. Its prompt cannot be edited by a session —
`update_trigger` refuses any Routine an agent did not create — so the text lives in
`docs/routine-prompts/edge-hunt.md` and was pasted in by hand on 2026-09-09 at 13:55 UTC;
keep that file in step with the Routine, because nothing else will. Since 2026-09-09 the prompt no longer restates the output contract: the
ranking key is whatever the skill and `edge-scores.json`'s own `ranking_key` field say,
because the old prompt named a key that a measurement then demoted.

**The five pipeline Routines do not currently exist.** `RemoteTrigger list` on
2026-08-29 returned six routines on this account — a disabled SFNL tender monitor, three
spent one-shot wakers, and two trivial `hey` jobs. None of stages 0 through 4 is among
them. The times in the table above therefore describe an intended schedule, not a
running one, which is a far better explanation for missing days than any code path in
this repo. Stage C (`trig_01K1ZTiK4qQayC9aLvaK2Gyn`) is real but **was disabled on 2026-09-09 at
16:16 UTC**, a minute after stage N and from outside this repo. Its last run was that
day's 15:05 sweep. Stage C is the one stage whose day cannot be redone, so every day it
stays off is a permanent hole in the forward corpus.

Times are Europe/Amsterdam, and they are the **actual cron times** — check them against
`list_triggers` before trusting them, not the other way round. This table was stale for
five days (it still showed a pre-2026-08-08 schedule of 11:08 / 14:22 / 16:22 / 18:07)
and cost real runs: a stage 2 session concluded the platform clock was "running ahead"
and a stage 3 session reported stage 2 as overdue when it had in fact fired hours
earlier. If you find this table disagreeing with `docs/ROUTINES.md` or with the Routines
themselves, fix it in the same commit as whatever else you are doing.

See `docs/ROUTINES.md` for the cron expressions and the reasoning behind the spacing.

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

Stage 2 publishes after *each dossier*, not once per batch and not once at the end. A
run really did die partway through a batch; the names already pushed survived and the
rest were lost.

**Leave a heartbeat before you spend anything.** Any stage that is about to spawn
subagents first appends a `— STARTED` section to the run log and publishes it:

```bash
python3 scripts/run_log.py --heading "Stage <n> — <name> — STARTED" --line "<the plan>"
scripts/publish.sh "stage <n>: started for <YYYY-MM-DD>"
```

One cheap commit, and it is the only thing that distinguishes *a Routine that never
fired* from *a session that fired and was killed on its first subagent*. Those have
completely different fixes. Stage 2 published nothing on four consecutive days
(08-08 through 08-12) and, with no heartbeat, the most stage 3 could conclude was
"stage 2 never ran, or ran and failed before completing its first name."

**Append to `_run-log.md`, never rewrite it.** Each stage adds its own section, and
`scripts/run_log.py` is the safe way to do it. The run log is how a later stage — and
you, tomorrow — finds out that something upstream went wrong.

**Timestamp in UTC.** Sessions guess their local offset wrong: run-log entries have
claimed 11:08 CEST for work that committed at 08:45 CEST. `scripts/run_log.py` stamps
UTC for you. `date` inside the container is reliable; what is *not* reliable is a long
session's own sense of what day it is. A session can be interrupted and resumed days
later in a fresh container, and the date it was told at startup goes stale without
anything announcing it — that happened here across 08-13 to 08-17 and produced a
confidently wrong timeline. Re-read the clock whenever the date matters, and
cross-check it against `list_triggers` before concluding a stage is late.

**A missing day is not always a failed stage.** If a whole day is absent from
`research/`, check `list_triggers` before reading anything in this repo: on 08-14 and
08-17 the Routines did not fire at all, and a Routine that never fires leaves no
heartbeat, no log, and no directory to find. See `docs/ROUTINES.md`, "The fourth fault".

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
