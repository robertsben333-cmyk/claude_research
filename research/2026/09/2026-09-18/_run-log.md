# Run log — 2026-09-18

## Stage 0 — universe (05:13 UTC)
- Logged at 2026-09-18 05:15 UTC
- Window: After the US close on Friday 18 September 2026 through before the US open on Monday 21 September 2026
- Source: nasdaq
- Universe: 0 total (0 AMC, 0 BMO); 0 eligible after qualification
- Excluded: 0 (companies[] empty — nothing reached the eligibility check)
- Notes: Nasdaq returned rows (7 for 09-18, 8 for 09-21) but all but one carried time-not-supplied/unknown session; the one confirmed row (ABVX, amc on 09-21) does not fill the before-open slot. Per the qualification rule, unconfirmed-session rows are dropped rather than kept. Same pattern as 2026-09-17 (session_resolve.py may recover a real name from these later in stage E).

## Stage 1 — triage (06:39 UTC)
- Logged at 2026-09-18 06:39 UTC
- Mode: skipped (universe <= threshold: 0 eligible <= 10)
- Funnel: 0 universe -> 0 eligible -> 0 cleared floors -> 0 shortlisted
- Scouts: 0 subagents (screen skipped per triage.skip_if_universe_at_or_below)
- Session mix: 0 AMC / 0 BMO
- Notable drops: none (drop happened upstream in stage 0 qualification, not triage)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-18 08:24 UTC
- Shortlist: 0 names (triage_mode: skipped_small_universe, universe_eligible: 0, universe_total: 0); this batch: none
- Already on disk, skipping: none (02-dossiers/ does not exist yet)
- Plan: no researchers to spawn — today's universe had 0 eligible names (Nasdaq returned 7 after-close/8 before-open rows but only one, ABVX amc 09-21, had a confirmed session, and it doesn't fill the before-open slot), so stage 1 skipped with an empty shortlist

## Stage 2 — deep dive, batch 1 — FINISHED
- Logged at 2026-09-18 08:24 UTC
- Researched: none (shortlist empty)
- Skipped (already done): none
- Failed: none
- Subagents: 0 opus/high, 0 waves
- Median evidence completeness: n/a
- Note: 0 names capped from a shortlist of 0 — nothing dropped for the cap. Confirmed against 00-universe.json/01-shortlist.json before publishing this section, not just the earlier run-log entries. Batch 2 should also find nothing to do unless stage 1 is re-run and finds names.

