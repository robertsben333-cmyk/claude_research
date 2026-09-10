# Routine prompt — placing stage E's book

One Routine, fresh session per fire, weekdays. It does not exist yet: create it only
when `execution.enabled` is `true` in `config/pipeline.yaml` and the paper account has
been watched by hand for a few days. Stage E's own Routine
(`trig_01CvGQJWoKeNLXWCxiffM3ED`) is **not** changed by any of this — it has to be
pasted in by hand and one hand-pasted prompt is already enough to keep in step.

One Routine is enough because `open` flattens before it enters: it sells whatever is
still in the account, then places today's book. There is no second invocation to
schedule and no overnight order to babysit. See `docs/EXECUTION.md`, "The daily run
flattens first", for what that costs against the measured exit.

## Entry — `20:45` Amsterdam, weekdays (cron `45 18 * * 1-5` in UTC)

Stage E fires at 16:04 and normally has `edge-scores.json` on `main` within the hour,
so this is four hours behind it, not racing it. The binding constraint at the other
end is Alpaca's MOC cutoff, ten minutes before the US close: 21:50 Amsterdam while
both sides are on summer time, earlier on US half-days. 20:45 leaves an hour for a
slow session.

```
Place stage E's book for today at Alpaca.

Resolve today's run directory with `python3 scripts/run_paths.py --json` and work in
`<run_dir>/edge`.

1. If `edge-scores.json` is not there, stop. Append a line to the run log saying the
   edge hunt did not publish and no book was placed, publish it, and end. Do not
   improvise a ranking, and do not flatten the account either: leaving yesterday's
   book open one more session is a smaller error than selling it on no information.
2. `python3 scripts/alpaca_trade.py plan --run <run_dir>/edge` and read the output.
   If it warns that the entry close has passed, stop and record that instead. A
   forced fill is not the price the measurement uses.
3. `python3 scripts/alpaca_trade.py open --run <run_dir>/edge --submit`
   This sells every existing position at market first, waits for flat, then places
   the new book market-on-close.
4. `python3 scripts/alpaca_trade.py status --run <run_dir>/edge`
5. Append to the run log with `scripts/run_log.py`: what was sold and at what P&L,
   how many names met the benchmark, how many orders went in, the gross as a
   percentage of equity, and every name that was refused with its reason. Then
   `scripts/publish.sh "stage E: book placed for <date>"`.

Do not change the benchmark, the sizing or the config. Do not size a name by its
score -- the book is equal weight by design. If a leg is refused, record the reason
and leave it refused. If the flatten reports it is still holding something, say so in
the run log: an entry in that same name will have been rejected as a wash trade.
Everything the script does is in docs/EXECUTION.md.
```

## Why not two Routines

An earlier version of this file scheduled a second Routine to close the book
market-on-close on the exit date, which is the window `edge_resolve.py` measures. That
is still the better exit on the evidence (ρ=+0.514, p=0.0015 to the next close against
ρ=+0.331, p=0.046 to the next open), and `scripts/alpaca_trade.py close` still does
it. It was dropped because two firings a day, each with its own cutoff, is two things
that can fail silently, and because the account is meant to be rebuilt from scratch
daily anyway. If the flatten exit turns out to cost more than that convenience,
set `orders.flatten_before_entry: false` and add the second Routine back:

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
