# Prompt trial, 2026-10-01: why Opus 5.5 hunters return near-zero sums

Question: since the hunters moved from Opus 5 to Opus 5.5 (switch 2026-09-22, between
18:56 and 19:09 UTC), US `impact_sum` fell from a median |x| of ~1.7-3.0 per run to
~0.0-0.4, and findings per name from ~3.5 to ~1.1. Is the ranking still there at a
smaller scale, and do small prompt changes move the numbers?

## a) Does Opus 5.5 still rank, at a smaller scale?

Within-day Spearman of `impact_sum` against the realised move to the close, pooled over
days, within-day permutation p (dashboard ledger, duplicates excluded):

| era | names | days | rho | p | zeros |
|---|---|---|---|---|---|
| Opus 5, 08-31..09-22 | 118 | 14 | +0.136 | 0.18 | 3 |
| Opus 5, 09-09..09-22 | 73 | 8 | +0.043 | 0.74 | 3 |
| Opus 5.5, 09-23..09-29 | 32 | 5 | -0.101 | 0.60 | 12 |

No evidence either way. The recent Opus 5 days did not rank either, and 12 of 32 Opus 5.5
names are exact zeros, so the ranking is partly a tie.

## b) Trial hunts

Same agent definition (`unpriced-hunter`, served on Opus 5.5), same sealed baselines, only
the spawn brief differs. Forward names (prints 2026-10-05/06), so no look-ahead. Baselines
were sealed at 08:30 UTC with the US market shut, so no option chain on any of them.

- **A, control**: the brief the skill sends.
- **B, no stacking**: lessons calibrate a size and do not veto a finding; each rule applies
  once; drop only for no URL, outside window, duplicate or contradicted by a document.
- **C, scale anchor**: the day is ranked, so a name with a lead must read visibly
  different from one with none; size against the name's own median reaction; record
  uncertain findings small rather than leave them out.

`impact_sum` (sum of the per-finding sizes, which is what the scorer ranks):

| name | A control | B no stacking | C scale anchor |
|---|---|---|---|
| LW | +0.5 (1 of 2 drafts kept) | +0.9 (4 of 4) | -0.2 (2 of 2) |
| APOG | 0.0 (0 drafts) | +1.0 (2 of 2) | +2.8 (3 of 4) |
| SAR | 0.0 (1 draft moved out of window) | 0.0 (0 drafts) | -0.3 (3 of 3) |
| findings per name | 0.33 | 2.0 | 2.67 |
| mean abs(impact_sum) | 0.17 | 0.63 | 1.10 |

RELL was dropped: both hunters found the company's own release puts the print on
2026-10-07, not the calendar's 10-05.

Three hunts per arm is anecdote, not measurement. Same-name hunts disagree in sign (LW
B +0.9 against C -0.2), the same reproducibility problem the double hunt measured on Opus 5.
