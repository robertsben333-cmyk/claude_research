# Run log — 2026-09-08

## Stage 0 — universe (07:17 CEST / 05:17 UTC)
- Logged at 2026-09-08 05:17 UTC
- Window: After the US close on Tuesday 08 September 2026 through before the US open on Wednesday 09 September 2026
- Source: nasdaq (after-close and before-open both single-source, clean fetch, exit 0)
- Universe: 24 total (7 AMC, 17 BMO); 15 above the $500,000,000 market-cap floor; 15 eligible after qualification
- Excluded: 9, all below_market_cap_floor (CAL $0.41B, JILL $0.29B, PPIH $0.22B, OCC $0.12B, NNOX $0.06B, MIND $0.04B, DXLG $0.03B, YQ $0.03B, CRMT $0.02B)
- Notes: session timing (BMO/AMC) single-sourced from nasdaq, no cross-source conflicts to check. Options-market qualification verified via WebSearch for the four recent listings among the 15 eligible (SUNB, JMKE, TTAN, SAIL) — all confirmed to have live options chains; the remaining 11 (CASY, CHWY, CNM, KFY, BRZE, SIG, ASO, INNV, AVO, ODD, CGNT) are established long-listed names treated as eligible by inspection, consistent with prior practice. No OTC, SPAC-remnant, or duplicate-share-class names in the above-floor set. Eligible count (15) exceeds triage.skip_if_universe_at_or_below (10), so stage 1 will run normally today.

## Stage 1 — triage (run by stage 2 session, stage 1 Routine had not published)
- Logged at 2026-09-08 08:26 UTC
- Mode: scouted
- Reason: 01-shortlist.json did not exist by 08:23 UTC / 10:23 CEST, ~2h past the 08:38 CEST slot; ran earnings-triage myself per the deep-dive skill's guidance rather than lose the day
- Funnel: 24 universe -> 15 eligible -> 11 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium), single 15-ticker batch
- Session mix: 2 AMC / 4 BMO (TTAN, BRZE amc; CHWY, SAIL, ASO, SIG bmo)
- Notable drops: JMKE (ai_edge 25<30, brand-new IPO no history), KFY (change_expectation 30<35, slow grinder), ODD & CGNT (tradeable:false, thin sub-$1B ADRs with doubtful options depth)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-08 08:27 UTC
- Shortlist: 6 names (TTAN, BRZE, CHWY, SAIL, ASO, SIG); this batch (1 of 2): TTAN, BRZE, CHWY
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers, publish after each wave -- wave 1: TTAN, BRZE; wave 2: CHWY

## Stage 2 — deep dive, batch 1 — FINISHED
- Logged at 2026-09-08 09:01 UTC
- Researched: TTAN, BRZE, CHWY
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (wave 1: TTAN, BRZE; wave 2: CHWY)
- Median evidence completeness: 84/100
- Notes: TTAN dossier corrects triage's EPS/analyst-count read (GAAP -$0.09 vs non-GAAP consensus $0.35; 15-18 analysts, not 5). CHWY dossier corrects triage's premise that Chewy 'missed EPS badly last print' -- Q1 was a +0.51% surprise, the selloff was a guidance cut. This is batch 1 of 2 -- ranking (02-ranking.json) deferred to batch 2 after SAIL, ASO, SIG are researched.

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-08 10:23 UTC
- Shortlist: 6 names (TTAN, BRZE, CHWY, SAIL, ASO, SIG); this batch (2 of 2): SAIL, ASO, SIG
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers, publish after each wave -- wave 1: SAIL, ASO; wave 2: SIG

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-08 10:59 UTC
- Researched: SAIL, ASO, SIG
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves (wave 1: SAIL, ASO; wave 2: SIG)
- Median evidence completeness: 82/100 (SAIL 84, ASO 82, SIG 80)
- Corrections to triage vs primary sources: SAIL is 20-25 analysts not 5; ASO is 12-19 analysts not 4; SIG is 11 analysts / 12 ratings not 3 -- triage's coverage counts were wrong on all three names this batch, so the 'thin coverage' rationale in selection_rationale does not hold for any of them
- Panel-eligible after this batch (full 6-name shortlist ranked): TTAN (54.65), CHWY (48.6), SAIL (48.5), BRZE (47.75), SIG (47.1), ASO (45.1) -- all 6 pass the exclusion floors (confirmed, evidence>=50, implied-move anchor); panel.names=2 selects TTAN and CHWY for stage 3

## Stage E — edge hunt — STARTED
- Logged at 2026-09-08 14:10 UTC
- Window: 2026-09-08 amc + 2026-09-09 bmo. edge_universe.py --window resolved 24 of 73 calendar rows, 0 time-not-supplied (no --include-unknown).
- Universe: CASY,SUNB,SAIL,CHWY,TTAN,CNM,JMKE,KFY,BRZE,SIG,ASO,INNV,AVO,ODD,CGNT,CAL,JILL,PPIH,OCC,NNOX,MIND,DXLG,YQ,CRMT
- Baselines sealed and pushed BEFORE any agent launch (commit 89072b4). 23 of 24 ok; JMKE no baseline (only 28 usable bars, recent listing).
- Option chains live on 12 of 24 (10:07 NY fire time worked): usable event-implied move on 9 — BRZE 15.0%, CASY 7.6%, CHWY 10.2%, CNM 9.2%, ODD 20.7%, SAIL 13.0%, SIG 10.1%, SUNB 9.8%, TTAN 10.1%. Tightest ATM spreads TTAN 0.17, SAIL 0.17, BRZE 0.20, CHWY 0.25 of mid.
- Baseline event_plausibility: 19 fits_cadence; unknown x4 (CGNT, NNOX, ODD cadence_implausible — Israeli FPI 6-K guard; SUNB only 2 prior prints); suspect x1 (YQ, 5-day gap vs 78-day median). History untrustworthy as an earnings base rate for those five — hunters will be told.
- Plan: 1 edge-sweep over all 24 -> shed to ~8 hunted names (budget cap 20 = 1 sweep + 10 hunters + 8 adversaries = 19) -> 2 isolated hunters on top-2 by hunt_priority, 1 on the rest -> 1 priced-in-adversary per ticker over all its findings, both sides -> edge_score.py -> edge-note.md.
- Shed will follow budget.edge_degrade_order (unconfirmed first, then lowest hunt_priority), with the documented deviation of preferring names that have a live chain so 'what the market priced' is measured rather than inferred.

