# dashboard — what the hunt is actually worth

Stage E produces a number per company. This folder is the only place that asks,
systematically and over every day at once, whether that number is worth anything —
and what the account did with it.

Nothing here runs a hunt, scores a finding or places an order. It reads.

Top level on purpose: `dashboard/dashboard.html` is the file to open, and it opens
straight off the disk with no server and no network.

```
dashboard/
  update.sh                 the button: rebuild everything, optionally publish
  ../.github/workflows/dashboard.yml   the same rebuild, in CI, for the fetched copy
  scripts/build_ledger.py   collect runs + broker + prices -> data/ledger.json
  scripts/build_dashboard.py render data/ledger.json -> dashboard.html
  data/ledger.json          the whole dataset, one file
  data/names.csv            one row per ranked name per run
  data/trades.csv           one row per position the account opened
  data/sectors.json         sector and industry per ticker (cached, Yahoo)
  data/assets.json          shortability per ticker (cached, Alpaca)
  data/costs.csv            measured tokens per run, if you have them — else a proxy
  scripts/serve.py          localhost server that makes the page's refresh button real
  dashboard.html            open it from disk; no server, no network, no CDN
  LOG.md                    what each update changed, and what it now reads
```

## Three levels, and they are not the same thing

| level | what it is | where it comes from |
| --- | --- | --- |
| **names** | every rankable name of every run, priced at eight exit horizons **and at every half hour of the entry session** | `edge-scores.json` + `baselines/` + Yahoo bars |
| **trades** | every position the account opened and closed, matched from the fill stream | Alpaca `/v2/account/activities/FILL` |
| **account** | the equity curve as the broker reports it | Alpaca portfolio history |

A fourth thing sits beside those three and is not one of them: the **markets** level in
`data/markets.json`, the research record of stage EU, J and AU. Those stages place no
orders, so it has names and no trades and no equity curve. See "The other three markets"
below.

A name is not a trade. The conviction floor, the $200k turnover floor and the
borrow check mean most ranked names are never traded, and the two strongest
convictions of 2026-09-10 were all three untradable. A traded name can also be
closed by hand at a price no horizon knows about — six of the nine closed
positions were. Every figure in the dashboard says which level it came from, and
mixing them is how you get a number that flatters the stage.

## Running it

```bash
./dashboard/update.sh            # broker + re-price + render
./dashboard/update.sh --offline  # no broker call, keep the last broker state
./dashboard/update.sh --publish  # and commit + push
./dashboard/update.sh --fresh    # drop the bar cache, re-price everything
./dashboard/update.sh --serve    # and serve it, so the page's own button works
```

**The refresh button in the page, including from a file.** A `file://` page may not run
a script — a browser rule, not a setting — but it may talk to a server that is already
running, and `serve.py` answers one on purpose. Run `--serve-bg` once and you get your
shell back; every copy of the page, served or opened off the disk, probes
`127.0.0.1:8765` on load, shows **live** beside the button when it answers, and a click
then rebuilds the ledger and rewrites `dashboard.html` on disk, which the reload picks
up.

**And when the page is FETCHED rather than opened, the button starts a GitHub Action.**
A page on the web has no machine of yours to build on: it cannot run a script and it
cannot reach `127.0.0.1` — an https page is not allowed to talk to plain http at all.
So `.github/workflows/dashboard.yml` does the rebuild, and the button fires it. The
published copy is <https://robertsben333-cmyk.github.io/claude_research/>.

| where the page came from | what the button does | what the badge says |
| --- | --- | --- |
| disk or localhost, with `--serve-bg` running | rebuilds here, rewrites the file | **live** |
| fetched over http(s) | starts the `dashboard` workflow | **CI** |
| neither reachable | hands over the command | (none) |

