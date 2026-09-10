# Edge hunt — 2026-09-10 amc + 2026-09-11 bmo

**Ranking key: `impact_sum`** — the hunters' signed per-finding sizes added up, in points of
spot, as named by `edge-scores.json`'s own `ranking_key` field. There is no call, no
threshold and no direction label anywhere below. Any cut is the reader's, applied afterwards
to the complete table.

17 names in the window, **17 of 17 confirmed by the sweep, zero phantom rows** — the best
confirmation rate this stage has recorded. 17 hunters, one per name, 61 findings.

## The ranking

`conviction` is `|impact_sum|`. `floor` marks the seven names clearing the 3.0-point
conviction floor from `config/pipeline.yaml`. `-run_up_20d` is the free control. `turnover`
is spot × 20-day average volume, in $m a day.

|  # | ticker | session | impact_sum | floor | −run_up_20d | turnover $m | chain |
| --: | --- | --- | --: | :-: | --: | --: | :-: |
|  1 | HOFT | bmo 09-11 | **+7.30** | ✓ | +16.64 | 0.4 | — |
|  2 | RH   | amc 09-10 | **+3.00** | ✓ | +23.12 | 83.0 | ✓ |
|  3 | ZUMZ | amc 09-10 | +2.50 | | +8.37 | 3.1 | — |
|  4 | MNY  | bmo 09-11 | +2.00 | | +10.16 | 0.0 | — |
|  5 | DSGX | amc 09-10 | +1.30 | | +4.19 | 44.2 | — |
|  6 | IBEX | amc 09-10 | +1.20 | | −6.46 | 3.7 | — |
|  7 | LPTH | amc 09-10 | +0.40 | | +27.90 | 33.8 | ✓ |
|  8 | CMCM | bmo 09-11 | −1.00 | | −15.56 | 0.0 | — |
|  9 | CSBR | amc 09-10 | −2.00 | | −5.24 | 0.0 | — |
| 10 | ADBE | amc 09-10 | −2.20 | | +2.66 | 1,064.6 | ✓ |
| 11 | KR   | bmo 09-11 | −2.30 | | −1.50 | 314.4 | ✓ |
| 12 | CPRT | amc 09-10 | −2.70 | | −10.81 | 303.8 | ✓ |
| 13 | ORCL | amc 09-10 | **−3.20** | ✓ | −2.80 | 3,397.1 | ✓ |
| 14 | FEIM | amc 09-10 | **−3.50** | ✓ | +18.78 | 13.2 | ✓ |
| 15 | REF  | amc 09-10 | **−3.50** | ✓ | +14.93 | 4.4 | — |
| 16 | AENT | amc 09-10 | **−7.50** | ✓ | +4.85 | 0.1 | — |
| 17 | RENT | bmo 09-11 | **−8.50** | ✓ | +23.42 | 0.2 | — |

## Read the order separately from the sign

**Below the conviction floor the sign is a coin flip.** Over the 38 de-duplicated events
resolved so far, the sign of `impact_sum` was right on 53% of them — nothing. What does
carry information is the *rank* of conviction: it predicted whether the sign was right at
ρ=+0.514, permutation p=0.0015, and above the median conviction the sign was right on 74% of
events. `|impact_sum| ≥ 3` gave 16 of 21 at +6.37% per trade.

So ZUMZ at +2.50 and CSBR at −2.00 are **not** a bullish and a bearish view. They are two
names near the middle of an ordering. The seven floor-clearing names are where the sign has
historically meant something; the other ten are ranking data.

**`impact_sum` is not a forecast of the move.** It sums findings, and the same fact often
arrives twice from two sources — the cluster-max was built to stop exactly that, and the
cluster-max is what measurement demoted. Several hunters flagged their own double-counting
today (REF's three findings share one prospectus; AENT's last two share one DEF 14C; MNY's
revenue and EBITDA legs rest on one revenue assumption). The number ranks. It does not size.
Regression slope against realised moves is 0.72–0.76 and median absolute error 6–7 points
against a realised standard deviation near 11.

