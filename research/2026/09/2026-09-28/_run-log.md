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