The workflow rebuilds the ledger, renders the page, **commits both back to `main`** and
republishes the site. It runs on a schedule (11:40 and 21:40 UTC, weekdays — the second
after the US close, so the day's bar exists), on a push that touches `research/` or the
scripts, and on demand. Its own commit touches only the outputs, which are not in its
`paths:` filter, so it cannot trigger itself.

Two things it needs, and neither is fatal when absent:

- **`ALPACA_API_KEY_ID` / `ALPACA_API_SECRET_KEY` as repository secrets** (optionally
  `ALPACA_BASE_URL`). Without them the build passes `--offline`: names are re-priced,
  and the trades, the equity curve and the fills stay at whatever the last build with
  credentials found. The page says so rather than reporting a zero. The ledger only
  ever reads the broker — nothing in this workflow can place, cancel or amend an order.
- **A GitHub token in your browser**, for the button to dispatch the run itself. Without
  one a click opens the workflow's own page, where *Run workflow* is one more click. With
  one — fine-grained, this repository, *Actions: read and write* — the button dispatches,
  watches the run and reloads when it lands. It is kept in that browser's `localStorage`
  and is sent to `api.github.com` and nowhere else. Reading the run's status needs no
  token at all, which is how the page can say *there is a newer build than this one*.

**Pages needs one click before any of this is served.** `actions/configure-pages` asks
to turn it on and `GITHUB_TOKEN` is refused — *Resource not accessible by integration*,
measured on the first run of 2026-09-19. Set **Settings → Pages → Source** to *GitHub
Actions* once, and the publish starts working. Until then the workflow still rebuilds
and still commits to `main`; it skips the publish rather than going red, so the button's
CI path reports success for a page nobody can fetch yet.

The helper runs those two scripts and nothing else; no part of a request reaches a
shell, it binds to `127.0.0.1`, and the broker is only ever read. Its CORS headers name
`null` (a file page) and localhost, so a site you happen to be visiting cannot read
what comes back — it could still fire the POST, which would rebuild a dashboard and
nothing more. `--token` closes even that.

Daily bars and 5-minute bars are cached under `.cache/bars` (gitignored), so a
rebuild that adds one day costs one day of fetches. A run whose outcome window has
not closed is reported as a problem, not as a zero — it re-prices itself on the
next update.

## The controls, and what they change

Everything on the page is recomputed client-side from the rows in the ledger, so a
control is not a view — it re-derives every statistic under it. That is the point: a
threshold you cannot move is a threshold you cannot test.

| control | what it does |
| --- | --- |
| **lens** | *onderzoek* is every ranked name at its board return; *handel* keeps only names that became a position and uses the broker's own return |
| **uitstap** | which exit the board return is measured at. **Default `strategie`**, which is not one moment: amc sells into the opening print at 15:30 CET and bmo at 20:00 CET. The eight fixed horizons stay in the list so any of them can still be swept |
| **drempel** | `\|impact_sum\| >=` this. Off by default, so the landing view is the full sample; on, **every table and chart on the page** holds only names that clear it |
| **verhandelbaar** | a turnover floor per side — shorts get a higher one, because a short needs size *and* a borrow — plus an optional "only what Alpaca will lend" |
| **positiecap** | the sizing rule, recomputed: a gross budget split equally over the day's names, capped per name. Off means equal weight and always fully invested, which is the research number and not what an account does |
| **periode** | which runs count, by preset or by two dates. Every chart's x-axis follows it |
| **sessie / sector** | amc against bmo, and one sector at a time |

## The default exit is the strategy's, not a single horizon

The two sessions are sold at different moments, so one column cannot describe the
book. `strategy` resolves per session in the ledger and is carried as if it were a
horizon, so every tab reads it the same way as the rest:

| session | CET | ET | field |
| --- | --- | --- | --- |
| amc | 15:30 | 09:30 | `mv_open`, the opening print |
| bmo | 20:00 | 14:00 | `hr_22` on the hour grid from the 16:00 ET entry close |

**The live config sells bmo an hour earlier than this column.** `orders.exit_mode` is
`amc_open`, whose bmo leg goes at plain market on stage E's own 13:05 ET run — 19:05
CET. On the 28 bmo names above the floor that hour is worth +4.24% at 19:05 against
+4.36% at 20:00 and +5.22% at the close, so the ordering is monotonic and the
dashboard default sits between the two. The page and the account disagree by one
hour; decide which is right rather than leaving it.

## The Hypotheses tab

A register of hunches, deliberately **not** wired into the `edge-performance` skill: it
is a place to test, not a step in a routine. Two halves, and the order is the point.

**1. Intermediate variables, screened first.** Thirteen candidates against three
outcomes that are not the same question — was the SIGN right, what did the BOOK earn,
how far did the stock MOVE. A variable that only ranks the third is a volatility proxy
and says nothing about skill; `retail_tilt`, `realised_vol_20d` and `rank` all sit
there, and they are largely the same fact three times.

**2. Hypotheses, written after reading that screen.** That is the honest order to work
in and the dishonest order to report, so the tab says so in its own header. One verdict
rule for all of them: the gap must carry the predicted sign and clear **two standard
errors of its own difference** — roughly a t-test at p<0.05. A first version used a flat
2pp bar and returned *steun* for seven of nine hypotheses on a book whose per-name
standard deviation is twelve, which is what a loose rule does.

A hypothesis comparing the same names at two exits (H2a, H2b) is **paired**, and is
tested on the per-name difference. Running it as two independent groups puts the whole
between-name spread into the standard error and can never find anything.

On the 13 resolved days three of ten survive: the sector spread, the price-lean
relationship, and the conviction floor itself — which is the anchor, and the only rule
in this repo that ever cleared a family-wise correction. Everything else reads *geen
effect*, including two the operator expected: bmo over amc, and the amc-early /
bmo-late exit split. Both exit tests lean the predicted way (+1.9pp and +2.2pp per name)
and neither reaches |t| = 2, so they are the two worth watching forward rather than
acting on.

## The Weging tab and the pre-registered weightings

**w2 is the design being carried forward.** The conviction floor stays the gate — no
factor adds a name and none removes one — and four factors set the SIZE instead, with
a per-name cap raised from 33% to 50% of equity:

    evidence      more findings behind the score
    retail        the consumer/retail character
    lean_agree    the sealed price lean points the same way
    search_quiet  less search traffic into the print

Each is −1 / 0 / +1; weight = clamp(1 + 0.125 * Σ, 0.5, 1.5); the day's gross is split
pro rata, capped per name, and a capped name's leftover redistributed — the same shape
as the live sizer, with a different weight and a different cap.

**The tab separates two things the headline mixes**, because they are a risk decision
and a research claim:

| book | per day | sd | t | compounded | per unit deployed |
| --- | ---: | ---: | ---: | ---: | ---: |
| A normal, equal, cap 33% | +4.28% | 6.29 | 2.36 | +62.1% | 4.551% |
| B cap 50% only, still equal | +4.94% | 7.01 | **2.44** | +74.0% | 4.941% |
| C w2 weighted, cap 50% | +5.12% | 7.47 | 2.37 | +77.0% | 5.121% |
| D w2 weighted, cap back to 33% | +4.37% | 6.92 | 2.18 | +62.9% | 4.641% |

**The cap does the work; the weighting adds almost nothing and costs variance.** A→B is
+0.66pp from deploying more on thin days. B→C is +0.18pp and t falls from 2.44 to 2.37.
At the old cap (D) the weighting is +0.09pp and t falls to 2.18. `evidence` is in the
spec on instruction and is the one factor the register measured as `geen effect` on its
own (H7); it is the first to drop if w2 underperforms.

**What the higher cap costs:** the per-name cap is the only risk control in the stage.
The 23% single-name gap that moved the account 4.5% at a 20% cap and ~7.5% at 33% moves
it ~11.5% at 50%. Nothing was added to offset that, and w2 is switched on nowhere.

### The factors are judged on every researched name, not on the book

The four books above are placed on the 56 names above the conviction floor, because that
is what the gate buys. The four **factors** are a claim about the hunt, and the hunt
ranked 105 names on the same days. Judging them on the traded half alone discards the
other half for no reason: the floor selects on `|impact_sum|`, which is not what any of
the four measure. The tab prints both columns.

| factor | n all | per name all | n book | per name book |
| --- | ---: | ---: | ---: | ---: |
| more findings +1 | 66 | +1.32% | 41 | +3.85% |
| more findings −1 | 11 | +0.18% | 4 | — |
| retail tilt +1 | 50 | +2.15% | 31 | +4.68% |
| retail tilt −1 | 55 | −0.85% | 25 | +2.47% |
| lean agrees +1 | 55 | +2.88% | 28 | +7.27% |
| lean agrees −1 | 50 | −1.96% | 28 | +0.11% |
| less search +1 | 28 | +0.41% | 14 | +5.32% |
| less search −1 | 19 | −1.12% | 8 | +0.37% |

**All four keep their sign on the doubled sample** and every level is lower, because the
below-floor half returns −2.98% per name against +3.69% above it.

The 49 names below the floor are the one part of these days no factor was chosen on —
every hypothesis in the register was asked of the traded book. It is not a clean
out-of-sample test (same days, same hunters, and the names are there *because* the hunt
found little), so read the sign of the gap and not its level:

| factor | gap below the floor | gap in the book | same sign |
| --- | ---: | ---: | --- |
| more findings | −1.86pp | — (n=4) | — |
| retail tilt | +1.64pp | +2.21pp | yes |
| lean agrees | +2.93pp | +7.16pp | yes |
| less search | −2.29pp | +4.95pp | **no** |

The two factors with register support behind them keep their sign; the two without —
`evidence`, which H7 measured as `geen effect`, and `search_quiet`, which is one
Bonferroni-uncorrected cell — invert. No gap here reaches two standard errors. Nothing
moves on it: the floor is still the gate and these names are not bought either way.

### w1, superseded and kept

w1 multiplies the score, so it changes which names clear the floor. It does **not**
replace the live rule: `edge_score.py` is untouched, the
book is still placed on the plain score, and this runs beside it so the two can be
compared on days that do not exist yet.

    w_score = impact_sum * clamp(1 + K * sum(tilts), 0.5, 1.5)      K = 0.15

Four tilts, each −1 / 0 / +1, drawn from what the hypothesis register found: price-lean
agreement (H5), search quiet (H9), retail tilt (H3), sector (H4). One magnitude for all
four — four fitted weights on 56 traded names is how a scheme memorises its sample.

**Two variants ship, both frozen, both tracked forward.** `w1` is symmetric; `w1_filter`
may only remove a name from the book and can never promote one the plain floor rejected.
The second exists because of what the first did in sample, and that reasoning is in the
module rather than hidden in a constant:

| rule | n | raak | per name |
| --- | ---: | ---: | ---: |
| plain | 56 | 64% | +3.69% |
| w1 symmetric | 52 | 65% | +3.09% |
| w1_filter demote-only | 48 | 69% | +4.27% |

The names `w1` **drops** were correctly dropped (+0.22%), what it keeps beats the book
(+4.27%), and the four it **promotes** return −11.01% — the whole of its
underperformance. The conviction floor is the only rule in this repo that ever cleared a
family-wise correction, so a tilt chosen on 13 days overruling it is the weakest link
doing the most consequential thing.

Shipping both rather than picking the better one is deliberate: `w1_filter` was designed
after seeing those four names, so choosing it on this sample would be the same fitting
error one level up. **Nothing here may be re-tuned.** A tilt that turns out wrong becomes
`w2` beside `w1`, never a quietly edited constant.

## The four tabs added 2026-09-18

`Timing` moves the EXIT with the entry fixed at the 22:00 CET close. These are the
questions that sit beside it, and each one is recomputed from the filtered rows like
everything else — a threshold you cannot move is a threshold you cannot test.

| tab | the question | what came back |
| --- | --- | --- |
| **Instap** | buy at 20:00 CET, or later? The exit is held at the selected horizon and only the entry moves | nothing: about half a point between the best and worst entry of the whole session, against a per-name sd near 13 |
| **Aanloop** | does the 2/5/10/20-session return INTO the entry predict whether the sign was right, and does it pay when run-up and prediction agree? | nothing, and the agreement result flips sign between the full sample and the traded book, which is what noise does when you cut it in two |
| **Zoekvolume** | does Google Trends interest say anything about the trade? | the one lead: above the floor a bigger search spike goes with a worse outcome. Half the book is not measurable at all, and the measurable half is the liquid half |
| **Agenda** | what reports next week, through both gates | a plan, not a measurement — no prediction, no ranking, no score |

Two feeders run before the ledger and are allowed to fail without costing you the
rebuild: `researcher_us/scripts/edge_search_volume.py` (Google Trends, cached) and
`researcher_us/scripts/edge_calendar.py` (the forward week). `--no-feeders` skips both. The
calendar is dropped by the ledger once it is more than three days old, because a stale
list of "what is coming" is a list of what already came.

**Read `measures()` in `edge_search_volume.py` before trusting a Trends number.** Each
series is normalised to its OWN maximum, so a name searched on three days out of ninety
reads 0…0,100 and a spike over a zero median comes out at 100×. Eleven such names filled
the top tercile on the first run. A series now needs a non-zero median to be scored.

Three returns travel together on the overview, because they are not the same number and
the difference between them is usually larger than either: **per name or position** (with
its standard deviation, quartiles and worst/best, since on this sample the spread is an
order of magnitude wider than the mean), **per day** (every day weighted equally, whatever
its name count, scaled by what the position cap would actually have deployed), and
**total** (compounded over the period, beside what the broker's own equity did).

The **Drempel** tab sweeps the threshold rather than assuming one: return, hit rate, ρ
and n at fifteen cuts, split by session and by thin against thick turnover. It is the
tab to read before believing any single cut, because the cut in `config/pipeline.yaml`
was chosen on the same events it is judged on.

## A run whose window has not closed

A stage E run resolves against the session *after* the print, so this morning's run has
no outcome until tonight's close. `edge_exit.py` refuses those rows, rightly — it feeds
the analysis scripts. But refusing them made the whole day disappear here: on 2026-09-17
the 09-16 run had two live positions and no row anywhere, and every chart simply stopped
a day early with nothing saying why. `build_ledger.py` now adds a **pending row** for
such a name, carrying the horizons that already exist (the after-hours print, the
pre-market) and `pending: true`. At the `close` horizon it still has no return and drops
out of the statistics; switch the exit control to `pre_open` and today's names appear
with what the market is doing to them right now. The overview names them explicitly
rather than letting the line end.

## A sector's consumer tilt

There is no free source for ownership — Yahoo's holders breakdown sits behind a crumb and
13F is quarterly and institutional-only — so the sector tab carries a **proxy**, built
from four things already in the tree that all point the same way: daily dollar volume over
market cap, small market cap, low share price, and 20-day realised volatility. Each is a
percentile over the whole sample, averaged to 0–100. It is a tilt, not a measurement, and
the components sit beside it in the table so a reader can see which one moves a sector.
The scatter next to it asks the question the indicator exists for: does the edge live in
the names consumers trade? On the first build the answer is no — slope 0.04, r² 0.00.

## The other three markets: Europa, Japan, Australië

Stage EU, stage J and stage AU run the same hunt with the same scorer over the ASX,
Tokyo and ten European venues, and **none of the three places an order**. So they get
their own tabs rather than rows in the ledger: there is no money level for them and
there must not be one. Everything on those three tabs is the research level.

```bash
python3 dashboard/scripts/build_markets.py             # collect what is on disk
python3 dashboard/scripts/build_markets.py --resolve   # and fetch missing outcomes
```

`update.sh` runs it with `--resolve` as a third feeder, allowed to fail like the other
two; `--no-feeders` skips all three. It writes `dashboard/data/markets.json`, which
`build_dashboard.py` inlines beside the ledger. A missing file is not an error: the tabs
say so themselves.

**It does not own the outcome window, and that is deliberate.** Europe and Australia
report before the open, so their window is `close(D−1) → close(D)`; Tokyo's runs from
the close to the next open. That logic lives in `eu_resolve.py`, `jp_resolve.py` and
`au_resolve.py`, and this collector reads the `*-resolved.json` those write. With
`--resolve` it calls the market's own resolver for a run whose window has closed and
which has no outcome yet. A realised move on these tabs was computed by the market's
resolver or it is not there.

Three things the tabs keep apart, because each of them has already been read wrong once
somewhere in this repo:

- **A validation run is not research.** The two European days that have resolved ran on
  *synthetic* findings to test the chain end to end. They are excluded by default and the
  switch that includes them says what they are. Stage AU's validation never landed in
  `research/` at all, so that tab is honestly empty.
- **An unhunted name is not a zero.** Seven UK names on 2026-09-23 carry `impact_sum: 0`
  and `rankable: false` because the session could not spawn subagents. They appear in the
  names table with `not_rankable_because` in place of the number and count in no
  statistic; a nought nobody measured pulls every ranking toward the middle.
- **A shut exchange is not a failed run.** Tokyo was closed on 2026-09-21 and 09-22, and
  the run directory says so in `market_closed`. The runs table prints the reason instead
  of a zero.

**ρ is withheld below five names.** On three names a rank correlation of exactly 1.0
comes up one time in six, which `au_resolve.py` writes down after the first synthetic
Australian run duly produced one. Below five the tab shows the names and no coefficient.
Above it, the pooling is one flat pool over all days rather than the within-day centring
the US tabs use — there are not enough days for that yet — and there is no permutation
test and no multiplicity correction, because on this many names both would suggest more
precision than exists.

**A premature resolve is re-resolved.** Yahoo's European daily closes lag a session or
two, so a run resolved the morning after its print writes a file in which every row is
`move_pending`. Treating that as done would freeze the day at nothing permanently, and it
would look exactly like a day on which the hunt had no outcome. A resolved file with no
realised move and at least one live row is fetched again; one that carries even a single
move is left alone, because the window it priced has closed.

## What the numbers mean

- **bord-rendement** (board return) is the realised move in the direction of the
  sign of `impact_sum`. No spread, no slippage, no borrow cost. It is what the
  ranking would have paid if execution were free, which it is not.
- **ρ** is Spearman rank correlation pooled *within* days — each day converted to
  within-day ranks, centred, then correlated across days. Concatenating raw pairs
  across days lets market-wide drift into the rank structure and overstates
  nothing but flatters the noise.
- **the free control** is `-run_up_20d_pct`: one number off the sealed baseline,
  available before a single subagent is spawned. The hunt has to beat it to have
  established anything, and on the current sample it does not.
- **conviction** is `|impact_sum|`. The direction test asks whether its rank
  predicts whether the sign turned out right, which needs no threshold.

## What it establishes today, stated plainly

Over 13 runs and 102 ranked names on 11 days, the pooled ranking correlation is
**negative**. The five days the repo's own `EDGE_ANALYSIS.md` was written on
(08-31 through 09-07) rank at ρ≈+0.38; every day since 09-08 ranks at or below
zero, and the free control went negative with it. The account is up double digits
over eight sessions on nine closed positions, and that result is one leg: the
longs paid and the three shorts all lost. Nine positions is not a sample, the 95%
interval per trade spans more than twenty points, and the dashboard says so on its
first screen.

Read the numbers here as a measurement instrument that is now running, not as a
verdict. The verdict needs days.

## Theoretical against actual, and what the gap contains

The **Handel** tab prices every closed position twice: what the broker got, and what
the price series says the same name did over the stage's own window. Two gaps, and
they answer different questions.

- **policy gap** — actual minus the board return from the close before the print to
  the close after. It contains the entry timing (the book goes in around 13:24 ET
  while the board assumes that day's close), the spread, and every hour the exit was
  early or late.
- **exec gap** — actual minus the board return *at the hour the position was actually
  closed*. Timing is divided out, so what is left is the spread, the fill quality and
  the partial fills. It is only computable where a grid hour sits within two hours of
  the real exit, which rules out the positions that sat open for four days.

## Cost per run

No token count is recorded anywhere in this repo, so the **Kosten** tab runs on a
proxy: the bytes each run wrote, over four, plus its subagent count. Drop real numbers
into `data/costs.csv` (`run_date,tokens_in,tokens_out,usd,note`) and they are used
instead, with the proxy kept beside them so the two never silently merge.

## What it deliberately does not do

- It never submits, cancels or modifies an order. `researcher_us/scripts/alpaca_trade.py`
  is the only thing in this repo that does, and it knows only the US account: the
  Europe, Japan and Australia tabs have no money level at all.
- It does not re-score a run. `impact_sum` is read as the run wrote it.
- It does not drop a losing day, a microcap or an outlier. Every exclusion in the
  ledger is a duplicate event (one issuer reporting once, hunted twice) and is
  flagged as such in `names.csv`.
