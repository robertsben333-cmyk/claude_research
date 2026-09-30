# Run log — 2026-09-30

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-29 06:40 UTC
- Fired Tue 2026-09-29 06:40 UTC (16:40 Sydney) on main (e1d53bb); sealing for next ASX session (expected Wed 2026-09-30). Plan: au_universe -> au_priced_in -> unpriced-hunter-au waves -> edge_score -> note. No orders.

## Stage AU — universe and seal
- Logged at 2026-09-29 06:41 UTC
- 1575 vendor rows / 12 scheduled / 4 eligible / 4 hunted; selection.method: all 4 eligible (under cap 20), seed au-2026-09-30 unused; session_unresolved 0. market_open true (weekday, not an ASX holiday). AUE PDI USL session amc (window close 09-30 -> close 10-01), MKR bmo (close 09-29 -> close 09-30).
- Filer mix: 4 of 4 quarterly_report_only (4C/5B), 0 results. ASIC register 20260923 (prev 20260916), lag 4 sessions. 30 Sep is the June-FY statutory annual-report deadline, the same vendor-row defect the 09-24/25/28 runs hit. One wave of 4 hunters.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-29 06:47 UTC
- 12 scheduled / 4 eligible / 4 hunted / 4 rankable / 0 above floor 3.0. AUE MKR PDI USL all impact_sum 0.00, no findings on any name: day has no ranking.
- All four vendor rows are the June-FY statutory annual report (due 30 Sep), fourth run running; ends after today. Register 20260923, lag 4. Filer mix 4 quarterly_report_only. Note: research/2026/09/2026-09-30/australia/australia-note.md

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-29 13:39 UTC
- Fired Tue 2026-09-29 13:38 UTC (15:38 Amsterdam, markets open) on main (380e15971); sealing for next European session Wed 2026-09-30. Plan: eu_universe -> eu_priced_in seal -> one market hunter per name in waves of 5 -> edge_score -> europe-note. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main pinned).

## Stage EU — universe and seal
- Logged at 2026-09-29 13:41 UTC
- 41 scheduled / 10 eligible above $200k / 10 hunted; selection.method: all 10 eligible (at or under cap 20), seed eu-2026-09-30 unused. by_market uk 5, de 2, fr 1, se 1, it 1; es/pl/dk/no/fi 0. market_concentration: uk 0.50 of the day, 5 markets. No market_closed.
- Registers read: uk (09-28), de (09-28), fr (09-25), it (09-28), se (09-28). anchor_covered 6 of 10 (DEBS GXI KOF PINE SAGA SPI). session_unresolved 8 of 10 (all bmo?; PINE and SKIS_B resolved bmo). history.basis observed_rns for 5 UK, estimated_from_cadence for ADE GXI DIB KOF SKIS_B. Two waves of 5: UK first, then DE/FR/IT/SE.

## Stage EU — wave 1 complete
- Logged at 2026-09-29 13:51 UTC
- 5 of 5 UK hunters returned: SAGA +1.1 (guide firm/raise, fuel hedge), AVG 0 (FY26 pre-released in line), PINE 0 (448p scheme, court 7 Oct), SPI 0 (250p final offer, vote 30 Oct), DEBS 0 event_confirmed false (H1 update already 17 Sep; interims likely Nov, vendor date probable phantom).
- Wave 2 early return: ADE event_confirmed false — H1 report published 2026-09-29 09:00 CEST (EQS), before the seal; neither window contains it. At resolve, amend ADE baseline with event_occurred: false + that URL (German archive cannot reach it automatically).

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-29 13:59 UTC
- 10 hunted / 6 rankable / 0 above floor 3.0. SAGA +1.10, GXI +0.50, AVG 0, PINE 0 (448p scheme), SPI 0 (250p final offer), SKIS_B -0.50. Not ranked (no event in window): ADE (H1 out 09-29 09:00 CEST), DIB (FY out 09-24 evening), KOF (9M amc 1 Oct per issuer), DEBS (probable phantom, interims Nov).
- At resolve: hand-amend ADE and DIB baselines with event_occurred: false (DE/IT cannot reach it automatically). Resolve SKIS_B within ~a week. Note: research/2026/09/2026-09-30/europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-30 01:05 UTC
- Fired 01:04 UTC 2026-09-30 (10:04 JST). Plan: jp_universe -> seal baselines -> unpriced-hunter-jp in waves of 5 -> edge_score -> japan-note. No orders.

## Stage J — universe + baselines sealed
- Logged at 2026-09-30 01:06 UTC
- 10 scheduled / 5 eligible / 5 hunted (2354 YE DIGITAL, 2685 and ST HD, 2975 Star Mica, 6083 ERI HD, 9369 KRS); method: all 5 eligible at or under cap 25, no draw. calendar_as_of 2026-09-03 (sheets kessan07_0904, kessan08_0918). Short register file 20260918 (12 days stale); 2354 and 2685 in it, other three truncated zero. One wave of 5 hunters launched.

## Stage J — resolved 2026-09-28
- Logged at 2026-09-30 01:06 UTC
- jp_resolve on the 09-28 run: 8227 impact_sum -0.5, realised +2.76%, event confirmed. 1 row, no statistics.

