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
| E | `earnings-edge-hunt` | 19:04 | Seal what the market priced, hunt for what it did not, rank the day on one signed number |
| X | (no skill) | 12:00 | "Close AMC" — the second exit Routine. A no-op while `exit_mode` is `uniform` |

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
rounded into a bucket upstream. Falsifiable by `edge/scripts/edge_resolve.py`, which reports
Spearman rank correlation against the realised move with a permutation p-value. Until
many days have pooled, it is not better than anything.

Ten runs exist: two on 2026-08-31 and one on each of 09-01, 09-02, 09-03, 09-04, 09-07,
09-08, 09-09 and 09-10. Six are resolved — **43 names, 249 findings, 65 hunts**; the
09-08, 09-09 and 09-10 runs are not. (This paragraph said "seven" and omitted 09-09
until 09-10; the six-resolved decomposition in `edge/EDGE_ANALYSIS.md` is unaffected,
because it covers 08-31 through 09-07 and never included them.) The 09-10 run is the
first under the one-hunter-per-name contract: 17 names in the window, **17 of 17
confirmed by the sweep with zero phantom rows**, 17 hunters, 61 findings, 7 clearing the
conviction floor. Its ranking is near-orthogonal to the free control (Spearman 0.054
against `-run_up_20d_pct`), and four of its seventeen names are ranked substantially by
one regulatory event — the IEEPA tariff refunds — which is a correlated exposure the
scorer cannot see. The 08-31 pair is archived separately,
`research/2026/08/2026-08-31/edge/_run1-bmo/` and `edge/`. Run 1 (that day's `bmo`, with
`--include-unknown`) found eight of twelve calendar rows had no earnings event at all and
produced no ranking worth the name: every judged finding fell into one of two verdict
buckets and twelve names collapsed to one non-zero score and eleven zeros. The categories
the stage has since dropped are why, and its `edge-scores.json` carries
`legacy_rescore: true` — midpoints, never evidence about that day.

**The ordering problem is fixed; the scorer is now the problem.** `edge/EDGE_ANALYSIS.md`
decomposes all six resolved runs, pooling *within* days (`edge/scripts/edge_decompose.py`).
The shipped `edge_score` ranks at ρ=0.243, p=0.156 — not significant. The hunters' raw
impact sum, before the cluster-max, the √k discount, the agreement discount and the
quality multiplier, ranks at ρ=0.407, p=0.017. A paired bootstrap over days puts that
gap at +0.165 with a 95% CI of [+0.082, +0.244], so the aggregation in
`edge/scripts/edge_score.py` is subtractive, not small-sample noise. Traded as a long
top-third / short bottom-third, the shipped ranking returns +2.17pp per day against
+11.45pp for its own raw inputs.

**Money placed on it would have lost to doing nothing.** `edge/scripts/edge_trade.py` runs
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
too. See `edge/EDGE_ANALYSIS.md`, "Conviction is where the direction lives" — the
sign of the impact sum over all 38 events is a coin flip (53%), so the conviction floor is
the whole finding.

**About a third of that conviction number is the double hunt.** Every one of the 38 events
was scored while the day's two highest-`hunt_priority` names got two hunters and the rest
got one, and the key is a *sum*, so those names carry the largest conviction by
construction: 10 double-hunted names average 8.00 findings and |impact| 9.13 against 3.71
and 3.53 for the other 28. `edge/scripts/edge_hunter_control.py` rebuilds every name's key
from a single hunter — the only control that keeps all 38 events, since dropping the
double-hunted names selects on a sweep score assigned before any hunting. Rebuilt, the
conviction correlation falls from +0.514 (p=0.002) to +0.361 (p=0.045) and the ranking from
+0.360 to +0.303 (p=0.099). Inflated, not manufactured — but the forward regime is one
hunter per name, so **+0.361 is the number to expect, not +0.514**, and on single-hunted
names alone the `|pred| >= 3` cut the trading rule rests on is 9/14 at +4.62% with a
bootstrap interval spanning zero. See `edge/EDGE_ANALYSIS.md`, "The double hunt inflates
both headline numbers".

