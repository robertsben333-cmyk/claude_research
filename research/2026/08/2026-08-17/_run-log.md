# Run log — 2026-08-17

## Stage 0 — universe
- Logged at 2026-08-17 09:16 UTC
- Window: After the US close on Monday 17 August 2026 through before the US open on Tuesday 18 August 2026
- Source: nasdaq (after-close and before-open both ok, no fallback needed)
- Universe: 22 total (7 AMC, 15 BMO); 12 above the $500M market-cap floor; 11 eligible after qualification
- Excluded: 11 total — 10 below_market_cap_floor (FLXS, HSAI, PRE, DUOT, DCGO, ELTK, THCH, PRPO, UCL, EVGN); 1 no_options_market (ENRD — listed Jun 2026, too new to have an options market per Nasdaq/aggregator check)
- Notes: catch-up run fired by hand on 2026-08-17; scheduled Routines had not fired since 2026-08-13 (2026-08-14 and today's 05:12 UTC firing both produced nothing). Pulled main first per config/pipeline.yaml updates from 08-13 (shortlist_size now 6, panel.names now 2). No conflicting BMO/AMC timing found (single source nasdaq for both sides).
