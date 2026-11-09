# Run log — 2026-11-10

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-09 14:38 UTC
- Fired 2026-11-09 ~14:37 UTC (Mon). Sealing for event date 2026-11-10 (Tue). Plan: universe -> seal -> provenance -> hunters in waves of 5 -> score -> 4-judge panel -> note -> IBKR handoff. Step 0: local main shallow/unrelated to force-updated origin/main; re-pointed main at origin/main (clean tree), all scripts present.

## Stage EU — IBKR
- Logged at 2026-11-09 14:38 UTC
- mode: execution_eu.enabled is false; broker = executor server (auth tws); this session makes no broker call

## Stage EU — progress
- Logged at 2026-11-09 14:48 UTC
- Universe: 68 scheduled, 42 eligible, 20 drawn (random, seed eu-2026-11-10): it 6, de 5, se 5, uk 2, dk 1, no 1; largest it 30%. 20 baselines sealed ~14:50 UTC (intraday spots). Wave 1 launched: A2A ABDP BAHN_B BEAMMW_B BFF.

## Stage EU — panel STARTED
- Logged at 2026-11-09 15:18 UTC
- 20/20 hunts banked, all search_complete. 18 ranked; BAHN_B (Q3 on 11-17, Telenor SEK 62 offer) and BEAMMW_B (Q3 on 11-11) not ranked, no event. None above floor 2.8; top DIA +1.60, bottom ABDP -0.80. Hunters re-read BFF and INW as amc (release after close, reaction 11-11). 18 packs, four -intl- judges.

## Stage EU — IBKR handoff
- Logged at 2026-11-09 15:25 UTC
- ibkr-handoff.json written (no broker call; execution_eu.enabled false, so the executor places nothing). Rule panel_pct>=70 + 4 judges: BUY BFF (74.4), SELL A2A (72.0); DIA not taken (turnover $0.14m < $0.20m floor). Caveat: BFF releases amc per hunter, so its reaction is 11-10 close -> 11-11 close.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-09 15:25 UTC
- Sealed for 2026-11-10 (Tue) ~14:47 UTC Mon 11-09 (intraday spots). 68 scheduled, 42 eligible, 20 drawn (it 6, de 5, se 5, uk 2, dk 1, no 1). 20/20 hunts, all search_complete. 18 ranked; BAHN_B (Q3 11-17) and BEAMMW_B (Q3 11-11) not ranked. None above floor 2.8; top DIA +1.60, bottom ABDP -0.80. Panel 4/4 members, 18/18 each, no fallback; selected DIA long 4/4 (panel_pct 90). BFF and INW are amc per hunters. anchor_covered 4/20; es/pl 0; de 5. Pushed to main (EARNINGS_DATA_BRANCH=main).
