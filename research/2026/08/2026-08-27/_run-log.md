# Run log — 2026-08-27

## Stage 0 — universe (07:16 CET)
- Window: After the US close on Thursday 27 August 2026 through before the US open on Friday 28 August 2026
- Source: nasdaq (after-close and before-open, single source — `get_earnings.py` exited 0)
- Universe: 21 total (14 AMC, 7 BMO); 18 eligible after qualification
- Excluded: 3 (below_market_cap_floor: JFIN $0.12B, LFVN $0.09B, NA $0.05B)
- Notes: 7 above-floor names carry non-US domicile or sub-$10B market cap (FRO, HAFN,
  BWLP, MNSO, BBAR, CHA, FINV) — spot-checked each via WebSearch for a live listed-options
  market; all confirmed optionable (option-chain pages on Nasdaq/Yahoo/Seeking
  Alpha/Webull/etc.), so none excluded on that basis. No conflicting BMO/AMC timing
  found — only one source (nasdaq) was needed since it returned complete data for both
  sides of the window, so there was nothing to cross-check across.
