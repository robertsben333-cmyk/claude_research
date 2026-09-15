# Stage 1 — Triage shortlist — 2026-09-15

**Window:** After the US close on Tuesday 15 September 2026 through before the US open
on Wednesday 16 September 2026

## Funnel

universe 4 → eligible 2 → cleared floors 2 → shortlisted 2

Eligible count (2) is at or below `triage.skip_if_universe_at_or_below` (10). The
screen was **skipped**: both eligible names carry forward with no scores.

## Shortlist

| Ticker | Session | Change exp. | AI edge | Rationale |
| --- | --- | --- | --- | --- |
| TCOM | amc | — | — | universe at or below the triage threshold — all eligible names carried forward |
| LUXE | bmo | — | — | universe at or below the triage threshold — all eligible names carried forward |

Session mix: 1 AMC / 1 BMO — balanced by construction (nothing was screened out).

## Dropped names

None dropped at this stage — no scouting was run. Stage 0 already excluded EPM and
ISPR for failing the market-cap floor (see `00-universe.json`).

## Notes for stage 2

- Both names are unscored (`triage_mode: skipped_small_universe`); stage 2 gets no
  `change_expectation`/`ai_edge` signal to prioritize between them — treat both as
  equally in-scope for a dossier.
- Universe is thin (2 names). No evidence-quality or session-imbalance concerns.
