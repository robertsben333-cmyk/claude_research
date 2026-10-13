# Is "top 20%" a top 20% in every market? (2026-10-12)

Question (operator): per country, are the current percentages the scoring uses about right?

Three lines are meant to be a top 20%:

- **the panel line**: a judge's "own top 20%", the 80th percentile of |impact_sum| over the
  last 200 sizes in that market's `panel-history.json`; a name is selected at 3 of 4;
- **the hunter floor**, `edge_hunt.conviction_floor` 2.8 on |impact_sum| (emphasis outside
  the US), set as p80 of an Opus 5.5 reference set;
- **the US money gate**, `execution.benchmark.min_conviction` 1.76 on |impact_scaled|,
  set the same way.

`python3 country_thresholds.py > output.txt` reads the dashboard data, the baselines,
the panel histories, the four-model re-judge (`../rejudge-four-models/`, 231 resolved
names, anonymised ones left out) and the October runs. Gross, research only.

## Result

**Outside the US none of the three lines is a top 20%. They are a top 0-5%.**

| market | median \|move\|, resolved | judges' median \|impact\|, re-judge | names in a judge's top line, re-judge | live panel selection | live >= 2.8 / >= 1.76 |
|---|---|---|---|---|---|
| US | 5.36% (184) | 0.80-1.42 | 34-38% | 5 of 35 (14%) | 2 of 36 / 2 of 37 |
| Europe | 4.08% (57) | 0.24-0.60 | 0-3% | 0 of 6 | 0 of 16 / 0 of 17 |
| Japan | 2.61% (65) | 0.48-0.71 | 0-10% | 1 of 25 (4%) | 0 of 77 / 0 of 73 |
| Australia | 1.88% (16) | 0.00 | 0% | no October names | none |
| Canada | 2 resolved | no re-judge | n/a | 0 of 1 | 0 of 3 |

Why: every non-US history was seeded on 2026-10-08 with a copy of the E-P history at scale
1.0, so each market's line sits on a US earnings scale. Stage IPO was seeded at 0.674 for
exactly this reason; the regional stages were not. The judges size Europe at about 35-45%
of their US sizes and Japan at about 45%, more than the move ratio alone (Europe 0.76,
Japan 0.49 of the US) would justify.

**In the US the panel line is too LOW on the re-judge and about right live.** 77 of the
200 sizes in the US window are European, Japanese and Australian re-judge rows. Without
them the lines rise from 1.95/1.40/1.20/1.44 to 2.88/1.92/1.60/2.40. On the re-judge, the
US-only line selects 21 names, 17 right, +5.48% (t 2.30) against 38, 26 right, +3.12%
(t 1.71) now. Live, the E-P judges size smaller than the re-judge did, so the mixed line
lands at 11-23% per judge, near its target, and the US-only line would cut it to 6-14%.
The re-judge result is in sample: the 3-of-4 rule was chosen on these names.

**The hunter gates are a top 5% in the US and a top 0% elsewhere.** Live October p80 is
1.3 on |impact_sum| (against 2.8) and 0.96 on |impact_scaled| (against 1.76). Both were
read off a reference that is mostly blind re-judges, and the live hunters size about half
as large.

## Per country inside Europe

One pooled EU line, and that is the right call for now. Resolved names: UK 34, France 7,
Germany 6, every other market 2 or fewer. France (4.9%) and Germany (5.0%) move about as
much as the US, the UK 3.5%, the Nordic, Italian and Polish names less, all on samples too
small to set a line. A pooled line selects the bigger movers more easily, which is size
and not skill; revisit when a country has 30 resolved names.

## Does opening the gate help?

Only Europe has a sign worth having. At each region's own p80 the 3-of-4 rule picks:
Europe 4 names, 4 right, +9.5% (t 1.84); Japan 1 name, wrong; Australia 5 names, 1 right,
-2.7%. The panel's sign on every name: Europe 17 of 29 right, Japan 1 of 9 (t -2.15),
Australia 2 of 6. Tiny samples, and Japan and Australia point the wrong way, as the
re-judge already said.

## When the borrowed seed leaves on its own

A 200-name window at October's pace: Japan (11 names a run, 25 already own) in about 16
runs; Europe (3.3 a run) in about 60 runs, three months; Canada (1.5) about six months;
Australia has had no names since 2026-10-02 (off-season, Feb/Aug reporting).

## What it does not show

The re-judge's non-US names are Opus 5-era hunts and few (Europe 35, Japan 10, Australia
16). Live panel days are 1-2 per market. Nothing here is a measured edge; it is a
measurement of which share of names each line lets through.

## Addendum 2026-10-13: Europe's OWN top 20% (operator: "the top 20% in Europe is accurate")

Relative to Europe's own sizes, not the US-scale line. Resolved, non-validation, gross.

| what ranks | Europe's top 20% | all non-zero names |
|---|---|---|
| hunter `impact_sum`, Sept Opus 5.5 out (dashboard default) | 3 of 5, +1.7% | 13 of 25, -0.4% |
| hunter `impact_sum`, Sept Opus 5.5 in | 7 of 10, +3.5% (binom p 0.17) | 27 of 48, +0.3% |
| re-judge Opus 5 / Sonnet 5.5 / Fable 5.1 (35 names, anonymised out) | 6 of 7 each, +4.8 / +6.8 / +5.2% (p 0.06 each) | 15-17 of 28 |
| re-judge Opus 5.5 | 5 of 7, +3.1% | 15 of 27 |
| re-judge median of the four | 6 of 7, +5.9% (p 0.06) | |

The judges' top 20% is mostly the same names (LIKE, SAGA, MTEC, KGF), so the four rows are
one test, not four. Every one of these names falls BELOW the lines now in use, which is the
argument for rescaling: the part that looks good is exactly what the US-scale line blocks.
Seven names from 09-16..09-30, mostly UK, several definitions tried: a lead to run forward,
about 20 selected names (seven weeks at 3-4 names a run) before it can tell 80% from 55%.
