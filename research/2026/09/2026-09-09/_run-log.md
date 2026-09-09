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

## Data availability check — test data inventory
- Logged at 2026-09-09 13:59 UTC
- Scored all six claude_naive days for the first time (LEDGER.md created, 39 events, 18 directional). Pooled the edge hunt across 7 runs (n=51). No pipeline stage run.

## Backtest feasibility — edge hunt on the capture corpus
- Logged at 2026-09-09 14:16 UTC
- Checked whether the edge hunt can be backtested on backtest/captures (387 events, 205 sealed past). Yes on the expected-move proxy anchor, no on options. Four blockers written up in backtest/FINDINGS.md section 33, including a look-ahead options leak in scripts/priced_in.py.

## Backtest blockers — all four fixed
- Logged at 2026-09-09 14:36 UTC
- as-of options guard in priced_in.py; seal.py written (111 of 205 captures scorable, 90 phantom calendar rows); implied_basis recorded in edge_resolve.py; corpus-only hunter and adversary agents. Plus cik_for class-share fix. smoke_test passes.

## Edge-corpus backtest — STARTED
- Logged at 2026-09-09 14:39 UTC
- Running the edge hunt over the sealed capture corpus: 109 events across 7 event days (2026-08-31 .. 2026-09-09), one hunter agent per day plus one adversary agent per day. Baselines built with the as-of guard, so every name is proxy-anchored. Output under backtest/runs/edge-corpus/<date>/.

## Edge-corpus contamination audit
- Logged at 2026-09-09 14:55 UTC
- Re-audited against the sealed acceptance instant instead of the calendar date: 31 of 109 names hold post-print material, 29 of them because a bmo capture's daily sweep runs hours after a bmo 8-K. Non-destructive clean-view files written; FINDINGS.md section 35.

## Edge-corpus corpus-quality findings
- Logged at 2026-09-09 15:07 UTC
- 95 of 109 captures hold no news item at all (12015 filings, 662 news, 316 social across the sample) - the sample is two experiments and must be reported split. 37 of 109 are sealed on a 6-K acceptance time, which RZLV shows can be hours after the release. FINDINGS.md sections 36 and 37.

## Edge-corpus interim: zero-collapse returns
- Logged at 2026-09-09 15:20 UTC
- 48% of the first 25 scored names carry edge_score exactly zero (11 of 20 filings-only captures against 1 of 5 news-bearing). Half the ranking is ties. FINDINGS.md section 38.
