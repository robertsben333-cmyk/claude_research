# Run log — 2026-11-30

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-27 14:37 UTC
- Fired 14:36 UTC 2026-11-27 (Fri). Sealing for event date 2026-11-30 (Mon). RUN=research/2026/11/2026-11-30/europe. Plan: universe (cap 20), seal, one hunter per name, score, 4-judge panel, note, IBKR handoff. Local main was a stale pre-force-push copy; reset to origin/main (clean tree).

## Stage EU — IBKR
- Logged at 2026-11-27 14:37 UTC
- mode: would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is 'live' (expected here: no broker env in the cloud session; the executor server trades)

## Stage EU — universe and baselines
- Logged at 2026-11-27 14:39 UTC
- 28 scheduled, 5 eligible above $100k, all 5 hunted (under cap): uk 2 (EAH, POLR), no 2 (CAPT, NORSE), se 1 (SIVE). Largest market uk 40%. bankier.pl 403 (PL issuer calendar unavailable). Registers read: no, se, uk. anchor_covered: POLR, SIVE. Session: SIVE amc; CAPT and POLR session_unresolved (bmo?).

## Stage EU — hunts launched
- Logged at 2026-11-27 14:40 UTC
- One wave of 5: EAH, POLR (unpriced-hunter-uk); CAPT, NORSE (nordic/no); SIVE (nordic/se).

## Stage EU — hunts banked (1)
- Logged at 2026-11-27 14:41 UTC
- POLR back: phantom as a results event (interims RNS 2026-11-24 07:00; 11-30 is an RNS Reach investor webinar at 11:00 London). event_confirmed false, impact_sum 0. Running: EAH CAPT NORSE SIVE.

## Stage EU — hunts banked (2)
- Logged at 2026-11-27 14:43 UTC
- NORSE back: solvency event, not an ordinary print. Operating subsidiary filed bankruptcy 27 Nov 13:00 UTC, all 12 leases terminated, Recovery Box, ~0.011 NOK after -95%/20d. Q3 still calendared bmo 30 Nov, may be postponed. impact_sum -13.0, abs_move 45, p_up 33. Running: EAH CAPT SIVE.

## Stage EU — hunts banked (3)
- Logged at 2026-11-27 14:45 UTC
- EAH back: real interims 30 Nov (date per 6 Nov RNS; 07:00 by convention). H1 pre-released 6 Nov (-12.1%). impact_sum -0.6, abs_move 5.0, p_up 50. Running: CAPT SIVE.

## Stage EU — hunts banked (4)
- Logged at 2026-11-27 14:45 UTC
- SIVE back: real Q3, amc (~18:00 CET 30 Nov per issuer's 20 Nov release, moved from 26 Nov). Window close(11-30)->close(12-01). impact_sum +0.8, abs_move 13, p_up 48 (scaled -0.52, sign disagrees). Running: CAPT.

## Stage EU — hunts
- Logged at 2026-11-27 14:46 UTC
- 5/5 hunted. CAPT back: real Q3 bmo (07:30 CET pattern; 23 Nov notice sets 30 Nov), impact_sum +0.6, abs_move 5.0, p_up 56. POLR phantom (webinar of 24 Nov interims). SIVE amc.

## Stage EU — panel STARTED
- Logged at 2026-11-27 14:46 UTC
- 4 packs (SIVE, CAPT, EAH, NORSE), four judges

## Stage EU — panel
- Logged at 2026-11-27 14:49 UTC
- 4/4 judges, no fallback. Selected: NORSE short, panel_pct 100, 4/4. Not selected: CAPT 68 long (1/4), EAH 49 long, SIVE 28 long (sd 68, fable51 short).
