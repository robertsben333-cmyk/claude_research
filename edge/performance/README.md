# edge/performance — what the hunt is actually worth

Stage E produces a number per company. This folder is the only place that asks,
systematically and over every day at once, whether that number is worth anything —
and what the account did with it.

Nothing here runs a hunt, scores a finding or places an order. It reads.

```
edge/performance/
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
| **names** | every rankable name of every run, priced at eight exit horizons | `edge-scores.json` + `baselines/` + Yahoo bars |
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
./edge/performance/update.sh            # broker + re-price + render
./edge/performance/update.sh --offline  # no broker call, keep the last broker state
./edge/performance/update.sh --publish  # and commit + push
./edge/performance/update.sh --fresh    # drop the bar cache, re-price everything
./edge/performance/update.sh --serve    # and serve it, so the page's own button works
```

**The refresh button in the page.** Opened as a file, a page cannot run a script, so
the button hands over the command instead of pretending. Started with `--serve` it
POSTs to a localhost-only helper that runs the same two scripts and reloads the page.
The helper runs those two scripts and nothing else — nothing from the request reaches
a shell, and the broker is only ever read.

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
| **sessie / sector** | amc against bmo, and one sector at a time |

The **Drempel** tab sweeps the threshold rather than assuming one: return, hit rate, ρ
and n at fifteen cuts, split by session and by thin against thick turnover. It is the
tab to read before believing any single cut, because the cut in `config/pipeline.yaml`
was chosen on the same events it is judged on.

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
