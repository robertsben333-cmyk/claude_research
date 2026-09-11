# Run log — 2026-09-11

## Stage 0 — universe (07:30 CEST)
- Logged at 2026-09-11 05:16 UTC
- Window: After the US close on Friday 11 September 2026 through before the US open on Monday 14 September 2026 (Friday roll to Monday, correct).
- Source: nasdaq (get_earnings.py exit 0).
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification.
- Excluded: 3, all below_market_cap_floor (CODA $112.9M, RFIL $110.7M, HAIN $57.9M vs $500M floor) -- not close calls, corroborated independently.
- CSHR ($0.70B) passed floor; options listing and BMO timing for 2026-09-14 cross-confirmed via WebSearch against the company's own press release. No network issues, no holiday.
- Stage 1 will be SKIPPED: 1 eligible name is at or below triage.skip_if_universe_at_or_below (10) -- CSHR goes straight to the deep-dive stage per config.
