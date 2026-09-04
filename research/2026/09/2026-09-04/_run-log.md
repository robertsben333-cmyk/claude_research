# Run log — 2026-09-04

## Stage 0 — universe (07:19 CEST)
- Logged at 2026-09-04 05:18 UTC
- Window: After the US close on Friday 04 September 2026 through before the US open on Tuesday 08 September 2026 (Monday 07 Sep is Labor Day; roll to Tuesday handled by get_earnings.py)
- Source: nasdaq (after-close + before-open)
- Universe: 5 total (0 AMC, 5 BMO); 2 eligible after qualification
- Excluded: 3 (below_market_cap_floor: WDH $0.35B, CAN $0.24B, GMHS $0.05B)
- Eligible: ABM, UNFI — both NYSE-listed, real listed-options markets, BMO timing cross-checked via WebSearch against a second independent source (investing.com for ABM, company press release for UNFI)
- Notes: three-day trading gap ahead of the window (Labor Day) means the before-open side rolls all the way to Tuesday 08 Sep; nothing else odd.

## Stage 1 — triage (06:40 UTC)
- Logged at 2026-09-04 06:40 UTC
- Mode: skipped (universe eligible=2 <= threshold 10)
- Funnel: 5 universe -> 2 eligible -> 2 cleared floors (not screened) -> 2 shortlisted
- Scouts: 0 subagents (skipped)
- Session mix: 0 AMC / 2 BMO
- Notable drops: WDH (below $500M cap floor), CAN (below $500M cap floor), GMHS (below $500M cap floor) — all excluded by stage 0, not triage
