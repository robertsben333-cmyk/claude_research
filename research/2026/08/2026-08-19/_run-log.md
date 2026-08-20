# Run log — 2026-08-19

## Stage 0 — universe (07:16 CET)
- Window: After the US close on Wednesday 19 August 2026 through before the US open on Thursday 20 August 2026
- Source: nasdaq
- Universe: 36 total (12 AMC, 24 BMO); 22 eligible after qualification
- Excluded: 14 (13 below_market_cap_floor: TWIN, UFI, FLX, SLSN, ARAY, CCIF, JG, BOSC, EVAX, BEEM, HUIZ, YJ, KRKR; 1 no_options_market: AIIR — Air Global PLC, IPO'd on Nasdaq ~2026-05-21, no dedicated options-chain page found on Nasdaq/Barchart/Yahoo despite WebSearch, too recent a listing to have a real options market yet)
- Notes: get_earnings.py returned status ok on first attempt (exit 0), no fallback needed. All timing (BMO/AMC) came from a single source (nasdaq) with no cross-source conflicts to check; no company had an unknown session. Options-market qualification for the smaller/foreign-ADR names above the cap floor (ATAT, DAO, AIIR, RERE, DDL, IOND) was verified via WebSearch rather than assumed: ATAT, DAO (thin: put vol 3 / call vol 0), RERE, DDL, and IOND all confirmed optionable across Yahoo/Barchart/Webull/moomoo; AIIR was the only one with no evidence of a listed options market.

## Stage 1 — triage (11:12 CET)
- Mode: scouted (22 eligible > skip threshold of 10)
- Funnel: 36 universe -> 22 eligible -> 11 cleared floors -> 6 shortlisted
- Scouts: 2 subagents (sonnet/medium), batch 1 = 15 names, batch 2 = 7 names
- Session mix: 3 AMC / 3 BMO
- Notable drops: AEG (change_expectation 20, formality print), ATHM/SCSC/JBSS (below change_expectation floor, low-drama prints), LYTS (below ai_edge floor, too little public info despite large prior-year move), BULL/IOND/ATAT/DAO/RERE/DDL (marked not tradeable — thin US options liquidity on recent listings or China ADRs, despite BULL and IOND scoring well on change_expectation)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-08-19 08:22 UTC
- Tickers: WOLF, BABA, BILL
- Plan: 2 waves (wave 1: WOLF, BABA; wave 2: BILL), publish after each wave and after each dossier

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-08-19 10:23 UTC
- Batch 2 scope: BILL, HOV, COTY, FUTU
- Note: batch 1 (WOLF, BABA, BILL) completed WOLF and BABA but BILL was never researched (no failure log, no batch-1 close section) — covering it here since this is the last chance today; total for the day stays at the shortlist cap of 6.
- Plan: 2 waves of 2 opus/high researchers (wave 1: BILL, HOV; wave 2: COTY, FUTU), publish after each wave

## Stage 3 — panel & advice (18:09 CEST)
- Logged at 2026-08-19 16:09 UTC
- Panelled: WOLF
- Calls: WOLF Neutral / No Edge, unsigned band 7.7-24.6% (Med certainty, reversal risk High 68.9)
- Panel seats filled: 7/7
- Chair overrides: none
- Degradations: 02-ranking.json rebuilt by stage 3 (stage 2 batch 2 never wrote one, and never researched COTY/FUTU); panel.names reduced from config default 2 to 1 (next step of budget.degrade_order) because stage 2 shed scope with no closing log entry
- Anchor refresh: WOLF spot updated from stage-2's stale $31.46 to $27.91 (-11.3% intraday) after chair WebSearch could not resolve it cleanly but two independent personas did (stockanalysis.com)

## Stage 4 — calibration — DEFERRED
- Logged at 2026-08-20 06:25 UTC
- Attempted at 2026-08-20 06:25 UTC (08:25 CEST), on schedule.
- 04-advice.json exists (WOLF panelled Neutral/No Edge; BILL, BABA, HOV non-panelled). No 05-outcome.md.
- Cannot score yet: measurement convention is close-before-print to close-after-first-full-session-following. WOLF and BILL reported amc 2026-08-19, so the first full session following is today's (2026-08-20) regular session; BABA and HOV report bmo 2026-08-20, so their first full session is also today's session. All four need the 2026-08-20 close, and NYSE has not opened yet at this run time (opens 13:30 UTC, closes 20:00 UTC) -- confirmed via WebSearch (market status: pre-open).
- Not fabricating an intraday quote as a close. Deferring: the next stage-4 firing (2026-08-21 08:20 CEST) is the earliest time 2026-08-20's close is known, so it should pick this run up on the next attempt.
- Flag for schedule review: stage 4 at 08:20 'of yesterday' cannot generally close out a run whose window extends to a bmo print or an amc print the prior evening, because both resolve on the *current* day's close, which has not happened yet at 08:20. LEDGER.md still shows no runs scored as of this attempt.
- No LEDGER.md change made; no 05-outcome.md written.
