# Run log — 2026-10-02

## Stage AU — Australia researcher — STARTED
- Logged at 2026-10-01 06:41 UTC
- Fired 06:41Z 2026-10-01; sealing for the next ASX session (2026-10-02). Plan: universe -> seal -> one unpriced-hunter-au per name in waves -> edge_score -> note. No orders.

## Stage AU — Australia researcher — EMPTY UNIVERSE
- Logged at 2026-10-01 06:41 UTC
- Case: market_open true with zero names (basis: 'beyond the tape: a weekday that is not an ASX holiday'). Vendor scan read 1577 rows, 0 scheduled for 2026-10-02 after the Sydney-date shift, 0 eligible, 0 hunted, 0 session_unresolved. Genuinely thin session outside the Feb/Aug reporting seasons.
- No baselines sealed, no hunters spawned, no scores. No orders (this stage never places any).

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-01 13:38 UTC
- Fired Thu 2026-10-01 13:38 UTC (15:38 Amsterdam, markets open) on main (8f333bcd); sealing for next European session Fri 2026-10-02. Plan: eu_universe -> eu_priced_in seal -> one market hunter per name in waves of 5 -> edge_score -> europe-note. No orders. Pushing to main (EARNINGS_DATA_BRANCH=main pinned).

## Stage EU — universe and seal
- Logged at 2026-10-01 13:39 UTC
- 3 scheduled (uk 1, fr 1, pl 1) / 1 eligible above $200k / 1 hunted; selection.method: all 1 eligible (under cap 20), seed eu-2026-10-02 unused. by_market uk 1 (JDW J D Wetherspoon, $1.12m/day). market_concentration: uk 1.00, 1 market. Dropped below floor: ALBPK (fr, $8.8k/day), KER (pl, $41k/day). No market_closed. Off-primary filtered: se 231, pl 325.
- Register read: uk (2026-09-29, 420 rows). anchor_covered 1 of 1 (JDW disclosed 4.57%, change -0.01pp). session_unresolved 0 (bmo, vendor flag). history.basis observed_rns (n 8, median |move| 4.91%). es/pl 0, de 0. One wave of 1 hunter (unpriced-hunter-uk).

## Stage EU — Europe researcher — DONE
- Logged at 2026-10-01 13:46 UTC
- 1 hunted / 1 rankable / 0 above floor 3.0. JDW -0.91 (FY27 outlook line after +13.5% rally from July warning; abs 6.5, p_up 43; pre_lessons -0.88). Event confirmed by issuer's 22 Jul RNS.
- Note: research/2026/10/2026-10-02/europe/europe-note.md. No orders. Published to main (EARNINGS_DATA_BRANCH=main).

## Stage J — Japan researcher — STARTED
- Logged at 2026-10-02 01:05 UTC
- Fired 01:05Z 2026-10-02 (10:05 JST) on main (4b54850). Plan: jp_universe -> jp_priced_in seal -> provenance stamp -> one unpriced-hunter-jp per name in waves of 5 -> edge_score -> japan-note. No orders.

## Stage J — universe and seal
- Logged at 2026-10-02 01:06 UTC
- 9 scheduled / 5 eligible (4 dropped below ¥15m turnover floor) / 5 hunted; selection.method: all 5 eligible names (at or under the cap 25), seed jp-2026-10-02 unused. market_closed null. Sheets kessan07_0904 (as_of 09-03), kessan08_0918 (as_of 09-17). Short register 20260929 read (598 codes); margin ratio resolved 4 of 5 (4394 None). baseline_quality direction 0.6 x4, 0.45 x1. One wave of 5 unpriced-hunter-jp.

## Stage J — Japan researcher — DONE
- Logged at 2026-10-02 01:15 UTC
- 5 hunted / 5 rankable / 0 above floor 3.0. Ranking: 3321 +0.60, 7611 +0.40, 7965 +0.10, 6279 -0.25, 4394 -1.00. 3 positive / 2 negative. One in-session release (7611, 15:00). Prompt jp.v6. Last resolved lean_vs_free_control_rho 0.80 (09-30, n=5). Note: research/2026/10/2026-10-02/japan/japan-note.md. No orders.

