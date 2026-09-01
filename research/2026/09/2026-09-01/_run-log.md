# Run log — 2026-09-01

## Stage 0 — universe (07:17 CEST)
- Logged at 2026-09-01 05:19 UTC
- Window: After the US close on Tuesday 01 September 2026 through before the US open on Wednesday 02 September 2026
- Source: nasdaq (both after-close and before-open legs)
- Universe: 16 total (6 AMC, 10 BMO); 13 above the $500M market-cap floor; 12 eligible after qualification
- Excluded: 4 — GASS/YSG/SPWH below_market_cap_floor; BF.A no_options_market (Class A voting shares carry no active listed-options chain; BF.B, the optionable class, is kept)
- Notes: single-source fetch (nasdaq) succeeded on both legs with no network issues; no conflicting BMO/AMC timing observed to adjudicate. Verified options-market status for the six sub-$2B eligible names (CXM, FCEL, GIII, REX, DAKT) plus the BF.A/BF.B split via WebSearch since the API does not report it; all confirmed via option-chain listings. 12 eligible is above triage.skip_if_universe_at_or_below (10), so stage 1 will trigger.

## Stage 1 — triage
- Logged at 2026-09-01 06:43 UTC
- Mode: scouted (1 scout, batch of 12 — universe fit within triage.batch_size of 15)
- Funnel: 16 universe -> 12 eligible -> 10 tradeable -> 9 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium)
- Session mix: 4 AMC / 2 BMO
- Notable drops: FCEL (ai_edge 25 < floor 30, high-beta but unforecastable), REX & DAKT (tradeable: false, thin options liquidity), PANW (tied 50.5 with GIII on priority_score, dropped for AMC/BMO balance), OLLI (47.25, below cut), BF.B (37.25, formulaic quarter)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-01 08:24 UTC
- Shortlist (6, cap=triage.shortlist_size=6, no names dropped for cap): CRDO, MDB, GTLB, DELL, CXM, GIII
- Batch 1 (top 3 by priority_score): CRDO (73.75), MDB (66.0), GTLB (57.5)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (wave_size=2) — wave 1: CRDO+MDB, wave 2: GTLB — publish after each wave

## Stage 2 — deep dive, batch 1 — FINISHED (08:54 UTC)
- Logged at 2026-09-01 08:54 UTC
- Researched: CRDO, MDB, GTLB
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves of wave_size=2 (wave 1: CRDO+MDB; wave 2: GTLB)
- Median evidence completeness: 80/100 (CRDO 78, MDB 84, GTLB 80)
- Panel-eligible after this batch: not computed — final batch only (batch 2 covers DELL, CXM, GIII)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-01 10:23 UTC
- Shortlist: 6 names (cap=triage.shortlist_size=6, no names dropped for cap); batch 1 already covered CRDO, MDB, GTLB
- This batch: DELL, CXM, GIII
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (wave_size=2) — wave 1: DELL+CXM, wave 2: GIII — publish after each wave
