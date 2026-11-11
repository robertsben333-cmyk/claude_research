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

## Stage M — morning exit review — STARTED
- Logged at 2026-11-11 14:15 UTC
- source research/2026/11/2026-11-10/edge-panel, 09:16 ET (fired 09:15, late)

## Stage M — morning exit review — done
- Logged at 2026-11-11 14:17 UTC
- 7 names (NRGV AMPX STUB FOSL CRWV LPTH MRCY): exit_open x4 (NRGV STUB FOSL CRWV), exit_limit x2 (AMPX 9.85, MRCY 87.00), exit_1000 x1 (LPTH). Compiled 09:17 ET. Pool over 102 names/14 days: review_minus_static +0.001 (t 0.00).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-11 14:38 UTC
- Fired 14:36 UTC (15:36 Amsterdam, markets open). Sealing for event date 2026-11-12 (Thu), RUN research/2026/11/2026-11-12/europe. Plan: universe (cap 20), seal, provenance, one hunter per name in waves, edge_score, four-model panel, note, IBKR handoff. Local main was a stale shallow checkout diverged from origin; kept as branch local-main-backup-20261111 and main re-pointed at origin/main f3cdaaa62.

## Stage EU — IBKR
- Logged at 2026-11-11 14:38 UTC
- mode: would refuse: execution_eu.enabled is false (auth tws; executor server trades, this session makes no broker call).

## Stage EU — universe and seal
- Logged at 2026-11-11 14:41 UTC
- Event date 2026-11-12. 190 scheduled, 116 eligible, 20 hunted by date-seeded random draw: de 8, it 4, no 3, uk 2, se 2, pl 1 (fr/dk/fi/es 0). 20 baselines sealed at ~14:43 UTC (intraday spots, not closes). Provenance stamped. Hunters launching as slots free (up to 8 concurrent) so the handoff reaches main before the close.

## Stage EU — hunts in progress
- Logged at 2026-11-11 14:42 UTC
- 14:47 UTC: running SIE COK OHB BKHT SMWH BRBY XPLRA KAR (session cap 8 concurrent). Queued: REY CAR SYNSAM ENDUR GENO 1U1 GLJ VBK VH2 DIB MN TFIN.

## Stage EU — hunts in progress
- Logged at 2026-11-11 14:55 UTC
- Banked 12: COK OHB XPLRA KAR SMWH BKHT BRBY SIE CAR REY ENDUR GENO. CAR: vendor date phantom (Q3 is 2026-11-17 amc per RB 2/2026). XPLRA/ENDUR hunters found register positions the baseline missed on spelling (2.48% / 0.51%); baselines untouched. Running 8: SYNSAM 1U1 GLJ VBK VH2 DIB MN TFIN.

## Stage EU — panel STARTED
- Logged at 2026-11-11 15:02 UTC
- 20 of 20 hunted; 19 ranked, CAR not ranked (no event on 2026-11-12; Q3 report is 2026-11-17). No name above the 2.8 floor; top SMWH +1.00, bottom SIE -2.20. DIB hunter puts the release after the 11-12 close (amc). 19 packs, four judges.

## Stage EU — ranking
- Logged at 2026-11-11 15:12 UTC
- 19 ranked, CAR phantom (Q3 is 2026-11-17). No name above the 2.8 floor; top SMWH +1.00, bottom SIE -2.20. Panel (4 of 4 members, no fallback) selects SYNSAM short (92, 4/4), SIE short (87, 3/4), XPLRA short (83, 3/4). DIB releases after the 11-12 close (amc).

## Stage EU — IBKR handoff
- Logged at 2026-11-11 15:12 UTC
- Handoff written (no broker call): 4 names at panel_pct >= 70 with four judges — SELL SYNSAM (92.2), SELL SIE (86.6), SELL XPLRA (83.0), BUY VBK (72.1). execution_eu.enabled is false per mode at 0s, so the executor should send nothing.

## Stage EU — published
- Logged at 2026-11-11 15:13 UTC
- All output pushed to main (EARNINGS_DATA_BRANCH=main); origin/main head 314171364 'stage EU: IBKR handoff for 2026-11-12' confirmed, ibkr-handoff.json present on main.

## Edge hunt (panel) — 2026-11-11 amc + 2026-11-12 bmo — STARTED
- Logged at 2026-11-11 18:08 UTC
- Stage E-P fire; session began 18:07 UTC (13:07 ET). Universe 124 names (34 amc 11-11, 90 bmo 11-12). edge_universe.py ran directly (needed pip install requests in the container). Baselines being sealed by code (13 parallel priced_in processes); one edge-sweep in parallel. Plan: up to 20 unpriced-searchers (max 8 per turn), step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — baselines sealed
- Logged at 2026-11-11 18:11 UTC
- 124 of 124 baselines sealed by 18:11 UTC, before any searcher. provenance stamped US-P: unpriced-searcher us-searcher.v3 on claude-opus-5-5.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-11 18:15 UTC
- 18:15 UTC. Sweep: 33 of 124 checked, 29 company-confirmed, 4 unconfirmed (OPRX TWST PLGO AGRO), 0 phantom, 91 unchecked (8 small amc + 83 bmo). Session unsettled among confirmed: DGII TNK TK (+others). Cap 20, hunted by hunt_priority: amc ACOG AVEX XNDU CURI ALVO AGBK DDI CINT VYLR CTVA ENS EZPW ITRG CAE DGII(session unsettled) TTEK; bmo LUNR NBIS ASND YETI. Shed: confirmed below priority 42 (TNK ECO CEPU FNV HBM OR TK BSRT BN), unconfirmed 4, unchecked 91. No hunted baseline is suspect; no amendment. Sweep flag: ITRG may have released 11-10 — searcher told to check. Wave 1 (8 amc): ACOG AVEX XNDU CURI ALVO AGBK DDI CINT.

## Edge hunt (panel) — wave 2
- Logged at 2026-11-11 18:22 UTC
- 18:22 UTC. Returned, search_complete true per hand-backs: DDI ALVO CINT CURI XNDU AVEX. Launched as slots freed: VYLR CTVA ENS EZPW ITRG CAE. Running: ACOG AGBK + those six. To launch: DGII TTEK, then bmo LUNR NBIS ASND YETI.

## Edge hunt (panel) — all 20 launched
- Logged at 2026-11-11 18:28 UTC
- 18:28 UTC. All 20 searchers launched (YETI last). Returned, search_complete true per hand-backs: DDI ALVO CINT CURI XNDU AVEX ACOG AGBK ITRG EZPW VYLR ENS. Running: CTVA CAE DGII TTEK LUNR NBIS ASND YETI.
