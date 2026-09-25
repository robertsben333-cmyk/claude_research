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