**Scored on the sealed backtest corpus, the hunt found no rank signal at all.**
`backtest/runs/edge-corpus/` re-runs stage E over 104 resolved events on 7 days of
point-in-time captures, judged by `backtest/scripts/edge_corpus_report.py`: ρ=+0.073
(p=0.45) raw, +0.109 (p=0.27) normalised, and no subgroup — clean captures, corpora holding
news, measured rather than inferred sessions — reaches significance. That is 104 events
against 38, on a corpus the hunters could not see past, and it is the single most
discouraging number in the repo. Read its caveats in `backtest/FINDINGS.md` §33 before
weighing it: the option anchor is unrecoverable retrospectively so every event runs on the
historical-reaction proxy, and 30 of the captures kept sweeping past the print.

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

**The exit is in the wrong place for the amc names.** `edge_resolve.py` scores one
window — regular close before the print to regular close after the first full session —
and nobody chose it. `edge/scripts/edge_exit.py` re-resolves all 38 de-duplicated events at
eight horizons off 5-minute pre/post bars (`edge/analysis/edge-exit.json`). No *uniform* early
exit is distinguishable from holding to the close: every horizon's Δρ against the close
has a CI spanning zero, and the family-wise p over the eight is 0.115. But the two legs
of the hold cancel rather than agree. The entry-to-open gap ranks at ρ=0.315 and pays the
whole conviction book (+6.21%, t=2.99); the open-to-close session leg ranks at ρ=0.078
and pays −0.20%, for 6 points of movement sat through. And the two sessions want opposite
things: **amc** gaps at ρ=+0.273 / +8.91% and then gives back −3.00% intraday (−2.61%
day-demeaned, and the book is 6 long / 6 short so it is not drift), while **bmo** is
+0.187 at the open and +0.670 at the close. Selling into the release is the one variant
the sample rejects: only 46% of the move exists there and for bmo names its ranking is
negative. Priced per hour of the clock (`edge/analysis/edge-exit-hourly.html`), the conviction book
peaks at **+6.38% per trade at 09:00 pre-market** (t=3.54) against +5.60% at the close, and
the two sessions peak in different places: amc at +8.45% at 09:00 then bleeding to +5.07%
by 16:00, bmo at zero until 07:00 and then climbing to its best value of +6.23% at the
close. The free control is on the opposite clock — shorting every name pays −0.5 to −2.0
per day before the open and +1.7 to +2.5 after it, so its edge is intraday drift and
exiting at the open removes it as a rival. The hybrid — amc at the opening print, bmo at the close — is the best of six
policies at ρ=0.461 and +7.81% (t=4.01), but it was chosen after reading the split off
these same 38 events, the bootstrap puts its gain at +1.87pp with a CI of [−1.30, +4.55],
and the best of the six beats the close in 91% of resamples. Run it forward; do not
believe it yet. Extended-hours bars carry no volume from this source, so every horizon
before the opening auction is a price that existed and not size that could have traded.

**The exit finding does not replicate on the first two forward days, and a second sample in
this repo contradicts it.** `edge_exit.py --runs <edge dir>` scores any day directly, with a
cutoff at the current clock so nothing unresolved is reported (`edge/analysis/edge-exit-forward.json`).
On 09-08 plus 09-09 — 30 names, 14 above the conviction floor, neither day in the fitted
sample — every horizon available on both days is flat to negative: −1.42% per trade in the
after-hours, −0.05% at the opening print, −1.22% an hour in. On 09-09 the free control paid
+3.9% to +4.5% per day at every hour after 08:00 against −0.2% to −0.9% for the hunt's own
book, and the two largest predictions were both wrong and large (NAVN +10.0 fell 18.4%, WLTH
−10.5 rose 8.0%). And `backtest/RESULTS.md` priced its 37 sealed events at both exits: all
three arms did **better at the close** (+2.16% against +0.90% per trade for arm A). Re-price
those 37 events on the hourly grid before acting on any exit rule. Execution reality, checked
against Alpaca's current docs: extended hours are limit-only, an `opg` (opening auction) order
is rejected between 09:28 and 19:00 ET so no European-afternoon Routine can place one, `cls`
(closing auction) is rejected between 15:50 and 19:00 ET, shorts need a margin account and an
easy-to-borrow name checked daily, and fractional shorts do not exist.

