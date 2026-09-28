# Run log — 2026-09-28

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-25 13:39 UTC
- Fired Fri 2026-09-25 13:39 UTC (European markets still open; sealed spot is intraday). Sealing for event date Mon 2026-09-28, the next European trading day.
- Plan: eu_universe -> eu_priced_in seal -> one bilingual hunter per name by submarket, waves of 5, publish per wave -> edge_score -> note. No orders.
- Checkout: local main had no common ancestor with origin/main (history force-rewritten); reset local main to origin/main a558d7d8 before any work. Publishing with EARNINGS_DATA_BRANCH=main.

## Stage EU — universe and seal
- Logged at 2026-09-25 13:45 UTC
- 15 scheduled (uk 6, fr 3, it 2, pl 4; de/se/dk/no/fi/es 0), 6 eligible above $200k, 6 hunted, no draw (under cap 20). uk 3 (LIKE, SEE, TLW), fr 2 (EQS, OSE), pl 1 (PKP). market_concentration: uk 0.50 over 3 markets.
- session_unresolved (defaulted bmo): EQS, PKP, SEE, TLW. OSE amc (vendor flag), so its reaction lands 2026-09-29. LIKE bmo (vendor flag).
- DEFECT FIXED before any hunter ran: eu_positioning.load_uk() crashed ('>' NoneType vs NoneType) because the FCA renamed its date column to 'Position date (of latest position date notified)'; every UK name sealed register_unreadable. Fixed to match the header by prefix and compare DD/MM/YYYY as ISO (the old string compare also mis-ordered dates). First seal discarded and re-sealed; no hunter had read it. Earlier runs' UK baselines (09-22..09-25) not affected.
- anchor_covered 1 of 6: TLW (FCA 2.45%, +0.01pp). LIKE/SEE/EQS/OSE read, not named (truncated zero). PKP no register (pl). history observed_rns for the 3 UK names, estimated_from_cadence for EQS/OSE/PKP.

## Stage EU — wave 1 complete
- Logged at 2026-09-25 13:54 UTC
- 5 of 5 hunters returned: TLW +0.9 sum (confirmed bmo, 07:00 RNS), LIKE +2.0 (confirmed bmo, Notice of Results 17 Sep), EQS -1.0 (confirmed bmo, issuer agenda 'avant bourse'), OSE -1.3 (confirmed amc), SEE 0 findings, PHANTOM: FY26 audited results moved to 'by the end of November' (Proactive CEO/CFO interview 24 Sep); no Notice of Results RNS. Wave 2 (PKP) launched 14:05 UTC.

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-25 14:04 UTC
- Event date 2026-09-28 (sealed Fri 09-25 intraday). 15 scheduled / 6 eligible / 6 hunted / 5 rankable / 0 above floor 3.0. LIKE +2.00, TLW +0.90, PKP -0.30, EQS -1.00, OSE -1.30; SEE not ranked (phantom, FY26 results moved to end-Nov).
- PKP session is amc (post-17:00 Warsaw filings), not the defaulted bmo: read move_amc_window_pct at resolve. OSE amc too. Resolve from 2026-09-30.
- Note: research/2026/09/2026-09-28/europe/europe-note.md. Publishing with EARNINGS_DATA_BRANCH=main pinned.

## Stage EU — publish check
- Logged at 2026-09-25 14:05 UTC
- git log -1 origin/main after publish: 9cb4733d 'stage EU: Europe ranking for 2026-09-28' — the ranking is on main.

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-27 06:40 UTC
- Fired Sun 2026-09-27 06:40 UTC; sealing for next ASX session (expected Mon 2026-09-28). Plan: au_universe -> au_priced_in -> unpriced-hunter-au waves -> edge_score -> note. No orders.

