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

## Stage 3 — advice published
- Logged at 2026-08-27 16:10 UTC
- 04-advice.md / .json written: ESTC Neutral/No Edge (High certainty, High reversal risk), AFRM Neutral/No Edge (Med certainty, High reversal risk)
- Ranked field includes S, MRVL, RBRK (deep-dived but not panelled) plus a not_researched entry for IREN

## Stage 4 — calibration — FINISHED
- Logged at 2026-09-01 06:27 UTC
- Logged at 2026-09-01 06:27 UTC (scheduled run, 2026-09-01)
- Scored today. All 5 close prices sourced from stockanalysis.com history tables, cross-checked against at least one independent source (CNBC, TipRanks, Barchart, Seeking Alpha, StockStory) for direction/magnitude.
- ESTC (panelled, High certainty): +19.31% (close $83.74 -> $99.91), a miss under the below-expected-move convention (19.31% >> 13.4% expected), inside its 6.7-27.8% band, broke the 12.9% implied move. Beat-and-raise -- the opposite of the beat-then-fall pattern the panel's red-team case leaned on. Preliminary read (-20) also wrong -- a rare case where both methods missed together.
- AFRM (panelled, Med certainty): +0.35% (close $77.49 -> $77.76), a clean hit (0.35% < 10.8% expected); popped +8.34% after hours then faded to nearly flat, consistent with the panel's own split-panel logic that direction hinged on the credit/margin guide, not the near-certain beat. Preliminary read (-18) is a technical miss on a functionally flat print.
- S (non-panelled, prelim -15): -5.15%, preliminary hit. MRVL (non-panelled, prelim -15/Lean Down): -10.28%, preliminary hit -- initial Alphabet-deal pop reversed to a priced-for-perfection selloff. RBRK (non-panelled, prelim -10): -13.05%, preliminary hit -- ran up into the print then sold the news hard.
- IREN excluded (shortlisted but never researched -- stage 2 batch 2 stalled, logged 2026-08-27).
- Certainty-tier signal is no longer a single data point: High-certainty calls are now 1/3 (OKTA miss, DLTR hit, ESTC miss) against Med-certainty 2/2 (WOLF, AFRM) -- two independent High-certainty misses share the same mechanism (certainty driven by alignment around a historical beat-then-X narrative that broke this quarter). Flagged prominently in LEDGER.md as a standing concern for scripts/synthesize.py's certainty scoring, not yet acted on.
- Wrote 05-outcome.md / 05-outcome.json. Updated LEDGER.md (running totals: panelled 3/5, prelim 8/13). Rebuilt PREDICTIONS.csv/json (13 predictions, 13 scored, 60% panelled hit rate).
