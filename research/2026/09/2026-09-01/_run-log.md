# Run log — 2026-09-01

## Stage 0 — universe (07:17 CEST)
- Logged at 2026-09-01 05:19 UTC
- Window: After the US close on Tuesday 01 September 2026 through before the US open on Wednesday 02 September 2026
- Source: nasdaq (both after-close and before-open legs)
- Universe: 16 total (6 AMC, 10 BMO); 13 above the $500M market-cap floor; 12 eligible after qualification
- Excluded: 4 — GASS/YSG/SPWH below_market_cap_floor; BF.A no_options_market (Class A voting shares carry no active listed-options chain; BF.B, the optionable class, is kept)
- Notes: single-source fetch (nasdaq) succeeded on both legs with no network issues; no conflicting BMO/AMC timing observed to adjudicate. Verified options-market status for the six sub-$2B eligible names (CXM, FCEL, GIII, REX, DAKT) plus the BF.A/BF.B split via WebSearch since the API does not report it; all confirmed via option-chain listings. 12 eligible is above triage.skip_if_universe_at_or_below (10), so stage 1 will trigger.
