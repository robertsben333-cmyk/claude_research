# Run log — 2026-10-28

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-27 14:01 UTC
- Fired 13:59 UTC 2026-10-27 (scheduled 13:35), sealing for event date 2026-10-28 (Wed), markets still open so sealed spots are intraday.
- Plan: eu_universe (cap 20, $100k floor) -> seal baselines -> provenance -> hunters in waves of 5 -> edge_score -> four-model panel -> note. Publishing to main (EARNINGS_DATA_BRANCH=main).

## Stage EU — universe and baselines sealed
- Logged at 2026-10-27 14:11 UTC
- Event date 2026-10-28. 88 scheduled, 53 eligible (uk 6, de 7, fr 5, se 7, dk 4, no 8, fi 11, it 1, es 3, pl 1), 20 drawn (random, seed eu-2026-10-28): fi 5, no 4, uk 3, fr 2, se 2, dk 2, de 1, es 1. Largest market fi 25%, 8 markets. Yahoo calendar unavailable on all ten; bankier (PL) unavailable. Baselines sealed ~14:10 UTC at intraday spots. amc: AIR, DBV, AOJ_B. session_unresolved: CGEO, JYSK, SRT. Registers: es none; others read. Provenance stamped, orchestrator claude-opus-5-5. Wave 1: 8TRA ACAST AIR AOJ_B BNOR.

## Stage EU — wave 1 mostly banked, wave 2 launched
- Logged at 2026-10-27 14:21 UTC
- Banked: BNOR +0.3 (merger target of VAR, pinned), ACAST +0.8, AOJ_B +0.5 (amc confirmed), AIR +0.1 (amc confirmed; Dutch issuer, not on AMF flux). 8TRA still running. Launched CGEO, DBV, ELE, GSK.

## Stage EU — wave 2 banked
- Logged at 2026-10-27 14:32 UTC
- Banked: 8TRA +1.1, CGEO +0.5 (bmo confirmed 07:00 RNS), JYSK 0.0 (Q3 pre-released 12 Oct; bmo by pattern), GSK +0.3, ELE +0.7, LASTIK -0.3, DBV -3.4 (date NOT confirmed by issuer; Earnings Whispers says 11-04 — possible phantom, amc). Running: ORNAV PEAB_B PHO SALME SANOMA.

## Stage EU — panel STARTED
- Logged at 2026-10-27 14:48 UTC
- All 20 hunts banked; 19 ranked (SRT: no event). DBV -3.40 the only name above floor 2.8 (date unconfirmed by issuer). Packs built, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-27 14:56 UTC
- 19 ranked: 8TRA +1.10 ... DBV -3.40 (only floor-clearer; date not confirmed by issuer, possible phantom). SRT not ranked (no event). Panel 4/4 members, no fallback, 3 selected: DBV short (4/4, pct 96), SALME short (4/4, 86), 8TRA long (3/4, 81). anchor_covered 5/20; es 1 name; 9 se/dk/fi names need resolving within ~a week. Note: europe/europe-note.md. No orders. Pushed to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-28 01:06 UTC
- Fired 01:04 UTC (10:04 JST) 2026-10-28. Plan: jp_universe (cap 25, seeded draw) → seal baselines → provenance → unpriced-hunter-jp in waves of 5 → edge_score → four-model intl panel → note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-28 01:07 UTC
- Universe: 46 scheduled, 39 eligible (7 dropped on turnover), 25 hunted, method "random sample of 39 eligible, seed 'jp-2026-10-28'". calendar_as_of 2026-10-01. Short register 20261027 (626 codes). provenance jp.v5 / claude-opus-5-5. Five waves of 5. Wave 1: 1930 2002 2664 2760 3003.

## Stage J — resolved 2026-10-26
- Logged at 2026-10-28 01:08 UTC
- jp_resolve: 5/5 usable, impact_sum rho 0.0 (p 1.0), free control 0.4, sign right 1/5, lean_vs_free_control_rho 0.70 (5 names; short_squeeze/short_building unresolvable, no register positions). Panel resolved too. One day is not a result.

