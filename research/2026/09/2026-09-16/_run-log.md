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
