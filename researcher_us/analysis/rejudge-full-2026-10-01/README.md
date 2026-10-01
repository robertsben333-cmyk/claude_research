# Full blinded re-judge, 2026-10-01: Opus 5.5 and Sonnet 5.5 on every resolved run

Question: under the new shared hunter core (`config/hunter-core.md`), would Opus 5.5 or
Sonnet 5.5, judging the evidence each live hunt collected, rank the day better or run a
better book than the live hunt did? And how does the |impact_sum| threshold move the
return per trade?

Setup. `key.json` lists every resolved hunted name in the US, Europe, Japan and
Australia (Canada has no resolved run; stage R is left out). 38 names are excluded for
leakage, because their ticker or company name appears in CLAUDE.md, an agent definition
or a LESSONS file. The other 174 are split into five packs (`packs-*.json`): the sealed
baseline and every item the live hunter surfaced, with its sizes, verdicts and final
numbers removed. Ten fresh cloud sessions, one per pack per model, read only `brief.md`
and their pack. Served models were confirmed (`claude-opus-5-5`, `claude-sonnet-5-5`) and
every session reports zero web searches and zero fetches. Outputs are `out-<pack>-<model>.json`.

`score_full.py` writes `scores.json`. Return per trade = sign(impact_sum) x realised move,
gross. US names use the strategy exit and the $200k turnover floor; other regions use
their resolver window. Spearman is within day, pooled, with a within-day permutation p.
`threshold-chart.html` draws the curves, on an absolute threshold and on a rank-relative
cut (the same share of each arm's largest scores).

## Result

| group | n | short all | arm | zeros | median abs | rho (p) | book >=0 | top 20% | >=3 |
|---|---|---|---|---|---|---|---|---|---|
| all | 174 | +1.35% | live | 31 | 1.00 | -0.12 (0.14) | -1.21% on 123 | +2.7% on 25 | +2.73% on 25 |
| | | | Opus 5.5 | 28 | 0.70 | -0.10 (0.24) | -1.35% on 126 | -0.3% on 25 | 1 name |
| | | | Sonnet 5.5 | 25 | 0.54 | -0.06 (0.53) | -0.85% on 129 | +0.5% on 26 | 0 names |
| US | 113 | +3.14% | live | 13 | 1.90 | -0.17 (0.10) | -1.81% on 80 | +1.7% on 16 | +3.18% on 22 |
| | | | Opus 5.5 | 8 | 1.00 | -0.19 (0.07) | -1.93% on 85 | +1.6% on 18 | 1 name |
| | | | Sonnet 5.5 | 6 | 0.70 | -0.12 (0.26) | -1.20% on 87 | +1.3% on 18 | 0 names |
| ex-US | 61 | -1.33% | live | 18 | 0.50 | -0.03 (0.83) | -0.09% on 43 | +0.5% on 9 | 3 names |
| | | | Opus 5.5 | 20 | 0.32 | +0.06 (0.67) | -0.13% on 41 | +2.2% on 9 | 0 |
| | | | Sonnet 5.5 | 19 | 0.24 | +0.06 (0.68) | -0.14% on 42 | +4.0% on 9 | 0 |

No arm ranks the US days: all three rho are negative and none is significant. In the US
no arm's book beats shorting every tradable name (+3.14%) at any cut with more than ten
names. The re-judges size smaller than the live hunt (median 0.70 and 0.54 against 1.00),
so on an absolute threshold they run out of names before 3.0; at equal selectivity they
land in the same range as live. Their high points (Sonnet +11.5% at >=2 on 6 names,
Opus +6.4% on 7) are too thin to read. Outside the US the re-judges look slightly better
than live at the top cuts (+2 to +4% on 9 names), also too thin.

Split by era, the live hunt in the US is no better before the model change (rho -0.15 on
82 names up to 09-22) than after it (-0.22 on 31), and the re-judges track it in both. On
this sample the problem is not the model or the prompt on the same evidence: the evidence
does not rank the day.

Caveats. Leakage exclusion removes the names this repo wrote about most, which skews the
sample away from the largest past convictions. Ex-US days are few and partly validation
days. The re-judges see only what the live hunter found; they cannot test whether a
deeper search under the new core finds more. Gross of costs, no multiplicity correction.
