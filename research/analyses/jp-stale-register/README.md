# What the stale JPX short register did to stage J (2026-10-01 to 10-14)

Question (Xavier, 2026-10-14): `xlrd` was missing, so every October stage J baseline was
sealed on the 2026-09-29 JPX short register. How much did that change the predictions and
how they did?

Method: `analyse.py <main checkout> jpx-registers-0929-1014.json`. For every October
baseline, take the latest JPX file dated before the seal day in Tokyo, rebuild
`lean_components()` from `jp_priced_in.py` with that register (margin ratio and run-up as
sealed), and rank the sealed and corrected numbers against `realised_move_pct` from
`jp-resolved.json`. Permutation p, 5,000 shuffles, pooled over days.

## Result

- 127 baselines over 10 runs. The register inputs (level or day-on-day change) differ for
  **41**. 25 of those are resolved.
- Lean shift: mean |Δ| 0.20 pt, more than 0.25 pt on 28 names, largest 3.17 pt (3083 on
  10-14: sealed 0%, register 9.51%).
- Against the outcome, 77 resolved names, 10-01 to 10-09:

| ranker | sealed (stale) | corrected |
| --- | --- | --- |
| `priced_lean_pct` | ρ −0.004, p 0.97 | ρ +0.067, p 0.56 |
| `short_squeeze` | ρ −0.287, p 0.012 | ρ −0.145, p 0.20 |
| `short_building` | ρ +0.204, p 0.073 | ρ +0.002, p 0.99 |
| lean sign right | 39 / 77 | 40 / 77 |
| `impact_sum` (unchanged) | ρ +0.112, p 0.34 | same |

- The ranking key is untouched: `impact_sum` is the hunters' sum and the lean is a
  diagnostic and a free control, never an input to the ranking or the panel selection.
- Hunters: 45 findings mention short or margin positioning; about five rest on the
  register's numbers for a name whose inputs were stale (3321, 3498, 3382, 6814, 2809), at
  −0.6 to +0.5 pt each. Several hunters sourced positioning themselves and caught the
  baseline missing it (3063).

## Reading

The stale register did not move the predictions that are judged: the key and the panel are
the same numbers. It did corrupt the one test the positioning anchor was built for. The
stale `short_squeeze` ranks *against* its prior sign at p 0.012, and on the correct-day
register that falls to p 0.20. One cell of seven, 77 names, seven days: noise, not a
finding, in either direction. October 1 to 14 cannot say whether the JPX register helps;
measure it from the first run after the fix, and never pool those runs with these.
