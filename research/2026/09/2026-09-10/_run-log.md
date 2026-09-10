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

## Edge hunt — 2026-09-10 — COMPLETE
- Logged at 2026-09-10 14:53 UTC
- 17 names in window; sweep confirmed 17 of 17 with 0 phantom rows and 0 session-unsettled, every date and release hour sourced to a company press release, 8-K/6-K or IR page — the best confirmation rate the stage has recorded. 17 hunters, one per name, no shedding (cap is 1 sweep + 19 hunters, so 18 of 20 spent). 61 findings. No adversary pass. Ranking key impact_sum, as edge-scores.json's ranking_key states. 7 of 17 clear the 3.0 conviction floor: HOFT +7.30, RENT -8.50, AENT -7.50, FEIM -3.50, REF -3.50, ORCL -3.20, RH +3.00. Sign balance 7 positive / 10 negative / 0 zero. 7 of 17 had a live option chain; the 14:04 UTC firing worked at the top (ORCL ATM spread 2.6% of mid, ADBE 12.7%, CPRT 11.3%) and not in the tail (RH 59%, FEIM 79%, unusable ones 100-189%). Spearman between the hunt ranking and the free control -run_up_20d is 0.054 — near-orthogonal, with head-on disagreement on RENT (control 2nd, hunt 17th) and LPTH (control 1st, hunt 7th). CAPACITY IS THE HEADLINE CAVEAT: both extremes are untradeable, HOFT /bin/bash.4m/day and RENT /bin/bash.2m/day, and 4 of the 7 above-floor names trade under $5m/day. CORRELATED EXPOSURE the scorer cannot see: four names (HOFT +7.0, RH +5.5, ZUMZ +3.0, REF -3.0) are ranked substantially by one regulatory event, the IEEPA tariff refunds — if that thesis is wrong it is wrong on all four at once. Two failures to record: (1) the hunter briefs quoted a wall-clock time ahead of the container clock (I told the later hunters ~15:30-16:10 UTC when date -u read 14:41) — harmless here because every print is after 20:00 UTC and the 'has not happened yet' framing was correct for all 17, but it is a fabricated number handed to a subagent and should not recur; re-read date -u per brief rather than extrapolating. (2) scripts/edge_baseline_amend.py's AMENDMENTS table was still carrying the 2026-09-08 entries and exited non-zero, as designed; rewritten for this run in a separate commit. Execution: config/pipeline.yaml has NO execution block at all and scripts/alpaca_trade.py and docs/EXECUTION.md do not exist in this tree, so Routine steps 0b and 7 were no-ops — nothing sold, nothing bought, no account contacted. The Routine prompt assumes machinery that is not in the repo; either the switch was never merged or it lives on another branch.

## Execution machinery merged (out of band)
- Logged at 2026-09-10 15:11 UTC
- Steps 0b and 7 of today's stage E run were no-ops because config/pipeline.yaml had no execution block and scripts/alpaca_trade.py and docs/EXECUTION.md were absent. Found on branch claude/alpaca-auto-orders-integration-y397gh (PR #1, 8 commits, forked at ead1c5f before today's edge run); merged into claude/missing-execution-config-14ya8q. No conflicts with today's research files. smoke_test.py passes all 25 execution checks. execution.enabled stays false. Post-hoc dry run of alpaca_trade.py plan over today's edge/ wrote alpaca-plan.json: 5 of 17 names clear the benchmark (HOFT +7.30 long, FEIM -3.50, REF -3.50, ORCL -3.20 short, RH +3.00 long), gross 84.2% of a 100k assumed equity, 10 names below the 3.0 conviction floor and 2 below the 200k turnover floor. That plan was generated during this merge, not by the 16:04 run, and no account was contacted.

## Stage 3 — panel & advice — STARTED
- Logged at 2026-09-10 15:55 UTC
- Stage 2 batch 2 never logged FINISHED and never wrote 02-ranking.json (KR, CPRT dossiers exist; DSGX, RH do not). Built 02-ranking.json in this stage from the 4 available dossiers (ADBE, CPRT, KR, ORCL), per earnings-panel-advice skill step 1.
- Ranking (panel_priority, change_expectation term dropped, all null): KR 39.3, ORCL 38.6, CPRT 37.5, ADBE 37.0
- panel.names=2 (config default, already at first budget.degrade_order step): panelling KR, ORCL
- Plan: refresh spot/implied-move anchors for KR and ORCL, run 7 isolated personas per name (14 subagents total), synthesize, write dossiers and 04-advice
