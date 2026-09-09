# Stage E — what the edge hunt's output actually measures

Seven runs exist: 2026-08-31 (two, one archived) and 09-01 through 09-08. Six are
resolved — **43 names, 249 findings, 65 hunts**. The 09-08 run's eight names are pending
the 2026-09-09 close. Run 1 of 08-31 (`edge/_run1-bmo/`) is excluded: its scores are a
`--legacy` re-score built from substituted midpoints with only 9 of 28 findings judged.

## How the pooling is done here, and why not the way the script does it

`edge_resolve.py --pool` concatenates every `(edge_score, move_pct)` pair from every day
and runs one Spearman. That lets day-level drift into the rank structure — on a day when
everything fell 8%, cross-day rank pairs carry market direction rather than the ranking's
own skill — and it also assumes each day's `edge_score` distribution is on a comparable
scale, which it is not.

Everything below converts each day to **within-day ranks**, centres them, and correlates
the centred ranks across days. That is a day-fixed-effect rank correlation: only ordering
inside a day can contribute. p-values come from permuting the realised moves **within
each day**, 20k draws.

The difference is not cosmetic. The script's own pooled figure for `edge_score` is
ρ=0.189 (p=0.224); done within days it is ρ=0.243 (p=0.156).

## The scorer's transformations subtract signal

| ranking key | ρ | p |
| --- | --- | --- |
| sum of finding impacts, pre-adversary | **+0.407** | **0.017** |
| sum of finding residuals, no multipliers | **+0.376** | **0.027** |
| hunt's own `expected_move_pct` (field the scorer never reads) | +0.341 | 0.044 |
| `priced_lean_pct` — baseline only, no hunting | +0.340 | 0.046 |
| minus 20-day run-up — free, no research at all | +0.335 | 0.050 |
| residual sum by cluster | +0.284 | 0.098 |
| cluster sum ÷ √k | +0.279 | 0.104 |
| `edge_pct` | +0.248 | 0.150 |
| **`edge_score` as shipped** | **+0.243** | **0.156** |
| `baseline_quality` | +0.074 | 0.681 |
| mean `priced_in_pct` | +0.046 | 0.800 |
| `confidence` | −0.090 | 0.605 |
| number of findings | −0.256 | 0.134 |

Read the middle of the table as a pipeline. Raw impact 0.407 → after the adversary 0.376
→ cluster-max 0.284 → ÷√k 0.279 → agreement discount and quality multiplier 0.243. Every
step lowers ρ, and the raw inputs clear p=0.05 while the shipped score does not.

Thirteen candidates were tested, so no single p here survives a Bonferroni correction.
That is the right caveat for the individual rows and the wrong one for the comparison:
the pre-registered question is whether `edge_score` ranks, and the answer is that it does
not clear significance on 43 names. The rest is exploratory.

### The gap between raw evidence and shipped score is robust

Paired bootstrap, resampling the six days with replacement:

| comparison | Δρ | 95% CI | P(Δ≤0) |
| --- | --- | --- | --- |
| impact sum − `edge_score` | +0.165 | [+0.082, +0.244] | 0.000 |
| residual sum − `edge_score` | +0.132 | [+0.053, +0.206] | 0.000 |
| impact sum − minus-run-up | +0.080 | [−0.164, +0.314] | 0.274 |
| impact sum − `priced_lean_pct` | +0.071 | [−0.097, +0.251] | 0.234 |
| hunt `expected_move_pct` − minus-run-up | +0.011 | [−0.224, +0.215] | 0.455 |

Two readings, and both matter.

**The machinery is measurably subtractive.** The first two rows exclude zero on every
resample. This is not a small-sample artefact any more: the aggregation in
`scripts/edge_score.py` costs the stage about 0.15 of rank correlation, which is the
difference between clearing 0.05 and not.

