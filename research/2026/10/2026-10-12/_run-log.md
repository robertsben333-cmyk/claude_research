# Run log — 2026-10-12

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-11 06:41 UTC
- Fired Sun 2026-10-11 06:40 UTC; sealing for ASX session Mon 2026-10-12. Plan: au_universe -> seal -> provenance -> unpriced-hunter-au waves -> edge_score -> 4-model panel -> note.

## Stage AU — Australia researcher — EMPTY
- Logged at 2026-10-11 06:41 UTC
- au_universe: 1573 scanner rows, 0 scheduled for 2026-10-12, 0 eligible, 0 hunted. market_open true (basis: 'beyond the tape: a weekday that is not an ASX holiday'). Case 3: a thin Australian session outside the Feb/Aug reporting seasons. No baselines sealed, no hunters, no panel.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-12 01:05 UTC
- Routine fire 01:05 UTC 2026-10-12: universe -> seal -> provenance -> unpriced-hunter-jp waves -> edge_score -> 4-model panel -> note. No orders.

## Stage J — Japan researcher — market closed
- Logged at 2026-10-12 01:05 UTC
- 2026-10-12 is スポーツの日 (国民の祝日): universe.json market_closed='public holiday: スポーツの日', scheduled_today 0. Nothing to hunt, no hunters spawned, no panel. Sheets read: kessan08_1002 (as_of 2026-10-01), kessan09_1009 (as_of 2026-10-08). No orders (stage J never places any).

## Close AMC — 2026-10-12 10:14 UTC
- Logged at 2026-10-12 10:21 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open, amc -> day order queued for open). verify: 14 legs, none UNFILLED, nothing held. close --submit: no leg due today, no orders sent, no refusals. Account reachable.

## Stage IPO — IPO researcher — STARTED
- Logged at 2026-10-12 12:38 UTC
- 2026-10-12 (Mon). Universe → seal → provenance → one unpriced-hunter-ipo per name → edge_score → four-model IPO panel → note. No orders.

## Stage IPO — IPO researcher — EMPTY DAY
- Logged at 2026-10-12 12:51 UTC
- NYSE open (market_closed null); eligible 0: no debut first-trades 2026-10-12 and no lock-up's first free session is today. Funnel all zeros (debut_scheduled 0, lockup_scheduled 0). Cross-checked against Nasdaq's IPO calendar at 12:51 UTC: last priced RTSN/TRXB 10-09, next upcoming IAM 10-15 and CTY 10-16. No hunters, no panel, no orders. Note: ipo_universe.py needed 'pip install requests' in this container and took ~12 min to run.

## Edge hunt — 2026-10-12 amc + 2026-10-13 bmo — STARTED
- Logged at 2026-10-12 17:08 UTC
- Fired 17:04 UTC (13:05 ET). execution.enabled true, exit_mode amc_open. STEP 0b DENIED: alpaca_trade.py verify (bare form, matching the settings.json allow rule) refused twice by the auto-mode classifier [Real-World Transactions]; nothing sold. Close AMC at 10:14 UTC reported 14 legs, none UNFILLED, nothing held, so no position is believed open. Universe: 9 names, all bmo 2026-10-13 (JPM JNJ UNH GS WFC C DPZ ACI FBK), all with an option chain; baselines sealed. Thin-day check: --include-unknown adds 6 time-not-supplied rows (UNTY FNGR RMCF NCPL BMRA MSS); session_resolve killed 0, confirmed 0 by press release, carried 6 — not hunted (no announcement; four are microcaps well past cadence). edge_universe.py needed 'python3 -m pip install requests'. Plan: 1 sweep + 9 hunters.
