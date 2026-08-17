# Run log — 2026-08-17

## Stage 0 — universe
- Logged at 2026-08-17 09:16 UTC
- Window: After the US close on Monday 17 August 2026 through before the US open on Tuesday 18 August 2026
- Source: nasdaq (after-close and before-open both ok, no fallback needed)
- Universe: 22 total (7 AMC, 15 BMO); 12 above the $500M market-cap floor; 11 eligible after qualification
- Excluded: 11 total — 10 below_market_cap_floor (FLXS, HSAI, PRE, DUOT, DCGO, ELTK, THCH, PRPO, UCL, EVGN); 1 no_options_market (ENRD — listed Jun 2026, too new to have an options market per Nasdaq/aggregator check)
- Notes: catch-up run fired by hand on 2026-08-17; scheduled Routines had not fired since 2026-08-13 (2026-08-14 and today's 05:12 UTC firing both produced nothing). Pulled main first per config/pipeline.yaml updates from 08-13 (shortlist_size now 6, panel.names now 2). No conflicting BMO/AMC timing found (single source nasdaq for both sides).

## Stage 1 — triage
- Logged at 2026-08-17 09:21 UTC
- Mode: scouted (universe 11 eligible > skip_if_universe_at_or_below 10)
- Funnel: 22 universe -> 11 eligible -> 11 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium), 11 names in one batch
- shortlist_size is 6 as of the 2026-08-13 budget cut (config/pipeline.yaml verified against the fire payload's claim)
- Session mix: 1 AMC (FN) / 5 BMO (VNET, KLAR, PONY, BIDU, AS) -- real tilt, not corrected, flagged for stage 2
- Notable drops (cleared floors, cut on rank): IQ (50.80), XP (49.50), YALA (49.15), HD (47.85), RNW (42.25)
- Evidence quality: thin across the board; no expected_move_hint could be sourced for any name -- left null, not fabricated

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-08-17 10:24 UTC
- Batch 1 never ran today: no 02-dossiers/ files and no Stage 2 batch 1 section in the run log. Covering both halves per fallback rule.
- Tickers (all 6, priority order): FN, VNET, KLAR, PONY, BIDU, AS
- Plan: 3 waves of 2 opus/high researchers (FN+VNET, KLAR+PONY, BIDU+AS), publish after each wave and after each dossier
- Cap: shortlist_size=6 for the day as a whole -- researching all 6 does not exceed it
