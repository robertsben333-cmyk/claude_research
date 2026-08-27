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

## Stage 1 — triage (11:08 CET)
- Mode: scouted (universe 18 > threshold 10)
- Funnel: 21 universe -> 18 eligible -> 18 cleared floors -> 6 shortlisted
- Scouts: 2 subagents (sonnet/medium), 9 tickers each
- Session mix: 6 AMC / 0 BMO — full AMC tilt, see 01-shortlist.md warning
- Notable drops (ranked out, none floor-failed): GAP (63.25), ULTA (60.50), PD (58.85),
  FRO (57.25, best BMO candidate), HAFN (57.25)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-08-27 08:23 UTC
- Tickers: AFRM, S, MRVL
- Plan: 2 waves (wave 1: AFRM, S; wave 2: MRVL), 2 opus/high researchers per wave, publish after each wave