**Nothing sells a position twice and nothing forgets to sell one.** Two holes were open
until 2026-09-10. `close` only ever closed legs whose exit date was exactly today, so one
missed run left a position that no later run would sell; it now treats a past exit date as
**overdue** and sends it at plain market immediately. And `open` now REFUSES to enter a new
book while any position is past its exit date with no exit submitted (`--allow-stale`
overrides and stacks a second book on the first). That refusal is what makes the
per-session exit safe to switch on: `flatten_before_entry` used to guarantee a clean slate
by selling everything, and once the flatten is off the guarantee has to come from checking.

**The per-session exit is three modes in `alpaca_trade.py`, and it ships on the dullest
one.** `orders.exit_mode` picks which instrument closes a position, per session. Per trade
over the 38 de-duplicated events, on the conviction book: **`uniform`** +4.49% (t=2.52),
the flatten selling everything at market when the next run starts, about 10:00 ET;
**`bmo_close`** +6.27% (t=3.34), amc at market on the run and bmo into today's closing
auction; **`auction_split`** +7.81% (t=4.01), amc into the opening auction and bmo into the
close. The two sessions want opposite things — amc pays +8.91% in the opening auction,
+6.08% at 10:00 ET and +5.23% at the close, bmo pays +2.96%, +2.58% and +6.48% — because an
amc print has had a whole overnight to be processed while a bmo print has had two thin hours
of pre-market and keeps repricing.

**`bmo_close` is reachable from the existing Routine; `auction_split` is not.** Alpaca
*rejects* rather than queues an `opg` order between 09:28 and 19:00 ET, so nothing firing in
the European afternoon can sell an amc position into its own opening auction. `bmo_close`
therefore buys +1.77pp of the +3.32pp on offer for one config line
(`flatten_before_entry: false`), and `auction_split` buys the other +1.54pp at the cost of a
second daily Routine at 14:00 Amsterdam that **only a person can create** — `create_trigger`
is refused to agent sessions here, confirmed on 2026-09-10. The prompt is written out in
`edge/routine-prompts/edge-execute.md`. Do `bmo_close` first. **Recycling the amc cash buys
no extra return**: with one auction entry a day the capital slot is 24 hours either way,
which is why `capital_table` in `edge_exit.py` prints return per slot-day equal to return
per trade and flags the hours-held version as a denominator artefact. What it buys is
settled cash before the auction that funds the next book, and fewer hours of exposure. See
`edge/EXECUTION.md`, "The exit the two sessions actually want".

**And the stage has not yet beaten a free control.** `-run_up_20d_pct`, one number from
the sealed baseline available before any subagent is spawned, ranks at ρ=0.335 and is
positive on 6 of 6 days when traded (+10.97pp). The hunt's raw evidence leads it by 0.080
with a CI spanning zero. Note also that `edge_resolve.py --pool` concatenates days and
understates every ranker (0.189 vs 0.243 for `edge_score`), that `confidence` and
`baseline_quality` rank at −0.090 and +0.074 and must not be read as reader guidance, and
that `spearman_vs_move_over_implied` normalises 18 of 43 names on a median historical
reaction rather than an option-implied move. Fix the scorer before spending another day
on hunts.

**Stage E can place its book at Alpaca, and it is switched off.**
`edge/scripts/alpaca_trade.py` takes the one rule that survived a family-wise correction —
`|impact_sum| >= conviction_floor`, side from the sign, plus a $200k turnover floor
and a shortability check — and places it as an immediate market order on the entry
date, flattening at market at the start of the next run. Nothing is sent unless `execution.enabled` is
`true` in `config/pipeline.yaml` **and** `--submit` is given **and** credentials are in
the environment **and** the endpoint is paper; it is committed as `false`.

**It rides in stage E's own Routine, not a separate one.** Two steps in the same
session: step 0b sells yesterday's book at market before the sweep launches, step 7
buys today's **at market, immediately** after the note is published. The sell goes
first so that a session killed mid-hunt leaves the account in cash rather than holding a
book nobody is managing. That trades away the measured exit — the next close ranked
ρ=+0.514, p=0.0015 against ρ=+0.331, p=0.046 to the next open, and selling half an hour
into the session is nearer the open. The immediate entry, by contrast, costs almost
nothing measured: on the same 18 traded events the closing auction gave 15/18 and
+5.86% a trade against 14/18 and +5.82% at 14:00 ET, four hundredths of a point
(`edge/scripts/edge_entry_timing.py`). What that cannot see is the spread, so the fills go
in the run log and `orders.entry: market_on_close` puts it back in the auction. The
only deadline left is that the US session is open; `open` refuses rather than sending
an order into a closed market.
`edge/scripts/alpaca_trade.py close` still does the market-on-close exit if
`orders.flatten_before_entry` is turned off and the fallback exit Routine in
`edge/routine-prompts/edge-execute.md` is added. Sizing is **equal weight, whole
budget**:
the gross budget split N ways, 20% of equity per name, a capped name's leftover
redistributed over the rest. Nothing reads the score — the key ranks and does not
size. Under five names the account is deliberately under-invested, and at 100% gross
the whole account rides five to nine prints overnight with no stop. See
`edge/EXECUTION.md` for what it refuses to do and what it does not know.

