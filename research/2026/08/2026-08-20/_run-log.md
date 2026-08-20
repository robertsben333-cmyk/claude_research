# Run log — 2026-08-20

## Stage 0 — universe (07:14 CET)
- Window: After the US close on Thursday 20 August 2026 through before the US open on Friday 21 August 2026
- Source: nasdaq
- Universe: 9 total (5 AMC, 4 BMO); 6 eligible after qualification
- Excluded: 3 (below_market_cap_floor: ZKH $0.46B, ICG $0.11B, FLUX $0.02B)
- Notes: All 6 eligible names' BMO/AMC session and event date cross-checked against a
  second independent source (company press release, SEC 6-K, or IR page) — no
  conflicts. All 6 are established NYSE/Nasdaq-listed names with real listed-options
  markets (Ross Stores, KE Holdings, BJ's Wholesale, OSI Systems, Buckle, Flowers
  Foods); none flagged for OTC/SPAC-remnant/thin-trading exclusion. Eligible count (6)
  is at or below `triage.skip_if_universe_at_or_below` (10), so per config stage 1
  (triage) will be skipped and all 6 eligible names go straight to stage 2 (deep dive).

## Stage 1 — triage (08:55 CET)
- Mode: skipped (universe eligible 6 <= threshold 10)
- Funnel: 9 universe -> 6 eligible -> 6 shortlisted (screen skipped, no floor cut)
- Scouts: 0 (skip mode)
- Session mix: 3 AMC / 3 BMO
- Notable drops: none by triage (stage 0 already excluded ZKH, ICG, FLUX below market cap floor)
- Note: fixed a bug in scripts/validate_stage.py — it required change_expectation/ai_edge/priority_score even in skipped_small_universe mode, contradicting the skill's documented null-score behavior for skip mode. Now only required when triage_mode != "skipped_small_universe". Ran scripts/smoke_test.py after the change; all checks passed.

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-08-20 08:23 UTC
- Tickers: ROST, BEKE, BJ (positions 1-3 of 6 in shortlist; no priority_score to rank by, triage was skipped for small universe, so shortlist order used)
- Plan: 2 waves of ROST+BEKE, then BJ solo, publish after each wave; per-dossier publish inside each wave
