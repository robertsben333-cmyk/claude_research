# Run log — 2026-10-21

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-20 13:38 UTC
- Fired 13:37 UTC Tue 2026-10-20; sealing for event date 2026-10-21 (Wed, next European session). Plan: eu_universe (cap 20, $100k floor, seeded draw) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-model intl panel -> note. No orders. Publishing to main (EARNINGS_DATA_BRANCH pinned).

## Stage EU — universe and baselines sealed
- Logged at 2026-10-20 13:48 UTC
- Event date 2026-10-21. 62 scheduled, 37 eligible, 20 hunted by seeded draw (eu-2026-10-21): se 15, de 2 (FTK, SAP), no 1 (DNB), fi 1 (TTALO), es 1 (IBE). Largest market se 75%, 5 markets. Yahoo calendar unavailable on all ten. Registers: de 2026-10-19, fi 2026-10-16, no 2026-10-19, se 2026-10-20, es none. anchor_covered: ALTRA BULTEN FABG FTK JM MIPS (6 of 20). History observed for DNB only (observed_newsweb). session_unresolved: ALTRA, FTK, KEBNI_B. amc: SAP, BULTEN (window 10-21 close -> next close). Provenance stamped (nordic.v5, de/es v-current, opus-5-5 by alias timeline; get_session unavailable).

## Stage EU — wave 1 done
- Logged at 2026-10-20 14:02 UTC
- IBE +0.35, TTALO -0.10 (profit warning pre-released 10-20 13:45 EEST, before seal), DNB -0.15, SAP +0.70 (amc 22:05 CEST), FTK -1.3. FTK: IR calendar says Q3 at 18:00 CEST 10-21, after the Xetra close (amc); the sealed bmo window contains no release — eu_resolve should score it from session_check / both windows. Wave 2: ALTRA BERG_B BULTEN FABG GETI_B (se, unpriced-hunter-nordic).

## Stage EU — wave 2 done
- Logged at 2026-10-20 14:11 UTC
- ALTRA +0.70 (MFN estimates 12:00 in-session; Q1 came 19:40, timing uncertain), BERG_B +0.60, BULTEN +1.90 (issuer invitation: 13:30 CEST in-session, so the sealed amc window is WRONG; session_check says bmo), FABG +0.85, GETI_B -0.20. Wave 3: HEBA_B INWI JM KEBNI_B MIPS (se).

## Stage EU — wave 3 done
- Logged at 2026-10-20 14:21 UTC
- HEBA_B +0.50 (12:00 in-session, window holds it), INWI +1.00, JM -1.00, KEBNI_B 0.00, MIPS +2.90 (largest so far; below the 2.8 floor? no — 2.9 clears it). Wave 4 running: NMAN OVZON SALIX SHB_A SKF_A.

## Stage EU — panel STARTED
- Logged at 2026-10-20 14:30 UTC
- 20 hunts done; 20 ranked, 1 above 2.8 (MIPS +2.90). Wave 4: NMAN 0.00, OVZON +0.30, SALIX +0.30, SHB_A -0.30, SKF_A +0.05. 20 packs, four intl judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-20 14:38 UTC
- Event date 2026-10-21. 20 ranked (se 15, de 2, no/fi/es 1), drawn from 37 eligible. 1 above floor 2.8: MIPS +2.90. Bottom FTK -1.30. Panel 4/4, no fallback: selected MIPS long (k=4, panel_pct 92), JM short (k=3, 85), BULTEN long (k=3, 83; marginal, Sonnet exactly at q80). Session corrections: FTK is amc (18:00 CEST), BULTEN in-session 13:30 (sealed amc) — check eu_resolve rows. TTALO pre-released via 10-20 profit warning. Resolve the 15 SE names + TTALO within ~a week. Note: europe-note.md. Published with EARNINGS_DATA_BRANCH=main.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-21 01:05 UTC
- Fired 01:05 UTC (10:05 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp waves of 5 -> edge_score -> four-model panel -> note. No orders.

## Stage J — panel STARTED
- Logged at 2026-10-21 01:11 UTC
- 3 packs, four judges (intl)

## Stage J — Japan researcher — DONE
- Logged at 2026-10-21 01:14 UTC
- 5 scheduled / 3 eligible / 3 hunted. impact_sum: 296A +0.50, 8953 +0.35, 3290 +0.25; none above floor. Panel 4/4 members, none selected (296A panel_pct 68, k=1). Note: japan/japan-note.md. No orders.

## Close AMC — 2026-10-21 10:11 UTC
- Logged at 2026-10-21 10:23 UTC
- mode --require-exit-tif opg exit 0 (amc -> open as market DAY). verify: 14 legs, none held, none UNFILLED. close --submit: no leg due today, nothing sent, no refusals. status: no open positions.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-21 13:14 UTC
- source research/2026/10/2026-10-20/edge-panel; 09:15 ET; picks NP, WFRD, ALK, MCB (4 analysts launched)

## Stage M — morning exit review — done
- Logged at 2026-10-21 13:16 UTC
- 4 names: NP exit_limit, WFRD exit_open, ALK exit_open, MCB exit_open; pool (prev mornings) 6 names / 2 days, review_minus_static +0.83 t 0.67

## Intraday panel 12:00 — STARTED
- Logged at 2026-10-21 16:00 UTC
- Fired 15:59 UTC (11:59 ET). First snapshot of the day (no 10:00 snapshot on disk): build universe + sweep, freeze, seal, Opus 5.5 searchers (cap 19, amc first), guard, edge_score, four judges, panel_score --dry-run. No orders.

## Intraday panel 12:00 — sweep
- Logged at 2026-10-21 16:04 UTC
- Universe 118 names (64 amc 10-21, 54 bmo 10-22), 118 baselines sealed 16:03 UTC and published before any agent. Deviation: the sweep ran as THREE edge-sweep agents in parallel over interleaved thirds of the universe (40/39/39), merged into one sweep.json, because one agent over 118 names would eat the amc names' pre-release time. Same agent, same absolute 0-100 hunt_priority scale.

## Intraday panel 12:00 — wave 1
- Logged at 2026-10-21 16:11 UTC
- Sweep (3 parts merged): 108 of 118 confirmed; unconfirmed FCFS ZGN AMBP NTST OSBC DOW CVBF BMI KRNY NVEC (not hunted). Names frozen in edge-intraday/names.json by this snapshot. Budget 19 by hunt_priority (strict order, no option-chain deviation): MOH MEDP LBRT EGBN SLG CASH ASIC KALU LOB HXL WDFC QS KNX LUV (amc) + THRM ARGX SPOT IIIN CRS (bmo); 89 confirmed names shed on lowest priority. unpriced-searcher (Opus 5.5), amc first.

## Intraday panel 12:00 — searchers launched
- Logged at 2026-10-21 16:13 UTC
- ~16:20 UTC: MOH MEDP LBRT EGBN SLG CASH ASIC running (unpriced-searcher native). Queue: KALU LOB HXL WDFC QS KNX LUV, then THRM ARGX SPOT IIIN CRS. THRM baseline amended suspect->unknown (edge_baseline_amend.py table rewritten for this run) before any hunt.
