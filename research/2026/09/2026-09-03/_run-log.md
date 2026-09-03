# Run log — 2026-09-03

## Stage 0 — universe — 07:22 CET
- Logged at 2026-09-03 05:22 UTC
- Window: After the US close on Thursday 03 September 2026 through before the US open on Friday 04 September 2026
- Source: nasdaq (after-close + before-open)
- Universe: 21 total (20 AMC, 1 BMO); 13 eligible after qualification
- Excluded: 8, all below_market_cap_floor ($500M floor) — none excluded for options/timing
- Notes: all 13 above-floor names hand-verified for a real listed options market and single-source-confirmed BMO/AMC session (Nasdaq option-chain listings + company IR press releases for IOT and OXM, cross-checked against TipRanks/StockTitan/Investing.com). No conflicting timing found. Stage 1 (triage) will trigger: 13 eligible > skip_if_universe_at_or_below (10).
