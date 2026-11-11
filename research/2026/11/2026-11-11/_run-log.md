# Run log — 2026-11-11

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-10 14:38 UTC
- Fired 2026-11-10 ~14:36 UTC (15:36 Amsterdam, markets open). Sealing for event date 2026-11-11 (Wed; next European session). Plan: universe -> baselines -> provenance -> hunters in waves of 5 -> edge_score -> four-judge panel -> note -> IBKR handoff file.
- Checkout note: local main had diverged from a force-updated origin/main; old local main kept as branch local-main-pre-forcepush-20261110 (not pushed), work is on a fresh main tracking origin/main.

## Stage EU — IBKR
- Logged at 2026-11-10 14:38 UTC
- would refuse: execution_eu.enabled is false (mode only; no broker call from this session)

## Stage EU — universe and baselines
- Logged at 2026-11-10 14:48 UTC
- 71 scheduled, 40 eligible above $100k, 20 drawn (random, seed eu-2026-11-11): de 7, se 3, dk 3, it 3, uk 2, no 1, es 1, fr 0, fi 0, pl 0 (Warsaw shut: exchange holiday). Largest market de at 35%.
- 20 baselines sealed at ~14:46-14:47 UTC (intraday spots, not closes). Provenance stamped: uk.v7, de.v7, nordic.v5, it.v5, es.v5, all claude-opus-5-5 (alias timeline). Hunters: 4 waves of 5.

## Stage EU — hunts in progress
- Logged at 2026-11-10 14:50 UTC
- Waves overlapped on purpose: the handoff has to reach main before the 17:30 CET close for the executor to buy, so names are launched as subagent slots free (session cap 8 concurrent) rather than strictly 5 at a time. Running: ADN1 ALZCUR BEAMMW_B BNR CRE DFDS DIGIS EIN. Queued: FNM FNTN GYC ICG KWS OKEA PRT PST RBREW RWAY V1NC VWS.

## Stage EU — panel STARTED
- Logged at 2026-11-10 15:12 UTC
- 19 rankable names scored (OKEA not ranked: hunter found no event; Q3 was out 2026-11-03). Four judges launched.

## Stage EU — ranking
- Logged at 2026-11-10 15:20 UTC
- 19 ranked, OKEA phantom (Q3 out 2026-11-03). No name above the 2.8 floor; top FNM +1.90, bottom V1NC/PRT -1.40. Panel (4 of 4 members, no fallback) selects FNM long (100) and EIN short (88). Session corrections from hunters: PRT, RBREW, PST release after the 11-11 close (PST on 12-11 morning); RWAY in-session.

## Stage EU — IBKR handoff
- Logged at 2026-11-10 15:20 UTC
- Handoff written (no broker call): 3 names at panel_pct >= 70 with four judges — SELL EIN (88.5), SELL V1NC (85.5), SELL PRT (78.6). FNM (100) not taken: turnover $0.12m below the $0.20m floor. execution_eu.enabled is false per mode at 0s. Note: PRT's hunter puts its release after the 11-11 close, so a short entered today holds no print until 12-11.

## Stage EU — published
- Logged at 2026-11-10 15:20 UTC
- All output pushed to main (EARNINGS_DATA_BRANCH=main); origin/main head eccc5d594 'stage EU: IBKR handoff for 2026-11-11' confirmed at 15:20 UTC.

## Close AMC (stage E amc exit) — 2026-11-11
- Logged at 2026-11-11 11:24 UTC
- Fired 11:17 UTC (06:17 ET, pre-market). Guard mode --require-exit-tif opg: exit 0 (amc_open, amc -> open as market DAY order). verify over research/*/*/*/edge: 14 exit legs, all ok, none UNFILLED, nothing still held. close --submit: no stage E leg due today or overdue, so no order sent and no refusal. Stage E's Routine is stopped since 2026-10-19; stage E-P's amc legs are not in this scan (that is stage E-PX's job, whose Routine is not yet created).
