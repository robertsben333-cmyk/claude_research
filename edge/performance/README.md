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
```

Daily bars and 5-minute bars are cached under `.cache/bars` (gitignored), so a
rebuild that adds one day costs one day of fetches. A run whose outcome window has
not closed is reported as a problem, not as a zero — it re-prices itself on the
next update.

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

## What it deliberately does not do

- It never submits, cancels or modifies an order. `edge/scripts/alpaca_trade.py`
  is the only thing in this repo that does.
- It does not re-score a run. `impact_sum` is read as the run wrote it.
- It does not drop a losing day, a microcap or an outlier. Every exclusion in the
  ledger is a duplicate event (one issuer reporting once, hunted twice) and is
  flagged as such in `names.csv`.
