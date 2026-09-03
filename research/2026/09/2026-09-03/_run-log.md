# Run log — 2026-09-03

## Stage 0 — universe — 07:22 CET
- Logged at 2026-09-03 05:22 UTC
- Window: After the US close on Thursday 03 September 2026 through before the US open on Friday 04 September 2026
- Source: nasdaq (after-close + before-open)
- Universe: 21 total (20 AMC, 1 BMO); 13 eligible after qualification
- Excluded: 8, all below_market_cap_floor ($500M floor) — none excluded for options/timing
- Notes: all 13 above-floor names hand-verified for a real listed options market and single-source-confirmed BMO/AMC session (Nasdaq option-chain listings + company IR press releases for IOT and OXM, cross-checked against TipRanks/StockTitan/Investing.com). No conflicting timing found. Stage 1 (triage) will trigger: 13 eligible > skip_if_universe_at_or_below (10).

## Stage 1 — triage — STARTED
- Logged at 2026-09-03 06:42 UTC
- 13 eligible names, above skip threshold (10); spawning 1 earnings-triage-scout batch (all 13 fit in one batch of 15) to score change_expectation/ai_edge before cutting to shortlist_size=6.

## Stage 1 — triage (06:44 UTC)
- Logged at 2026-09-03 06:45 UTC
- Mode: scouted
- Funnel: 21 universe -> 13 eligible -> 11 cleared timing/tradeability -> 11 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium), all 13 eligible tickers in one batch
- Session mix: 6 AMC / 0 BMO (all 13 eligible names in today's universe report AMC; no BMO name cleared the market-cap floor)
- Notable drops: MAMA (tradeable: false, illiquid options), SWBI (timing_confirmed: false, one source says 09-04 not 09-03 -- would have ranked top-3 on score, worth a manual re-check before stage 2), DOCU (ranked 8th, already ran +17% into print), ASAN (ranked 7th, closest miss)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-03 08:26 UTC
- Shortlist: 6 names (PATH, PL, AMBA, LULU, ZS, IOT); this batch: PATH, PL, AMBA (positions 1-3 of 6, cap unchanged)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (PATH+PL, then AMBA), publish after each dossier and after each wave

## Stage 2 — deep dive, batch 1 — wave 1 done
- Logged at 2026-09-03 08:47 UTC
- Researched: PATH, PL
- Both event_confirmed; PATH triage rationale corrected (magnitude framing inverted, real catalyst is 09-22 Investor Day); PL triage rationale corrected (not a guidance-validation print, it's about ATM dilution/backlog)

## Stage 2 — deep dive, batch 1 — FINISHED
- Logged at 2026-09-03 09:05 UTC
- Researched: PATH, PL, AMBA
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (PATH+PL, then AMBA), published individually and after each wave
- Median evidence completeness: 84/100 (PATH 84, PL 87, AMBA 82)
- Notable: PATH and PL triage rationales both corrected on further evidence (see wave-1 log entry); AMBA's implied move (12.93%) reads as cheap vs its own 8Q realised-move mean (15.08%), opposite of triage's framing
- Panel-eligible after this batch: n/a — final ranking happens after batch 2

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-03 10:25 UTC
- Shortlist: 6 names (PATH, PL, AMBA, LULU, ZS, IOT); this batch: LULU, ZS, IOT (positions 4-6 of 6, cap unchanged)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (LULU+ZS, then IOT), publish after each dossier and after each wave

## Stage 2 — deep dive, batch 2 — wave 1 done
- Logged at 2026-09-03 10:40 UTC
- Researched: LULU, ZS
- Both event_confirmed; LULU evidence completeness 84 (no IV rank/skew found); ZS evidence completeness 80 (implied move figure six sessions stale, no IV rank found)

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-03 10:59 UTC
- Researched: LULU, ZS, IOT
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (LULU+ZS, then IOT), published individually and after each wave
- Median evidence completeness: 84/100 (LULU 84, ZS 80, IOT 84)
- Panel-eligible after this batch: PATH, PL, LULU, AMBA, IOT, ZS (all 6, rank order) -- panel.names=2 in config so stage 3 takes PATH and PL

## Edge hunt — 2026-09-03 amc + 2026-09-04 bmo — STARTED
- Logged at 2026-09-03 14:10 UTC
- Stage E. Universe: 21 of 68 calendar rows resolved to today's amc (20) plus next-day bmo (1: KNOP). No --include-unknown. Baselines sealed at 14:08 UTC for all 21 — every one returned event_plausibility ok, and 12 of 21 carry a live front-expiry option chain (ZS 13.15%, PL 18.23%, ASAN 18.20%, AMBA 14.44%, NX 14.23%, PATH 13.70%, SWBI 13.61%, GWRE 12.96%, IOT 11.27%, MAMA 11.55%, DOCU 10.62%, LULU 9.42% implied). The 16:04 Amsterdam firing did its job: ZS ATM spread is 9% of mid against 41% on the first run's weekend marks. Budget plan at the edge_hunt cap of 20: 1 sweep + 10 hunters (8 names, double-hunted top 2) + 8 adversaries = 19. 21 names does not fit, so the shed is planned now, not discovered later: shed per budget.edge_degrade_order — unconfirmed names first, then lowest hunt_priority — while deliberately keeping names with a live chain, so 'what the market priced' is measured rather than inferred from a run-up. Shed names sit in the table as rankable:false with a stated reason.

## Edge hunt — 2026-09-03 — sweep done, hunt set fixed
- Logged at 2026-09-03 14:25 UTC
- Sweep: 21 of 21 events CONFIRMED, ZERO phantom calendar rows — 20 from a company source (IR release, GlobeNewswire/BusinessWire/PRNewswire, or the company's own site), 1 (LND/BrasilAgro) press-corroborated only because ri.brasil-agro.com served an unpopulated template and no pre-announcing 6-K was found. 2 sessions unsettled: LND (no release hour recoverable) and GROW (company gave only 'prior to the webcast', webcast 09-04 08:30 ET, so the release could land amc 09-03 or bmo 09-04; prior five 8-K item 2.02 filings were all amc). NX is a third session wrinkle worth recording: release is amc 09-03 but the call is intraday 09-04 11:00 ET, so the reaction can split across two sessions. BUDGET SHED. 21 names against the edge_hunt cap of 20 subagents. Nothing to shed under edge_degrade_order step 1 (drop_unconfirmed_names_first) because the sweep confirmed all 21, so the shed ran entirely on step 2 (drop_lowest_hunt_priority_names): 8 names hunted, 13 shed. Shed names are NOT dropped from the output — edge_score.py scores every ticker in baselines/, so all 13 appear in the table as rankable:false / not_rankable_because 'no hunt', which is the visible loss the skill prefers over keeping a name and measuring it worse. Hunted: SWBI 78, AMBA 72, PL 69, DOMO 66, ASAN 63, MAMA 61, LULU 57, NX 56. Shed: CURV 59, BBCP 54, AOUT 52, PATH 51, GWRE 49, LND 47, OXM 45, ZS 43, EGAN 41, IOT 39, DOCU 36, KNOP 31, GROW 21. ONE DELIBERATE DEVIATION from the sweep's ordering: NX (56, live chain) swapped in for CURV (59, no chain). Three priority points traded for a measured baseline instead of one inferred from a 20-day run-up, per the skill's stated judgement call to keep names with a live option chain. That leaves 7 of 8 hunted names with a live two-sided chain, against 3 of 10 on 2026-08-31. I did NOT override the sweep a second time on GWRE (49) despite the most striking tape on the day (+26.3% over 20 days into a fiscal-year-end print, still -22.7% off the 52w high, puts bid at +3.44 skew) — the sweep is the designated priority authority and a second override on my own read of what looks interesting is the contamination the stage forbids. NO BASELINE AMENDMENT, deliberately. edge_baseline_amend.py correctly refused to run: its amendments table is still 2026-08-31's (AMBR/GOLD/MEI/WLYB) and it exits non-zero rather than reporting 'nothing to amend'. On the merits there was nothing to amend anyway: no baseline returned 'suspect', so nothing is gated out of ranking by the suspect rule, and no baseline denies its event. Four carry cadence_implausible (KNOP 14d, LND 15d, MAMA 56d, AOUT 69d) and GWRE has no recoverable cadence, but all five already sit at 'unknown' (event_q 0.6) rather than 'suspect' (0.05). Of those, only MAMA is in the hunted set, and upgrading it to fits_cadence would raise its quality multiplier from 0.6 to 1.0 while the defect it rests on is in the reaction HISTORY, not the event flag — MAMA's event is company-confirmed with an explicit hour, but its 8 recorded 'prints' at a 56-day cadence are contaminated by non-earnings 8-Ks, so 'unknown' is nearer the truth than 'fits_cadence' would be. An amend pass here would have moved exactly one hunted name, upward, which is the asymmetric tuning the skill forbids. Recorded instead as an explicit warning to the MAMA and DOMO hunters. CONCURRENCY: waves of 5 rather than the configured 4. Every hunted name is amc tonight (release 20:00 UTC, ~5.5h out) and the skill sanctions exceeding the concurrency guideline for amc names so their adversaries land before the release. Total spend stays inside the cap: 1 sweep + 10 hunters + up to 8 adversaries = 19 of 20.

## Edge hunt — 2026-09-03 — COMPLETE
- Logged at 2026-09-03 14:58 UTC
- Spend 19 of 20: 1 sweep + 10 hunters + 8 adversaries. Sweep confirmed 21 of 21 events, ZERO phantom rows (20 company-sourced, LND press-corroborated only). 8 names hunted, 13 shed on hunt_priority and left in the table as rankable:false/'no hunt'. RANKING (8 rankable, 8 distinct scores, strict order): SWBI +20.8, ASAN +12.3, MAMA +10.9, AMBA +0.1, DOMO -7.1, LULU -7.2, NX -23.3, PL -32.5. edge_pct spans +1.05 to -1.68 points of spot (2.73 points, against 0.62 on 2026-08-31). Adversary judged ALL 33 findings on both sides; edge_brief.py --check reports JOIN CLEAN, no orphans, no nulls, no silent drops. Mean priced_in 65.7, median 64.0, range 42-90 -- nothing survived below 42% priced, which is why the table compresses. THE TWO-HUNTER SPLIT PAID OFF AGAIN, and differently on each name: AMBA's two hunters returned +2.0 and -4.0 from the same sealed baseline and the same 10-Q, reading the same fact (the -20% drawdown is a round-trip of the 31 July NXP takeover-rumour spike) in opposite directions; dispersion 0.68, the highest of the eight, which flowed into uncertainty rather than a gate and landed AMBA at +0.1, mid-table. SWBI's two hunters instead CONVERGED to within 0.5 points (+5.0/+4.5) on the same primary NICS series, dispersion 0.38. Neither could see the other in either case. ADVERSARY BREAKS worth keeping: (1) PL#0's claim of 'no nine-figure booking, only two seven-figure deals' is factually wrong -- NGA exercised a 2M Luno B option year on 2026-06-04 inside the window, press-released; the adversary also noted backlog ROSE 900M->906M while the hunter cited only the RPO metric that fell. (2) SWBI's adversary conceded every one of the seven bullish facts and refused the inference using a fact neither hunter had: RGR flat at 38.20->38.32 while SWBI fell 11.7% over 08-19 to 09-03, making the de-rating idiosyncratic rather than sectoral -- a SWBI-specific negative no claim addresses. (3) SWBI-b#0 cites the Outdoor Wire /releases/2026/07/ path (the June release) as source for a July datapoint published only in the /2026/08/ release; substance survives, citation was wrong. (4) SWBI's adversary collapsed 8 claims from 2 hunters into 5 source clusters. SURVIVED BEST: MAMA#2 at 42% priced (94m raised for M&A on 2026-06-30, no 8-K 1.01/2.01 since, prior-year Crown I deal announced into this same slot) -- and the adversary sized it at +6.0 against the hunter's +3.5, the largest size disagreement of the run and with the adversary the MORE bullish party. MOST DISMISSED: ASAN#4 and PL#2 both at 90%, restatements of published guidance/targets. SIGN BALANCE 6 of 10 hunts positive, 4 negative (4 names positive, 3 negative, 1 split) -- this REVERSES 2026-08-31's six-of-eight negative, so neither day's skew is a pattern; recorded for pooling. MEASUREMENT QUALITY, stated precisely because the raw count misleads: 12 of 21 in the universe and 7 of 8 hunted names carry a quoted straddle, but only 3 of 8 (SWBI, ASAN, LULU) carry a 25-delta skew, so for FIVE of eight ranked names the agreement discount fired against a lean inferred from a 20-day run-up rather than measured. Better than 2026-08-31 (7 of 10 had no options at all) but '12 chains' overstates it. Chain quality inside the hunted set varies hugely and opt_q handles it: LULU 9.0% ATM spread / 34,908 OI / q_opt 0.85 down to NX 73.7% / 199 OI / q_opt 0.0 and AMBA 68.7% / q_opt 0.0. The 16:04 firing is why any skew exists -- ZS ATM spread 9% of mid against 41% on the first run's weekend marks. NO BASELINE AMENDMENT (reasoning in the prior log entry and the note); MAMA's hunter was warned instead and rebuilt the reaction history by hand, establishing 6 of 8 recorded dates are genuine prints and 2025-09-02 is the Crown I acquisition 8-K, not an earnings event. DOMO's hunter was warned its 18% median is pre-deal and correctly refused to inherit it for a 10-Q-only, no-call event. DEVIATIONS: NX (priority 56, live chain) hunted in place of CURV (59, no chain); GWRE (49) deliberately NOT overridden into the set despite the most striking tape of the day (+26.3% 20d into a fiscal-year-end print, puts bid, hist_n=0 from an EDGAR former-name artifact) because the sweep is the priority authority -- flagged as tomorrow's most obvious candidate to revisit. Concurrency ran at 5 and briefly 8 against a configured 4, sanctioned for amc names so no adversary landed after its 20:00 UTC event. THREE SESSION CAVEATS: LND and GROW session_unsettled (both shed, so out of the ranking); NX releases amc 09-03 but calls 09-04 11:00 ET, so its reaction splits across two sessions -- the scoring window captures both. ONE DAY IS AN ANECDOTE: eight names cannot produce a meaningful rank correlation and the note says so; the pooled edge_resolve figure is the result.

## Capture — 2026-09-03 — STARTED
- Logged at 2026-09-03 15:07 UTC
- Plan: universe sweep --horizon-days 15 script-only, then agent-layer nine-area search + capture.py --plan for the 6 largest names reporting within 3 days.

## Capture — 2026-09-03 — LULU tripwire investigated
- Logged at 2026-09-03 15:17 UTC
- Doc 9cce7dbac9...027d53 (marketbeat Q1 FY26 transcript, June 2025) tripped the tells regex because it names 'September 3, 2026' as the upcoming Q2 call date while separately discussing the PRIOR quarter beating expectations. Confirmed false positive per FINDINGS.md's known class (prior-quarter recap naming the next event date); document is legitimate pre-print content and stands.
