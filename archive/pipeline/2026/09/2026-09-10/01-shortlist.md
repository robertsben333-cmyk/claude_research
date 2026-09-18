# Stage 1 — Shortlist for 2026-09-10

**Window:** After the US close on Thursday 10 September 2026 through before the US open
on Friday 11 September 2026

**Mode:** skipped — universe eligible (8) ≤ `triage.skip_if_universe_at_or_below` (10).
No scouts were spawned; every eligible name from stage 0 is carried forward unscored,
per the skill's skip-mode rule.

## Funnel

17 universe → 8 eligible → 8 cleared floors (screen skipped) → **8 shortlisted**

## Shortlist

| Ticker | Session | Event date | Market cap | change_expectation | ai_edge | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| ORCL | amc | 2026-09-10 | $468.1B | — | — | universe at/below triage threshold — carried forward |
| ADBE | amc | 2026-09-10 | $102.3B | — | — | universe at/below triage threshold — carried forward |
| KR | bmo | 2026-09-11 | $35.0B | — | — | universe at/below triage threshold — carried forward |
| CPRT | amc | 2026-09-10 | $30.2B | — | — | universe at/below triage threshold — carried forward |
| DSGX | amc | 2026-09-10 | $6.5B | — | — | universe at/below triage threshold — carried forward |
| RH | amc | 2026-09-10 | $2.7B | — | — | universe at/below triage threshold — carried forward |
| FEIM | amc | 2026-09-10 | $0.73B | — | — | universe at/below triage threshold — carried forward |
| LPTH | amc | 2026-09-10 | $0.67B | — | — | universe at/below triage threshold — carried forward |

Session mix: 7 AMC / 1 BMO — heavily AMC-tilted, driven by the day's actual calendar
(12 of 17 universe rows were AMC), not by any screen. Stage 2 should not read the
skew as a triage artifact.

## Dropped names (from stage 0, not by this stage)

Stage 1 did not screen — the 8 eligible names above are exactly stage 0's eligible set.
Stage 0 excluded 9 names before this stage ran:

- **REF** (Reformation Inc.) — `unconfirmed_timing`: IPO'd 2026-07-30 (~6 weeks public);
  conflicting third-party earnings-date estimates (9/4, 9/10, 11/3) with no official
  IR/8-K confirmation of a 2026-09-10 report; listed-options market also unverified.
- **IBEX, ZUMZ, AENT, HOFT, CMCM, RENT, CSBR, MNY** — `below_market_cap_floor` (all under
  the $500M floor; market caps from $38.7M to $494.1M).

## Warning for stage 2

Unscored shortlist — `change_expectation`/`ai_edge`/`priority_score` are all `null` by
design in skip mode, so stage 2 has no triage-derived ranking signal for these 8 names
going into the deep dive. Two mega-caps (ORCL, ADBE) and two under $1B (FEIM, LPTH) sit
side by side with no prioritization between them; stage 2's own batching/waves should
decide order, not treat this list as pre-ranked.