The code is on the main line as of 2026-09-10. The 2026-09-10 stage E run found steps 0b
and 7 were no-ops: `edge/scripts/alpaca_trade.py`, `edge/EXECUTION.md` and the `execution`
block did not exist in the tree it cloned, because they were still sitting on
`claude/alpaca-auto-orders-integration-y397gh`. That branch was merged in response, so
the script, the docs and the config block are now here.

**Both of those are done, and the stage now trades unattended.** The prompt was
re-pasted from `edge/routine-prompts/edge-hunt.md` on 2026-09-10 at 13:20 UTC — the
Routine's `updated_at` confirms it and the 14:04 run received both steps — and
`execution.enabled` was turned on later the same day, by the operator, for the paper
account. From 2026-09-11 the scheduled fire flattens the previous book at step 0b and
places a new one at step 7 with nobody watching. Setting `execution.enabled` back to
`false` is the only thing that stops it; the prompt alone will not, and a session
cannot edit the Routine because `update_trigger` refuses any Routine an agent did not
create.

The first book went in by hand on 2026-09-10 at 17:59 UTC: 4 names of 17 (HOFT long,
FEIM/ORCL short, RH long), all filled, gross $7,813 on $10,000 of equity. Three of the
seven above-floor names could not be traded at all — AENT and RENT on the $200k
turnover floor, REF because Alpaca will not lend it — and those were the two strongest
convictions of the day, so the traded book is the middle of the conviction range rather
than the top of it. That run also found two defects, both fixed the same day: sizing
divided by the sealed baseline spot (four hours stale, so a 20.0% cap produced a 20.3%
position) and nothing recorded the quote at submission, which made `orders.entry`'s own
decision criterion uncomputable. See `edge/EXECUTION.md`, "The price the budget is
divided by".

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

**The scripts moved to `edge/scripts/` on 2026-09-10, and four shims stayed behind.**
`scripts/edge_score.py`, `scripts/edge_universe.py`, `scripts/priced_in.py` and
`scripts/alpaca_trade.py` are three-line forwarders. They exist because the live Routine
prompt names those paths, *verifies two of them exist before doing anything else*, and
cannot be edited from a session — so removing them would have stopped the next unattended
run at step 0, before step 0b sold the previous day's book. Delete them once
`edge/routine-prompts/edge-hunt.md` has been re-pasted with the `edge/` prefix. Import the
modules from `edge/scripts`, never from the shims: they forward a command line and expose
nothing.

**A Routine prompt guards on an exit status, not on a config key it reads by eye.**
`python3 edge/scripts/alpaca_trade.py mode --require <mode>` prints the effective
execution settings and exits non-zero unless execution is enabled and that mode is
configured. The second exit Routine's prompt used to say "if `orders.exit_mode` is not
`auction_split`, do nothing", which fails in both directions: a key that has been renamed
away reads as a guard that can never pass, and reports a tidy no-op every morning while
the mode never takes effect; a key that is absent reads as a guard clearly meant to be
satisfied, and puts `cls` orders in at 06:00 ET that the 14:04 flatten then cancels. And
a non-uniform `exit_mode` while `flatten_before_entry` is `true` is now **refused** rather
than documented in three places and enforced in none.

**Stage E moved from 14:04 to 17:04 UTC on 2026-09-10 at 18:28, from outside this repo,
and it eats the entry margin.** `trig_01CvGQJWoKeNLXWCxiffM3ED` now reads
`4 17 * * 1-5` — 19:04 Amsterdam, **13:04 New York** — where every line written about this
stage says 16:04 Amsterdam / 10:04 ET. Its last run under the old cron fired at 14:06 on
09-10. Two consequences, opposite in size:

