# Run log — 2026-09-10

## Stage 0 — universe (05:15 UTC / 07:15 CEST)
- Logged at 2026-09-10 05:18 UTC
- Window: After the US close on Thursday 10 September 2026 through before the US open on Friday 11 September 2026
- Source: nasdaq (after-close 12 rows, before-open 5 rows)
- Universe: 17 total (12 AMC, 5 BMO); 9 above the $500M market-cap floor; 8 eligible after qualification
- Excluded: 9 total — 8 below_market_cap_floor (IBEX, ZUMZ, AENT, HOFT, CMCM, RENT, CSBR, MNY); 1 unconfirmed_timing (REF — IPO'd 2026-07-30, ~6 weeks public, conflicting third-party earnings-date estimates with no official IR/8-K confirmation for today, listed-options market also unverified)
- Notes: DSGX, FEIM and LPTH sessions cross-checked against official IR/8-K sources (not just the calendar feed) since they are the thinnest names above the floor; all confirmed AMC today. 8 eligible is at/below triage.skip_if_universe_at_or_below (10), so stage 1 should be skipped and all 8 names should go straight to stage 2.

## Stage 1 — triage (08:38 CEST)
- Logged at 2026-09-10 06:41 UTC
- Mode: skipped (universe eligible 8 <= triage.skip_if_universe_at_or_below 10)
- Funnel: 17 universe -> 8 eligible -> 8 cleared floors -> 8 shortlisted
- Scouts: 0 subagents (screen skipped)
- Session mix: 7 AMC / 1 BMO
- Notable drops (from stage 0): REF (unconfirmed_timing), IBEX/ZUMZ/AENT/HOFT/CMCM/RENT/CSBR/MNY (below_market_cap_floor)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-10 08:27 UTC
- Shortlist: 8 names, all priority_score null (stage 1 ran in skip mode, unscored). Capped to triage.shortlist_size=6 using market cap as tie-break (already the shortlist's own order); dropped for cap: FEIM ($0.73B), LPTH ($0.67B) — smallest two, documented per skill step 1.
- This batch: ORCL, ADBE, KR (positions 1-3 of the capped 6; N=ceil(6/2)=3)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (deep_dive.wave_size=2), publish after each wave and after each dossier

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-10 10:26 UTC
- Shortlist: 8 names, capped to 6 (triage.shortlist_size=6) by market cap; dropped for cap: FEIM, LPTH
- Batch 1 (ORCL, ADBE, KR) left KR unresearched with no HALTED note in the log -- picking it up here alongside this batch's own half
- This batch: KR, CPRT, DSGX, RH (position 3 from batch 1's gap, plus positions 4-6)
- Already on disk, skipping: ORCL, ADBE (both .md and .json present from batch 1)
- Plan: waves of 2 opus/high researchers (deep_dive.wave_size=2) -- wave 1: KR, CPRT; wave 2: DSGX, RH -- publish after each wave and after each dossier; final batch, so 02-ranking.json follows

## Edge hunt — 2026-09-10 amc + 2026-09-11 bmo — STARTED
- Logged at 2026-09-10 14:10 UTC
- Stage E fired 14:04 UTC (16:04 Amsterdam, 10:04 New York), ~34 min into the US session. Universe: 17 of 52 calendar rows resolve to the window (12 amc 09-10, 5 bmo 09-11); --include-unknown withheld. Baselines sealed and committed BEFORE any agent launch: all 17 status=ok. 7 names carry a live option chain (ORCL spread 2.6% of mid, ADBE 12.7%, CPRT 11.3%, LPTH 22.2%, KR 30.0%, RH 59.0%, FEIM 79.1%) — the 16:04 timing gave ORCL/ADBE/CPRT two-sided quotes. Event-plausibility flags to resolve at sweep: CSBR suspect; DSGX and MNY unknown+cadence_implausible; REF and ZUMZ unknown (no reaction history). Plan: 1 edge-sweep over all 17, then 1 unpriced-hunter per confirmed name, cap 20 subagents (1+19), so up to 17 hunters fits with no shedding. No adversary pass (removed 2026-09-09). Execution: config/pipeline.yaml has no execution block and scripts/alpaca_trade.py is absent from this tree, so steps 0b/7 of the Routine prompt are no-ops — dry run, no book sold and none bought.

## Edge hunt — 2026-09-10 — sweep + baseline amendment
- Logged at 2026-09-10 14:19 UTC
- Sweep (1 agent, all 17 names): 17 confirmed, 0 phantom, 0 session-unsettled — every date and every session hour sourced to a company press release, 8-K/6-K or IR page. That is the best confirmation rate the stage has recorded; the phantom problem that motivated the sweep did not appear today. 4 names rated baseline_history_trustworthy=false: DSGX, CMCM, MNY (FPI 6-K text-matcher caught non-earnings filings) and ZUMZ (history.n=0 records artefact) — each of those hunters is told so explicitly. Baseline amendment applied symmetrically before any hunter launched: UPGRADE CSBR suspect->fits_cadence (April-30 fiscal year end makes a ~45-day Q1 gap legitimate; the same pattern produced the 2025-09-15 print already in its own history) and ZUMZ unknown->fits_cadence (records-bug zero history, event confirmed by company PR 2026-08-27); DOWNGRADE CMCM fits_cadence->unknown (FPI matcher history, the NIO/YSG failure mode). Deliberately NOT amended: DSGX and MNY stay 'unknown' despite company-confirmed events, because upgrading would forgive the same history defect (DOO/PSNY/ZGN precedent); REF stays 'unknown' on the opposite reasoning — its 2026-07-30 IPO means zero history is a fact not an artefact, and EDGAR CIK 0001787117 carries no 8-K naming the date, so confirmation rests on wire copy only. Only the CSBR upgrade changes anything ranked: edge_score sets rankable=False on 'suspect' alone, and every other verdict feeds only event_q into baseline_quality, which lives in diagnostics and decides nothing.