**The hunt has still not beaten a free control.** `-run_up_20d_pct` is one number from the
sealed baseline, available before any subagent is spawned, and it ranks at 0.335. The
hunt's raw evidence is ahead of it by 0.080 with a CI spanning zero. For six of the
resolved names `priced_lean_pct` *is* that run-up number, because with no option chain it
falls back to `-0.05 × run_up_20d_pct`; 18 of 43 resolved names have no chain at all.

Leave-one-day-out, pooled ρ:

| day dropped | `edge_score` | impact sum | minus run-up |
| --- | --- | --- | --- |
| 08-31 | +0.219 | +0.368 | +0.257 |
| 09-01 | +0.336 | +0.492 | +0.492 |
| 09-02 | +0.186 | +0.336 | +0.309 |
| 09-03 | +0.323 | +0.524 | +0.329 |
| 09-04 | +0.229 | +0.375 | +0.326 |
| 09-07 | +0.180 | +0.360 | +0.303 |
| none | +0.243 | +0.407 | +0.335 |

No single day carries the result, and the ordering of the three columns never changes.

## Traded, the ranking pays less than the free control

Long the top third, short the bottom third, per day:

| day | `edge_score` | impact sum | minus run-up |
| --- | --- | --- | --- |
| 08-31 | +3.02pp | +9.18pp | +15.65pp |
| 09-01 | −4.91pp | +20.16pp | +1.84pp |
| 09-02 | +13.19pp | +19.86pp | +17.64pp |
| 09-03 | −14.31pp | −10.47pp | +7.30pp |
| 09-04 | +3.88pp | +17.83pp | +12.56pp |
| 09-07 | +12.16pp | +12.16pp | +10.86pp |
| mean | **+2.17pp** | **+11.45pp** | **+10.97pp** |
| positive days | 4/6 | 5/6 | 6/6 |

Six days is not a backtest and these are gross of everything. The point is the column
order: the shipped ranking earns a fifth of what its own raw inputs earn, and the free
run-up control is positive on every day.

## The adversary judges well and sizes redundantly

Execution is clean across all seven runs: **249 of 249 findings judged**, `priced_in_pct`
spread 18 to 94, median 70, no bucket pile-up. The run-1 category collapse is genuinely
fixed and stayed fixed.

But the adversary also returns `size_check_pct`, which `edge_score.py` averages with the
hunter's number on the stated grounds that "where the two disagree badly the disagreement
is information". They do not disagree: median gap **0.60pp** over 249 findings. The
averaging is a rubber stamp. Whatever the adversary is worth, it is worth it through
`priced_in_pct` — and note that the pooled ρ of the residual sum (0.376, post-adversary)
is *below* the impact sum (0.407, pre-adversary), so on this sample the priced-in haircut
also costs ordering rather than adding it. That is the single most surprising number in
this file and it needs more days before anyone acts on it.

`priced_in_pct` cannot flip a finding's sign, so the finding-level direction rate is the
hunters' alone: **131 of 210 non-zero findings (62%)**.

## Magnitude is signed right and scaled wrong

The `expected_move_pct` the hunters volunteer — a summary forecast the scorer discards —
got the sign right on **35 of 55 hunts (64%)**, and on those 35 it under-scaled the move
by a median of **2.14×** (p25 1.07×, p75 4.15×; 54% of them off by more than 2×).

That is the same bias `backtest/RESULTS.md` measured on all three arms and
`claude_naive/README.md` warned about, and the live `claude_naive` ledger now shows it too
(median raw error 4.63pp against a 3.64pp proxy floor). Three independent measurements of
the same failure make under-scaling the most reproducible property in this repo.

The shipped `edge_pct` is not merely under-scaled, it is a different unit: on 08-31 it
ranged +0.04 to −0.58 points of spot against realised moves of 1.5% to 23%. `edge-note.md`
says so plainly and tells the reader not to read −11.5 as a forecast. Fine for a rank-only
measure, but the docstring's "the residual the market has not priced, in points of spot"
is not what the field contains.

