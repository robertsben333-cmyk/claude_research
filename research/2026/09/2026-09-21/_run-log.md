# Run log — 2026-09-21

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-21 01:07 UTC
- Fired 2026-09-21 01:05 UTC (10:05 JST). Plan: jp_universe.py for today's Tokyo window, then jp_priced_in.py baselines, then one unpriced-hunter-jp per name in waves, edge_score.py, japan-note.md. 2026-09-21 is 敬老の日 per CLAUDE.md, so market_closed is expected to be set — will read universe.json rather than guess. Research only, no orders.

## Stage J — Japan researcher — COMPLETE (empty: market closed)
- Logged at 2026-09-21 01:10 UTC
- Tokyo shut: 敬老の日. universe.json carries market_closed; calendar READ IN FULL (680 rows, both cohort sheets, calendar_as_of 2026-09-03), scheduled_today 0. This is the closed-exchange case, not an unpublished cohort sheet.
- 0 eligible, 0 hunted, no baselines sealed, no hunters spawned, no ranking. No orders (stage J never places any).
- DEFECT FOUND AND FIXED: the container ships no openpyxl, so the first pass parsed 0 of 680 rows and every sheet carried an error. Harmless today because the holiday short-circuits it; on a TRADING day it would have produced scheduled_today=0 with a null market_closed, which the skill tells a session to read as 'cohort sheet not up yet'. Installed openpyxl and regenerated; added calendar_readable + an explicit note to jp_universe.py so 'nothing was read' can never again be read as 'nobody reports'. smoke_test.py passes.
- No resolved Japan run exists, so lean_vs_free_control_rho could not be reported. Next two fires (09-22 休日, 09-23 秋分の日) are also holidays; first rankable session is 09-24, which already has a 2026-09-18 forward hunt and should be RESOLVED rather than re-hunted.

## Close AMC — pre-market exit sweep
- Logged at 2026-09-21 10:15 UTC
- Guard: `alpaca_trade.py mode --require-exit-tif opg` exited 0 (execution.enabled=true, exit_mode=amc_open, amc placement=open as a plain market DAY order queued pre-market since auction_orders=false).
- verify --scan before close: 12 exit legs across 7 runs (2026-09-10 through 2026-09-18), all marked ok, still held 0.0 — nothing UNFILLED.
- close --submit --scan: no new orders placed. 2026-09-18's run had 0 positions (all 14 candidates rejected, none cleared the conviction/turnover floor), so no book was left open over the weekend for this Routine to close.
- status --scan: account is flat, equity == cash ($11,582.19), no open positions.
- No refusals, no UNFILLED legs, no unreachable-account condition. Quiet morning — nothing to sell.

## Edge hunt — 2026-09-21 amc + 2026-09-22 bmo — STARTED
- Logged at 2026-09-21 17:12 UTC
- Fired 17:05 UTC (13:05 ET), Monday. Window: today amc + next-session bmo. Universe: 5 of 27 calendar rows confirmed (AZO, ABVX, THO, MLKN, HERE); 19 time-not-supplied rows dropped.
- Thin-day check done (skill sec.1, window under ten): --include-unknown gave 24 rows, session_resolve.py checked all 19 carried rows against EDGAR + Nasdaq press releases — 0 killed, 0 confirmed by announcement, 19 carried unresolved. Same outcome as 2026-09-17 (which was 19 of 20 phantom). Cadence prior reads 'fits' on CURR (89d), FRGT (153d), ZENA (62d) — read as a prior, NOT filtered on and NOT used to add a name; that is exactly the TRT failure. Carried rows handed to the sweep to settle or drop.
- Step 0b execution: execution.enabled=true, exit_mode=amc_open. verify --scan over 7 runs / 12 exit legs: all 12 'ok', 0 shares still held, nothing to --fix. Account flat — 0 positions, equity $11,582.19, all cash. Nothing sold at step 0b because nothing was held; unrealised P&L on the exit: n/a.
- Baselines sealed and committed before any agent launched. 4 of 5 carry a live option chain (AZO, ABVX, THO, MLKN); HERE is no_options_market, tier thin. Plan: 1 edge-sweep over all 24 rows, then 1 unpriced-hunter per confirmed name. Budget 20, so no shedding.
