# Run log — 2026-08-18

## Stage 0 — universe (07:15 CET)
- Window: After the US close on Tuesday 18 August 2026 through before the US open on Wednesday 19 August 2026
- Source: nasdaq
- Universe: 29 total (11 AMC, 18 BMO); 21 eligible after qualification
- Excluded: 8 (7 below_market_cap_floor: AUNA, DVLT, TOYO, ANTA, AXIL, IRIX, IQST; 1 no_options_market: AAPG — recent Chinese-biotech US listing, no dedicated options-chain page found on Nasdaq/Barchart, confirmed via WebSearch)
- Notes: get_earnings.py returned status ok on first attempt (exit 0), no fallback needed. All timing (BMO/AMC) came from a single source (nasdaq) with no cross-source conflicts to check. Options-market qualification for the 9 smaller/foreign-ADR names (AAPG, DRD, KC, FLNG, LU, WB, ZIM, OPRA, YMM) was verified via a WebSearch subagent rather than assumed; all confirmed optionable except AAPG.

## Stage 1 — triage (13:05 CET)
- Mode: scouted (universe 21 > threshold 10)
- Funnel: 29 universe -> 21 eligible -> 14 cleared floors -> 6 shortlisted
- Scouts: 2 subagents (sonnet/medium), batches of 15 and 6
- Session mix: 2 AMC (MRCY, TOL) / 4 BMO (OPRA, VIK, WB, FLNG)
- Notable drops: TGT (68/62, highest raw score in the batch, timing_confirmed false), ZIM (70/45, largest change_expectation in the universe, timing_confirmed false), EL (65/55, timing_confirmed false), LOW (45/50, timing_confirmed false), KC (60/25, not tradeable + ai_edge below floor), LU (60/30, timing_confirmed false, conflicting date sources), JKHY (25/30, both scores weakest in the batch)
- Warning for stage 2: OPRA, WB, and FLNG all came back `evidence: thin` from the scout pass — deep-dive researchers should expect real sourcing legwork rather than scout citations. TGT and ZIM were the two largest raw movers in the entire universe and were dropped purely on unconfirmed timing, not on merit.