## Two labelling defects

`edge_resolve.py` reports `spearman_vs_move_over_implied` and the docstring calls it "the
skill measure … dividing out how much each name was ever going to move". 18 of the 43
resolved names have no option chain, and for those the divisor falls back to
`baseline.expected_move_pct`, whose own basis field reads `median historical reaction (no
usable option chain)`. Rename it, or compute it only where a chain exists.

`confidence` and `baseline_quality` are presented as reader guidance and rank at −0.090
and +0.074. On 08-31 the name carrying that day's entire correlation (RZLV) had the run's
worst quality (0.07) and lowest confidence (5.0), while the highest-confidence name (MDT,
50.1) was uninformative. Selecting on confidence would have inverted the result.

## What seven runs cost

114 universe rows screened, 51 rankable, 43 resolved. 65 hunts and 1,107 unique hunt
sources, plus a full adversary pass on every one of 249 findings. Every run hit its
20-subagent cap and every run above ten names shed the rest.

## What the raw impact sum is

Each finding a hunter returns carries `expected_impact_pct`: the hunter's own signed
estimate, in percentage points of the share price, of what that one fact is worth **if
the market has not already priced it**. The adversary independently sizes the same fact
as `size_check_pct` and `edge_score.py` averages the two, but they barely differ (median
gap 0.60pp over 249 findings), so in practice the number is the hunter's.

The impact sum is those numbers added up per company. Nothing else. It is the ranking key
with every one of the scorer's five subsequent steps removed:

| step in `edge_score.py` | what it does | ρ after |
| --- | --- | --- |
| — | the impact sum itself | +0.407 |
| `× (1 − priced_in/100)` | haircut each finding by how much the adversary says is already in | +0.376 |
| cluster-max | two findings citing one domain count once, the largest | +0.284 |
| `÷ √k` | discount for correlation between the surviving clusters | +0.279 |
| `× 0.55` if it agrees with the price lean, `× (0.35 + 0.65·q)` for baseline quality | shrink evidence that merely repeats the price, and shrink thin names | +0.243 |
| `100·tanh(edge_pct/5)` | bound the scale for sorting; order-preserving, so ρ is unchanged | +0.243 |

So "the raw impact sum beats edge_score" means: the hunters' unadjusted sizes, summed,
order a day better than the same sizes after five defensible-sounding adjustments.

Two things it is **not**. It is not a forecast of the move — the same fact often appears
in two findings from two sources, and adding both double-counts it, which is exactly what
the cluster-max was built to stop. And it is not a claim that the adjustments are wrong in
principle; the priced-in haircut costing ordering (0.407 → 0.376) is the most
counter-intuitive number in this file and rests on six days.

## What money placed on it would have done

`scripts/edge_trade.py`. Entry is the close before the print, exit the close after the
first full session — the window `edge_resolve.py` already scores, held through the print.
The hunt fires at 16:04 CET, before that entry, so there is no look-ahead. Each strategy
is one unit of capital, so a long/short book splits it in half and a day's return is
`mean(long)/2 − mean(short)/2`, not the raw spread, which is 2× gross.

Gross of costs, six days, 43 names:

| strategy | mean/day | sd | t | bootstrap 95% CI | cumulative | up days |
| --- | --- | --- | --- | --- | --- | --- |
| `edge_score` L/S top-third | +1.09% | 5.23 | 0.51 | [−2.72, +4.80] | +6.0% | 4/6 (p=0.69) |
| impact sum L/S top-third | +5.73% | 5.80 | 2.42 | [+0.90, +9.17] | +38.6% | 5/6 (p=0.22) |
| minus run-up L/S top-third | +5.49% | 2.88 | 4.67 | [+3.28, +7.48] | +37.5% | 6/6 (**p=0.031**) |
| `edge_score` L/S on sign | +2.82% | 3.10 | 2.23 | [+0.36, +4.86] | +17.9% | 5/6 (p=0.22) |
| **always short — the null** | **+1.49%** | 3.27 | 1.12 | [−0.73, +4.03] | +9.0% | 3/6 (p=1.00) |

