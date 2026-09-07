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

## Stage E — edge hunt — FINISHED
- Logged at 2026-09-07 15:01 UTC
- Universe: 6 names, all 2026-09-08 bmo (ABM, UNFI, WDH, CAN, DLNG, GMHS). Sweep confirmed 6 of 6 from company sources with an hour attached: ZERO phantom calendar rows, ZERO unsettled sessions. --include-unknown withheld.
- Ranked, 6 of 6 rankable, 6 distinct scores, strict order: ABM +1.7 (conf 18.0) > WDH +1.5 (9.6) > DLNG -8.7 (14.9) > UNFI -9.0 (42.1) > CAN -9.9 (3.8) > GMHS -11.3 (13.9). edge_pct spans only +0.09% to -0.57% of spot. Score is a ranking key, not a forecast.
- Sign balance: 7 of 8 hunts leaned negative, 1 positive (ABM +1.5). More one-sided than 08-31's 6-of-8; flagged in the note as more plausibly an artefact of the hunter prompt than a fact about six companies. Watch it across runs.
- Adversary: 34 findings, 34 verdicts, JOIN CLEAN. Median priced_in 65.5, range 38-88. Three findings REFUTED ON FACT: GMHS#0 (claimed Q4 FY2025 revenue was never reported -- company reported US$30.7m verbatim twice on 2025-09-09), CAN-a#2 (claimed the June insider cluster was invisible -- company press-released it 2026-06-24 and the stock fell 5.87% that day; cluster also under-enumerated 565k vs 1,065k ADS), WDH#2 (called RMB639.6m undisclosed while WDH#0 in the same brief cites it as disclosed).
- Survived best: DLNG#1 at 38% priced -- Clean Energy idle at anchor 33 days on a Rio Grande charter, AIS-verified by the adversary itself, no media coverage found; size cut to -1.2pt because time-charter hire is paid regardless and the idling began 5 Aug, i.e. Q3, outside the reported quarter.
- Most informative output: the two isolated CAN hunters (-6.0 vs -4.0) disagreed on FACT about whether Canaan has issued equity off its shelf. Adversary resolved it from primary filings -- last 424B5 was 2025-11-04, none in 2026, and the one large 2026 issuance (806,439,900 Class A to Cipher Mining) is UNREGISTERED, which is exactly why the second hunter's Rule 144 lock-up argument works. Both hunters consistent; neither wrong. That resolution exists only because neither could see the other.
- Baseline measured vs inferred: only ONE name of six has a usable chain (UNFI, 13.15% implied, +6.97 skew, 1,789 OI, baseline_quality 0.87). ABM's 8.13% is indicative only -- 93 contracts front-expiry OI, ATM spread 78% of mid -- and the adversary was told to treat it as unusable and did. WDH/CAN/DLNG/GMHS have no options, so priced_lean_pct falls back to -0.05 x 20d run-up. Five of six inferred, not observed.
- Baseline amendment: ONE entry, a DOWNGRADE. WDH fits_cadence -> unknown (three 6-Ks inside one quarter, a literal duplicate row, and a 'last print 46 days ago' that would make 09-08 a second print in the same quarter). CAN/DLNG/GMHS deliberately NOT upgraded despite company-confirmed dates with the hour -- upgrading would forgive a history defect. No name gained an event multiplier. scripts/edge_baseline_amend.py's per-run table was stale (dated 09-04) and was rewritten from this run's sweep before applying.
- Sweep also caught: DLNG announced this date TWICE -- 2026-09-01 said 09-07 amc, superseded 2026-09-02 by 09-08 bmo, almost certainly because 09-07 is Labor Day. A hunter on the first release would have had the wrong session. Dynagas holds no earnings call, so the session rests on company wording, not a call time.
- Budget: 15 of the edge_hunt cap of 20 (1 sweep + 8 hunters + 6 adversaries). No shed; edge_degrade_order not invoked. Two-hunter split applied to UNFI (priority 78) and CAN (72). No option-chain deviation needed -- both names with any chain were already above median priority.
- ONE DAY IS AN ANECDOTE: six names cannot produce a meaningful rank correlation. Stated in the note. The pooled figure from edge_resolve.py --pool is the result; this is one row of it.

## Capture — 2026-09-07 — STARTED
- Logged at 2026-09-07 15:06 UTC
- Sweep universe --horizon-days 15 script-only, then agent-layer capture for top 6 by market cap reporting within 3 days, per earnings-capture skill.

