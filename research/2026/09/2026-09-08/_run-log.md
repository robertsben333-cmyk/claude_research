# Run log — 2026-09-08

## Stage 0 — universe (07:17 CEST / 05:17 UTC)
- Logged at 2026-09-08 05:17 UTC
- Window: After the US close on Tuesday 08 September 2026 through before the US open on Wednesday 09 September 2026
- Source: nasdaq (after-close and before-open both single-source, clean fetch, exit 0)
- Universe: 24 total (7 AMC, 17 BMO); 15 above the $500,000,000 market-cap floor; 15 eligible after qualification
- Excluded: 9, all below_market_cap_floor (CAL $0.41B, JILL $0.29B, PPIH $0.22B, OCC $0.12B, NNOX $0.06B, MIND $0.04B, DXLG $0.03B, YQ $0.03B, CRMT $0.02B)
- Notes: session timing (BMO/AMC) single-sourced from nasdaq, no cross-source conflicts to check. Options-market qualification verified via WebSearch for the four recent listings among the 15 eligible (SUNB, JMKE, TTAN, SAIL) — all confirmed to have live options chains; the remaining 11 (CASY, CHWY, CNM, KFY, BRZE, SIG, ASO, INNV, AVO, ODD, CGNT) are established long-listed names treated as eligible by inspection, consistent with prior practice. No OTC, SPAC-remnant, or duplicate-share-class names in the above-floor set. Eligible count (15) exceeds triage.skip_if_universe_at_or_below (10), so stage 1 will run normally today.

## Stage 1 — triage — STARTED
- Logged at 2026-09-08 06:39 UTC
- 15 eligible names, above skip threshold (10). Spawning 1 earnings-triage-scout (batch_size=15 covers all 15 in one batch).
