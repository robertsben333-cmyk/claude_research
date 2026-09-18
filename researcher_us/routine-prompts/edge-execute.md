# Execution rides in stage E's Routine, with one exception

**As shipped there is no separate execution Routine, and none is needed.** Trading is two
steps inside stage E's own Routine and its own session: step 0b sells yesterday's book
before the hunt starts, step 7 buys today's after the note is published. Both live in
`researcher_us/routine-prompts/edge-hunt.md`, which is the file to keep in step with
`trig_01CvGQJWoKeNLXWCxiffM3ED`, and in `.claude/skills/earnings-edge-hunt/SKILL.md`.

**The exception is any mode that aims the amc leg at the OPEN** — `auction_split` and,
since 2026-09-15, `amc_open`. An exit at the open has to be submitted before the open, and
stage E's own Routine fires at 13:04 ET. So it needs a second Routine in the European
morning, and that Routine has to exist *before* the mode goes on. The prompt is below.

**`orders.exit_mode: bmo_close` needs no second Routine at all**, and it is where most of
the money is: amc at market on the run (+6.08% a trade) and bmo into today's closing
auction (+6.48%), which is +6.27% on the book against +4.49% for the flatten. The extra
step from there to `auction_split` is +1.54pp and costs this whole second firing. Do
`bmo_close` first.

This file used to say flatly that a second Routine should never exist; that was written
before the per-session exit and is corrected here rather than left to mislead.

Why one Routine and not two, while the mode is `uniform`:

- A second firing a day is a second thing that can fail silently, each with its own
  market-on-close deadline.
- The flatten has to happen **before** a session that might die, not after. A killed
  session then leaves the account in cash rather than holding a book nobody is managing.
- Nothing has to be handed between two sessions, so there is no state to lose.

What it costs, and it is worth restating wherever this is described: selling half an
hour into the session is nearer the next **open** (ρ=+0.331, p=0.046) than the next
**close** (ρ=+0.514, p=0.0015), which is the exit every number in
`researcher_us/EDGE_ANALYSIS.md` was measured at.

## Three things still have to be true

1. **`researcher_us/scripts/alpaca_trade.py` is on `main`.** Done on 2026-09-10: a Routine clones the
   default branch, the 2026-09-10 run found no script because the code was still on
   `claude/alpaca-auto-orders-integration-y397gh`, and that branch was merged. Nothing
   left to do here; the two below are still open.
2. **The credentials are on the environment**, not in a shell: `ALPACA_API_KEY_ID`,
   `ALPACA_API_SECRET_KEY` and `ALPACA_BASE_URL=https://paper-api.alpaca.markets`, in
   `.env` format. `researcher_us/EXECUTION.md` step 3 has the walkthrough.
3. **`execution.enabled` is `true`** in `config/pipeline.yaml`, on `main`. Done on
   2026-09-10, by the operator, for the paper account. From 2026-09-11 the scheduled
   14:04 fire flattens the previous book and places a new one with nobody watching.
   Setting it back to `false` is the only thing that stops that.

## The second Routine, required by any mode that sends amc to the opening auction

Two modes do: `auction_split` and **`amc_open`, which is what ships since 2026-09-15**.
Both get amc names out at the open, because that is where an amc print was measured to
pay (`researcher_us/EXECUTION.md`, "The exit the two sessions actually want"). They differ only
in the bmo leg — `auction_split` sends it to that day's closing auction, `amc_open` sells
it at plain market on stage E's own run, so the position is certainly gone before the
same afternoon buys the next book.

Either **needs this Routine to exist**, for a reason that is not negotiable: the order
has to be in before 09:30 ET, and stage E's own session fires at 13:04 ET. It held when the
instrument was an `opg` auction order, which Alpaca rejects outright between 09:28 and
19:00 ET, and it still holds now that it is a market DAY order queued in the pre-market —
one submitted at 13:04 ET is simply a market order in the middle of the session, which is
a different exit from the one the mode asked for.

So there are two runners (times as they actually are, checked against `list_triggers`):

| Amsterdam | ET | who | what |
| --- | --- | --- | --- |
| 12:00 | 06:00 | **this Routine** (`0 10 * * 1-5`) | amc legs due today, aimed at the open |
| 19:04 | 13:04 | stage E, step 0b | bmo legs due today, plus anything overdue, at market |

