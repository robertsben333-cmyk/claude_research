# Run log — 2026-08-19

## Stage 0 — universe (07:16 CET)
- Window: After the US close on Wednesday 19 August 2026 through before the US open on Thursday 20 August 2026
- Source: nasdaq
- Universe: 36 total (12 AMC, 24 BMO); 22 eligible after qualification
- Excluded: 14 (13 below_market_cap_floor: TWIN, UFI, FLX, SLSN, ARAY, CCIF, JG, BOSC, EVAX, BEEM, HUIZ, YJ, KRKR; 1 no_options_market: AIIR — Air Global PLC, IPO'd on Nasdaq ~2026-05-21, no dedicated options-chain page found on Nasdaq/Barchart/Yahoo despite WebSearch, too recent a listing to have a real options market yet)
- Notes: get_earnings.py returned status ok on first attempt (exit 0), no fallback needed. All timing (BMO/AMC) came from a single source (nasdaq) with no cross-source conflicts to check; no company had an unknown session. Options-market qualification for the smaller/foreign-ADR names above the cap floor (ATAT, DAO, AIIR, RERE, DDL, IOND) was verified via WebSearch rather than assumed: ATAT, DAO (thin: put vol 3 / call vol 0), RERE, DDL, and IOND all confirmed optionable across Yahoo/Barchart/Webull/moomoo; AIIR was the only one with no evidence of a listed options market.
