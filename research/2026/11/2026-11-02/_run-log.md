# Run log — 2026-11-02

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-30 15:35 UTC
- Fired 15:34 UTC 2026-10-30 (scheduled 14:35 UTC = 15:30 Amsterdam). Sealing for event date 2026-11-02 (Mon, next European session). RUN research/2026/11/2026-11-02/europe/. Plan: universe -> baselines -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note. No orders. Local main had been force-diverged from origin (52/52, clean tree); reset to origin/main via checkout -B.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-30 15:41 UTC
- Event date 2026-11-02 (Mon). 15 scheduled, 9 eligible, 9 hunted (all eligible, under cap 20): uk ADVT, de AAD, fr COFA, se ACAD, no BAKKA, fi FRAMERY, it LTMC, es GRF, pl LBW; dk 0. Largest market share 11%, 9 markets. amc: AAD, GRF, LTMC (window 11-02 close -> 11-03 close). session_unresolved: COFA, LBW, ADVT. anchor_covered 1/9 (ACAD). es+pl 2 names. Baselines sealed ~15:40 UTC Fri at intraday spots. Provenance stamped (orchestrator claude-opus-5-5). scripts/hunt_status.py absent from main, backstop cannot run. Wave 1: AAD ACAD ADVT BAKKA COFA.

## Stage EU — panel STARTED
- Logged at 2026-10-30 15:59 UTC
- 9/9 hunts banked, all search_complete true. 8 ranked (LBW phantom date: issuer calendar says Q3 report 2026-11-30). None above floor 2.8. Session corrections by hunters: COFA reports amc (17:35 Paris) not bmo; ADVT bmo confirmed 07:00 London. 8 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-30 16:05 UTC
- Sealed for 2026-11-02 (Mon). 15 scheduled, 9 eligible, 9 hunted (one each uk de fr se no fi it es pl). 8 ranked: top COFA +1.30, AAD +1.10; bottom GRF -1.50, ACAD -0.40; none above floor 2.8. LBW phantom date (issuer calendar: Q3 report 2026-11-30). COFA reports amc (17:35 Paris), sealed bmo? - resolve both windows. Panel 4/4 members, no fallback, 1 selected: AAD long (3/4, pct 89). anchor_covered 1/9 (ACAD); es+pl 2 names. hunt_status.py absent; all 9 search_complete true. Note: europe/europe-note.md. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main).
