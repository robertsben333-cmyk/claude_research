# Run log — 2026-08-08

## Stage 0 — universe (11:36 CET)
- Window: After the US close on Saturday 08 August 2026 through before the US open on Monday 10 August 2026
- Source: nasdaq (both after-close and before-open sides; single source, no network block)
- Universe: 48 total (0 AMC, 48 BMO); 27 eligible after qualification
- Excluded: 21 (below_market_cap_floor: 21)
- Notes: Reference date (2026-08-08, Saturday) is not a trading day; `get_earnings.py`
  correctly rolled the window to the next open (Monday 2026-08-10) and reported empty
  after-close as expected for a weekend. Qualification against `config/pipeline.yaml`
  used the nasdaq feed as the sole source (no cross-source timing conflicts to check);
  options-market/OTC/SPAC-remnant screening was done by inspection — all 27 above-floor
  names are established Nasdaq/NYSE operating companies with analyst coverage. One
  unfamiliar name, `KEEL` (Keel Infrastructure Corp.), was spot-checked via WebSearch
  and confirmed Nasdaq-listed (XNAS) with a live options market. No exclusions applied
  beyond the market-cap floor. 27 eligible names exceeds the stage-1 skip threshold
  (`triage.skip_if_universe_at_or_below: 10`), so stage 1 (triage) will run normally.

## Stage 1 — triage (11:57 CEST)
- Mode: scouted (27 eligible > skip threshold of 10)
- Funnel: 48 universe -> 27 eligible -> 23 cleared floors -> 10 shortlisted
- Scouts: 2 subagents (sonnet/medium), batches of 15 and 12
- Session mix: 10 BMO / 0 AMC — tonight's entire eligible universe is BMO (stage 0
  found 0 AMC candidates), so no session tilt was introduced by triage
- Dropped for floors/tradeability (4): B, FERG, GCMG (change_expectation below 35),
  KSPI (untradeable — thin ADR options market, ai_edge 25)
- Notable drops among names that cleared floors but missed the top 10: SBET
  (ai_edge sits exactly at the 30 floor — effectively an ETH-NAV vehicle, print adds
  little new info), MPT (distressed hospital-REIT turnaround, priority 55.0, just
  missed the cut)
- Flag for stage 2: KEEL and BW cleared floors mechanically but scouts flagged real
  forecastability caveats — KEEL's move is largely crypto/hashrate-sentiment driven,
  BW's short-seller dispute partly hinges on facts not yet public. Dossiers for these
  two should be explicit about how much of the move is genuinely forecastable.
- No fabricated data: all `expected_move_hint` fields are null (no options-implied
  move sourced by either scout within its time budget)
