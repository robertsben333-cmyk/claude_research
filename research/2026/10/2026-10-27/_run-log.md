# Run log — 2026-10-27

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-26 13:47 UTC
- Fired 13:35 UTC 2026-10-26 (Routine trig_018WGfdq2fUm1ZqJhCGQ1wde), session start 13:45 UTC. Sealing for event date 2026-10-27 (Tue), next European session. Plan: eu_universe (cap 20, $100k floor) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> four-model intl panel -> note. No orders. Local main was a shallow clone unrelated to the force-updated origin/main; working on a local branch cut from origin/main 840103925, publish.sh pushes HEAD:main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-26 13:50 UTC
- Event date 2026-10-27. 57 scheduled, 40 eligible (uk 2, de 3, fr 4, se 10, no 4, fi 8, it 2, es 2, pl 5), 20 drawn (random, seed eu-2026-10-27): fi 5, se 4, de 3, no 2, pl 2, uk/fr/it/es 1 each. Largest market fi 25%, 9 markets. Baselines sealed ~13:50-13:51 UTC at intraday spots (European markets still open). session_unresolved: BEI, VIB3, GOFORE, VRLA, YACHT, BDX, KRU. ENC sealed amc. Registers: es/pl none; all others read. Provenance stamped (orchestrator model not passed; get_session not available). Wave 1 launched: BEI P911 VIB3 ENC FIA1S.

## Stage EU — short-register cache
- Logged at 2026-10-26 13:50 UTC
- eu-short-cache.json refreshed by the seal; committed so tomorrow's Nordic/IT short change is computable.

## Stage EU — wave 1 mostly banked, wave 2 launched
- Logged at 2026-10-26 14:00 UTC
- Banked: VIB3 +0.6, FIA1S -0.5, BEI -1.4, ENC -0.9 (ENC confirmed amc by issuer filing: window 27 Oct close -> 28 Oct close). P911 still running. Wave 2 launched early (4/5 of wave 1 banked): GOFORE GRK TIETO TYRES VRLA.

## Stage EU — session corrections from hunters
- Logged at 2026-10-26 14:11 UTC
- VRLA: sealed bmo (session_unresolved), issuer calendar says 'communiqué de presse après bourse' 27 Oct -> amc, true window 27 Oct close -> 28 Oct close. ENC: sealed amc, confirmed amc. YACHT and TYRES release intraday (inside the sealed window). Baselines not revised (sealed); eu_resolve.py measures both windows for unresolved sessions.

## Stage EU — BDX session
- Logged at 2026-10-26 14:13 UTC
- BDX: sealed bmo (session_unresolved); hunter infers amc from the last two quarterly filings (18:18, 19:33 Warsaw) -> likely window 27 Oct close -> 28 Oct close. Inferred, not observed.

## Stage EU — KRU session
- Logged at 2026-10-26 14:15 UTC
- KRU: sealed bmo (session_unresolved); every KRUK interim report since 3Q25 filed 17:13-17:19 Warsaw (after close) -> amc, window 27 Oct close -> 28 Oct close. Q3 net profit pre-released 16 Oct. Short register read via rksgpw.com mirror: 2.21% building (hunter-sourced, not the baseline).

## Stage EU — panel STARTED
- Logged at 2026-10-26 14:19 UTC
- 20 hunts banked and scored (impact_sum range +0.80 VNV to -2.00 VRLA; none above floor 2.8). 20 packs, four intl judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-10-26 14:28 UTC
- 20 ranked: VNV +0.80 ... VRLA -2.00; none above floor 2.8. Panel 4/4 members, no fallback, 1 selected: VRLA short (k=3, panel_pct 79). Sessions: VRLA, KRU, BDX probably amc (sealed bmo?); ENC amc as sealed. anchor_covered 3/20; es/pl 3 names; 9 se/fi names need resolving within ~a week. Note: europe/europe-note.md. No orders. Pushed to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-27 01:05 UTC
- Fired 01:05 UTC (10:05 JST) 2026-10-27. Plan: jp_universe -> seal baselines -> provenance -> unpriced-hunter-jp in waves of 5 (cap 25) -> edge_score -> four-model panel -> note. No orders.

## Stage J — wave 1 launched
- Logged at 2026-10-27 01:07 UTC
- Universe: 29 scheduled, 25 eligible (4 dropped on turnover), 25 hunted, method 'all 25 eligible names (at or under the cap)'. Calendar sheets kessan.xlsx, kessan08_1002 (as_of 10-01), kessan09_1023 (as_of 10-22). Baselines sealed ~01:08 UTC, short register 20261026 (575 codes); provenance jp.v5 / claude-opus-5-5. Five waves of 5. Wave 1: 2212 3911 4063 4479 4519.

## Stage J — resolved 2026-10-23
- Logged at 2026-10-27 01:07 UTC
- jp_resolve: 8/9 usable, impact_sum rho 0.335 (p 0.40), free control 0.571, sign right 4/8, lean_vs_free_control_rho -0.071. Panel resolved too. One day is not a result.

