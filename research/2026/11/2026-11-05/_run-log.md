# Run log — 2026-11-05

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-04 14:37 UTC
- Fired 2026-11-04 14:36 UTC (Wed; 15:36 Amsterdam, markets open, spots intraday). Sealing for event date 2026-11-05 (Thu). Plan: universe (10 markets, cap 20), seal, provenance, waves of 5 hunters, score, 4-judge intl panel, note. Publishing to main (EARNINGS_DATA_BRANCH=main). Note: container's local main had unrelated shallow history; worked from a branch off origin/main b6de4e03d.

## Stage EU — sealed
- Logged at 2026-11-04 14:41 UTC
- Event date 2026-11-05 (Thu). 195 scheduled, 109 eligible, 20 drawn (seed eu-2026-11-05): de5 fr3 it3 dk2 no2 se2 uk1 fi1 pl1 es0; largest market de 25%. Sealed ~14:45 UTC on intraday spots (not closes). 18 bmo, 2 amc (ENX, INISS_B). session_unresolved: DEZ HFG SFQ SMHN AMBU_B DIS FBK PKO ASC. Registers read for 9 markets; pl none. Waves: [AMV0 AMBU_B AKE DIS ASC] [DEZ ORSTED ENX FBK AUTO] [HFG CAPMAN LR ZV NRC] [SFQ SMHN PKO INISS_B SKA_B].

## Stage EU — wave 1 banked (4 of 5)
- Logged at 2026-11-04 14:51 UTC
- AMV0 -0.7, AKE +1.2, AMBU_B +0.9, ASC +2.5; all search_complete, all event_confirmed bmo. DIS still running. AMBU_B hunter: baseline short_ratio 0.0 is a register JOIN MISS — Finanstilsynet lists AMBU A/S 6.08% (03-11-2026), cache key 'AMBU A S'; baseline not revised (sealed), anchor_covered understated. Wave 2 launched: DEZ ORSTED ENX FBK AUTO. publish.sh rebase was blocked by a dirty eu-short-cache.json; committed and rebased by hand.
