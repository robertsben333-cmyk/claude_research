# Run log — 2026-09-16

## Stage 0 — universe (05:13 UTC)
- Logged at 2026-09-16 05:16 UTC
- Window: After the US close on Wednesday 16 September 2026 through before the US open on Thursday 17 September 2026
- Source: nasdaq (both sides), status ok, no fallback needed
- Universe: 4 total (3 AMC, 1 BMO); 2 above the $500M cap floor; 1 eligible after qualification
- Excluded: 3 (1 no_options_market: LEN.B — Class B has no listed-options chain, LEN Class A kept; 2 below_market_cap_floor: ALMU $229.5M, IPHA $206.6M)
- Notes: single-name day. Eligible count (1) is at or below triage.skip_if_universe_at_or_below (10), so stage 1 will skip and LEN goes straight to stage 2.

## Stage 1 — triage (06:39 UTC)
- Logged at 2026-09-16 06:39 UTC
- Mode: skipped (universe <= threshold of 10)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors -> 1 shortlisted
- Scouts: 0 subagents (screen skipped)
- Session mix: 1 AMC / 0 BMO
- Notable drops: none scored by triage (stage 0 already excluded LEN.B no_options_market, ALMU and IPHA below_market_cap_floor)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-16 08:22 UTC
- Shortlist: 1 name; this batch: LEN
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers, publish after each wave (single name = one wave of one)

## Stage 2 — deep dive, batch 1 — FINISHED (08:35 UTC)
- Logged at 2026-09-16 08:36 UTC
- Researched: LEN
- Skipped (already done): none
- Failed: none
- Subagents: 1 opus/high, in 1 wave of 1 (shortlist has only 1 eligible name today)
- Median evidence completeness: 82/100
- Panel-eligible after this batch: n/a — ranking deferred to final batch per skill step 4

