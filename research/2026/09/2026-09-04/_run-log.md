# Run log — 2026-09-04

## Stage 0 — universe (07:19 CEST)
- Logged at 2026-09-04 05:18 UTC
- Window: After the US close on Friday 04 September 2026 through before the US open on Tuesday 08 September 2026 (Monday 07 Sep is Labor Day; roll to Tuesday handled by get_earnings.py)
- Source: nasdaq (after-close + before-open)
- Universe: 5 total (0 AMC, 5 BMO); 2 eligible after qualification
- Excluded: 3 (below_market_cap_floor: WDH $0.35B, CAN $0.24B, GMHS $0.05B)
- Eligible: ABM, UNFI — both NYSE-listed, real listed-options markets, BMO timing cross-checked via WebSearch against a second independent source (investing.com for ABM, company press release for UNFI)
- Notes: three-day trading gap ahead of the window (Labor Day) means the before-open side rolls all the way to Tuesday 08 Sep; nothing else odd.

## Stage 1 — triage (10:31 CEST, run by stage 2 session — stage 1 Routine had not published)
- Logged at 2026-09-04 08:29 UTC
- Mode: skipped (universe 2 <= threshold 10)
- Funnel: 5 universe -> 2 eligible -> 2 cleared floors -> 2 shortlisted
- Scouts: 0 (screen skipped)
- Session mix: 0 AMC / 2 BMO
- Notable drops: none (stage 0 already excluded WDH, CAN, GMHS below market-cap floor)
- Note: 01-shortlist.json was absent when this session started (~2h after stage 1's scheduled 08:38 CEST fire); ran earnings-triage inline per earnings-deep-dive step 1's guidance rather than block stage 2

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-04 08:29 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: ABM
- Already on disk, skipping: none
- Plan: 1 wave of 1 opus/high researcher (ABM), publish after the wave

## Stage 2 — deep dive, batch 1 — FINISHED (08:50 UTC)
- Logged at 2026-09-04 08:51 UTC
- Researched: ABM
- Skipped (already done): none
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1
- Median evidence completeness: 80/100
- Panel-eligible after this batch: N/A (ranking runs after the final batch)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-04 10:26 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: UNFI
- Already on disk, skipping: ABM (batch 1 completed)
- Plan: 1 wave of 1 opus/high researcher (UNFI), publish after the wave
