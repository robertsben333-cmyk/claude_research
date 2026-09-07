# Run log — 2026-09-07

## Stage 0 — universe (07:15 CEST / 05:15 UTC)
- Logged at 2026-09-07 05:17 UTC
- Window: After the US close on Monday 07 September 2026 through before the US open on Tuesday 08 September 2026
- Source: nasdaq (after-close and before-open both single-source, clean fetch, exit 0)
- Universe: 6 total (1 AMC, 5 BMO); 2 eligible after qualification (ABM, UNFI)
- Excluded: 4, all below_market_cap_floor (WDH $0.36B, CAN $0.30B, DLNG $0.13B, GMHS $0.04B)
- Notes: 2026-09-07 is Labor Day (reference_is_trading_day: false in the feed); the nasdaq calendar still returned a same-day AMC row (DLNG) despite the holiday -- treated as a calendar-dated event, not a market-hours artifact, and excluded anyway on market cap. Both eligible names (ABM, UNFI) verified via WebSearch for real listed options markets and confirmed, non-conflicting BMO timing; UNFI's fiscal_quarter_ending label from the feed (Jul/2026) undercounts -- this is actually UNFI's Q4/FY2026 print, noted in 00-universe.md but not a qualification issue since timing is not in conflict.