## Stage J — wave 1 banking
- Logged at 2026-10-28 01:13 UTC
- Banked 1930 3003 (+2760 file written). Rolling slots: 3771 3778 3850 launched.

## Stage J — wave 2 banking
- Logged at 2026-10-28 01:19 UTC
- Wave 1 banked 5/5 (1930 2002 2664 2760 3003). 3771 3850 banked; 3778 4373 4832 4956 6023 running (rolling slots of 5). Push conflict at 01:16 (dirty short-positions cache blocked publish.sh rebase) fixed by committing the cache and rebasing.

## Stage J — panel STARTED
- Logged at 2026-10-28 01:42 UTC
- 25/25 hunts banked and scored (top 2664 +1.70, 7276 +1.60; bottom 6023 -1.00, 6807/8871 -0.50; none above 2.8). 25 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-28 01:51 UTC
- 25 ranked: top 2664 +1.70, 7276 +1.60; bottom 6023 -1.00, 6807/8871 -0.50; none above floor 2.8. Signs 17+/2 zero/6-. Panel 4/4 members, no fallback, 2 selected (6807 S 4/4, 4832 S 3/4). 13 names release in-session. Resolved 10-26 (lean_vs_free_control_rho 0.70 on 5). Note: japan/japan-note.md. No orders.

## Close AMC (stage X) — 2026-10-28
- Logged at 2026-10-28 11:15 UTC
- Guard mode --require-exit-tif opg: exit 0 (amc_open, amc exit as market DAY order).
- verify: 14 exit legs, all ok, nothing held, no UNFILLED legs.
- close --submit: no exit legs due today, nothing sent, no refusals. Last positions (MANU, WOR) flat since 09-23. Run files rewritten with refreshed fill status only.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-28 13:27 UTC
- Routine fired late: 13:26 UTC = 09:26 ET (scheduled 09:10 ET), past the 09:24 compile deadline. Source research/2026/10/2026-10-27/edge-panel. Picking + compiling without analysts; no time for reviews before the 09:30 open.

## Stage M — morning exit review — done
- Logged at 2026-10-28 13:28 UTC
- Late fire (13:26 UTC = 09:26 ET, scheduled 09:10 ET): 8 picks (BOOM, OI, RBBN, ENPH, LUNG, KIDS amc; AMRN, JMKE bmo), snapshot taken, NO analysts launched because the 09:24 compile deadline had passed and the open was 3 minutes away; compiled as Geen advies for all 8 (static rule stands). Previous morning 2026-10-27 resolved; pool: 42 names / 7 days, review_minus_static -0.078 (t -0.18).

## Edge hunt (panel) — 2026-10-28 amc + 2026-10-29 bmo — STARTED
- Logged at 2026-10-28 17:22 UTC
- Stage E-P fire 17:06 UTC (session start 17:09). Universe 289 names (134 amc 10-28, 155 bmo 10-29), baselines sealed for all 289 in edge-panel/baselines before any agent (17:22 UTC). Plan: one edge-sweep, up to 20 unpriced-searchers, step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-10-28 17:28 UTC
- Sweep finished 17:28 UTC (34 of 289 checked): 30 company-confirmed (27 with settled session), 0 phantoms, 255 unchecked. Cap 20: the 20 highest-priority confirmed (amc 10-28: MVIS MDXG CLPT VNDA TDOC PRCH HDSN AWRE VKTX MAX HRTG CYH; bmo 10-29: LENZ BFLY ESTA FVRR NVCR HIPO XRX BAND). Shed by hunt_priority: ASTL RSI PI NEO COHU ALKT CLB (confirmed), PHAT SIMO TSAT (session unsettled), all unchecked. Searchers unpriced-searcher, amc first, 8 at a time.
