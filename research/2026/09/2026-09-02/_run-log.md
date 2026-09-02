# Run log — 2026-09-02

## Stage 0 — universe (07:18 CEST / 05:18 UTC)
- Logged at 2026-09-02 05:19 UTC
- Window: After the US close on Wednesday 02 September 2026 through before the US open on Thursday 03 September 2026
- Source: nasdaq (both after-close and before-open, single-source feed, status ok)
- Universe: 31 total (16 AMC, 15 BMO); 24 above the $500M market-cap floor; 23 eligible after qualification
- Excluded: 8 (7 below_market_cap_floor: GCO, LE, MTRX, CHPT, DLTH, TLYS, AMBR; 1 no_options_market: WLYB — WebSearch-confirmed no listed-options chain, WLY class A kept)
- Verified by WebSearch: GOLD is A-Mark Precious Metals' Dec-2025 NYSE rebrand (real listed name, not a data error); VSXY is Victoria's Secret & Co's post-rename ticker (was VSCO); VBNK, ZGN, NTSK, MEI, AGX all confirmed to have real listed-options markets; AGX's Sept 2 AMC timing confirmed by company press release
- Notes: local main branch was behind origin/main by a full day of pipeline commits at session start (shallow-clone merge-base artifact, not a real divergence); fast-forwarded cleanly before starting this stage

## Stage 1 — triage — STARTED
- Logged at 2026-09-02 06:39 UTC
- Screening 23 eligible names via 2 earnings-triage-scout subagents (batches of ~12), floors change_expectation>=35 / ai_edge>=30, shortlist_size 6

## Stage 1 — triage (06:46 UTC)
- Logged at 2026-09-02 06:43 UTC
- Mode: scouted (2 subagents, sonnet/medium)
- Funnel: 31 universe -> 23 eligible -> 19 cleared floors -> 6 shortlisted
- Session mix: 5 AMC / 1 BMO (VSXY swapped in for WOOF on session-mix grounds, 0.65pt gap)
- Notable drops: NTSK (tradeable:false, thin options liquidity), DOO (timing_confirmed:false, conflicting date/listing), VBNK (tradeable:false, thin liquidity), BRC (change_expectation 30<35), HPE/CIEN (tied 8th at 60.50, just missed cut)
