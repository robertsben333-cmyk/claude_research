# Run log — 2026-09-17

## Stage 0 — universe — 07:14 CEST
- Logged at 2026-09-17 05:14 UTC
- Window: After the US close on Thursday 17 September 2026 through before the US open on Friday 18 September 2026
- Source: nasdaq (after-close 15 rows, before-open 8 rows; 1 in window)
- Universe: 1 total (1 AMC, 0 BMO); 0 eligible after qualification
- Excluded: 1 (below_market_cap_floor: UPXI, $76.0M market cap vs $500M floor)
- Notes: Thin actionable window as of this run — not a holiday, just few confirmed prints on the calendar yet. Eligible count (0) is at or below triage.skip_if_universe_at_or_below (10), so stage 1 will skip today.

## Maintenance — per-name cap raised to 33% of equity
- Logged at 2026-09-17 06:38 UTC
- execution.sizing.max_position_pct_of_equity: 20 -> 33, on the operator's instruction. Live on main from this commit; it applies to the NEXT book, not to the ALMU and LEN positions already open, which were sized under the 20% cap.
- At the current paper equity of ~$11,260 a capped name is $3,710. Two names deploy 66% of the account, three names 99%. Below three names the book is deliberately under-invested, where that used to be below five.
- What it costs, stated rather than buried: concentration. The 22-23% gaps in the resolved sample (NX +22.23%, CANG -23.01%) move the account about 7.5% at a 33% weight against 4.5% at 20%. Nothing in this stage is hedged or stopped out, so the cap is the risk control.
- max_position_pct_of_adv stays at 1.0%. At $10k of equity a 33% position is 1.65% of a $200k/day name, so capacity now binds before equity in the thinnest tradable names and the leftover is redistributed over the rest of the book.
- Updated with it: config comments, edge/EXECUTION.md (four passages), CLAUDE.md. scripts/smoke_test.py no longer hardcodes the old cap in its under-deployment check; it reads the shipped numbers and is green.

## Stage 1 — triage (08:40 CEST)
- Logged at 2026-09-17 06:40 UTC
- Mode: skipped (universe eligible count 0, at or below threshold 10)
- Funnel: 1 universe -> 0 eligible -> 0 cleared floors -> 0 shortlisted
- Scouts: 0 subagents (nothing to screen)
- Session mix: n/a
- Notable drops: UPXI (excluded at stage 0, market cap $76.0M < $500M floor)
- Note: validate_stage.py's shortlist check previously required a non-empty list, which a genuinely empty eligible universe can't satisfy under skip-mode; fixed to allow shortlist: [] when triage_mode is skipped_small_universe and universe_eligible is 0.

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-17 08:22 UTC
- Shortlist: 0 names (triage_mode: skipped_small_universe, universe_eligible: 0); this batch: none
- Already on disk, skipping: none
- Plan: no researchers to spawn — shortlist is empty because today's universe had only 1 AMC print (UPXI, $76.0M market cap) which failed the $500M floor at stage 0, so stage 1 skipped with 0 names

## Stage 2 — deep dive, batch 1 — FINISHED (08:23 UTC)
- Logged at 2026-09-17 08:22 UTC
- Researched: none (shortlist empty)
- Skipped (already done): none
- Failed: none
- Subagents: 0 opus/high, 0 waves
- Median evidence completeness: n/a
- Note: 0 names capped from a shortlist of 0 — nothing dropped for the cap. Confirmed against 00-universe.json/01-shortlist.json before publishing this section, not just the earlier run-log entries.

