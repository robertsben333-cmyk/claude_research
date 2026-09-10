# Routine prompts — placing and closing stage E's book

Two Routines, both fresh-session-per-fire, both weekdays. Neither exists yet: create
them only when `execution.enabled` is `true` in `config/pipeline.yaml` and the paper
account has been watched for a while. Stage E's own Routine
(`trig_01CvGQJWoKeNLXWCxiffM3ED`) is **not** changed by any of this — it has to be
pasted in by hand and one hand-pasted prompt is already enough to keep in step.

Times are Amsterdam. The binding constraint is Alpaca's MOC cutoff, ten minutes
before the US close: 21:50 in Amsterdam standard time, 21:50 CEST while the US and
Europe are both on summer time, and earlier on US half-days. Both Routines are set an
hour ahead of that so a slow session still lands inside the window.

## 1. Entry — `20:45` Amsterdam, weekdays (cron `45 18 * * 1-5` in UTC)

Stage E fires at 16:04 and normally has `edge-scores.json` on `main` within the hour,
so this is four hours behind it, not racing it.

```
Place stage E's book for today at Alpaca.

Resolve today's run directory with `python3 scripts/run_paths.py --json` and work in
`<run_dir>/edge`.

1. If `edge-scores.json` is not there, stop. Append a line to the run log saying the
   edge hunt did not publish and no book was placed, publish it, and end. Do not
   improvise a ranking.
2. `python3 scripts/alpaca_trade.py plan --run <run_dir>/edge` and read the output.
   If it warns that the entry close has passed, stop and record that instead — a
   forced fill is not the price the measurement uses.
3. `python3 scripts/alpaca_trade.py open --run <run_dir>/edge --submit`
4. Append the result to the run log with `scripts/run_log.py`: how many names met the
   benchmark, how many orders went in, and every name that was refused with its
   reason. Then `scripts/publish.sh "stage E: book placed for <date>"`.

Do not change the benchmark, the sizing or the config. If a leg is refused, record
the reason and leave it refused. Everything the script does is in docs/EXECUTION.md.
```

## 2. Exit — `20:45` Amsterdam, weekdays (cron `45 18 * * 1-5` in UTC)

Same firing time as the entry Routine, and deliberately so: on any given day the
positions being closed were entered the previous session, and both legs belong at the
close. Run the exit first if the two ever have to be sequenced by hand.

```
Close whatever of stage E's book is due today at Alpaca.

1. `python3 scripts/alpaca_trade.py close --scan 'research/*/*/*/edge' --submit`
   It closes only the legs whose exit date is today and reads the real position
   quantity from the account, so a partial fill still closes flat.
2. `python3 scripts/alpaca_trade.py status --scan 'research/*/*/*/edge'`
3. If anything is still open whose exit date is in the past, close it now:
   `--all --now` sends plain market orders. Record that you did.
4. Append what closed, and at what fill, to today's run log and publish.

If the account is unreachable, say so in the run log and publish that — an open
position nobody recorded is the one failure this whole file exists to prevent.
```

## Why two Routines and not one session

The entry and the exit are a day apart and each has to land before a cutoff. A single
session that tried to hold both would have to survive overnight in an ephemeral
container, which is exactly the failure mode `CLAUDE.md` opens with. Two independent
firings, each idempotent on its `client_order_id`, recover from a killed session by
being run again.
