# Run log — 2026-11-25

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-24 14:38 UTC
- Fired 14:38 UTC 2026-11-24 (15:38 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-25. Plan: universe -> baselines -> hunters in waves of 5 -> score -> 4-model panel -> note -> IBKR handoff.

## Stage EU — IBKR
- Logged at 2026-11-24 14:38 UTC
- mode: broker=IB Gateway on the executor's server (auth tws); this session only hands over. Last line: would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is 'live' (expected in the cloud: no broker env here).

## Stage EU — universe and baselines
- Logged at 2026-11-24 14:47 UTC
- 39 scheduled, 25 eligible (>= $100k), 20 drawn (seed eu-2026-11-25): uk 5, no 5, se 3, es 2, pl 2, de 1, fr 1, dk 1. Concentration: UK 25%, 8 markets. 20 baselines sealed (intraday spots, ~15:00 UTC). Hunters in waves of 5.

## Stage EU — hunters launched
- Logged at 2026-11-24 14:48 UTC
- First 8 (concurrency limit): EZJ PETS (uk) AT1 (de) MPCC (no) SECT_B (se) GRE (es) LOUP (fr) TXT (pl). Queued: HLCL IPX NRR BWO JACK NORSE SOFTX ROCK_A BIOA_B CANTA HBX MUR.

## Stage EU — hunts banked (partial)
- Logged at 2026-11-24 14:53 UTC
- Returned so far: TXT (hunter settles session as amc from issuer IR notice: H1 after the WSE close on 25 Nov, so the sealed bmo window holds no release), AT1, EZJ. HLCL launched.

## Stage EU — hunts banked (2)
- Logged at 2026-11-24 14:56 UTC
- Back: TXT AT1 EZJ MPCC PETS SECT_B LOUP (+NORSE file). LOUP hunter settles session amc (AMF flux timestamps 17:45 Paris on the last two results), so like TXT its print is outside the sealed bmo window. EZJ: under a 715p Apollo cash offer, event_confirmed false. Running: GRE HLCL IPX NRR BWO NORSE BIOA_B ROCK_A. Queued: JACK SOFTX CANTA HBX MUR.

## Stage EU — hunts banked (3)
- Logged at 2026-11-24 14:59 UTC
- 12/20 back (+BWO GRE NRR HLCL NORSE). NORSE: issuer moved Q3 to 2026-11-30 (NewsWeb 687104, 2026-11-20), event_confirmed false. All 20 launched; running IPX ROCK_A BIOA_B JACK SOFTX CANTA HBX MUR.

## Stage EU — hunts
- Logged at 2026-11-24 15:05 UTC
- 20/20 hunts returned, scored. 18 ranked; EZJ and NORSE not ranked (no event on date: EZJ unconfirmed under a 715p bid, NORSE moved Q3 to 11-30). No name above the 2.8 floor (max |impact_sum| 0.9: MPCC +0.9; IPX, LOUP -0.9). TXT and LOUP settled amc by their hunters.

## Stage EU — panel STARTED
- Logged at 2026-11-24 15:05 UTC
- 18 packs, four judges

## Stage EU — panel
- Logged at 2026-11-24 15:11 UTC
- 4/4 judges, no fallback. Selected (3 of 4 in own top 20%): HBX 89 short (4/4), MPCC 85 long (3/4), SOFTX 77 short (3/4). GRE 77 long (2/4).

## Stage EU — IBKR handoff
- Logged at 2026-11-24 15:11 UTC
- handoff written (before the note, to beat the 16:25 Oslo close): 3 names, offline plan at sealed spots on EUR 10,000: SELL HBX 40.9%, BUY MPCC 35.4%, BUY GRE 23.2%. Not taken: SOFTX (turnover $0.10m < $0.20m floor), ROCK_A 64.6 and LOUP 67.2 (< 70). Published to main; the executor server buys.

## Stage EU — done
- Logged at 2026-11-24 15:13 UTC
- Note published. Handoff went out before the note (15:12 UTC) to reach the server before the Oslo close. Defect for a dev session: ROCK_A baseline short 0.0 vs Finanstilsynet 2.49% (name-join miss on share-class suffix; join on ISIN). Pushed to main (EARNINGS_DATA_BRANCH=main).

## Stage E-P amc exit — 2026-11-25
- Logged at 2026-11-25 14:08 UTC
- Fired 14:07 UTC (09:07 ET). Guards: live and paper both exit 0 (amc -> open as market DAY, matched on placement). Verify: live 6 earlier exit legs ok, paper 8 ok, nothing UNFILLED, no rescues. LIVE close (2026-11-24 edge-panel): QFIN amc day 34ebc8c1-d3fe-4e17-9f48-4bdd8a9bea16, DELL amc day 1ca34bd1-1ec7-47ff-b850-9fa4498346b2, AMBA amc day 18f1823e-82fb-4e6e-bd14-21d47f2559a5. PAPER close: QFIN amc day b6fd79f5-5a70-40c7-94d7-d76df317ec1a, DELL amc day a6528f41-8174-4a83-99ee-0b4fc48d4706, AMBA amc day cfb0eb22-d271-44d5-84f0-121241521235. All queued for the 09:30 open. No refusals; no bmo legs due today.

## Edge hunt (panel) — 2026-11-25 amc + 2026-11-27 bmo — STARTED
- Logged at 2026-11-25 18:09 UTC
- Fired 18:07 UTC (13:07 ET). Thanksgiving week: window is 11-25 amc + 11-27 bmo (Friday half day). Only 2 confirmed-session names (FINV amc 11-25, XYF bmo 11-27); baselines sealed. Thin day: 33 time-not-supplied rows checked with session_resolve.py (1 killed: PVL already reported; 32 carried, 0 announced). SEC_USER_AGENT unset, www.sec.gov 403, EDGAR checks degraded. The 32 carried rows go to the sweep to settle date and session; baselines for any it confirms are sealed before any searcher launches. Plan: 1 sweep, up to 20 searchers, 4 judges; sell at 3s, buy at 6b, live then paper.

## Edge hunt (panel) — sweep
- Logged at 2026-11-25 18:17 UTC
- Sweep confirmed 3 of 35: FINV amc 11-25, BMA amc 11-25, XYF bmo 11-27 (all react in the 11-27 half-day session). 32 time-not-supplied rows dropped (KT/NWCL/UCFI/AEXA/EDVA/LEXX already reported, NAT 11-30, AREC/AAME/SCLX delinquent, rest unsourced). BMA baseline sealed after the sweep, before any searcher. Wave: 3 searchers, none shed.
## Edge hunt (panel v3b) — 2026-11-25 amc + 2026-11-27 bmo — STARTED
- Logged at 2026-11-25 18:19 UTC
- Strict window: 2 names (FINV amc 11-25, XYF bmo 11-27). Thin day, so the 33 time-not-supplied rows were checked with session_resolve.py: 3 killed by EDGAR (NWCL, PVL, ENLV), 30 carried, none announced. 11 carried rows at/above $200k turnover plus BMA/UCFI (no bars at first seal) go to the sweep with the 2 confirmed: 13 names. 19 below-floor unknown rows not hunted. Searcher unpriced-searcher-v3b, judges panel-judge-v3b-*, no orders.

## Edge hunt (panel) — 3s sell
- Logged at 2026-11-25 18:28 UTC
- 18:28 UTC: all 3 searchers finished (hunt_status: 0 unfinished of 3). Live: mode ok (enabled, kill switch off); flatten: 0 positions held, nothing to sell. Paper: flatten: 0 positions held, nothing to sell. No amc leg was still held (E-PX sold QFIN/DELL/AMBA at the open).

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-25 18:28 UTC
- 3 packs, four judges
## Edge hunt (panel v3b) — sweep
- Logged at 2026-11-25 18:26 UTC
- Sweep: 13 names, 3 confirmed from company sources (FINV amc 11-25, BMA amc 11-25, XYF bmo 11-27), 4 phantoms (KT, NAT, UCFI, AEXA), 6 unconfirmed with no company date (EH, LEE, OPHI, SIDU, AREC, SRTM). BMA re-sealed with its confirmed amc session and XYF re-sealed after a Yahoo bars failure, both before any searcher. Launching 3 unpriced-searcher-v3b, amc first.

## Edge hunt (panel v3b) — wave 1
- Logged at 2026-11-25 18:27 UTC
- 3 confirmed, 3 searchers launched in one turn (FINV, BMA amc; XYF bmo), none shed. FINV brief initially carried a placeholder for its sweep row; sent the row file by message.

## Edge hunt (panel) — 6b buy
- Logged at 2026-11-25 18:35 UTC
- 18:36 UTC (13:36 ET): all four judges (opus5, opus55, sonnet55, fable51) on 3/3 packs, no fallback. 0 names at panel_pct >= 80 (FINV 79.2 short, 3 of 4 in own top 20%; BMA 61 S; XYF 57 S). No-strong-name top-up APPLIED on both accounts with FINV short (cap 33%). Live (equity $3,479): FINV short 484 @ 2.3625, filled, $1,147 (33.0%). Paper (equity $24,135): FINV short 3,360, order read partially_filled 2,778 @ 2.36 at status time while the position showed -3,360 @ 2.36. Exit: FINV is amc, so E-PX sells at the 11-27 open (half day). BMA/XYF not traded (below 70). V2 grounded written before the first print. Stage E wrote no edge/ today (Routine stopped).
## Edge hunt (panel v3b) — panel STARTED
- Logged at 2026-11-25 18:35 UTC
- 3 hunts finished (search_complete true, v3b fields present on all 3). edge_score: FINV -2.80, BMA -0.40, XYF +0.40. 29 unhunted baselines moved to baselines/_not_hunted/ (default bmo label, not an established session) before V2, which then grounded 3 of 3. 3 packs, four v3b judges.

## Edge hunt (panel v3b) — done
- Logged at 2026-11-25 18:39 UTC
- Four v3b judges ran on their named agents, 3/3 coverage. Own history: FINV selected short at 94 (4/4 in own top 20%), BMA 10 short, XYF 3 long; E-P scale 94/9/3. Stage E-P: no selection (FINV 79.2); rho of panel_pct_signed +1.00 on n=3; XYF side differs. No orders, no shadow ledger.

## Holistic research — 2026-11-25 — STARTED
- Logged at 2026-11-25 19:16 UTC
- 19:17 UTC (14:17 ET). Pick from E-P's sweep (3 confirmed: FINV, BMA amc; XYF bmo 11-27), evolving hp.v4 + control hp.v1 on every name, one wave. No orders.
