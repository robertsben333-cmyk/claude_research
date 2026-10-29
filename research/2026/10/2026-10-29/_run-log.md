# Run log — 2026-10-29

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-28 13:47 UTC
- Fired 13:46 UTC 2026-10-28 (scheduled 13:35), sealing for event date 2026-10-29 (Thu). Plan: universe (cap 20, $100k floor), seal, stamp, hunters in waves of 5, score, four-judge panel, note. Local main had diverged from origin (stale container copy, 52/52); work done on a fresh branch off origin/main, published with publish.sh to main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-28 14:00 UTC
- Event date 2026-10-29. 115 scheduled, 78 eligible (uk 5, de 11, fr 6, se 11, dk 4, no 18, fi 12, it 3, es 6, pl 2), 20 drawn (random, seed eu-2026-10-29): no 6, fi 3, es 3, fr 2, se 2, it 2, uk 1, de 1. Largest market no 30%, 8 markets. Baselines sealed ~14:15 UTC at intraday spots. session_unresolved: RDC, AL2SI, AMP, IG, BOHUS, DVD, KOG, PPH. anchor_covered 6/20 (AMP, IG, DVD, PPH, RDC + see note). es 3 names (no anchor, no archive). Provenance stamped. Wave 1: AKRBP AL2SI AMP BOHUS DNO.

## Stage EU — 14 of 20 hunts banked
- Logged at 2026-10-28 14:26 UTC
- Banked: BOHUS +1.4, FDR +1.2, IG +0.9, PDX +0.8, DNO +0.7, ENENTO +0.6, NESTE +0.3, AMP +0.2, ENGCON_B +0.1, KOG -0.1, DVD -0.3, AKRBP -0.4, EPR -0.7, AL2SI -4.5. Session corrections by hunters: AL2SI and AMP report amc (issuer pattern / 18:30 CET call), so the sealed bmo window may hold no release; ENENTO and IG release in session (inside the bmo window). Running: IDR NTGY POSTI PPH RDC STMPA (six concurrent for a few minutes, one over max_concurrent 5). Hunters run rolling, not in fixed waves; each banked hunt published on arrival.

## Stage EU — panel STARTED
- Logged at 2026-10-28 14:34 UTC
- All 20 hunts banked and scored; 20 ranked. AL2SI -4.50 the only name above floor 2.8. 20 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-28 14:42 UTC
- 20 ranked: BOHUS +1.40 top ... AL2SI -4.50 (only floor-clearer; hunter dates release amc, so sealed bmo window likely holds no release). Panel 4/4 members, no fallback, 4 selected: FDR long (4/4, pct 83), AL2SI short (3/4, 93), EPR short (3/4, 81), NESTE long (3/4, 80). anchor_covered 5/20; es 3 names, pl 0; 5 se/fi names need resolving within ~a week. AMP also amc per hunter. Note: europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main) from a fresh branch off origin/main, because local main had diverged.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-29 01:05 UTC
- Routine fire 01:05 UTC 2026-10-29 (10:05 JST). Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp in waves of 5 (cap 25) -> edge_score -> four-model intl panel -> note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-29 01:07 UTC
- Universe: 127 scheduled, 106 eligible (21 dropped on turnover), 25 hunted, random sample seed 'jp-2026-10-29'. calendar_as_of 2026-10-01. provenance jp.v5 / claude-opus-5-5. Wave 1: 1946 2594 3116 3199 4347.

## Stage J — resolved 2026-10-27
- Logged at 2026-10-29 01:07 UTC
- jp_resolve: 25/25 usable, impact_sum rho -0.313 (p 0.125), free control 0.055, lean_vs_free_control_rho 0.435. Panel: rho panel_pct -0.483 (p 0.01), selected 6 names 1 right, mean signed -6.22%. One day is not a result.

