# Run log — 2026-09-10

## Stage 0 — universe (05:15 UTC / 07:15 CEST)
- Logged at 2026-09-10 05:18 UTC
- Window: After the US close on Thursday 10 September 2026 through before the US open on Friday 11 September 2026
- Source: nasdaq (after-close 12 rows, before-open 5 rows)
- Universe: 17 total (12 AMC, 5 BMO); 9 above the $500M market-cap floor; 8 eligible after qualification
- Excluded: 9 total — 8 below_market_cap_floor (IBEX, ZUMZ, AENT, HOFT, CMCM, RENT, CSBR, MNY); 1 unconfirmed_timing (REF — IPO'd 2026-07-30, ~6 weeks public, conflicting third-party earnings-date estimates with no official IR/8-K confirmation for today, listed-options market also unverified)
- Notes: DSGX, FEIM and LPTH sessions cross-checked against official IR/8-K sources (not just the calendar feed) since they are the thinnest names above the floor; all confirmed AMC today. 8 eligible is at/below triage.skip_if_universe_at_or_below (10), so stage 1 should be skipped and all 8 names should go straight to stage 2.

## Stage 1 — triage (08:38 CEST)
- Logged at 2026-09-10 06:41 UTC
- Mode: skipped (universe eligible 8 <= triage.skip_if_universe_at_or_below 10)
- Funnel: 17 universe -> 8 eligible -> 8 cleared floors -> 8 shortlisted
- Scouts: 0 subagents (screen skipped)
- Session mix: 7 AMC / 1 BMO
- Notable drops (from stage 0): REF (unconfirmed_timing), IBEX/ZUMZ/AENT/HOFT/CMCM/RENT/CSBR/MNY (below_market_cap_floor)
