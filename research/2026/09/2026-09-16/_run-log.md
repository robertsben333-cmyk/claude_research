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
