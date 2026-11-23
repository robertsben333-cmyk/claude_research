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

## Stage EU — wave 2 launched
- Logged at 2026-11-23 14:56 UTC
- KEOC SBB_B (se) ATG BRCK CWK (uk), launched while wave 1 still had BWLPG CDR VOT running, to keep the handoff ahead of the European close. Wave 1 done: ELT, PGE (hunter reports PGE is amc: past reports 17:55-21:33 Warsaw).

## Stage EU — wave 1 banked
- Logged at 2026-11-23 14:57 UTC
- 5/5 returned: BWLPG ELT PGE CDR VOT. CDR and PGE hunters settle session as amc (issuer timestamps); VOT session unsettled. Running: KEOC SBB_B ATG BRCK CWK GROW IGP KGF (8-subagent concurrency limit). Queued: LMP MARS POLR RNWH SFR SUP TEP.

## Stage EU — defect found by SBB_B hunter
- Logged at 2026-11-23 15:05 UTC
- Sealed SBB_B baseline reads short 0.0, but the FI aggregate register lists 'Samhällsbyggnadsbolaget i Norden AB' at 16.22% (2026-11-20), per the hunter. Likely a diacritic name-match miss in eu_positioning's Swedish join (vendor name 'Samhallsbyggnadsbolaget I Norden AB'). Baseline left as sealed; not verified in code this run — flag for a development session.

## Stage EU — hunts
- Logged at 2026-11-23 15:09 UTC
- 20/20 hunts returned, scored. No name above the 2.8 floor (max |impact_sum| 1.2: ATG, BWLPG, VOT +1.2; ELT -1.2).

## Stage EU — panel STARTED
- Logged at 2026-11-23 15:09 UTC
- 20 packs, four judges

## Stage EU — panel
- Logged at 2026-11-23 15:15 UTC
- 4/4 judges, no fallback. Selected (3 of 4 in own top 20%): ELT 96 short (4/4), KEOC 89 short (4/4), ATG 89 long (4/4), IGP 84 long (3/4). VOT 79 long (2/4).

## Stage EU — IBKR handoff
- Logged at 2026-11-23 15:17 UTC
- handoff written: 4 names (offline plan, sealed spots, EUR 10,000 equity): SELL ELT 26.5%, BUY ATG 30.5%, SELL KEOC 30.4%, BUY BRCK 12.5%. Not taken: IGP and VOT (turnover $0.12m < $0.20m floor), GROW (pct 68.9 < 70). Published to main; the executor server buys.

## Stage EU — done
- Logged at 2026-11-23 15:17 UTC
- Published to main, verified: origin/main at c4be35bbe carries ibkr-handoff.json. Work done on a local branch off origin/main because local main had diverged after a force-push; local main left untouched.