## Stage J — DEFECT found and fixed: stale JPX short register
- Logged at 2026-09-30 01:15 UTC
- jp_positioning.load() returned the newest CACHED register file <= today without ever checking JPX for a newer one, so every seal since 2026-09-19 used the 20260918 file (the '11/12 days stale' in the 09-29 and 09-30 logs was this bug, not JPX). Caught by the 2354 hunter, who read files up to 20260929. Fixed: load() now checks the JPX index for a newer file and uses the cache only as a fallback. Tested: load('2026-09-30') -> 20260929, 598 codes (2354 at 4.17% vs 3.17% sealed). Today's baselines stay SEALED on 20260918; not revised.

## Stage J — Japan researcher — DONE
- Logged at 2026-09-30 01:16 UTC
- Wave 1: 5 of 5 hunters returned. 5 ranked, 0 above floor 3.0: 2685 +1.50, 2354 +1.00, 2975 +1.00, 6083 +1.00, 9369 -0.80. Register sealed on 20260918 (stale by defect, fixed in e336548; baselines not revised). Note: japan/japan-note.md. No orders.

## Close AMC — 2026-09-30 10:10 UTC
- Logged at 2026-09-30 10:19 UTC
- Guard passed (amc open as day). verify: 14 legs, none UNFILLED-with-shares-held (all still held 0.0). close --submit: no leg due today, nothing sent, no refusals. Account reachable.

## Edge hunt — 2026-09-30 amc + 2026-10-01 bmo — STARTED
- Logged at 2026-09-30 17:08 UTC
- Fired 17:04 UTC (13:05 ET). 6 names in window (MU, PRGS, BSET amc 09-30; ACN, MKC, AYI bmo 10-01); MKC.V folded into MKC. Thin day (<10), so dropped time-not-supplied rows checked with session_resolve.py: 22 unresolved, 2 killed (HUBG, SA), 0 confirmed by announcement, 20 carried on cadence only — NOT added (measured phantom rate 20/20 on 09-17, 8/8 on 08-31). Baselines sealed for all 6 (5 with a live option chain; BSET none). Plan: 1 sweep + 6 hunters.
- Step 0b NOT RUN: the session's permission classifier refused alpaca_trade.py verify --fix --submit as a real-world transaction. No broker order was sent by this session, and step 7 will not be either. Close AMC's 10:10 UTC run reported no leg due today, so nothing appears to be left unsold, but this session did not verify that.

## Edge hunt — 2026-09-30 amc + 2026-10-01 bmo — DONE
- Logged at 2026-09-30 17:19 UTC
- 6 in window, sweep confirmed 6, 0 phantom. 6 hunters (all returned with pre_lessons, print_vs_bar_pct, expected_move_pct). Ranking key impact_sum: BSET +1.30, MKC +0.80, PRGS +0.30, AYI 0.00, MU 0.00, ACN -0.30. 0 of 6 clear the 3.0 floor. V2 calibrated (181 obs), written before the first print.
- Execution: execution.enabled is true, but this session placed NO orders. Step 0b (verify/close --submit) was refused by the session's permission classifier as a real-world transaction. Step 7 was not attempted: 0 names met the benchmark, so the book would have been empty. Close AMC at 10:10 UTC reported no leg due today; this session did not re-verify the account.
- Budget: 1 sweep + 6 hunters = 7 of 20. Nothing shed.

## Stage CA — Canada researcher — STARTED
- Logged at 2026-09-30 18:33 UTC
- 18:33 UTC (14:33 ET, inside the Toronto session). Plan: ca_universe -> seal baselines before 16:00 ET -> one unpriced-hunter-ca per name in waves of 5 -> edge_score -> note. No orders.

## Stage CA — Canada researcher — empty universe
- Logged at 2026-09-30 18:34 UTC
- Nobody eligible was scheduled; the TSX was open. 2,514 scanner rows, 4 scheduled for 2026-09-30 (LIO, CCDS, SR, WEST; calendar split confirmed 0 / agreed 0 / wsh_only 0 / vendor_only 4 / disputed 0, moved_off_target_by_wsh none). All 4 fell below the $200k/day turnover floor (largest LIO $53,975), so 0 eligible and 0 hunted. 3 of the 4 are filing_only, but the turnover floor removed them first. No baselines sealed, no hunters spawned, no scoring, so no register snapshot today and no anchor-arm split.
- DEFECT FOUND AND FIXED: the first ca_universe run (18:33 UTC) wrote market_closed='National Day for Truth and Reconciliation'. The TSX does NOT observe 30 September; TMX bars show RY trading 885,397 shares on 2026-09-30 by the time of the run. Removed 2026-09-30 and 2027-09-30 from TSX_HOLIDAYS in researcher_canada/scripts/ca_market.py. ca_smoke.py passes. Without the fix, every future 30 September would have been published as an exchange closure.
- FX: Yahoo did not answer, so the floor used the fallback constant CAD/USD 0.71. It cannot have changed the outcome: the largest name is 3.7x under the floor.

## Stage R — reversal researcher — STARTED
- Logged at 2026-09-30 19:04 UTC
- Fired 19:04 UTC = 15:04 ET, inside the 13:30-16:05 ET window. Plan: intraday screen of 2026-09-30, K=15, seal baselines, one reversal-hunter per name, edge_score.py, resolve 2026-09-29 run, note before 16:00 ET. No orders.
