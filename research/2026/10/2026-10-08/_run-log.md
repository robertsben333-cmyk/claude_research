# Run log — 2026-10-08

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-08 01:05 UTC
- Fired 01:05Z. Plan: jp_universe -> seal baselines -> provenance -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> note. No orders.

## Stage J — universe and baselines sealed
- Logged at 2026-10-08 01:06 UTC
- 29 scheduled / 19 eligible (10 microcaps under ¥15m) / 19 hunted; selection: all eligible (under cap 25). Calendar sheets kessan08_1002 + kessan09_1002, as_of 2026-10-01. Baselines sealed 01:1xZ, quality 0.6 (0.45 for 3907, no margin ratio).

## Stage J — resolved earlier runs
- Logged at 2026-10-08 01:07 UTC
- jp_resolve.py on 2026-10-05 (11/11 usable, rho -0.336 p 0.32, lean_vs_free_control_rho 0.482) and 2026-10-06 (7/7, rho -0.126 p 0.79, lean_vs_free_control_rho 0.679). 2026-10-07 window not closed yet.

## Stage J — wave 1 banked
- Logged at 2026-10-08 01:17 UTC
- 2809 +1.3, 3382 +0.4, 3907 -1.5, 4763 +1.4, 4825 +0.3 (impact_sum). Rolling 5-concurrent: 6323, 7513, 7649, 8016, 8125 in flight; 8194..9983 queued.

## Stage J — wave 2 banked
- Logged at 2026-10-08 01:24 UTC
- 6323 +1.1, 7513 -0.3, 7649 +0.2, 8016 +0.7. In flight: 8125, 8194, 8203, 8278, 9414; queued 9716, 9765, 9861, 9946, 9983.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-08 01:40 UTC
- 29/19/19; 19 of 19 rankable, 0 above the 2.8 floor; top 9983 +1.60, bottom 3907 -1.50; 14 positive / 5 negative. Note: research/2026/10/2026-10-08/japan/japan-note.md. Hunter scratch dirs hunts/h9765, hunts/h9861 left in tree (not read by scorer).

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-08 06:41 UTC
- Fired 06:41 UTC 2026-10-08; sealing for the next ASX session (expected 2026-10-09). Plan: universe -> seal baselines -> provenance -> unpriced-hunter-au waves of 5 -> edge_score -> note. No orders.

## Stage AU — Australia researcher — EMPTY SESSION
- Logged at 2026-10-08 06:41 UTC
- Event date 2026-10-09 (next ASX session). 1575 vendor rows, 0 scheduled, 0 eligible, 0 hunted, 0 session_unresolved. market_open true (basis: 'beyond the tape: a weekday that is not an ASX holiday') — a genuinely thin session outside the Feb/Aug reporting seasons, not a fetch fault. Empty universe published at research/2026/10/2026-10-09/australia/universe.json; no baselines, no hunters, no ranking, no orders.

## Close AMC — 2026-10-08 10:10 UTC (06:10 ET)
- Logged at 2026-10-08 10:16 UTC
- guard mode --require-exit-tif opg: exit 0 (amc open as day, matched on placement). verify: 14 exit legs, none UNFILLED, nothing still held (older amc/bmo legs show 0 filled but 0 held, closed by hand earlier). close --submit: no legs with exit date today, so no orders sent, no refusals. status: no open positions.

## Edge hunt — 2026-10-08 amc + 2026-10-09 bmo — STARTED
- Logged at 2026-10-08 17:09 UTC
- Fired 17:04 UTC (13:04 ET). Step 0b: account all cash (equity $11,200.86 = cash, no positions); verify/close --submit were DENIED by the auto-mode classifier [Real-World Transactions] even in the exact allow-rule form, so the 10-08 settings.json fix does NOT hold — harmless today because nothing was held. Universe: 4 confirmed-session rows (DAL, HOVR bmo 10-09; ODC, PKE amc 10-08) of 14; thin, so session_resolve.py checked the time-not-supplied rows: CMMB killed (6-K 09-30), HIFS dropped (no CIK), NRIX and GLDG carried with session_unresolved for the sweep to settle or drop. universe.json is the 6-name file; universe-confirmed-only.json kept. Baselines sealed for all 6 (option chain on DAL and PKE only). Plan: 1 sweep + up to 6 hunters.

## Edge hunt — sweep
- Logged at 2026-10-08 17:13 UTC
- Sweep: 6 in, 4 confirmed (ODC, PKE amc 10-08; DAL, HOVR bmo 10-09), 0 phantom, 2 unconfirmed (NRIX: no company date, vendors disagree 10-08/10-09/10-12; GLDG: interim 6-K filer with no release, not an earnings event). 4 hunters launched in parallel at ~17:20 UTC; NRIX and GLDG not hunted and enter as rankable:false.

## Edge hunt — 2026-10-08 amc + 2026-10-09 bmo — DONE
- Logged at 2026-10-08 17:21 UTC
- 4 hunted, 4 rankable, 0 clear 2.8 on impact_sum and 0 clear 1.76 on impact_scaled. Key impact_sum: ODC +0.80, PKE +0.60, DAL -0.90, HOVR -0.90. All 4 hunts under us.v9 with pre_lessons and print_vs_bar_pct present. V2 REFUSED: edge_grounded_score.py dated the first print 2026-10-08 09:30 ET, apparently from the unconfirmed NRIX row (date 10-08, session unknown); the real first print (ODC/PKE amc) had not passed. Defect, not worked around.
- Execution: enabled (paper, amc_open). Step 0b: account all cash at $11,200.86, no positions; verify/close --submit DENIED by the auto-mode classifier [Real-World Transactions] even in the exact allow-rule form 'python3 researcher_us/scripts/alpaca_trade.py ...', so the 2026-10-08 settings.json rule does NOT hold in this Routine session (read-only plan/assets/status calls did run). Step 7: plan says no name meets the benchmark, so open was not called; 0 orders, gross 0% of equity. Refusals: ODC 0.90, PKE 0.68, DAL 0.22, HOVR 1.26 < 1.76; GLDG and NRIX not rankable (no hunt). Context labels written (edge-context.json). Step 6c shadow ledger skipped (optional, nothing waits on it).
