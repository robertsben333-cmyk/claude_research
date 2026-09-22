# claude_research — daily earnings pipeline

This repository runs one thing: a daily research pipeline over US companies reporting
earnings between today's close and tomorrow's open. Each stage is fired by a scheduled
Routine into a **fresh session** that knows nothing except this file and the repo
contents.

If you are a Routine session, read this whole file before doing anything.

## STOP — stages 1, 2, 3 and 4 were retired on 2026-09-18

**If your Routine prompt names `earnings-triage`, `earnings-deep-dive`,
`earnings-panel-advice` or `earnings-calibration`, do not run it.** Append one line to
that day's `_run-log.md` saying the stage is retired, publish, and end the session.
Their Routines still fire because a session cannot disable a Routine it did not create,
so this file is the only thing that stops them. Do not re-create the folders they used
to write.

The measurements are in `archive/README.md`. In one line each: stage 2's preliminary
read went 39 of 75 on direction, which is worse than shorting the same names blind;
stage 3 produced 21 Neutrals and one wrong call in 22 panels because its ±25 threshold
sits above anything a seven-way average can reach, and its hidden signed consensus was
right 6 times in 22; stage 4's headline hit rate turned out to be a restatement of
whether the option-implied move was broken.

**Stage 0 and stage E still run**, and stage E is still placing money. Everything below
about the edge hunt, the execution path and the exit modes is live. The stage 1 to 4
material below is kept because the live stages reference it, not because it runs.

## The stages

| # | Skill | Fires | What it does |
| --- | --- | --- | --- |
| 0 | `earnings-universe` | 07:12 | Fetch and qualify the day's earnings universe |
| ~~4~~ | `earnings-calibration` **RETIRED** | 08:20 | Score *yesterday's* calls, update the ledger |
| ~~1~~ | `earnings-triage` **RETIRED** | 08:38 | Screen it down to ~6 names worth researching |
| ~~2~~ | `earnings-deep-dive` **RETIRED** | 10:22 & 12:22 | One deep Opus/high dossier per name, in two batches |
| ~~3~~ | `earnings-panel-advice` **RETIRED** | 17:52 | Seven-persona panel on the top names → the advice note |
| ~~C~~ | `earnings-capture` **ARCHIVED** | 17:03 | Track B: capture the run-in to *upcoming* prints, before the outcome exists |
| N | `earnings-naive-forecast` | 19:30 | `claude_naive` — the backtest-winning naive method, run live |
| E | `earnings-edge-hunt` | 19:04 | Seal what the market priced, hunt for what it did not, rank the day on one signed number |
| P | `edge-performance` | on demand | Fold every closed position and resolved run into `dashboard/`, rebuild the dashboard, log what it now reads |
| J | `researcher-japan-hunt` | 03:04 | **Stage J — the Japan researcher.** Same question, Tokyo market, research only, no orders. `trig_0192kQeqhumBKpNGzzyQrS1H`, cron `4 1 * * 1-5` = 01:04 UTC = 10:04 JST |
| EU | `researcher-europe-hunt` | 15:30 | **Stage EU — the Europe researcher.** **Ten markets pooled since 2026-09-19** — UK, France, Germany, Sweden, Denmark, Norway, Finland, Italy, Spain, Poland — one stage, seven language-specific hunters, research only, no orders. `trig_018WGfdq2fUm1ZqJhCGQ1wde`, cron `30 13 * * 1-5` = 13:30 UTC, **two hours before the European close on the operator's instruction**, so it seals an intraday spot and not a close. Seals for the NEXT trading day, because Europe reports before the open |
| AU | `researcher-australia-hunt` | 08:30 | **Stage AU — the Australia researcher.** Same question, ASX, research only, no orders. One English hunting pass and no local-language pass, deliberately. `trig_01Qy7FjBpjY4dEGcZsYGnpt3`, cron `30 6 * * 0-4` = 06:30 UTC **Sunday to Thursday**, after the 16:00 Sydney close. Seals for the NEXT session, because 91% of ASX results land before the open, so the fire that seals for Monday is the Sunday one |
| X | (no skill) | 12:00 | "Close AMC" — the second exit Routine. Live since 2026-09-11; `exit_mode` is `amc_open` since 2026-09-15, so it places the amc `opg` legs while stage E sells bmo at market on its own run. See "`exit_mode` moved to `amc_open`" below |

**`list_triggers` IS SCOPED TO THE CALLING ACCOUNT, AND STAGE E IS ON A DIFFERENT ONE.**
Stage E's Routine (`trig_01CvGQJWoKeNLXWCxiffM3ED`) and "Close AMC"
(`trig_01MPuhVvtDgvUYzZXkKpHpKD`) are **not visible from the account this repo's research
sessions run on**, and that is by design, not a fault. Confirmed by the operator on
2026-09-19 after a session called `list_triggers` with `include_completed: true` and
`has_more: false`, got eight Routines, found neither ID among them, and wrote a loud
warning into this file saying the money-placing stage had no schedule. It has one. It is
simply somewhere this tool cannot look.

**So the rule in this file — check the table against `list_triggers` rather than the other
way round — has an exception, and it is the expensive kind.** An absent Routine has two
causes that look identical from here and mean opposite things: it was disabled or deleted,
or it lives on another account. Only the second is true of stage E and "Close AMC". Before
concluding that any Routine is missing, check whether it is one of those two; if it is,
nothing is wrong. For everything else on this account the original rule stands, and stage N
and stage C really were disabled from outside this repo on 2026-09-09.

The three Routines this account *can* see and edit are stage J
(`trig_0192kQeqhumBKpNGzzyQrS1H`), stage EU (`trig_018WGfdq2fUm1ZqJhCGQ1wde`) and stage AU
(`trig_01Qy7FjBpjY4dEGcZsYGnpt3`, added 2026-09-22), all created by a session, all enabled,
all editable with `update_trigger`.

**The research Routines run on Opus.** Stage AU was pinned to `claude-opus-5` at
creation on 2026-09-22 for the same reason the other two were on 2026-09-19: an empty
`model` resolves to the account default and the stage EU hand-fire served
`claude-sonnet-5` that way.

**Stage J and stage EU were moved to Opus on 2026-09-19 09:11 UTC.** Stage J and stage EU
both carried an empty `model`, which resolves to the account default — the stage EU
hand-fire served `claude-sonnet-5`. Both are now pinned to `claude-opus-5` on the
operator's instruction ("move everything to opus"). The config and the agent definitions
were already Opus throughout: every `model:` in `config/pipeline.yaml` reads `opus`, and
the only Sonnet agent left is `earnings-triage-scout`, which belongs to retired stage 1.
So the Routine's own model was the whole gap, and it governs the session that orchestrates
a run rather than the hunters it spawns.

Stage N is not part of the daily advice pipeline. It is `archive/backtest/` arm A promoted to
production: the method that scored 72% direction and +0.90% per trade over 37 events
while the pipeline's own stage-2 method (arm C) scored 55% and lost money. It writes to
`archive/claude_naive/` and reads nothing from `research/`. Its Routine is
`trig_01XmfJNU2CM7q5uvdb5r4ydF` and **it was disabled on 2026-09-09 at 16:16 UTC**,
alongside stage C, by someone outside this repo — observed in `list_triggers`, reason not
recorded anywhere. It had a run due at 17:35 that day and did not take it. Check
`list_triggers` before concluding a missing `archive/claude_naive/<date>/` is a failure. See `archive/claude_naive/README.md` for what
that result does and does not establish — in short, the direction ranking is a lead and
the magnitude finding is the part worth acting on.

Stage E is a second experiment alongside it, and nothing downstream reads it either. It
asks a narrower question than stage N: not "what will this stock do" but **"is there
anything here the market has missed, and how does that rank against the other names
reporting today."** It emits one signed number per company — `impact_sum`, in points of
spot, unbounded — with no call, no threshold and no direction label, because the question being tested is whether the day's
companies can be **ranked** — and that is only answerable at every cut if nothing was
rounded into a bucket upstream. Falsifiable by `researcher_us/scripts/edge_resolve.py`, which reports
Spearman rank correlation against the realised move with a permutation p-value. Until
many days have pooled, it is not better than anything.

