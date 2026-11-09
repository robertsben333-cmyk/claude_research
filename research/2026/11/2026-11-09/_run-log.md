# Run log — 2026-11-09

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-06 14:37 UTC
- Fired Fri 2026-11-06 14:36 UTC (15:36 Amsterdam, markets open; spots intraday). Sealing for next European session Mon 2026-11-09. Plan: universe (cap 20) -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note. Local main was a stale shallow clone diverged from force-updated origin/main; re-pointed to origin/main 1415d26e5.

## Stage EU — progress
- Logged at 2026-11-06 14:40 UTC
- Universe: 22 scheduled, 16 eligible, all 16 hunted (at/under cap 20). by_market uk2 de4 fr1 dk1 it6 es1 pl1; largest it 37.5%. Baselines sealed 16/16 (intraday spots Fri 14:4x UTC). Provenance stamped. Wave 1 launched: G1A HNR1 HYQ PAT NTG.

## Stage EU — progress
- Logged at 2026-11-06 14:49 UTC
- Wave 1 banked 5/5, all search_complete: G1A 0.0, HNR1 +1.0, HYQ -0.6, PAT +1.8 (session amc per issuer timestamps), NTG +0.55 (session amc per issuer). Wave 2 launched: ALM ALCLS DOV EGLA IOT. Note: publish.sh push was refused non-fast-forward while CI moved main (shallow clone); recovered with pull --rebase + push.

## Stage EU — progress
- Logged at 2026-11-06 14:54 UTC
- Wave 2: ALM -0.7, ALCLS 0 (no release in window, event_confirmed false; Cellectis releases amc and has not announced a Q3 date), DOV -0.1 (session amc per issuer timestamps), EGLA 0 (PHANTOM: board 2026-11-16 per issuer calendar). IOT running. Rolling into wave 3 at 5 concurrent: NWL PHN UCG TEN launched; KNOS REC queued.

## Stage EU — panel STARTED
- Logged at 2026-11-06 15:02 UTC
- 16/16 hunts banked, all search_complete. 13 ranked; ALCLS/EGLA/REC not ranked (no event in window: ALCLS no Q3 date announced, EGLA board 11-16, REC printed 11-06). None above floor 2.8. Top IOT +2.10, bottom TEN -0.90. Hunters re-read session as amc for PAT NTG DOV PHN NWL. 13 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-06 15:09 UTC
- Sealed for 2026-11-09 (Mon) at ~14:45 UTC Fri 11-06 (intraday spots). 22 scheduled, 16 eligible, all 16 hunted (no draw; it 6 largest, 37.5%), all search_complete. 13 ranked; ALCLS (no Q3 date), EGLA (phantom, board 11-16), REC (duplicate of 11-06 interims) not ranked. Top IOT +2.10, bottom TEN -0.90; none above floor 2.8.
- Panel: 4/4 members, 13/13 each, no fallback. Selected IOT long 3/4 (panel_pct 88).
- Six names re-sessioned amc by hunters (PAT NTG DOV PHN NWL[10-11 08:05] TEN); resolve after 11-10. anchor_covered 4/16; es 1, pl 1, de 4. publish.sh's own push failed non-fast-forward twice (CI moving main); recovered with pull --rebase. Pushing to main (EARNINGS_DATA_BRANCH=main).

## Close AMC — 2026-11-09
- Logged at 2026-11-09 11:22 UTC
- Guard passed (exit_mode amc_open, amc exit as market DAY). verify: 14 legs, none held, none UNFILLED. close --submit: no leg with exit date today, nothing sent. Fill check ran clean. Fired 11:15 UTC (06:15 ET), before open.
