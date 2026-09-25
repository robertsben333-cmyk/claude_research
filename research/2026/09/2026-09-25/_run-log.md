# Run log — 2026-09-25

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-24 06:41 UTC
- Fired 06:41 UTC 2026-09-24. Sealing for the next ASX session, expected 2026-09-25.
- Plan: au_universe -> au_priced_in seal -> unpriced-hunter-au in waves, one per name -> edge_score -> note. No orders.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-24 06:53 UTC
- 27 scheduled / 6 eligible / 6 hunted (no draw, under cap 20) / 0 rankable. session_unresolved 0. All 6 quarterly_report_only; all 6 hunters: event not confirmed, 0 findings.
- Defect (2nd day): late-Sept vendor rows for June-FY 5B filers are the statutory annual report (due 30/09), not a print. 6 of 6 hunts spent on it today, 8 of 12 on 09-24. A pre-hunt filter is warranted; not changed in this run.
- Register lag 3 sessions (ASIC 2026-09-18). ASX PDFs encrypted, eu_pdftext.py fails; hunters' scratch decryptors collided in shared /tmp.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-24 13:39 UTC
- Fired 13:38 UTC 2026-09-24 (markets still open; sealed spot is intraday, not a close). Sealing for event date 2026-09-25 (Fri).
- Plan: eu_universe -> eu_priced_in seal -> one bilingual hunter per name by submarket, waves of 5, publish per wave -> edge_score -> note. No orders.
- Checkout: local main had diverged from origin/main (forced update, no ff); worked from a branch equal to origin/main b643b708, publishing with EARNINGS_DATA_BRANCH=main.

## Stage EU — universe and seal
- Logged at 2026-09-24 13:40 UTC
- 21 scheduled (uk 8, de 2, fr 2, it 4, pl 5; se/dk/no/fi/es 0), 2 eligible above $200k, 2 hunted, no draw. CHG (de) and VGO (pl); both session_unresolved (defaulted bmo), both history estimated_from_cadence, anchor_covered 0 of 2 (DE register read as of 09-23, CHG not named; PL has no register).