Ten runs exist: two on 2026-08-31 and one on each of 09-01, 09-02, 09-03, 09-04, 09-07,
09-08, 09-09 and 09-10. Six are resolved — **43 names, 249 findings, 65 hunts**; the
09-08, 09-09 and 09-10 runs are not. (This paragraph said "seven" and omitted 09-09
until 09-10; the six-resolved decomposition in `researcher_us/EDGE_ANALYSIS.md` is unaffected,
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

**The analysis has been reading six days out of thirteen, since 2026-09-09.**
`edge_decompose.py` reads `edge_score`, `edge_pct`, `confidence` and `baseline_quality`
off each ranked row, and those left the top level of `edge-scores.json` the day
`impact_sum` became the key. It has raised `KeyError: 'edge_score'` on every run since,
so **every number in `researcher_us/EDGE_ANALYSIS.md` still rests on 38 de-duplicated events**
while seven more run days sat on disk in no sample at all.
`researcher_us/scripts/edge_sample.py` reads the fields both schemas carry and loads the lot:
**106 resolved, de-duplicated events over 13 hunt days, 55 above the conviction floor.**
It sums `impact_sum` from `findings` for the pre-09-09 runs — that is the definition of
the field, not a reconstruction, and all 38 rows of the existing `edge-rows.json`
reproduce exactly. Use it for anything new; `edge_decompose.py` is still the only thing
that computes the residual/cluster decomposition, and it is still broken past 09-08.

**On that larger sample the free control stops working, and the hunt still beats doing
nothing.** `-run_up_20d_pct` ranks the first six days at ρ=0.335 and was positive on 6 of
6 days traded; over 105 events it returns **−0.42% per trade**. So the control that every
paragraph above measures the hunt against is not stable either. What survives: the hunt
above the floor pays **+3.37%** per trade against **+1.59%** for shorting every name with
no research at all.

**`w2` IS THE WEIGHTING BEING CARRIED FORWARD (2026-09-18, operator's design).** The
conviction floor stays the only gate — no factor adds a name and none removes one — and
four factors set the SIZE instead: more findings, retail tilt, price-lean agreement, less
search traffic, each −1/0/+1, weight = clamp(1 + 0.125·Σ, 0.5, 1.5), with the per-name cap
raised from 33% to **50% of equity**. A wrong factor costs size on a good name and can
never buy a name the hunt did not conviction-rank, which is where `w1` lost.

**The factors are measured on all 105 researched names, not on the 56 the floor buys
(2026-09-18).** The books are placed above the floor because that is what the gate buys;
the factors are a claim about the hunt, and the floor selects on `|impact_sum|`, which is
not what any of the four measure. On the doubled sample **all four keep their sign** and
every level falls, because the below-floor half returns −2.98% per name against +3.69%
above it: more findings +1.32% against +0.18%, retail +2.15% against −0.85%, lean agrees
+2.88% against −1.96%, less search +0.41% against −1.12%. The 49 names below the floor are
the one part of these days no factor was chosen on, and there the two register-backed
factors keep their sign (retail +1.64pp, lean +2.93pp) while the two without it invert
(`evidence` −1.86pp, `search_quiet` −2.29pp). No gap reaches two standard errors and
nothing moves on it.

**The headline mixes a risk decision and a research claim, so read them apart.** Per day
over 12 traded days: **A** normal (equal, cap 33) +4.28%, t 2.36; **B** cap 50 only
+4.94%, t 2.44; **C** w2 weighted at cap 50 +5.12%, t 2.37; **D** w2 weighted at cap 33
+4.37%, t 2.18. A→B is the cap (+0.66pp, and deployment goes 94%→100% because 33% left
cash on thin days). B→C is the weighting: **+0.18pp with the sd up from 7.01 to 7.47, so
t falls**. At the old cap the weighting is worth +0.09pp and t falls to 2.18. **The
capital decision carries the result; the weighting earns close to nothing and buys
variance.** All four factors point the right way one at a time (lean +7.27% against
+0.11%, search-quiet +5.32% against +0.37%, retail +4.68% against +2.47%). `evidence` is
in on instruction and is the one factor H7 measured as `geen effect` alone — first to drop
if w2 underperforms. **The 50% cap is the only risk control in the stage**: the 23%
single-name gap that moved the account 4.5% at a 20% cap and ~7.5% at 33% moves it ~11.5%
at 50%. Nothing is switched on; w2 is computed beside the live rule.

**`w1` IS SUPERSEDED AND KEPT (2026-09-18).** `dashboard/scripts/weighting.py`, version `w1`, frozen today:
`w_score = impact_sum * clamp(1 + 0.15 * Σ tilts, 0.5, 1.5)`, four tilts at −1/0/+1 —
price-lean agreement, search quiet, retail tilt, sector — one magnitude for all four
because four fitted weights on 56 traded names is memorisation. `edge_score.py` is
untouched and the book is still placed on the plain score. **Nothing in that spec may be
re-tuned**: a tilt that turns out wrong becomes `w2` beside `w1`, never an edited
constant, because a constant that moves with the data is not a hypothesis.

**In sample the symmetric variant LOSES, and that is the finding.** +3.09% per name
against +3.69% for the plain rule, on the very days every tilt was chosen from.
Decomposed: the names it drops were correctly dropped (+0.22%), what it keeps beats the
book (+4.27%), and the four names it promotes over the floor return −11.01%. Every tilt
on its own points the right way. The damage is entirely in promotion — the conviction
floor is the only rule here that ever cleared a family-wise correction, and a tilt chosen
on 13 days was overruling it. So `w1_filter` ships beside it: demote-only, structurally
unable to add a name the floor rejected, +4.27% on 48 names. **Both are frozen and both
run forward**; picking the better one on the sample that produced it is the same error
one level up. The `Weging` tab tracks them per day.

**There is a hypothesis register on the dashboard, and it is NOT part of the skill
(2026-09-18).** The `Hypotheses` tab is a place to test, not a step in a routine — do not
fold it into `edge-performance`. Intermediate variables are screened first against three
outcomes that are not the same question (sign right / book return / move size), and the
named hypotheses were written after reading that screen, which the tab states in its own
header. One verdict rule for all of them: the gap carries the predicted sign and clears
two standard errors of its own difference. A hypothesis comparing the same names at two
exits is **paired** and tested on the per-name difference.

The hypotheses are asked of the TRADED BOOK, not of every ranked name, and the verdict
ladder has a middle rung — `mogelijk · meer data` for a gap that is practically large
(≥ 1.5pp per name) with |t| still under 2, printed with how many names it would take to
settle. Of ten on 13 days: one sector carries the result (Consumer Cyclical 27
names, 70.4%, +5.97% against Technology 48.3%, −1.89%), the hunt pays more where it
**agrees with the sealed price lean** (ρ +0.33 on the book, p 0.017), and the conviction
floor — the anchor. **The price-lean result is the uncomfortable one**: this stage exists
to find what the market has missed, so a variable saying it earns most where it follows
the price points the other way, and it is the first thing to measure forward. What does
NOT survive includes two that were expected: bmo over amc, and the amc-early / bmo-late
exit split — the paired tests give +1.88pp (16/28, t 0.93) and +2.18pp (19/28, t 1.20),
both leaning the predicted way and neither clearing |t| = 2. And `retail_tilt` interacts
with the floor rather than adding to it: high tilt above the floor is 78.1% / +4.90%,
high tilt below it 38.1% / −3.66%, low tilt ~46% either way. **Move NOTHING on any of
this** — thirteen days, no multiplicity correction, every rule chosen after seeing these
days. Three of the four variables that clear the screen's rough bar rank move SIZE, which
is volatility and not skill.

**The dashboard's default exit is the strategy's, not a horizon (2026-09-18).** One
column cannot describe this book: amc sells into the opening print at **15:30 CET**
(`mv_open`) and bmo at **20:00 CET** (`hr_22`). `attach_strategy_exit()` resolves it
per session and carries it as if it were a horizon, so every tab reads it like the
eight fixed ones, which stay selectable. On the conviction book it pays +3.69% per name
against +3.19% at the close. **It disagrees with the live config by an hour**:
`orders.exit_mode: amc_open` sells bmo at plain market on stage E's own 13:05 ET run,
which is 19:05 CET. Over the 28 bmo names above the floor the three are monotonic —
+4.24% at 19:05, +4.36% at 20:00, +5.22% at the close — so the config is the worst of
them and the dashboard default is the middle. Pick one rather than leaving the page and
the account disagreeing.

**The dashboard is `dashboard/` at the top level, and it is the one reading surface.**
It was `edge/performance/` on the unmerged branch `claude/epic-ride-s4bcg4` until
2026-09-18; merging it was the fix for "there is no dashboard in the repo", which is
what a session concluded from the git history alone while the branch sat unmerged.
Open `dashboard/dashboard.html` off the disk — no server, no network, no CDN — and
rebuild it with `./dashboard/update.sh`. Everything on the page is recomputed
client-side from `dashboard/data/ledger.json`, so every control re-derives every
statistic under it rather than filtering a view. Its own README is the authority on
the controls and the three levels (names / trades / account), which are not the same
thing and must not be mixed.

**And it rebuilds itself in CI since 2026-09-19, because the button could not work on a
fetched page.** `.github/workflows/dashboard.yml` — the first workflow in this repo —
runs the same `./dashboard/update.sh`, commits `dashboard/` back to `main` and publishes
the page to GitHub Pages at <https://robertsben333-cmyk.github.io/claude_research/> —
**which needs Settings → Pages → Source set to *GitHub Actions* once**, because
`GITHUB_TOKEN` is refused when it asks to create the site; until that is done the
workflow rebuilds and commits as normal and skips the publish rather than going red. It
fires at 11:40 and 21:40 UTC on weekdays, on a push touching `research/` or the scripts,
and on demand. The page's own button now knows which of the two worlds it is in: a local
rebuilder on `127.0.0.1:8765` (**live**) or the workflow (**CI**), and on a fetched page
a click dispatches the run, watches it and reloads. It is read-only about the broker like
every other part of `dashboard/` — no order is ever placed, cancelled or amended from it.
Two things it needs: `ALPACA_API_KEY_ID` / `ALPACA_API_SECRET_KEY` as **repository
secrets**, without which the build passes `--offline` and the trades and equity curve
stay at the last build that had them; and a GitHub token in the browser for the button
to dispatch, without which the click opens the workflow page instead. **Its commit
touches only `dashboard/` and the three feeder files, and its `paths:` filter excludes
them, so it cannot trigger itself** — do not add `dashboard/**` to that filter.

**The other three researchers have their own tabs since 2026-09-22, and they are the
research level only.** `Europa`, `Japan` and `Australië` are fed by
`dashboard/scripts/build_markets.py` into `dashboard/data/markets.json`, which
`build_dashboard.py` inlines beside the ledger; `update.sh` runs it with `--resolve` as a
third feeder that may fail without costing the rebuild. **There is no money level on
those three tabs and there must not be one**: stages EU, J and AU place no orders, so the
ledger's trades and equity curve say nothing about them, and the filter bar (lens, cap,
sector, exit horizon) is hidden on a market tab because none of it has anything
underneath. The collector does NOT own the outcome window — Europe and Australia are
`close(D−1) → close(D)`, Tokyo is close to next open — it reads the `*-resolved.json`
that `eu_resolve.py`, `jp_resolve.py` and `au_resolve.py` write, and with `--resolve`
calls the market's own resolver for a run whose window has closed and which has none. A
resolved file whose rows are all `move_pending` is fetched again, because Yahoo's
European closes lag a session and treating that file as done would freeze the day at
nothing for good.

**What those tabs show today is almost nothing, which is the point of building them
now.** Europe: four runs, 18 hunted names, 59 findings, and **the only resolved days are
the two validation runs that ran on synthetic findings** — excluded by default, behind a
switch that names them. Japan: two hunted days, three names, nothing resolved, plus two
days on which Tokyo was shut and the runs table prints the holiday instead of a zero.
Australia: no run directory in `research/` at all, since its validation never landed
there. Three rules are enforced in the rendering rather than left to a reader: an
unhunted name (`rankable: false`, seven UK names on 09-23) is shown with
`not_rankable_because` instead of the 0 the scorer writes and counts in no statistic; a
shut exchange is not a failed run; and **ρ is withheld below five names**, because on
three a rank correlation of 1.0 arrives one time in six and `au_resolve.py` already says
so.

**Three new questions, three near-nulls and one lead (2026-09-18).** They are tabs on
that dashboard — `Instap`, `Aanloop`, `Zoekvolume`, plus `Agenda` — not separate pages.
An earlier standalone set under `researcher_us/analysis/dashboard/` was deleted the same day: two
renderers over one dataset is the drift this repo keeps paying for. The artifact
https://claude.ai/artifact/JjEfQYMhb1UN25SCGp4SK3 is a dated snapshot of that interim
version and is not maintained.

- **The pre-print run-up says nothing** (`edge_runup.py`). The 2/5/10/20-session return
  to the 20:00 CET entry does not predict whether the hunt's sign was right: largest
  |ρ| 0.153, smallest p 0.117, hit rate flat at 49–57% across run-up terciles. And
  agreement between run-up and prediction does not pay on the book that is traded — over
  all names the 2d window looks helpful (+2.55% against −1.12%), above the floor it
  **inverts at all four windows** (10d: +0.71% agreeing against +5.75% disagreeing).
  Two subsets pointing opposite ways with overlapping intervals are noise measured twice.
- **The entry hour does not matter** (`edge_entry_clock.py`). Exit held fixed, entry
  swept 10:00–16:00 ET in half hours: best minus worst over the whole session is
  **0.40pp** on the conviction book against a per-trade sd of 15. The close is nominally
  best (+3.59% against +3.37% at 20:00 CET) and that gap is not worth acting on. There is
  no intraday drift to time either — no t above 1.6 on the unsigned drift to the close.
  What the grid cannot see is the SPREAD, which is the one real argument for entering
  later and is unmeasured; TRT quoted a 14.6% half-spread on 09-17.
- **Google search attention is the one lead** (`edge_search_volume.py`). Daily Trends
  interest, US, 90 days to the entry, one fixed query per company (registered name minus
  the legal suffix, never the ticker — "TRT" and "RH" are English words). Above the
  floor the entry-day spike ranks at **ρ=−0.504, permutation p=0.018 on 22 events**: more
  attention, worse outcome, and the high-attention names also move least (median 4.67%
  against 10.08%). It is one cell out of ten looked at — **p=0.18 after Bonferroni** — and
  the measurable half is systematically the liquid half (median turnover $22.7m against
  $1.4m for the names Google reports nothing for). The cheap way to settle it is to put
  the spike in the sealed baseline beside `run_up_20d_pct` and let it pool.
  **Read `measures()` before trusting any Trends number**: each series is normalised to
  its own maximum, so a name searched on three of ninety days reads 0…0,100 and a spike
  over a zero median comes out at 100×. Eleven such names filled the top tercile on the
  first run. A series now needs a non-zero median to be scored at all.

**`edge_runup.py`, `edge_entry_clock.py` and `edge_search_volume.py` are the CLI
versions of those three tabs.** The dashboard does not call the first two — the ledger
computes `enpx` and `runup_*d` from its own bars, so there is one price source — but it
does read `edge-search-volume.json`, and `update.sh` runs that script and the calendar
before every build. Either feeder may fail without costing the rebuild.

**`edge_calendar.py` is the forward week, with both gates applied.** Nasdaq's calendar
with the `time-not-supplied` rows and the `min_dollar_volume_usd` floor counted
separately rather than folded together, so the candidate count is honest: 80 rows to
2026-09-25, 25 with a confirmed session, 22 clearing the floor. It carries no prediction —
that comes from a hunt that has not run.

**The ordering problem is fixed; the scorer is now the problem.** `researcher_us/EDGE_ANALYSIS.md`
decomposes all six resolved runs, pooling *within* days (`researcher_us/scripts/edge_decompose.py`).
The shipped `edge_score` ranks at ρ=0.243, p=0.156 — not significant. The hunters' raw
impact sum, before the cluster-max, the √k discount, the agreement discount and the
quality multiplier, ranks at ρ=0.407, p=0.017. A paired bootstrap over days puts that
gap at +0.165 with a 95% CI of [+0.082, +0.244], so the aggregation in
`researcher_us/scripts/edge_score.py` is subtractive, not small-sample noise. Traded as a long
top-third / short bottom-third, the shipped ranking returns +2.17pp per day against
+11.45pp for its own raw inputs.

**Money placed on it would have lost to doing nothing.** `researcher_us/scripts/edge_trade.py` runs
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
too. See `researcher_us/EDGE_ANALYSIS.md`, "Conviction is where the direction lives" — the
sign of the impact sum over all 38 events is a coin flip (53%), so the conviction floor is
the whole finding.

**About a third of that conviction number is the double hunt.** Every one of the 38 events
was scored while the day's two highest-`hunt_priority` names got two hunters and the rest
got one, and the key is a *sum*, so those names carry the largest conviction by
construction: 10 double-hunted names average 8.00 findings and |impact| 9.13 against 3.71
and 3.53 for the other 28. `researcher_us/scripts/edge_hunter_control.py` rebuilds every name's key
from a single hunter — the only control that keeps all 38 events, since dropping the
double-hunted names selects on a sweep score assigned before any hunting. Rebuilt, the
conviction correlation falls from +0.514 (p=0.002) to +0.361 (p=0.045) and the ranking from
+0.360 to +0.303 (p=0.099). Inflated, not manufactured — but the forward regime is one
hunter per name, so **+0.361 is the number to expect, not +0.514**, and on single-hunted
names alone the `|pred| >= 3` cut the trading rule rests on is 9/14 at +4.62% with a
bootstrap interval spanning zero. See `researcher_us/EDGE_ANALYSIS.md`, "The double hunt inflates
both headline numbers".

**Scored on the sealed backtest corpus, the hunt found no rank signal at all.**
`archive/backtest/runs/edge-corpus/` re-runs stage E over 104 resolved events on 7 days of
point-in-time captures, judged by `archive/backtest/scripts/edge_corpus_report.py`: ρ=+0.073
(p=0.45) raw, +0.109 (p=0.27) normalised, and no subgroup — clean captures, corpora holding
news, measured rather than inferred sessions — reaches significance. That is 104 events
against 38, on a corpus the hunters could not see past, and it is the single most
discouraging number in the repo. Read its caveats in `archive/backtest/FINDINGS.md` §33 before
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
and nobody chose it. `researcher_us/scripts/edge_exit.py` re-resolves all 38 de-duplicated events at
eight horizons off 5-minute pre/post bars (`researcher_us/analysis/edge-exit.json`). No *uniform* early
exit is distinguishable from holding to the close: every horizon's Δρ against the close
has a CI spanning zero, and the family-wise p over the eight is 0.115. But the two legs
of the hold cancel rather than agree. The entry-to-open gap ranks at ρ=0.315 and pays the
whole conviction book (+6.21%, t=2.99); the open-to-close session leg ranks at ρ=0.078
and pays −0.20%, for 6 points of movement sat through. And the two sessions want opposite
things: **amc** gaps at ρ=+0.273 / +8.91% and then gives back −3.00% intraday (−2.61%
day-demeaned, and the book is 6 long / 6 short so it is not drift), while **bmo** is
+0.187 at the open and +0.670 at the close. Selling into the release is the one variant
the sample rejects: only 46% of the move exists there and for bmo names its ranking is
negative. Priced per hour of the clock (`researcher_us/analysis/edge-exit-hourly.html`), the conviction book
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
cutoff at the current clock so nothing unresolved is reported (`researcher_us/analysis/edge-exit-forward.json`).
On 09-08 plus 09-09 — 30 names, 14 above the conviction floor, neither day in the fitted
sample — every horizon available on both days is flat to negative: −1.42% per trade in the
after-hours, −0.05% at the opening print, −1.22% an hour in. On 09-09 the free control paid
+3.9% to +4.5% per day at every hour after 08:00 against −0.2% to −0.9% for the hunt's own
book, and the two largest predictions were both wrong and large (NAVN +10.0 fell 18.4%, WLTH
−10.5 rose 8.0%). And `archive/backtest/RESULTS.md` priced its 37 sealed events at both exits: all
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

**`exit_mode` moved to `amc_open` on 2026-09-15, on the operator's requirement that a
bmo leg is gone before the same afternoon buys the next book.** amc still exits at the
open from the "Close AMC" Routine (as an `opg` order until 2026-09-18, as a market DAY
order queued in the pre-market since); bmo now goes at **plain market on stage E's
own run at 13:05 ET** instead of into that day's closing auction. It is measurably worse
on the fitted sample and that was accepted, not missed: `researcher_us/scripts/edge_exit.py` scores
it as the `amc_open_bmo_1300` policy at ρ=0.391, 16/22 and **+6.49% per trade (t=3.42)**
against ρ=0.461, 17/22 and +7.81% (t=4.01) for `auction_split` — 1.31pp, on a paired day
bootstrap against `uniform_close` of +0.57 [−2.86, +3.18], so neither is established. Two
things that number cannot see: the +6.48% for a bmo closing auction **assumes the `cls`
order fills**, and on this book it has filled 39 of 183 and 17 of 161 before expiring; and
a bmo leg still open at 13:05 ET is still open when step 7 buys at 13:24 ET, so gross
exposure stacks — VRA and FPS were held straight through LUXE's entry on 09-15, and
`open`'s refusal does not catch it because a leg whose exit order is *working* is not past
its exit date. A market sell is verifiable inside the same session, so the budget the
entry divides is a known quantity. What it does not buy is return per unit of capital:
`capital_table` prints return per slot-day equal to return per trade for every policy,
because with one entry a day the slot is 24 hours either way.

**The second Routine's guard had to change with the mode, and only a person can paste
it — it has been pasted, and it still passes.** "Close AMC" exists to place the exit that
must go in before the open, and its original guard named `auction_split`, so from
2026-09-15 it failed and reported a correct-looking no-op every morning while no amc leg
reached its auction. It was re-pasted with `alpaca_trade.py mode --require-exit-tif opg`,
which the 2026-09-17 run confirms: two `opg` orders went in at 10:05 UTC. Since
2026-09-18 that guard asks about the PLACEMENT rather than the literal instrument, so it
exits 0 although the amc exit is now a market DAY order queued for the open. **Do not
re-paste it to name the new tif** — a session cannot edit a Routine, so a guard that
failed shut would be the same silent no-op again. `--require` also takes a
comma-separated list.

**The auction exits did not sell because this account cannot place an auction order.**
Ten exit legs have gone into an auction since `exit_mode: auction_split` shipped. **One
filled in full**: ORCL, the only mega-cap. HOFT filled 17 of 161 and expired, CODA 39 of
183, FEIM 0 of 31, RH 0 of 14, RLGT 0 of 224, VRA 0 of 642, FPS 0 of 64, LUXE 0 of 292 —
and on 2026-09-17 ALMU 0 of 167 and **LEN 0 of 28**, expired at 09:30:52 ET. Twenty-eight
shares of a $20bn homebuilder in its own opening cross is not a liquidity problem, which
is what this paragraph said for a week on the strength of the thin-name rows alone. The
cause, checked against Alpaca's docs on 2026-09-18, is the account: *"OPG and CLS orders
are only available to Elite Smart Router users"*, and this is an $11.5k paper account.
Paper compounds it — fills there are simulated against the NBBO quote stream with
"partial fills for a random size 10% of the time", which describes the 17-of-161 exactly.
Nothing rejects the order; it is accepted, it sits, it is cancelled at a cross it never
reached.

**And the early Routine was taking the bmo leg too (fixed 2026-09-18).** `close` takes
every leg whose exit date is today and two runs a day call it, so "Close AMC" at 06:05
ET was selling the bmo leg as well as the amc one. Harmless under `auction_split` —
bmo wanted `cls` and a closed market refuses it — but live under `amc_open`, where the
bmo instrument is a plain DAY order that Alpaca **queues for the open**. TRT's exit
went in at 06:07 ET on 09-18 that way, so the book ran amc at the open and bmo at the
open, against a configured policy of bmo at market on stage E's 13:05 ET run, and bmo
is the session that measured worst at the open (+2.96% against +6.48% at the close and
+2.58% around 10:00 ET). `close` now defers a leg whose placement is `market` to the
run that fires inside the session, with two exemptions: an overdue leg still goes
immediately, and nothing is deferred when the clock could not be read.
`defer_to_session_run()` is the whole rule and `smoke_test.py` covers all four cases.

**The fix separates WHERE an exit is aimed from WHICH order gets it there
(2026-09-18).** `orders.auction_orders` is new and `false`: `exit_placement()` returns
`open`/`close`/`market` from the mode, and `exit_tif_for()` turns that into an instrument
the account has. `amc_open` still sends amc to the open — now as a plain market **DAY**
order submitted in the pre-market, which Alpaca accepts while the market is closed and
routes at the next open. The pasted "Close AMC" guard `mode --require-exit-tif opg`
**still exits 0**, by design: it matches on the placement family, because a session
cannot edit a Routine and a guard failing shut would mean a tidy no-op every morning
while the amc legs went unsold. Do not "correct" it to the new tif. What this costs is
the difference between the 09:30 auction print and the NBBO seconds later, widest in
exactly the thin names this book trades; what it buys is an exit that happens. **Still
unmeasured on this account: whether a queued pre-market DAY order fills at the open.**
Alpaca's docs say it does and `auction_window()` has assumed so since 09-16, but this
book has never sent one — `researcher_us/EXECUTION.md` has a one-share test, paired against an
`opg` control, that settles it in one morning.

What made the failures open positions rather than logged misses was three things in this
repo, all fixed on 2026-09-15: `send` stored the status Alpaca returns at submission —
always `pending_new` — and nothing ever re-read it; the retry asked for the same auction,
so RLGT's 13:05 ET retry was refused inside Alpaca's 09:28–19:00 `opg` window and the
position sat another day; and `upsert` merged records, so a successful retry kept the
failed attempt's `reason`. The operator has been closing these by hand — the market
orders at the broker carrying random client_order_ids, most recently ALMU and LEN at
09:47 ET on 09-17. **`close` waits `orders.fill_check_seconds` (300) and re-reads every
exit it sent, and `alpaca_trade.py verify [--fix --submit]` does it on demand**: per leg,
closed / working / UNFILLED, where UNFILLED means shares still held and every order for
the leg dead at the broker. `--fix` re-sends the residual at plain market, sized to what
Alpaca reports is held and only while every prior order is dead — and from the pre-market
that rescue now works rather than being refused, because a market DAY order is accepted
while the market is closed. See `researcher_us/EXECUTION.md`, "The auction exits mostly did not
sell, and the reason was the account".

**The per-session exit is three modes in `alpaca_trade.py`; it shipped on the dullest one
until 2026-09-11** (see "`exit_mode` moved off `uniform`" below for what runs now).
`orders.exit_mode` picks which instrument closes a position, per session. Per trade
over the 38 de-duplicated events, on the conviction book: **`uniform`** +4.49% (t=2.52),
the flatten selling everything at market when the next run starts, about 10:00 ET;
**`bmo_close`** +6.27% (t=3.34), amc at market on the run and bmo into today's closing
auction; **`auction_split`** +7.81% (t=4.01), amc into the opening auction and bmo into the
close. The two sessions want opposite things — amc pays +8.91% in the opening auction,
+6.08% at 10:00 ET and +5.23% at the close, bmo pays +2.96%, +2.58% and +6.48% — because an
amc print has had a whole overnight to be processed while a bmo print has had two thin hours
of pre-market and keeps repricing.

**`bmo_close` was reachable from the existing Routine alone; `auction_split` needed the
second one, which now exists.** Alpaca *rejects* rather than queues an `opg` order between
09:28 and 19:00 ET, so nothing firing in the European afternoon can sell an amc position
into its own opening auction — that is what "Close AMC" (created 2026-09-10, cron `0 10
* * 1-5`) is for. `bmo_close` bought +1.77pp of the +3.32pp on offer for one config line
(`flatten_before_entry: false`); `auction_split` buys the other +1.54pp on top of that
Routine, which **only a person could create** — `create_trigger` is refused to agent
sessions here, confirmed on 2026-09-10. The prompt is written out in
`researcher_us/routine-prompts/edge-execute.md`. `auction_split` ran from 2026-09-11 until the
2026-09-15 move to `amc_open` — see below; what this paragraph says about the second
Routine still holds, because `amc_open` keeps the same `opg` leg. **Recycling the amc cash buys
no extra return**: with one auction entry a day the capital slot is 24 hours either way,
which is why `capital_table` in `edge_exit.py` prints return per slot-day equal to return
per trade and flags the hours-held version as a denominator artefact. What it buys is
settled cash before the auction that funds the next book, and fewer hours of exposure. See
`researcher_us/EXECUTION.md`, "The exit the two sessions actually want".

**The performance record has its own place, and on the current sample it
contradicts the paragraphs above.** `dashboard/` holds one ledger over every run, every fill the broker reports and the equity curve, plus a dashboard built from
it; `./dashboard/update.sh` rebuilds both (`--serve` makes the page's own
refresh button work) and the `edge-performance` skill folds in what has closed since
the last build and writes the reading into `dashboard/LOG.md`. It is read-only:
it never places an order and never re-scores a run. The page recomputes every statistic
client-side under a lens (research or money), an exit horizon, a conviction threshold,
a per-side turnover floor, a session and a sector — so a threshold can be swept rather
than assumed, which is how the first slice worth acting on turned up: **raising the
threshold lifts bmo monotonically (+2.5% at ≥0 to +12.0% at ≥7) and lowers amc over the
same range (−0.7% to −2.9%)**, and the pooled curve is the average of two opposite
movements. Do not move `conviction_floor` on it yet — at ≥7 that is nine bmo names
against eleven amc. Its first build, 2026-09-17, prices 102 ranked names over 11 days
and puts the pooled ranking at **ρ = −0.145 against −0.137 for the free control**.
The split is by date, not by method: the five days `researcher_us/EDGE_ANALYSIS.md` was
written on pool at ρ ≈ +0.38 and reproduce its conviction figure, and every day from
09-08 onward is at or below zero. The account is +17.3% over eight sessions on nine
closed positions — six longs at +17.7% against three shorts at −13.9%, in a week when
shorting everything paid −1.7% a name, so that number is a market and not a result.
Six of those nine were closed by hand rather than by stage E, and HOFT and CODA sat
95 hours before someone sold them. Read the dashboard's first screen before quoting
any figure in this file: the numbers above were measured on the first six days and
the ledger is what is measuring them now.

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
`researcher_us/scripts/alpaca_trade.py` takes the one rule that survived a family-wise correction —
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
(`researcher_us/scripts/edge_entry_timing.py`). What that cannot see is the spread, so the fills go
in the run log and `orders.entry: market_on_close` puts it back in the auction. The
only deadline left is that the US session is open; `open` refuses rather than sending
an order into a closed market.
`researcher_us/scripts/alpaca_trade.py close` still does the market-on-close exit if
`orders.flatten_before_entry` is turned off and the fallback exit Routine in
`researcher_us/routine-prompts/edge-execute.md` is added. Sizing is **equal weight, whole
budget**:
the gross budget split N ways, **33% of equity per name since 2026-09-17** (20%
before, raised on the operator's instruction), a capped name's leftover redistributed
over the rest. Nothing reads the score — the key ranks and does not size. Under three
names the account is deliberately under-invested, and at 100% gross the whole account
rides three to nine prints overnight with no stop. The cap is the only risk control in
the stage, so what the raise costs is concentration and nothing else changed to offset
it: the 23% gap that moved the account 4.5% at 20% moves it about 7.5% at 33%. See
`researcher_us/EXECUTION.md` for what it refuses to do and what it does not know.

The code is on the main line as of 2026-09-10. The 2026-09-10 stage E run found steps 0b
and 7 were no-ops: `researcher_us/scripts/alpaca_trade.py`, `researcher_us/EXECUTION.md` and the `execution`
block did not exist in the tree it cloned, because they were still sitting on
`claude/alpaca-auto-orders-integration-y397gh`. That branch was merged in response, so
the script, the docs and the config block are now here.

**That failure repeated twice on 2026-09-15 and cost two live things, so check the
branches before blaming an agent definition.** Both were merged on 2026-09-16 and both
had been sitting unmerged for a day while the Routines ran against a tree without them:
`claude/optimistic-hypatia-5qvags` held `researcher_us/LESSONS.md` and the hunter contract that
returns `print_vs_bar_pct`, which the pasted Routine prompt already asked for — so the
09-16 run's "agent-definition drift" was a missing merge. `claude/alpaca-sell-orders-filling-mwumuw`
held the `verify` subcommand, `mode --require-exit-tif` and the `amc_open` exit mode, so
the "Close AMC" Routine failed its own guard on 09-16 with an argparse error, submitted
nothing, and left VRA and FPS two days overdue. The tell is the same both times: the
Routine prompt names something the tree does not have. A session cannot edit a Routine,
so the tree is what moves — merge first, and only then suspect the definition.

**Both of those are done, and the stage now trades unattended.** The prompt was
re-pasted from `researcher_us/routine-prompts/edge-hunt.md` on 2026-09-10 at 13:20 UTC — the
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
decision criterion uncomputable. See `researcher_us/EXECUTION.md`, "The price the budget is
divided by".

Run 2's own failures are written into the skill and the agent definitions rather than
left in the run log: a same-directory collision between the two runs that would have
pooled twelve stale zeros into run 2's ranking, a cadence heuristic in `priced_in.py`
that flagged four company-confirmed reporters as non-events, an adversary agent with no
`Write` tool, and two entries of `budget.edge_degrade_order` that each contradicted a
hard rule stated elsewhere. All four are fixed.

**The hunters learn from the resolved days through one file, `researcher_us/LESSONS.md`** (since
2026-09-15). It holds the patterns that repeated across the post-mortems of 09-08 through
09-14 — a verified fact is not a predicted reaction, name the line a finding lands on,
the hunter's own caveat has to reach the number, financing is a question, a narrow proxy
loses to a broad series, verify the bar and keep findings inside the exit window,
positioning is the thing to beat — as rules with no company fixes in them. The hunter
now answers two questions (`print_vs_bar_pct` and `expected_move_pct`), each finding
carries `lands_on` and `resolves_by`, and `researcher_us/scripts/edge_postmortem.py` scores a
resolved run finding by finding so the file can grow from measurement.

**`time-not-supplied` rows are checkable, since 2026-09-17, and on that day the check
bought back nothing.** Nasdaq's `time` field is a schedule for `time-pre-market` and
`time-after-hours` and an admission of ignorance for `time-not-supplied`, and the third
case is usually the larger half of the calendar: 20 of 22 rows on 2026-09-17, leaving
**one name in the window**. `researcher_us/scripts/session_resolve.py` checks the dropped rows
against two free sources and no agent — EDGAR kills a row whose results were filed in
the ten days before the event, Nasdaq's press-release feed confirms one the company
itself announced a date for. On the twelve labelled rows of 2026-08-31 the `announced`
test kept **4 of 4 real reporters and none of the 8 phantoms**. It is precise and not
sensitive: on 2026-09-17 it confirmed none of the twenty, and **it was right about all
twenty**. TRT was recovered by hand on the cadence evidence the script had already
returned (`unresolved / fits / last item-2.02 2026-05-14, 126 days`), cleared the floor
at +5.10, was the day's only trade — **and never reported**. EDGAR on 2026-09-18: last
item-2.02 still 2026-05-14, and the 2026-09-15 filings are CERT / Form 25 / 8-A12B, an
exchange transfer. Its baseline now carries `event_occurred: false` and it is out of
every ranking and pooled sample; the trade stands in `alpaca-orders.json` because it
happened. So the measured phantom rate on `time-not-supplied` is **20 of 20** for the
09-17 window and 8 of 8 for 08-31, and withholding `--include-unknown` cost that day
nothing at all. `--announced-only` is still for a day with more confirmed names than
hunters rather than a thin one, but the reason is no longer that it would have cost a
real name — it is that one day of 20 does not establish recall. **The cadence prior is
the part that failed.** It read `fits` on TRT and on two 08-31 phantoms; it is the same
defect that made `priced_in.py`'s cadence heuristic useless as a filter, and on 09-17 a
human read it as confirmation and put 33% of equity behind it. Read it as a prior, never
as evidence a print exists. It cannot settle the **session** either: Nasdaq serves the
release body as a JavaScript shell, so a carried row reaches the sweep with
`session_unresolved: true` and the sweep settles it or drops the name.

**`event_occurred: false` is the retrospective kill, added 2026-09-18.** A sealed
baseline can be amended after its window passes to record that no release came, with the
source that establishes the absence in `event_occurred_note`. `edge_score.py` then marks
the name not rankable ahead of every other reason, because it is the only one settled by
the outcome rather than predicted before it. It does not touch the trade record. TRT on
2026-09-17 is the worked example.

**One issuer is one event, since 2026-09-16.** `researcher_us/scripts/share_class.py` folds a
second share class into its issuer in `edge_universe.py`, before a baseline is sealed,
and `edge_score.py` repeats the check on the scored rows — the folded name keeps its
hunt and its findings but leaves the ranking. On 2026-09-16 LEN and LEN.B were both
hunted and both ranked off one Lennar release, and the run log had to warn in prose
that `edge_resolve.py` would count one print as two events. Earlier runs are unchanged,
so a pooled sample that spans them still carries that pair twice.

**And the file itself is scored, since 2026-09-16.** The hunter sizes the day with the
baseline alone, freezes that draft as `pre_lessons`, reads `researcher_us/LESSONS.md`, then
revises; `edge_score.py` carries `diagnostics.impact_sum_pre_lessons` beside the key and
`edge_resolve.py` ranks both against the same realised move (`spearman_pre_lessons`).
The cost is that the file can no longer steer a search, only a size and a selection.
The gain is that guidance which costs rank correlation shows up within a few resolved
days. Nothing pools yet: until several days carry both numbers, a delta is one day's
noise. The note's
`tradable` column separates thin liquidity from Alpaca borrow (a short Alpaca will not
lend is usually borrowable at IBKR; `elsewhere`, not `no`), and it ends with a critical
read of every floor-clearer. None of this touches the key, the floor or the book rule.

Stage N and stage E overlap deliberately and must not be merged. N forecasts every name
it looks at; E scores whether the market has missed something. If E's ranking turns out
to carry no information that N's does not, that is a result worth having cheaply.

Stage C is not part of the daily advice pipeline and nothing downstream reads it. It
builds the forward corpus the backtest needs, and it is the only stage whose work cannot
be redone tomorrow — the day will have moved. See `archive/backtest/scripts/capture.py`.

**`edge/` was renamed to `researcher_us/` on 2026-09-18, and `edge` is now a symlink to
it.** The stage is "the US researcher" rather than "the edge hunt"; a second market is
intended to sit beside it as its own top-level directory. Three names did NOT change,
because the live Routine prompt hard-verifies them and **a session cannot edit that
prompt**: the skill is still `.claude/skills/earnings-edge-hunt/`, the four shims are
still `scripts/edge_score.py`, `scripts/edge_universe.py`, `scripts/priced_in.py` and
`scripts/alpaca_trade.py`, and the per-day output directory is still
`research/<YYYY>/<MM>/<DATE>/edge/`. Two constants are also deliberately untouched:
`CLIENT_PREFIX = "edge"` in `alpaca_trade.py`, which is the prefix of every
`client_order_id` this repo has ever sent to Alpaca and therefore identifies live
orders at the broker, and the `edge-scores.json` / `edge-note.md` filenames that ten
resolved runs already carry. The symlink is what keeps the prompt's `edge/…` references
resolving; **do not delete it until the prompt has been re-pasted** from
`researcher_us/routine-prompts/edge-hunt.md` with the new paths, and the Routine's
`updated_at` confirms the paste. This is the same failure that cost two live things on
2026-09-15 — the Routine prompt naming something the tree does not have — so the rename
was made non-breaking rather than complete.

**The scripts moved to `researcher_us/scripts/` on 2026-09-10, and four shims stayed behind.**
`scripts/edge_score.py`, `scripts/edge_universe.py`, `scripts/priced_in.py` and
`scripts/alpaca_trade.py` are three-line forwarders. They exist because the live Routine
prompt names those paths, *verifies two of them exist before doing anything else*, and
cannot be edited from a session — so removing them would have stopped the next unattended
run at step 0, before step 0b sold the previous day's book. Delete them once
`researcher_us/routine-prompts/edge-hunt.md` has been re-pasted with the `edge/` prefix. Import the
modules from `researcher_us/scripts`, never from the shims: they forward a command line and expose
nothing.

**A Routine prompt guards on an exit status, not on a config key it reads by eye.**
`python3 researcher_us/scripts/alpaca_trade.py mode --require <mode>` prints the effective
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
  of a point. `researcher_us/analysis/edge-exit-hourly.html`, hour 21.
- **The entry margin is gone.** Step 7 buys at market and `open` refuses to send into a
  closed market, so the run must finish before 16:00 ET. From 13:04 that is 2h56m. The
  2026-09-09 run took **2h53m end to end**. Three minutes. A day with more names, a
  retried subagent or a slow sweep misses the entry outright, and the note will still
  publish, so the failure is quiet. Either move the Routine back or make step 7 tolerate
  a closed market by queueing the next open; do not leave it at 17:04 and hope.

The prompt pasted in that Routine still tells the session it fires at "14:04 UTC, which is
16:04 Amsterdam and 10:04 New York". It also tells it to re-read the clock with `date -u`,
which is the only reason that is survivable. Fix it on the next paste.

It is enabled and it is the only pipeline Routine still running. It does **not** appear in `list_triggers` from this account, because it lives on another one — see the scoping note under the stage table before reading that absence as a fault. Its prompt cannot be
edited by a session —
`update_trigger` refuses any Routine an agent did not create — so the text lives in
`researcher_us/routine-prompts/edge-hunt.md` and was pasted in by hand on 2026-09-09 at 13:55 UTC;
keep that file in step with the Routine, because nothing else will. Since 2026-09-09 the prompt no longer restates the output contract: the
ranking key is whatever the skill and `edge-scores.json`'s own `ranking_key` field say,
because the old prompt named a key that a measurement then demoted.

**A second Routine now exists: "Close AMC", `trig_01MPuhVvtDgvUYzZXkKpHpKD`, created
2026-09-10 at 18:26 UTC and enabled.** It is the second exit Routine from
`researcher_us/routine-prompts/edge-execute.md`, and three things about it are worth knowing before
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
  `researcher_us/routine-prompts/`, because this Routine fires at 10:00 UTC — before any session
  can be asked about it.

**`exit_mode` moved off `uniform` on 2026-09-11, on the operator's explicit instruction,
replication risk knowingly accepted.** `config/pipeline.yaml` shipped
`exit_mode: auction_split` and `flatten_before_entry: false` from that day until
2026-09-15, when the same operator moved it again, to `amc_open`. Read this paragraph as
the history of the first move and the `amc_open` section above for what runs now; the
flatten has stayed off throughout. The requirement stated was
"amc is always run and closed by market open" — the two caveats above (unreplicated on
09-08/09-09, and `archive/backtest/RESULTS.md`'s 37 sealed events favoring the close for all three
arms) were read and set aside, not missed. Practically: the "Close AMC" Routine is no
longer a no-op, `mode --require auction_split` exited 0 until the 09-15 move
(`mode --require-exit-tif opg` is the guard that survives both), and stage E's own run must stop
flattening the book at the start of each session — `open`'s refusal to enter a new book
over an unsold, past-exit-date position is now the only thing keeping the account from
stacking books, so do not reintroduce `flatten_before_entry: true` without also reverting
`exit_mode`. The first book run under this config: 2026-09-11, closing 2026-09-10's amc
legs (FEIM, ORCL, RH) into that morning's opening auction; HOFT (bmo) deferred to stage
E's own closing-auction leg since `cls` is not accepted at 08:00 ET. If a future session
finds `exit_mode: uniform` again, that is a reversion someone made deliberately — check the
run log and this file's history before assuming it is stale, the same way the table above
must be checked against `list_triggers` rather than trusted by itself.

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

**Stage J is a second market, added 2026-09-18: `researcher_japan/`.** The same
hunt, the same hunter contract and — deliberately — the *same scorer*
(`researcher_us/scripts/edge_score.py`, unchanged), run over Tokyo. It exists to ask
whether the result stage E is chasing is a property of the method or a property of the
US market. **It places no orders.** There is no execution block, no broker call and
there must not be one; that is the one thing that separates it from stage E.

Korea was the original target and was rejected on measurement, not on taste. Querying
DART directly: Korean periodic filings arrive in four spikes a year of roughly 3,000
each (Nov 3,077 quarterly, Mar 2,880 annual, May 3,059, Aug 3,121) and the weeks between
carry almost nothing — 14–18 September 2026 had zero quarterly or semi-annual reports.
Korean issuers are near-universally December fiscal year-end, so they all report at once.
Korea also has no mandatory forward earnings-date notice (the 결산실적 예고 공시 is
explicitly voluntary), no liquid single-stock options, and KIND returns 403 here.
Japan's fiscal year-ends are staggered, so the flow never stops: counting 決算短信 on
TDnet, 456 on 2026-08-14 at the peak but still 79 on 09-11, 39 on 09-18 and 11 on 09-17
off-season. The quietest day sampled was half the US stage's daily universe.

**Three things about stage J that a reader will otherwise get wrong.** First, **the
missing option anchor is substituted, not merely disclosed.** Japan has no liquid
single-stock options, so until 2026-09-18 `priced_lean_pct` was `-0.05 *
run_up_20d_pct` — which is *also the free control every ranker is measured against*, so
the baseline's lean and its own benchmark were one number and `baseline_quality` was
capped at 0.40. `researcher_japan/scripts/jp_positioning.py` now supplies three
substitutes from what Tokyo does publish: JPX's daily disclosed short register (every
position at or above 0.5% of shares outstanding, so an absent name is a real zero), the
change in that register (shorts building or covering into the print), and 信用倍率, the
margin long/short ratio. Measured on the 2026-09-11 universe the lean's correlation with
the free control fell from **1.0 by construction to 0.446–0.59** and `baseline_quality`
rose from **0.40 to 0.725**. The weights are priors with no Japanese measurement behind
them, so `jp_resolve.py` ranks every component separately and reports
`lean_vs_free_control_rho` — if that climbs back to 1.0 the sources stopped resolving and
the lean is the run-up again. What is still absent: none of it says what the market
expects from *this* print, so `archive/backtest/FINDINGS.md` §33 (ρ=+0.073, p=0.45 over 104
events) is made testable, not refuted.

Second, the day is **cut at random**: microcaps go on median 20-day turnover (¥30m, the
same ~$200k/day the US run screens on), and if more than 25 survive a **date-seeded
random draw** picks them, because any other cut is a second ranking the scorer cannot
see — which is exactly what the double hunt turned out to be. Third, `history` is an
**estimated cadence**, not a record of announcement dates; TDnet keeps only ~31 days, so
prior dates are inferred by applying this quarter's notified lag backwards. It is a
scale. Reading a cadence prior as evidence is how TRT got ranked, traded and never
reported.

**The shared scorer gained two optional baseline keys on 2026-09-18, and US output is
byte-identical.** `edge_score.baseline_quality()` now reads `anchor_quality:
{magnitude, direction}` when a baseline supplies it, and `edge_score.priced_lean_pct()`
returns a baseline's own `priced_lean_pct` when it carries one. Both branches are
unreachable for a US baseline, which sets neither key. Verified by rescoring
`research/2026/09/2026-09-10/edge`: 17 rows compared, 0 changed.

**Stage J's Routine can be edited from a session, and one thing about it is still
unverified.** `trig_0192kQeqhumBKpNGzzyQrS1H` was created by a session, so
`update_trigger` works on it — its prompt was rewritten on 2026-09-18 at 17:38 UTC and
its `updated_at` moved. That is the one thing stage E's Routine cannot do, so keep
`researcher_japan/routine-prompts/japan-hunt.md` in step with it from a session rather
than by hand. **What is NOT verified**: it came back with empty `sources`, `outcomes`
and `allowed_tools`, unlike the pipeline Routines which all carry a populated repository
source and tool list. Its prompt clones the repo itself at step 0, so this may be
harmless, but that path needs `add_repo` and `register_repo_root`, and `update_trigger`
cannot set those three fields. Fire it once by hand and read the result, or recreate it
from the Routines UI, before believing a quiet morning.

**Tokyo closes more often than the cron does.** 2026-09-21, 09-22 and 09-23 are
敬老の日, a 国民の休日 and 秋分の日, so the first three scheduled fires after this was
built all land on a shut exchange. `jp_universe.py` reads the Cabinet Office's own
国民の祝日 list and writes `market_closed` into the universe file, because an empty
calendar otherwise has two causes that look identical and mean opposite things: the
exchange is shut (nothing to wait for) or the fiscal cohort's sheet is not up yet.

**The stage was run end to end with real hunters on 2026-09-18**, over the first two
Tokyo sessions that have scheduled prints: 09-24 4716 日本オラクル `impact_sum` −3.50
(above the floor), 09-25 2742 ハローズ −3.90 (above) and 3333 あさひ −2.50 (below).
`baseline_quality` read 0.725 on all three. 3333's `pre_lessons` sum (−3.0) differs from
its key (−2.5), so the lessons control is live and measurable. Three defects came out of
that run and all three are fixed: **`WebFetch` returns HTTP 403 where `curl` returns 200
on the same URL** — verified on kabutan and on TDnet's list and its 月次 PDFs, which are
the highest-value Japanese series — so `unpriced-hunter-jp` carries `Bash` and documents
the fallback; **the 20-day run-up hid the move that mattered** (4716 read −0.42% over 20
days against +4.38% over five, on a US-parent read-through), so `run_up_5d_pct` is sealed
and `jp_resolve.py` ranks it as its own free control, deliberately NOT folded into
`priced_lean_pct`; and the holiday handling above.

Nothing has resolved in Japan. The stack was validated end to end on 2026-09-18 against
2026-09-11 (76 scheduled, 34 eligible, 25 drawn, 24 of 25 confirmed on TDnet, one
correctly killed as `event_occurred: false`, median realised move 2.87%) using
*synthetic* findings, which ranked at ρ=0.154, p=0.47 — what random findings should do.
See `researcher_japan/README.md`.

**Stage AU is a fourth market, added 2026-09-22: `researcher_australia/`.** The same
hunt, the same hunter contract and the same scorer
(`researcher_us/scripts/edge_score.py`, unchanged: a US run rescores identically because
nothing was touched), run over the ASX. **It places no orders.** Alpaca does not carry
the ASX and execution would be a separate build against a different broker.

**IT WAS CHOSEN FOR ITS ANCHOR, NOT ITS CALENDAR, AND CANADA HAS THE BETTER CALENDAR.**
Annualised by cadence above the $200k floor on the same vendor instrument stage EU uses:
Canada 6.89 events a trading day (median gap 93 days, 62% quarterly), the UK leg 5.01,
**Australia 3.08** (median gap 187 days, 0.5% quarterly). Canada was declined on
reachability, which is the axis this repo keeps paying for: `sedarplus.ca` answered **0
of 4** and `ciro.ca` **0 of 7**, both behind bot protection, so Canada today is Spain and
Poland from stage EU — no positioning anchor and no way to reach `event_occurred: false`.
EDGAR does not rescue it for the band this stage targets: only 166 of 456 eligible
Canadian names match an EDGAR ticker, and that 36% is an **upper bound** because bare
tickers collide with US issuers; by band it is 31% at $0.2–1m and 26% at $1–5m against
59% above $25m.

**ASIC'S REGISTER IS A DIFFERENT CLASS OF OBJECT FROM EVERY OTHER ONE IN THIS REPO.** The
FCA, JPX, the Bundesanzeiger and the AMF all publish positions at or above a 0.5%
disclosure threshold. ASIC publishes the **aggregate for every product**: on the
2026-09-16 file, 755 products, minimum 0.000000%, median 0.309%, maximum 17.30%, and
**430 of 755 rows below 0.5%**. So the level is real at every size, there are no
truncated zeros and no `anchor_covered` arm, and the change moves when the position moves
rather than when a holder crosses a line. Its index carries **4,113 dated files back to
2010-06-16**, which makes it the only positioning anchor here that can be BACKTESTED over
a long history — and that test needs no stage at all. What it costs is the lag: ASIC
publishes about four business days in arrears, carried as `positioning.lag_sessions` and
never to be treated as zero.

**AND THE LEAN THIS BUILD SHIPS WITH IS WORSE THAN TOKYO'S, WHICH IS STATED RATHER THAN
FIXED.** On the 2026-08-27 validation run `lean_vs_free_control_rho` read **0.80 over 20
names** against stage J's healthy 0.446–0.59: the lean is `short_squeeze` +
`short_building` + `runup`, and the run-up term dominates whenever short interest is
small, which on an untruncated register is most names. So Australia's lean is more
entangled with its own benchmark than Tokyo's. The weights are Tokyo's priors with no
Australian measurement behind them and they were deliberately NOT re-tuned — a constant
that moves with the data is not a hypothesis, which is why `w1` is frozen. `au_resolve.py`
ranks every component separately so measurement can replace them. This is the first thing
a resolved Australian run should settle.

**Three more things a reader will otherwise get wrong.** First, **the vendor's date is
one day early for 85% of Australian rows** — Sydney is UTC+10 or +11 and the vendor
stamps the UTC instant, so BHP's 08:31 Appendix 4E on 18 August reads as 17 August.
`au_market.sydney_event_date()` converts the instant rather than adding a constant, so it
survives the 2026-10-04 daylight-saving change, and every row carries `event_date_basis`.
Getting it wrong does not throw; it seals on the wrong evening and hunts a name whose
print was yesterday. Second, **Australia reports before the open harder than Europe
does** — 67 of 74 measured results announcements (91%) landed before the 10:00 Sydney
open against the UK's 89.4% — so the window is `close(D−1) → close(D)`, the baseline is
sealed the evening before, and **the Routine's cron is Sunday to Thursday**, because the
fire that seals for Monday has to happen on Sunday. Third, **half the ASX lodges a
cash-flow report and not a profit result**: an Appendix 4C or 5B quarterly activities
report under Listing Rule 4.7B is a real, market-moving event (IperionX's eleven observed
ones carry a median absolute reaction of 4.66%) with a completely different bar, so
`history.filer_type` carries which, and `au_resolve.py` reports `by_filer_type` so a
pooled number cannot hide the mix.

**What is BETTER here than in Tokyo: the reaction history is observed.** The ASX
per-issuer announcement archive is queryable by year and goes back years, so prior prints
carry real dates and real timestamps and may be cited as facts — where stage J applies
this quarter's lag backwards and labels every row `estimated`. Three classifier defects
came out of building it and all three are fixed, each having scored a non-event as a
reaction: a "Results Release Date" notice (Myer, −3.53%), two "Details" notices of
presentation arrangements (TUA), and an S&P index rebalance (−4.88%). That is the Oslo
defect stage EU already measured, where "Invitation to Q4 results" counted as a print for
12 of Nordic Semiconductor's 25 rows.

**ONE ENGLISH HUNTING PASS, AND NO `pre_local` FREEZE (operator's instruction).** Stages
EU and J freeze an English draft and then run a local-language or domestic-source pass.
Australia runs one pass. There is no Australian-language press the wires do not read, and
stage EU already carries the degenerate case: its UK hunter varies *source locality*
instead of language, `eu_resolve.py` **refuses to pool** its delta with the German and
French ones, and its own definition says a UK zero is not evidence about language. A
second Australian pass would spend tokens measuring a variable that does not exist and
would emit a structurally zero delta somebody would later pool as if it were one.
`unpriced-hunter-au` has no `pre_local` field, `australia_hunt.language_pass` is `false`,
and `smoke_test.py` asserts the field does not come back. The `pre_lessons` control still
runs and `researcher_australia/LESSONS.md` is deliberately empty until a run resolves.

**What no new market fixes: the option anchor.** Measured 2026-09-22 on the repo's own
authenticated Yahoo path, AAPL returns 22 expiries, TSM 19 and ITUB 8, while `BHP.AX`,
`CBA.AX`, `SHOP.TO`, `0700.HK`, `7203.T`, `NESN.SW` and `RELIANCE.NS` all return **zero**.
So stage AU runs anchor-less exactly like stages J and EU — the regime
`archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events. There are
now three unresolved anchor-less stages and zero resolved days outside the US, and that
belongs in any argument for a fifth market.

Nothing has resolved in Australia. The stack was validated end to end on 2026-09-22
against 2026-08-27 (67 scheduled, 37 eligible, 20 drawn at the cap, 19 of 20 confirmed
against the ASX record and one correctly left `announced_unclassified`) using *synthetic*
findings, which ranked at ρ=0.215, p=0.36 — what random findings should do. On that same
day the free control `-run_up_20d_pct` ranked at **ρ=−0.508, p=0.025**, which is the
opposite sign to the US sample; one day is not a result and it is recorded because it is
the kind of thing that gets remembered wrongly. See `researcher_australia/README.md` and
`researcher_australia/SUBMARKET.md`.

**Stage EU is a third market, added 2026-09-18: `researcher_europe/`.** Ten European
markets pooled into one stage, on the same scorer again
(`researcher_us/scripts/edge_score.py`). **It places no orders.** Alpaca carries none of
these venues, so execution would be a separate build against a different broker.

**SEVEN MARKETS WERE ADDED ON 2026-09-19 AND THE CAP WENT FROM 12 TO 20**, on the
operator's instruction: Stockholm, Copenhagen, Oslo, Helsinki, Milan, Madrid and Warsaw,
on the same $200k floor and the same scorer. **The obvious measurement says they add
nothing and it is measuring the wrong window.** Over the ten sessions 2026-09-21 → 10-02
they add SIX names to a pooled median of seven a day, because late September is the UK's
month. By month of forward vendor events, **October is the existing stage's thinnest at
114 for UK+DE+FR and the new seven carry 456**; November is 309 against 515; February and
March are barely touched. Sweden alone carries 259 October events. And the cadence is
better — measured median gaps of 91–98 days across the Nordics and Poland against the
UK's 217 and France's 204 — so a Nordic name recurs four times a year where a UK one
recurs twice.

**THEY ARE NOT EQUALLY INSTRUMENTED AND THAT IS THE PART TO CARRY INTO ANY POOLED
NUMBER.** `researcher_europe/scripts/eu_market.py`'s `CAPABILITY` is the measured table
and the code reads it rather than assuming. Norway is now the best-instrumented market in
this stage after the UK — a dated short-position event history, a true ticker-keyed day
archive, and the only other market whose `history` carries OBSERVED announcement dates
rather than a cadence estimate. Sweden, Denmark and Finland have registers and a day
archive, but the Nasdaq Nordic feed **has no date query at all** — its `fromDate` is
accepted and ignored — so it is paged back about twelve days and `event_occurred: false`
is reachable only inside that window: **resolve a Nordic run within about a week**. Italy
has both, behind a WAF that answers about 7 of 8. **Spain and Poland have NEITHER a short
register NOR a day archive**, so those names carry no positioning anchor — their
`priced_lean_pct` IS the free control every ranker is measured against, so they cannot
beat the benchmark with anything that uses it — and their prints can never be confirmed
or killed. Both were given the eight-try standard that rescued France and Italy and
failed it (`gpw.pl` and `espi.pap.pl` scored 0 of 8 on the sweep where emarketstorage
scored 7 of 8). A pooled ρ that does not say how much of it is `es`/`pl` is being
oversold.

**Five defects were found building it and all five are fixed; two would have failed
silently.** YAML parsed unquoted `no` as boolean False, which dropped Norway from the
configured market list without an error — the smoke test now asserts it. Nordic share
classes are `OMXSTO:INVE_A` on the vendor and `INVE-A.ST` on Yahoo, and a wrong symbol
returns an empty chart rather than an error, so the day would quietly have lost its
largest Nordic names. Norway's observed history counted "Invitation to Q4 results" as a
print — 12 of Nordic Semiconductor's 25 rows, each a week before the real event, halving
the measured reaction scale. Sweden's ODS was read as a dated history and is a per-issuer
snapshot, so the change came out equal to the level for all 342 names. And eMarket
STORAGE's `data_to` is EXCLUSIVE, so a naive single-day query returns zero rows and looks
exactly like a silent day.

**The draw is random and the calendar is seasonal, so a day can be one market.** 15 of 20
names were Swedish on 2026-10-22. That is a correlated exposure the scorer cannot see —
the same shape as the four US names the IEEPA tariff refunds ranked together on
2026-09-10. The draw is deliberately NOT stratified, because a per-market quota is a
second selection and this stage has already paid once for a cut the scorer could not see;
`selection.market_concentration` in the universe file carries it instead, and the note
must report it.

**`researcher_europe/scripts/eu_sheet.py` is new**: ODS and XLSX with the standard
library, because Sweden's and Italy's registers are spreadsheets and this container has
no `openpyxl`, no `odfpy` and no `pandas` — the same constraint that produced
`eu_pdftext.py`.

**The Routine's prompt was re-pasted from a session on 2026-09-19 at 13:25 UTC** and its
`updated_at` confirms it. It now names all ten markets, the cap of 20 and the seven
hunters including `unpriced-hunter-nordic`, and it carries the per-market resolve
deadline. It was renamed to "Stage EU — Europe researcher (10 markets)". **Unlike stage
E's, this Routine CAN be edited from a session**, so
`researcher_europe/routine-prompts/europe-hunt.md` and the Routine must move in the same
commit — that file now carries the pasted text verbatim.

**And that call corrected a claim this file and the prompt file both carried.** Stage
EU's Routine does NOT have empty `sources`, `outcomes` and `allowed_tools` any more: the
update response returns a populated `session_request.config` with a `git_repository`
source for this repo, a full `allowed_tools` preset, and an **`outcomes` branch of
`claude/pensive-sagan`**. So a fired session does get a checkout.

**THE OUTCOME BRANCH CANNOT BE CHANGED FROM A SESSION, AND THE PROMPT NOW PINS THE
DESTINATION INSTEAD (2026-09-21).** `update_trigger` takes only `name`,
`cron_expression`, `enabled`, `model`, `prompt` and `run_once_at` — there is no field for
`sources` or `outcomes`, and `create_trigger` has none either, so
`outcomes: claude/pensive-sagan` is settable **only from the Routines UI**. Changing it
there is the operator's job and it is the one loose end left on this stage.

What was done instead is the part that actually decides where the day's research lands:
the prompt re-pasted at 06:46 UTC **exports `EARNINGS_DATA_BRANCH=main` explicitly**
before calling `publish.sh`, and then runs `git fetch origin main && git log --oneline -1
origin/main` and requires the run to say in its reply if its own commit is not there.
`publish.sh` performs a real `git push` to that branch, which is a different mechanism
from the harness's `outcomes` metadata — so pinning the variable makes the data
destination deterministic whatever the outcome field says, and the verification line
makes a wrong destination visible instead of silent. **That is belt-and-braces, not a
fix**: until somebody clears the `outcomes` branch in the UI, the two still disagree on
paper, and the first fire under this prompt is the observation that settles it.

**Its Routine exists since 2026-09-19: `trig_018WGfdq2fUm1ZqJhCGQ1wde`, cron
`30 13 * * 1-5`.** Created by a session, so `update_trigger` works on it, and
`researcher_europe/routine-prompts/europe-hunt.md` must be changed in the same commit as
any re-paste. It came back with empty `sources`, `outcomes` and `allowed_tools` exactly as
stage J's did. **The hand-fire meant to settle whether a fired session gets a checkout did
not settle it**: session `cse_01GPAvkwHzwzxuWdsscSUPUN`, 2026-09-19 08:24 UTC, spent 165k
tokens over ten minutes and **published nothing at all** — no commit, no branch, no run
directory on any remote — and its transcript cannot be read from another session. So the
prompt was rewritten at 08:39 UTC to stop depending on the answer: step 0 clones the repo
when `CLAUDE.md` is absent and distinguishes "no repo" from "branch not merged", and every
fire must now publish something, even an empty day or a failure, because a fire that
publishes nothing is indistinguishable from a Routine that never fired. It served on
`claude-sonnet-5` while the `europe_hunt` block asks for `model: opus`; the config governs
the hunters it spawns, the Routine's model governs the session that orchestrates them, and
whether that matters is unmeasured.

**It fires two hours before the European close, not after it, on the operator's
instruction.** The obvious slot is after the 17:30 CET closes so every `close(D-1)` is
final. 13:30 UTC is 15:30 Amsterdam in summer and 14:30 in winter, while the markets are
still trading. This does **not** corrupt the measurement, because `eu_resolve.py` takes the
realised move from daily bars and never from the sealed spot; it does mean the sealed spot
and `run_up_20d_pct` are intraday prices, struck at the same instant as the free control
they are measured against. Never call the sealed spot a close. The cron is UTC and the
exchanges are not, so the gap widens to three hours after the October change.

**Pooling is not a convenience, it is the only thing that makes the stage possible.**
Each market fails the stream test alone and each fails it differently: Germany's Prime
Standard quarterly statement under §63 BörsO is real (156 of 259 names quarterly, median
gap 97 days) but **synchronised** — 153 of 259 forward events land in November and one in
June, which is the Korea failure mode in milder form. France is thinner still (17 of 161
quarterly) and 94 of 161 events fall in February–March. **The UK is the staggered one**,
with every month carrying a non-trivial count, which is the December/March/June/September
year-end spread Korea and China lack entirely — but above a $1m/day floor the UK alone
runs a median of 4 names and bottoms out at 1 on Fridays. They peak in different months,
so pooled the day clears the Japan bar on a median day and **not on every day**: August,
late December, Fridays and the German June–July gap still give two- and three-name days.

**The option anchor was expected to be Europe's advantage over Tokyo and it is not
there.** No European single-stock chain proved retrievable free from this container:
Yahoo returns 21 expiries for AAPL and **zero** for SAP.DE, MC.PA, BARC.L and BNP.PA;
Eurex's daily zip downloads but carries trading parameters only, no settlement prices, no
open interest, no underlying map. The coverage fraction could not be measured because the
coverage could not be reached. **So Europe runs anchor-less exactly like Japan** — the
regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.

**What Europe does have, and Tokyo does not, is a short register worth using — and
since 2026-09-19 all three markets' registers read.** The FCA publishes current
aggregated net short positions as a plain CSV *and* the full per-holder history back to
2012, so a European positioning anchor can be **backtested**, which JPX's cannot.
Coverage of the UK results cohort is 89% in the $1–5m turnover band against Japan's 9–11
of 25 names. Germany resolves through the Bundesanzeiger with a session cookie.

**France was the unsolved leg and the diagnosis that closed it was wrong.** Phase 1
tried `www.data.gouv.fr` four times, got four connection resets and wrote the host off
as unreachable. Re-tested eighteen times it answers **roughly one request in three** —
the failure is a TLS exchange that dies after 7s, indistinguishable from a block and not
one, and a tight retry loop scores 0 of 12 where a 2–4s backoff scores about 1 in 3. So
`eu_positioning.load_fr()` takes two retried hops: the dataset endpoint for the
resource's current URL (the filename carries an export timestamp and changes daily),
then the CSV off `object-api.infra.data.gouv.fr`, which has never failed here. **5.1 MB,
40,696 per-holder rows back to 2012, 74 issuers with an open position** (Ubisoft 12.56%
across 11 sellers, Valeo 10.69%, Renault 9.59%). Its publication **end** dates let the
aggregate be reconstructed as of any past date, so the French change is measured rather
than approximated and the anchor is backtestable — better instrumented than Germany's
current-only snapshot. A register that fails on the day is served from cache for up to
five days with `stale_cache_days` set. What is still true: the French financial press
(Les Echos, Investir, Boursier, Zonebourse, actusnews) is shut to both `curl` and
`WebFetch`, so France remains the thinnest leg on sources, and it carries 74 disclosed
issuers against 419 UK and 124 German.

**The Japan `curl`-beats-`WebFetch` finding does not generalise.** On this path the two
mostly agree; what differs is paywalls, not the fetcher. Each hunter definition carries
its own measured reachability table rather than inheriting Japan's.

**Europe reports before the open, which no other stage does.** 339 of 379 UK results
announcements landed before 08:00 London (89.4%), so the window is
`close(D−1) → close(D)` and **the baseline must be sealed the evening before**. Getting
this wrong is not cosmetic: Barratt Redrow moved +11.72% over the correct window and
+1.78% over the one a US-shaped stage would have used.

**The calendar is far cleaner than the US one.** Measured against four full weeks of the
RNS record via Investegate — a full mirror queryable by date back to 1999, where TDnet
keeps about 31 days — TradingView's forward rows show a **2.2% phantom rate** (88 of 90
UK rows had a same-day results RNS from the same issuer) against the US
`time-not-supplied` rate of 20 of 20. Six of the eight apparent misses were a headline
classifier, not a missing print.

**Germany and France have day archives too, since 2026-09-19 (`eu_archive.py`), and
Phase 1 was wrong about both.** France is `info-financiere.gouv.fr`, the AMF's own
regulated-information flux: an Opendatasoft API, no key, **536,868 records back to
2012**, current to yesterday, 42–152 filings a day, queryable by date. It is the only
one of the three that carries **the issuer's own declared filing category**, which is the
one real fix for the Trustpilot failure mode — a French results release is often filed as
*Informations privilégiées / Communiqué sur comptes, résultats*, which a headline
classifier reads as nothing; over twenty sampled days 78 of 178 results rows classify by
category and 100 by headline. Germany is the EQS-News **search** — `/search-results/`,
paginated at `/page/<n>/`, 67 pages for one mid-cap — not the front page Phase 1 measured
and wrote off as same-day-only. Two German catches: EQS has **no whole-day query**, so
the German archive is assembled per issuer and `event_occurred: false` is unreachable
there by construction; and `searchword=HORNBACH Holding AG & Co. KGaA` returns **zero**
rows where `HORNBACH` returns 25, because the search ANDs over words.

**What the archives changed about the measured stream: France is 3.6× the vendor,
Germany is 0.78×.** Unfiltered, one issuer counted once a day, on the week where the
vendor's last-release field is current: UK 23.4 measured against 13.6 vendor rows a day
(1.7×), **France 10.0 against 2.8**, Germany 1.6 against 0.6 on single digits — and in
Germany's August peak week **10.8 measured against 13.8 vendor rows**. So the UK's 2.2×
undercount generalises to France and not to Germany; France's contribution to the pooled
stream is materially larger than `SUBMARKET.md` claimed, and the thin German months are
seasonality, not a bad feed. Phantom rates against the archives: UK 2 of 90, **France 1
of 17** (plus one vendor date off by a day), Germany **not measurable** — three of six
rows returned nothing from a per-issuer search, which is not a phantom.

**Yahoo's European daily closes lag, so a European run cannot be resolved the morning
after the print.** Measured 2026-09-19: `.PA` and `.DE` carried timestamps for 09-17 and
09-18 with **null closes**, on liquid names as well as thin ones, `.L` one session
behind. `eu_resolve.py` carries `last_bar_date` and `move_pending` per row and warns when
every row is pending.

**The size band contradicts the obvious prior and the universe is deliberately NOT cut to
it.** Analyst coverage runs 1–2.5 names below $1m/day, 5–7 at $1–5m, 11–13 at $5–25m and
16–19.5 above — so MDAX/SDAX, SBF 120 ex-CAC 40 and FTSE 250 sit in the *well-covered*
band and the genuinely under-read one is $1–5m, a band lower than "mid cap" would suggest.
Selecting the universe on the thesis would make the thesis unfalsifiable, so the stage
takes a turnover floor then a seeded random draw, carries `analyst_band` in every
baseline, and `eu_resolve.py` ranks the hunt **by band**. Let the measurement find the
band.

**The floor moved from $1m to $200k on 2026-09-19, on the operator's instruction, and
the cost is now carried in the data.** The reason given: $200k is what stages E and J
screen on, so all three markets are cut the same way and their resolved numbers are
comparable, and it adds names on exactly the thin days. Measured forward over ten
sessions (2026-09-21 → 10-02, live vendor calendar and live tape) it is **not
cosmetic**: the pooled day goes from a median 2.5 names to **6.5** and a mean 2.8 to
6.1, 28 names to 61 over the ten days, with France going from a median of zero a day to
one. What it costs is the anchor — in the UK the short register names **80% of the names
above $1m and 32% of the names the new floor adds** (16/20 against 8/25), which is less
bad than Phase 1's "12% below $1m" suggested because that figure pooled the $200k–$1m
band with everything under it. So every baseline now seals **`anchor_covered`** (true
only where the register names that issuer; a truncated zero and an unreadable register
are both false, kept apart by `anchor_coverage.state`), `anchor_quality.direction` pays
a truncated zero 0.15 where a disclosure earns 0.45, and `eu_resolve.py` reports
**`by_anchor_covered`** — Spearman, sign rate and count in each arm. If the half this
floor bought ranks at zero, a fortnight of pooled days says so rather than nobody ever
finding out.

**Each hunter runs English first, then local, and the order is load-bearing.** The
English pass is frozen as `pre_local` before the local-language pass revises it, so
`diagnostics.impact_sum_pre_local` and `spearman_pre_local` measure whether searching in
German and French earns rank correlation or only costs tokens — the same control shape as
`pre_lessons`, which still runs after it. **The UK case is degenerate and is labelled as
such**: its second pass varies *source locality* (RNS, Investegate, the domestic trade
press), not language, so `eu_resolve.py` **refuses to pool** the UK delta with the German
and French ones. A UK zero is not evidence about language.

**The shared scorer gained 42 lines and moved nothing.** Verified by rescoring all five
live US runs (09-14 through 09-18) with the pre-stage-EU scorer and the current one: every
ranked row identical, rank, `impact_sum`, `conviction` and `priced_lean_pct` alike.

Nothing has resolved in Europe. The stack was validated end to end on 2026-09-18 against
2026-09-16 (22 vendor rows, 4 eligible above $1m, 4 of 4 confirmed by a real results RNS
out of the 40 EPICs filing that day, short register 4 of 4, UK
`lean_vs_free_control_rho` 0.40) using **synthetic findings**, which ranked at ρ=−0.80,
p=0.33 on four names — noise by construction. Spread is entirely unmeasured, and it is
the cost that would matter most in the band this stage targets.

**A German and a French name went through with real research on 2026-09-19, for the
2026-09-23 session** (`research/2026/09/2026-09-23/europe/`): KWS SAAT `impact_sum`
−2.10 and Quadient +0.90, neither above the conviction floor. Quadient at $0.51m/day
of turnover is a name the old $1m floor would have excluded, so the French leg exists
because the floor moved. Both were confirmed against the **issuer's own calendar** —
KWS's Finanzkalender (23 September 07:00 CEST) and Quadient's (23 September, after
close) — and both hunts held their emitted number inside the sum of their findings.
What the run establishes and what it does not: the chain runs end to end for DE and FR
(universe → share-class fold → `anchor_covered` baseline with all three registers
reading → hunt with a real `pre_local` freeze → `edge_score.py` → `eu_resolve.py` →
note), and **it is not a ranking** — the session could not spawn subagents, so the seven
UK names were left unhunted, a shed recorded in the run log, and two names cannot be
ranked against each other. **`pre_lessons` in both hunts is not a measurement**: one
context ran both hunts and had read `LESSONS.md` first, so the freeze is equal to the
emitted set by construction. `impact_sum_pre_local` is a real freeze and a two-name
delta is still noise.

**Three defects came out of that run and all three are fixed.** `eu_resolve.py` would
have **killed names that had not reported yet** — resolving a forward run read the day
archives for a date that has not happened, found nothing from the issuer and wrote
`event_occurred: false`, the mirror image of the TRT mistake; it now refuses to confirm
a future date. `eu_positioning.load()` re-fetched every register on every invocation,
which with France's intermittent host meant **twelve minutes before a single baseline
was sealed**; today's file is now read from the cache unless `--refresh` is passed. And
**no PDF could be read in this container at all** — no `pdftotext`, `pdfminer` and
`pypdf` both dead on a broken `cryptography` module, `WebFetch` returning "garbled
binary data" — which matters because the AMF flux links every French filing as a PDF;
`researcher_europe/scripts/eu_pdftext.py` reads them with the standard library, and it
is what turned Quadient's 5%-threshold declaration from a search snippet into a
quotable primary document.
See `researcher_europe/README.md` and `researcher_europe/SUBMARKET.md`.

**The five stage 0–4 pipeline Routines were disabled on 2026-09-18** at the operator's
request, and the stage table's claim that they "do not currently exist" was wrong before
that: all six were enabled and firing. They are disabled now, not deleted. Stage E is
untouched and still runs.

**One folder per experiment, since 2026-09-10.** `edge/` is stage E, `archive/backtest/` is the
sealed backtest, `archive/claude_naive/` is stage N. `scripts/` holds only what the pipeline
stages share, plus four forwarding shims described below. Nothing about an experiment
lives in `docs/` any more; `docs/ROUTINES.md` is all that is left there, because it covers
every Routine rather than one stage.

```
researcher_us/                         stage E — see researcher_us/README.md
  EDGE_ANALYSIS.md  EXECUTION.md       what the runs establish; the Alpaca contract
  scripts/                             the stage's own tools
  analysis/                            everything those tools generate
  routine-prompts/                     the text pasted into the Routines, by hand
dashboard/                             the standing performance record and the one
  update.sh  scripts/  data/  LOG.md   reading surface — see dashboard/README.md
  dashboard.html                       open it from disk; rebuilt by update.sh
  scripts/build_markets.py             stage EU/J/AU into data/markets.json, for the
                                       Europa, Japan and Australië tabs
.github/workflows/dashboard.yml        the same rebuild in CI + GitHub Pages, for the
                                       copy that is fetched rather than opened
edge -> researcher_us                  SYMLINK. The live Routine prompt names edge/
                                       paths and cannot be edited from a session.
researcher_japan/                      stage J — see researcher_japan/README.md
  scripts/                             jp_universe, jp_positioning, jp_priced_in,
                                       jp_resolve
  routine-prompts/                     the text in the stage J Routine
  LESSONS.md                           deliberately empty until a run resolves
researcher_australia/                  stage AU — see researcher_australia/README.md
  scripts/                             au_market (the Sydney date shift, the trading
                                       calendar, the three headline classifiers),
                                       au_positioning, au_priced_in, au_resolve
  SUBMARKET.md                         why Australia and not Canada, with the counts
  routine-prompts/                     the text in the stage AU Routine
  LESSONS.md                           deliberately empty until a run resolves
researcher_europe/                     stage EU — see researcher_europe/README.md
  scripts/                             eu_market (incl. CAPABILITY), eu_universe,
                                       eu_positioning, eu_priced_in, eu_archive,
                                       eu_resolve, eu_sheet, eu_pdftext
  SUBMARKET.md                         why these markets pooled, with the counts behind
                                       it; section 10 is the 2026-09-19 expansion
  routine-prompts/                     the text in the stage EU Routine
archive/                               retired 2026-09-18 — see archive/README.md
  backtest/                            the sealed backtest, arms A/B/C + edge-corpus
  claude_naive/                        stage N, disabled 2026-09-09
  pipeline/<YYYY>/<MM>/<date>/         stages 1-4's output, day by day
  pipeline/LEDGER.md PREDICTIONS.*     the forecast ledger and the flat prediction table
scripts/                               shared: run_paths, publish, run_log, get_earnings,
                                       build_predictions, update_index, validate_stage,
                                       synthesize, smoke_test — and four shims
config/pipeline.yaml                   one config for all of it
.claude/{agents,skills}/               where the harness looks; cannot move

research/<YYYY>/<MM>/<YYYY-MM-DD>/
  00-universe.json  00-universe.md      stage 0 — still written every day
  edge/                                 stage E's run for that day
  _run-log.md                           appended by every stage
  01-* 02-* 03-panel/ 04-* 05-*         stages 1-4, MOVED to archive/pipeline/ on
                                        2026-09-18. Do not write them again.
INDEX.md         rolling archive index (generated — never hand-edit)
```

`archive/pipeline/PREDICTIONS.csv` is the file to open when the question is "what did the
retired pipeline call, and what happened". It joins the triage scores, the dossier's
preliminary read, the panel synthesis and the realised outcome into one flat table.
`scripts/build_predictions.py` still builds it from `research/`, which now holds none of
those files, so it would write an empty table over a frozen one. Leave it alone.

Never invent a path. Always resolve with:

```bash
python3 scripts/run_paths.py --json
```

## Rules that apply to every stage

**`scripts/publish.sh` pushes to `main`, not to your branch.** `BRANCH="${EARNINGS_DATA_BRANCH:-main}"`
is deliberate: a Routine session's job is to put the day's research on the data branch, and
every stage's closing step depends on it. It is a trap for a *development* session working
on a feature branch, which will push its work-in-progress to `main` without meaning to —
that happened on 2026-09-19 and put three of stage EU's four tasks on `main` unreviewed
(harmlessly: `main` stayed a strict ancestor of the branch and nothing outside
`researcher_europe/`, the three Europe hunters, the Europe skill and the `europe_hunt`
config block was touched, so the live stage E was unaffected). If you are building rather
than running a stage, use plain `git commit` and `git push origin <your branch>`, or set
`EARNINGS_DATA_BRANCH` first. Do not change the default; the Routines depend on it.

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
