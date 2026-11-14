# Stage E-P v3b against stage E-P: pre-registration

Written 2026-11-14, before stage E-P v3b's first run (first fire 2026-11-16, 13:10 New
York). Nothing below may be changed after that date; a change is a new file with a new
date, and the old one stays.

## The question

Do the v3b prompts (`config/searcher-addendum-v3b.md`, `config/panel-judge-v3b.md`)
predict the earnings reaction better than stage E-P's prompts (us-panel.v3, searcher
`us-searcher` and the `panel-judge-*` brief as of 2026-11-14)? Models, sweep, cap, packs
format and selection rule are the same in both stages.

## The sample

Every run day on which both `research/<Y>/<M>/<D>/edge-panel/edge-scores-panel.json`
and `.../edge-panel-v3b/edge-scores-panel.json` exist, and on that day only the names
both stages ranked. A name only one stage ranked is counted and left out. Moves are the
close before the print to the close after the first full session
(`edge_resolve.realised`), gross. The scaled move is the move divided by the sealed
`expected_move_pct` of v3b's baseline.

The comparison runs while stage E-P stays on us-panel.v3. If stage E-P's searcher or
judge prompt changes, the days after the change are a new sample. If v3b's prompts
change, that is us-panel-v3b.v2 and its count starts at zero.

## When it is read

`researcher_us/scripts/v3b_compare.py`. A first read at 20 run days, the decision at 30
(the review estimated 25 to 30 run days before an effect of 0.1 expected moves per sd
shows at a probability of 0.95). Nothing is read before 20.

## Primary measure

Δρ = ρ_scaled(v3b) − ρ_scaled(E-P), where ρ_scaled is the within-day pooled Spearman
correlation of `panel_pct_signed` (from each stage's own `edge-scores-panel.json`)
against the scaled move. Uncertainty from a day bootstrap (2,000 resamples of days).

- **v3b predicts better**: P(Δρ > 0) ≥ 0.90 at 30 days.
- **v3b predicts worse**: P(Δρ > 0) ≤ 0.10.
- Otherwise: no difference shown.

## Secondary measures, reported whatever they show

1. ρ on the raw move, same test.
2. The book at `panel_pct` ≥ 80 with all four judges, and the band at ≥ 60: number of
   names, hit rate, mean side return, mean scaled side return, per stage.
3. The judges' mean `p_up`: Brier score against the sign of the move, and its spread
   across names. The review's problem was resolution (sd 5.7 points): v3b is better
   here only if the spread is wider and the Brier score is not worse.
4. v3b's three-part forecast: the mean over judges of p × move_if_clears + (1 − p) ×
   move_if_misses (p = p_clears_real_bar / 100), ranked as the primary.
5. On v3b's runs alone, the leads of the review, with the sign each is expected to
   carry, by the searcher's `evidence_type` tags:
   - A: `consensus_bar` items carry less move per judged point than the average type.
   - B: `expectations` items carry more.
   - C: `mid_quarter_statement` items help as the main item of a call at ≥ 60.
   - D: `one_off` and unlinked `peer` items are weak.
   - E: `counterparty` items carry the most per point.
   - F: more disagreement between the judges' `p_up` does not mean a worse side return.
   A lead that keeps its sign earns a firmer instruction in a later version; one that
   flips is dropped. These are tested on v3b's own runs only, never pooled with v3.

## Known differences besides the prompts

- Each stage runs its own sweep, so the hunted names can differ at the margin; only
  common names are compared.
- v3b's judges are read against their own history, seeded with a frozen copy of stage
  E-P's; for the first days the seed sets the scale. `edge-scores-panel-epscale.json`
  carries v3b on stage E-P's scale for a check.
- The two stages search the same afternoon and may compete for the same rate limits;
  unfinished hunts are excluded by both stages' own rule.
