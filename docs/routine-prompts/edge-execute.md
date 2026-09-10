# Execution rides in stage E's Routine — this file is the fallback

**There is no separate execution Routine, and there should not be one.** Trading is two
steps inside stage E's own Routine and its own session: step 0b sells yesterday's book
before the hunt starts, step 7 buys today's after the note is published. Both live in
`docs/routine-prompts/edge-hunt.md`, which is the file to keep in step with
`trig_01CvGQJWoKeNLXWCxiffM3ED`, and in `.claude/skills/earnings-edge-hunt/SKILL.md`.

Why one Routine and not two:

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

## The fallback: a separate exit Routine

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
