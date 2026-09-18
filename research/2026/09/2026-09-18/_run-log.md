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

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-18 10:24 UTC
- Shortlist: 0 names (triage_mode: skipped_small_universe, universe_eligible: 0, universe_total: 0); this batch: none
- Already on disk, skipping: none (02-dossiers/ empty, confirmed on disk not just from batch 1's log)
- Batch 1 already confirmed and published this empty state (08:24 UTC) and covers the day; nothing to add for batch 2
- Plan: no researchers to spawn; writing 02-ranking.json empty as final batch, since stage 3 reads it and does not re-derive it

## Stage 2 — deep dive, batch 2 — FINISHED
- Logged at 2026-09-18 10:24 UTC
- Researched: none (shortlist empty)
- Skipped (already done): none
- Failed: none
- Subagents: 0 opus/high, 0 waves
- Median evidence completeness: n/a
- Wrote 02-ranking.json: 0 names, top_n_for_panel: [] -- confirmed empty state directly (00-universe.json, 01-shortlist.json, 02-dossiers/ on disk), not just from batch 1's log
- Panel-eligible after this batch: none
## Execution — close no longer sells a bmo leg from the pre-market run
- Logged at 2026-09-18 10:25 UTC
- Follow-up to the 10:30 UTC entry, on the operator's instruction to fix it rather than record it. `close` takes every leg whose exit date is today and two runs a day call it (Close AMC 06:05 ET, stage E 13:05 ET), so the early run was taking the bmo leg as well. Harmless under auction_split — bmo wanted `cls` and window_for('cls') refuses a closed market — and live under amc_open, where the bmo instrument is a plain DAY order that Alpaca QUEUES FOR THE OPEN.
- RULE: `defer_to_session_run(placement, overdue, session_open)`. A leg whose placement is not `open` is left to the run that fires inside the session; it is recorded as not-sent with the reason 'market placement, and the market is closed'. Two exemptions, both deliberate: an OVERDUE leg still goes immediately (its event is over, and queueing it for the open beats another seven hours of exposure on the chance the later run fires), and nothing is deferred when the clock could not be read (session_open None) — an unknown clock must not become the reason a position goes unsold. A not-sent record does not block a later retry: `close` counts only prior exits with submitted true.
- COST, stated: if stage E's own run then dies, the bmo leg is held overnight instead of having been sold at the open by accident. The overdue rule is the net — it goes at market on the next run either way, and `open` refuses to buy a new book over it.
- TODAY'S TRT ORDER IS NOT CANCELLED, on purpose and it is a judgement call. It was already queued at 06:07 ET before this rule existed, and cancelling it would destroy the one thing this account has never measured: whether a queued pre-market DAY order fills at the open. That is the instrument the amc leg now depends on. One bmo trade exiting at the open rather than 13:05 ET is the price of the measurement, and the expected gap on a single name is small against an unverified assumption sitting under every future amc exit. Read it back after 13:30 UTC.
- Verified: smoke_test.py passes with four new checks over the rule (market leg deferred, open leg not deferred, overdue never deferred, unreadable clock never defers). The close path itself could not be dry-run — the sandbox blocks live account calls from this session.

## Research sample — TRT removed from 2026-09-17: the print never happened
- Logged at 2026-09-18 15:05 UTC
- The operator flagged that TRT did not in fact report. Verified against EDGAR CIK 0000732026 on 2026-09-18: the most recent item-2.02 8-K is still 2026-05-14, and the three filings dated 2026-09-15 are CERT / Form 25 / 8-A12B -- an exchange listing transfer, not a results release. The 2026-09-18 bmo row was a phantom.
- MECHANISM, and it is new: baselines can now carry `event_occurred: false` plus an `event_occurred_note` holding the source that establishes the absence. edge_score.py checks it AHEAD of every other rankable test, because it is the only one settled by the outcome rather than predicted before it. TRT's sealed baseline carries it; edge-scores.json for 2026-09-17 was regenerated and now reads 1 of 2 rankable, UPXI only, and ZERO names clearing the 3.0 floor.
- THE TRADE IS NOT RETRACTED. 338 shares went in at 19:58 UTC on 09-17 and the exit ran this morning. That is a real position with a real P&L and alpaca-orders.json is its record. A trade on a phantom event is a fact about execution; it is not a data point about whether earnings reactions can be ranked, and the two must not be netted.
- WHAT IT COSTS THE RECOVERY STORY. The 09-17 note argues the operator was right to overturn sweep 2's refutation of TRT, and on the evidence available that day the reasoning still reads correctly -- 127 days against a 90-day cadence, and the 2025-09-19 precedent the sweep missed was real. It was still the wrong answer. The sweep said 09-22 and was nearer the truth than the hand check that overruled it. The cadence prior is a prior; it is not evidence that a print exists, and on 09-17 it was read as evidence and 33% of equity followed.
- CORRECTED IN THREE PLACES: a correction banner at the top of research/2026/09/2026-09-17/edge/edge-note.md (the body is left as the record of what was believed), the time-not-supplied paragraph in CLAUDE.md (phantom rate for that window goes from 19 of 20 to 20 of 20, and session_resolve.py's 0-of-20 result was correct about all twenty), and this log. smoke_test.py passes.

## Dashboard — a research register for stage E, and a sample three times the size
- Logged at 2026-09-18 15:33 UTC
- THE SAMPLE WAS STUCK AND NOBODY NOTICED. edge_decompose.py reads edge_score, edge_pct, confidence and baseline_quality off each ranked row. Those left the top level of edge-scores.json on 2026-09-09 when impact_sum became the key, so it has raised KeyError on every run since, and every number in edge/EDGE_ANALYSIS.md still rests on the first six days -- 43 names, 38 de-duplicated. Seven run days were on disk and in no sample.
- edge/scripts/edge_sample.py reads the fields BOTH schemas carry: 106 resolved, de-duplicated events over 13 hunt days, 55 above the conviction floor. impact_sum is summed from findings for pre-09-09 runs, which is the definition of the field rather than a reconstruction -- all 38 rows of the existing edge-rows.json reproduce to 3 decimals. Scope is stage E only: research/*/*/*/edge, nothing from stages 0-4, claude_naive or backtest, and the 08-31 legacy_rescore run is skipped.
- QUESTION 1 (edge_runup.py) -- does the 2/5/10/20-session return to 20:00 CET predict whether the hunt's sign was right? NO. Largest |rho| 0.153, smallest p 0.117, hit rate by run-up tercile flat in a 49-57% band. Not a weak signal needing more days; the shape of nothing.
- QUESTION 2 -- does agreement between run-up and prediction pay? NOT ON THE TRADED BOOK. Over all names the 2d window looks helpful (+2.55% agree against -1.12% disagree); above the conviction floor it INVERTS at all four windows (10d: +0.71% agree against +5.75% disagree). Two subsets of the same data pointing opposite ways, with fully overlapping day-bootstrap intervals, are noise measured twice. Sixteen cells were looked at.
- QUESTION 3 (edge_entry_clock.py) -- is 20:00 CET the right entry, or is later better? IT DOES NOT MATTER. Exit held fixed, entry swept 10:00-16:00 ET in half hours: the best and worst entry of the whole session differ by 0.40pp on the conviction book, against a per-trade sd of 15. The close is nominally best (+3.59% against +3.37% at 20:00 CET). No intraday drift to time either -- no t above 1.6 on the unsigned drift-to-close. amc wants early and bmo wants late, the same shape as the exit finding, but on 28 and 27 events with the best hour chosen after reading the chart. What is NOT measured is the spread, which is the only argument for entering later.
- QUESTION 4 (edge_search_volume.py) -- Google Trends daily interest, US, 90 days to the entry day, one fixed query per company (registered name minus the legal suffix, never the ticker). THE ONLY ONE THAT IS NOT EMPTY. Above the floor, spike_day ranks at rho -0.504, permutation p 0.018 on 22 events: MORE search attention, WORSE outcome. Lowest spike tercile +10.76% on 6 of 7, highest -1.17% on 4 of 8, and the high-spike names also move least (median 4.67% against 10.08%). p is 0.18 after Bonferroni over the ten cells looked at.
- AND THE FIRST RUN OF THAT SCRIPT WAS WRONG, which is written into the page rather than quietly fixed. Each Trends series is normalised to its OWN maximum, so a name searched on three of ninety days reads 0,0,...,100 and a spike over a zero median comes out at 100x. Eleven such names filled the top tercile. measures() now rejects a series with a zero median -- fewer than half the days carrying interest -- as unusable. That takes the sample from 95 'measurable' to 47 real ones, and the survivors are systematically the LIQUID half: median turnover $22.7m against $1.4m for the dropped ones. So this correlation says nothing about the half of the book this stage most often trades.
- A CONTROL THAT HAS BEEN LOAD-BEARING JUST MOVED. Minus the 20-day run-up ranks the first six days at rho 0.335 and was 6 of 6 positive when traded; on these 105 events it returns -0.42% per trade. The comparison that does survive: the hunt above the floor +3.37% per trade against +1.59% for shorting every name with no research at all.
- DELIVERABLE: edge/scripts/edge_dashboard.py generates edge/analysis/dashboard/{index,runup,entry-clock,search-volume,calendar}.html from the analysis JSON. Generated, never hand-edited, so a page cannot drift from the run that measured it. Published at https://claude.ai/artifact/JjEfQYMhb1UN25SCGp4SK3 . Also edge_calendar.py: the forward week with the session and liquidity gates both applied -- 80 calendar rows to 2026-09-25, 25 with a confirmed session, 22 clearing the $200k floor.
- Verified: smoke_test.py passes. The chart palette was run through the dataviz validator against both surfaces before use (all checks pass; light aqua sits under 3:1, so every series is direct-labelled and every chart has a table beside it).

## Stage 3 — panel & advice (15:56 UTC)
- Logged at 2026-09-18 15:56 UTC
- - Panelled: none — 02-ranking.json sealed top_n_for_panel: [] (stage 0 universe was 0 eligible, cascaded through stage 1 skip and both stage 2 batches)
- - Calls: none
- - Panel seats filled: 0/0 (no names to panel)
- - Chair overrides: none
- - Degradations: none (empty universe made the panel budget moot, not exceeded)
- - Wrote 04-advice.md/.json with status: no_names, ranked_names: []; validated with validate_stage.py advice
## Dashboard — the main dashboard was an unmerged branch; merged, moved to dashboard/, four tabs added
- Logged at 2026-09-18 15:59 UTC
- THE MAIN DASHBOARD EXISTED AND WAS UNMERGED. Earlier today this session searched the repo and the git history, found only two standalone HTML files, and told the operator there was no dashboard. That was wrong in the way CLAUDE.md already warns about twice: the thing was on `claude/epic-ride-s4bcg4`, four commits, never merged. A git-history search that only looks at `main` cannot see an unmerged branch -- check `git branch -r` before concluding something does not exist.
- MERGED, AND MOVED TO THE TOP LEVEL. `edge/performance/` is now `dashboard/`, on the operator's instruction that the file you open should be easy to find. Paths fixed in update.sh, the three scripts (parents[3] -> parents[2]), the skill, scripts/publish.sh, .gitignore, CLAUDE.md and edge/README.md. Nothing about the build changed beyond the paths; ./dashboard/update.sh --offline runs clean end to end.
- FOUR NEW TABS, recomputed client-side from the filtered rows like everything else on that page, so they move with the lens, the exit horizon, the threshold, the period, the session and the sector.
-   Instap -- the ENTRY side of the clock. The existing Timing tab moves the exit with the entry fixed at the 22:00 CET close; this moves the entry with the exit fixed at whichever horizon is selected. New per-name field `enpx`, the entry-day price at every half hour of the regular session, computed by build_ledger.py from the bars it already fetches so there is ONE price source. Answer: it does not matter. About half a point between the best and worst entry of six hours against a per-name sd near 13, and the unsigned drift to the close is flat at every hour.
-   Aanloop -- new fields runup_2d/5d/10d/20d, measured to the 20:00 CET bar and NOT to the close, because the two hours after it are on the wrong side of the decision they are supposed to inform. Neither question returns anything: no |rho| above 0.07 against whether the sign was right, and the agreement result flips sign between the full sample and the traded book. The tab says that where the reader is, and tells them to toggle the drempel control and watch the last column change sign.
-   Zoekvolume -- new fields search_spike, search_level, search_state, attached from edge_search_volume.py's own output rather than recomputed, because that script owns the query rule and the test that throws a series away. The one lead in the set: above the conviction floor a bigger search spike goes with a worse outcome, and the high-attention names also move least. One cell of ten looked at, and half the book is below Google's reporting threshold, so the measurable half is the liquid half.
-   Agenda -- the forward week from edge_calendar.py, session gate and liquidity floor counted separately so the candidate count is honest. The ledger drops it once it is more than three days old: a stale list of what is coming is a list of what already came.
- update.sh now runs both feeders before the ledger (search volume, calendar). Either may fail without costing the rebuild, and --no-feeders skips them. The ledger records a missing feeder as a problem rather than as a zero.
- DELETED: edge/analysis/dashboard/ and edge/scripts/edge_dashboard.py, the standalone pages built earlier today. The content is in the tabs above; two renderers over one dataset is exactly the drift this repo keeps paying for. The published artifact JjEfQYMhb1UN25SCGp4SK3 is a dated snapshot of that interim version and is not maintained.
- ONE CAPTION WAS WRONG AND IS FIXED. The Zoekvolume tab claimed the pooled rank correlation of search spike against |move| supported 'high-attention names move less'. It does not -- that rho is +0.006. The tercile table does show it (4.60% median against 9.74%), so the effect is in the tails and not monotonic, and the caption now says exactly that instead.
- Verified: smoke_test.py passes; ./dashboard/update.sh --offline rebuilds ledger and page; the page renders in a headless browser with no JS errors and all 23 calendar rows present.
