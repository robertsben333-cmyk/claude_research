# Confirmation on the sealed judge-lab test days (written before unsealing)

Written 2026-10-05 after the discovery analysis (`analyze.py`, `deep.py`,
`mechanism.py`, `checks.py`, all on 143 hunts / 138 prints with the judge-lab TEST
days excluded) and BEFORE any outcome on those days was read by this analysis. The
labels for the test names exist (the labeler never sees outcomes); their outcomes were
never joined. Committed before `--unseal` is run.

## The 20 sealed names

Run days 2026-08-31 (8), 2026-09-15 (4), 2026-09-23 (8). Nine have no option-implied
move, eleven have one. Twenty names is a sign check, not a test with power: each
contrast below is read as **holds** (same sign as discovery), **flat** (gap within
±0.05 of hit rate or ±0.10 of mean signed move/priced) or **flips** (opposite sign). A
flip counts against the finding.

## Frozen definitions (from discovery, not re-fitted)

- low sufficiency: labeler `pack_sufficiency` < 42.5 (the discovery median);
- low reliability (item): labeler `reliability` < 68 (the discovery lower tercile);
- no anchor: the sealed baseline has no option-implied move;
- the judge: `median4`, the median of the four blinded re-judges' `impact_sum`.

## The four contrasts

- **C1, the original observation, as a name effect.** median4's sign is right more often
  on low-sufficiency names than on high-sufficiency names. Discovery: 39/62 (63%)
  against 31/64 (48%).
- **C2, the mechanism.** median4's sign is right more often on names without an option
  anchor than on names with one. Discovery: 37/58 (64%) against 33/68 (49%).
- **C3, the source type that carries it.** In names without an option anchor, items the
  labeler calls `focal_primary` (the company's own disclosure) point the right way:
  mean signed move/priced > 0. Discovery: 63% right, +0.52.
- **C4, the hypothesis that started this, in its item form.** Low-reliability items do
  NOT carry the sign: their mean signed move/priced is <= 0. Discovery: 44% right,
  −0.34. (This is the user's hypothesis turned into its tested opposite; if it flips,
  the user's reading gains support.)

Reported beside them, without a verdict: the same numbers for every judge, the
top-20% book inside each sufficiency half, and every discovery table re-run on all
158 prints (discovery + test) with `--unseal`.
