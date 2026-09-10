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
| `min_dollar_volume_usd: 200000` | below this an order is a meaningful share of the day's volume. It was $5m until 2026-09-10; see below for what the loosening costs. |
| Alpaca `shortable` | a rejected short leg turns a market-neutral book into a naked long. Names Alpaca will not lend are dropped, not flipped. |

### Where the turnover floor came from

Measured on the 38 de-duplicated events, close-before to close-after, taking every
name with `|impact_sum| >= 3` and its sign:

| floor | trades | direction | binom p | return per trade | t |
| --- | --- | --- | --- | --- | --- |
| none | 21 | 17/21 | 0.004 | +6.18% | 2.66 |
| **$200k** (shipped) | **18** | **15/18** | **0.004** | **+5.86%** | **2.38** |
| $1m | 16 | 13/16 | 0.011 | +6.08% | 2.20 |
| $2m | 15 | 12/15 | 0.018 | +4.95% | 1.84 |
| $5m (was shipped) | 12 | 11/12 | 0.003 | +8.09% | 3.85 |
| $10m | 9 | 9/9 | 0.002 | +9.64% | 4.22 |

Regenerate that table with `python3 scripts/edge_turnover_floor.py`, which also lists
the individual trades each floor adds or refuses.

**The shipped floor is not the best row, and the reason it is not is deliberate.**
Higher floors look better here, and that is most of the reason to distrust the shape:
picking the floor that maximises an in-sample return over 38 events is the same move
that put the ranking's own p at 0.056 under a max-statistic test. The six trades that
$200k admits and $5m refused came in at 4/6 and +1.40% a trade, with one −22.23% (NX,
short, $4.89m of turnover) among them. At n=38 no two adjacent rows are
distinguishable.

Two things the table cannot see decided it:

- **Spread.** The measurement charges a flat 1.5% round trip, which was the argument
  for a high floor. The operator's reading is that the real spread in these names is
  far below that, which removes it. If that turns out wrong the cost lands on exactly
  the names this floor admits, so it is worth checking against a few actual fills
  before the position sizes matter.
- **Event rate.** 18 of 38 events trade at $200k against 12 at $5m. That is how a
  forward sample stops being one small sample a week, and it is a claim about
  learning speed, not about expected return.

The 1%-of-turnover sizing cap does the rest, and at this account size the two lines
meet: at $10k of equity the 20% per-name cap is $2,000, which is exactly 1% of a
$200k/day name. Below that floor a position would be capacity-bound anyway, so the
floor and the cap are saying the same thing from two directions.

Names whose event the sweep could not confirm (`rankable: false`) never reach the
book. `edge-scores.json` itself is still unfiltered — the ranking test needs the
complete table — and this script is the only place a cut is applied.

## Setting it up

**Nothing to install.** The script is standard library plus PyYAML, which the repo
already uses. No `alpaca-py`, no market-data subscription: it reads spot from the
sealed baseline and calls only the trading API (`/v2/orders`, `/v2/positions`,
`/v2/account`, `/v2/assets`, `/v2/clock`, `/v2/calendar`), all of which are free on a
paper account.

1. **An Alpaca account, on paper.** app.alpaca.markets → Paper Trading → generate an
   API key. A paper account starts with $100k and needs no funding.
2. **Margin, if the shorts are meant to happen.** Paper accounts are margin accounts
   by default. On a cash account every short leg comes back rejected and the book is
   long-only, which is a different strategy from the one that was measured.
3. **Credentials as environment variables**, never in the repo. Locally that is a
   shell export; for anything unattended it has to be on the cloud environment,
   because a Routine fires into a fresh container that has only this repo:

   ```bash
   export ALPACA_API_KEY_ID=...
   export ALPACA_API_SECRET_KEY=...
   export ALPACA_BASE_URL=https://paper-api.alpaca.markets    # the default
   ```

   On the cloud environment (claude.ai/code → the cloud icon → the environment →
   **Environment variables**), the same three lines in `.env` format, one
   `KEY=value` per line, no quotes and no `export`. A session copies the values once
   at startup, so a session that is already running keeps the old ones: restart it
   after editing. Everyone who uses that environment can read them, which is the
   argument for keeping the keys paper-only.

   **Network access.** The environment has to be able to reach
   `paper-api.alpaca.markets`. The `Default` environment on this account
   (`env_01TeUycLFPpAmGb3pDNEHNtp`) does — verified 2026-09-10, the endpoint answers
   401 rather than being blocked. If a Routine is ever pointed at another
   environment, set **Network access** to **Custom** and add the host.

   On Pro and Max there is also an **API credentials** slot that keeps a key outside
   the sandbox entirely and lets the agent proxy attach it. It is the safer shape in
   principle, but Alpaca authenticates with two custom headers
   (`APCA-API-KEY-ID` and `APCA-API-SECRET-KEY`), and this script builds those
   headers itself and refuses to submit when it finds no credentials — so using it
   that way needs a code change, not just configuration. Environment variables are
   what is supported today.
