# Run log — 2026-11-12

## Close AMC — stage E pre-market exit
- Logged at 2026-11-12 11:19 UTC
- Fired 11:12 UTC (06:12 ET). Guard `mode --require-exit-tif opg` exit 0 (amc_open; amc -> open as market DAY, auction_orders false). verify over 12 edge runs / 14 exit legs: none UNFILLED, nothing held. close --submit: 0 legs due today, NO orders sent, no refusals (stage E's Routine is stopped, so no new edge book exists; stage E-P's amc legs are not in this scan). Post-wait verify: all 14 ok.

## Stage E-P amc exit — 2026-11-12
- Logged at 2026-11-12 14:08 UTC
- 14:08 UTC (09:08 ET). Guard mode --require-exit-tif opg: exit 0 (amc -> open as market DAY, matched on placement). verify --fix --submit over 18 edge-panel runs: 0 exit legs to check, nothing UNFILLED, no rescue. close --today-only --submit: 2 amc legs of the 2026-11-11 book SENT as market DAY orders queued for the open: CURI (order a02c6084-d77f-4a12-b951-a1ca28612d15) and CTVA buy-to-cover 839 sh (order cfbc3a00-ad2e-47fa-ab48-e4c8e7fd56cc), both pending_new. No refusals printed; no bmo legs due today.

## Stage M — morning exit review — STARTED
- Logged at 2026-11-12 14:15 UTC
- source research/2026/11/2026-11-11/edge-panel, 09:15 ET, 3 picks (CURI, CAE, CTVA), analysts launched

## Stage M — previous morning scored
- Logged at 2026-11-12 14:15 UTC
- pool: 109 names over 15 days; review +2.40% (t 2.01) vs static +2.42% (t 2.17); review_minus_static −0.02pp (t −0.04); Brier review−prior p_open_lags −0.016 (t −1.32), p_fade −0.007 (t −0.76)

## Stage M — morning exit review — done
- Logged at 2026-11-12 14:17 UTC
- 3 names: CURI exit_1000, CTVA exit_open, CAE exit_open; compiled 09:17 ET; all 3 analysts ran (morning-reaction-analyst)

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-12 14:37 UTC
- Fired 14:36 UTC (15:36 Amsterdam, markets open). Sealing for event date 2026-11-13 (Fri), RUN research/2026/11/2026-11-13/europe. Plan: universe (cap 20), seal, provenance, one hunter per name (up to 8 concurrent), edge_score, four-model panel, note, IBKR handoff. Local main was a stale shallow checkout diverged from a force-updated origin; main re-pointed at origin/main 95ec29fb0.

## Stage EU — universe and seal
- Logged at 2026-11-12 14:40 UTC
- Event date 2026-11-13. 66 scheduled, 23 eligible above $100k, 20 hunted by date-seeded random draw (seed eu-2026-11-13): it 7, de 4, uk 2, se 2, es 2, dk 1, no 1, pl 1 (fr/fi 0). Largest market it at 35%. 20 baselines sealed ~14:45 UTC (intraday spots, not closes). Provenance stamped (uk.v7, de.v7, nordic.v5, it.v5, es.v5, pl.v5). IBKR mode: execution_eu.enabled true, environment live (since 2026-11-12, executor server trades); this session has no IBKR env and makes no broker call, handoff file only.

## Stage EU — hunts in progress
- Logged at 2026-11-12 14:40 UTC
- 14:40 UTC: running AEIN AFG ASMDEE_B BAVA BC8 COG DIA ELN (8 concurrent). Queued: ERG ETH FAA G IP IRLAB_A LAND MARR MRL NA9 TIP TRE.

