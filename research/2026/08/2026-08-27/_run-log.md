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

## Stage 2 — deep dive, batch 1
- Logged at 2026-08-27 08:52 UTC
- Researched: AFRM, S, MRVL
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high (2 waves: AFRM+S, then MRVL), published per-dossier
- Median evidence completeness: 84/100 (AFRM 82, S 84, MRVL 85)
- Note: S researcher flags the triage selection_rationale's PANW read-through as wrong — PANW reports 2026-09-01, after S; the live peer read is CRWD and OKTA (both reported 2026-08-26 amc)
- Panel-eligible after this batch: not computed — ranking runs after the final batch (batch 2)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-08-27 10:23 UTC
- Shortlist: 6 names; this batch: RBRK, ESTC, IREN
- Already on disk, skipping: AFRM, S, MRVL (batch 1)
- Plan: 2 waves (wave 1: RBRK, ESTC; wave 2: IREN), 2 opus/high researchers per wave, publish after each wave

## Stage 3 — panel prep: ranking recovered (STARTED)
- Logged at 2026-08-27 15:54 UTC
- Stage 2 batch 2 never closed: logged STARTED (RBRK, ESTC, IREN) but no FINISHED/HALTED entry; IREN dossier missing.
- Built 02-ranking.json from the 5 dossiers that exist (AFRM, S, MRVL, RBRK, ESTC) per panel.rank_by; all 5 panel-eligible.
- Ranked: ESTC 53.4, AFRM 52.8, S 51.75, MRVL 51.5, RBRK 49.85
- panel.names=2 (config default, already at first degrade_order step) -> panelling ESTC, AFRM

## Stage 3 — panel & advice (17:5x CEST)
- Logged at 2026-08-27 16:09 UTC
- Panelled: ESTC, AFRM (top 2 of 5 eligible per rebuilt 02-ranking.json; panel.names=2)
- Refreshed price anchors before panelling: ESTC spot 79.25->84.66 (+6.83% intraday), implied move kept at stage-2's derived 12.9% (could not re-derive the two-expiry decomposition intraday; raw monthly re-check 17.54%). AFRM spot 76.46->76.99, implied move re-confirmed unchanged at 10.55%.
- ESTC: aligned panel (disparity 8.7), consensus -20.7 -> Neutral / No Edge (just short of Lean Down), certainty High, reversal risk High (72, red-team).
- AFRM: split panel (disparity 28.0, 4 up/3 down), consensus -0.1 -> Neutral / No Edge, certainty Med, reversal risk High (65, red-team).
- Panel seats filled: 14/14 (7/7 each, no retries needed)
- Chair overrides: none
- Degradations: none beyond the already-configured panel.names=2 default