4. **`execution.enabled: true`** in `config/pipeline.yaml`. This is the switch. Four
   things must all hold before a single order is sent: `enabled: true`, `--submit` on
   the command line, credentials in the environment, and a paper endpoint — a live
   endpoint additionally needs `--live-account-i-understand`. Any one missing and the
   run is a dry run that prints the book and writes `alpaca-plan.json`.
5. **Check it end to end on one past run first**, which needs no credentials at all:

   ```bash
   python3 scripts/alpaca_trade.py plan --run research/2026/09/2026-09-09/edge
   ```

6. **Re-paste the stage E Routine prompt** from `docs/routine-prompts/edge-hunt.md`,
   which carries both trading steps. No new Routine is needed. Do this only once steps
   1 to 5 have been watched for a few days — and note that steps 1, 2 and 5 are worth
   doing before step 4, so the first few days run with the switch still off.

## Sizing: equal weight, whole budget

Every name that clears the benchmark gets the same dollars. The gross budget
(`gross_exposure_pct_of_equity`, 100%) is split N ways, each name is capped at
`max_position_pct_of_equity` (20%), and whatever a capped name cannot take is
redistributed equally over the names that are not yet capped, repeating until nothing
moves. So the account deploys as much as the caps allow and every uncapped name holds
the same amount as every other one.

**Nothing in the sizing reads the score.** A name at `impact_sum` 12 gets exactly what
a name at 3.1 gets. That is not modesty: the key ranks and does not size — median
absolute error 6 to 7 points against a realised standard deviation near 11 — so
weighting by it would be sizing on a number with no measured relationship to the size
of the move.

Two consequences worth knowing before the first run:

- **Under five names the account is deliberately under-invested.** Three names at the
  20% cap is 60% deployed, and there is nowhere for the rest to go.
- **The whole account rides five to nine earnings prints overnight, unhedged, with no
  stop.** Two names in the resolved sample gapped 22–23% (NX +22.23%, CANG −23.01%);
  at a 20% weight either one moves the account about 4.5%. Reg T allows twice equity
  overnight, so 100% gross fits comfortably in buying power — the constraint here is
  not margin, it is that nothing cuts a loss.

`max_position_pct_of_adv` (1%) stays as a slippage guard and only starts to bind as
the account grows: at $10k of equity a 20% position is $2,000, which is 1% of a
$200k/day name. The plan prints `%adv` per name either way, so the share of the
closing auction each order represents is visible rather than inferred.

## Where this runs: inside stage E, not beside it

There is no separate execution Routine. Trading is two steps in the stage E skill and
its own session, four hours apart:

| step | when | what |
| --- | --- | --- |
| 0b | before the sweep launches, ~16:05 Amsterdam | `flatten --submit` — sell yesterday's book at market |
| 7 | after the note is published, ~19:00 | `plan`, then `open --submit --no-flatten` — buy today's at market |

The sell goes **first**, and not because it is tidier. Every position in the account
has already been through its print by then, so nothing is cut short of its event; and
if the session dies mid-hunt — four consecutive days of that have happened to another
stage in this repo — the account is in cash rather than holding a book nobody is
managing. Flattening at the end would leave a killed session's positions open
indefinitely.

It is not free. The measured exit is the next **close** (direction ρ=+0.514,
permutation p=0.0015); selling half an hour into the session is nearer the next
**open**, which measured weaker on the same events (ρ=+0.331, p=0.046). That gap is
the price of one Routine with nothing handed between sessions.

**Step 7 buys at market, not in the closing auction.** Both were measured on the same
18 traded events:

| entry | direction | binom p | return per trade | t |
| --- | --- | --- | --- | --- |
| market-on-close | 15/18 | 0.004 | +5.86% | 2.38 |
| market at 14:00 ET | 14/18 | 0.015 | +5.82% | 2.41 |