## Stage EU — hunts in progress
- Logged at 2026-11-12 14:48 UTC
- 14:48 UTC: banked 13: AEIN DIA BAVA ASMDEE_B AFG BC8 COG ELN ERG FAA ETH LAND IRLAB_A. DIA phantom (H1 out 2026-11-10; 13 Nov is an investor presentation). AEIN pre-released Q3 by ad-hoc 12 Nov 13:17 CET. Hunters put COG, ELN, ETH after the 11-13 close (amc); ERG in-session. IRLAB_A fell ~72% on 12 Nov inside-info release (restructuring). Running: G IP MARR MRL NA9 TIP TRE.

## Stage EU — panel STARTED
- Logged at 2026-11-12 14:54 UTC
- 20 of 20 hunted; 19 ranked, DIA not ranked (no event: H1 out 2026-11-10). No name above the 2.8 floor; top MRL +1.40, bottom TRE -1.30. Hunters put COG, ELN, ETH, TIP after the 11-13 close (amc); ERG, MARR, IP in-session on 11-13. 19 packs, four judges.

## Stage EU — IBKR handoff
- Logged at 2026-11-12 15:02 UTC
- Handoff written (no broker call): 2 names at panel_pct >= 70 with four judges — SELL TRE (71.8, es), SELL MARR (71.5, it). Offline plan sized on a 10,000 EUR placeholder equity at the sealed spots; the executor sizes on the real account. Caveat: MARR releases in-session ~15:30-16:15 CET on 11-13, so part of its reaction may land 11-16. execution_eu.enabled true, environment live.

## Stage EU — ranking
- Logged at 2026-11-12 15:02 UTC
- 19 ranked, DIA phantom (H1 out 2026-11-10). No name above the 2.8 floor; top MRL +1.40, bottom TRE -1.30. Panel (4 of 4 members, no fallback) selects none under 3-of-4; highest panel_pct MARR and TRE short at 72. Italy 35% of the day.
- Published to main (EARNINGS_DATA_BRANCH=main): origin/main head d1ae494c9 'stage EU: IBKR handoff for 2026-11-13' confirmed at 15:02 UTC.

## Edge hunt (panel) — 2026-11-12 amc + 2026-11-13 bmo — STARTED
- Logged at 2026-11-12 18:09 UTC
- Stage E-P fire; session began 18:08 UTC (13:08 ET). Universe 148 names (124 amc 11-12, 24 bmo 11-13). edge_universe.py ran directly (needed pip install requests). Baselines sealing by code (14 parallel priced_in processes); one edge-sweep in parallel. Plan: up to 20 unpriced-searchers (max 8 per turn), step 3s flatten live then paper, four-judge panel, step 6b buy live then paper.

## Edge hunt (panel) — baselines sealed
- Logged at 2026-11-12 18:11 UTC
- 148 of 148 baselines sealed by 18:11 UTC, before any searcher (ACCV: only 28 usable bars, spot None). provenance stamped US-P: unpriced-searcher us-searcher.v3 on claude-opus-5-5.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-12 18:12 UTC
- 18:12 UTC. Sweep (time-boxed): 29 of 148 checked, 15 company-confirmed, 7 unconfirmed (NU STN INTR SMFG MFG ELPC CIG), 0 phantom, ~119 unchecked. Session unsettled: DLO XXI. Cap 20: hunted the 15 confirmed + unconfirmed by hunt_priority NU STN INTR SMFG MFG. Shed: ELPC CIG (unconfirmed, lowest priority), all unchecked. baseline_history_trustworthy false: XXI ACCV SMFG MFG. Wave 1 (8 amc): CBRS ACCV BLTE ANDG LFTO HAWK ARWR DLO.

## Edge hunt (panel) — all 20 launched
- Logged at 2026-11-12 18:25 UTC
- 18:25 UTC. All 20 searchers launched (MFG last). Returned, search_complete true per hand-backs: BLTE ARWR ANDG LFTO HAWK CBRS DLO ACCV CSCO NKTR HTFL AMAT. DLO session settled amc from the company's release. Running: STNE FLO NU STN XXI INTR SMFG MFG.
