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

## Stage E-P amc exit — 2026-11-24
- Logged at 2026-11-24 14:09 UTC
- Fired 14:07 UTC (09:09 ET). Guards: live and paper both exit 0 (amc_open, amc -> open as day, matched on placement). Verify --fix: live 5 legs all filled (STEM OMER FEAM RRGB SNEX), paper 7 legs all filled (CURI CTVA STEM OMER FEAM RRGB SNEX); nothing UNFILLED, no rescue. Close --today-only: LIVE SYM amc (2026-11-23 run) market DAY queued for open, order c1c6ea6f-0b4e-4410-8449-aa2ca633da8d; PAPER SYM amc market DAY, order 8e859408-0108-4765-86ab-11f53f022b99. DKS bmo not sent on either account (market placement, market closed): left for stage E-P's own run.

## Edge hunt (panel) — 2026-11-24 amc + 2026-11-25 bmo — STARTED
- Logged at 2026-11-24 18:13 UTC
- Fired 18:06 UTC (13:06 ET). 24 names in window (11 amc, 13 bmo), baselines sealed to edge-panel/baselines/. Plan: 1 edge-sweep, up to 20 unpriced-searchers (amc first), sell at 3s, four judges, buy at 6b.

## Edge hunt (panel) — sweep
- Logged at 2026-11-24 18:16 UTC
- Sweep: 16 confirmed, 1 phantom (PSNY, Q3 postponed 11-03), 7 unconfirmed. Hunting 20 (cap): the 16 confirmed + DELL, URBN, BBAR, GASS (unconfirmed, highest hunt_priority; searchers check the event). Shed: OMSE, YSG, ADXN, PSNY. SEC_USER_AGENT is unset in this environment, so FPI 6-K histories are empty (baseline_history_trustworthy false for every FPI). Waves: 8 amc now, then 3 amc + 5 bmo, then 4 bmo.
## Edge hunt (panel v3b) — 2026-11-24 amc + 2026-11-25 bmo — STARTED
- Logged at 2026-11-24 18:15 UTC
- Fired 18:12 UTC (13:12 ET). Universe 24 rows (11 amc 11-24, 13 bmo 11-25), no share classes folded; 24 baselines sealed in edge-panel-v3b/baselines/. Plan: one edge-sweep, up to 20 unpriced-searcher-v3b (amc first, max 6 a turn), four panel-judge-v3b judges, two panel_score calls. No orders.

## Edge hunt (panel v3b) — wave 1
- Logged at 2026-11-24 18:22 UTC
- Sweep: 22 of 24 confirmed, 0 phantom; URBN and ADXN unconfirmed (vendor-only; URBN likely 11-25 amc, outside the window), YSG session unsettled (bmo likely). Hunting 20: shed URBN, ADXN (unconfirmed) and HDL (12), OMSE (22) (lowest hunt_priority). Wave 1 (turn 1, 6 amc): CLSK AMBA NTNX QFIN WDAY ADSK, agent unpriced-searcher-v3b (not the fallback). Queued: HPQ DELL BBAR NOAH (amc), GDS PSNY LI BZ GOTU NNOX DE YSG DSX GASS (bmo).
## Edge hunt (panel) — unfinished search
- Logged at 2026-11-24 18:23 UTC
- ADSK searcher hit the turn's shared WebSearch budget (200) ~18:30 UTC: search_complete false. hunt_status retry moved it to hunts/_unfinished/; relaunched in a later turn. Further launches capped below 8 per turn.
