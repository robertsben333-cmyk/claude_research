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

## Close AMC — 2026-11-02
- Logged at 2026-11-02 11:18 UTC
- 11:15 UTC (06:15 ET). Guard mode --require-exit-tif opg exit 0 (amc_open, placement matched, tif day). verify: 14 legs, none held, no UNFILLED. close --submit: no leg due today, nothing sent, windows {} (the close process then lingered past 5 min and was killed). No refusals; account reachable.

## Stage M — morning exit review — SKIPPED (after open)
- Logged at 2026-11-02 14:57 UTC
- Fired 2026-11-02 14:56 UTC = 09:56 ET, 46 min after its 09:10 ET schedule (14:10 UTC) and 27 min after the open; morning.py slot inside_hours=false. No picks, no analysts, no advice. Source run research/2026/10/2026-10-30/edge-panel exists. Previous morning not scored on this fire.

## Edge hunt (panel) — 2026-11-02 amc + 2026-11-03 bmo — STARTED
- Logged at 2026-11-02 18:15 UTC
- Stage E-P fire 18:06 UTC (13:06 ET, EST since 11-01; CRON_TZ NY). Universe 199 names (103 amc 11-02, 96 bmo 11-03), baselines sealed for all 199 in edge-panel/baselines before any agent (18:15 UTC). share_classes_folded empty although CRD.A/CRD.B and LBTYA/B/K are on the calendar; edge_score.py's fold applies. Plan: one edge-sweep, up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-02 18:19 UTC
- Sweep finished 18:18 UTC (20 of 199 checked): 16 company-confirmed with session settled (amc 11-02: AEHR ICHR LIFE INSP HNGE MTCH IBTA VRTX AAPL ROKU; bmo 11-03: VITL BETA UPST CHGG DOCN SHOP), 4 unconfirmed (EBS HLF BRCC PLTR), 0 phantoms, 179 unchecked. Cap 20 = all 20 checked hunted; 179 unchecked shed. Sweep wrote a stray 'SHOP-checked' into unchecked_names, removed. Searchers unpriced-searcher, amc first, at most 8 per turn. Wave 1: AEHR ICHR LIFE INSP HNGE MTCH IBTA VRTX.

## Edge hunt (panel) — step 3u
- Logged at 2026-11-02 18:27 UTC
- IBTA searcher hit the per-turn WebSearch budget (~19:00 UTC per its hand-back); hunt_status check --apply marked it UNFINISHED, retry moved it to hunts/_unfinished/, fresh searcher relaunched in a later turn. All other returned hunts finished (AEHR HNGE ICHR INSP LIFE MTCH VRTX).

## Edge hunt (panel) — waves 2-3
- Logged at 2026-11-02 18:33 UTC
- All 20 names launched by 18:34 UTC (relaunched as slots freed, 8 concurrent). Returned and finished so far: AEHR HNGE ICHR INSP LIFE MTCH VRTX ROKU IBTA(relaunch) AAPL EBS HLF. EBS and HLF confirmed amc 11-02 by company notices the sweep missed. Out: BRCC PLTR VITL BETA UPST CHGG DOCN SHOP.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-11-02 18:38 UTC
- 20/20 searchers returned by 18:38 UTC (unpriced-searcher, native, Opus 5.5). hunt_status check --apply: 0 unfinished of 20 (IBTA's first hunt hit the per-turn WebSearch budget, was retried and the relaunch finished). Sweep-unconfirmed EBS HLF BRCC PLTR all confirmed amc 11-02 by company releases. mode: execution enabled, amc_open. flatten --submit at 18:38 UTC: 1 position held (TSEM 37, -4.41% unrealised), closed; account flat.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-02 18:38 UTC
- 20 packs, four judges, one part. edge_score and V2 grounded written ~18:40 UTC, before the first print.
