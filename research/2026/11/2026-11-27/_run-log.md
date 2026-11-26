# Run log — 2026-11-27

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-26 14:38 UTC
- Fired 14:36 UTC 2026-11-26 (Thu). Sealing for event date 2026-11-27 (Fri). RUN=research/2026/11/2026-11-27/europe. Plan: universe (cap 20), seal, one hunter per name, score, 4-judge panel, note, IBKR handoff. Local main was a stale pre-force-push copy (diverged 52/58); worked from a detached checkout of origin/main, local branch left untouched.

## Stage EU — IBKR
- Logged at 2026-11-26 14:38 UTC
- mode: auth tws, executor server trades; cloud has no broker env (expected). Last line: would refuse: IBKR_ENVIRONMENT None vs execution_eu.environment 'live' (cloud only; no call made).

## Stage EU — universe sealed
- Logged at 2026-11-26 14:43 UTC
- 42 scheduled, 11 eligible, 11 hunted (all, under cap 20): no 5 (DDRIL ENH NORAM PLSV VTURA), pl 4 (MDV NTT PLW VGO), de 1 (GXI), se 1 (RVRC). bankier (pl issuer calendar) 403. 11 baselines sealed.

## Stage EU — hunters launched
- Logged at 2026-11-26 14:44 UTC
- 8 running (concurrency limit 8): DDRIL ENH NORAM PLSV VTURA RVRC GXI MDV. Queued: NTT PLW VGO.

## Stage EU — hunts banked (1)
- Logged at 2026-11-26 14:45 UTC
- NORAM back: phantom (Q3 released 2026-11-24 17:13 UTC on NewsWeb 687324; 11-27 is only a distribution payment date), event_confirmed false. NTT launched in the freed slot.

## Stage EU — hunts banked (2)
- Logged at 2026-11-26 14:45 UTC
- RVRC back: phantom (Q1 released 2026-11-19 07:30 CET; 11-27 is the SEK 1.50 ex-dividend day, ~-2.8% mechanical on unadjusted close — resolver must not score it). PLW launched.

## Stage EU — hunts banked (3)
- Logged at 2026-11-26 14:49 UTC
- VTURA back: real release 11-27 before Oslo open; target of ENH all-share bid (5.50 ENH/VTURA, LOI 2026-09-11) — ENH also in today's set, so VTURA and ENH are one correlated exposure. impact_sum +0.1. VGO launched (last).