## Stage J — wave 1 banking
- Logged at 2026-10-29 01:14 UTC
- Banked 1946 2594 3199 (rolling slots). Running: 3116 4347 4366 4502 5482. Resolved 10-27 published earlier.

## Stage J — wave 2 banking
- Logged at 2026-10-29 01:16 UTC
- Wave 1 banked 5/5 (1946 2594 3116 3199 4347). Running: 4366 4502 5482 6345 6349 (rolling slots).

## Stage J — wave 3 banking
- Logged at 2026-10-29 01:27 UTC
- Banked 13/25: 1946 2594 3116 3199 4347 4366 4502 5482 6345 6349 6419 6471 6822. Running: 6810 6902 7259 7962 8706. Hunters now told to use per-name scratch subfolders after one reported a shared-scratchpad filename collision.

## Stage J — panel STARTED
- Logged at 2026-10-29 01:47 UTC
- 25/25 hunts banked and scored (top 1946 +1.70, 5482 +1.20; bottom 3116/9202 -1.00; none above 2.8). 25 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-29 01:56 UTC
- 25 ranked: top 1946 +1.70, 5482 +1.20; bottom 3116/9202 -1.00; none above floor 2.8. Signs 13+/1 zero/11-. Panel 4/4 members, no fallback, 3 selected (1946 L 4/4, 3116 S 3/4, 6471 L 3/4). 9 names release in-session, 4366 unknown. Resolved 10-27 (lean_vs_free_control_rho 0.435). Judge-definition sizing rule conflicts with hunter-core (reported by opus55 judge), recorded in note. Note: japan/japan-note.md. No orders.

## Stage M — morning exit review — SKIPPED (fired after the open)
- Logged at 2026-10-29 13:47 UTC
- Routine scheduled 13:10 UTC (09:10 ET) fired at 13:46:56 UTC = 09:46 ET, 17 minutes after the open; slot reports inside_hours false. Per the skill no review was run and no advice compiled for 2026-10-29 (source run research/2026/10/2026-10-28/edge-panel exists). No orders placed.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-29 14:44 UTC
- Fired 14:43 UTC (scheduled 14:36). Sealing for event date 2026-10-30 (Fri, next European session). RUN research/2026/10/2026-10-30/europe/. Plan: universe -> baselines -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note. No orders.

## Stage EU — panel STARTED
- Logged at 2026-10-29 15:34 UTC
- 20/20 hunts banked (all search_complete true; scripts/hunt_status.py is absent from main, so the backstop check could not run). 18 ranked, GSJ and SCYR phantom dates (SCYR reports 2026-11-03 amc). None above floor 2.8. 18 packs, four judges.

## Stage EU — Europe researcher — DONE
- Logged at 2026-10-29 15:44 UTC
- Sealed for 2026-10-30 (Fri). 61 scheduled, 33 eligible, 20 hunted (es 6, no 5, de 2, fr 2, uk/se/dk/fi/pl 1). 18 ranked: top EBP +1.10, SAN +0.95; bottom ACX -1.20, GXI/TRIFOR -0.90; none above floor 2.8. GSJ and SCYR phantom dates (SCYR reports 2026-11-03 amc). Panel 4/4 members, no fallback, 2 selected: ACX short (4/4, pct 90), GXI short (3/4, 79). anchor_covered 4/20; es+pl 7 names. scripts/hunt_status.py absent from main (backstop not run; all 20 hunts search_complete true). No European run after 2026-10-16 is resolved; Nordic names from 10-19 on are near their ~12-day archive window. Note: europe/europe-note.md. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main).

## Edge hunt (panel) — 2026-10-29 amc + 2026-10-30 bmo — STARTED
- Logged at 2026-10-29 17:16 UTC
- Stage E-P fire 17:06 UTC (session start 17:09). Universe 167 names (117 amc 10-29, 50 bmo 10-30), baselines sealed for all 167 in edge-panel/baselines before any agent (17:16 UTC). Plan: one edge-sweep, up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.
