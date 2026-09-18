# Stage EU — validation run, event date 2026-09-16

**THIS IS NOT A RESULT ABOUT ANYTHING.** It is the end-to-end validation of stage EU
against a real past date, run on 2026-09-18. The findings are **synthetic** — random
signs and sizes, generated to exercise the scorer's arithmetic and the resolver's
plumbing. Nothing here is a claim about Advanced Medical Solutions, Barratt Redrow, Pan
African Resources or Supermarket Income REIT, and the ranking below means nothing.

Three things about it are contaminated by hindsight and are labelled in the files
themselves:

- The universe was built with `eu_universe.py --use-last-release`, which reads the
  vendor's **last** release date instead of its next one so a past day can be assembled
  at all. Every file it produced carries `validation_only: true`.
- The baselines were sealed on 2026-09-18 for a 2026-09-16 event, so `tape.spot`, both
  run-ups and realised volatility were read **after** the print. Each baseline carries a
  `validation_note` saying so.
- The short register read is the one current on 2026-09-18, not the one current on
  2026-09-15.

## What the run actually establishes

| | |
| --- | --- |
| Vendor calendar rows for 2026-09-16 across UK/DE/FR | 22 |
| Eligible above the $1m/day turnover floor | 4 (all UK) |
| Hunted | 4 — `all 4 eligible names (at or under the cap)` |
| Baselines sealed | 4, `options` null in all of them |
| Short register resolved | 4 of 4 (FCA, as of 31/08/2026) |
| History basis | `observed_rns` on all four — real dated announcements, 5 to 8 rows each |
| **Confirmed by a real results RNS** | **4 of 4**, out of 40 EPICs that filed one on Investegate that day |
| `lean_vs_free_control_rho`, UK | **0.40** — the lean is not the run-up |

The ranking on synthetic findings came out at ρ = −0.80 with a permutation p of 0.33 on
four names, which is what random findings on four names should do.

## Ranked table (SYNTHETIC — do not read the order)

| # | market | ticker | company | `impact_sum` | `pre_local` | session | realised, bmo window | realised, amc window | analysts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | UK | AMS | Advanced Medical Solutions | +6.48 | +5.78 | bmo | +0.18% | +0.00% | 7 |
| 2 | UK | SUPR | Supermarket Income REIT | +3.67 | +0.37 | bmo | +2.06% | +1.01% | 8 |
| 3 | UK | BTRW | Barratt Redrow | +2.36 | +2.43 | bmo | **+11.72%** | +1.78% | 19 |
| 4 | UK | PAF | Pan African Resources | −3.84 | −3.25 | bmo | +5.50% | +5.13% | 7 |

## The one genuinely useful number in this table

**Barratt Redrow moved +11.72% over the correct `bmo` window and +1.78% over the `amc`
one.** That is the whole argument for why this stage windows `close(D−1) → close(D)` and
why `session_unresolved` is carried rather than defaulted away. The vendor calls the
session unknown for 150 of 318 German and 238 of 346 French rows; on a name like this,
getting it wrong would have thrown away six sevenths of the move and left the ranking
measuring a different day.

## The retrospective kill was verified separately

Not on this run — all four names here reported. The `event_occurred: false` path was
checked against two names Phase 1 had already identified as vendor no-shows. On
2026-09-15 Investegate carried 37 results RNS and 296 issuers announcing anything, and:

- **ITM Power** and **Petra Diamonds** appear in neither list → `event_occurred: false`.
  This is the TRT path, and it works.
- **Trustpilot** appears in the "announced anything" list and not the results list,
  because its interims were headlined *"AI, Enterprise and US momentum fuel strong
  growth"* → `announced_unclassified`, a human call and not an automatic kill.

## What this run does not test

- Any German or French name, because none cleared the turnover floor on this date. The
  German confirmation path (EQS-News, same-day only) and the French one (nothing
  readable) were exercised only as code paths, not against real rows.
- A real hunter. No `unpriced-hunter-uk`, `-de` or `-fr` was spawned; the hunt files are
  generated JSON.
- The language pass. `pre_local` was perturbed synthetically, so
  `stats.language_pass` reports a delta that is noise by construction.
- Anything at all about whether this stage has an edge.

---

*Research, not investment advice. This is a forecasting exercise over public information
and the numbers above are synthetic. See `config/pipeline.yaml` for the standing
disclaimer.*