## Stage X — Close AMC — 2026-10-02
- Logged at 2026-10-02 10:15 UTC
- Guard mode --require-exit-tif opg exit 0 (amc open as day). verify: 14 legs, none UNFILLED, nothing held. close --submit: no legs due today, no exits sent, no refusals; account reachable. status: no open positions.

## Edge hunt — 2026-10-02 amc + 2026-10-05 bmo — EMPTY WINDOW
- Logged at 2026-10-02 17:06 UTC
- Step 0b: execution.enabled is true, but alpaca_trade.py (mode/verify --fix --submit) was DENIED by this session's auto-mode permission classifier (real-world transactions); no exit was sent and none attempted another way. Repo record: no position held since the 2026-09-22 book closed 09-23, and 2026-09-25 onward placed 0 entries, so nothing appears owed. This session did not verify the account at the broker.
- Universe: edge_universe.py --window found 0 of 3 calendar rows in the window (2026-10-02 amc + 2026-10-05 bmo). All 3 are time-not-supplied rows dated 2026-10-05.
- Thin-day check: --include-unknown + session_resolve.py: 0 killed, 0 confirmed, 3 carried (not applied). AEHR: company has pre-announced Q1 FY27 for Mon 2026-10-05 AFTER the close (call 17:00 ET), per https://www.marketbeat.com/instant-alerts/upcoming-aehr-test-systems-aehr-set-to-announce-quarterly-earnings-on-monday-2026-09-28/ — that is 10-05 amc, which belongs in Monday's window and not this one. NCPL (last results 291 days ago) and MSS (563 days ago) are well past cadence and read as phantom rows.
- Result: empty universe, stopped cheaply per the skill. No baselines, no sweep, no hunters (0 of 20 subagents), no edge-scores.json, no V2. Step 7: no names, so no book; open --submit not attempted (and would be refused by the same classifier). 0 orders, gross 0%.
- Standing blocker for the operator: until a narrow allow rule for researcher_us/scripts/alpaca_trade.py is added to .claude/settings.json (a session may not write it), any day WITH floor-clearers will not trade from this Routine. Fifth consecutive run (since 09-28) with the denial.

## Edge hunt (panel) — 2026-10-02 amc + 2026-10-05 bmo — EMPTY WINDOW
- Logged at 2026-10-02 17:09 UTC
- Stage E-P fired 17:07 UTC on main (dd2b274). Own edge_universe.py --window into edge-panel/: 0 of 3 rows (all time-not-supplied, dated 10-05). Thin-day check --include-unknown + session_resolve.py (dry run): 0 killed, 0 confirmed, 3 carried; AEHR is company-announced for 10-05 amc (next window), NCPL 291d and MSS 563d past cadence. Stopped cheaply: 0 searchers, 0 judges, no packs, no edge-scores, no V2. No alpaca_trade.py call of any kind. Note: research/2026/10/2026-10-02/edge-panel/edge-note.md.

## Stage CA — Canada researcher — STARTED
- Logged at 2026-10-02 18:33 UTC
- Fired 18:33Z. Plan: ca_universe -> seal baselines before 20:00 UTC close -> provenance -> one unpriced-hunter-ca per name -> edge_score -> note. No orders.

## Stage CA — Canada researcher — EMPTY DAY
- Logged at 2026-10-02 18:33 UTC
- 18:33Z: ca_universe.py: 2510 scanner rows, 6 candidates in the ±window, 0 reconciled to 2026-10-02. market_closed null and scheduled_today 0 = nobody scheduled (normal Canadian weekday outside the peaks), not a closed exchange. Reconciliation all zero; moved_off_target_by_wsh empty; 0 filing_only drops. No baselines sealed, so no short-register snapshot stored today. No hunters spawned. No orders (stage places none).