## Stage AU — universe and seal
- Logged at 2026-09-27 06:42 UTC
- 53 scheduled / 14 eligible / 14 hunted; selection.method: all 14 eligible (under cap 20), seed au-2026-09-28 unused; session_unresolved 1 (IPX). market_open true (weekday, not an ASX holiday).
- Filer mix: 13 quarterly_report_only (4C/5B), 1 results (PNR). ASIC register 20260921, lag 4 sessions. AT4/HCH/KGL/SGQ re-appear from 09-25, where all hunters found the vendor row was the June-FY statutory annual report, not a print. Hunting anyway per skill (no pre-hunt filter exists); waves of 5.

## Stage AU — wave 1 complete
- Logged at 2026-09-27 06:49 UTC
- 5 of 5 returned: AT4 0 (no findings), BCM 0 (event not confirmed), BML +0.4 (1 finding), CHN 0, GLN 0. All five identify the vendor row as the June-FY statutory annual report (due 30 Sep), not a 4C/5B print — same defect as 09-24/09-25. Wave 2: HCH IPX KGL MI6 PEN.

## Stage AU — wave 2 complete
- Logged at 2026-09-27 06:54 UTC
- 5 of 5 returned: HCH 0, IPX 0 (event not confirmed; ~1/3 odds annual report lands in window), KGL 0 (not confirmed), MI6 0 (short 4.44%->9.63% read as placement/index hedging), PEN -0.4 (Davidson Kempner 28.1m-share residual below disclosure line). Wave 3: PNR SGQ VMM WC8.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-27 07:03 UTC
- 53 scheduled / 14 eligible / 14 hunted / 8 rankable / 0 above floor 3.0. BML +0.40, AT4 MI6 SGQ VMM 0, PEN -0.40, WC8 -0.50, PNR -0.60; BCM CHN GLN HCH IPX KGL not ranked (no event confirmed).
- All 14 vendor rows are the June-FY statutory annual report (due 30 Sep), third run running. Register 20260921, lag 4. Note: research/2026/09/2026-09-28/australia/australia-note.md

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-28 01:06 UTC
- 01:06 UTC fire on main (6d420b2). Plan: jp_universe -> seal baselines -> unpriced-hunter-jp in waves of 5 -> edge_score -> japan-note. No orders.

## Stage J — universe + baseline sealed
- Logged at 2026-09-28 01:08 UTC
- 2 scheduled / 1 eligible / 1 hunted (8227 しまむら; 7624 ＮａＩＴＯ dropped as microcap). Method: all eligible at or under cap. Short register file 20260918. Hunter spawned.

## Stage J — resolved 09-24 and 09-25
- Logged at 2026-09-28 01:08 UTC
- 09-24: 4716 confirmed, impact_sum -3.50, realised +8.15% (sign wrong); n=1 so no rho and no lean_vs_free_control_rho. 09-25: 2742 and 3333 confirmed on TDnet, move_pending until today's close.

## Stage J — Japan researcher — DONE
- Logged at 2026-09-28 01:18 UTC
- 1 name ranked: 8227 impact_sum -0.50 (below floor). Hunter hit 60-turn limit and was resumed to write output. Short register file 20260918 (10 days stale). Note: japan/japan-note.md.

## Close AMC — pre-market exit sweep
- Logged at 2026-09-28 10:21 UTC
- Fired 10:11 UTC (06:11 ET), inside the pre-market window before the 09:28 ET opg cutoff. Guard: mode --require-exit-tif opg -> exit 0 (execution.enabled true, exit_mode amc_open, amc exits placed as a market DAY order queued for the open since orders.auction_orders is False). verify --scan found all 14 tracked exit legs across 12 prior runs already at 'still held 0.0' -- nothing UNFILLED, nothing to rescue. close --submit re-scanned the same 12 runs (2026-09-10 through 2026-09-25); no leg has an exit date of 2026-09-28 and every prior leg is already closed (filled, expired or canceled with zero held), so nothing new was placed -- an idempotent no-op by design, not a guard failure. status confirms the account is flat: equity $11,200.86, no open entry or exit orders on any dated run 2026-09-10 through 2026-09-25, and 09-18/09-21/09-23/09-24/09-25 carry no positions at all.

