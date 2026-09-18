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
up. Nothing answering means the button hands over the command instead of pretending.

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
| **uitstap** | which of the eight exit horizons the board return is measured at |
| **drempel** | `\|impact_sum\| >=` this. Off by default, so the landing view is the full sample; on, **every table and chart on the page** holds only names that clear it |
| **verhandelbaar** | a turnover floor per side — shorts get a higher one, because a short needs size *and* a borrow — plus an optional "only what Alpaca will lend" |
| **positiecap** | the sizing rule, recomputed: a gross budget split equally over the day's names, capped per name. Off means equal weight and always fully invested, which is the research number and not what an account does |
| **periode** | which runs count, by preset or by two dates. Every chart's x-axis follows it |
| **sessie / sector** | amc against bmo, and one sector at a time |

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
rebuild: `edge/scripts/edge_search_volume.py` (Google Trends, cached) and
`edge/scripts/edge_calendar.py` (the forward week). `--no-feeders` skips both. The
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

- It never submits, cancels or modifies an order. `edge/scripts/alpaca_trade.py`
  is the only thing in this repo that does.
- It does not re-score a run. `impact_sum` is read as the run wrote it.
- It does not drop a losing day, a microcap or an outlier. Every exclusion in the
  ledger is a duplicate event (one issuer reporting once, hunted twice) and is
  flagged as such in `names.csv`.