## The control, which the hunt has still not beaten

`-run_up_20d_pct` — one number off the sealed baseline, available before a single subagent
was spawned — ranked the six resolved runs at ρ=0.335, against 0.407 for the hunt's raw
evidence, a gap whose confidence interval spans zero. Traded, the control was positive on 6
of 6 days. **Until the hunt beats it, the hunt has not been shown to add anything.**

Today the two rankings are close to orthogonal: **Spearman between them is 0.054.** The
control's order is LPTH, RENT, RH, FEIM, HOFT, REF, MNY, ZUMZ, AENT, DSGX, ADBE, KR, ORCL,
CSBR, IBEX, CPRT, CMCM. The disagreements are head-on, not marginal — the control ranks RENT
second and LPTH first (biggest drawdowns), the hunt ranks them seventeenth and seventh. RH
and HOFT are the only two names both rank near the top. This is a genuinely independent
signal or a genuinely uninformative one, and one day cannot tell you which.

## The top name

**HOFT +7.30** (Hooker Furnishings, bmo 2026-09-11). Driven almost entirely by one finding
worth +7.0: Hooker submitted **approximately $8 million of IEEPA tariff refund claims** in
fiscal Q1 and recognised none of it, booking under a gain-contingency model that waits for
cash. $8m pre-tax is roughly 6% of the $133m market cap and about $0.75/share against a
($0.02) consensus.
Source: <https://www.sec.gov/Archives/edgar/data/1077688/000118518526002495/hoft10q050326.htm>
(10-Q, 2026-06-12).

What the price already says: nothing about this. There is no option chain, so no priced
expectation exists at all; the only directional statement the tape makes is a −16.6% 20-day
drift, and the control ranks HOFT fifth on that. The hunter's argument for it being unpriced
is checkable and specific — on the 11 June call the CFO was asked for the rebate number and
answered that they had decided not to disclose it publicly, pointing to the queue instead, so
only a reader of the 10-Q body has the figure. Corroboration from a different issuer: Ethan
Allen disclosed receiving $5.0m of IEEPA refund cash inside its quarter ended 30 June 2026.

**Note the same mechanism appears on three separate names today** — HOFT (+7.0), RH (+5.5)
and ZUMZ (+3.0) are all IEEPA tariff-refund findings, and REF's largest negative (−3.0) is
the reverse side of it, a margin flattered by a refund that will not repeat. Four of today's
seventeen names are ranked substantially by one regulatory event. That is a correlated
exposure the scorer cannot see, and if the refund thesis is wrong it is wrong on all four at
once.

## The bottom name

**RENT −8.50** (Rent the Runway, bmo 2026-09-11). Four findings, the two largest at −3.0
each: the Q2 call is a **pre-recorded** conference call and webcast, the first in at least
four quarters (the three prior announcements all say "live webcast"), with the company under
an interim CEO — <https://www.globenewswire.com/news-release/2026/08/21/3349299/0/en/rent-the-runway-to-report-second-quarter-2026-results-on-september-11-2026.html>
(2026-08-21); and RENT drew a **$10,000,000 incremental term loan on 2026-09-01**, ten days
before the print and after quarter end, at a point where the minimum-liquidity covenant had
already been permanently removed and interest could be PIK'd — so there was no covenant to
cure and no cash interest to service —
<https://www.sec.gov/Archives/edgar/data/1468327/000095010326013373/dp252774_8k.htm>.

What the price already says: a great deal. The stock is at its 52-week low after a −28.5%
week and −23.4% over 20 days, and the hunter says so explicitly, sizing at roughly half the
18.2% median historical reaction because the two 8-Ks are demonstrably leaking into the
price. The control ranks RENT **second from the top** on that same drawdown. This is the
sharpest disagreement in today's table.