## Edge hunt — 2026-09-28 amc + 2026-09-29 bmo — STARTED
- Logged at 2026-09-28 17:09 UTC
- Fired 17:05 UTC. Window: 9 of 37 calendar rows (6 amc 09-28: JEF MTN IDT TRAK SANG POCI; 3 bmo 09-29: CCL KMX UEC). Thin day (<10), so session_resolve.py checked the 23 time-not-supplied rows: 1 killed by EDGAR, 0 confirmed by press release, 22 carried as unresolved — not added (base rate 20/20 phantom). Baselines sealed for all 9 (6 with a live option chain: JEF MTN IDT CCL KMX UEC). Plan: 1 edge-sweep + up to 9 unpriced-hunters, 10 of 20 subagents.
- Step 0b NOT RUN: execution.enabled is true, but every alpaca_trade.py call that touches the broker (verify --fix --submit, and even read-only status) was refused by this session's permission classifier as a real-world transaction. The repo's own order records show no leg due today (last book 09-22 MANU/WOR, exits dated 09-23; 09-23..09-25 placed nothing), so nothing is known to be left unsold, but the broker state itself was NOT read. Step 7 will be blocked the same way.

## Edge hunt — 2026-09-28 amc + 2026-09-29 bmo — DONE
- Logged at 2026-09-28 17:27 UTC
- 9 names in window, sweep confirmed 9/9, 0 phantom rows. 9 hunters (one per name), all returned the current contract (pre_lessons, print_vs_bar_pct, expected_move_pct present). Ranking key impact_sum: TRAK +0.90, KMX +0.40, POCI +0.20, IDT/JEF/MTN 0, CCL -0.50, SANG -0.50, UEC -0.90. 0 of 9 clear the 3.0 floor. V2 calibrated (177 obs), written before first print. Control -run_up_20d ranks the day at Spearman -0.67 vs the hunt.
- Execution: DRY/NOT RUN. execution.enabled is true but the session permission classifier refused every alpaca_trade.py broker call (verify, status). Step 0b sold nothing; step 7 not run; with 0 names meeting the benchmark the book would have been empty anyway (0 orders, 0% gross). alpaca_trade.py assets not run (broker lookup) — tradable column built from baseline spot x 20d volume, borrow unchecked.

## Stage E V2 — shadow ledger — 2026-09-28
- Logged at 2026-09-28 17:31 UTC
- collected 11 8-Ks for 9 tickers; shadow-scorer scored 11/11 blind; ingested 11, refused 0; measured 12 complete (198 pending). Pooled n at session_close 179, kappa +0.353 (se 0.069).

## Stage CA — Canada researcher — STARTED
- Logged at 2026-09-28 18:33 UTC
- Fired 18:33 UTC (14:33 ET). Plan: ca_universe -> seal baselines before 16:00 ET -> one unpriced-hunter-ca per name -> edge_score -> note. No orders.

## Stage CA — Canada researcher — EMPTY DAY
- Logged at 2026-09-28 18:33 UTC
- universe.json written 18:33 UTC. market_closed: null, scheduled_today: 8 (TSX open, names scheduled) — but 0 eligible: all 8 fall below the $200k/day turnover floor (largest MMY $148,672). Not a fault; no baselines sealed, no hunters spawned, no ranking.
- calendar_reconciliation: confirmed 1 (STC) / agreed 0 / wsh_only 0 / vendor_only 6 / disputed 1 (DND); moved_off_target_by_wsh: none.
- filing_only: 4 of 8 (ROS, XXIX, FCLX, SR), but none was the binding cut — all four were already below the floor. Anchor arms: 0 options / 0 register (nothing sealed). No short-register snapshot stored today, so the register history does not advance.
- Degradation: fx_source = FALLBACK CONSTANT 0.71 (Yahoo did not answer). Immaterial today (MMY would need CAD/USD ~0.96 to clear). TMX calendar/archive answered; no vendor-stack outage.
