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

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-10 08:27 UTC
- Shortlist: 8 names, all priority_score null (stage 1 ran in skip mode, unscored). Capped to triage.shortlist_size=6 using market cap as tie-break (already the shortlist's own order); dropped for cap: FEIM ($0.73B), LPTH ($0.67B) — smallest two, documented per skill step 1.
- This batch: ORCL, ADBE, KR (positions 1-3 of the capped 6; N=ceil(6/2)=3)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (deep_dive.wave_size=2), publish after each wave and after each dossier