## Execution — the amc exit instrument, root-caused and changed
- Logged at 2026-09-18 09:34 UTC
- The 2026-09-17 amc exit failed the same way as the three before it: ALMU (167) and LEN (28) went in as `opg` market orders at 10:05 UTC from the Close AMC Routine and both EXPIRED with ZERO filled, at 09:31:31 and 09:30:52 ET. The operator covered both by hand at 09:47 ET with random client_order_ids (ALMU 12.10 against a 13.35 short, LEN 77.83 against 79.96).
- LEN IS WHAT SETTLES THE CAUSE. 28 shares of a $20bn homebuilder in its own primary-listing opening cross is not a name with 'no size in the auction', which is what this repo has said for a week off the thin-name rows. Running tally over all auction legs sent since 09-11: 10 legs, ONE full fill (ORCL 12/12), two partials (HOFT 17/161, CODA 39/183), seven zeros.
- ROOT CAUSE, from Alpaca's own documentation, checked 2026-09-18. (1) Its order-types page: 'OPG and CLS orders are only available to Elite Smart Router users.' This is an $11.5k paper account, not an Elite one, and nothing rejects the order at submission — it is accepted, sits, and is cancelled at a cross it never reached. (2) Paper fills are simulated against the NBBO quote stream, and eligible orders 'receive partial fills for a random size 10% of the time', which describes HOFT's 17 of 161 exactly. Either cause alone is sufficient; neither is separable without an Elite live account, and it does not matter which, because on THIS account an auction order is not an exit.
- FIX: placement and instrument are now separate. New `orders.auction_orders: false`. `exit_placement()` returns open/close/market from the mode; `exit_tif_for()` turns that into an instrument the account has. `amc_open` still aims amc at the open — it now gets there as a plain market DAY order submitted pre-market, which Alpaca accepts while the market is closed and routes at the next open. Exit records carry a `placement` field beside the tif.
- THE PASTED ROUTINE GUARD STILL EXITS 0, by design and not by luck. 'Close AMC' runs `mode --require-exit-tif opg`; a session cannot edit a Routine, so a guard failing shut would mean a correct-looking no-op every morning while the amc legs went unsold — the exact failure that guard replaced. `--require-exit-tif` now matches on the placement family and prints a NOTE saying so. Do not re-paste it to name the new tif.
- WHAT THE CHANGE COSTS: the +8.91% for an amc opening exit was priced at the 09:30 auction print; a queued market order fills at the NBBO seconds later, which is widest in exactly the thin names this book trades. Against an order that does not sell at all it is not a close comparison. Nothing about the ranking, the conviction floor or the book rule changes.
- STILL UNMEASURED ON THIS ACCOUNT: whether a queued pre-market DAY order fills at the open. Alpaca's docs say orders submitted while the market is closed are accepted and routed at the next open, and auction_window() has assumed it since 09-16, but this book has never sent one. I tried to settle it with a paired 1-share test (F, market/day against F, market/opg, both pre-market, same open) and the sandbox refused the order submission and every live account call. The test is written out in edge/EXECUTION.md for the operator to run in one morning.
- Verified offline: smoke_test.py passes (its exit-mode checks now assert PLACEMENT in every configuration and the instrument conditionally on auction_orders), and `mode --require-exit-tif opg` exits 0 against the shipped config. The close/verify paths could not be dry-run here — the sandbox blocked both.
## Close AMC — opg exit guard and sweep — 2026-09-18
- Logged at 2026-09-18 10:13 UTC
- Fired ~10:05 UTC (06:05 ET), well before the 09:28 ET opg cutoff. Re-read clock with date -u.
- Guard: python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg -> exit 0 (execution.enabled=true, exit_mode=amc_open, amc -> opg, bmo -> day). Proceeded.
- verify --scan 'research/*/*/*/edge' before any send: all 11 pre-existing exit legs (HOFT, FEIM, ORCL, RH, CODA, VRA, FPS, RLGT, LUXE, ALMU, LEN) report still held 0.0 — nothing UNFILLED, nothing to rescue.
- close --scan 'research/*/*/*/edge' --submit: no amc leg has an exit date of 2026-09-18, so no opg order was placed this run. The only leg due today is TRT (2026-09-17 entry, bmo, exit 2026-09-18) — sent as a day-tif market order per the amc_open instrument mapping (bmo -> day, not opg), client_order_id 66ee2f1a-aa2d-4d6d-acf5-714200e24ada, working/unfilled at report time (bmo exit does not cross at the open, so no fill expected yet).
- status --scan confirms: TRT is the only OPEN position (338 sh long, +0.36%), its exit order is 'new'/unsubmitted-fill, all other runs flat.
- Refusals: none. Account reachable throughout (paper, equity $11,541.63).
- No amc opg leg was placed today because none was due — this is a correct no-op for the opg instrument, not a guard failure. Left to stage E's own run and the next 'Close AMC' firing to pick up any future amc exit.

## Execution — today's Close AMC run is an accidental test of the new instrument, and exposes one policy gap
- Logged at 2026-09-18 10:15 UTC
- Merged origin/main (4d4bffe, the 10:13 UTC Close AMC publish) into this branch. Only conflict was this file; both sections kept in chronological order. smoke_test.py passes after the merge and `mode --require-exit-tif opg` still exits 0.
- THE TEST I COULD NOT RUN IS RUNNING ITSELF. The open question in the 09:34 entry was whether a queued pre-market DAY order actually fills at the open on this account — Alpaca's docs say orders submitted while the market is closed are accepted and routed at the next open, but this book had never sent one. This morning's Close AMC run sent exactly that: TRT 338 shares, market/day, submitted 10:07:11 UTC (06:07 ET), status `new` at the 10:12 verify. That is the same instrument the amc leg now uses. Read it back after 13:30 UTC: filled at or just after the opening print settles the question, still `new` or expired means the queued-market path does not work here and the exit has to move into the regular session.
- AND IT EXPOSES A POLICY GAP THAT PREDATES TODAY'S CHANGE. `amc_open` is specified as amc at the open, bmo at plain market on stage E's own run at 13:05 ET — that is the `amc_open_bmo_1300` policy edge_exit.py scores at +6.49% a trade, and the stated reason for choosing it over auction_split is that a bmo leg is CERTAINLY gone before the same afternoon buys the next book. But `close --scan --submit` takes every leg whose exit date is today, so the 06:05 ET Routine picked the bmo leg up too and TRT will exit at the OPEN, not at 13:05 ET. The Routine prompt has always said this may happen ('a bmo leg due today may go in here'), which was harmless under auction_split where bmo wanted `cls` and the pre-market run could not place one. Under amc_open the bmo instrument is a plain day order, so the earlier Routine simply takes it — and the book is being run on a policy nobody scored: amc at the open, bmo at the open. Measured, bmo at the opening auction paid +2.96% against +6.48% at the close and +2.58% at ~10:00 ET, so this is the weakest of the three for that session.
- NOT CHANGED HERE. It is a real deviation from the configured intent and the fix is one line in `close` (skip a leg whose placement is `market` when the run is outside market hours, leaving it for stage E), but it changes which session sells a live position and that is the operator's call, not a session's. Recorded so the next run does not read TRT's 06:07 ET exit as a defect in today's instrument change — it is not; the two are independent.
