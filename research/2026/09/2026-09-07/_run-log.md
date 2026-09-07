# Run log — 2026-09-07

## Stage 0 — universe (07:15 CEST / 05:15 UTC)
- Logged at 2026-09-07 05:17 UTC
- Window: After the US close on Monday 07 September 2026 through before the US open on Tuesday 08 September 2026
- Source: nasdaq (after-close and before-open both single-source, clean fetch, exit 0)
- Universe: 6 total (1 AMC, 5 BMO); 2 eligible after qualification (ABM, UNFI)
- Excluded: 4, all below_market_cap_floor (WDH $0.36B, CAN $0.30B, DLNG $0.13B, GMHS $0.04B)
- Notes: 2026-09-07 is Labor Day (reference_is_trading_day: false in the feed); the nasdaq calendar still returned a same-day AMC row (DLNG) despite the holiday -- treated as a calendar-dated event, not a market-hours artifact, and excluded anyway on market cap. Both eligible names (ABM, UNFI) verified via WebSearch for real listed options markets and confirmed, non-conflicting BMO timing; UNFI's fiscal_quarter_ending label from the feed (Jul/2026) undercounts -- this is actually UNFI's Q4/FY2026 print, noted in 00-universe.md but not a qualification issue since timing is not in conflict.

## Stage 1 — triage (skipped) — 06:41 UTC
- Logged at 2026-09-07 06:41 UTC
- Mode: skipped (universe 2 <= threshold 10)
- Funnel: 6 universe -> 2 eligible -> 2 cleared floors (screen skipped) -> 2 shortlisted
- Scouts: 0 subagents (screen not needed)
- Session mix: 0 AMC / 2 BMO
- Notable drops: none by this stage (4 names already excluded upstream at stage 0 on market cap: WDH, CAN, DLNG, GMHS)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-07 10:24 UTC
- Shortlist: 2 names (ABM, UNFI); cap 6, both within cap
- Batch 1 published no heartbeat and no dossiers exist -- its half (ABM) is missing; covering both halves as batch 2
- Already on disk, skipping: none
- Plan: single wave of 2 opus/high researchers (ABM, UNFI), publish after each dossier

## Stage 2 — deep dive, batch 2 — FINISHED (10:45 UTC)
- Logged at 2026-09-07 10:46 UTC
- Researched: ABM, UNFI (batch 2 covered both halves -- batch 1 published no heartbeat and no dossier for its assigned name, ABM, existed when this batch started)
- Skipped (already done): none
- Failed: none
- Subagents: 2 opus/high, in 1 wave of wave_size 2
- Median evidence completeness: 85.5/100
- Panel-eligible after this batch: ABM (panel_priority 35.5), UNFI (panel_priority 33.35) -- both eligible, ranked in 02-ranking.json

## Stage E — edge hunt — STARTED
- Logged at 2026-09-07 14:08 UTC
- Window: 2026-09-07 amc + 2026-09-08 bmo -> edge_universe --window resolved 6 of 34 calendar rows, 0 unresolved-session rows (no --include-unknown needed). All six are 2026-09-08 bmo: ABM, UNFI, WDH, CAN, DLNG, GMHS.
- Baselines sealed and pushed BEFORE any agent launch (commit cb92bbd): all 6 status=ok. Live option chains on 2 of 6 -- ABM impl 8.4%, UNFI impl 13.15% (skew 6.97). WDH/CAN/DLNG/GMHS have no listed options, so their expected_move_pct is a historical median, not a priced expectation.
- Baseline event_plausibility: ABM fits_cadence (95d vs 86d), UNFI fits_cadence (91d vs 91d), WDH fits_cadence (46d vs 84d, ratio 0.55 -- early, flag for sweep). CAN/DLNG/GMHS all unknown + cadence_implausible (inferred cadences 13d/21d/55d) -- foreign private issuers whose 6-K operational updates were caught by the text matcher. Symmetric amendment from company sources only, after the sweep, before hunters.
- Plan: 1 edge-sweep over all 6 -> unpriced-hunter with double_hunt_top_n=2 on the top two by hunt_priority + 1 on the rest -> 1 priced-in-adversary per ticker with findings, briefs built by edge_brief.py -> edge_score.py -> edge-note.md.
- Budget arithmetic: 1 sweep + (6 confirmed + 2 double) 8 hunters + 6 adversaries = 15 of the edge_hunt cap of 20. Fits; no shed planned. If the sweep kills names, the hunter and adversary counts fall with it.
