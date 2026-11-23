# Run log — 2026-11-24

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-23 14:38 UTC
- Fired 14:37 UTC Mon 2026-11-23 (15:37 Amsterdam, markets open). Sealing for event date 2026-11-24 (Tue). RUN = research/2026/11/2026-11-24/europe. Plan: universe -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff.
- Note: origin/main was force-rewritten since the container snapshot; local main diverged (86/50). Worked from a fresh local branch off origin/main; publish.sh pushes HEAD:main.

## Stage EU — IBKR
- Logged at 2026-11-23 14:38 UTC
- mode: broker=IB Gateway on executor server (auth tws); this session only hands over. Last line: 'would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is live' — expected here, no credentials in the Routine.

## Stage EU — universe and baselines
- Logged at 2026-11-23 14:48 UTC
- 42 scheduled, 25 eligible (>= $100k), 20 drawn (seed eu-2026-11-24): uk 13, pl 4, se 2, no 1. Concentration: UK 65%. Yahoo calendar unavailable on every market; bankier (PL) 403. 20 baselines sealed. Provenance stamped (orchestrator claude-opus-5-5).
- Hunters: 4 waves of 5. Wave 1: BWLPG(no) CDR ELT PGE VOT(pl).
