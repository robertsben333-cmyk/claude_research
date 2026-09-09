# Run log — 2026-09-09

## Stage 0 — universe (07:16 CEST)
- Logged at 2026-09-09 05:18 UTC
- Window: After the US close on Wed 2026-09-09 through before the US open on Thu 2026-09-10
- Source: nasdaq (both after-close and before-open feeds returned ok)
- Universe: 20 total (11 AMC, 9 BMO); 8 above the $500M market-cap floor; 7 eligible after qualification
- Excluded: 13 (12 below_market_cap_floor; 1 no_options_market — YB, a Sept-2026 Chinese-ADR IPO with no listed contracts on Nasdaq's option-chain page and a 31M-share float)
- Confirmed BMO/AMC timing and options market by web search for the three newer/smaller eligible names: NAVN and WLTH sessions confirmed via company BusinessWire/GlobeNewswire releases and their Nasdaq/Yahoo/Barchart option chains; TEN's BMO 09-10 confirmed via TEN Ltd.'s own GlobeNewswire release, options market assumed from its long NYSE listing (no chain data surfaced in search, noted for stage 1/2 awareness)
- COO, AVAV, M, AEO not independently re-verified beyond the nasdaq feed — large, long-listed, obviously optionable names; verification effort spent on the borderline/newer tickers instead

## Stage 1 — triage (06:40 UTC)
- Logged at 2026-09-09 06:41 UTC
- Mode: skipped (universe 7 <= threshold 10)
- Funnel: 20 universe -> 7 eligible -> 7 cleared floors -> 7 shortlisted
- Scouts: 0 subagents (skip mode, no scoring)
- Session mix: 5 AMC / 2 BMO
- Notable drops: YB (no_options_market, dropped at stage 0, not by triage)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-09 08:25 UTC
- Shortlist: 7 names, all priority_score=null (stage 1 ran in skip mode, universe<=10). Capped to triage.shortlist_size=6 by shortlist order (market-cap descending); dropped TEN (smallest cap, and stage 0 flagged its options-chain data as unconfirmed).
- This batch (1 of 2): COO, AVAV, NAVN
- Batch 2 will cover: M, AEO, WLTH
- Already on disk, skipping: none
- Plan: waves of deep_dive.wave_size=2 opus/high researchers (COO+AVAV, then NAVN alone), publish after each wave

## Stage 2 — deep dive — NAVN
- Logged at 2026-09-09 08:55 UTC
- NAVN (Navan, Inc.) dossier complete. Event confirmed AMC 2026-09-09 (Q2 FY27, qtr ended 2026-07-31) via company BusinessWire release + MarketBeat/Benzinga/Ortex. Spot $26.64 (2026-09-08 close), mkt cap $6.78B, ~6.8x EV/FY27 guided sales. NO published implied move exists for this name (TipRanks week-of table covers 23 tickers incl. AVAV/AEO/COO/M but omits NAVN; Benzinga 403, MarketChameleon paywalled) — derived ~13-15% (pt est 14%) myself from the 18-Sep chain via investing.com; marked snippet_only. Only 3 post-IPO realised moves exist (IPO 2025-10-30): -7.8%, +42.5%, -1.0% (Bloomberg via Investing.com); mean_abs 17.1 is driven entirely by one outlier, median_abs 7.8. Key finding: usage yield compressed ~45-50bp YoY (FY26 ~7.03% -> Q1 FY27 6.52%) as GBV +50% outran usage revenue +41%, while the sourced Street pair ($2.86B GBV / $220.5M rev, Oppenheimer) implies a snap-back to 7.71%. Decisive precedent: the 10-Jun print beat revenue 7.3%, swung EPS positive and raised FY guide $25M above Street, popped ~19% AH and CLOSED -1.0%. Company has itself guided non-GAAP op margin DOWN 11%->6% this quarter. Macro hostile: 10y ~4.80% (highest since late 2023), Sept Fed a coin flip on a HIKE, CPI Friday, software sold two straight sessions on GPT-6 Astra agent fears (NAVN -4.10% on 09-08). Preliminary read -18 / prob_up 43 / conviction Low. Evidence completeness 78. Unreachable domains: businesswire, benzinga, optionstrat, daytraders, cnbc/quotes, nasdaq option-chain, yahoo quote+API, marketchameleon.

## Stage 2 — deep dive, batch 1 — FINISHED (08:56 UTC)
- Logged at 2026-09-09 08:56 UTC
- Researched: COO, AVAV, NAVN
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (COO+AVAV, then NAVN)
- Median evidence completeness: 80/100 (COO 80, AVAV 84, NAVN 78)
- Dropped from the day's cap: TEN (7th by market cap, capped out at shortlist_size=6; also flagged at stage 0 for unconfirmed options-chain data)
- Batch 2 (M, AEO, WLTH) not yet run

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-09 10:24 UTC
- Shortlist: 7 names, capped to 6 by shortlist order (market-cap descending); batch 1 already covered COO, AVAV, NAVN. TEN (7th, smallest cap) dropped from the day's cap.
- This batch (2 of 2): M, AEO, WLTH
- Already on disk, skipping: none
- Plan: waves of deep_dive.wave_size=2 opus/high researchers (M+AEO, then WLTH alone), publish after each wave

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-09 10:53 UTC
- Researched: M, AEO, WLTH
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (M+AEO, then WLTH)
- Median evidence completeness: 76/100 (M 76, AEO 84, WLTH 68)
- Day's cap (6 of 7 shortlisted names) now fully researched: COO, AVAV, NAVN (batch 1), M, AEO, WLTH (batch 2). TEN dropped from the cap.
- 02-ranking.json written from all 6 dossiers. panel_priority = 0.45*|preliminary_direction_score| + 0.35*evidence_completeness (change_expectation term dropped: triage ran in skip mode, no scores exist for any name).
- Panel-eligible after this batch: COO, AVAV, NAVN, M, AEO, WLTH (all 6; none excluded — all event_confirmed, all evidence_completeness>=68, WLTH's missing implied move is covered by 3 historical post-IPO reactions)
- Top 2 by panel_priority for panel.names=2: NAVN (35.4), WLTH (35.05)

## Stage E — scorer rebuilt, impact_sum is the key
- Logged at 2026-09-09 13:52 UTC
- edge_score.py now ranks on impact_sum (hunters' signed per-finding sizes, points of spot) with conviction beside it; cluster-max, sqrt(k), agreement discount, quality multiplier, tanh, confidence and uncertainty are demoted to diagnostics (residual_sum and edge_score_legacy kept, the latter reproduces the old key exactly). config gains conviction_floor 3.0 as a floor on emphasis, never a filter. edge_resolve.py reads impact_sum with fallback to edge_score, adds the conviction-vs-sign correlation and both free controls, and pools within days. Skill sections 5-7 rewritten. The Routine prompt could NOT be updated from here (update_trigger refuses routines an agent did not create); replacement text is in docs/routine-prompts/edge-hunt.md.

## Edge hunt — 2026-09-09 amc + 2026-09-10 bmo — STARTED
- Logged at 2026-09-09 14:10 UTC
- Stage E run for the window 2026-09-09 amc + 2026-09-10 bmo. edge_universe.py --window resolved 22 of 84 calendar rows, 0 unresolved session, no --include-unknown. Baselines sealed for all 22 in two priced_in.py calls (12 amc on 09-09, 10 bmo on 09-10) and committed before any agent launches.
- Baseline read: 7 of 22 names have a live option chain (COO 8.7%, AVAV 11.9%, NAVN 14.1%, AEO 13.3%, M 7.7%, FLWS 19.7%, LMNR 6.1% implied move); the other 15 take the historical-median fallback. event_plausibility: 16 fits_cadence, 6 unknown (AEO, DBI, LAKE, SHOE with no cadence read; GLOO and IMPP flagged cadence_implausible).
- Plan: 1 edge-sweep over all 22 names, then shed to 8 hunted names per budget.edge_degrade_order (drop_unconfirmed_names_first, then drop_lowest_hunt_priority_names, keeping names with a live chain). 1 + (8+2) hunters + 8 adversaries = 19 of the 20-subagent edge_hunt cap. Ranking key is impact_sum per SKILL.md section 5 and edge-scores.json's own ranking_key.

## Edge hunt — 2026-09-09 amc + 2026-09-10 bmo — COMPLETE
- Logged at 2026-09-09 14:52 UTC
- Universe 22 confirmed (sweep: 22 of 22 from company sources, ZERO phantom rows, zero unsettled sessions — the best confirmation rate this stage has recorded; structural, because this universe pre-announces date and hour by wire). 8 names hunted, 10 hunters, 37 findings, 8 adversaries, join verified clean 37/37.
- Ranking key impact_sum per edge-scores.json ranking_key. NAVN +9.75, AVAV +3.25, FLWS +1.50, LMNR +1.50, SKIL -2.50, LSAK -3.35, KEQU -10.50, WLTH -15.50. Five clear the 3.0 conviction floor. Control -run_up_20d ranks SKIL, AVAV, FLWS, NAVN, LSAK, KEQU, WLTH, LMNR — differs at both extremes but the hunt has NOT been shown to beat it.
- BUDGET: 19 of the 20-subagent edge_hunt cap (1 sweep + 10 hunters + 8 adversaries). Shed 14 of 22 names via budget.edge_degrade_order step 2 (drop_lowest_hunt_priority_names); step 1 (drop_unconfirmed_names_first) shed nothing because the sweep confirmed every name. Shed names sit in edge-scores.json as rankable:false / 'no hunt'.
- DEVIATION, recorded per SKILL.md section 3: FLWS (hunt_priority 68) was swapped in for LAKE (71) because FLWS has a live option chain and LAKE does not. Cost 3 priority points; took names with a measured rather than inferred baseline from 3 of 8 to 4 of 8. Only 7 of the 22-name window have a chain at all.
- PLATFORM: concurrency cap is 8 subagents, not the 4 in config or the 20 spend cap. Two hunter launches (AVAV, KEQU) were rejected on the first wave and relaunched as slots freed; the AVAV adversary likewise. No budget was spent on the rejected launches. Total wall clock ~45 min.
- ADVERSARY: median priced_in_pct 72, mean 69.9, range 44-92; 3 findings <=50, 11 >=80. Factual breaks — LMNR-h1#2 (92): covenant deferral misread, the amendment defers to Oct-2027 not Oct-2026, so the mechanism does not reach this print. FLWS-h1#1 (82): 'short base has not moved' contradicted by its own source (9.30m shares 13 Mar vs 7.75m 14 Aug), and the same finding re-reported four sealed-baseline fields as discoveries. Survived best: SKIL-h1#1 at 44 (CFO transition calendar), LMNR-h1#3 at 45 (Colorado River Record of Decision, 19 days pre-print).
- OPEN ISSUE 1 — double counting. All 8 adversaries independently reported that findings on their name rest on shared documents or mirror each other, and impact_sum sums them anyway. The cluster-max was built for exactly this and docs/EDGE_ANALYSIS.md demoted it because it LOWERED measured rank correlation over six runs. Both facts hold; resolving them needs more resolved days, not a decision taken in a run. diagnostics.residual_sum and edge_score_legacy are in the JSON for that test.
- OPEN ISSUE 2 — code/doc discrepancy, flagged not fixed. SKILL.md and edge_score.py's docstring both describe impact_sum as 'the hunters' signed per-finding sizes, added up'. scripts/edge_score.py:206-211 instead re-sizes each finding to the MEAN of the hunter's number and the adversary's independent size_check_pct before summing. Today median disagreement 0.5 pts, max 11.0 (KEQU-h1#0: hunter -4.0, adversary -15.0, booked -9.5) and KEQU's rank depends on it. Needs someone who can check which version EDGE_ANALYSIS.md measured at rho=0.407. Nothing changed in this run.
- OPEN ISSUE 3 — capacity vs selection. Only 3 of 8 hunted names clear $5m/day turnover; 5 are under $1m and KEQU is $0.07m (368 shares traded the prior session) while carrying the second-largest conviction. The shed is made on hunt_priority, which scores room-for-something-unpriced and is close to a measure of obscurity, so it systematically selected the illiquid tail and dropped the four most liquid names in the window (M $115.7m, COO $108.5m, AEO $85.5m, SHOE $10.6m). Selection rule and capacity pull opposite ways and nothing in the pipeline notices.
- Sign balance: 6 of 10 hunts leaned negative, matching 2026-08-31's 6 of 8 — still more plausibly an artefact of the hunter prompt than a fact about the companies. LMNR's hunter wrote expected_move_pct -2.5 while its own findings sum to +1.50; the scorer uses the findings, but hunt file and table disagree in sign.
- No baseline amendment needed: no name carried a suspect event_plausibility verdict. edge_baseline_amend.py exited non-zero on a stale per-run table (CRMT/SUNB/YQ from an earlier run) — the guard working as designed. Routine prompt is the current post-2026-09-09 text and does NOT restate the output contract, so no staleness note is due; verified against list_triggers (trig_01CvGQJWoKeNLXWCxiffM3ED, cron 4 14 * * 1-5, updated 2026-09-09T13:55Z).
- CLAUDE.md stage-E paragraph corrected in the same run: it still described the output as 'one signed score per company on -100...+100', which impact_sum (points of spot, unbounded) has not been since 2026-09-09. Cron times in the stage table verified against list_triggers and are correct; the five pipeline Routines still do not exist.
- Resolve after the 2026-09-10 close (amc names) and the 2026-09-11 close (FLWS). 2026-09-08's eight names are also still awaiting resolution.

## Capture - 2026-09-09 - STARTED
- Logged at 2026-09-09 15:06 UTC
- Sweep universe --horizon-days 15 (script-only), then agent-layer 9-area capture for the 6 largest names reporting within 3 days; publish after each name.