Four consequences, in the order that matters.

**The shipped ranking loses to doing no research.** `always short` needs no subagents, no
baselines and no findings, and returns more per day than `edge_score`'s long/short book.
This sample skewed down — 23 of 43 names fell, mean move −1.77% — and any short-tilted
book was flattered by that. It is the null the stage has to clear and on six days it does
not.

**Costs kill it and leave the alternatives standing.** At a flat 1.5% per unit of capital
per day, which is not pessimistic for names of this size held through a print,
`edge_score`'s book goes to −0.41%/day and −3.1% cumulative. The impact sum stays at
+4.23%/day, the run-up control at +3.99%.

**The best trade in the sample was uninvestable.** DLTH, ranked #1 on 09-02, moved +23.20%
and turns over **$170k a day** — spot $3.62 on 46,449 shares. Six of `edge_score`'s 22
positions traded under $1m a day. Screen the universe to names above $5m of daily turnover
and only 29 of 43 survive; `edge_score long the #1` then goes from +6.79%/day to
−1.29%/day, because the one position carrying it drops out. Nothing in this repo's budget
or scoring notices capacity, and the ranking is systematically drawn to the illiquid end
where information is genuinely least priced and least tradeable.

**Single-name risk is the whole book.** A top-third/bottom-third split on eight names is
four positions at 25% each, held over a print. The worst position was −20.04% (long CRDO
on 09-01) and the second worst −22.23% (short NX on 09-03). Borrow is not modelled at all:
shorting RZLV, CANG, MMED, ZEPP or DLTH is expensive where it is possible.

The one strategy with a defensible p-value is minus the 20-day run-up: positive on 6 of 6
days, sd of 2.88 against the others' 5+, sign test p=0.031. It uses no findings, no
adversary and no subagents. That is the number the stage is competing against, and the
reason to fix the scorer before buying another day of hunts.

Six days of 43 names in one regime is not a backtest, every figure here is gross of borrow
and slippage, and none of it is advice.

## Trading the raw impact sum

First, a defect this exposed. Five names — ABM, UNFI, WDH, CAN, GMHS — appear on **two**
edge days each: the 09-07 run re-hunts the same 09-08 prints the 09-04 run already
covered. So 43 rows are 38 events, and `edge_resolve.py --pool` counts those five twice
as if they were independent. Every figure below is given both ways.

Gross, long/short top-third, one unit of capital:

| | all 6 days (43 rows) | 5 independent days (38 events) |
| --- | --- | --- |
| impact sum | +5.73%/day, sd 5.80, t=2.42, CI [+0.90, +9.17], 5/6 up, cum +38.6% | +5.66%/day, sd 6.48, t=1.95, CI [−0.21, +9.79], 4/5 up, cum +30.6% |
| `edge_score` | +1.09%/day, t=0.51, 4/6 up, cum +6.0% | **+0.09%/day, t=0.04, 3/5 up, cum −0.1%** |
| minus run-up | +5.49%/day, sd 2.88, t=4.67, 6/6 up, cum +37.5% | +5.50%/day, sd 3.22, t=3.82, 5/5 up, cum +30.4% |
| impact sum, >$5m turnover | +6.52%/day, sd 2.22, t=7.20, 6/6 up, cum +46.0% | **+6.05%/day, sd 2.11, t=6.41, 5/5 up, cum +34.0%** |

`edge_score`'s entire positive return came from the duplicated day. The impact sum's
survives de-duplication almost intact, but its confidence interval now touches zero.