Four hundredths of a point per trade, one event of eighteen changing sign (PL, 09-03).
`scripts/edge_entry_timing.py` regenerates it. So the auction buys nothing worth a
pending order and a cutoff, and the entry is a plain market order filled while the
session watches.

What that measurement **cannot** see is the spread: it compares trade prices, not
fills, and the closing auction is the deepest liquidity of the day — which matters more
since the turnover floor dropped to $200k, not less. `status` prints
`filled_avg_price` per order, the run log is asked to record it, and
`orders.entry: market_on_close` puts it back in the auction if those fills come back
materially worse than the plan's notional. That is the one number that should decide it.

The only deadline left is that the US session has to still be open: 16:00 New York,
22:00 Amsterdam in summer. A run firing at 16:04 has three hours of margin after its
hunts; the 2026-09-09 run took 2h53m end to end. A session that was retried, resumed or
ran long may have none, and `open` refuses rather than sending an order into a closed
market.

`--no-flatten` on step 7 stops `open` from re-running a flatten that already happened.
Run without it — by hand, or with `orders.flatten_before_entry: true` and no step 0b —
and `open` is self-contained: it cancels, closes, waits for flat, then enters.

Two smaller things the flatten brings:

- Selling a name at market and buying it back the same day is a **day trade**. Under $25k of equity, FINRA allows three in five business days
  before the account is restricted. It only happens when a name is in the book two
  days running; `open` prints a warning naming the symbols when it does.
- Waiting for flat is not optional. An open opposing order in a symbol that is also in
  today's book gets the entry rejected as a potential wash trade.

`--no-flatten` keeps the existing positions. `flatten` on its own is the panic button:
it cancels and closes everything, at market, now.

## Invocations

The stage E session runs these itself, at the two moments in the table above. By hand,
on the entry date and while the US session is open:

```bash
python3 scripts/alpaca_trade.py flatten --submit                                  # step 0b
python3 scripts/alpaca_trade.py plan --run research/2026/09/2026-09-09/edge        # step 7
python3 scripts/alpaca_trade.py open --run research/2026/09/2026-09-09/edge --submit --no-flatten

# any time
python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'
```

`flatten --submit` on its own is also the panic button: everything out, at market, now.

Entry dates come off the window `edge_resolve.py` scores, so the traded return and the
measured return share an entry:

| print | entry | measured exit | what the flatten does instead |
| --- | --- | --- | --- |
| `amc` on day D | close of D | close of D+1 | sells the morning of D+1 |
| `bmo` on day D | close of D−1 | close of D | sells the morning of D |

Every name in one run enters at the same close — the run's own date.

`close` is still there for the measured exit, and it is what to use if the
flatten-at-open exit ever looks like it is costing more than the operational
simplicity is worth. Set `orders.flatten_before_entry: false` and run it on the exit
date, before the same cutoff:

```bash
python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit
```

It walks every run with an `alpaca-orders.json`, closes only the legs whose
`exit_date` is today, and reads the real position quantity from Alpaca so a partial
fill still closes flat.

To run it unattended, no new Routine is needed — the two steps are in stage E's own
prompt, `docs/routine-prompts/edge-hunt.md`, which has to be pasted into
`trig_01CvGQJWoKeNLXWCxiffM3ED` by hand because `update_trigger` refuses any Routine an
agent did not create. Keep that file in step with the Routine, because nothing else
will.

## The exit the two sessions actually want

The shipped path gives the whole book one exit: `flatten` sells everything at market at
the start of the next run. `scripts/edge_exit.py` re-priced all 38 de-duplicated events
at eight exit horizons and at every hour of the clock, and the two sessions turn out to
want opposite things. Per trade, on the conviction book:

| | opening auction | closing auction |
| --- | --- | --- |
| **amc** (12 trades) | **+8.91%** (t=3.20) | +5.23% (t=1.48) |
| **bmo** (10 trades) | +2.96% (t=1.01) | **+6.48%** (t=2.34) |
| combined, split by session | **+7.81%** (t=4.01) | +5.80% for one uniform close |

An amc print gets a whole overnight of processing, so the opening auction is already the
informed price and the session that follows takes about three points back off the book:
the open-to-close leg ranks at ρ=−0.351 and pays −2.61% day-demeaned, on a book that is
six long and six short, so it is not market drift. A bmo print gets two thin hours of
pre-market instead and goes on repricing all day: ρ +0.187 at the open against +0.670 at
the close.

