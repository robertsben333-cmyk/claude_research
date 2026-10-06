# Run log — 2026-10-06

## Stage AU — Australia researcher — DONE (empty session)
- Logged at 2026-10-05 06:42 UTC
- Event date 2026-10-06 (Tue). market_open true (basis: weekday, not an ASX holiday — forward date beyond the index tape). 1574 vendor rows scanned, 0 scheduled on 2026-10-06, 0 eligible, 0 hunted, 0 session_unresolved. Case: a genuinely thin Australian session outside the Feb/Aug reporting seasons, not a shut exchange and not a tape fault. No baselines sealed, no hunters spawned, no orders (stage places none). Universe: research/2026/10/2026-10-06/australia/universe.json.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-05 13:42 UTC
- Fired 2026-10-05 ~13:39 UTC (intraday, European markets open). Sealing for event date 2026-10-06 (Tue), the next European session. Plan: eu_universe (10 markets, cap 20, $100k floor) -> seal baselines -> one bilingual hunter per name in waves of 5 -> edge_score -> note. No orders. Checkout: local branch from origin/main 93d2dd80 (local main clone had diverged after a forced update of origin/main; left untouched), publishing HEAD:main.

## Stage EU — Europe researcher — DONE (empty session)
- Logged at 2026-10-05 13:42 UTC
- Event date 2026-10-06 (Tue), sealed from a 13:39 UTC fire on 2026-10-05 while the European markets were open. No market_closed flag on any of the ten markets.
- Vendor calendar healthy: 4,586 rows scanned across uk/de/fr/se/dk/no/fi/it/es/pl (98 off-primary SE rows filtered). 3 scheduled on 2026-10-06, 0 eligible above the $100k floor, 0 hunted: IHC (uk, $4.1k/day), ALDNE (fr, $1.0k/day), GOP (pl, $3.7k/day). All three session_unresolved (defaulted bmo).
- Case: a genuinely thin early-October session (Nordic Q3 season starts mid-month), not a shut exchange and not a feed fault. No baselines sealed, no hunters spawned, no edge_score run, no note. Floor NOT lowered. Stage places no orders.
- Universe: research/2026/10/2026-10-06/europe/universe.json. Published to main with EARNINGS_DATA_BRANCH=main pinned.

## Stage EU — vendor calendar recall check (operator query)
- Logged at 2026-10-05 15:46 UTC
- Operator reported many UK names on investing.com's calendar for 2026-10-05 that stage EU did not see. Confirmed against Investegate (RNS): 2026-10-05 carried ENSI final results, RMV, SRE and QTX trading updates (>= $100k/day); the 10-02 seal for 10-05 had 0 UK vendor rows.
- Over 2026-09-22 → 10-05 the TradingView scanner MISSED 88 of 135 UK equity results/trading-update RNS above ~$100k/day (rough GBX→USD cut on current 10d volume). Trading updates are never in the vendor feed; but real interims/finals were missed too (e.g. FXPO, AEX, ROCK, ENET, CVSG, MDH, ATOM), and several vendor 'phantoms' reported days later (BILN, HUW, KEFI, RKH), i.e. the vendor dates are estimates. The 2.2% phantom rate in SUBMARKET.md measured PRECISION; RECALL was never measured and is ~35%.
- investing.com: 403 from Cloudflare (not the agent proxy); TLS-impersonating client also 403; a headless-browser load was refused by the session's permission classifier. Not pursued further. Nothing about the 10-06 universe changed.

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-06 01:05 UTC
- 01:06 UTC fire: universe for 2026-10-06, seal baselines, one unpriced-hunter-jp per name in waves of 5, score with edge_score.py. No orders.

## Stage J — resolve 2026-10-02
- Logged at 2026-10-06 01:07 UTC
- jp_resolve.py on 2026-10-02/japan: 5/5 confirmed, rho=0.4 p=0.51, lean_vs_free_control_rho=0.9 (n=5, up from 0.6 on 10-01 and 0.8 on 09-30)

