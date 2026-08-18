# Run log — 2026-08-18

## Stage 0 — universe (07:15 CET)
- Window: After the US close on Tuesday 18 August 2026 through before the US open on Wednesday 19 August 2026
- Source: nasdaq
- Universe: 29 total (11 AMC, 18 BMO); 21 eligible after qualification
- Excluded: 8 (7 below_market_cap_floor: AUNA, DVLT, TOYO, ANTA, AXIL, IRIX, IQST; 1 no_options_market: AAPG — recent Chinese-biotech US listing, no dedicated options-chain page found on Nasdaq/Barchart, confirmed via WebSearch)
- Notes: get_earnings.py returned status ok on first attempt (exit 0), no fallback needed. All timing (BMO/AMC) came from a single source (nasdaq) with no cross-source conflicts to check. Options-market qualification for the 9 smaller/foreign-ADR names (AAPG, DRD, KC, FLNG, LU, WB, ZIM, OPRA, YMM) was verified via a WebSearch subagent rather than assumed; all confirmed optionable except AAPG.