**The return is ordering, not the down-skew.** A top-third/bottom-third book is immune to
the day's drift by construction: adding a constant to every move leaves
`mean(long) − mean(short)` unchanged. Both legs contribute — after removing each day's own
mean, the long leg is +7.04%/day and the short leg +4.41%/day. That is the answer to the
`always short` null, which only looked competitive against `edge_score` because that
strategy earns nothing.

**Cost is not the binding constraint.** The impact-sum book breaks even at 5.73% per unit
of capital per day, against 1.09% for `edge_score`. At a flat 1.5% it still returns
+4.23%/day.

**Capacity is.** Under the $5m turnover screen the 18 positions have a median turnover of
$20.6m/day. At 5% of a day's volume per name that is roughly $1.0m per position and a $4m
book — real, and small. Push the screen to $20m and the edge disappears: +1.17%/day,
t=0.44, on 18 names across 4 days. That may be sample loss rather than a capacity
boundary, but on this evidence the return lives in the $5m–$20m band and nowhere above it.

**It does not clearly beat the free control.** +5.66%/day against the run-up's +5.50%,
with the run-up carrying lower volatility (sd 3.22 vs 6.48) and up on 5 of 5 days. Δρ is
+0.080 with a CI spanning zero, and 45% of the two strategies' positions are literally the
same names. Averaging the two within-day rankings gives ρ=0.409 — no better than the
impact sum alone — but +5.90%/day at sd 3.54 instead of 6.48. Same return, two-thirds the
volatility. If anything here were to be run forward, that is the version.

### The selection problem, priced honestly

The impact sum was chosen as the best of thirteen candidates *after* seeing the outcomes.
A max-statistic permutation test asks what the best of thirteen would reach by chance
under the null (moves shuffled within days, 20k draws):

| test | p |
| --- | --- |
| impact sum alone, two-sided | 0.017 |
| impact sum alone, one-sided | 0.008 |
| **best of 13 candidates ≥ 0.407, one-sided** | **0.056** |
| best of 6 trading strategies ≥ +5.73%/day | 0.016 |

Corrected for having gone looking, the ranking result sits just outside 0.05. It is a lead
worth running forward, not a finding. Five independent days, 38 events, one regime, gross
of borrow and slippage, and a strategy picked after the fact. None of it is advice.

## Can the impact sum call direction? No.

Ranking and direction are different questions, and the impact sum answers only the
first. Scored the way `claude_naive` scores — **buy at 20:00 CET (14:00 ET) on the last
session before the print, exit at the next open or the next close** — the sign of the
impact sum is a coin flip. `scripts/edge_direction.py`; the per-event table is below and
`docs/edge-direction.json` carries it machine-readable.

| exit | direction | binomial p | return/trade | sd | t | always-short on the same events | realised down |
| --- | --- | --- | --- | --- | --- | --- | --- |
| next open | 21/38 = **55%** | 0.314 | +1.81% | 10.53 | 1.06 | -0.39% | 19/38 |
| next close | 20/38 = **53%** | 0.436 | +1.08% | 11.34 | 0.59 | +2.11% | 20/38 |

On the close exit the always-short floor (+2.11%/trade) beats the impact sum (+1.08%),
and neither return is distinguishable from zero: t=1.06 and t=0.59 against a per-trade
standard deviation above 10 percentage points. `edge_score`'s sign does no better (57%
and 21/37), nor does the hunters' own volunteered `expected_move_pct` (55%).

**What does survive is size, not sign.** Predicted against realised: Pearson 0.448 and
Spearman 0.367 on the open exit, 0.380 and 0.320 on the close, with a median absolute
error of 6.11pp and 7.67pp. So the impact sum orders *how far* a name travels better than
it calls *which way* — the same split the pilot-40 backtest found on all three arms, and
the reason `edge_resolve.py` measures rank correlation rather than a hit rate.

It also explains why the long/short book works while the direction call does not. Under
this entry convention the top-third/bottom-third book still returns +3.75%/day to the open
and +4.45%/day to the close (against +5.73% on the close-to-close convention — entering at
14:00 ET rather than on the close costs about a point a day in pre-print drift), because
that book only ever trades the extremes of the ordering and never asks the middle 24 names
which way they are going.

