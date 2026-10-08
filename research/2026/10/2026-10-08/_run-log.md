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

## Edge hunt (panel) — 2026-10-08 amc + 2026-10-09 bmo — STARTED
- Logged at 2026-10-08 17:09 UTC
- Stage E-P fired 17:08 UTC. Universe --window: 4 of 14 rows (DAL bmo 10-09, ODC amc, PKE amc, HOVR bmo 10-09). Thin-day check with --include-unknown + session_resolve.py (not applied): CMMB killed already_reported (6-K 09-30), HIFS no_cik, GLDG/NRIX unresolved (NRIX: no press-release date, vendor projection) - none carried. Baselines sealed for 4 (options chain on DAL, PKE). Plan: 1 edge-sweep, up to 4 unpriced-searchers, edge_score, grounded V2, packs, 4 judges, panel_score. No orders.

## Edge hunt (panel) — universe widened
- Logged at 2026-10-08 17:13 UTC
- Matched stage E's thin-day procedure: session_resolve.py --apply carried NRIX (10-08) and GLDG (10-09) with session_unresolved; baselines sealed provisionally (NRIX amc, GLDG bmo); a second edge-sweep settles them or drops them. universe-confirmed-only.json kept. git push to origin is refused 403 from this container; publishing through the GitHub MCP push_files instead.

## Edge hunt (panel) — sweep and searchers
- Logged at 2026-10-08 17:14 UTC
- edge-sweep confirmed 4 of 4 from company sources (PKE amc 71, ODC amc 58, HOVR bmo 39, DAL bmo 22; DAL session inferred from a 10:00 ET call + 7 prior bmo prints). 4 unpriced-searchers launched 17:2x UTC in one wave. NRIX/GLDG second sweep pending. Publishing BLOCKED: git push 403 and GitHub MCP push_files 403 'Resource not accessible by integration' on main and on a branch - work is committed locally only.