`orders.exit_mode` turns that into the exit instrument, and there are **three** schemes
rather than two, because what a single 16:04-Amsterdam Routine can reach is not what the
measurement wants. Per trade on the same 22 trades:

| mode | amc | bmo | per trade | what it needs |
| --- | --- | --- | --- | --- |
| `uniform` *(ships)* | market ~10:00 ET | market ~10:00 ET | +4.49% (t=2.52) | nothing; it is the flatten |
| `bmo_close` | market ~10:00 ET | today's close (`cls`) | **+6.27%** (t=3.34) | `flatten_before_entry: false` |
| `auction_split` | opening auction (`opg`) | today's close (`cls`) | **+7.81%** (t=4.01) | that, plus a second Routine |

**Do `bmo_close` first.** It is +1.77pp of the +3.32pp on offer and it needs no machinery
that does not already exist: the amc leg is the plain market sell the flatten was already
doing, and the bmo leg goes into a closing auction Alpaca accepts until 15:50 ET, hours
after a 16:04 Amsterdam start. The whole gap between it and `auction_split` is the amc
leg, worth +1.54pp, and that leg costs a second daily firing.

**Three things stand between any of it and being right**, whichever mode:

1. **It was read off the events it is justified by.** The paired day bootstrap puts the
   split's gain at +1.87pp per trade with a 95% interval of [-1.30, +4.55], and the best
   of six candidate rules beats a uniform close in 91% of resamples. That describes the
   sample; it does not test the rule.
2. **It does not replicate yet.** On 09-08 and 09-09 - 30 names, 14 above the floor,
   neither day in the fitted sample - every exit hour available on both days paid between
   -1.42% and -0.05% per trade. On 09-09 shorting the day blind paid +3.9% to +4.5% while
   the book paid -0.2% to -0.9%.
3. **The other 37 events in this repo disagree.** `backtest/RESULTS.md` prices its sealed
   corpus at both exits and all three arms did better at the **close** (+2.16% against
   +0.90% per trade for arm A). Re-pricing those 37 on `edge_exit.py`'s hourly grid is
   the cheapest way to settle it and has not been done.

### What it needs operationally, if it is ever switched on

- **`flatten_before_entry: false`.** A flatten at the start of the run sells the amc names
  hours before their opening auction arrives, so the two settings cancel out.
- **A second run a day, for `auction_split` only.** Alpaca *rejects* rather than queues
  `opg` between 09:28 and 19:00 ET, so the amc leg cannot be placed by the run that placed
  the entries. It has to go in during the pre-market of the exit date; 14:00 Amsterdam is
  08:00 ET and works. `auction_window()` refuses rather than sending an order that will
  bounce. The prompt is in `docs/routine-prompts/edge-execute.md` and **only a person can
  create that Routine** - `create_trigger` is refused to agent sessions in this
  environment, confirmed on 2026-09-10. `bmo_close` needs none of this.
- **Nothing that can leave a position unsold.** `close` treats an exit date already in the
  past as overdue and sends it at plain market immediately, and `open` refuses to enter a
  new book while any position is overdue with no exit submitted. That is the guarantee
  `flatten_before_entry` used to provide by sweeping; once the flatten is off it has to
  come from checking.
- **Nothing about capital recycling.** Closing amc in the opening auction frees the cash
  at 09:30 rather than 16:00, and with one auction entry a day that is **not** extra
  return: the capital slot is 24 hours either way. `capital_table` in `edge_exit.py`
  prints return per slot-day equal to return per trade to make that hard to misread —
  dividing by hours *held* instead is how a 16:30 exit reads as 206% per capital-day,
  which is a denominator artefact. What it does buy is settled cash before the auction
  that funds the next book, so sizing stops depending on unfilled proceeds, and 6.5 fewer
  hours of market exposure at a higher per-trade number.

## What it refuses to do

Every refusal is recorded with its reason, in the plan or in `alpaca-orders.json`:

- send anything without `enabled: true` **and** `--submit`
- touch a live endpoint without `--live-account-i-understand`
- place an entry on a day that is not the planned entry date (`--force-date` overrides,
  and a forced fill is no longer the price the measurement uses)
- send any entry outside the open session — and, when `orders.entry` is set back to
  `market_on_close`, inside Alpaca's cutoff (`--allow-market-fallback` downgrades that
  one to a plain market order)
- short a name Alpaca does not call shortable
- size a position above 20% of equity or 1% of the name's 20-day dollar volume
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
