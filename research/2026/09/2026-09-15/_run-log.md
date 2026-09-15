# Run log — 2026-09-15

## Stage 0 — universe (07:13 CEST)
- Logged at 2026-09-15 05:14 UTC
- Window: After the US close on Tuesday 15 September 2026 through before the US open on Wednesday 16 September 2026
- Source: nasdaq (after_close and before_open both ok, 17/23 raw rows)
- Universe: 4 total (2 AMC, 2 BMO); 2 eligible after qualification (TCOM, LUXE)
- Excluded: 2 (2 below_market_cap_floor: EPM $0.13B, ISPR $0.09B)
- Notes: Both eligible names verified against company IR releases for session/date and confirmed to have active listed-options markets (WebSearch, since WebFetch/curl to financial domains may be blocked). Eligible count (2) is at/below triage.skip_if_universe_at_or_below (10), so stage 1 will be skipped and both names go straight to stage 2.
