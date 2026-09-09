# Run log — 2026-09-09

## Stage 0 — universe (07:16 CEST)
- Logged at 2026-09-09 05:18 UTC
- Window: After the US close on Wed 2026-09-09 through before the US open on Thu 2026-09-10
- Source: nasdaq (both after-close and before-open feeds returned ok)
- Universe: 20 total (11 AMC, 9 BMO); 8 above the $500M market-cap floor; 7 eligible after qualification
- Excluded: 13 (12 below_market_cap_floor; 1 no_options_market — YB, a Sept-2026 Chinese-ADR IPO with no listed contracts on Nasdaq's option-chain page and a 31M-share float)
- Confirmed BMO/AMC timing and options market by web search for the three newer/smaller eligible names: NAVN and WLTH sessions confirmed via company BusinessWire/GlobeNewswire releases and their Nasdaq/Yahoo/Barchart option chains; TEN's BMO 09-10 confirmed via TEN Ltd.'s own GlobeNewswire release, options market assumed from its long NYSE listing (no chain data surfaced in search, noted for stage 1/2 awareness)
- COO, AVAV, M, AEO not independently re-verified beyond the nasdaq feed — large, long-listed, obviously optionable names; verification effort spent on the borderline/newer tickers instead

## Stage 1 — triage (06:40 UTC)
- Logged at 2026-09-09 06:41 UTC
- Mode: skipped (universe 7 <= threshold 10)
- Funnel: 20 universe -> 7 eligible -> 7 cleared floors -> 7 shortlisted
- Scouts: 0 subagents (skip mode, no scoring)
- Session mix: 5 AMC / 2 BMO
- Notable drops: YB (no_options_market, dropped at stage 0, not by triage)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-09 08:25 UTC
- Shortlist: 7 names, all priority_score=null (stage 1 ran in skip mode, universe<=10). Capped to triage.shortlist_size=6 by shortlist order (market-cap descending); dropped TEN (smallest cap, and stage 0 flagged its options-chain data as unconfirmed).
- This batch (1 of 2): COO, AVAV, NAVN
- Batch 2 will cover: M, AEO, WLTH
- Already on disk, skipping: none
- Plan: waves of deep_dive.wave_size=2 opus/high researchers (COO+AVAV, then NAVN alone), publish after each wave
