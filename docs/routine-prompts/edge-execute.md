# Routine prompt — placing stage E's book

One Routine, fresh session per fire, weekdays. **It does not exist yet.** An agent
session cannot create it: `create_trigger` is refused by the permission layer in this
environment, so this file is the copy-paste source and a person has to make the
Routine at claude.ai/code.

Stage E's own Routine (`trig_01CvGQJWoKeNLXWCxiffM3ED`) is **not** changed by any of
this. Its prompt has to be pasted by hand too, and one hand-pasted file is already
enough to keep in step.

One Routine is enough because `open` flattens before it enters: it sells whatever is
still in the account, then places today's book. There is no second invocation to
schedule and no overnight order to babysit. See `docs/EXECUTION.md`, "The daily run
flattens first", for what that costs against the measured exit.

## Three things have to be true first

1. **The code is on `main`.** A Routine clones the default branch, and
   `scripts/alpaca_trade.py` arrived on `claude/alpaca-auto-orders-integration-y397gh`.
   Until that branch is merged, the Routine fires into a checkout with no script. The
   prompt below handles that case by logging it and stopping, so creating the Routine
   early is harmless, but it will do nothing useful.
2. **The credentials are on the environment**, not in a shell.
   `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY` and
   `ALPACA_BASE_URL=https://paper-api.alpaca.markets`, in `.env` format, on the
   environment the Routine uses. `docs/EXECUTION.md` step 3 has the walkthrough.
3. **`execution.enabled` is `true`** in `config/pipeline.yaml`, on `main`. While it is
   `false` the Routine runs end to end and submits nothing, which is the sensible way
   to watch it for a few days before it touches the account.

Leave 3 for last. 1 and 2 alone give a Routine that produces a daily plan and a run-log
entry and places no orders.

## The Routine

Fresh session per fire (**not** bound to a session — every firing starts from nothing).
Weekdays. Push notification on, so a day that places orders says so.

**Cron `45 18 * * 1-5`** — 20:45 Amsterdam while Europe and the US are both on summer
time. In winter it is `45 19 * * 1-5`. Cron is evaluated in UTC and this repo has
already lost runs to that trap once; see `docs/ROUTINES.md`, "The DST trap this
document already warned about".

Why 20:45. Stage E fires at 16:04 and normally has `edge-scores.json` on `main` within
the hour, so this is four hours behind it, not racing it. The constraint at the other
end is Alpaca's market-on-close cutoff, ten minutes before the US close — 21:50
Amsterdam, earlier on US half-days. 20:45 leaves an hour for a slow session.

Paste this as the prompt, verbatim:

```
Place today's stage E book at Alpaca. Read CLAUDE.md and docs/EXECUTION.md before
doing anything. Everything below is in docs/EXECUTION.md; this prompt only names the
order of the steps.

You are a fresh session in the claude_research repo. Work on `main`. Do not improvise
a ranking, do not change the benchmark, the sizing or the config, and do not size a
name by its score — the book is equal weight by design.

1. Resolve today's paths: `python3 scripts/run_paths.py --json`. The edge run is
   `<run_dir>/edge`.

2. If `scripts/alpaca_trade.py` does not exist on this checkout, stop. The execution
   branch has not been merged. Append that to the run log with `scripts/run_log.py`,
   publish it with `scripts/publish.sh`, and end.

3. If `<run_dir>/edge/edge-scores.json` does not exist, stop. The edge hunt did not
   publish today. Append that to the run log, publish, and end. Do NOT flatten the
   account in this case: leaving yesterday's book open one more session is a smaller
   error than selling it on no information.

4. `python3 scripts/alpaca_trade.py plan --run <run_dir>/edge`

   Read the output. If it warns that the entry close has already passed, stop there
   and record that instead — a forced fill is not the price the measurement uses. If
   it warns about buying power or about shorting being disabled, record that too.

5. `python3 scripts/alpaca_trade.py open --run <run_dir>/edge --submit`

   This sells every existing position at market first, waits until the account is
   flat, then places today's book market-on-close. If `execution.enabled` is still
   `false` in config/pipeline.yaml the same command is a dry run that submits nothing
   — that is expected, it is not a failure, say so in the run log and continue.

6. `python3 scripts/alpaca_trade.py status --run <run_dir>/edge`

7. Append a section to the run log with `scripts/run_log.py` and publish it with
   `scripts/publish.sh "stage E: book placed for <YYYY-MM-DD>"`. Record at least:
   whether execution was enabled or this was a dry run; what was sold and at what
   unrealised P&L; how many names met the benchmark and how many orders were
   accepted; the gross as a percentage of equity; every name that was refused and
   why; and any warning the plan printed.

Publish even when nothing was placed. An open position nobody recorded is the failure
this whole step exists to prevent.

If the flatten reports it is still holding something, say so explicitly in the run
log: an entry in that same name will have been rejected by Alpaca as a potential wash
trade, and that leg is missing from the book.

This is a forecasting exercise on public information, not investment advice.
```

Record the Routine's id here and in `docs/ROUTINES.md` once it exists, because nothing
else will keep those two in step.

## Why not two Routines

An earlier version of this file scheduled a second Routine to close the book
market-on-close on the exit date, which is the window `edge_resolve.py` measures. That
is still the better exit on the evidence (ρ=+0.514, p=0.0015 to the next close against
ρ=+0.331, p=0.046 to the next open), and `scripts/alpaca_trade.py close` still does it.
It was dropped because two firings a day, each with its own cutoff, is two things that
can fail silently, and because the account is meant to be rebuilt from scratch daily
anyway. If the flatten exit turns out to cost more than that convenience, set
`orders.flatten_before_entry: false` and add the second Routine back:

```
Close whatever of stage E's book is due today at Alpaca.

1. `python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
2. `python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`
3. If anything is still open whose exit date is in the past, close it now with
   `flatten --submit`. Record that you did.
4. Append what closed, and at what fill, to today's run log and publish.
```

Either way, an open position nobody recorded is the one failure this file exists to
prevent. If the account is unreachable, say so in the run log and publish that.