## Close AMC — amc opening-auction exit — 2026-09-17
- Logged at 2026-09-17 10:11 UTC
- Guard: python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg exited 0 (execution.enabled=true, orders.exit_mode=amc_open, amc -> opg / bmo -> day). Proceeded.
- verify --scan 'research/*/*/*/edge' first: 9 of 11 exit legs already ok/closed from prior days (HOFT, FEIM, ORCL, RH, CODA, VRA, FPS, RLGT, LUXE all still held 0.0). ALMU and LEN (2026-09-16/edge, amc, exit_date 2026-09-17) were the only legs due today: still held 167 and 28 respectively, 0/167 and 0/28 filled — expected, fired pre-open.
- SENT: 2026-09-16/edge ALMU, amc session, exit_date 2026-09-17, opg (opening auction), qty 167 buy-to-cover, order 43561a60-077d-4108-9584-df101aa9bb2d, status pending_new at submission.
- SENT: 2026-09-16/edge LEN, amc session, exit_date 2026-09-17, opg (opening auction), qty 28 buy-to-cover, order af499521-2c8d-4331-960e-5e52f5ae53bf, status pending_new at submission.
- No bmo legs due today; no refusals this run.
- Post-submit verify (after the script's 300s fill-check wait): ALMU and LEN both report 'work' — filled 0, still held 167.0 / 28.0, 'waiting on the 09:30 ET opening auction; not verifiable until it has crossed'. Expected: an opg order does not fill until the auction runs, well after this pre-market firing.
- status --scan confirms both still OPEN: ALMU -167 @ 13.35 (+13.86% unrealized), LEN -28 @ 79.96 (+4.50% unrealized); exit order state 'new' for both.
- Account reachable throughout: paper, equity $11,669.19, cash $15,727.77, buying power $40,771.06.
- Not a rescue point: firing before 09:28 ET means no plain-market rescue is available here even if the auction cross under-fills (documented behavior: HOFT 17/161, CODA 39/183, RLGT 0/224 in past runs). Stage E's own run inside the session is what carries an UNFILLED leg forward via 'verify --fix'.

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-17 10:23 UTC
- Shortlist: 0 names (triage_mode: skipped_small_universe, universe_eligible: 0); this batch: none (N=ceil(0/2)=0, batch 2 covers positions 1..end of an empty capped list)
- Already on disk, skipping: none (02-dossiers/ is empty)
- Batch 1 already ran and correctly found 0 names to research (not a failure — the empty shortlist is genuine: universe_total 1, universe_eligible 0). No gap to cover.
- Plan: no researchers to spawn; confirm against 00-universe.json/01-shortlist.json, then write 02-ranking.json (empty) since this is the final batch.

## Stage 2 — deep dive, batch 2 — FINISHED (10:24 UTC)
- Logged at 2026-09-17 10:23 UTC
- Researched: none (shortlist empty — universe_total 1, universe_eligible 0, UPXI excluded at stage 0 for market cap $76.0M < $500M floor)
- Skipped (already done): none
- Failed: none
- Subagents: 0 opus/high, 0 waves
- Median evidence completeness: n/a
- 02-ranking.json written (final batch): 0 names, panel_names_top_n 2, top_n_for_panel []
- Panel-eligible after this batch: none

## Stage 3 — panel & advice — 15:55 UTC
- Logged at 2026-09-17 15:55 UTC
- Panelled: none — 02-ranking.json exists with names: [] and top_n_for_panel: [] (universe had 1 candidate, UPXI, excluded at the $500M market-cap floor; universe_eligible 0).
- Calls: none.
- Panel seats filled: n/a (no names to panel).
- Chair overrides: none.
- Degradations: none — nothing to shed; this is a genuinely empty day, not a budget cut.
- 04-advice.md/.json written with status: no_names; ranked field lists UPXI's exclusion for context.

## Edge hunt — 2026-09-17 amc + 2026-09-18 bmo — STARTED
- Logged at 2026-09-17 17:09 UTC
- Stage E fired 17:05 UTC (13:05 ET). Repo on main @ 15999ff; scripts/edge_score.py, scripts/priced_in.py and the skill all present.
- Step 0b (execution.enabled: true, exit_mode: amc_open, paper endpoint): NOTHING TO SELL. verify --scan over 5 runs / 11 exit legs returned ok on all 11, still-held 0.0 on every leg. Alpaca account is flat: equity $11,527.83, cash $11,527.83, 0 positions, 0 open orders. close --scan --submit ran and sent nothing. Yesterday's book (LUXE bmo, ALMU/LEN amc) was already closed before this session. Unrealised P&L on the exit is therefore not this session's to record — no position was held at 17:05 UTC.
- Universe: 22 calendar rows over the window (15 on 09-17, 7 on 09-18). 20 of 22 are time-not-supplied and were dropped per the skill (8 of 8 such rows were phantom on 2026-08-31). Of the 2 rows carrying an explicit session, IPHA is 09-17 bmo — already past, outside the window. ONE name in the window: UPXI (Upexi, Inc.), 2026-09-17 amc, $77m cap. --include-unknown deliberately withheld.
- Baseline sealed for UPXI before any agent launches: spot $1.05, straddle implied move 11.43% off a LIVE option chain (measured, not the historical-median fallback), event_plausibility fits_cadence (127 days vs 92-day cadence), 6 prior reactions off exact 8-K item 2.02 acceptance times, median abs move 6.58%, run_up_20d 19.32%.
- Plan: 1 sweep + 1 hunter = 2 of the 20-subagent cap. A one-name day cannot be ranked — there is nothing to rank it against — so today contributes one event to the pooled sample and no within-day correlation.

## Edge hunt — 2026-09-17 — sweep
- Logged at 2026-09-17 17:15 UTC
- 1 of 1 CONFIRMED, 0 phantom, 0 session-unsettled. UPXI's FY2026 print is company-confirmed by a 2026-09-15 GlobeNewswire release naming a 5:30 p.m. ET call on 2026-09-17 (date verified on the URL path), so amc is settled and the reaction session is the 2026-09-18 regular session. hunt_priority 78.
- The sweep set baseline_history_trustworthy: FALSE, and this is the run's most important caveat. priced_in.py built UPXI's six-print reaction history from what it took to be 8-K item 2.02 acceptance times, but EDGAR supports only one of them (2026-02-10, accepted 22:15:30 UTC, items 2.02/8.01/9.01). The 2025-11-12 row lines up with two 8-Ks carrying items 8.01/9.01 and no 2.02 while the company's own release put that earnings call on 11-11; the 2026-05-13 row is a day off the Q3 8-K accepted 2026-05-12 at 20:40:59 UTC. Upexi files 8.01 current reports constantly (SOL holdings, buybacks, treasury) — the exact contamination mode the skill warns about, plainly present. median_abs_move_pct 6.58 and deadband_pct 3.29 therefore inherit the defect and were NOT passed to the hunter as a base rate.
- No baseline amendment applied. edge_baseline_amend.py dry-run proposed nothing, correctly: event_plausibility is fits_cadence (127d vs 92d) and the sweep confirmed the event, so the event-existence flag is right. The defect is in the reaction history, which that script does not touch — it is recorded here and was handed to the hunter in prose instead.
- Everything else in the baseline stands: spot $1.05, run_up_20d 19.32%, avg 20d volume 4.57m (~$4.8m/day turnover, clears the $200k floor and the $1m thin threshold). The option chain is LIVE rather than the historical-median fallback, but only barely — front expiry 2026-09-18 at 1 DTE, ATM spread 67% of mid, total OI 11,453, put/call OI 0.06. The baseline itself warns the 11.43% implied move is indicative only.
- 1 hunter launched on UPXI. Spend: 1 sweep + 1 hunter = 2 of the 20-subagent cap. Nothing shed — the window is one name, so budget.edge_degrade_order never engaged.

## Edge hunt — 2026-09-17 — hunt, score, book
- Logged at 2026-09-17 17:26 UTC
- 1 hunter on UPXI returned the CURRENT contract in full — findings with lands_on and resolves_by, expected_move_pct, print_vs_bar_pct, bar, positioning_check, outside_window, pre_lessons, lessons_applied. No agent-definition drift: the tree's .claude/agents/unpriced-hunter.md is the one that ran. 16 sources, 6 findings in-window, 4 outside.
- RANKING KEY, as edge-scores.json names it in ranking_key: impact_sum, the hunter's signed per-finding sizes summed, in points of spot. UPXI impact_sum -2.30, conviction 2.30. 1 of 1 rankable, 0 of 1 clears the conviction floor of 3.0. Control -run_up_20d_pct = -19.32. legacy edge_score -0.80, priced_lean_pct -0.97 — both diagnostics, neither decides anything.
- A ONE-NAME DAY CANNOT BE RANKED. There is nothing to rank UPXI against, so this run contributes one event to the pooled sample and no within-day Spearman at all. edge_resolve.py will have nothing to report for 2026-09-17 standalone. That is the day, not a failure.
- Most interesting finding (-1.2): two live Nasdaq deficiencies with zero media coverage — a 2026-06-24 Staff determination that Upexi violated Listing Rule 5635(a) by issuing $151.2m of converts at $4.25 and ~$36m at $2.39 without shareholder approval, remediation plan due 2026-08-10 with no 8-K reporting acceptance and no proxy filed; plus a 2026-07-31 $1.00 bid-price notice with a 2027-01-26 deadline. https://www.sec.gov/Archives/edgar/data/1775194/000147793226004047/upxi_8k.htm — a targeted search returns the SEC document and law-firm explainers, nothing else, against a BitGo amendment three days ago that was picked up everywhere. Sized only -1.2 because the 10-K may not be filed before the 2026-09-18 close (FY2025's went in 2025-09-24), in which case the risk factors never appear inside the exit window.
- THE ADVERSARY DID NOT BREAK IT, BECAUSE THERE IS NO ADVERSARY. diagnostics.adversary_judged reads 0/6. Nothing in this run checked any finding for being factually wrong. Removed 2026-09-09 as measured-subtractive; not reinstated, not improvised around, and no finding was dropped or shrunk here on a priced-in judgement of mine.
- edge/LESSONS.md moved the number and by how much is on the record: pre_lessons sum -3.5 -> -2.3, lessons_delta 1.2. Driven by capping sizes on a one-source bar ($7.00m revenue / ($0.09) EPS, MarketBeat family, uncorroborated — TipRanks attaches the same -0.09 to a different fiscal quarter), shrinking negatives into a 27.33%-of-float short rather than only offsetting them, and resolving a finding that contained its own rebuttal. ONE DAY'S DELTA IS NOISE — it takes several resolved days carrying both numbers before spearman_pre_lessons says anything.
- Sign balance: 1 of 1 hunts leaned negative; findings split 2 positive / 4 negative. edge_score flagged that the sum nets opposing theses rather than resolving them — the gross negative case is about -4.8 and nets to -2.3. Second flag: 4 sourced findings worth -16.0 dated after the exit window, correctly kept out of the key.
- Baseline measured vs inferred: 1 of 1 names has a LIVE option chain, but barely — front expiry 2026-09-18 at 1 DTE, ATM spread 67% of mid, total OI 11,453, put/call 0.06. The baseline's own warning is 'implied move is indicative only', so the 11.43% straddle was not handed to the hunter as a market view.
- STEP 7 — NOTHING TRADED, and this is the benchmark working, not a failure. execution.enabled: true, exit_mode amc_open, paper endpoint. plan: 'no name meets the benchmark'. open --submit --no-flatten: 0 orders, 154 minutes to the close, so no closed-market refusal was involved. status: equity $11,527.83, cash $11,527.83, 0 positions. 1 name met the benchmark's rankable test and 0 met the conviction floor (2.30 < 3.00). No fills to compare against plan notional — there were none. Gross 0% of equity.
- Refusals, in full: UPXI — below the conviction floor (2.30 < 3.00). Note separately that alpaca_trade.py assets asked live and got shortable=false for UPXI, so the negative row could not have been taken even had it cleared: liquidity is fine ($4.80m/day, above the $200k floor and the $1m thin threshold), the constraint is borrow. Reported as 'elsewhere' rather than 'no' — a short Alpaca will not lend is routinely borrowable at IBKR, and COE read borrowable the morning after this book refused it.
- Step 0b reprise for completeness: nothing was sold because nothing was held. The account was already flat at session start and 11 tracked exit legs across 5 runs all verified ok with 0.0 still held.
- SPEND: 2 of the 20-subagent cap (1 sweep + 1 hunter). Nothing shed. Session 17:05-17:30 UTC, ~25 minutes end to end against the 2h53m of the 2026-09-09 run — the 17:04 Routine's three-minute entry margin was never tested today and remains the standing risk on a normal-sized day.

## Edge hunt — 2026-09-17 — CORRECTION: the sweep's baseline allegation was false
- Logged at 2026-09-17 17:28 UTC
- Posted after the note was first published, on a hand re-check of EDGAR. EARLIER ENTRIES IN THIS LOG THAT CALL THE UPXI BASELINE HISTORY CONTAMINATED ARE WRONG — the baseline is clean and the SWEEP was wrong.
- The sweep set baseline_history_trustworthy: false and claimed EDGAR supported only one of the six baseline prints. Checked against https://data.sec.gov/submissions/CIK0001775194.json, all six baseline dates ARE exactly the six most recent 8-K item-2.02 acceptances: 2026-05-13, 2026-02-10, 2025-11-12, 2025-09-26, 2025-05-16, 2024-12-23. priced_in.py filters on the item code at edge/scripts/priced_in.py:218 and filtered correctly. NO DEFECT IN priced_in.py — do not go looking for one on the strength of the earlier entries.
- The sweep's two specific claims, both refuted by that feed: (a) it said the 2025-11-12 row lines up with 8-Ks carrying items 8.01/9.01 and no 2.02 — the 2025-11-12 8-K carries items 2.02,9.01 accepted 21:06:12 UTC, and the 8.01/9.01 filing is dated 2025-11-14, a different filing two days later; (b) it said the 2026-05-13 row is measured a session late against a Q3 8-K accepted 2026-05-12 at 20:40:59 UTC — that filing is the 10-Q, not an 8-K, and the item-2.02 8-K is 2026-05-13 accepted 20:35:40 UTC.
- CONSEQUENCE FOR THE KEY. median_abs_move_pct 6.58, the 2-up-of-6 skew and deadband_pct 3.29 were all usable, and the hunter was told — on the sweep's authority and in this session's own briefing to it — not to use them. Its lessons_applied records rebuilding a base rate it called 'n=1 clean' when n=6 was clean. impact_sum -2.30 was therefore formed under a false premise about its own baseline.
- NOT RESCORED AND NOT RE-HUNT. Re-running a name after seeing its first number is the selection this stage exists to avoid, nothing was traded (2.30 < 3.00), and an honest record is worth more to edge_postmortem.py than a tidier one. The row stands as measured, with this defect attached to it. Direction of the effect is not obvious: the true history (median abs 6.58%, 2 up of 6) and the hunter's substitute (two prints in a 9-16% band) point the same way in kind, and the hunter's stated reason for a small number was the 19% run-up and the 27% short base, not the base rate.
- ONE RESIDUAL QUESTION, much narrower than the contamination alleged: the company's own release put the Q1 FY2026 call on 2025-11-11 while the item-2.02 8-K was accepted 2025-11-12 at 17:06 ET. If the news was genuinely out on 11-11, that ONE move is measured a session late. Unresolved; cheap to settle from the 2025-11-11 release timestamp if anyone wants it.
- WHAT THIS IS AN INSTANCE OF. The adversary was removed on 2026-09-09 as measured-subtractive and the accepted cost was that nothing checks a finding for being factually wrong. Today a factually wrong claim entered the run through the SWEEP — upstream of where the adversary ever looked — and reached the hunter's sizing unchallenged. It surfaced only because this session re-checked EDGAR by hand after the key was written. Worth a line in edge/LESSONS.md if it recurs: the sweep's notes_on_baseline is asserted, unsourced against the feed it cites, and is currently trusted absolutely by the hunter brief.

## Edge hunt — 2026-09-17 — the 20 time-not-supplied rows, checked
- Logged at 2026-09-17 19:23 UTC
- Run on the operator's instruction after the main run published: confirm the dropped time-not-supplied rows from company sources and hunt whatever confirms, without scaling back for the market close. One extra edge-sweep agent over all 20 rows; output at research/2026/09/2026-09-17/edge/sweep-unknown.json. Universe rebuilt with --include-unknown into the scratchpad only — the sealed universe.json was NOT modified.
- RESULT: 0 of 20 confirmed in-window. 20 of 20 phantom or out-of-session. NO HUNTER WAS LAUNCHED, because there was nothing to launch one on. Total stage spend 3 of the 20-subagent cap (2 sweeps + 1 hunter).
- The refutations are specific, not a failure to search. Already reported: CMMB 2026-08-19 (6-K, Q2/1H), ALAR 2026-09-02. Weeks away: NB is an October event on an item-2.02 cadence of 2025-10-14 / 2026-01-12; TRT's fiscal-year prints land ~09-23 and its 2026-08-19 8-K was items 3.01/8.01, a listing matter. No event at all: HUBG is mid-restatement, its Nasdaq exception to file the FY2025 10-K and the 2026 Q1/Q2 10-Qs expired 2026-09-14, it expects a delisting determination and its lender deadline runs to 2026-11-30 — the calendar row is a vendor slot for a quarter the company cannot report. Out on session: DAVA, YRD and IH release pre-US-open, so a 09-17 row is bmo and already past. Prior-year relabels: HTLM's 1H 2025 release was 2025-09-17 (date off the URL path) and it has since moved to quarterly; IH's lead traces to 2025-09-18. The remaining ten are sub-$40m names with no discoverable IR schedule, where the row is a filing-deadline projection.
- PHANTOM RATE ON time-not-supplied ROWS IS NOW MEASURED AT 20 OF 20. Prior data points: 8 of 8 on the 2026-08-31 first run (which passed --include-unknown), 0 of 10 on the second run (which withheld it). Three runs agree the flag buys phantoms. Today it would have spent up to 17 Opus/high hunters establishing that no event existed — the exact failure the sweep exists to prevent, prevented here for one agent. The standing rule to withhold --include-unknown is upheld and should stay.
- Two rows are worth a cheap EDGAR watch rather than a hunt, because the print is genuinely missing rather than imaginary: VFS (Q2 2026 outstanding since the 2026-07-29 6-K said timing would be announced later, no announcement since, but it releases bmo and has always pre-announced) and HTLM (1H 2026 missing, prior-year analogue landed 09-17, no company source and no call to settle a session).
- NOTHING ABOUT THE DAY'S RANKING CHANGED. No name was added, no baseline was sealed, edge-scores.json is untouched and UPXI remains the only scored row at impact_sum -2.30, below the 3.0 floor. The book stays empty and the account stays flat. The market close was never the binding constraint here — the absence of confirmable events was.

## Edge hunt — 2026-09-17 — TRT added, day rescored, BOOK PLACED
- Logged at 2026-09-17 20:01 UTC
- The operator pushed back on the 0-of-20 result and was right. The day's second sweep refuted TRT on an INCOMPLETE FILING HISTORY: it claimed TRT's fiscal-year prints 'historically land ~09-23', citing 2022-09-23 and 2024-09-23, and missed the most relevant precedent — TRT filed its FY2025 item-2.02 8-K AND its 10-K on 2025-09-19, a Friday, one day off the 2026-09-18 calendar row. Verified directly at https://data.sec.gov/submissions/CIK0000732026.json: the FY print lands mid-to-late September every year for twenty years (09-19, 09-23, 09-27, 09-23, 10-05, 09-24, 09-24, 09-26, 09-21...), no item-2.02 since 2026-05-14, 10-K deadline ~09-28, baseline verdict fits_cadence at 127 days against a 90-day cadence.
- TRT baseline SEALED AND COMMITTED at 7ab1ed5 BEFORE the hunter launched — the never-degrade rule was honoured for the late addition. Baseline is clean: its six history dates match EDGAR's six most recent item-2.02 acceptances exactly. spot $11.28, turnover $1.63m/day, NO OPTIONS MARKET so expected_move is a historical median, run_up_20d -0.35%. Move distribution +30.54 / +2.12 / +3.37 / +0.55 / -6.23 / -1.13.
- RESCORED: 2 of 2 rankable, 1 of 2 clears the 3.0 floor. TRT impact_sum +5.10 conviction 5.10 FLOOR YES; UPXI -2.30 conviction 2.30 below. Control -run_up_20d_pct: TRT +0.35, UPXI -19.32 — the free control orders the day the same way the hunt does, which on two names means nothing but is recorded.
- BOOK PLACED. plan/open --submit --no-flatten at 19:58 UTC with 2 minutes to the close. TRT LONG 338 shares @ $11.259171, $3,799 notional = 33.0% of equity, 0.23% of ADV, filled. Execution cost 0.229% against the mid at submission, inside a measured half-spread of 14.577% — that spread is the number to remember about this name. UPXI refused: below the conviction floor (2.30 < 3.00), and separately not lendable at Alpaca so the short was unavailable anyway. Account after: equity $11,521.35, cash $7,722.23, 1 position. Exit date 2026-09-18.
- THE ROW IS A FLOOR-CLEARER I DO NOT RECOMMEND, and the note says so at length. edge_score flagged it: hunter's expected_move_pct (+2.00) is UNDER HALF the sum of its findings (+5.10) — its own caveats did not reach the sum. The hunter's conviction_note is explicit that +5.1 becomes +2.0 through a ~0.45 probability that the print lands in the window at all (TRT has NEVER pre-announced an earnings date in its EDGAR history; aggregators split 09-18 vs 09-21; 09-18 would be the earliest FY print in nine years) and a 15% sell-the-news haircut after a +12.46% five-day run. Neither haircut can reach impact_sum by construction. Second flag: bar UNSOURCED — no analyst estimate exists for TRT at all, no guidance, no options — so the sizes should have been capped and were not.
- The 09-15 Form 25 / 8-A12B / CERT lead resolved OPPOSITE to how it reads: not a delisting but the mechanical follow-through of a VOLUNTARY UPGRADE from NYSE American to the Nasdaq Global Market, disclosed 2026-08-19, last day on NYSE MKT 09-15, first on Nasdaq 09-16. A month old and priced. No finding taken. Also resolved: the +30.54% on 2026-05-14 was FQ3 revenue $16.5m +124% YoY on AI-GPU and EV burn-in demand reported alongside an $81k OPERATING LOSS — this shareholder base pays for the revenue headline and ignores the P&L. But it paid only +0.55% for the FISCAL-YEAR print on 2025-09-19, and a year-end is what lands tomorrow.
- LESSONS DELTA, both directions: UPXI pre-file -3.5 -> -2.3 (delta 1.2, shrank it); TRT pre-file +3.0 -> +5.1 (delta 2.1, GREW it, pushing a name from just above the floor to well above it and into the book). That is the direction worth watching in spearman_pre_lessons as days pool.
- THIRD BAD AGENT CALL OF THE DAY, and they belong together rather than as three accidents: (1) sweep 1 asserted UPXI's baseline history was contaminated when it was clean; (2) sweep 2 refuted TRT on an incomplete filing history and cost the day its only tradeable name until a hand check recovered it; (3) sweep 2's ZONE reasoning was thin even where the conclusion held. Nothing in the stage checks a sweep's assertions — the adversary never looked there — and all three surfaced only by hand. Candidate for edge/LESSONS.md: a sweep's notes_on_baseline and its refutations are asserted, unsourced against the feeds they cite, and are currently trusted absolutely.
- PHANTOM RATE CORRECTED TO 19 of 20 for this window, not the 20 of 20 the earlier entry claimed. The other six 09-18 rows were re-verified by hand against EDGAR and all hold: NB no item-2.02 since 2026-01-12 (overdue or October); ZONE fiscal year ends JUNE and last year's FY print was 2025-08-22, with no item-2.02 at all in 2026; CELU last 2.02 2025-05-09 and filed an NT 10-Q on 2026-08-14; ENLV December year end so H1 was an August event; HTLM has no 1H/Q2 2026 results and is running an F-1 plus FWP follow-on; LNAI has no 2.02 or 6-K in its recent history. The rule to withhold --include-unknown still holds on cost — 19 hunters to find 1 name — but IT IS NOT COSTLESS and today it cost the only name in the book.

## Edge hunt — 2026-09-17 — time-not-supplied rows checked
- Logged at 2026-09-17 19:47 UTC
- 20 of 22 calendar rows were dropped as time-not-supplied, leaving one name (UPXI). New edge/scripts/session_resolve.py checks those rows against EDGAR submissions and Nasdaq's press-release feed, no agent. Result for this window: 2 provably already reported (HUBG 8-K item 2.02 of 09-15, VFS 6-K of 09-11), 0 with a company press release announcing a date in the window, 18 with no evidence either way. No name bought back. Validated against the 12 labelled rows of 2026-08-31: the announced test kept 4 of 4 real reporters (SAIC, SY, LX, BLRX) and none of the 8 phantoms; the filing-cadence prior separated nothing. Report at research/2026/09/2026-09-17/edge/session-resolve.json.
- CORRECTED AGAINST THE 20:01 ENTRY ABOVE, which landed on main while this was being written. The phantom rate for this window is 19 of 20, not 20 of 20: TRT was real, was hunted, cleared the floor at +5.10 and was traded. So `no name bought back` above is the press-release channel's result, not the day's.
- THE TWO METHODS AGREE ON TRT AND THE SCRIPT GOT THERE WITHOUT AN AGENT. session_resolve.py returned TRT `unresolved / prior: fits` on last item-2.02 2026-05-14, 126 days — the same evidence the hand check used to overturn sweep 2 (which cited 127 days). It also returned `announces_dates: false`, so TRT's missing press release is not evidence against it, which is why the absent-announcement kill is gated on that flag.
- WHAT THIS COSTS THE `announced` TEST. High precision, low recall: 4 of 4 real reporters on 2026-08-31 and 0 of 8 phantoms, but 0 of 1 today, because TRT has never pre-announced an earnings date in its EDGAR history. `--announced-only` would have dropped the day's only tradeable name. It is for a day with more names than hunters, never for a thin one, and the cadence prior is to be read rather than filtered on.
