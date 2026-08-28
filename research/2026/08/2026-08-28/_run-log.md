# Run log — 2026-08-28

## Stage 0 — universe (07:19 CEST)
- Window: After the US close on Friday 28 August 2026 through before the US open on Monday 31 August 2026
- Source: nasdaq (both after-close and before-open sides)
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification
- Excluded: 3 (below_market_cap_floor: SY, LX, BLRX)
- Notes: Friday run correctly rolled the before-open side to Monday 2026-08-31 (weekend skip).
  Only SAIC cleared the $500M market-cap floor. Cross-checked SAIC's BMO timing against a second,
  independent source (SAIC's own GlobeNewswire IR release, issued 2026-08-13) beyond the Nasdaq
  calendar — both agree on before-market-open, 2026-08-31, so timing is confirmed, not just
  single-sourced. SAIC has an active listed-options market. Eligible universe of 1 is well below
  `triage.skip_if_universe_at_or_below: 10`, so stage 1 (triage) will be skipped — the single
  eligible name goes straight to stage 2.

## Stage 1 — triage (11:08 CEST)
- Mode: skipped (universe <= threshold — 1 eligible <= 10)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors (screen skipped) -> 1 shortlisted
- Scouts: 0 subagents (screen skipped)
- Session mix: 0 AMC / 1 BMO
- Notable drops: none by triage (SY, LX, BLRX already excluded at stage 0 for below_market_cap_floor)
