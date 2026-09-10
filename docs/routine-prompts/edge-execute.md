# Execution rides in stage E's Routine, with one exception

**As shipped there is no separate execution Routine, and none is needed.** Trading is two
steps inside stage E's own Routine and its own session: step 0b sells yesterday's book
before the hunt starts, step 7 buys today's after the note is published. Both live in
`docs/routine-prompts/edge-hunt.md`, which is the file to keep in step with
`trig_01CvGQJWoKeNLXWCxiffM3ED`, and in `.claude/skills/earnings-edge-hunt/SKILL.md`.

**The exception is `orders.exit_mode: auction_split`.** That mode sends amc positions into
the opening auction, and Alpaca rejects an `opg` order between 09:28 and 19:00 ET, so
nothing firing in the European afternoon can place one. It needs a second Routine at 14:00
Amsterdam and that Routine has to exist *before* the mode goes on. The prompt is below.

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
`docs/EDGE_ANALYSIS.md` was measured at.

## Three things still have to be true

1. **`scripts/alpaca_trade.py` is on `main`.** Done on 2026-09-10: a Routine clones the
   default branch, the 2026-09-10 run found no script because the code was still on
   `claude/alpaca-auto-orders-integration-y397gh`, and that branch was merged. Nothing
   left to do here; the two below are still open.
2. **The credentials are on the environment**, not in a shell: `ALPACA_API_KEY_ID`,
   `ALPACA_API_SECRET_KEY` and `ALPACA_BASE_URL=https://paper-api.alpaca.markets`, in
   `.env` format. `docs/EXECUTION.md` step 3 has the walkthrough.
3. **`execution.enabled` is `true`** in `config/pipeline.yaml`, on `main`.

Leave 3 for last. With 1 and 2 alone the stage runs its hunt exactly as before and both
trading steps are silent.

## The second Routine, required only for `exit_mode: auction_split`

`orders.exit_mode: auction_split` gives amc names the opening auction and bmo names the
closing auction, because the two were measured to want opposite exits (`docs/EXECUTION.md`, "The
exit the two sessions actually want"). The mode is off, and turning it on **needs this
Routine to exist first**, for a reason that is not negotiable: Alpaca *rejects* rather than queues
an `opg` order between 09:28 and 19:00 ET, so the amc leg cannot be placed by a Routine
that fires at 16:04 Amsterdam. Nothing in the stage E session can sell an amc position
into its own opening auction.

The split therefore needs two runners:

| Amsterdam | ET | who | what |
| --- | --- | --- | --- |
| 14:00 | 08:00 | **this Routine** | amc legs due today, into the opening auction (`opg`) |
| 16:04 | 10:04 | stage E, step 0b | bmo legs due today (`cls`), plus anything overdue at market |

Set `orders.exit_mode: auction_split` **and** `orders.flatten_before_entry: false`
together. Either alone is wrong: the flatten on its own sells the amc names before their
auction, and the mode on its own leaves the flatten selling everything anyway.

**What happens if this Routine never fires.** The amc positions stay open past their exit
date. The next stage E run then finds them: `close` sends anything overdue at plain market
immediately, and `open` **refuses to enter a new book** while a position is past its exit
date with no exit submitted (`--allow-stale` overrides, and stacks a second book on the
first). So a missed firing costs the measured exit and one loud refusal; it does not
quietly accumulate a book nobody is managing. That refusal is the whole reason the guard
exists.

```
Close stage E's amc positions in today's opening auction.

You fire at 08:00 New York, which is inside Alpaca's pre-market and BEFORE the 09:28
cutoff after which `opg` orders are rejected rather than queued. That timing is the
only reason this Routine exists as a separate firing.

0. Clone the repo on main, as docs/routine-prompts/edge-hunt.md step 0 describes, and
   verify scripts/alpaca_trade.py exists. If it does not you are on the wrong branch:
   stop and say so.

1. If `execution.enabled` is false in config/pipeline.yaml, or
   `orders.exit_mode` is not `auction_split`, do nothing and say so in one line. As
   shipped `enabled` is false and the mode is `uniform`.

2. `python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
   It closes only legs whose exit date is today, reads the real position quantity from
   the account so a partial fill still closes flat, and picks the instrument per
   session: amc into the opening auction, bmo into the closing auction. At 08:00 ET the
   `cls` window is open too, so a bmo leg due today may go in here rather than waiting
   for stage E. That is fine and not a double-send: exits are keyed by a deterministic
   client_order_id and an already-submitted leg is skipped.

3. `python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`

4. Append to today's run log and publish: which legs were sent, with which
   time_in_force, and every refusal with its reason. Publish even when nothing was
   placed. If the account is unreachable, say so in the run log and publish that — an
   open position nobody recorded is the failure this step exists to prevent.

An order sent into an auction does not fill until that auction runs, so do not wait
for a fill price here. Stage E's own run reads it back later.
```

An agent session cannot create this Routine: `create_trigger` is refused by the
permission layer in this environment, so a person has to make it at claude.ai/code and
record the id here and in `docs/ROUTINES.md`. Cron is evaluated in UTC — 08:00 New York
is `0 12 * * 1-5` in summer and `0 13 * * 1-5` in winter, and this repo has lost runs to
that trap once.

## The older fallback: one exit Routine in the evening


Worth adding only if the step-0b exit turns out to cost more than the single-Routine
simplicity is worth. Set `orders.flatten_before_entry: false`, drop step 0b from the
stage E prompt, and schedule this as its own weekday Routine at 20:45 Amsterdam
(cron `45 18 * * 1-5` in summer, `45 19 * * 1-5` in winter — cron is evaluated in UTC
and this repo has lost runs to that trap once). That puts the exit at the measured
close instead of the morning after.

```
Close whatever of stage E's book is due today at Alpaca.

1. `python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
   It closes only the legs whose exit date is today and reads the real position
   quantity from the account, so a partial fill still closes flat.
2. `python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`
3. If anything is still open whose exit date is in the past, close it now:
   `flatten --submit` sends plain market orders. Record that you did.
4. Append what closed, and at what fill, to today's run log and publish.

If the account is unreachable, say so in the run log and publish that. An open
position nobody recorded is the failure this step exists to prevent.
```

An agent session cannot create that Routine either: `create_trigger` is refused by the
permission layer in this environment, so a person has to make it at claude.ai/code and
record the id here and in `docs/ROUTINES.md`.
