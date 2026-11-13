# Stage EU at Interactive Brokers

Since 2026-11-08 (operator's instruction) stage EU's panel book can be traded in a
dedicated IBKR account: **sell everything at 15:35 Amsterdam, buy the panel's names once
the Routine has scored them**. It is committed switched off (`execution_eu.enabled:
false`, `environment: paper`).

**The EU panel has no measured edge yet.** The 2026-10-21 study put it at rho +0.22,
p 0.19 over 45 live names on 7 days, with four names at or above 70. Trading it is a way
to find out, with money at risk, not the use of a finding.

## Who places the orders: the operator's server, not the Routine

IBKR gives API logins without a gateway (OAuth) to **institutional clients only**. The
operator's OAuth registration was refused on 2026-11-08 ("OAuth1.0a is only available to
institutional clients"), and IBKR's own page says OAuth 2.0 "is not available to
Individual account structures". An individual account reaches the API only through a
logged-in gateway, and a Routine is a fresh cloud container that cannot hold one.

So the work is split:

| where | what | code |
| --- | --- | --- |
| cloud Routine (stage EU) | research, panel, then step 6b `ibkr_trade.py handoff`: writes `<RUN>/ibkr-handoff.json` and publishes. No broker call. | skill steps 0s / 6b |
| operator's server (Oracle Always Free or any VPS) | IB Gateway kept logged in by IBC; `eu_executor.py` sells at 15:35 and buys when the handoff is on main | `researcher_europe/executor/` |

Nothing connects in to the server: it only fetches from GitHub and talks to the gateway
on localhost. IBKR's username and password live on that server only. The order code is
the same `ibkr_trade.py`, through `ibkr_tws.py` (the TWS API via `ib_async`) instead of
the REST client; `ibkr_client.py` (OAuth / Client Portal) stays for the day IBKR opens
OAuth to individuals.

## The day

| Amsterdam | where | what happens |
| --- | --- | --- |
| 15:30 | cloud | Routine fires, heartbeat, step 0s prints `mode` only |
| 15:35 | server | `eu-flatten.timer`: git pull, `check`, `flatten`: cancel working orders, sell/cover every position (collared DAY limits), wait 2 min, log what is still held |
| 15:35-16:20 | cloud | universe, baselines, hunters, panel, note, publish (40-45 min measured) |
| ~16:20 | cloud | step 6b `handoff`, publish |
| 16:00-17:30 | server | `eu-open.timer`: git pull every 2 minutes; on today's handoff, `open` once: buy/short names with `panel_pct` >= 70 and four judges |
| 16:25-17:35 | | markets close; a name is skipped only if its market is already closed |

A position is held from about an hour before the close of D-1 to about two hours before
the close of D. The scored window is close(D-1) to close(D). A Friday book is held over
the weekend. If the server is off, nothing is sold or bought that day; the next flatten
sells whatever is held.

## The rule (`execution_eu` in `config/pipeline.yaml`)

- **Entry**: `panel_pct` >= 70 with all four judges; side from the panel; turnover at
  least $200k a day; the name's market still open.
- **Weight**: `panel_pct` - 60, linear, at most 50% of equity a name; what a capped name
  cannot take goes to the others (`alpaca_trade.allocate`, the same code as stage E-P).
- **Budget**: 100% of net liquidation minus anything still held.
- **Hard limits**, checked again right before each order: `max_gross_base` 10,000,
  `max_name_base` 5,000 (account base currency), `max_names` 6, `max_orders_per_run` 20,
  and a name is dropped when IBKR's price is more than 20% from the sealed spot.
- **Orders**: DAY limits 1% through the price for entries, 2% for exits, routed SMART.
  Prices are IBKR's free delayed quotes (no market-data subscription, operator's choice);
  IBC sets `AllowBlindTrading=yes` so the gateway accepts orders without live data.

## Four switches, all needed to send an order