### Every event, predicted against realised

Sorted by predicted return. `pred` is the impact sum in points of spot; both realised
columns are measured from the 14:00 ET entry.

| # | ticker | print | hunted | pred | → open | → close | sign open | sign close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SWBI | 2026-09-03 amc | 2026-09-03 | +16.30% | +14.84% | +5.57% | hit | hit |
| 2 | SPWH | 2026-09-01 amc | 2026-09-01 | +11.25% | +13.56% | +8.47% | hit | hit |
| 3 | DLTH | 2026-09-03 bmo | 2026-09-02 | +11.00% | +18.25% | +25.14% | hit | hit |
| 4 | MAMA | 2026-09-03 amc | 2026-09-03 | +8.25% | -1.84% | -5.38% | miss | miss |
| 5 | DELL | 2026-09-01 amc | 2026-09-01 | +5.25% | +8.36% | +15.43% | hit | hit |
| 6 | WOOF | 2026-09-02 amc | 2026-09-02 | +4.50% | +20.53% | -4.37% | hit | miss |
| 7 | NTSK | 2026-09-02 amc | 2026-09-02 | +3.70% | +14.21% | +4.71% | hit | hit |
| 8 | DOO | 2026-09-03 bmo | 2026-09-02 | +3.20% | +2.12% | +2.33% | hit | hit |
| 9 | CRDO | 2026-09-01 amc | 2026-09-01 | +2.35% | -10.44% | -21.46% | miss | miss |
| 10 | ASAN | 2026-09-03 amc | 2026-09-03 | +1.85% | -13.34% | -12.72% | miss | miss |
| 11 | AGX | 2026-09-02 amc | 2026-09-02 | +1.60% | +4.28% | +0.56% | hit | hit |
| 12 | FCEL | 2026-09-02 bmo | 2026-09-01 | +1.30% | -9.62% | -14.72% | miss | miss |
| 13 | AMBA | 2026-09-03 amc | 2026-09-03 | +1.00% | -3.15% | -3.63% | miss | miss |
| 14 | NIO | 2026-09-01 bmo | 2026-08-31 | +0.55% | -5.64% | -6.22% | miss | miss |
| 15 | MDB | 2026-09-01 amc | 2026-09-01 | +0.50% | -13.67% | -14.38% | miss | miss |
| 16 | MDT | 2026-09-01 bmo | 2026-08-31 | +0.08% | +3.35% | +1.22% | hit | hit |
| 17 | ABM | 2026-09-08 bmo | 2026-09-04 | -0.05% | -2.32% | +7.89% | hit | miss |
| 18 | MMED | 2026-09-01 bmo | 2026-08-31 | -0.30% | +2.51% | +12.41% | miss | miss |
| 19 | DOMO | 2026-09-03 amc | 2026-09-03 | -0.55% | -5.37% | +1.31% | hit | miss |
| 20 | AI | 2026-09-02 amc | 2026-09-02 | -1.40% | +2.58% | +4.06% | miss | miss |
| 21 | HMR | 2026-09-01 bmo | 2026-08-31 | -1.65% | -1.60% | -12.22% | hit | hit |
| 22 | WDH | 2026-09-08 bmo | 2026-09-04 | -1.90% | +10.29% | +4.90% | miss | miss |
| 23 | GTLB | 2026-09-01 amc | 2026-09-01 | -2.15% | +21.93% | +9.45% | miss | miss |
| 24 | UNFI | 2026-09-08 bmo | 2026-09-04 | -2.57% | +3.12% | +2.49% | miss | miss |
| 25 | PANW | 2026-09-01 amc | 2026-09-01 | -2.60% | -4.09% | -9.00% | hit | hit |
| 26 | LULU | 2026-09-03 amc | 2026-09-03 | -3.00% | -17.81% | -15.79% | hit | hit |
| 27 | ZEPP | 2026-09-01 bmo | 2026-08-31 | -4.40% | +1.63% | -8.54% | miss | hit |
| 28 | CANG | 2026-08-31 amc | 2026-08-31 | -4.50% | -13.21% | -23.06% | hit | hit |
| 29 | DLNG | 2026-09-08 bmo | 2026-09-07 | -4.80% | +2.98% | +4.61% | miss | miss |
| 30 | NX | 2026-09-03 amc | 2026-09-03 | -5.75% | +9.38% | +21.32% | miss | miss |
| 31 | YEXT | 2026-09-01 bmo | 2026-08-31 | -6.45% | +13.40% | -3.33% | miss | hit |
| 32 | PL | 2026-09-03 amc | 2026-09-03 | -7.25% | +5.93% | +1.37% | miss | miss |
| 33 | MEI | 2026-09-02 amc | 2026-09-02 | -7.90% | -16.40% | -15.29% | hit | hit |
| 34 | GMHS | 2026-09-08 bmo | 2026-09-04 | -8.25% | -13.36% | -3.47% | hit | hit |
| 35 | GOLD | 2026-09-02 amc | 2026-09-02 | -9.15% | -3.91% | -5.73% | hit | hit |
| 36 | CXM | 2026-09-02 bmo | 2026-09-01 | -9.20% | -4.52% | -10.19% | hit | hit |
| 37 | CAN | 2026-09-08 bmo | 2026-09-04 | -15.25% | -4.98% | -6.43% | hit | hit |
| 38 | RZLV | 2026-09-01 bmo | 2026-08-31 | -18.35% | -13.10% | -17.41% | hit | hit |

