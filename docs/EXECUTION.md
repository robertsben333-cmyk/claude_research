# Placing stage E at Alpaca

`scripts/alpaca_trade.py` turns stage E's ranking into real orders and closes them
again. It is off in the committed config and stays off until someone sets
`execution.enabled: true` deliberately.

## The one rule

```
|impact_sum| >= conviction_floor   ->   long if positive, short if negative
```

That is the whole selection. It is the only cut in `docs/EDGE_ANALYSIS.md` that
survived a family-wise correction over the thirteen candidate rankings it was chosen
from: above the floor the sign was right on 16 of 21 events at +6.37% per trade
(t=2.74, CI [+1.80, +10.72], +4.87% after a 1.5% round-trip cost); over all 38 events
it is 53%, a coin flip. Below the floor nothing is traded, because below the floor
there is nothing to trade.

Two screens sit on top of it, both because the measured result is unreachable
without them:

| screen | why |
| --- | --- |
| `min_dollar_volume_usd: 5000000` | six of the first 22 long/short positions traded under $1m a day, and the best trade in the sample (DLTH +23.20%) turns over $170k. A fill at that size is not a price the measurement ever saw. |
| Alpaca `shortable` | a rejected short leg turns a market-neutral book into a naked long. Names Alpaca will not lend are dropped, not flipped. |

Names whose event the sweep could not confirm (`rankable: false`) never reach the
book. `edge-scores.json` itself is still unfiltered — the ranking test needs the
complete table — and this script is the only place a cut is applied.

## Setting it up

```bash
export ALPACA_API_KEY_ID=...            # paper keys first, and for a long time
export ALPACA_API_SECRET_KEY=...
export ALPACA_BASE_URL=https://paper-api.alpaca.markets    # the default
```

Credentials live in the environment. Nothing writes them to the repo, and the
account number never enters a committed file.

Then in `config/pipeline.yaml`, under `execution:`, set `enabled: true`. Four things
must all hold before a single order is sent: `enabled: true`, `--submit` on the
command line, credentials in the environment, and a paper endpoint — a live endpoint
additionally needs `--live-account-i-understand`. Any one missing and the run is a
dry run that prints the book and writes `alpaca-plan.json`.

Shorting needs a margin account. On a cash account every short leg comes back
rejected and the book is long-only, which is a different strategy from the one that
was measured.

## Two invocations, two days

Both legs are market-on-close, because that is the window `edge_resolve.py` scores:

| print | entry | exit |
| --- | --- | --- |
| `amc` on day D | close of D | close of the next session |
| `bmo` on day D | close of the session before D | close of D |

Every name in one run therefore enters at the same close — the run's own date — and
exits one session later. Alpaca stops accepting MOC orders ten minutes before the
bell, so:

```bash
# on the entry date, after stage E has written edge-scores.json, before 15:50 ET
python3 scripts/alpaca_trade.py plan  --run research/2026/09/2026-09-09/edge
python3 scripts/alpaca_trade.py open  --run research/2026/09/2026-09-09/edge --submit

# on the exit date, before 15:50 ET
python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit

# any time
python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'
```

`close` with `--scan` walks every run that has an `alpaca-orders.json` and closes
only the legs whose `exit_date` is today, so one daily invocation covers whatever is
open. It reads the actual position quantity from Alpaca rather than the order, so a
partial fill closes flat. `--all` ignores the dates and `--now` sends plain market
orders instead of MOC — that pair is the panic button.

To run it unattended, two Routines are needed beside stage E's own. The prompts are
in `docs/routine-prompts/edge-execute.md`. Stage E's Routine prompt is deliberately
**not** changed: it has to be pasted in by hand and one hand-pasted file is already
drifting.

## What it refuses to do

Every refusal is recorded with its reason, in the plan or in `alpaca-orders.json`:

- send anything without `enabled: true` **and** `--submit`
- touch a live endpoint without `--live-account-i-understand`
- place an entry on a day that is not the planned entry date (`--force-date` overrides,
  and a forced fill is no longer the price the measurement uses)
- send an MOC order inside Alpaca's cutoff (`--allow-market-fallback` sends a plain
  market order instead, at a worse price than the one measured)
- short a name Alpaca does not call shortable
- size a position above 4% of equity or 1% of the name's 20-day dollar volume
- place a second order for a leg it has already placed — `client_order_id` is
  `edge-<date>-<TICKER>-<entry|exit>`, so a re-run of a killed session is a no-op
  rather than a doubled position

## What it does not know

- **The rule is 21 trades over 5 independent days.** `max_positions: 10`,
  `gross_exposure_pct_of_equity: 20` and the 4% per-name cap are sized for a lead, not
  for an edge. Re-derive the floor from the pooled sample before raising any of them.
- **Nothing checked the findings.** There is no adversary pass and no second hunter,
  so a factually wrong finding enters `impact_sum` at full size and reaches the book
  unexamined.
- **The key is not reproducible to better than its own size.** While the double hunt
  ran, twelve paired names came back with a median gap of 2.40 points and four of the
  twelve had opposite signs, on a key whose typical magnitude is about 5. Nothing
  re-measures that now.
- **It has not beaten a free control.** `-run_up_20d_pct`, available before any
  subagent is spawned, ranked the same six days at ρ=0.335 and was positive on 6 of 6
  days when traded. The plan prints `run_up_20d_pct` beside each position for exactly
  that comparison.
- **Share counts come off the sealed baseline's spot**, taken hours before the close
  the order fills at, so the notional drifts with the day's move. The alternative is
  an unsourced live quote.
- **The position is held through the print overnight**, unhedged, with no stop. That
  is the window that was measured; a stop would be a different strategy with no
  measurement behind it.

This is research, not investment advice.

## Files it writes

```
research/<Y>/<M>/<date>/edge/
  alpaca-plan.json      what the benchmark selected, sized, with every rejection and
                        its reason. Written by `plan` and by `open`. Derived state.
  alpaca-orders.json    what was actually submitted: client_order_id, order id, qty,
                        side, entry and exit dates, and an append-only log. Written
                        only when something is really submitted. NOT derived state —
                        it is the record of what the account was told to do.
```
