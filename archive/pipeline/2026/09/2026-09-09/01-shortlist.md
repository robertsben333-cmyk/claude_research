# Stage 1 — Shortlist for 2026-09-09

**Window:** After the US close on Wednesday 09 September 2026 through before the US open
on Thursday 10 September 2026

**Mode:** skipped (universe at or below threshold)

## Funnel

20 universe → 7 eligible → 7 cleared floors (screen skipped) → **7 shortlisted**

Eligible universe (7) is at or below `triage.skip_if_universe_at_or_below` (10), so the
screen was skipped entirely per the skill: all 7 eligible names carry forward with no
`change_expectation` / `ai_edge` scores. No `earnings-triage-scout` subagents were spawned.

## Shortlist (7 names, all eligible names carried forward)

| Ticker | Session | Event date | Market cap | Scores | Rationale |
| --- | --- | --- | --- | --- | --- |
| COO | amc | 2026-09-09 | $13.6B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| AVAV | amc | 2026-09-09 | $7.4B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| NAVN | amc | 2026-09-09 | $7.1B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| M | bmo | 2026-09-10 | $6.1B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| AEO | amc | 2026-09-09 | $2.9B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| WLTH | amc | 2026-09-09 | $1.4B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |
| TEN | bmo | 2026-09-10 | $1.3B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |

Session mix: 5 AMC / 2 BMO.

## Dropped names

None dropped by triage. One name failed stage-0 qualification before reaching this
stage: **YB** (Yuanbao Inc. / market cap $632M) — excluded at the universe stage for
`no_options_market` (recent IPO, no listed contracts). The remaining 12 universe rows
were below the $500M market-cap floor and never reached "eligible."

## Note for stage 2

Six of the seven names have zero triage scoring (skip mode carries no `change_expectation`
or `ai_edge` signal) — stage 2 should treat this as an unranked candidate pool, not a
priority-ordered one, and apply its own judgment on depth/order across all seven. With
`deep_dive.wave_size: 2` and two firings/day, seven names will take four waves total
(2+2+2+1) rather than the three implied by a six-name shortlist — plan the day's batches
accordingly.