## Conviction is where the direction lives

The observation that the effect concentrates in the larger predictions is correct, and it
is the only result in this file that survives every robustness check I can run on 38
events.

The right test is the one with **no threshold in it**: does the rank of `|impact sum|`
correlate with whether the sign turned out right? One test, nothing chosen after the fact.

| exit | rank correlation, \|pred\| vs sign-correct | permutation p (within days) |
| --- | --- | --- |
| next open | +0.331 | 0.046 |
| **next close** | **+0.514** | **0.0015** |

Above the median prediction the sign is right on 74% of events to the close and 68% to the
open. Below it, it is a coin flip. As a threshold, the same thing:

| threshold | n | direction (close) | return/trade | sd | t | bootstrap 95% CI | after 1.5% cost | median turnover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 38 | 20/38 = 53% | +1.08% | 11.34 | 0.59 | [−2.48, +4.65] | −0.42% | $20.0m |
| \|pred\| ≥ 1 | 32 | 19/32 = 59% | +2.57% | 11.54 | 1.26 | [−1.46, +6.44] | +1.07% | $16.2m |
| \|pred\| ≥ 2 | 25 | 17/25 = 68% | +4.38% | 11.68 | 1.87 | [−0.20, +8.78] | +2.88% | $10.9m |
| **\|pred\| ≥ 3** | **21** | **16/21 = 76%** | **+6.37%** | 10.64 | 2.74 | **[+1.80, +10.72]** | +4.87% | $6.9m |
| \|pred\| ≥ 5 | 14 | 11/14 = 79% | +6.31% | 11.22 | 2.10 | [+0.32, +11.70] | +4.81% | $7.5m |
| \|pred\| ≥ 8 | 9 | 8/9 = 89% | +8.56% | 8.64 | 2.97 | [+3.38, +14.11] | +7.06% | $6.9m |

Even correcting for having searched seven thresholds, the best of them clears: a
max-statistic permutation test gives family-wise p=0.032 to the open and 0.034 to the
close.

