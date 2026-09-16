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