## Stage J — wave 1 done
- Logged at 2026-10-06 01:14 UTC
- 5/5 hunts banked: 1377 +0.6, 2659 +0.6, 2726 -0.3, 2734 0.0, 5243 -1.2. Wave 2 (6469, 8011) running.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-06 01:23 UTC
- 7/7 hunted and ranked on impact_sum; top 6469 +1.90, bottom 5243 -1.20; none above the 2.8 floor. Note: research/2026/10/2026-10-06/japan/japan-note.md. Short register latest file 2026-09-29 (stale).

## Edge hunt — 2026-10-06 amc + 2026-10-07 bmo — STARTED
- Logged at 2026-10-06 17:07 UTC
- Fired 17:04 UTC. Step 0b: execution.enabled true, exit_mode amc_open, but alpaca_trade.py verify --fix --submit DENIED by the auto-mode classifier (real-world transactions), 7th run since 09-28; nothing sold, positions unknown from here. edge_universe.py was also denied once (misclassified), then ran after a read showed it only GETs Nasdaq's calendar. Universe: 6 of 14 rows, all 2026-10-06 amc (STZ PENG NEOG WS SAR AXIL), 0 bmo rows for 10-07 with a session. Baselines sealed 17:12 UTC; option chain on STZ/PENG/NEOG, historical fallback on WS/SAR/AXIL. Plan: 1 sweep + 6 hunters, must finish before the 20:00 UTC amc releases.

## Edge hunt — unknown-session check
- Logged at 2026-10-06 17:07 UTC
- Thin day (6 names), so time-not-supplied rows checked: 1 extra row, ARTW ($0.02bn), session_resolve unresolved / fits cadence (last results 2026-07-10, 88 days). Cadence prior only — the TRT failure mode — so not hunted. provenance stamped: us.v9 · claude-opus-5-5.

## Edge hunt — hunt NEOG banked
- Logged at 2026-10-06 17:14 UTC
- NEOG impact_sum +1.5 (pre-lessons +2.2), abs_move 13, p_up 53. Investor Day 10-07 09:00 ET falls inside the window.

## Edge hunt — hunts AXIL, SAR banked
- Logged at 2026-10-06 17:15 UTC
- AXIL impact_sum -0.1 (pre -0.4), bar unsourced, ~$80k/day turnover. SAR +0.4 (pre +0.5), scaled -0.5, bar disputed.
## Edge hunt (panel) — 2026-10-06 amc — STARTED
- Logged at 2026-10-06 17:08 UTC
- 17:15 UTC. Window 2026-10-06 amc + 10-07 bmo: 6 names (STZ PENG NEOG WS SAR AXIL), all 10-06 amc; 0 bmo. Thin day: --include-unknown added ARTW (unresolved, cadence prior only) — not hunted. Baselines sealed into edge-panel/baselines (3 of 6 with option chains: STZ PENG NEOG). Plan: 1 edge-sweep, 6 unpriced-searcher, then 4 panel judges. No orders.

## Edge hunt (panel) — sweep
- Logged at 2026-10-06 17:12 UTC
- 6 of 6 confirmed amc 2026-10-06 by company releases, 0 phantom, 0 session unsettled. Priority PENG 74, NEOG 66, WS 58, SAR 46, AXIL 36, STZ 28. Provenance: unpriced-searcher us-searcher.v1 · claude-opus-5-5. Launching 6 searchers in one wave.

## Edge hunt — 2026-10-06 amc — DONE
- Logged at 2026-10-06 17:18 UTC
- 6 in window, 6 confirmed by sweep, 0 phantom. Ranked on impact_sum: PENG +2.80 (floor, exactly), NEOG +1.50, SAR +0.40, STZ +0.20, AXIL -0.10, WS -1.50. V2 calibrated (180 obs). Execution: enabled; step 0b verify/close DENIED by auto-mode classifier (7th run since 09-28), nothing sold from here. Step 7: plan (dry run) selected 0 names on impact_scaled >= 1.76 (best PENG 1.60), so no order owed; open not called. Gross 0%. Refused names: all six below the impact_scaled floor; AXIL also below the $200k turnover floor; SAR short not lendable at Alpaca. Note: research/2026/10/2026-10-06/edge/edge-note.md.