- **The exit costs nothing.** The `uniform` flatten was measured at ~10:00 ET (+4.49% per
  trade on the conviction book); at 13:00 ET the same grid gives +4.44%. Five hundredths
  of a point. `edge/analysis/edge-exit-hourly.html`, hour 21.
- **The entry margin is gone.** Step 7 buys at market and `open` refuses to send into a
  closed market, so the run must finish before 16:00 ET. From 13:04 that is 2h56m. The
  2026-09-09 run took **2h53m end to end**. Three minutes. A day with more names, a
  retried subagent or a slow sweep misses the entry outright, and the note will still
  publish, so the failure is quiet. Either move the Routine back or make step 7 tolerate
  a closed market by queueing the next open; do not leave it at 17:04 and hope.

The prompt pasted in that Routine still tells the session it fires at "14:04 UTC, which is
16:04 Amsterdam and 10:04 New York". It also tells it to re-read the clock with `date -u`,
which is the only reason that is survivable. Fix it on the next paste.

It is enabled and it is the only pipeline Routine still running. Its prompt cannot be
edited by a session —
`update_trigger` refuses any Routine an agent did not create — so the text lives in
`edge/routine-prompts/edge-hunt.md` and was pasted in by hand on 2026-09-09 at 13:55 UTC;
keep that file in step with the Routine, because nothing else will. Since 2026-09-09 the prompt no longer restates the output contract: the
ranking key is whatever the skill and `edge-scores.json`'s own `ranking_key` field say,
because the old prompt named a key that a measurement then demoted.

**A second Routine now exists: "Close AMC", `trig_01MPuhVvtDgvUYzZXkKpHpKD`, created
2026-09-10 at 18:26 UTC and enabled.** It is the second exit Routine from
`edge/routine-prompts/edge-execute.md`, and three things about it are worth knowing before
`exit_mode` is ever moved off `uniform`:

- **Its cron is `0 10 * * 1-5`, not the `0 12 * * 1-5` that file recommends.** 10:00 UTC
  is 06:00 ET in summer and 05:00 ET in winter, so it does clear both rejection windows
  (`opg` from 09:28, `cls` from 15:50) and nothing breaks. But its own prompt text says
  "You fire at 08:00 New York", which is wrong by two hours, and the reasoning it gives
  for its timing therefore lands by accident. Either move it to `0 12 * * 1-5` or fix the
  sentence; do not leave a Routine whose prompt misdescribes when it runs.
- **Its guard is the old hand-read one.** The pasted text says "if `orders.exit_mode` is
  not `auction_split`, do nothing". That is correct against today's config and today's
  outcome is a correct no-op. Replace it with
  `alpaca_trade.py mode --require auction_split` on the next paste.
- **It names two paths that no longer hold what they used to.** `scripts/alpaca_trade.py`
  is one of the four shims and works unchanged. The old `docs/routine-prompts/edge-hunt.md`
  is gone; `docs/routine-prompts/README.md` was left in its place pointing at
  `edge/routine-prompts/`, because this Routine fires at 10:00 UTC — before any session
  can be asked about it.

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

**One folder per experiment, since 2026-09-10.** `edge/` is stage E, `backtest/` is the
sealed backtest, `claude_naive/` is stage N. `scripts/` holds only what the pipeline
stages share, plus four forwarding shims described below. Nothing about an experiment
lives in `docs/` any more; `docs/ROUTINES.md` is all that is left there, because it covers
every Routine rather than one stage.

```
edge/                                  stage E — see edge/README.md
  EDGE_ANALYSIS.md  EXECUTION.md       what the runs establish; the Alpaca contract
  scripts/                             the stage's own tools
  analysis/                            everything those tools generate
  routine-prompts/                     the text pasted into the Routines, by hand
backtest/                              the sealed backtest
  runs/pilot-40/  runs/edge-corpus/    arms A/B/C; and stage E scored on the corpus
claude_naive/                          stage N
scripts/                               shared: run_paths, publish, run_log, get_earnings,
                                       build_predictions, update_index, validate_stage,
                                       synthesize, smoke_test — and four shims
config/pipeline.yaml                   one config for all of it
.claude/{agents,skills}/               where the harness looks; cannot move

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
  edge/                                 stage E's run for that day
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