**Guard on the placement, not on the mode name and not on the literal instrument.**
This Routine's whole purpose is to place the exit that has to go in *before the open*;
which mode asked for it, and which order type carries it, are not its business. A guard
naming `auction_split` broke silently the day `amc_open` shipped. Since 2026-09-18 the
instrument is a plain market DAY order queued in the pre-market rather than an `opg`
auction order — `opg` and `cls` turned out to be Elite Smart Router order types this
account does not have, and nine of ten of them expired unfilled — and
`mode --require-exit-tif opg` still exits 0, because it asks the placement question.
**Do not "fix" that guard to match the new tif.** A session cannot edit a Routine, so a
guard that failed shut would report a tidy no-op every morning while the amc legs went
unsold.

Set the mode **and** `orders.flatten_before_entry: false`
together. Either alone is wrong: the flatten on its own sells the amc names before their
auction, and the mode on its own leaves the flatten selling everything anyway. Since
2026-09-10 that is **refused rather than documented**: `exit_mode()` raises on any
non-uniform mode while `flatten_before_entry` is true, so the half-set config fails loudly
on the next `open`, `close` or `mode` instead of running the wrong exit quietly.

**What happens if this Routine never fires.** The amc positions stay open past their exit
date. The next stage E run then finds them: `close` sends anything overdue at plain market
immediately, and `open` **refuses to enter a new book** while a position is past its exit
date with no exit submitted (`--allow-stale` overrides, and stacks a second book on the
first). So a missed firing costs the measured exit and one loud refusal; it does not
quietly accumulate a book nobody is managing. That refusal is the whole reason the guard
exists.

```
Close stage E's amc positions at today's open.

You fire at 10:00 UTC, which is 06:00 New York in summer and 05:00 in winter. Re-read
the clock with `date -u` rather than trusting this line. Either way you are in Alpaca's
pre-market, which is the only reason this Routine exists as a separate firing: an exit
aimed at the open has to be submitted before the open, and stage E's own run fires at
13:04 ET, hours after it.

0. Clone the repo on main, as researcher_us/routine-prompts/edge-hunt.md step 0 describes, and
   verify researcher_us/scripts/alpaca_trade.py exists. If it does not you are on the wrong branch:
   stop and say so.

1. ASK THE CODE, DO NOT READ THE CONFIG BY EYE:
   `python3 researcher_us/scripts/alpaca_trade.py mode --require-exit-tif opg`
   It prints the effective settings and exits 0 only when execution is enabled AND some
   session's exit is aimed at the OPEN — which is the one thing this Routine exists to
   place, because only a pre-market firing can. On a non-zero exit, do nothing further,
   paste its output into your one-line report, and stop.

   It may print `matched on placement, not on the literal tif`. That is correct and
   expected: since 2026-09-18 the amc exit goes as a plain market DAY order queued in
   the pre-market, not as an `opg` auction order. Leave the command as written.

   GUARD ON THE PLACEMENT, NOT ON A MODE NAME. The previous version of this line said
   `--require auction_split`, and it broke silently on 2026-09-15 when `amc_open`
   shipped: the guard failed, this Routine reported a tidy no-op every morning, and the
   amc legs it exists to sell never left at the open. Two modes now aim amc at the open
   and more may follow, and the instrument that carries it has already changed once.

   Do not substitute your own reading of `config/pipeline.yaml` for this command.
   The guard used to be "if `orders.exit_mode` is not `auction_split`, do nothing",
   read by eye out of a YAML file whose keys have already been renamed once — and a
   key read by eye fails in both directions. A key that has been renamed away looks
   like a guard that can never pass, so the Routine reports a tidy no-op every
   morning and the mode never takes effect. A key that is simply absent looks like a
   guard that was clearly meant to be satisfied, and then `close --submit` puts `cls`
   orders in at 06:00 ET that stage E's own flatten cancels four hours later. The
   exit status has neither failure mode.

2. `python3 researcher_us/scripts/alpaca_trade.py verify --scan 'research/*/*/*/edge' --fix --submit`
   FIRST, and read it. A submitted sell is not a sold position: nine of the first ten
   auction exits part-filled or filled nothing and then expired — HOFT 17 of 161, CODA
   39 of 183, RLGT 0 of 224, LEN 0 of 28. Any leg it marks UNFILLED is one nothing will
   sell on its own. `--fix` re-sends the residual at plain market, sized to what Alpaca
   reports is still held; from the pre-market that order is accepted and queued for the
   open rather than refused, so the rescue now works here instead of waiting for stage
   E's run seven hours later. Name every UNFILLED leg and every rescue in your report.

   A leg reported `working` with `queued while the market is closed` is fine — that is
   the ordinary state of a pre-market order and nothing is re-sent for it.

3. `python3 researcher_us/scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
   It closes only legs whose exit date is today, reads the real position quantity from
   the account so a partial fill still closes flat, and picks the instrument per
   session from the configured placement. Under `amc_open` with auction orders off that
   is a market DAY order for the amc legs, which Alpaca queues and routes at the open.

   IT WILL LEAVE SOME LEGS ALONE, AND THAT IS THE POINT. A leg whose placement is
   `market` — the bmo leg under `amc_open` — belongs to the run that fires INSIDE the
   session, not to you: a market order sent from the pre-market is queued for the open,
   and bmo measured worst at the open of the three exits it was priced at. Since
   2026-09-18 `close` refuses those with "market placement, and the market is closed".
   Report the refusal; it is correct, not a failure. An OVERDUE leg is exempt and still
   goes immediately.