## Close AMC — opening-auction exit — BLOCKED, no orders submitted
- Logged at 2026-09-16 10:08 UTC
- Step 1 guard as specified in the Routine prompt does not exist in this codebase: 'python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg' fails with argparse error (exit 2, unrecognized arguments). The 'mode' subcommand only supports '--require <MODE_NAME>' (uniform/bmo_close/auction_split), not an instrument/tif-based guard.
- Step 2 as specified also does not exist: 'alpaca_trade.py verify --scan ...' fails (exit 2, invalid choice 'verify'; valid subcommands are plan, open, flatten, close, status, assets, mode).
- The Routine prompt also references an 'amc_open' exit mode as having shipped 2026-09-15; grep of the full tree finds no such mode anywhere in edge/scripts/alpaca_trade.py (EXIT_MODES = uniform, bmo_close, auction_split only; 'amc_open' appears solely as part of 'amc_open_bmo_close', a label inside edge/scripts/edge_exit.py's analysis code, not an execution mode). This looks like the same class of drift CLAUDE.md documents for 2026-09-10 (a Routine prompt referencing code that lives on an unmerged branch) rather than a live feature on main.
- Per the Routine's own instruction ('do not substitute your own reading of config/pipeline.yaml for this command'; 'on a non-zero exit, do nothing further ... and stop'), no close order was submitted this run. Ran plain 'mode' (no flags, informational only, not used as the guard) and 'status' (read-only) instead to capture context.
- 'mode' reports: execution.enabled=true, orders.exit_mode=auction_split, exit instrument amc -> opg, bmo -> cls -- consistent with config/pipeline.yaml, but this was not treated as satisfying the specified exit-status guard.
- 'status' shows no amc leg is actually due into the opening auction today: LUXE (from 2026-09-15, exit_date 2026-09-16) is session=bmo, so its exit is a closing-auction (cls) order this Routine would not place before market open regardless.
- 'status' also surfaces an unrelated, pre-existing problem worth a human's attention: VRA and FPS (entered 2026-09-14, session=bmo, exit_date 2026-09-15) are still OPEN two days past their exit date -- VRA +40.14%, FPS +8.61% on paper. Their 2026-09-15 closing-auction exit orders both show 'expired filled 0' (0 shares sold). RLGT from the same batch (amc) resolved and is no longer open.
- Recommend a human: (1) check whether edge/scripts/alpaca_trade.py is missing a 'verify' subcommand and a 'mode --require-exit-tif' flag that a newer version of the Routine prompt assumes, or whether the prompt was pasted from a draft never merged to main; (2) decide how VRA and FPS (2 days overdue, unresolved) should be closed -- they were not touched by this run.

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-16 10:23 UTC
- Shortlist: 1 name (LEN); this batch: none — capped_len=1, N=ceil(1/2)=1, batch 1 took position 1..1, batch 2 covers 2..end which is empty
- Already on disk, skipping: LEN (both .md and .json present from batch 1)
- Plan: no researchers to spawn this batch; proceed straight to final-batch ranking (step 4) over the day's one dossier

## Stage 2 — deep dive, batch 2 — FINISHED (10:24 UTC)
- Logged at 2026-09-16 10:24 UTC
- Researched: none (batch 2 range was empty — shortlist has only 1 name, fully covered by batch 1)
- Skipped (already done): LEN
- Failed: none
- Subagents: 0 opus/high, 0 waves — no researcher spawned this batch
- Median evidence completeness: 82/100 (LEN, the day's only dossier)
- Panel-eligible after this batch: LEN

## Stage 3 — panel & advice — STARTED
- Logged at 2026-09-16 16:02 UTC
- Panelling LEN only (top_n_for_panel=[LEN]; config panel.names=2 but only one name panel-eligible, not a budget degrade). 7/7 persona seats filled, no retries needed. Panel synthesized: Lean Down, consensus -25.7, disparity 12.5 (aligned), certainty High (91.2).

## Stage 3 — panel & advice (16:20 UTC)
- Logged at 2026-09-16 16:04 UTC
- Panelled: LEN
- Calls: LEN Lean Down -1.4% (High certainty, P(down) 59.5%)
- Panel seats filled: 7/7, no retries needed
- Chair overrides: none (noted, not overridden: 5/7 personas cited the same Ortex positioning article as a secondary source for reversal-risk data; primary directional drivers were independently sourced)
- Degradations: none (config asks for top 2 names; only 1 was panel-eligible today, not a budget shortfall)

## Edge hunt — 2026-09-16 amc + 2026-09-17 bmo — STARTED
- Logged at 2026-09-16 17:06 UTC
- Session fired 17:04 UTC (13:04 ET). Window resolves 4 of 37 calendar rows: LEN, LEN.B (2026-09-16 amc), ALMU (2026-09-16 amc), IPHA (2026-09-17 bmo). No --include-unknown. Under the cap of 20 (1 sweep + 4 hunters), no shedding.
- Step 0b exit: execution.enabled is TRUE and orders.exit_mode is auction_split, so the flatten is wrong and 'close --scan' ran instead. Sold: LUXE (2026-09-15 book, bmo) 292 sh into today's CLOSING auction (cls), order b0c56188-0f95-49d8-a416-ede78c3fbd88 accepted, unrealised +24.31% on a 7.20 entry at the time of submission. That was the only open position; the 09-10, 09-11 and 09-14 books were already flat. Account: paper, equity $11,236.08, cash $8,622.68.
- Baselines sealed BEFORE any agent launched: 4 of 4 written, all status ok. LEN has a live option chain (event-implied 6.33%, skew -0.77, OI 47,283); LEN.B, ALMU and IPHA — ALMU shows a straddle print at 13.46% but the file's expected_move_basis needs checking; the others fall back to a historical median. IPHA carries event_plausibility.verdict=unknown with cadence_implausible: true — an 8-day inferred cadence from 6-K operational filings, not earnings — so its 8 recorded reactions are NOT an earnings base rate and its hunter will be told so explicitly.
- Tree note: edge/LESSONS.md does not exist in the repo and no agent definition references it, contrary to the Routine prompt, which says each hunter reads it and that 'its definition says so'. Nothing was substituted. The Routine prompt is also stale on the clock (it says 14:04 UTC / 10:04 ET; the Routine now fires 17:04 UTC / 13:04 ET) — replacement text is in edge/routine-prompts/edge-hunt.md, waiting to be pasted by a person; update_trigger refuses any Routine an agent did not create.

## Edge hunt — 2026-09-16 — sweep
- Logged at 2026-09-16 17:10 UTC
- One edge-sweep agent over all 4 names. Result: 4 confirmed, 0 phantom, 0 sessions unsettled — every date and hour company-sourced. hunt_priority: ALMU 78, LEN 63, IPHA 52, LEN.B 38.
- LEN and LEN.B are ONE event: two share classes of one issuer releasing one set of Q3 FY2026 results after the close on 09-16 (call 09-17 11:00 ET). They are hunted separately because the room for an unpriced finding differs (LEN.B is thin and index-excluded), but they are not two independent observations of the fundamentals and the note says so. The sweep also caught an aggregator preview claiming LEN 'reports September 17 during market hours' — the company release governs and the row stays amc 09-16.
- IPHA is confirmed but is NOT a quarterly earnings print: Innate Pharma's own 2026 financial calendar schedules HALF-YEAR statements on 2026-09-17, released before the CET open with the call at 14:00 CEST / 08:00 EDT, so bmo 09-17 is right. The sweep set baseline_history_trustworthy: false — the baseline's eight 'prior prints' on an inferred 8-day cadence are 6-K text matches (the 2026-08-10 +28.3% move is almost certainly a news event, not a results reaction), so median_abs_move 2.97% and the 3-up-of-8 base rate are not an earnings prior. Its hunter was told this explicitly. edge_baseline_amend.py dry run proposed nothing; the baselines stand exactly as sealed.
- Free control (-run_up_20d_pct, off the sealed baseline before any agent spawned): LEN +5.86, LEN.B +6.01, IPHA +6.28, ALMU +16.77. Turnover (spot x avg_volume_20d): LEN $235.9m/day, LEN.B $6.59m, ALMU $6.17m, IPHA $48.5k — IPHA is already below the $200k benchmark floor and cannot be traded whatever it ranks.

## Edge hunt — 2026-09-16 — hunts, score, note
- Logged at 2026-09-16 17:25 UTC
- 4 hunters, one per confirmed name, 11 findings. impact_sum: LEN.B +0.00 (0 findings, a researched zero), IPHA -2.20 (4), LEN -3.00 (4), ALMU -5.00 (3). 4 of 4 rankable; 2 clear the conviction floor of 3.0 (LEN, ALMU), both negative and both tradable. Sign balance 3 negative / 1 zero / 0 positive.
- The free control DISAGREES with the hunt almost completely. -run_up_20d_pct ranks the day ALMU +16.77, IPHA +6.28, LEN.B +6.01, LEN +5.86; the hunt ranks it LEN.B, IPHA, LEN, ALMU. Spearman between the two orders is -0.40, and the name they disagree about hardest is the hunt's most convicted one. The stage has still not been shown to beat that free number.
- LEN.B ranks FIRST on a +0.00. It is a researched zero, not an absent hunt — 30 sessions of A/B discount measured, buyback by class, Section 16, index calendar, the defeated dual-class proposal, all empty. A zero sorts above every negative name by construction and the note says so. Its hunter also refuted the sweep row it was handed (the A/B discount is 1.54-2.20%, sd 0.18pp, NOT 'wide and mean-reverting' — that framing traces to a 2018 piece) and flagged that LEN.B's own baseline expected_move_pct of 3.69% and deadband 1.84% are stale-regime artefacts understating this print by ~40%.
- LEN and LEN.B are ONE event. Treat this day as three independent events, not four; edge_resolve.py will double-count the Lennar print unless told otherwise.
- Baseline caveats found by the hunters, both worth carrying forward: (1) LEN's 6.33% event-implied move is CONTAMINATED — the 2026-09-18 straddle it was struck from also spans today's 14:00 ET FOMC decision and dot plot and 08:30 ET August housing starts on 09-17, so three events sit in one option and any normalisation by it understates the reaction. (2) IPHA's sealed spot of 1.94 is a MID-SESSION snapshot taken at 17:06 UTC while the session was open, although last_close_date reads 2026-09-16; an independent quote at 13:08 ET was 1.97, +5.91% on ~3x normal volume with no sourceable cause. ALMU's chain is unreadable (ATM spread 56% of mid on 3,305 OI) so its 13.05% implied move is indicative only. Only LEN has a measured baseline; LEN.B and IPHA have no options market at all.
- Agent-definition drift against the Routine prompt, both recorded rather than worked around: no hunt returned print_vs_bar_pct, because .claude/agents/unpriced-hunter.md in this tree does not ask for it and edge_score.py does not read it; and edge/LESSONS.md does not exist in the repo, so no hunter read it and none was told to. Nothing was substituted for either. The prompt is also stale on the clock (says 14:04 UTC / 10:04 ET; the Routine fires 17:04 UTC / 13:04 ET). Replacement text is in edge/routine-prompts/edge-hunt.md and only a person can paste it.
- No adversary pass, per the skill. Nothing checked any finding for being factually wrong. The only checks that happened were the hunters' own: IPHA's hunter caught and discarded a bogus '+17.74% today' price row that was an unclosed-session artefact, and LEN.B's hunter refuted its own sweep row.

## Edge hunt — 2026-09-16 — execution
- Logged at 2026-09-16 17:26 UTC
- EXECUTION WAS ON. execution.enabled: true, paper endpoint, orders.exit_mode auction_split, flatten_before_entry false. This was not a dry run.
- Step 0b (sell), run first at 17:06 UTC before any agent launched: exit_mode is auction_split so 'close --scan' ran instead of 'flatten'. LUXE (2026-09-15 book, bmo, 292 sh from a 7.20 entry) sent into today's CLOSING auction as cls, order b0c56188-0f95-49d8-a416-ede78c3fbd88, unrealised +24.31% at submission. It was the only open position; the 09-10, 09-11 and 09-14 books were already flat. Account at that moment: equity $11,236.08, cash $8,622.68.
- Step 7 (buy), at 17:26 UTC with 154 minutes to the close. 2 of 4 names met the benchmark (|impact_sum| >= 3.0, turnover >= $0.2m, shortable): ALMU and LEN. Both SHORT — the book is short-only, because the positive end of today's ranking is a researched zero. Equal weight, both capped at the 20%-of-equity per-name limit: ALMU 167 sh, LEN 28 sh, ~$2,240 each, gross $4,484 = 39.8% of $11,262 equity. Under-deployed on purpose: with two names the per-name cap binds before the 100% gross target, which is the cap doing its job.
- 2 orders sent, 2 accepted, 2 FILLED: ALMU sell 167 @ 13.35, LEN sell 28 @ 79.96. Fill quality is clean — execution cost against the mid at submission was +0.336% for ALMU and +0.212% for LEN, each EXACTLY its own half-spread, mean +0.274%. That is crossing the spread and nothing more, so there is no case here for moving orders.entry back to market_on_close. Exit date 2026-09-17 for both; both are amc, so under auction_split they exit into tomorrow's OPENING auction via the 'Close AMC' Routine.
- Names refused, with reasons: LEN.B — below the conviction floor (0.00 < 3.00). IPHA — below the conviction floor (2.20 < 3.00), and it would have been refused anyway at $48.5k/day of turnover against the $200k floor. No name was hand-picked in and nothing was sized by its score.
- The free control disagrees with BOTH traded positions: -run_up_20d_pct is +16.8 for ALMU and +5.9 for LEN, so it would be long both names the hunt is short. 0 of 2 agreement. Over six resolved runs that control ranked at rho=0.335 against the hunt's raw 0.407 with a CI spanning zero, and it was positive on 6 of 6 days when traded. This book is a bet against it.
- One macro overlap worth recording for whoever resolves 09-16: today's 14:00 ET FOMC decision and dot plot land BEFORE tonight's amc prints, and August housing starts print 08:30 ET on 09-17 before the exit auction. Both traded names are housing-adjacent in the case of LEN and the option anchor for LEN spans all three events.

## Maintenance — two unmerged 2026-09-15 branches merged
- Logged at 2026-09-16 18:45 UTC
- Both defects the 09-16 runs recorded were missing merges, not agent or code bugs. claude/optimistic-hypatia-5qvags held edge/LESSONS.md and the hunter contract returning print_vs_bar_pct; claude/alpaca-sell-orders-filling-mwumuw held the verify subcommand, mode --require-exit-tif, the fill check and exit_mode amc_open. Both merged to claude/youthful-johnson-aius7n.
- Close AMC is unblocked: 'python3 edge/scripts/alpaca_trade.py mode --require-exit-tif opg' now exits 0 (amc -> opg, bmo -> day). exit_mode is amc_open, flatten_before_entry false, execution.enabled true.
- New this session: edge/LESSONS.md is itself scored. The hunter sizes the day with the baseline alone, freezes pre_lessons, then reads the file and revises; edge_score.py carries diagnostics.impact_sum_pre_lessons and flags a hunt with no draft, edge_resolve.py reports spearman_pre_lessons per day and pooled. The file can no longer steer a search, only a size and a selection - that is the price of measuring it.
- New this session: one issuer is one event. edge/scripts/share_class.py folds a second share class into its issuer in edge_universe.py before baselines are sealed, and edge_score.py drops it from the ranking if a run reaches it with both. Re-scored today's run: LEN.B leaves the ranking with its hunt intact, LEN/ALMU/IPHA unchanged. Today's published edge-scores.json was NOT rewritten.
- Still needs a person: the stage E Routine prompt and the Close AMC prompt both need re-pasting from edge/routine-prompts/. The stage E block now carries the 17:04 UTC clock with its entry margin, the pre_lessons sentence in step 4, the share-class line and the amc_open step 0b. update_trigger refuses any Routine an agent did not create.
- Unchecked: the 09-15 LUXE exit reads 'canceled, filled 0' while the position is no longer held. The fill-verification pass merged today is what would have caught that inside the session.
- scripts/smoke_test.py is green again. Its two exit-mode assertions had failed since 2026-09-11 and now check the flatten/mode pairing and membership of at.EXIT_MODES.
## Edge hunt — 2026-09-16 — CORRECTION to the 'stale prompt' finding above
- Logged at 2026-09-16 18:33 UTC
- The earlier entry has the direction wrong. The Routine prompt is NOT stale on edge/LESSONS.md or print_vs_bar_pct — it is written against branch origin/claude/optimistic-hypatia-5qvags, which is unmerged, and the TREE is behind the prompt. That branch changes 14 files, not one: edge/LESSONS.md plus .claude/agents/unpriced-hunter.md and edge-sweep.md, the skill, edge_score.py, edge_resolve.py, alpaca_trade.py, config/pipeline.yaml and a new edge/scripts/edge_postmortem.py. It is a contract change, not a document. (The clock discrepancy in the prompt — 14:04 UTC stated, 17:04 actual — is separate and IS stale.)
- What the merge would add to the hunter contract: print_vs_bar_pct (what will the NUMBER be, separately from what the STOCK does), lands_on, resolves_by, positioning_check, and an outside_window array. Only the last touches the key, and it does so at the hunter, not the scorer: impact_sum stays the sum of findings[].expected_impact_pct, and a finding resolving after the exit window goes in outside_window instead of findings.
- Applied by hand to today's four hunt files, for whoever resolves this day. IPHA: its +1.5 PACIFIC-9 leg has a registry primary-completion date of 2026-09-30, thirteen days past the exit, so lesson 6 moves it to outside_window and IPHA goes -2.20 -> -3.70, CROSSING the 3.0 floor; but lesson 3 also bites, because that hunter's own independence field says findings 1 and 2 are one document read two ways, and collapsing them gives -2.50. Net: -2.5 to -3.7, indeterminate on the floor. ALMU: lesson 8 is a direct hit — the hunter sized -5.0 explicitly 'well inside the 7.79% median historical reaction' on a 2-4 analyst name with a confirmed unpriced company number, which is the exact understatement lesson 8 names; sized on the name's own reaction distribution it is nearer -7 to -8. Offset by lesson 7, which it could not satisfy (short interest irreconcilable between sources, left out). LEN: largely survives — it already sourced the bar three ways, dropped a finding that argued against itself, and shrank for a crowded short. LEN.B: a zero with no findings; nothing to move.
- Effect on the ranking: LEN and IPHA may swap places in the middle; the top and bottom rows are unchanged. Effect on the BOOK: none. ALMU and LEN are short either way, LEN.B is a zero, and IPHA cannot be traded at $48.5k/day whether or not it clears the floor. The branch's execution changes are reporting-only (a 'thin' flag at $1m/day that drops nothing, and a non-lendable short reading 'elsewhere' rather than 'no'); both of today's shorts were lendable at Alpaca.
- Recommended merge order, not carried out by this session: merge AFTER the 'Close AMC' Routine has flattened the 09-17 exits, so that no position is opened under one hunter contract and closed under another.

## Maintenance — note on the two entries above
- Logged at 2026-09-16 19:05 UTC
- The two sessions reached the same diagnosis independently and the entries are both kept, in the order they were written. The merge the correction recommends holding is already done on `claude/youthful-johnson-aius7n`; it is NOT on `main`, so nothing a Routine clones has changed yet.
- The recommended order (merge after Close AMC flattens the 09-17 exits) cuts against the second branch: the Close AMC prompt guards on `mode --require-exit-tif opg`, which does not exist in main's `alpaca_trade.py`, so on main that Routine fails again at 10:00 UTC on 09-17, submits nothing, and ALMU and LEN are picked up as overdue at market by stage E's own 17:04 run instead of going into the opening auction. Landing the merge on main BEFORE 10:00 UTC is what makes the chosen exit reachable; landing it after keeps the contract clean but repeats the blocked run. Whoever merges should pick deliberately, not by whichever entry they read first.

## Maintenance — the merge is on main
- Logged at 2026-09-16 22:21 UTC
- Pushed to main on the operator's explicit go-ahead. main is now f12310bd; the two entries above that say the merge is only on claude/youthful-johnson-aius7n are superseded by this line.
- Live from the next clone: edge/LESSONS.md and the pre_lessons contract, edge/scripts/share_class.py, the verify subcommand and mode --require-exit-tif, and exit_mode: amc_open with flatten_before_entry false.
- The merge landed BEFORE the 10:00 UTC Close AMC run of 09-17, deliberately: on main's previous tree that Routine's guard failed with an argparse error and submitted nothing, so ALMU and LEN would have missed the opening auction and been sold as overdue at market in the afternoon. The competing recommendation (merge after the 09-17 exits, to keep one hunter contract per position) was read and set aside; the same entry judged the book effect to be none.
- Unchanged and still needing a person: both Routine prompts must be re-pasted from edge/routine-prompts/. Until then the stage E prompt still states 14:04 UTC and the Close AMC prompt still names the old hand-read guard.