## Stage E — sweep, amendment pass and shed
- Logged at 2026-09-08 14:25 UTC
- Sweep (1 agent, all 24 names): 23 event_confirmed, 0 phantom, 1 unconfirmed (CRMT), 2 session_unsettled (OCC, CRMT). Phantom rate zero for the second run in a row without --include-unknown.
- CRMT killed correctly: Car-Mart pre-announces every print 7-14 days ahead and no such release exists for Q1 FY2027; vendors split across 2026-09-09 bmo, 2026-09-09 amc and 2026-09-17.
- CAL's date MOVED — company PR of 2026-09-01 pulled Q2 forward from 2026-09-10 to 2026-09-09 bmo; syndicated copies still carry 09-10. Recorded because the resolver measures the session we name.
- OCC session unsettled: company release names the date and an 11:00 ET call but no release hour, and the 2026-06-08 print's timestamp was unsourceable.
- Baseline amendment pass (edge_baseline_amend.py, rewritten from THIS run's sweep — the shipped table was 2026-09-07's WDH entry and exited non-zero as designed). Two upgrades, one downgrade: YQ suspect->unknown, SUNB unknown->fits_cadence, CRMT fits_cadence->suspect.
- YQ is the amendment that mattered: a suspect verdict sets rankable=false and multiplies baseline_quality by 0.05, so a company-confirmed event (GlobeNewswire 2026-09-02, amc 2026-09-08, 9pm ET call) would have been arithmetically unrankable. Its 5-day 'cadence' is the 2026-09-03 US$10m buyback 6-K, which is also what the +42.5% 20-day run-up is. Held at unknown not fits_cadence because the history is untrustworthy for the same reason.
- NOT amended, deliberately: ODD, NNOX, CGNT stay unknown. All three are Israeli FPIs whose cadence_implausible flag comes from the 6-K text matcher catching non-earnings filings; upgrading would forgive a history defect and hand a 1.0 event multiplier. Per the CAN/DLNG/GMHS precedent.
- Known cosmetic residue: edge_baseline_amend.py updates event_plausibility.verdict but not the mirror copy in baseline_quality.event_plausibility. edge_score.py reads the former, so scoring is correct; the stale mirror is not a scoring path.
- SHED to 8 hunted names (cap 20 = 1 sweep + 10 hunters + 8 adversaries = 19). Dropped 16.
- Shed step 1 (drop_unconfirmed_names_first): CRMT (priority 12.7).
- Dropped despite priority 79.4: JMKE. priced_in.py produced no baseline at all — 28 usable bars, no options, no reaction history, because Jersey Mike's IPO'd in 2026. The event IS company-confirmed for 2026-09-09 bmo, but 'is this already priced' is unanswerable with no priced-in measurement, so it is a visible loss rather than a hunter spent against a baseline that does not exist.
- Shed step 2 (drop_lowest_hunt_priority_names), with the documented chain deviation: took the top 4 by hunt_priority unconditionally (YQ 86.5, ODD 76.2, NNOX 71.8, INNV 69.3), then filled the remaining 4 slots with the highest-priority names carrying a usable event-implied move (SUNB 67.1, SIG 47.6, TTAN 45.3, CNM 43.9).
- Reason for the deviation: a straight top-8 by priority would have been YQ, ODD, NNOX, INNV, SUNB, AVO, MIND, CGNT — only 2 of 8 with a measured chain, reproducing the 2026-08-31 weakness where 7 of 10 names had priced_lean_pct inferred from a run-up. The chosen 8 carry 5 measured chains (ODD 20.7%, SIG 10.1%, TTAN 10.1%, SUNB 9.8%, CNM 9.2% event-implied).
- Not hunted, by priority: JMKE 79.4 (no baseline), AVO 66.9, MIND 65.4, CGNT 63.7, DXLG 61.2, PPIH 59.6, OCC 57.3, CAL 54.8, JILL 52.1, KFY 49.7, SAIL 42.4, ASO 40.8, BRZE 38.2, CHWY 29.6, CASY 21.4, CRMT 12.7. All sit in edge-scores.json as rankable=false.
- Double hunt on the top 2 of the kept set: YQ and ODD, two isolated hunters each. Not economised at any budget.
- Wave plan: W1 = YQ-a, YQ-b, INNV, TTAN (the three amc names report tonight after the 20:00 UTC close, so they go first and their adversaries must land before it). W2 = ODD-a, ODD-b, NNOX, SUNB. W3 = SIG, CNM.