## Stage EU — CHG phantom
- Logged at 2026-09-24 13:42 UTC
- CHG: vendor date is a phantom. Issuer Finanzkalender: H1 report '1. Oktober – 31. Oktober' (https://www.chaptersgroup.de/finanzkalender/); 8 Sep release says October. H1 figures already pre-released by ad-hoc 2026-09-08. 0 findings, event_confirmed false. Germany cannot reach event_occurred: false in eu_resolve, so this must be read from the hunt, not the resolver.
- Orchestrator error, caught by the hunter: my brief named researcher_us/LESSONS.md; the agent definition's researcher_europe/LESSONS.md is the right file and was the one read.

## Stage EU — Europe researcher — DONE
- Logged at 2026-09-24 13:50 UTC
- Event date 2026-09-25. 21 scheduled / 2 eligible / 2 hunted / 1 rankable / 0 above floor 3.0. VGO (pl) +0.50; CHG (de) not ranked, phantom date (H1 report due in October per issuer).
- VGO session is amc, not the defaulted bmo: last four interim ESPI releases 17:03-19:57 CEST. Reaction lands 2026-09-28; read move_amc_window_pct at resolve. Baseline left sealed.
- Note: research/2026/09/2026-09-25/europe/europe-note.md. Published to main with EARNINGS_DATA_BRANCH=main pinned.

## Stage J — Japan researcher — DONE (resumed)
- Logged at 2026-09-25 01:06 UTC
- Scheduled fire 01:04 UTC. Output for 2026-09-25 already existed from the 2026-09-18 validation run (2742 -3.90 above floor, 3333 -2.50). Universe re-read to scratch: unchanged, 4 scheduled / 2 eligible / 2 hunted, market_closed null. No new hunt, baselines not revised; addendum appended to japan/japan-note.md.
- Defect fixed: jp_resolve.py on 2026-09-24's run at 10:05 JST took the live 09-25 price as exit_close (4716 +6.77%, not a close). File discarded unpublished; resolver now drops bars for a Tokyo session not yet closed (before 15:30 JST). TDnet confirms 4716 reported 09-24. Resolve 09-24 after 15:30 JST today.

## Close AMC — 2026-09-25 10:00 UTC fire
- Logged at 2026-09-25 10:16 UTC
- Guard: 'python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg' exited 0. execution.enabled=true, orders.exit_mode=amc_open, orders.auction_orders=False -> amc exit placed as a market DAY order queued in the pre-market (opg/cls not available on this account).
- verify --scan 'research/*/*/*/edge' before submit: 14 tracked exit legs across 11 runs, all already resolved (still held 0.0 in each case) -- HOFT(bmo,161/161) FEIM(amc,0/31) ORCL(amc,12/12) RH(amc,0/14) CODA(bmo,183/183) VRA(bmo,0/642) FPS(bmo,0/64) RLGT(amc,0/224) LUXE(bmo,0/292) ALMU(amc,0/167) LEN(amc,0/28) TRT(bmo,338/338) MANU(bmo,187/187) WOR(amc,64/64). No UNFILLED legs to flag.
- close --scan 'research/*/*/*/edge' --submit: no leg had an exit date of 2026-09-25, so nothing new was sent -- every scanned run logged an empty close action (positions: 0, windows: {}). Post-submit fill check reproduced the same 14 already-resolved legs, unchanged.
- status --scan 'research/*/*/*/edge': account flat, equity $11,200.86 = cash $11,200.86, buying power $44,803.44. No open positions anywhere in the scan. 2026-09-23 and 2026-09-24 runs carry no entries at all (stage E's own concern, not this routine's).
- Nothing placed today. Account was already flat before this fire; the amc opening-auction exit this Routine exists for had nothing to act on.

## Edge hunt — 2026-09-25 amc + 2026-09-28 bmo — STARTED
- Logged at 2026-09-25 17:17 UTC
- Fired 17:04 UTC (date -u 17:05). Step 0b (exit_mode amc_open): verify --fix --submit found 14 tracked legs, all resolved, nothing UNFILLED; close --submit had no leg due; account flat, equity $11,200.86 cash, nothing sold, no unrealised P&L to record.
- Universe --window: 6 of 30 rows (IVA amc 09-25; KNDI NTWK GNS MITQ ADXN bmo 09-28). Thin day (<10), so session_resolve.py run on the 17 time-not-supplied rows: 1 killed (ENLV, 6-K 2026-09-22), 16 carried unresolved, 0 confirmed by press release. Carried rows go to the sweep as session_unresolved; any it confirms with a sourced session gets a baseline sealed after the sweep and before any hunter.
- Baselines sealed for the 6 before any agent; none has a live option chain. Plan: 1 sweep, then 1 hunter per confirmed name (cap 19).

## Edge hunt — sweep
- Logged at 2026-09-25 17:23 UTC
- Sweep (1 agent): 22 names swept, 5 confirmed (NTWK, MITQ, GNS, KNDI, ADXN, all 2026-09-28 bmo with a company-sourced session), 5 phantom (CHRN, GRFS, AIV, AIAI, PBM), 12 unconfirmed. IVA, the only amc row, is unconfirmed: no company date found, and last year's H1 went out on a Monday bmo. None of the 16 carried time-not-supplied rows was confirmed. 5 hunters launched 17:23 UTC, one per confirmed name; nothing shed.
- baseline_history_trustworthy=false for NTWK, GNS, KNDI, ADXN (cadence_implausible or under 3 prints); every hunter was told.

## Edge hunt — scored
- Logged at 2026-09-25 17:33 UTC
- 5 hunts returned, all under the current contract (pre_lessons, print_vs_bar_pct, lands_on, resolves_by present). edge_score.py: 5 of 6 rankable (IVA unconfirmed, not hunted), 0 of 5 clear floor 3.0. KNDI +0.50, ADXN 0.00, NTWK 0.00, MITQ -0.10, GNS -1.30. V2 calibrated (177 obs) and written before the first print.
- Assets: 4 of 5 ranked names are below the $200k turnover floor; GNS is $0.55m/day and not lendable at Alpaca. Note: edge-note.md.

## Edge hunt — DONE (execution)
- Logged at 2026-09-25 17:35 UTC
- Execution ON (paper). Step 0b sold nothing: account already flat. Benchmark met by 0 of 5 names (none at |impact_sum| >= 3.0; IVA unrankable). open --submit --no-flatten placed 0 orders with 147 min to the close; no fills. Gross 0% of equity, which stays $11,200.86 in cash.
- Refused: KNDI 0.50, ADXN 0.00, NTWK 0.00, MITQ 0.10, GNS 1.30, all below the floor; IVA had no hunt.
- V2 shadow ledger: collected 0 new 8-Ks, 0 brief inputs, no shadow-scorer launched; measure priced 2 complete (199 pending); fit n=177 at 1d.
- Routine prompt still says 17:04 UTC = 13:04 NY, which is correct; it still names scripts/ shims and edge/LESSONS.md (served via the edge symlink). No failures this run.

## Stage CA — Canada researcher — STARTED
- Logged at 2026-09-25 18:33 UTC
- Fired 18:30 UTC (date -u 18:33, 14:33 ET, inside the Toronto session). Plan: ca_universe.py -> seal baselines before 16:00 ET -> one unpriced-hunter-ca per name in waves of 5 -> edge_score.py -> canada-note.md. Research only, no orders.

## Stage CA — Canada researcher — DONE
- Logged at 2026-09-25 18:36 UTC
- Funnel 6 scheduled / 1 eligible (BRC) / 1 hunted / 0 rankable. Sealed 18:33 UTC inside the session; anchor arms options 0 · register 1; calendar vendor_only 6; register_business_date 2026-09-24; FX fallback 0.71 (Yahoo silent).
- BRC: hunter found no results event on 2026-09-25 (pre-revenue explorer, filing-only interims, Q3 not due till 10-30); event_confirmed false, not ranked.
- DEFECTS (not patched): (1) ca_universe.py marked BRC event_shape=release though it is filing-only; (2) history headline classifier counts 'Annual General Meeting Results' as financial results — all 3 of BRC's sealed history rows are AGMs.

## Stage R — reversal researcher — STARTED
- Logged at 2026-09-25 19:04 UTC
- Fired 19:04 UTC = 15:04 ET, inside the 13:30–16:05 ET screen window. Repo was present (no clone). Plan: rev_universe --intraday --k 15 for drop date 2026-09-25, seal 15 baselines, 15 reversal-hunters in parallel, edge_score, resolve 2026-09-24, note before 16:00 ET where possible.
