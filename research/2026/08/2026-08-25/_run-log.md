# Run log — 2026-08-25

## Stage 0 — universe (07:19 CEST)
- Window: After the US close on Tuesday 25 August 2026 through before the US open on Wednesday 26 August 2026
- Source: nasdaq (after-close and before-open feeds both `ok`, no network block, no fallback needed)
- Universe: 33 total (14 AMC, 19 BMO); 26 above the $500,000,000 market-cap floor; 23 eligible after qualification
- Excluded: 10 total — 7 below_market_cap_floor (DSC $0.43B, STRT $0.34B, ELMD $0.33B, ZH $0.29B, QMLS $0.19B, LANV $0.13B, LITB $0.06B); 3 additional manual exclusions:
  - `HEI.A` — duplicate_share_class: Heico's Class A shares reporting the same earnings event already captured by `HEI`, kept out to avoid double-counting one event downstream.
  - `FSCO` — no_options_market: FS Credit Opportunities Corp (closed-end BDC fund). Nasdaq's option-chain page returned no data and no other platform (Yahoo, Barchart, OptionCharts) showed a live chain for it.
  - `HDL` — no_options_market: Super Hi International Holding (Nasdaq ADS, IPO'd Dec 2024). Same "no data" signal on Nasdaq's option-chain page with no confirmation elsewhere.
- Qualification checks: options-market status for smaller-cap/foreign-ADR/fund names verified via WebSearch rather than assumed — `JOYY`, `TRMD`, `SFL`, `TIGR`, `QFIN`, `JKS` all confirmed to have active listed-options chains across multiple platforms (Nasdaq, Yahoo Finance, Barchart, Investing.com, OptionCharts, Benzinga, Moomoo). Established large/mid-cap US names (`INTU`, `HEI`, `ZM`, `WSM`, `SJM`, `LI`, `DY`, `SMTC`, `DCI`, `ANF`, `BOX`, `BBWI`, `NCNO`, `KSS`, `PLAB`, `MOV`) and long-listed liquid ADR `NOAH` were treated as eligible by inspection, consistent with prior days' practice for well-known optionable names. BMO/AMC session and event date came from a single source (nasdaq calendar via `get_earnings.py`) for every name; no second-source cross-check was run given the size of the eligible set (23) — no conflicting timing was surfaced, so nothing was dropped under `unconfirmed_timing`, but this stage's timing confidence should be read as single-sourced, not cross-verified.
- Notes: `get_earnings.py` returned status `ok` on the first attempt (exit 0). This is a catch-up-style observation, not a stage-0 action item: the pipeline's last completed stage-2 activity on `main` is "stage 2 batch 1: STARTED for 2026-08-21 (PDD, XPEV)" — no stage-0/1/2/3/4 output appears on `main` for 2026-08-22 through 2026-08-24. Flagging here for whoever runs the next stage/triage, since it may be worth investigating separately; out of scope for this stage-0 run. Eligible count (23) exceeds `triage.skip_if_universe_at_or_below` (10), so stage 1 (triage) will run normally today.

## Stage 1 — triage (07:52 CEST)
- Mode: scouted (universe eligible 23 > skip threshold 10)
- Funnel: 33 universe -> 23 eligible -> 21 cleared floors -> 6 shortlisted
- Scouts: 2 subagents (sonnet/medium), batches of 15 and 8
- Session mix: 3 AMC / 3 BMO
- Dropped for floors (2): SJM (change_expectation=30 < 35, packaged-foods grinder,
  guidance-driven not print-driven), DCI (change_expectation=28 < 35, filtration
  industrial, guidance already given, efficiently covered)
- Notable drops above the floors but outside the top 6: WSM (priority_score=63.25,
  exact 3-way tie with NCNO/QFIN for the last slots; cut to balance session mix — the
  top 4 by score were already 3 BMO/1 AMC), JOYY (ai_edge=30, exactly at the floor —
  opaque VIE disclosure limits how much synthesis can add despite being a likely mover)
- Carry-forward note from stage 0: no stage output appears on `main` for
  2026-08-22 through 2026-08-24 (gap between "stage 1: shortlist for 2026-08-21"
  and today's stage 0). Not a stage-1 blocker, but stage 2/3 owners should be aware
  the pipeline had a multi-day silent gap before today.