## Capture — 2026-09-07 — ORCL tripwire investigated
- Logged at 2026-09-07 15:26 UTC
- Tripwire fired on stocktwits.com/symbol/ORCL/sentiment (area 7, sha fe85856e...): matched beat/estimates regex. Investigated: the match text is a SNOW (Snowflake) news blurb embedded in ORCL's stocktwits related-news widget ('SNOW's Q2 earnings and revenues beat estimates'), not ORCL post-earnings language. The same document's structured upcomingLatestData block independently confirms ORCL callDate=2026-09-10, callTime=after_market, resolving in favor of the Sept-10 AMC date over the stale Sept-8 calendar row. Document kept in corpus; false positive, no upstream bug found.

## Capture — 2026-09-07 — SUNB tripwire investigated
- Logged at 2026-09-07 15:27 UTC
- Tripwire fired on stocktitan.net SUNB 10-K filing summary (area 5, sha f4dc54d8...): matched 'reported revenue of' regex. Investigated: the match is the company's FY2026 full-year revenue (year ended April 30, 2026, $11,154M) disclosed in the 10-K FAQ, i.e. the PRIOR fiscal year already reported in the annual report -- not the upcoming Sept 9, 2026 quarterly print. Document kept in corpus; false positive, no upstream bug found.

## Capture — 2026-09-07 — COO coverage gap
- Logged at 2026-09-07 15:29 UTC
- COO's search agent exhausted its WebSearch call budget (200/200) partway through; areas 7 (sentiment/alt-data) and 9 (macro/peers) were never searched for this name. Areas 1,3,4,5,6 completed (25 queries, 38 URLs selected, 17 new docs captured). Recorded as a genuine coverage gap, not papered over.

## Capture — 2026-09-07 — CASY tripwires investigated (2)
- Logged at 2026-09-07 15:31 UTC
- Two tripwires on CASY. (1) scanx.trade Q1 preview (sha ea14e24c...): matched miss/post-earnings regex, but text is a hypothetical preview question ('what could cause the company to MISS the consensus EPS estimate', 'could...lead to volatility POST-EARNINGS') -- speculative, not reported outcome. (2) trefis.com preview (sha ba3ca4ab...): 'stock rose/fell' match is a related-articles widget about OTHER tickers (Cadence, BridgeBio, Autodesk, CNH), not CASY; 'post-earnings' mentions are the article's historical-reaction-pattern methodology discussion (pre-event analytical content), not this print's outcome. Both false positives; documents kept in corpus.

## Capture — 2026-09-07 — CASY coverage note
- Logged at 2026-09-07 15:31 UTC
- CASY search agent's WebSearch budget was exhausted mid-sweep: 30 of 35 planned queries executed, 5 not run (recorded as gaps in the plan, not fabricated). Consensus EPS shows source disagreement ($6.59 calendar vs $6.78/$6.81 aggregators), left unreconciled per no-analysis rule.

## Capture — 2026-09-07 — DONE
- Logged at 2026-09-07 15:31 UTC
- 175 events swept script-only (15-day window, no cap floor), 1369 new documents, 0 tripwires, 5 minor errors (4x stocktwits on illiquid names, LEN.B edgar+quote -- known dual-class CIK issue per FINDINGS.md sec.3). Agent layer: 6 largest names reporting within 3 days (ORCL, ADBE, SUNB, CPRT, CASY, COO) -- 207 queries issued, 125 new documents, 0 snippet_only (no fetch blocks today), 4 tripwires all investigated and confirmed false positive (cross-ticker news widgets, prior-fiscal-year 10-K disclosure, hypothetical preview-article questions -- see prior run-log sections). Coverage gaps: COO missed areas 7+9 entirely and CASY missed 5 of 35 planned queries, both from the search agent's own WebSearch call budget running out mid-sweep, not from thin source availability. Data-quality finding: ORCL and CPRT each carried a stale duplicate calendar row (ORCL 09-08 vs corrected 09-10; CPRT 09-03, already past today, vs corrected 09-10) -- capture.py dedupes universe.json by (ticker,event_date), so a corrected Nasdaq calendar row does not retire the old one; both stale rows are now permanently in universe.json alongside the corrected ones. Worth a maintainer look at capture.py's merge key. No names skipped.

## Stage 3 — panel & advice — STARTED
- Logged at 2026-09-07 15:54 UTC
- Panelling both panel-eligible names from 02-ranking.json: ABM (panel_priority 35.5), UNFI (panel_priority 33.35). panel.names=2, both fit, no degrade needed.
- Note: same underlying event (ABM/UNFI report 2026-09-08 BMO) was already panelled on 2026-09-04, whose window rolled through the Sept 7 Labor Day to the same Sept 8 open. This run is a fresh, independent re-panel one day closer to the print, with anchors re-sourced today rather than reused.
- Plan: refresh spot + implied move for both names, build Phase-0 anchor packets, spawn 7 persona subagents per name (14 total) in parallel, synthesize each, chair review, write panel files + dossiers + advice note, publish.
