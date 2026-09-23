# Run log — 2026-09-23

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-23 01:05 UTC
- 01:05 UTC fire. 2026-09-23 is 秋分の日 (Autumnal Equinox Day); expecting market_closed. Build universe, publish, stop if shut.

## Stage J — Japan researcher — MARKET CLOSED
- Logged at 2026-09-23 01:05 UTC
- Tokyo shut: market_closed = 'public holiday: 秋分の日' (Cabinet Office 国民の祝日 list). scheduled_today 0 because the exchange is closed, not because a cohort sheet is missing. Sheets read: kessan07_0904.xlsx (as_of 2026-09-03, 236 rows), kessan08_0918.xlsx (as_of 2026-09-17, 444 rows). Empty universe published at japan/universe.json; no baselines, no hunters, no scoring. No orders: this stage has no broker step.

## Close AMC — 2026-09-23 opening auction
- Logged at 2026-09-23 10:17 UTC
- Guard: mode --require-exit-tif opg exited 0 (execution.enabled=true, exit_mode=amc_open, amc placement=open/day).
- verify before close: all 12 prior exit legs read still-held 0.0, none UNFILLED — nothing needed a rescue.
- close --submit: only one amc leg had an exit date of today — 2026-09-22/edge WOR, sent as a market DAY order queued for the open (client_order_id 5994e8fb-1ee0-415b-89aa-27a4ed43eb65).
- 2026-09-22/edge MANU (bmo) correctly deferred: exit placement is market, not open, so it is left to stage E's own 13:05 ET run rather than sent here.
- fill check at +300s: WOR reads work, filled 0/64, still held 64.0 — expected, since Alpaca queues a pre-market DAY order and does not route it until the 09:30 ET open; not verifiable from this session.
- status --scan confirms account state: equity $11,064.67, cash $11,552.50. 2026-09-22/edge shows MANU OPEN long 187 @ 20.43 (+0.39%) and WOR OPEN short -64 @ 59.23 (-14.05%), both awaiting their respective exits.
- No account/API errors. Nothing else to report.

## Edge hunt — 2026-09-23 — step 0b exits
- Logged at 2026-09-23 17:10 UTC
- execution.enabled true, exit_mode amc_open. verify: all 13 prior legs closed, nothing held. close: sent MANU (bmo, 09-22 book) at market 17:0x UTC, filled 187 @ 20.28 vs entry 20.43 (-$28, -0.7%). WOR (amc short, 09-22 book) had already been covered by Close AMC at the open: 64 @ 64.75 vs short 59.23 (-$353, -9.3%). Account flat, equity $11,200.86 all cash.

## Edge hunt — 2026-09-23 amc + 2026-09-24 bmo — STARTED
- Logged at 2026-09-23 17:15 UTC
- 8 of 44 calendar rows in window (FUL, SFIX, NEOV amc 09-23; DRI, SNX, BB, UXIN, MITQ bmo 09-24). Baselines sealed 17:15 UTC, 6 of 8 with an option chain (UXIN, MITQ none). Thin day (<10) so the 29 time-not-supplied rows were checked with session_resolve.py: 3 killed by EDGAR, 0 confirmed by press release, 26 carried unresolved — none added (measured phantom rate 20/20 on 09-17, 8/8 on 08-31). Plan: 1 sweep + up to 8 hunters. amc hunts must finish before 20:00 UTC.

## Edge hunt — 2026-09-23 amc + 2026-09-24 bmo — DONE
- Logged at 2026-09-23 17:28 UTC
- Execution ON (paper). Step 0b: MANU sold at market 187 @ 20.28 (entry 20.43, -$28); WOR already covered at the open by Close AMC 64 @ 64.75 (short 59.23, -$353). verify: all prior legs closed. Sweep: 8/8 confirmed, 0 phantom. 8 hunters, all returned pre_lessons and print_vs_bar_pct (tree's contract ran). ranking_key impact_sum: SFIX +0.8, BB +0.5, MITQ +0.2, DRI 0, FUL 0, SNX 0, NEOV -1.5, UXIN -3.0. 1 name met the conviction floor (UXIN) and was refused on turnover ($0.05m < $0.2m). 0 orders placed, gross 0% of equity $11,200.86, account all cash. V2 grounded written (calibrated, 170 obs) before first print. Key vs -run_up_20d_pct rho +0.10. No failures.

## Stage E V2 — shadow ledger 2026-09-23
- Logged at 2026-09-23 17:31 UTC
- collected 7 new 8-Ks (brief listed 8 inputs, incl. WOR re-scored over an existing score file); scored 8 blind, ingested 8, 0 refused; measure 5 complete; pooled n at session_close 165, kappa 0.362 (se 0.071).

## Stage CA — Canada researcher — STARTED
- Logged at 2026-09-23 18:33 UTC
- Fired 18:33 UTC (14:33 Toronto, inside the session). Plan: ca_universe -> seal baselines before 16:00 ET -> one unpriced-hunter-ca per name in waves of 5 -> edge_score -> canada-note. Research only, no orders.

## Stage CA — Canada researcher — DONE (empty day)
- Logged at 2026-09-23 18:33 UTC
- TSX open (market_closed null); 4 scheduled, 0 eligible, 0 hunted. All 4 fell below the $200k floor (MMY $139k, DND $119k disputed, WILD $55k, SR $10k filing_only). Calendar: confirmed 1 / agreed 0 / wsh_only 0 / vendor_only 2 / disputed 1; moved_off_target_by_wsh none. Anchor arms: options 0 / register 0. No baselines sealed, so no register snapshot stored today. TMX calendar and archive answered; Yahoo FX did not (fallback CAD/USD 0.71, not binding).
