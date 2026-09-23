# Run log — 2026-09-23

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-23 01:05 UTC
- 01:05 UTC fire. 2026-09-23 is 秋分の日 (Autumnal Equinox Day); expecting market_closed. Build universe, publish, stop if shut.

## Stage J — Japan researcher — MARKET CLOSED
- Logged at 2026-09-23 01:05 UTC
- Tokyo shut: market_closed = 'public holiday: 秋分の日' (Cabinet Office 国民の祝日 list). scheduled_today 0 because the exchange is closed, not because a cohort sheet is missing. Sheets read: kessan07_0904.xlsx (as_of 2026-09-03, 236 rows), kessan08_0918.xlsx (as_of 2026-09-17, 444 rows). Empty universe published at japan/universe.json; no baselines, no hunters, no scoring. No orders: this stage has no broker step.

## Close AMC — 2026-09-23 opening auction
- Logged at 2026-09-23 10:17 UTC
- Guard: mode --require-exit-tif opg exited 0 (execution.enabled=true, exit_mode=amc_open, amc placement=open/day).
- verify before close: all 12 prior exit legs read still-held 0.0, none UNFILLED — nothing needed a rescue.
- close --submit: only one amc leg had an exit date of today — 2026-09-22/edge WOR, sent as a market DAY order queued for the open (client_order_id 5994e8fb-1ee0-415b-89aa-27a4ed43eb65).
- 2026-09-22/edge MANU (bmo) correctly deferred: exit placement is market, not open, so it is left to stage E's own 13:05 ET run rather than sent here.
- fill check at +300s: WOR reads work, filled 0/64, still held 64.0 — expected, since Alpaca queues a pre-market DAY order and does not route it until the 09:30 ET open; not verifiable from this session.
- status --scan confirms account state: equity $11,064.67, cash $11,552.50. 2026-09-22/edge shows MANU OPEN long 187 @ 20.43 (+0.39%) and WOR OPEN short -64 @ 59.23 (-14.05%), both awaiting their respective exits.
- No account/API errors. Nothing else to report.
