# Run log — 2026-09-04

## Stage 0 — universe (07:19 CEST)
- Logged at 2026-09-04 05:18 UTC
- Window: After the US close on Friday 04 September 2026 through before the US open on Tuesday 08 September 2026 (Monday 07 Sep is Labor Day; roll to Tuesday handled by get_earnings.py)
- Source: nasdaq (after-close + before-open)
- Universe: 5 total (0 AMC, 5 BMO); 2 eligible after qualification
- Excluded: 3 (below_market_cap_floor: WDH $0.35B, CAN $0.24B, GMHS $0.05B)
- Eligible: ABM, UNFI — both NYSE-listed, real listed-options markets, BMO timing cross-checked via WebSearch against a second independent source (investing.com for ABM, company press release for UNFI)
- Notes: three-day trading gap ahead of the window (Labor Day) means the before-open side rolls all the way to Tuesday 08 Sep; nothing else odd.

## Stage 1 — triage (10:31 CEST, run by stage 2 session — stage 1 Routine had not published)
- Logged at 2026-09-04 08:29 UTC
- Mode: skipped (universe 2 <= threshold 10)
- Funnel: 5 universe -> 2 eligible -> 2 cleared floors -> 2 shortlisted
- Scouts: 0 (screen skipped)
- Session mix: 0 AMC / 2 BMO
- Notable drops: none (stage 0 already excluded WDH, CAN, GMHS below market-cap floor)
- Note: 01-shortlist.json was absent when this session started (~2h after stage 1's scheduled 08:38 CEST fire); ran earnings-triage inline per earnings-deep-dive step 1's guidance rather than block stage 2

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-04 08:29 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: ABM
- Already on disk, skipping: none
- Plan: 1 wave of 1 opus/high researcher (ABM), publish after the wave

## Stage 2 — deep dive, batch 1 — FINISHED (08:50 UTC)
- Logged at 2026-09-04 08:51 UTC
- Researched: ABM
- Skipped (already done): none
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1
- Median evidence completeness: 80/100
- Panel-eligible after this batch: N/A (ranking runs after the final batch)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-04 10:26 UTC
- Shortlist: 2 names (ABM, UNFI); this batch: UNFI
- Already on disk, skipping: ABM (batch 1 completed)
- Plan: 1 wave of 1 opus/high researcher (UNFI), publish after the wave

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-04 10:43 UTC
- Researched: UNFI
- Skipped (already done): ABM (batch 1)
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1
- Median evidence completeness: 80/100
- Ranking: 02-ranking.json written from both dossiers (ABM, UNFI); shortlist change_expectation was null for both (triage_mode skipped_small_universe), so the panel_priority formula's 0.20 change_expectation weight was dropped and the remaining two renormalized -- documented in the ranking file's note
- Panel-eligible after this batch: ABM (45.13), UNFI (39.5) -- both eligible, both go to panel (panel.names=2, only 2 dossiers exist)

## Stage E — edge hunt — 2026-09-04 amc + 2026-09-08 bmo — STARTED
- Logged at 2026-09-04 14:11 UTC
- Window resolved to 5 confirmed names, all 2026-09-08 bmo: ABM, UNFI, WDH, CAN, GMHS. Today's Friday amc contributed nothing — all 12 calendar rows were time-not-supplied and were dropped per the phantom-rate rule (--include-unknown withheld).
- BUG FIXED FIRST: edge_universe.py --window skipped weekends but not NYSE holidays, so it resolved the Friday before Labor Day to Monday 2026-09-07 (market closed) and returned 0 of 19 rows. It now uses next_trading_day() from get_earnings.py, which already knew the calendar. Window is now 09-04 amc + 09-08 bmo.
- Baselines sealed and committed before any agent launches. All 5 fits_cadence, all with 7-8 exact 8-K item 2.02 reaction histories, no cadence_implausible, no suspect verdicts — no amend pass needed.
- Only 1 of 5 has a usable option chain (UNFI, event-implied 12.02%, but ATM spread 39% of mid = indicative only). ABM's chain exists but spread is 188% of mid = unusable. WDH/CAN/GMHS no chain. So 4 of 5 baselines infer what is priced from a 20d run-up rather than measuring it.
- Plan: 1 edge-sweep over all 5, then 7 unpriced-hunters (2 each on top 2 by hunt_priority, 1 on the other 3), then 5 priced-in-adversaries, 1 per ticker judging all findings on both sides. Total 13 subagents against the edge_hunt cap of 20 — no shed needed.

## Stage E — sweep + baseline amend — 2026-09-04
- Logged at 2026-09-04 14:16 UTC
- CORRECTION to the STARTED entry above: it claimed all 5 baselines were fits_cadence. They were not. CAN and GMHS carry verdict 'unknown' with cadence_implausible true; I read the console 'status: ok' column instead of event_plausibility.verdict. The sweep caught this.
- Sweep: 5 of 5 confirmed, ZERO phantom calendar rows, and every one of the five was pre-announced by the company's own press release WITH the hour, so session_unsettled is 0 too. All five are 2026-09-08 bmo. Second consecutive run with a zero phantom rate under the no---include-unknown rule.
- hunt_priority: UNFI 78, CAN 66, ABM 61, WDH 47, GMHS 33.
- Baseline history trustworthy on only 2 of 5. ABM and UNFI are domestic filers on exact 8-K item 2.02 acceptance times. CAN (13-day median gap, monthly bitcoin-production 6-Ks), GMHS (55-day median, 3 of 8 rows outside any reporting quarter, one tagged intraday) and WDH (three 6-Ks inside one quarter) are all the 6-K text-matcher defect.
- AMEND PASS, applied before any hunter launched: exactly ONE amendment, WDH fits_cadence -> unknown. A pass whose only entry is a downgrade. CAN and GMHS were deliberately NOT upgraded despite company-confirmed dates, per the DOO/PSNY/VBNK/ZGN precedent: the event is real but the history does not characterise it, and upgrading would forgive the history defect and hand each a 1.0 event multiplier it has not earned. Net: one name loses a multiplier, none gains one.
- Option-chain reality: 1 of 5 measured, 4 of 5 inferred. Only UNFI has a usable chain (event-implied 12.02%, ATM spread 39% of mid = indicative only). ABM's chain exists but the ATM spread is 188% of mid on 93 total OI. WDH and GMHS have no options market at all; CAN's legs are not two-sided. The 16:04 Amsterdam firing time did tighten UNFI's spread from the 41% seen on stale weekend marks, but only to 39% — the binding constraint is 1,765 contracts of front-expiry OI, not the hour.

## Stage E — edge hunt — COMPLETE
- Logged at 2026-09-04 15:07 UTC
- Ranked 5 of 5: UNFI +6.4, WDH +0.1, ABM 0.0, CAN -10.6, GMHS -11.6. Spread is 0.90 points of spot end to end (+0.32 to -0.58) against a 12.02% option-implied move on the only name with a chain. Only 3 positions are meaningfully distinct — WDH and ABM differ by 0.002 points of spot and should be read as tied, not as ranks 2 and 3.
- Zero phantom rate for the second consecutive run. All 5 confirmed date AND hour from company press releases. All 12 of today's Friday amc rows were time-not-supplied and were dropped.
- BASELINE DEFECT FOUND AND VERIFIED, and it inverts this run's bottom rank. GMHS 2025-09-09 (the FY25 annual print, the closest analogue to this event) is recorded as -18.78%. Daily bars: 2025-09-08 close 1.73, 2025-09-09 close 2.29 on 22.5m shares, 2025-09-10 close 1.86. The real overnight reaction was +32.37%; the recorded number is the next-day give-back. Cause: prior_prints tags session from the EDGAR ACCEPTANCE time (amc if >=16:00 ET), but Gamehaus released 06:00 ET and furnished its 6-K later the same day, so reaction() measured event-close -> next-close. EDGAR acceptance time is the filing time, not the news time — for an FPI the 6-K routinely trails the release by hours. The GMHS hunter reasoned explicitly from 'the one clean analogue was -18.78%' and ranked the name last of five, so the most heavily weighted item in that reasoning has the OPPOSITE sign.
- DID NOT re-run the baseline or re-score. Findings were already in hand and I knew which way the correction cuts; re-running there is exactly how a scorer gets tuned toward a result. GMHS keeps rank 5 in edge-scores.json and the note records that rank 5 is untrustworthy. Fixed for FUTURE runs instead: priced_in.py now carries session_disagrees_with_volume(), advisory only, adding history.session_conflicts plus a per-row session_conflict block. Validated in a scratch dir against GMHS: catches that row and none of the other seven, reporting move_if_bmo_pct +32.37 vs move_as_tagged_pct -18.78. smoke_test passes.
- Two-hunter split earned its cost again. UNFI's two isolated hunters returned OPPOSITE signs (-3.0 and +1.8) off the same sealed baseline — dispersion 1.302 pts, the day's highest — and independently found the same undisclosed fact (Echols ceasing as Chief Corporate Affairs Officer 2026-08-24, in a Form 4 with no 8-K) and read it opposite ways. CAN's two converged (-6.0, -6.5). UNFI-h2 also refuted a premise the sweep gave it: told 'only 2 EPS estimates', it found nine analysts.
- Adversary: 27 of 27 findings judged on both sides, join verified clean by edge_brief.py --check. EIGHT factual refutations, not mere discounts — notably GMHS#1 sized a $200m shelf at 4.5x market cap when the cover page of its own cited source caps primary sales at ~$7.8m via F-3 General Instruction I.B.5 (overstated ~25x); ABM#0's 'after ABM last guided' framing is wrong for 2 of 3 carriers and its route suspensions land in Q4 not Q3; and CAN-h2#0 rested partly on an investing.com page carrying an auto-populated Q2 revenue 'actual' for an event that has not happened. Best survivor: UNFI-h2#0 at priced_in 30 — the US Foods fuel-surcharge read-across, whose facts the adversary verified verbatim while attacking only the foodservice-to-wholesale joint.
- Sign balance: 6 of 7 hunts and 19 of 27 findings leaned negative. The 2026-08-31 run was 6 of 8. Two consecutive runs at ~3/4 negative is more plausibly an artefact of asking hunters to find what the market missed into a print than a fact about these companies.
- Baseline measured vs inferred, worse than 2026-08-31: option chain usable on 1 of 5 (UNFI, and only 'indicative' at 39% of mid on 1,765 OI; ABM's is 188% of mid on 93 OI). Market-implied DIRECTION on 0 of 5 — no skew anywhere, so priced_direction is 0.0 for every name and baseline_quality is capped at 0.75. All five priced_lean values are the run-up fallback; the x0.55 agreement discount fired on 4 names against a lean the options market never stated. CAN's lean is -3.49% purely from being +69.8% in 20 days, halving its negative findings for 'agreeing with the price'.
- Reaction history trustworthy on 2 of 5 (ABM, UNFI on exact 8-K item 2.02). Amend pass before launch was ONE entry and it was a downgrade: WDH fits_cadence -> unknown. CAN and GMHS deliberately NOT upgraded despite confirmed dates. The WDH hunter and adversary then independently refined it: true last print is 2026-06-17 (Q1, +2.34%), not 2026-07-24, so the gap is 83 days vs an 85-day median and the cadence axis does fit — 6 of 8 rows are earnings, not 5. Not re-amended mid-run; it is the starting point for the next run on WDH.
- STRUCTURAL ISSUE RECORDED, NOT CHANGED: edge_score.py clusters by source DOMAIN, so every SEC filing is one 'sec.gov' cluster and only the largest residual in it survives. Five of CAN's findings came from five distinct primary documents and collapsed to one number. This penalises primary-filing work relative to citing five news sites, which is backwards. Not altered with today's findings in hand, since it would have raised CAN. Design question for a future run: cluster on the document, not the domain.
- ALSO FIXED FIRST, before the universe was built: edge_universe.py --window skipped weekends but not NYSE holidays, so the Friday before Labor Day resolved to Monday 2026-09-07 (market closed) and returned 0 of 19 rows — an empty universe indistinguishable from a thin day. Now uses next_trading_day() from get_earnings.py, which already knew the calendar.
- Spend: 13 subagents of the 20 cap (1 sweep + 7 hunters + 5 adversaries). Nothing shed, no degradation step taken.
- ONE DAY IS AN ANECDOTE: n=5 with two tied cannot produce a meaningful rank correlation. edge_resolve.py on this run alone will return noise. The pooled figure across many days is the result.

## Capture - 2026-09-04 - STARTED
- Logged at 2026-09-04 15:07 UTC
- Plan: universe-only sweep via capture.py --horizon-days 15 (script-only, no cap floor), then agent-layer nine-area capture for the 6 largest names reporting within 3 days, publishing after each name.

## Capture — 2026-09-04 — script-only sweep done
- Logged at 2026-09-04 15:18 UTC
- capture.py --horizon-days 15 (no --universe-only): 168 events in window, 337 tracked total, 1080 new documents (mostly EDGAR filing pointers + refreshed 63-day price bars; StockTwits captured for d<=2 events).
- Zero tripwires flagged by the script across all 168 events.

## Capture — 2026-09-04 — NB
- Logged at 2026-09-04 15:31 UTC
- Agent discovery: 48 queries across 9 areas (skipping raw price/volume + Form4/8-K enumeration), 45 URLs marked for fetch. Event genuinely upcoming (no post-earnings evidence found) but calendar date looks WRONG: 5 independent sources (stockanalysis, nasdaq, earningswhispers, tipranks, wallstreetzen) converge on the real date being 2026-09-09/10 AMC, not 2026-09-04 -- consistent with NB's own FY-end cadence (FY25 annual print ~Sept 11 2025). Captured under the tracked 2026-09-04 event_date since that is what the universe carries; event has not happened, so no leak risk from the date being off.
- capture.py: 30 new documents, 2 tripwires fired (both StockTwits pages, area 7 sentiment). INVESTIGATED: both tripwires are FALSE POSITIVES -- identical embedded JSON blob ('...post-earnings selloff as a manipulation-driven buying opportunity...', 'agentic AI', 'narrowing gross margins') is StockTwits sidebar/trending-widget boilerplate about a wholly unrelated company, not about NB (a rare-earth/scandium miner) or its own earnings. Confirmed by grepping both docs: identical string in both, describing a company profile (agentic AI pivot) that does not match NB at all. No corpus corruption; the 'stock jumped 7%' language in the other tripped doc is genuinely about a real, dated (Oct 2025 / Mar 2026 update) Lockheed Martin defense-contract catalyst, not an earnings reaction.

## Capture — 2026-09-04 — HTLM
- Logged at 2026-09-04 15:35 UTC
- Agent discovery: 45 queries across 9 areas, 40 URLs marked for fetch. Event genuinely upcoming (no post-earnings evidence found), but exact date uncertain across sources (Nasdaq implies 08/15, Moomoo shows a stale Nov echo, calendar says 09/04); HTLM reports semi-annually via 6-K and last year's H1 print landed Sept 17 2025, so a September print is plausible but not pinned to 09/04 by any source. Notable pre-print finding: a new Form F-1 (~Aug 2026) registering a fresh share offering + over-allotment, a dilution overhang landing right before the print.
- capture.py: 18 new documents, 0 tripwires.

## Capture — 2026-09-04 — NRT
- Logged at 2026-09-04 15:45 UTC
- Agent discovery: 38 queries across 9 areas, 33 URLs marked for fetch. Event genuinely upcoming: NRT is a passive royalty trust, not an EPS reporter -- the Q3 distribution (/bin/bash.26/unit) was already declared 2026-07-30 (paid 08-31, now stale news), but the 10-Q itself was stated by the trust's own release to post 'on or about September 4, 2026' -- today -- and no early/posted 10-Q was found. Notable macro context surfaced: European TTF gas spiked above EUR70-73/MWh in late Aug/early Sept on a Hormuz disruption, a tailwind for NRT's EUR-linked royalty stream.
- capture.py: 22 new documents, 1 tripwire (StockTwits symbol page, area 7). INVESTIGATED: confirmed FALSE POSITIVE, same root cause as NB's two tripwires earlier today -- identical embedded StockTwits sidebar/trending-widget JSON blob about an unrelated 'agentic AI' company's post-earnings price swings, not about NRT. This is now the THIRD occurrence of the exact same boilerplate string tripping the post-earnings tell today (2x NB, 1x NRT), all from stocktwits.com pages. SCRIPT-DESIGN FINDING for a future run: corpus_news.py's tell-scan should probably strip or de-scope shared page furniture (nav/sidebar/trending widgets) before running tripwire regexes against a StockTwits page body, since the same third-party boilerplate is now a confirmed recurring false-positive source across multiple tickers. Not fixed mid-run per the project's own precedent (investigate and record, don't tune the detector mid-flight).

## Capture — 2026-09-04 — IMPP
- Logged at 2026-09-04 15:45 UTC
- Agent discovery: 45 queries across 9 areas, 37 URLs marked for fetch. Event NOT yet happened, but calendar date is WRONG: IMPP's own press release (GlobeNewswire 3356593, issued today) states the real Q2/6-months 2026 results date is 2026-09-10 BMO, call 10:00am ET -- 6 days later than the tracked 2026-09-04. Namesake-collision risk flagged: an unrelated 2013-2016 Indiana biodiesel-fraud 'Imperial Petroleum' SEC case and 'Imperial Oil' (IMO) both surface on generic queries and must not be conflated with NASDAQ:IMPP. Analyst price-target aggregators disagree wildly (2.13 vs .00 avg) -- data-quality flag, unresolved.
- capture.py: 13 new documents, 1 tripwire (StockTwits symbol page, area 7). INVESTIGATED: confirmed FALSE POSITIVE, same exact root cause as NB (x2) and NRT (x1) earlier today -- identical embedded StockTwits sidebar/trending-widget JSON blob about an unrelated 'agentic AI' company, not about IMPP. Fourth occurrence of the identical string today; strengthens the script-design finding already logged under NRT's entry.