4. `python3 researcher_us/scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`

5. Append to today's run log and publish: which legs were sent, with which
   time_in_force, and every refusal with its reason. Publish even when nothing was
   placed. If the account is unreachable, say so in the run log and publish that — an
   open position nobody recorded is the failure this step exists to prevent.

An order queued before the open does not fill until the session starts, so do not wait
for a fill price here. Stage E's own run reads it back later.
```

### When it has to run: `0 12 * * 1-5`

**One cron, all year, and deliberately not an Amsterdam wall-clock time.** Cron is
evaluated in UTC, so a Routine pinned to a New York hour needs editing twice a year and
this repo has already lost runs to that trap. `0 12 * * 1-5` needs editing never:

| | 12:00 UTC in ET | Amsterdam | slack before the 09:28 cutoff |
| --- | --- | --- | --- |
| summer (EDT) | 08:00 | 14:00 | 88 min |
| winter (EST) | 07:00 | 13:00 | 148 min |

Both sit inside the window and neither is close to an edge, so the drift between the two
regimes costs nothing.

**The window is narrower than it looks, and the reason is the date.** A queued order
could in principle go in the evening before — but `close` selects legs whose `exit_date`
equals *today* off Alpaca's own clock, and at 20:00 ET the clock date is still the day
before the exit date. Such a run would select nothing and report success. So the usable
window is **00:00 ET to 09:30 ET on the exit date itself**, which is 05:00/06:00 to
15:30 Amsterdam. (It was 09:28 ET while the instrument was `opg`, the cutoff after which
Alpaca rejects one; a queued market order has until the open itself. Do not spend that
margin — the cron below keeps the old slack.)

Within that, later means less time to notice a failure and earlier means no benefit: an
order queued for the open does not care about pre-market liquidity either. There is no
automatic retry, so the slack is the whole argument: 12:00 UTC leaves an hour and a
half.

One side effect worth knowing: at 07:00–08:00 ET the `cls` window is open too, so this
firing can take the bmo legs due today as well. With this Routine in place,
`auction_split` is fully handled here and stage E's own run has nothing left to sell.

An agent session cannot create this Routine: `create_trigger` is refused by the
permission layer in this environment, confirmed 2026-09-10. A person has to make it at
claude.ai/code and record the id here and in `docs/ROUTINES.md`.

## The older fallback: one exit Routine in the evening


Worth adding only if the step-0b exit turns out to cost more than the single-Routine
simplicity is worth. Set `orders.flatten_before_entry: false`, drop step 0b from the
stage E prompt, and schedule this as its own weekday Routine at 20:45 Amsterdam
(cron `45 18 * * 1-5` in summer, `45 19 * * 1-5` in winter — cron is evaluated in UTC
and this repo has lost runs to that trap once). That puts the exit at the measured
close instead of the morning after.

```
Close whatever of stage E's book is due today at Alpaca.

1. `python3 researcher_us/scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
   It closes only the legs whose exit date is today and reads the real position
   quantity from the account, so a partial fill still closes flat. It then waits
   `orders.fill_check_seconds` and re-reads the exits it sent.
2. `python3 researcher_us/scripts/alpaca_trade.py verify --scan 'research/*/*/*/edge' --fix --submit`
   then `python3 researcher_us/scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`
3. If anything is still open whose exit date is in the past, close it now:
   `flatten --submit` sends plain market orders. Record that you did.
4. Append what closed, and at what fill, to today's run log and publish.

If the account is unreachable, say so in the run log and publish that. An open
position nobody recorded is the failure this step exists to prevent.
```

An agent session cannot create that Routine either: `create_trigger` is refused by the
permission layer in this environment, so a person has to make it at claude.ai/code and
record the id here and in `docs/ROUTINES.md`.
