# Run log — 2026-09-17

## Stage 0 — universe — 07:14 CEST
- Logged at 2026-09-17 05:14 UTC
- Window: After the US close on Thursday 17 September 2026 through before the US open on Friday 18 September 2026
- Source: nasdaq (after-close 15 rows, before-open 8 rows; 1 in window)
- Universe: 1 total (1 AMC, 0 BMO); 0 eligible after qualification
- Excluded: 1 (below_market_cap_floor: UPXI, $76.0M market cap vs $500M floor)
- Notes: Thin actionable window as of this run — not a holiday, just few confirmed prints on the calendar yet. Eligible count (0) is at or below triage.skip_if_universe_at_or_below (10), so stage 1 will skip today.

## Maintenance — per-name cap raised to 33% of equity
- Logged at 2026-09-17 06:38 UTC
- execution.sizing.max_position_pct_of_equity: 20 -> 33, on the operator's instruction. Live on main from this commit; it applies to the NEXT book, not to the ALMU and LEN positions already open, which were sized under the 20% cap.
- At the current paper equity of ~$11,260 a capped name is $3,710. Two names deploy 66% of the account, three names 99%. Below three names the book is deliberately under-invested, where that used to be below five.
- What it costs, stated rather than buried: concentration. The 22-23% gaps in the resolved sample (NX +22.23%, CANG -23.01%) move the account about 7.5% at a 33% weight against 4.5% at 20%. Nothing in this stage is hedged or stopped out, so the cap is the risk control.
- max_position_pct_of_adv stays at 1.0%. At $10k of equity a 33% position is 1.65% of a $200k/day name, so capacity now binds before equity in the thinnest tradable names and the leftover is redistributed over the rest of the book.
- Updated with it: config comments, edge/EXECUTION.md (four passages), CLAUDE.md. scripts/smoke_test.py no longer hardcodes the old cap in its under-deployment check; it reads the shipped numbers and is green.

## Stage 1 — triage (08:40 CEST)
- Logged at 2026-09-17 06:40 UTC
- Mode: skipped (universe eligible count 0, at or below threshold 10)
- Funnel: 1 universe -> 0 eligible -> 0 cleared floors -> 0 shortlisted
- Scouts: 0 subagents (nothing to screen)
- Session mix: n/a
- Notable drops: UPXI (excluded at stage 0, market cap $76.0M < $500M floor)
- Note: validate_stage.py's shortlist check previously required a non-empty list, which a genuinely empty eligible universe can't satisfy under skip-mode; fixed to allow shortlist: [] when triage_mode is skipped_small_universe and universe_eligible is 0.

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-17 08:22 UTC
- Shortlist: 0 names (triage_mode: skipped_small_universe, universe_eligible: 0); this batch: none
- Already on disk, skipping: none
- Plan: no researchers to spawn — shortlist is empty because today's universe had only 1 AMC print (UPXI, $76.0M market cap) which failed the $500M floor at stage 0, so stage 1 skipped with 0 names

## Stage 2 — deep dive, batch 1 — FINISHED (08:23 UTC)
- Logged at 2026-09-17 08:22 UTC
- Researched: none (shortlist empty)
- Skipped (already done): none
- Failed: none
- Subagents: 0 opus/high, 0 waves
- Median evidence completeness: n/a
- Note: 0 names capped from a shortlist of 0 — nothing dropped for the cap. Confirmed against 00-universe.json/01-shortlist.json before publishing this section, not just the earlier run-log entries.

## Close AMC — amc opening-auction exit — 2026-09-17
- Logged at 2026-09-17 10:11 UTC
- Guard: python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg exited 0 (execution.enabled=true, orders.exit_mode=amc_open, amc -> opg / bmo -> day). Proceeded.
- verify --scan 'research/*/*/*/edge' first: 9 of 11 exit legs already ok/closed from prior days (HOFT, FEIM, ORCL, RH, CODA, VRA, FPS, RLGT, LUXE all still held 0.0). ALMU and LEN (2026-09-16/edge, amc, exit_date 2026-09-17) were the only legs due today: still held 167 and 28 respectively, 0/167 and 0/28 filled — expected, fired pre-open.
- SENT: 2026-09-16/edge ALMU, amc session, exit_date 2026-09-17, opg (opening auction), qty 167 buy-to-cover, order 43561a60-077d-4108-9584-df101aa9bb2d, status pending_new at submission.
- SENT: 2026-09-16/edge LEN, amc session, exit_date 2026-09-17, opg (opening auction), qty 28 buy-to-cover, order af499521-2c8d-4331-960e-5e52f5ae53bf, status pending_new at submission.
- No bmo legs due today; no refusals this run.
- Post-submit verify (after the script's 300s fill-check wait): ALMU and LEN both report 'work' — filled 0, still held 167.0 / 28.0, 'waiting on the 09:30 ET opening auction; not verifiable until it has crossed'. Expected: an opg order does not fill until the auction runs, well after this pre-market firing.
- status --scan confirms both still OPEN: ALMU -167 @ 13.35 (+13.86% unrealized), LEN -28 @ 79.96 (+4.50% unrealized); exit order state 'new' for both.
- Account reachable throughout: paper, equity $11,669.19, cash $15,727.77, buying power $40,771.06.
- Not a rescue point: firing before 09:28 ET means no plain-market rescue is available here even if the auction cross under-fills (documented behavior: HOFT 17/161, CODA 39/183, RLGT 0/224 in past runs). Stage E's own run inside the session is what carries an UNFILLED leg forward via 'verify --fix'.
