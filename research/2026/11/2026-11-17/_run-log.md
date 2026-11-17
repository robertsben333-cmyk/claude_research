# Run log — 2026-11-17

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-16 14:37 UTC
- Fired 14:36 UTC 2026-11-16 (15:36 Amsterdam, markets open). Sealing for event date 2026-11-17 (next European session). Plan: universe (cap 20, $100k floor) -> seal -> one bilingual hunter per name in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Note: local main in this container had diverged from a force-updated origin/main; the run works on a fresh branch off origin/main and publishes HEAD:main.

## Stage EU — IBKR
- Logged at 2026-11-16 14:38 UTC
- mode (no broker call from this session): broker = IB Gateway on executor's server (auth tws); this session only hands over. Last line: 'would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is live' — expected here, no IBKR env in the Routine.

## Stage EU — universe and seal
- Logged at 2026-11-16 14:41 UTC
- Event date 2026-11-17 (Tue). 38 scheduled, 21 eligible above $100k, random draw of 20 (seed eu-2026-11-17): uk 5, se 3, dk 3, pl 3, de 2, es 2, fr 1, no 1. Largest market uk 25%, 8 markets. 20 baselines sealed ~14:45 UTC (intraday spots, not closes). Provenance stamped. Wave 1 launched: DPLM IMB ZEG ALO NIBE_B.

## Stage EU — hunts
- Logged at 2026-11-16 14:49 UTC
- Banked so far: DPLM +0.5, IMB -1.7, ALO -0.2 (amc 18:00 CET confirmed), NIBE_B +0.9. Running at 5 concurrent rather than strict waves, to reach the IBKR handoff before the 17:30 CET close. DEFECT for a building session: NIBE_B baseline seals short 0.0 but FI shows 5.27% aggregate (LEI 549300ZQH0FIF1P0MX67); looks like a register name-join miss in eu_positioning for se. Baseline left sealed as is.

## Stage EU — register defect
- Logged at 2026-11-16 14:54 UTC
- Second Swedish short-register miss: SEYE baseline 0.0 / anchor_covered false, FI aggregate lists 'Smart Eye Aktiebolag (publ)' at 4.47% (2026-11-13). With NIBE_B (5.27%) this is a systematic se name-join failure in eu_positioning; baselines left sealed. Fix in a building session.

## Stage EU — Spain register lead
- Logged at 2026-11-16 14:58 UTC
- EDR hunter: CNMV per-issuer short page (posicionescortas?nif=A02850956, and per-holder posicionescortascomunicaciones.aspx?nif=…&idDecl=<LEI>) answers from this container where the grid the baseline uses does not; EDR disclosed shorts 3.15% (Citadel 1.46, CFM 0.89, ActusRay 0.80). Possible Spanish positioning anchor for a building session to verify; baselines unchanged.

## Stage EU — panel STARTED
- Logged at 2026-11-16 15:12 UTC
- 20 of 20 hunted; 19 ranked, PXM not ranked (issuer's own date is 2026-11-23: a phantom). No name above the 2.8 floor; top NIBE_B/REACH +0.90, bottom OHLA -2.20. Packs built, four judges launching.

## Stage EU — IBKR handoff
- Logged at 2026-11-16 15:18 UTC
- ibkr-handoff.json written (no broker call): BUY NIBE_B (se, pct 86.1, 1189 sh @ 46.65 SEK, 49.99%) and BUY DPLM (uk, pct 70.8, 58 sh @ 71.8 GBP, 49.89%) on a 10,000 EUR offline plan. Not taken: REACH (turnover $0.12m below the $0.20m execution floor), OHLA (panel_pct 69.8 < 70), ZEG (65.5).

## Stage EU — DONE
- Logged at 2026-11-16 15:19 UTC
- 20 hunted, 19 ranked (PXM phantom: issuer date 23.11). No name above the 2.8 floor. Panel (4 of 4 members, no fallback) selects REACH and NIBE_B long. Handoff: NIBE_B, DPLM. Published to origin/main (pinned EARNINGS_DATA_BRANCH=main; publish.sh's rebase raced concurrent hunters writing eu-short-cache.json, so later pushes were done with plain git rebase + push HEAD:main). Defects for a building session: se short-register name join (NIBE_B 5.27, SEYE 4.47, BAHN_B 0.1 read as 0.0); CNMV per-issuer short page reachable (EDR).

## Stage E-P amc exit — 2026-11-17
- Logged at 2026-11-17 14:09 UTC
- Guards: live and paper both exit 0 (amc open as day, matched on placement). Verify: live 0 exit legs; paper CURI 4303/4303 and CTVA 839/839 filled, nothing UNFILLED, no rescue. Close --today-only (2026-11-16 run): LIVE STEM amc day SENT 54030db3-9b56-454d-9249-39dd982939d5, OMER amc day SENT 323bbad8-d1f7-4c9a-a585-ecb9862c1f43; PAPER STEM amc day SENT c8f4389c-ed16-48af-a902-8e3aa26b20a9, OMER amc day SENT 35bd0688-6423-41aa-8794-dab2a91c4f7d. KLAR bmo refused on both accounts: market placement and the market is closed, left for stage E-P's own run. Market DAY orders queued 09:09 ET for the 09:30 open.

## Edge hunt (panel) — 2026-11-17 amc + 2026-11-18 bmo — STARTED
- Logged at 2026-11-17 18:09 UTC
- 32 names in window (12 amc 11-17, 20 bmo 11-18), baselines sealed 18:09Z; plan: 1 edge-sweep, up to 20 unpriced-searchers, 4 judges. Orchestrator Routine fired 18:07 UTC (13:07 ET). SEC_USER_AGENT absence may thin 6-K histories (hist_n=0 on foreign issuers).

## Edge hunt (panel) — sweep and waves
- Logged at 2026-11-17 18:14 UTC
- Sweep: 29 confirmed of 32 (phantoms KNDI, CAAP, CISS); session unsettled TJX, SQM (both out before 11-18 open). Cap 20 by hunt_priority: hunted PRE IIIV BRBR LZB FEAM GLBE DLB JJSF JMIA SQM KRNT PONY BLSH ZIM ZKH ENRD TGT CSHR ZTO ICCM; shed (lowest priority) GLNG AUNA HAFN IRIX TJX GBDC LOW GLAD NVDA. Wave 1 (amc first): IIIV LZB FEAM DLB SQM ZTO PRE BRBR.
## Edge hunt (panel v3b) — 2026-11-17 amc + 2026-11-18 bmo — STARTED
- Logged at 2026-11-17 18:21 UTC
- 32 names in window (12 amc 11-17, 20 bmo 11-18), own baselines sealed 18:21Z; plan: 1 edge-sweep, up to 20 unpriced-searcher-v3b, 4 panel-judge-v3b judges; no orders.

## Edge hunt (panel v3b) — sweep and waves
- Logged at 2026-11-17 18:30 UTC
- Sweep: 29 confirmed of 32 (phantom/unconfirmed KNDI, CAAP, CISS); SQM session unsettled (reaction lands 11-18 either way). Cap 20 by hunt_priority: hunted BRBR PONY PRE GLBE JMIA KRNT BLSH LZB FEAM DLB IIIV ENRD SQM TGT ZKH JJSF AUNA CSHR LOW ICCM; shed (lowest priority) TJX IRIX ZTO NVDA GLNG HAFN GBDC GLAD ZIM. Wave 1 (amc first, max 6 a turn): LZB FEAM DLB IIIV SQM AUNA.