**AENT −7.50** sits just above it on a cleaner disagreement: the control is neutral on it
(+4.85) and the hunt's case is arithmetic — last June quarter's 15.8% gross margin was an
outlier against a 12.8% current run-rate, so AENT needs +23.5% revenue just to hold gross
profit flat.

## What nobody checked

**There is no adversary pass and no second hunter on any name.** Both were removed on
2026-09-09 after being measured as subtractive over 215 findings on six days. The
consequence, stated plainly: **a factually wrong finding entered this ranking at full size
and nothing in the run would have caught it.** The adversary was the only thing that ever
did — on 2026-09-09 it caught a covenant amendment misread by a year and a short-interest
claim contradicted by its own source. Today's table contains at least one finding of exactly
that shape (RENT's reading of which credit-agreement amendment removed the liquidity
covenant), and the only defence against it is that the hunter was warned and dated its own
source. That is not a check.

**And the key is not reproducible to better than its own size.** While the double hunt still
ran, twelve paired names came back with a median gap of 2.40 points and **four of the twelve
had opposite signs**, on a key whose typical magnitude is about 5. Nothing re-measures that
now. Read every number in the table above with that dispersion around it — including the
seven above the floor.

## Sign balance

**7 leaned positive, 10 leaned negative, none returned zero.** That is a milder negative tilt
than 2026-08-31's six-of-eight, but it still leans one way, and the standing worry applies:
asking hunters to find what the market has missed *into a print* may generate pessimism
rather than detect it. Only a count kept in every note makes that visible across days.

## How much of the baseline was measured rather than inferred

**7 of 17 names had a live option chain**: ORCL, ADBE, CPRT, KR, RH, LPTH, FEIM. For the
other ten, `priced_lean_pct` falls back to −0.05 × the 20-day run-up and the baseline's
"expected move" is a historical median rather than a priced expectation — so for those names
"what the market priced" is inferred, not measured.

Firing at 14:04 UTC (10:04 New York) did what it was meant to do at the top of the chain:
ORCL's ATM spread came back at **2.6% of mid**, ADBE 12.7%, CPRT 11.3% — real two-sided
quotes, against the 41%-of-mid weekend mark that motivated the timing change. It did not
rescue the tail: KR 30%, LPTH 22%, RH 59%, FEIM 79%, and the unusable ones ran to 100–189%.
Treat RH's and FEIM's implied moves as indicative only.

Note also that `edge_resolve.py`'s `spearman_vs_move_over_implied` normalises by that
expected move, so on a day where ten of seventeen names take the historical-median fallback,
it is not an implied-move measure.

## What the day would cost to trade

Capacity is in neither the scorer nor the budget, and today it is the headline caveat.

**Both extremes of the ranking are untradeable.** HOFT at the top turns over **$0.4m a day**
and RENT at the bottom **$0.2m a day**. Of the seven names above the conviction floor, four
trade under $5m a day: HOFT $0.4m, RENT $0.2m, AENT $0.1m, REF $4.4m. Only RH ($83m), ORCL
($3,397m) and FEIM ($13.2m) clear a $5m screen. Three of the seventeen — MNY, CMCM and
CSBR — trade under $100k a day and round to $0.0m in the table above; MNY is under $10k.

On the resolved sample a $5m turnover screen dropped 14 of 43 names, and the single best
trade in it (DLTH +23.20%) turned over $170k a day. A long top-third / short bottom-third
book built on today's table would put its two largest positions in names that cannot absorb
it. This is a research result. It is not a signal.

## One day is an anecdote

Seventeen names on one day cannot produce a meaningful rank correlation. The pooled figure
across many days is the result, and `edge_resolve.py --pool` is where it lives — pooling
within days, because concatenating raw pairs across days lets market-wide drift into the rank
structure and understates every ranker. On the six resolved runs the shipped ranking has not
been shown to beat the free control, and the honest summary of the stage's state is that its
one durable finding is the conviction floor, not the ordering.

Resolve this run after the 2026-09-11 close for the amc names and the 2026-09-14 close for
the bmo names:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-10/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'
```

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
