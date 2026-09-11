# Run log — 2026-09-11

## Stage 0 — universe (06:40 UTC / 08:40 CEST)
- Logged at 2026-09-11 06:41 UTC
- Window: After the US close on Friday 11 September 2026 through before the US open on Monday 14 September 2026
- Source: nasdaq
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification
- Excluded: 3 (below_market_cap_floor: CODA, RFIL, HAIN)
- Notes: Weekend roll — Friday close side empty (0 AMC), before-open side rolled correctly to Monday 2026-09-14. CSHR ($0.70B) is the only name above the $500M floor; verified via WebSearch as Nasdaq-listed common (de-SPAC'd 2026-04-01, not a SPAC remnant), with an active listed-options market since 2026-04-16, and BMO timing confirmed by CoinShares' own IR release.

## Stage 1 — triage (06:52 UTC / 08:52 CEST)
- Logged at 2026-09-11 06:42 UTC
- Mode: skipped (universe <= threshold)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors -> 1 shortlisted
- Scouts: 0 subagents (skip mode)
- Session mix: 0 AMC / 1 BMO
- Notable drops: CODA (below_market_cap_floor), RFIL (below_market_cap_floor), HAIN (below_market_cap_floor) -- all dropped at stage 0, none reached triage

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-11 08:24 UTC
- Shortlist: 1 name; this batch: CSHR
- Already on disk, skipping: none
- Plan: 1 researcher (single wave, wave_size=2 not needed), publish after it completes
