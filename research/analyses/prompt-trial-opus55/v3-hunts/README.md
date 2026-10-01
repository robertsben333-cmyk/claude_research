# Hunter core v3 test, 2026-10-01

The same three forward names and sealed baselines as the morning trial, hunted with the
shared core (`config/hunter-core.md`) in `unpriced-hunter`, once on the definition's own
model (Opus 5.5) and once with the model set to Sonnet 5.5.

| arm | name | abs_move_pct | p_up | impact_sum | findings | rejected |
|---|---|---|---|---|---|---|
| Opus 5.5 | LW | 11 | 42 | -1.76 | 5 | 3 |
| Opus 5.5 | APOG | 13 | 45 | -1.30 | 5 | 4 |
| Opus 5.5 | SAR | 4 | 52 | +0.16 | 6 | 1 |
| Sonnet 5.5 | LW | 11 | 52 | +0.40 | 2 | 1 |
| Sonnet 5.5 | APOG | 12 | 53 | +0.70 | 3 | 1 |
| Sonnet 5.5 | SAR | 7 | 40 | -1.40 | 2 | 1 |

All six hold the identity: the findings add up to (2 x p_up/100 - 1) x abs_move_pct. All
six set the scale from the name's own median reaction (10.0, 12.7 and 3.1%), and every
dropped candidate names one of the four allowed reasons. No hunter found a decisive
unpriced number, so p_up stays within 10 points of 50 and the sums stay small. That is the
non-result the core allows, not shrinkage. **The two models disagree on sign for all three
names**, which is the reproducibility problem the double hunt measured, and three names
cannot say which model is right.