**Why this is a design property rather than a mined cut.** The impact sum is a conviction
measure, not a probability. A near-zero value means the hunters found nothing on net —
often two findings of opposite sign that cancel — and asking a no-view to call direction is
meaningless. Conditioning a directional call on conviction is what any forecasting system
with an abstain option does. That is also why the threshold-free rank test is the right
test here, and it is the one that comes back at p=0.0015.

### Four things it is not

**Not one lucky day.** The nine events above \|pred\| = 8 are spread over five hunt days;
the five above 10 are one name on each of five different days.

**Not the microcaps.** The large-prediction bucket has a *median* turnover of $7.5m with 3
of 12 names under $1m. The small-prediction bucket has a median of $69.9m. The conviction
effect runs the opposite way from the capacity problem — the names the hunters have most to
say about are mid-small, but they are not the $170k-a-day tail.

**Not a volatility proxy.** If large predictions simply landed on names that move a lot,
the return would rise while the hit rate stayed at 50%. The hit rate is what rises, and the
\|pred\| ≥ 6 bucket has the *smallest* median realised move of the four (6.08% against
7.05–9.00%).

**Not a property of the shipped score.** Run the identical test on `|edge_score|` and the
rank correlation is +0.077 to the open and −0.003 to the close. The scorer's cluster-max,
√k discount, agreement discount and quality multiplier destroy the conviction signal along
with the ordering — `edge_score`'s magnitude carries no information about whether its own
sign is right. That is the fourth independent way the aggregation has now been shown to be
subtractive.

### The one blemish

The relationship is monotone across the buckets except for a dip below chance in the middle:

| \|pred\| bucket | n | direction, open | direction, close | return/trade (close) |
| --- | --- | --- | --- | --- |
| 0 – 1 | 6 | 3/6 (50%) | 1/6 (17%) | −6.83% |
| 1 – 3 | 11 | 3/11 (27%) | 3/11 (27%) | −4.69% |
| 3 – 6 | 9 | 6/9 (67%) | 6/9 (67%) | +4.40% |
| 6 – 20 | 12 | 9/12 (75%) | 10/12 (83%) | +7.86% |

A pure conviction story predicts the middle bucket near 50%, not 27%. Three of eleven is
noise-compatible (two-sided p=0.45) and the names in it are a genuinely mixed bag —
CRDO +2.4 predicted against −21.5 realised, FCEL +1.3 against −14.7, GTLB −2.1 against
+9.4. But if the inversion persists as days pool, the honest reading changes from "weak
conviction is uninformative" to "weak conviction is anti-informative", which would be a
different and more interesting finding.

### What this changes

The stage should emit the impact sum, and a reader should act on it only above a conviction
floor. Concretely: carry `impact_sum` into `edge-scores.json`, keep `edge_score` as a
diagnostic, and have `edge_resolve.py` report the threshold-free rank correlation between
\|prediction\| and sign-correctness beside the ranking correlation it already reports. That
number is the one to watch as days accumulate, because it needs no cut and no calibration.

Still 38 events on six days in one regime, gross of borrow and slippage. But this is the
first result in the stage that is significant on a test chosen before looking, robust to
day-clustering, liquidity and volatility, and mechanically explicable. It is worth running
forward properly.

## What to change

1. Score on the sum of finding impacts, or on the residual sum. Keep `edge_score` as a
   secondary column; the paired bootstrap says the multipliers cost 0.15 of ρ.
2. Add `-run_up_20d_pct` and `priced_lean_pct` as mandatory control columns in
   `edge_resolve.py`, per day and pooled. A run that does not beat them has established
   nothing, and right now none has.
3. Pool within days, not across them. The current pooled figure understates every ranker.
4. Carry the hunters' `expected_move_pct` into `edge-scores.json` and resolve it.
5. Drop the hunter/adversary size average; record the disagreement separately.
6. Rename `spearman_vs_move_over_implied`, or restrict it to names with a chain.
7. Stop presenting `confidence` and `baseline_quality` as reader guidance until they
   correlate with something.
