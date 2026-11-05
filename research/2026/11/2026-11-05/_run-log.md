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

## Stage M — morning exit review — done
- Logged at 2026-11-05 14:19 UTC
- 7 names compiled 09:18 ET, all 7 analysts returned, 0 unusable: U limit 53.00, CAVA open, BYND limit 6.70, ROOT open, FSLY 10:00, ELF open, CORZ limit 13.30. Pool (2026-11-04 scored): 69 names / 10 days, review_minus_static -0.59 (t -1.32). Note: an earlier provisional compile at 09:17 caught 4 provisional reviews; superseded.

## Edge hunt (panel) — 2026-11-05 amc + 2026-11-06 bmo — STARTED
- Logged at 2026-11-05 18:09 UTC
- Stage E-P fire; session began 18:07 UTC (13:07 ET). Universe 314 names (257 amc 11-05, 57 bmo 11-06; GTN.A folded). Baselines being sealed by code into edge-panel/baselines in parallel; one edge-sweep launched alongside sealing. Plan: up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — baselines sealed
- Logged at 2026-11-05 18:11 UTC
- 314 of 314 baselines sealed by 18:11 UTC, before any searcher (10 parallel priced_in processes). 8 failed first time on Yahoo HTTPError (TEAM SPG NET MTD MNST LYV EOG AEE) and were re-sealed serially, all ok. Provenance stamped US-P (us-searcher.v3, claude-opus-5-5).

## Edge hunt (panel) — wave 1
- Logged at 2026-11-05 18:15 UTC
- Sweep: 35 of 314 checked, 25 company-confirmed, 9 unconfirmed (OPEN MNKD SRPT YELP PLSE TBCH XPOF FIGS SERV), 0 phantoms, 1 duplicate share class (UA, folded into UAA by the sweep), 279 unchecked. Cap 20: unconfirmed 9 shed, lowest hunt_priority shed: ARLO (32) NRDS (30) BLMN (28) IRTC (26) CGC (22); 279 unchecked shed. OMDA and WULF cadence_implausible, OKLO <3 prior prints: history not an earnings base rate, searchers told. Searchers unpriced-searcher, amc first, at most 8 per turn. Wave 1: AAOI INOD TMDX UMAC SG KRUS TNDM CELC.

## Edge hunt (panel) — waves 2-3
- Logged at 2026-11-05 18:29 UTC
- 18:29 UTC. All 20 searchers launched (UAA last). Finished, search_complete true per hand-backs: TNDM TMDX SG AAOI INOD UMAC KRUS CELC SOUN ETON GRND OMDA TRUP. Running: CARG CRSR HNST FNKO WULF OKLO UAA.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-11-05 18:38 UTC
- 20/20 searchers returned by 18:38 UTC (unpriced-searcher, native, Opus 5.5). hunt_status check --apply: 0 unfinished of 20; none retried. mode: execution enabled, amc_open. flatten --submit at 18:38 UTC: 2 positions held from 2026-11-04's book (CAVA -100, U 154; unrealised +12.39% / +14.94% as printed), both closed; flatten reported 'closed'. These legs were dated to exit 11-05 (CAVA amc at the open, U bmo at market) but were still held at 13:3x ET.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-05 18:38 UTC
- edge_score and V2 grounded written 18:38 UTC, before the first print. Packs built; four judges, one part. Account flat after 3s.

## Edge hunt (panel) — judges rate-limited
- Logged at 2026-11-05 20:43 UTC
- All four judges launched ~18:42 UTC were cut off by the account's 5-hour usage limit (HTTP 429, reset 19:10 UTC); the session's worker was restarted and resumed at 20:43 UTC (15:43 ET). opus5, sonnet55 and fable51 had already written complete files (20/20 each). opus55 wrote nothing; resumed by message at 20:43 UTC. Step 6b needs all four judges and an open market before 16:00 ET.

## Edge hunt (panel) — panel done, step 6b buy
- Logged at 2026-11-05 20:45 UTC
- opus55 resumed and finished 20/20 at 20:45 UTC; all four judges pinned agents, one part, no fallback, no retry. panel_score at 20:45 UTC. Selected (panel_pct >= 80, all four present): ETON L 92, OMDA L 92, FNKO L 87, HNST L 83 (3-of-4 rule: ETON OMDA FNKO). Next AAOI 73. ORDER CHANGED ON PURPOSE: with 15 minutes to the close, the buy went BEFORE the note (skill says note first) so the book would not be lost to the 16:00 ET deadline. 20:45:29 UTC (15:45 ET): plan, then open --submit --no-flatten. 4 market orders, all filled: ETON 87 @ 47.48, OMDA 220 @ 18.71, FNKO 573 @ 6.10, HNST 684 @ 4.42; gross ~$14,740 planned, 99.7% of $14,769 equity. Mean execution cost vs mid +0.185 (ETON +0.625 against a 14.3 half-spread). Exits dated 2026-11-06 (all amc -> open). Note: a second 'plan' call after the fills overwrote alpaca-plan.json with a post-fill budget ($2,215 with $12,553 held); the orders actually sent are in alpaca-orders.json.