1. `execution_eu.enabled: true` on `main` (a PR). The server pulls main before every run.
2. `--submit`, which only `eu_executor.py` passes.
3. `IBKR_ENVIRONMENT` in the server's `/etc/eu-executor.env` equal to
   `execution_eu.environment`.
4. `IBKR_ACCOUNT_ID` naming the only account the gateway login sees, `DU...` on paper and
   `U...` on live.

Turning trading off is one line on main: `enabled: false`. Stopping the server's timers
(`sudo systemctl disable --now eu-flatten.timer eu-open.timer`) also stops it.

## Setup

`researcher_europe/executor/README.md` has the steps; `install.sh` does the server side.
In short: a dedicated IBKR account with its own username (IBKR Pro, margin, EUR base,
stock permissions in the ten markets), its paper account, an Ubuntu server, a GitHub
fine-grained token for this repository, then `bash install.sh`, approve the login on
the phone, and `eu_executor.py check`. The gateway restarts itself nightly; IBKR asks
for a phone confirmation about once a week (Sunday).

Then: paper first (`environment: paper`, `enabled: true`), at least two weeks, comparing
the fills on branch `eu-ibkr-log` with the scorebord; then live (`environment: live`, a
re-run of `install.sh` with the live username and `U...` account).

## Costs that a paper account hides

- UK stamp duty 0.5% on every UK purchase (not on a short); French FTT 0.4% and Spanish
  FTT 0.2% on purchases of large caps; Italian FTT 0.2% on positions held overnight. On a
  long that is held one day these are the same size as the expected edge.
- IBKR commissions in Europe are about 0.05% with a minimum per order (roughly EUR 1.25
  to 3 depending on the market), so a EUR 500 position pays a large share in minimums.
- Holding GBP, SEK, DKK, NOK and PLN positions from a EUR account creates negative
  currency balances (interest) and leaves positive ones after the sell.
- Paper fills are simulated against quotes and are kinder than real fills in thin names.
- The bid-ask spread in these names, roughly 0.5% a round trip, is larger than all of
  the above and the same at every broker.

## The limit price must sit on the exchange's tick ladder (fixed 2026-11-13)

The first live order, a MEGP short on 2026-11-13 for the 2026-11-16 print, never reached
the book: the LSE refused a sell limit at **101.376p** with Error 110 ("the price does not
conform to the minimum price variation"), and `open` reported `0 sent, 1 failed`. The limit
was the collared mid rounded to `contractDetails.minTick`, a contract-wide number far finer
than the LSE's price-banded ladder. Since the fix the TWS adapter reads the contract's
market rule (`marketRuleIds` -> `reqMarketRule`, the (lowEdge, increment) bands of the
primary listing, or the coarsest band any listed venue imposes if the primary cannot be
picked out) at the limit price itself, and rounds outward (down for a sell, up for a buy).
If an exchange still refuses the tick, `place_order` re-rounds once onto a coarse grid (1%
of the price's order of magnitude: 101p -> 1p) and records `retried_tick` on the leg. Any
other refusal is not retried. `smoke_test.py` replays the MEGP case.

## What is not verified yet

- The whole server path against a real gateway: `ibkr_tws.py` is tested only against a
  fake `ib_async` in `smoke_test.py`, and `install.sh` has not run on an ARM server.
  The first `eu_executor.py check` settles the connection.
- IBKR's symbols and exchange codes for each market (`DEFAULT_EXCHANGES`, matched on
  the primary exchange); `ibkr_trade.py contracts --run <RUN>` on the server lists every
  resolution, and `execution_eu.exchanges` / `conid_overrides` correct it.
- Whether IBKR quotes London in pence or pounds; the code detects it from the ratio to
  the sealed spot and refuses a London name when it cannot tell.
- Whether delayed snapshots arrive for every market without subscriptions. With a
  delayed price a 1% collar can miss a name that moved more than 1% in 15 minutes; the
  order then works until the close.

This is research, not investment advice.
