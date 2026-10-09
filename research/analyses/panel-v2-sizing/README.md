# Keys and the panel: impact_sum, impact_scaled, V2, one agent against four (2026-10-09)

Four questions from the operator: (a) `impact_scaled` against `impact_sum` against V2
grounded; (b) one agent against the four-model panel; (c) is there reason to expect the
panel to be more accurate, also at lower scores; (d) would the panel have done better on
`impact_sum` than on `impact_scaled`. All returns gross, sign(score) x realised move, US
on the strategy exit and the $200k turnover floor.

## Data

- **Retrospective, (b) and (c):** the 231-name four-model re-judge
  (`../rejudge-four-models/`), 206 tradable. `single_vs_panel.py`.
- **New run, (d):** Opus 5, Sonnet 5.5 and Fable 5.1 judged the 128 Opus 5-era names
  under the same brief Opus 5.5 used in `../rejudge-opus55-v2-sizing/` (two
  measurements in one session, never fitted to each other). 30 judges
  (`panel-judge-intl-*`, pinned models, Read/Write only, contract replaced by that
  brief), outputs `out-NN-<model>.json`, 0 validation problems, every name covered. The
  file blobs the judges read are the ones pinned in that folder's `manifest.json`.
  112 tradable names. `score.py` writes `scores.json`.
- **Forward, (a) and (b):** every resolved US run since 09-23 (48 names with V2), the
  `us.v9` hunts since 10-01 (40 hunts with `impact_scaled`, stage E and the E-P
  searcher), and the live E-P panel on 10-05..10-08 (20 names). Priced with
  `dashboard/scripts/build_ledger.py --offline --out <scratch>`; not checked in.

## (a) impact_scaled vs impact_sum vs V2

The three are one measurement. V2 grounded ranks against `impact_sum` at rho 0.95 with
45 of 48 signs equal; `impact_scaled` against the sum at 0.92 forward and 0.95-0.96 for
every judge here.

| sample | impact_sum | impact_scaled | V2 grounded |
|---|---|---|---|
| forward, 48 US names, rho | -0.04 | - | +0.00 |
| forward, top 20% | 9/10 +5.9% | - | 8/10 +3.2% |
| forward, 40 us.v9 hunts, rho | +0.26 (p 0.11) | +0.35 (p 0.05) | +0.31 (p 0.07) |
| forward, top 20% | 7/8 +5.7% | 7/8 +6.6% | 8/8 +3.8% |
| re-judge, 4 judges, rho | +0.09 to +0.20 | +0.15 to +0.23 | - |

`impact_scaled` ranks a little better in every sample and for every one of the four
judges; nothing is significant. V2 adds nothing over the sum and does no better than
`control_vol_only` (identical top 20% forward), which is the bar the repo set for it.

## (b) one agent against the panel

Retrospective, 206 names: the panel median ranks at rho +0.13, the same as the best
single model (Fable +0.14) and above live (+0.08). Top 20%: panel 29/43 +4.6%, the four
models +2.9 to +5.3% (mean +4.2%), live 24/43 +2.1%. The E-P selection (3 of 4 in their
own top 20%) is 23/30, +7.0%. So the panel matches the best model without having to know
which one it is; it does not beat it.

Forward, live E-P, 20 names: selected 5/5 +6.7%, k >= 2 6/6. Stage E's own hunter on
the same names: rho +0.35, 9/20 right. Most of that gap is the searcher's evidence
(searcher alone rho +0.61), not the panel (+0.63). Five days; anecdote.

## (c) more accurate, and at lower scores?

There are reasons to expect it is more accurate in the tail: the four-model median picks
names that move 1.6x the average (`../judge-lab/`), and its selection held in both
regions. There is **no** sign that it predicts below the top:

- by consensus: k = 4 16/21 +7.4%, k = 3 7/9 +5.9%, k = 2 10/19 -0.7%, k <= 1 62/131 -0.7%;
- by rank band: 20-50% 26/61 -1.0%, 50-100% 40/76 -0.4%;
- Brier on p_up over all names: every judge 0.246-0.249, the four-way mean 0.247,
  extremised 0.255; a coin is 0.250. No probabilistic skill across the range, and
  averaging adds none;
- where all four agree on the sign but none puts the name in its top, they are right
  46 of 108 (-1.7%).

What the panel does do below the top is lose less than one agent: live's bottom half is
27/68 -3.1% (t -3.1), the panel's -0.4%.

## (d) would impact_sum have done better in the panel? No.

| 112 names | rho | top 10% | selected (k >= 3) |
|---|---|---|---|
| panel on impact_sum | +0.17 | 9/12 +5.7% | 13/19 +4.2% (t 1.9) |
| panel on impact_scaled | +0.16 | 10/12 +9.1% | 13/18 +8.3% (t 3.5) |
| E-P recipe, earlier v3 re-judge | +0.19 | 8/12 +6.9% | 12/16 +8.9% (t 3.1) |
| live (Opus 5 impact_sum) | +0.17 | 9/12 +4.6% | - |

Same ranking, worse selection. The two selections share 14 names (10/14, +6.1%). The
whole gap is in the rest: five names only the sum picks return -1.1%, four only the
scaled number picks return +16.3%. Four names carry it. Per judge, the sum ranks below the scaled number for all four. The difference
in the selection is about one standard error, but it points the same way as everything
in (a). On the 81 clean US names (anonymised names out) no arm ranks (every rho below
zero) and both selections stay positive (sum 7/8, scaled 8/10).

## What it does not show

Gross of costs. Retrospective samples are the days every earlier analysis was chosen on.
The judges test judgement on the first hunter's evidence, not search. Every subagent
loads CLAUDE.md, which quotes outcomes from these days. Opus 5, Sonnet 5.5 and Fable 5.1 ran as
the `panel-judge-intl-*` agents and the Opus 5.5 member (run on 10-01) as
`general-purpose`, so the system prompt differs by member.
