# Run log — 2026-11-19

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-18 14:38 UTC
- Fired 14:38 UTC 2026-11-18 (15:38 Amsterdam, markets open). Sealing for event date 2026-11-19. Plan: universe (cap 20) -> seal -> provenance -> one bilingual hunter per name in waves -> edge_score -> 4-judge intl panel -> note -> IBKR handoff (no broker call).

## Stage EU — IBKR
- Logged at 2026-11-18 14:38 UTC
- mode: execution_eu.auth tws; broker is the operator's server. Last line: would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is 'live' (expected in this session; no broker call is made here).

## Stage EU — universe and seal
- Logged at 2026-11-18 14:42 UTC
- 79 scheduled, 34 eligible (uk 15, pl 10, se 3, fr 2, no 2, dk 1, fi 1), 20 drawn by random sample seed eu-2026-11-19: uk 10, pl 4, fr 2, no 2, se 1, fi 1. Largest market uk 50%. 20 baselines sealed; provenance stamped (orchestrator claude-opus-5-5). bankier (pl issuer calendar) HTTP 403. session_unresolved: AQ ATT AUROORA MBR NEU UBI. ELIOR amc.
- Hunting in two waves of 10 rather than four of 5, so the IBKR handoff can land before the European close (fired 14:38 UTC, an hour after the nominal slot).

## Stage EU — hunts
- Logged at 2026-11-18 14:43 UTC
- Platform concurrency cap is 8 subagents. Wave 1 running: BAB CMCX GPE GRI HLMA (uk), UBI ELIOR (fr), SUBC (no). Queue: HAUTO AGO + 10 more, launched as slots free.

## Stage EU — hunts
- Logged at 2026-11-18 14:45 UTC
- CMCX banked: phantom — interims moved to 26 Nov per company Q&A (7 Oct) and financial calendar; vendor row still 19 Nov. Findings empty. HAUTO launched.

## Stage EU — hunts
- Logged at 2026-11-18 14:47 UTC
- GPE banked: impact_sum +0.35, abs 3.0, p_up 53; interims bmo confirmed (14 Oct update). AGO launched.

## Stage EU — hunts
- Logged at 2026-11-18 14:48 UTC
- HLMA banked: impact_sum +0.6, abs 6.5, p_up 55; H1 bmo confirmed (24 Sep update). LIO launched.

## Stage EU — hunts
- Logged at 2026-11-18 14:49 UTC
- GRI banked: impact_sum -0.3, abs 4.5, p_up 51; FY bmo 07:00 confirmed (Notice of Results 22 Sep). MHA launched.
