# Run log — 2026-08-21

## Stage 0 — universe (07:14 CEST)
- Window: After the US close on Friday 21 August 2026 through before the US open on Monday 24 August 2026
- Source: nasdaq (after-close and before-open feeds both `ok`)
- Universe: 6 total (0 AMC, 6 BMO); 3 eligible after qualification
- Excluded: 3 (below_market_cap_floor: XYF $0.30B, NCTY $0.07B, GGR $0.03B — all below the $500M floor)
- Eligible: PDD ($128.39B), XPEV ($11.46B), NSSC ($1.35B) — all BMO, confirmed for Monday 2026-08-24
- Qualification checks: BMO/AMC timing cross-checked via WebSearch against 3-4 independent sources per eligible name (Nasdaq feed, company IR/GlobeNewswire, StockTitan, TipRanks/Barchart/MarketScreener, Yahoo Finance); no conflicting timing found. Listed-options markets confirmed present for all three via option-chain listings (Nasdaq/Webull/Moomoo/TradingView).
- Notes: Friday run — feed correctly rolled the before-open side to Monday 2026-08-24, skipping the weekend. No after-close names today. Eligible count (3) is at/below `triage.skip_if_universe_at_or_below` (10), so stage 1 (triage) will be skipped per config — all 3 eligible names should pass straight through to stage 2 (deep dive).
