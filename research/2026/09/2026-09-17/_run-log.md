# Run log — 2026-09-17

## Stage 0 — universe — 07:14 CEST
- Logged at 2026-09-17 05:14 UTC
- Window: After the US close on Thursday 17 September 2026 through before the US open on Friday 18 September 2026
- Source: nasdaq (after-close 15 rows, before-open 8 rows; 1 in window)
- Universe: 1 total (1 AMC, 0 BMO); 0 eligible after qualification
- Excluded: 1 (below_market_cap_floor: UPXI, $76.0M market cap vs $500M floor)
- Notes: Thin actionable window as of this run — not a holiday, just few confirmed prints on the calendar yet. Eligible count (0) is at or below triage.skip_if_universe_at_or_below (10), so stage 1 will skip today.

## Maintenance — per-name cap raised to 33% of equity
- Logged at 2026-09-17 06:38 UTC
- execution.sizing.max_position_pct_of_equity: 20 -> 33, on the operator's instruction. Live on main from this commit; it applies to the NEXT book, not to the ALMU and LEN positions already open, which were sized under the 20% cap.
- At the current paper equity of ~$11,260 a capped name is $3,710. Two names deploy 66% of the account, three names 99%. Below three names the book is deliberately under-invested, where that used to be below five.
- What it costs, stated rather than buried: concentration. The 22-23% gaps in the resolved sample (NX +22.23%, CANG -23.01%) move the account about 7.5% at a 33% weight against 4.5% at 20%. Nothing in this stage is hedged or stopped out, so the cap is the risk control.
- max_position_pct_of_adv stays at 1.0%. At $10k of equity a 33% position is 1.65% of a $200k/day name, so capacity now binds before equity in the thinnest tradable names and the leftover is redistributed over the rest of the book.
- Updated with it: config comments, edge/EXECUTION.md (four passages), CLAUDE.md. scripts/smoke_test.py no longer hardcodes the old cap in its under-deployment check; it reads the shipped numbers and is green.