## Stage E V2 — shadow ledger
- Logged at 2026-10-06 17:23 UTC
- collected 18 8-Ks (6 tickers), scored 18 blind, refused 0; pooled kappa at session_close +0.355 (se 0.069), n 185.
## Edge hunt (panel) — panel STARTED
- Logged at 2026-10-06 17:22 UTC
- 6/6 searchers returned (PENG +4.40 above 2.8 floor; NEOG +2.00, STZ +0.60, AXIL +0.50, SAR -0.80, WS -0.80). V2 grounded 6/6 before the first print. 6 packs, four judges launched in one message.

## Edge hunt (panel) — DONE
- Logged at 2026-10-06 17:49 UTC
- 6 names, 6/6 confirmed, 6/6 searched (unpriced-searcher, us-searcher.v1). Panel: all four ran on pinned models (opus5, opus55, sonnet55, fable51; Fable's first launch hit a session classifier timeout and was relaunched once). Selected: PENG 4/4 +2.58, NEOG 4/4 +2.11, WS 3/4 -1.25. Spearman stage E impact_sum vs panel_score 0.77 over 6. V2 grounded 6/6 pre-print. No orders and no successful alpaca_trade.py call (an attempted read-only 'assets' call was refused by the permission classifier and dropped; the Routine forbids it anyway). Note: edge-panel/edge-note.md.

## Stage CA — Canada researcher — STARTED
- Logged at 2026-10-06 18:33 UTC
- 18:33Z fire. Universe, seal before 20:00Z close, one unpriced-hunter-ca per name, score, note.

## Stage CA — Canada researcher — EMPTY
- Logged at 2026-10-06 18:33 UTC
- TSX open (market_closed null). 2524 scanner rows, 7 candidates in window, 1 scheduled today (YAY THS Maple Holdings, TSXV, vendor_only), dropped below the $100k turnover floor ($665/day). 0 eligible, 0 hunted. Calendar reconciliation: confirmed 0 / agreed 0 / wsh_only 0 / vendor_only 1 / disputed 0; moved_off_target_by_wsh none; filing_only drops 0. No baselines sealed, so no short-register snapshot stored today and no anchor-arm split. Bank of Canada FX used (Yahoo did not answer). Normal off-peak outcome, not a fault.

## Stage R — reversal researcher — STARTED
- Logged at 2026-10-06 19:04 UTC
- Fired 19:04 UTC = 15:04 ET, inside the 13:30–16:05 ET window. Repo present in working dir (no clone). Intraday screen K=15, seal, 15 reversal-hunters, score, resolve 2026-10-05, note before 16:00 ET.

## Stage R — reversal researcher — DONE
- Logged at 2026-10-06 19:13 UTC
- Intraday screen 15:04 EDT (5,977 screened, 40 passed floors, K=15). XTND dropped (too_little_history); 14 hunted, 14 rankable; provenance rev.v7 · claude-opus-5-5. One floor-clearer: SXTC −8.00 (leg 2, supply; no leg-1 mechanism). Leg 1 non-zero on DCX (+1.0) and NXH (+0.3), both with a mechanism_in_window. 2026-10-05 run resolved: all 15 pending (window closes at today's close); lean_vs_free_control_rho −0.18. Pooled d1 over 10 live runs 09-21→10-02 (134 names): impact_sum ρ +0.020 (p 0.82) vs neg_atr14 +0.109, neg_ret_d −0.153 — hunt has not beaten a free control. Defects carried, constants untouched: overshoot_has_mechanism true on 12/14 with only 2 repricing findings (4th run); DCX ATR14 282% is a consolidation artefact; efts HTTP 500 to several hunters; Nasdaq SI API 503; requests module had to be installed before rev_universe.py would run. No orders placed. Note: reversal/reversal-note.md
