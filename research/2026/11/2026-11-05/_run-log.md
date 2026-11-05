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

## Stage EU — wave 2 partial
- Logged at 2026-11-04 14:57 UTC
- AUTO +0.8, FBK +0.35 (event confirmed from issuer calendar). Running: DIS DEZ ORSTED ENX. Wave 3 launched early: HFG CAPMAN LR ZV (NRC next).

## Stage EU — progress
- Logged at 2026-11-04 14:59 UTC
- DIS +2.5 (release mid-session ~12:00 CET, inside bmo window), ORSTED +0.1. ORSTED hunter: second DK register join miss (Ørsted A/S 0.54% listed, baseline 0.0) — systematic for Danish names; baselines not revised. SFQ launched.

## Stage EU — progress
- Logged at 2026-11-04 15:03 UTC
- ENX +1.7 (17:45 CET release, amc confirmed), DEZ -1.0, HFG -0.1, CAPMAN -0.4. 13/20 banked. All 20 launched; running LR ZV NRC SFQ SMHN PKO INISS_B SKA_B.

## Stage EU — panel STARTED
- Logged at 2026-11-04 15:11 UTC
- 20/20 hunts banked, all search_complete, all event_confirmed; 20 ranked, none above floor 2.8. Top ASC/DIS +2.50, bottom ZV -1.60. 20 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-04 15:19 UTC
- Sealed for 2026-11-05 (Thu) at ~14:45 UTC Wed (intraday spots). 195 scheduled, 109 eligible, 20 drawn, 20 hunted, all search_complete, all event_confirmed, 20 ranked. Top ASC/DIS +2.50, bottom ZV -1.60; none above floor 2.8.
- Panel: 4/4 members, 20/20 each, no fallback (sonnet55 skipped the hunter definitions; opus5 read only fr). Selected ZV short (4/4, pct 89), AUTO long (3/4, 91), INISS_B long (3/4, 86), NRC short (3/4, 85).
- Defects: Danish register join miss (AMBU A/S 6.08%, Ørsted 0.54% sealed as 0.0); publish.sh rebase blocked by dirty eu-short-cache.json, pushed by hand. anchor_covered 9/20; es+pl 1 (PKO). DIS and ZV release in-session. Resolve by ~2026-11-13 (Nordic window). Pushing to main (EARNINGS_DATA_BRANCH=main).

## Close AMC — 2026-11-05
- Logged at 2026-11-05 11:20 UTC
- Fired 11:13 UTC (06:13 ET). Guard mode --require-exit-tif opg exit 0 (amc_open, amc->open as DAY). verify: 14 legs, all ok, nothing held. close --submit: no leg due today, no exit orders sent, no refusals. Account reachable. (Stage E legs end 2026-09-25; E-P now trades.)

## Stage M — morning exit review — STARTED
- Logged at 2026-11-05 14:17 UTC
- source research/2026/11/2026-11-04/edge-panel; fired 09:16 ET; 7 picks (U CAVA BYND ROOT FSLY ELF CORZ); analysts launched 09:17 ET
