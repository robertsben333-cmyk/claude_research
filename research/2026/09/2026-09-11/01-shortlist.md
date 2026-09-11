# Stage 1 — Shortlist for 2026-09-11

**Window:** After the US close on Friday 11 September 2026 through before the US open
on Monday 14 September 2026

**Mode:** skipped (universe at or below threshold)

## Funnel

4 universe → 1 eligible → 1 cleared floors (screen skipped) → **1 shortlisted**

Eligible universe (1) is at or below `triage.skip_if_universe_at_or_below` (10), so the
screen was skipped entirely per the skill: the one eligible name carries forward with no
`change_expectation` / `ai_edge` scores. No `earnings-triage-scout` subagents were
spawned.

## Shortlist (1 name, all eligible names carried forward)

| Ticker | Session | Event date | Market cap | Scores | Rationale |
| --- | --- | --- | --- | --- | --- |
| CSHR | bmo | 2026-09-14 | $0.70B | not scored (skip mode) | universe at or below the triage threshold — all eligible names carried forward |

Session mix: 0 AMC / 1 BMO — entirely BMO, unavoidable this cycle since the after-close
side of the window (Friday) had zero reporters at all.

## Dropped names

None dropped by triage — the screen never ran. Three names failed stage-0 qualification
before reaching this stage, all on `below_market_cap_floor`: **CODA** (Coda Octopus
Group, $0.11B), **RFIL** (RF Industries, $0.11B), and **HAIN** (Hain Celestial, $0.06B).

## Note for stage 2

This is a weekend-roll window: Friday's after-close side was empty, so every name in the
universe reports Monday 2026-09-14 before the open — including the one shortlisted here.
A single unscored name is a thin day for the pipeline. `deep_dive.wave_size: 2` and
`deep_dive.batches: 2` are built for a multi-name shortlist; today only one dossier is
possible regardless of batch/wave settings. Stage 2 should treat CSHR as unranked (no
triage priority signal) and, given it is the day's only candidate, research it on its own
merits rather than deferring on relative priority. Note also that CSHR only recently
began trading (Nasdaq listing 2026-04-01, options since 2026-04-16) — expect thin
historical-reaction data and say so explicitly in the dossier rather than estimating from
a short window.