## Stage J — wave 1 banked
- Logged at 2026-10-27 01:16 UTC
- 5/5 hunts returned: 2212, 3911, 4063, 4479, 4519. Wave 2 running as slots free (4684 4733 4765 4973 5344).

## Stage J — wave 2 banked
- Logged at 2026-10-27 01:24 UTC
- 4684 4733 4765 4973(running) 5344 5532 5911: 10/25 hunts banked by 01:24 UTC. Rolling slots of 5.

## Stage J — container restart
- Logged at 2026-10-27 01:28 UTC
- Container restarted at ~01:28 UTC; hunters 6337 6988 7102 7175 7309 lost mid-run and re-launched. 12/25 hunts banked.

## Stage J — panel STARTED
- Logged at 2026-10-27 01:46 UTC
- 25/25 hunts banked and scored (top 7102 +2.00, 6337 +1.90; bottom 4063 -1.40, 7751 -1.30; none above 2.8). 25 packs, four judges.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-27 01:55 UTC
- 25 ranked: top 7102 +2.00, 6337 +1.90; bottom 4063 -1.40, 7751 -1.30; none above floor 2.8. Panel 4/4 members, no fallback, 6 selected (7102 L, 6337 L, 3911 S, 5532 S, 4479 S, 7751 S). Resolved 10-23 (lean_vs_free_control_rho -0.071). One container restart, 5 hunters re-run. Note: japan/japan-note.md. No orders.

## Stage M — morning exit review — STARTED
- Logged at 2026-10-27 13:15 UTC
- source research/2026/10/2026-10-26/edge-panel, 10 picks (KNSA CLS GLXY AEYE CVLT DQ SOFI PSMT RMBS JBLU), 09:16 ET; concurrent subagent cap is 8, RMBS and JBLU queued

## Stage M — previous morning scored
- Logged at 2026-10-27 13:16 UTC
- resolve 2026-10-26 done; pool: 32 names over 6 days, review -1.70% (t -1.10), static -1.77% (t -1.11), review_minus_static +0.07 (t 0.14); brier_review_minus_prior open_lags -0.009 (t -0.64), fade -0.008 (t -0.54)

## Stage M — morning exit review — done
- Logged at 2026-10-27 13:19 UTC
- 10 names compiled 09:19 ET (10/10 analysts, morning-reaction-analyst, no fallback): exit_open CLS DQ RMBS JBLU; exit_1000 SOFI PSMT; exit_limit GLXY 16.95, AEYE 7.95, CVLT 148.50; exit_close KNSA. Concurrent subagent cap of 8 delayed RMBS and JBLU ~2 min. AEYE's what_would_change_it names 7.60, the analyst's own threshold rather than a tape price; left unrepaired per skill.

## Edge hunt (panel) — 2026-10-27 amc + 2026-10-28 bmo — STARTED
- Logged at 2026-10-27 17:15 UTC
- Stage E-P fire 17:06 UTC (session start 17:08). Universe 168 names (82 amc 10-27, 86 bmo 10-28), baselines sealed for all 168 in edge-panel/baselines before any agent. Plan: one edge-sweep, up to 20 unpriced-searchers, step 3s flatten, four-judge panel, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-10-27 17:22 UTC
- Sweep finished ~17:22 UTC (27 of 168 checked): 22 company-confirmed, all sessions settled; 0 phantoms proven; 5 checked-unconfirmed (BBAI TP MTLS RCKY ORN); RUSHB folded into RUSHA by the sweep; 141 unchecked. Cap 20: the 20 highest-priority confirmed (amc 10-27: LUNG BOOM KIDS RBBN BBNX ENPH UCTT LU OI INTA FSP SLDE SEVN BRSP; bmo 10-28: REPL OTLY OPFI JMKE AMRN DMC). Shed by hunt_priority: NHTC (62) and CTO (60), confirmed; all unconfirmed/unchecked. baseline_history_trustworthy=false for LU, JMKE. Searchers unpriced-searcher, amc first, 8 at a time.

## Edge hunt (panel) — searcher progress
- Logged at 2026-10-27 17:33 UTC
- 13 of 20 searchers returned by 17:33 UTC (all amc except BRSP SLDE still running); all 20 launched (DMC last at ~17:33). Running: SLDE BRSP REPL OTLY OPFI JMKE AMRN DMC.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-10-27 17:42 UTC
- 20/20 searchers returned by ~17:41 UTC (unpriced-searcher, native, Opus 5.5; all 20 events company-confirmed). mode: execution enabled. flatten --submit at 17:42 UTC: held AEYE 250 (+30.89%), CLS 8 (+1.22%), CVLT -11 (-2.25%), GLXY 134 (+5.96%), KNSA 33 (+25.30%) from the 2026-10-26 book, closed at market; account flat, equity $11,799.77.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-27 17:42 UTC
- 20 packs, four judges, one part. edge_score and V2 grounded written ~17:43 UTC, before the first print.
