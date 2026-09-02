# Run log — 2026-09-02

## Stage 0 — universe (07:18 CEST / 05:18 UTC)
- Logged at 2026-09-02 05:19 UTC
- Window: After the US close on Wednesday 02 September 2026 through before the US open on Thursday 03 September 2026
- Source: nasdaq (both after-close and before-open, single-source feed, status ok)
- Universe: 31 total (16 AMC, 15 BMO); 24 above the $500M market-cap floor; 23 eligible after qualification
- Excluded: 8 (7 below_market_cap_floor: GCO, LE, MTRX, CHPT, DLTH, TLYS, AMBR; 1 no_options_market: WLYB — WebSearch-confirmed no listed-options chain, WLY class A kept)
- Verified by WebSearch: GOLD is A-Mark Precious Metals' Dec-2025 NYSE rebrand (real listed name, not a data error); VSXY is Victoria's Secret & Co's post-rename ticker (was VSCO); VBNK, ZGN, NTSK, MEI, AGX all confirmed to have real listed-options markets; AGX's Sept 2 AMC timing confirmed by company press release
- Notes: local main branch was behind origin/main by a full day of pipeline commits at session start (shallow-clone merge-base artifact, not a real divergence); fast-forwarded cleanly before starting this stage

## Stage 1 — triage — STARTED
- Logged at 2026-09-02 06:39 UTC
- Screening 23 eligible names via 2 earnings-triage-scout subagents (batches of ~12), floors change_expectation>=35 / ai_edge>=30, shortlist_size 6

## Stage 1 — triage (06:46 UTC)
- Logged at 2026-09-02 06:43 UTC
- Mode: scouted (2 subagents, sonnet/medium)
- Funnel: 31 universe -> 23 eligible -> 19 cleared floors -> 6 shortlisted
- Session mix: 5 AMC / 1 BMO (VSXY swapped in for WOOF on session-mix grounds, 0.65pt gap)
- Notable drops: NTSK (tradeable:false, thin options liquidity), DOO (timing_confirmed:false, conflicting date/listing), VBNK (tradeable:false, thin liquidity), BRC (change_expectation 30<35), HPE/CIEN (tied 8th at 60.50, just missed cut)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-02 08:26 UTC
- Shortlist: 6 names; this batch: AVGO, SNOW, AI (top 3 of 6 by priority_score, cap=triage.shortlist_size=6, batches=2)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (deep_dive.wave_size=2), publish after each wave and after each dossier

## Stage 2 — deep dive, batch 1 — FINISHED (08:54 UTC)
- Logged at 2026-09-02 08:55 UTC
- Researched: AVGO, SNOW, AI
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves of 2 (wave 1: AVGO+SNOW, wave 2: AI)
- Median evidence completeness: 84/100
- Batch 2 covers NTAP, PVH, VSXY; ranking (02-ranking.json) deferred to that batch

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-02 10:25 UTC
- Shortlist: 6 names; this batch: NTAP, PVH, VSXY (positions 4-6 of 6 by priority_score, cap=triage.shortlist_size=6, batches=2)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (deep_dive.wave_size=2) — wave 1: NTAP+PVH, wave 2: VSXY — publish after each wave and after each dossier

## Stage 2 — deep dive, batch 2 — FINISHED (11:02 UTC)
- Logged at 2026-09-02 11:02 UTC
- Researched: NTAP, PVH, VSXY
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (wave 1: NTAP+PVH; wave 2: VSXY)
- Median evidence completeness: 82/100
- Ranking (02-ranking.json) built from all 6 dossiers (both batches): AI 55.0, SNOW 49.9, VSXY 49.8, AVGO 49.1, PVH 47.75, NTAP 47.6 — all panel-eligible
- Panel-eligible after this batch: AI, SNOW, VSXY, AVGO, PVH, NTAP (all 6; top panel.names=2 per config are AI, SNOW)

## Edge hunt — 2026-09-02 amc + 2026-09-03 bmo — STARTED
- Logged at 2026-09-02 14:15 UTC
- Window resolved 32 names from 98 calendar rows, 0 time-not-supplied (no --include-unknown needed). Baselines sealed for all 32 before any agent launch: 17 with a live option chain (straddle implied move present), 28 with >=5 EDGAR 8-K reaction history. 6 baselines returned event_plausibility=unknown, of which 4 carry cadence_implausible=true (DOO, PSNY, VBNK, ZGN - all foreign private issuers) plus GOLD and MEI. FIVE needed one retry after a bars HTTPError. Plan: 1 edge-sweep over all 32; shed to ~8 hunted names per budget.edge_degrade_order (cap 20 = 1 sweep + 10 hunters + 8 adversaries = 19); 2 isolated hunters on the top 2 by hunt_priority, 1 on the rest; 1 priced-in-adversary per ticker judging all findings both sides; edge_score.py then edge-note.md.

## Edge hunt — 2026-09-02 — SWEEP DONE, HUNT SET CHOSEN
- Logged at 2026-09-02 14:35 UTC
- Sweep: 31 of 32 rows company-sourced, 0 phantoms, 1 duplicate (WLYB = John Wiley class B, same CIK 0000107140 and same 8-K as WLY), 1 unconfirmed (AMBR - no scheduling 6-K one day before the calendar's date). 30 distinct hunt targets. hunt_priority spread 3-86. All four cadence_implausible flags (DOO, PSNY, VBNK, ZGN) were false positives of the 6-K text matcher and all four events are real and company-confirmed. Baseline amendment, symmetric, before any hunter launched: UPGRADE MEI and GOLD unknown->fits_cadence (MEI is the PANW/CXM former-name records bug - 68 valid item 2.02 prints discarded, EDGAR shows no former name, and hist_n stays 0 so the name still pays for the thin history; GOLD is a real 2025-12-01 A-Mark->Gold.com rename, history correctly truncated to 2 genuine prints). DOWNGRADE WLYB and AMBR fits_cadence->unknown. DELIBERATELY NOT amended: DOO, PSNY, VBNK, ZGN stay at unknown/0.6 - their events are real but their recorded medians are reactions to monthly wrappers, delivery updates, near-daily regulatory filings and quarterly revenue announcements respectively, so upgrading would forgive the history defect and hand them a 1.0 they have not earned. smoke_test.py passed after the edge_baseline_amend.py table rewrite. HUNT SET (8 names, budget 1 sweep + 10 hunters + 8 adversaries = 19 of 20): MEI 86, GOLD 83, AGX 80, NTSK 77, DLTH 74, WOOF 72, DOO 70, AI 65. Double hunt on MEI and GOLD. DEVIATION FROM STRICT hunt_priority ORDER, recorded per the skill's option-chain judgement call: MTRX (priority 68) dropped in favour of AI (priority 65). MTRX has no computable straddle at all (ATM spread 125% of mid on 998 contracts) so its priced lean would be inferred from a run-up, while AI has a genuinely measured chain (12.7% implied move, 135,726 contracts) and a trustworthy 8-print history. Near-equal priority, materially better-measured baseline. SHED per budget.edge_degrade_order: drop_unconfirmed_names_first (AMBR) and the WLYB duplicate, then drop_lowest_hunt_priority_names for the remaining 20. All 32 names still appear in edge-scores.json as rankable=false with a stated reason. Hunter isolation: each gets only its own sweep row from edge/sweep-rows/<TICKER>.json, never sweep.json.
