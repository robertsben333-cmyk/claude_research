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
