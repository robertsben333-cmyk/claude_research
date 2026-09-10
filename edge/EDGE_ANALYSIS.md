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
`edge/scripts/edge_score.py` costs the stage about 0.15 of rank correlation, which is the
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

`edge/scripts/edge_trade.py`. Entry is the close before the print, exit the close after the
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
impact sum is a coin flip. `edge/scripts/edge_direction.py`; the per-event table is below and
`edge/analysis/edge-direction.json` carries it machine-readable.

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

**Read "The double hunt inflates both headline numbers" below before quoting any number in
this section.** Every one of the 38 events was scored in a regime where the day's two
highest-`hunt_priority` names got two hunters and the rest got one, and the key is a sum, so
those names carry the largest conviction by construction. Rebuilt at one hunter per name —
which is how the stage has run since 2026-09-09 — the conviction correlation below falls
from +0.514 (p=0.002) to +0.361 (p=0.045). Inflated by about a third, not manufactured.

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

## The double hunt inflates both headline numbers; it does not manufacture them

Until `a109692` on 2026-09-09, `config/pipeline.yaml` set `double_hunt_top_n: 2`: the two
names with the highest `hunt_priority` got two independent hunters, everything else got
one. The key is a **sum** of signed per-finding sizes, so a second hunter adds findings and
pushes the name further from zero for free. Across the 38 de-duplicated events, 10 were
hunted twice:

| | n | mean findings | mean \|impact\| | median \|impact\| | mean `hunt_priority` |
| --- | --- | --- | --- | --- | --- |
| double-hunted | 10 | 8.00 | 9.13 | 9.18 | 77.2 |
| single-hunted | 28 | 3.71 | 3.53 | 2.80 | 59.9 |

So the day's largest convictions sit on the day's most-hunted names by construction, and
those are the names the sweep rated most promising. `edge/scripts/edge_hunter_control.py` runs
the separations the data allows; `edge/analysis/edge-hunter-control.json` is its output.

### Dropping the double-hunted names is the wrong control

The obvious test — restrict to the 28 single-hunted names — is selection on
`hunt_priority`, which the sweep assigns **before any hunting**. The survivors are not "the
same names without the doubling", they are the names the sweep rated lowest: mean priority
59.9 against 77.2. On that subsample conviction falls to ρ=+0.270 (p=0.29) to the close and
zero to the open, and the ranking correlation to +0.042 (p=0.87). Both numbers are real and
both are statements about the low-priority half of the sample, where the hunt has least to
say and the predictions are smallest. They are not a de-confounded estimate of anything.

### The right control: rebuild every name's key from one hunter

Each finding in `edge-scores.json` carries the hunter that produced it, so a double-hunted
name's key can be rebuilt from one hunter's findings alone. That holds the population at all
38 events, drops nothing, and puts every name at one hunter — which is exactly how the stage
runs from 2026-09-09. The hunters run in parallel, so "A" and "B" are labels, not an order;
both are shown.

| key | conviction ρ (close) | p | ranking ρ | p |
| --- | --- | --- | --- | --- |
| hunter A only | +0.361 | 0.045 | +0.303 | 0.099 |
| hunter B only | +0.299 | 0.076 | +0.343 | 0.062 |
| mean of the two hunters | +0.442 | 0.010 | +0.326 | 0.077 |
| **full sum, as published** | **+0.514** | **0.002** | **+0.360** | **0.048** |

(The ranking column is on the 38 de-duplicated events, so the published key reads +0.360
here and +0.407 on the 43 rows with duplicates.)

**Both effects survive the counterfactual at roughly 60–85% of their published size.** The
doubling inflates the estimate; it does not create it. Conviction on a single hunter's key
still clears p=0.05 on one draw and misses on the other, and the ranking sits at +0.30 to
+0.34 with p around 0.06–0.10.

The ordering is itself informative: full sum > mean of hunters > either hunter alone, on
conviction. Averaging two independent hunters beats one, which is what noise reduction looks
like, and summing them beats averaging, which says the extra magnitude the double hunt gave
the sweep's favourites was earned rather than spurious. On ten pairs that is a lead, not a
finding — but it argues against the reading that the double hunt was free inflation, and it
sits awkwardly beside the decision to remove it.

### What the second hunter actually did

| day | ticker | hunter A | hunter B | full | realised move |
| --- | --- | --- | --- | --- | --- |
| 08-31 | MMED | +1.25 | −1.55 | −0.30 | +10.66 |
| 08-31 | RZLV | −6.25 | −12.10 | −18.35 | −17.30 |
| 09-01 | SPWH | +6.75 | +4.50 | +11.25 | +6.67 |
| 09-01 | CXM | −5.15 | −4.05 | −9.20 | −8.55 |
| 09-02 | MEI | +2.85 | −10.75 | −7.90 | −15.36 |
| 09-02 | GOLD | −8.15 | −1.00 | −9.15 | −5.34 |
| 09-03 | SWBI | +7.40 | +8.90 | +16.30 | +5.05 |
| 09-03 | AMBA | +2.00 | −1.00 | +1.00 | −0.77 |
| 09-04 | UNFI | −3.12 | +0.55 | −2.57 | +2.28 |
| 09-04 | CAN | −5.25 | −10.00 | −15.25 | −10.28 |

The two hunters agree on sign on **6 of 10** names, with a median gap of 3.34 points on a key
whose typical size is about 5. The second hunter moves \|key\| by a median +4.28 points. And
it buys no direction: hunter A alone is sign-correct on 7 of 10, both hunters summed on the
same 7 of 10. What the second hunt adds is magnitude and, on the evidence of the table above,
a better-ordered magnitude — not a corrected sign.

### Traded, averaging the hunters pays nothing

The ranking advantage of the mean over one hunter (+0.442 against +0.361) does not reach
money, because a trade is taken on the **sign** and the mean and the sum share a sign on
every name — the mean can only differ where magnitude selects. Entry 14:00 ET on the last
session before the print, exit the next close, every name at sign(key), equal weight, gross:

| key | n at \|key\| ≥ 3 | sign | ret/trade | t | bootstrap 95% CI | day book |
| --- | --- | --- | --- | --- | --- | --- |
| full sum (published) | 21 | 16/21 | +6.37% | 2.74 | [+1.82, +10.60] | +5.66%/day |
| mean of hunters | 21 | 16/21 | +6.37% | 2.74 | [+1.82, +10.60] | +4.79%/day |
| hunter A only | 21 | 15/21 | +5.53% | 2.39 | [+1.02, +9.90] | +4.30%/day |
| hunter B only | 20 | 15/20 | +6.41% | 2.62 | [+1.63, +10.98] | +4.68%/day |

(Day book is long the top third, short the bottom third, close-to-close, capital halved.
Always-short on the same 38 events returns +2.11% per trade.)

Against the published key the mean is **identical** at the floor — halving the ten paired
names leaves all seven of them above 3.0, so the same 21 names are traded — and **worse** in
the day book, +4.79% against +5.66%, because shrinking the sweep's favourites pulls them out
of the day's extremes where they were earning.

Against a single hunter the mean is worth +0.84pp per trade at the floor (paired bootstrap
CI [+0.00, +2.32]). But hunter B alone beats hunter A by +0.88pp on the same cut — the same
size as the gain from averaging. On ten pairs, what you gain by averaging two hunters is
indistinguishable from which one you happened to draw.

And the combination does not fix disagreement. The two hunters differed on sign on 4 of the
10 paired names (MMED, MEI, AMBA, UNFI); summing them landed on the correct sign for **1 of
those 4**. Where the hunters agree the second one adds nothing to the sign, and where they
disagree the sum does not adjudicate. The noise-reduction reading above is a statement about
ordering conviction, not about the money, and it should not on its own reopen the double
hunt.

### The floor, re-derived on one hunter per name

`conviction_floor: 3.0` was derived from 16/21 = 76% at +6.37% per trade, t=2.74. On the
counterfactual key — hunter A only, all 38 events:

| threshold | n | share | sign (close) | ret/trade | bootstrap 95% CI | always-short |
| --- | --- | --- | --- | --- | --- | --- |
| all | 38 | 100% | 20/38 = 53% | +0.93% | [−2.69, +4.51] | +2.11% |
| \|pred\| ≥ 1 | 33 | 87% | 19/33 = 58% | +1.94% | [−1.92, +5.93] | +2.12% |
| \|pred\| ≥ 2 | 26 | 68% | 16/26 = 62% | +2.89% | [−1.61, +7.43] | +2.01% |
| **\|pred\| ≥ 3** | 21 | 55% | **15/21 = 71%** | **+5.53%** | **[+1.02, +9.90]** | +0.58% |
| \|pred\| ≥ 5 | 13 | 34% | 10/13 = 77% | +5.62% | [−0.61, +11.36] | −1.95% |
| \|pred\| ≥ 8 | 4 | 11% | 3/4 | +7.24% | [−2.60, +19.72] | −2.64% |

**The floor holds.** 3.0 is still the cut where the return CI clears zero, it still selects
about half the day (21 of 38, against 21 of 38 on the published key), and it still beats
always-short by a wide margin. What it rests on is 15/21 at +5.53% rather than 16/21 at
+6.37% — a haircut, not a reversal. There is no case for moving the value.

For completeness, on the low-priority subsample (single-hunted names only) the same cut gives
9/14 at +4.62% with a CI of [−1.62, +10.79]. That is the weakest defensible reading of the
floor and the one to quote if the question is specifically about names the sweep rates low.

### What is left

- Both headline numbers are **inflated by roughly a third** by the double hunt and survive
  its removal: conviction +0.361 (p=0.045) and ranking +0.303 (p=0.099) with one hunter per
  name, against +0.514 and +0.360 as published.
- Hunter count on its own predicts sign-correctness at only +0.208 (p=0.222), and
  `hunt_priority` at +0.224 — neither is doing the work, though the second is a free number
  worth watching.
- Two hunters on one name disagree on sign 4 times in 10 and add no direction skill (7/10
  either way). The key's reproducibility remains the stage's least-measured property.
- Nothing in this sample separates "a second opinion helps" from "the sweep picked well",
  because the two were assigned together. Days under `double_hunt_top_n: 0` will settle it;
  a deliberate double-hunt week would settle it faster and is wanted anyway.

Quote the published figures with the counterfactual beside them, not on their own.

## What `impact_sum` is, precisely — and the sizing correction of 2026-09-09

The 2026-09-09 edge-hunt run caught a discrepancy between this file and the code, and
resolving it changed the code rather than the prose.

`edge/scripts/edge_score.py` used to re-size every finding to the **mean** of the hunter's
number and the adversary's independent `size_check_pct` before summing. So the ρ=0.407
reported above was measured on the averaged sizes, not on the hunters' own — every
description of the key as "the hunters' signed per-finding sizes" was wrong about which
number it summed. Measured both ways over the same 43 names:

| the key sums | ρ | permutation p |
| --- | --- | --- |
| the mean of hunter and adversary (what the code did) | +0.407 | 0.014 |
| **the hunter's own number (what the docs claimed)** | **+0.453** | **0.006** |

They differ by a median of 0.80 points per name, are identical on 1 of 43, and reorder the
day on 4 of 6 days. So the averaging was not cosmetic and it was costing ordering. The key
now sums the hunter's number; `adversary_size_pct` and `size_disagreement_pct` sit beside
it, where a real disagreement stays visible instead of being split down the middle. On
2026-09-09 KEQU's hunter sized a finding at −4.0 against the adversary's −15.0 and that
name's rank turned on which was used. `edge_score_legacy` still reads the averaged value,
so it reproduces the pre-2026-09-09 key exactly — verified to 0.05 on all five names of
2026-09-04.

### Is it the predicted return?

Nearly, in scale; not at all, in precision. Regressing the realised move on the key over
the 38 de-duplicated events:

| exit | regression | pearson | median abs error | sd predicted vs realised |
| --- | --- | --- | --- | --- |
| next open | realised = +1.37 + **0.76** × predicted | +0.459 | 6.25pp | 6.48 vs 10.68 |
| next close | realised = −1.18 + **0.72** × predicted | +0.414 | 7.00pp | 6.48 vs 11.19 |

Above the conviction floor the slope tightens to 0.93 (open) and 0.86 (close) on 22
events. So the number is not systematically half or double the move — it is roughly
one-for-one, which is more than a pure ranking key needs to be. What it is not is a point
forecast: R² is about 0.2 and the typical miss is 6 to 7 points of spot against a realised
standard deviation near 11.

Three structural reasons it cannot be read as a forecast, whatever the slope says.
It sums "what this fact is worth **if the market has not priced it**" without subtracting
what is priced — that subtraction is `residual_sum`, and it sits in diagnostics because it
*lowered* measured ordering. It double-counts: the same fact reaching two findings from two
sources is added twice, and on 2026-09-09 all eight adversaries independently reported that
the findings on their name overlapped. And its dispersion is too narrow — a predicted
standard deviation of 6.5 against a realised 11.2 — so even a perfectly ordered table
understates how far the tails travel.

Read it as a conviction-weighted ranking that happens to be scaled in the right units.

## Two things the pre-earnings drift and the naive arm do not do

### (a) The two-day run-in does not predict whether the hunt is right

Measured on the 37 de-duplicated events carrying a non-zero prediction, with the run-in
taken from the close two sessions before the entry to the 14:00 ET entry price itself, so
nothing after the trade is in it.

| | rank correlation with sign-correct |
| --- | --- |
| signed 2-day run-in, exit open | −0.046 |
| signed 2-day run-in, exit close | −0.041 |
| \|2-day run-in\|, exit close | +0.148 |
| signed 1-day run-in, exit close | −0.066 |

Nothing. By bucket the hit rate reads 62% / 50% / 50% / 75% across run-ins below −3%,
−3–0%, 0–3% and above +3% — no shape, and the top bucket holds four names.

The one pattern with any size is agreement: where the run-in and the prediction point the
same way the sign is right on 12 of 18 (67%, p=0.119) against 9 of 19 (47%) when they
oppose, worth +4.80% against −1.00% per trade. But the same split on the **open** exit
gives 50% against 58% — it reverses. A signal that flips when you change the exit by six
hours is noise, and it is recorded here so nobody rediscovers it.

As a standalone ranking the two-day run-in is worth ±0.017 against the realised move,
against +0.335 for minus the **20-day** run-up on the same days. That contrast is the
finding worth keeping: the reversal effect that does rank these days is a month-scale
phenomenon and there is nothing usable at two days.

### (b) The naive arm and the edge hunt are independent, and only one of them has signal here

They overlap on 16 events — 42% of the edge sample, 52% of the scored naive sample —
because they select differently: `claude_naive` takes the day's largest by market cap and
the edge hunt takes the highest `hunt_priority`, which is close to a measure of obscurity.
On the 16 shared events:

| | signed forecast vs realised | median abs error | magnitude vs \|realised\| |
| --- | --- | --- | --- |
| edge `impact_sum` | pearson **+0.400** | 5.48pp | +0.318 |
| naive `direction_score` × expected move | pearson −0.109 | 8.41pp | −0.108 |
| 50/50 blend | +0.328 | 7.03pp | +0.152 |

The two predictions correlate at only +0.163, so they genuinely see different things — but
the blend is worse than the edge hunt alone, because on this subsample the naive arm's
signal is not merely different, it is absent. There is nothing to combine with.

Their errors correlate at +0.855, which looks damning and is mostly mechanical: the
realised move has a standard deviation near 11 against forecast dispersions of 6.5 and
below, so two under-dispersed forecasts share most of their error by construction. Read
the +0.163 between the predictions, not the +0.855 between the errors.

One caveat that cuts the other way. Over its own full 31 scored events the naive arm ran
60% direction and +1.80% per trade; the −0.109 above is a 16-event slice chosen by the
edge hunt's selection rule, not a verdict on the method. What the slice does establish is
that **on the names the edge hunt picks, the naive arm adds nothing** — and it largely
agrees, by abstaining: of the seven overlapping names above the conviction floor, naive
called Neutral on four (CXM, DELL, PL, RZLV).

So they are complementary in coverage and not in signal. Keep them separate, as
`CLAUDE.md` already requires, and do not average them.

## Is the adversary doing anything? Measured: no, and it costs 8 of 20 agents

The adversary produces three things. Two are numbers, and both have now been measured as
subtractive; the third is prose.

**`size_check_pct`** — demoted 2026-09-09. Summing the hunter's own size ranks at 0.453
against 0.407 for the mean of the two.

**`priced_in_pct`** — every way of letting it touch the ranking makes the ranking worse,
and monotonically so:

| the key sums | ρ | p |
| --- | --- | --- |
| every finding at the hunter's size — **the key as shipped** | **+0.453** | 0.007 |
| × (1 − priced_in/100), the haircut | +0.325 | 0.060 |
| findings with priced_in ≥ 90 dropped | +0.407 | 0.016 |
| ≥ 85 dropped | +0.402 | 0.019 |
| ≥ 80 dropped | +0.328 | 0.054 |
| ≥ 70 dropped | +0.221 | 0.200 |
| only findings with priced_in ≤ 50 kept | +0.305 | 0.075 |

Read the monotonicity, not any single row: the more the adversary is allowed to remove,
the worse the day sorts. Its own summary statistic, mean `priced_in_pct` per name, ranks
at +0.046. So the adversary's judgment of *what the market already knows* does not
correlate with *which names move*, in any form, at 215 findings over six days.

**And since the 2026-09-09 rewrite it reaches the output through neither channel.**
`impact_sum` sums hunter sizes; `conviction` is its absolute value; `rankable` comes from
the sweep. Everything the adversary returns lands in `diagnostics` and in the note's
prose. Eight subagents a day, 40% of the stage's cap, currently changing nothing that is
ranked, scored or resolved.

### What it does that the numbers do not capture

It catches findings that are factually wrong. On 2026-09-09 it broke LMNR-h1#2 — the
covenant amendment defers to October 2027, not October 2026, so the mechanism cannot reach
this print — and FLWS-h1#1, whose "the short base has not moved" was contradicted by its
own source (9.30m shares in March against 7.75m in August), and which re-reported four
sealed-baseline fields as discoveries. Those are real errors and nothing else in the stage
would have found them.

But note what happens to them now: a refuted finding still enters `impact_sum` at full
size, because the only lever the adversary has is `priced_in_pct` and that no longer feeds
the key. Both of those corrections changed the 09-09 ranking by exactly zero.

### The decision: removed outright, and the double hunt with it

The adversary is gone — no daily pass and no weekly audit. So is the double hunt on the
top two names, which failed the same test: over six runs it paired twelve names, and the
gap between the two hunters predicted neither the eventual error (rank correlation +0.203)
nor whether the sign was right (+0.028), at n=12. Two slots for no signal.

The stage is now one sweep and one hunter per name, 19 names against the old 8.

| | before | after |
| --- | --- | --- |
| sweep | 1 | 1 |
| hunters | 10 (8 names + 2 double) | 19 (19 names) |
| adversaries | 8 | 0 |
| **names ranked** | **8** | **19** |

**Two things are knowingly given up, and both belong in every note from here.**

*Nothing checks a finding for being factually wrong.* The adversary was the only thing
that did — on 2026-09-09 a covenant amendment misread by a year, and a "the short base has
not moved" claim contradicted by its own source. Those now enter the key at full size. The
fix, when hunter reliability starts to show, is the hunter prompt.

*Nothing measures how reproducible the key is.* While the double hunt ran, twelve paired
names came back with a **median gap of 2.40 points and four of twelve carrying opposite
signs**, on a key whose typical magnitude is about 5. Run the same name twice and a third
of the time you get the other direction. That is a property of every ranking the stage has
ever produced, it is now unmeasured, and a tidy table should not be read as implying a
precision the key does not have. Re-run a double-hunt week occasionally rather than letting
the number rot.

Both are accepted for the same reason: a check with no path to the output is not a check,
and sample size is what every open question in this file is waiting on. Nineteen names a
day against eight gets there roughly two and a half times faster.

## The exit is in the wrong place for half the names

Everything above scores one window: the regular close before the print to the regular
close after the first full session. That holds the print through a whole session of
trading, which is a choice nobody in this repo ever made deliberately — it is what
`realised()` in `edge_resolve.py` happened to compute. The question is whether the hunt's
findings are about the **initial repricing** and everything after it is other people's
news. `edge/scripts/edge_exit.py` re-resolves all 38 de-duplicated events at eight exit
horizons against the same unchanged entry, off 5-minute Yahoo bars with
`includePrePost=true`. Output in `edge/analysis/edge-exit.json`.

| exit | ρ (impact sum) | p | conviction ρ | floor book | t | median share of the close move |
| --- | --- | --- | --- | --- | --- | --- |
| after-hours / early pre-market | +0.230 | 0.221 | +0.255 | +5.16% | 2.75 | 0.46 |
| pre-open indication | +0.360 | 0.047 | +0.342 | +6.61% | 3.17 | 0.68 |
| opening print | +0.315 | 0.071 | +0.365 | +6.21% | 2.99 | 0.69 |
| open + 15 min | +0.272 | 0.120 | +0.389 | +4.31% | 2.26 | 0.78 |
| open + 30 min | +0.270 | 0.151 | +0.526 | +5.16% | 2.62 | 0.82 |
| open + 60 min | +0.303 | 0.092 | +0.395 | +4.59% | 2.37 | 0.75 |
| midday | +0.305 | 0.101 | +0.511 | +4.24% | 2.03 | 0.93 |
| **first close (current)** | **+0.375** | **0.029** | +0.440 | **+5.80%** | 2.57 | 1.00 |

"Floor book" is the `|impact_sum| >= 3` trade of the conviction section above, signed by
the prediction. A paired day bootstrap of each horizon minus the close puts every Δρ
between −0.15 and −0.02 with a CI spanning zero, and every Δ return between −1.7pp and
+0.7pp, also spanning zero. **Read flat: no uniform early exit is distinguishable from
holding to the close.** The family-wise p over the eight horizons is 0.115 for the best ρ
and 0.007 for the best conviction ρ.

### The legs say something the horizons hide

Split the hold into its two legs and the flatness turns out to be two effects cancelling.

| leg | ρ | floor book | t | day-demeaned | mean abs move |
| --- | --- | --- | --- | --- | --- |
| entry → opening print (the gap) | +0.315 | +6.21% | 2.99 | +5.31% | 8.36% |
| opening print → close (the session) | +0.078 | −0.20% | −0.11 | −0.19% | 5.99% |

The gap pays the whole thing. The session leg carries 6 points of movement per name and
pays nothing for it. On the pooled sample that is an argument about risk, not return:
same money, roughly 40% less of the move sat through.

### amc and bmo want opposite exits

| | gap ρ | gap book | session ρ | session book | session book, day-demeaned |
| --- | --- | --- | --- | --- | --- |
| **amc** (n=21, 12 in the book) | +0.273 | **+8.91%** | **−0.351** | **−3.00%** | −2.61% (t=−1.56) |
| **bmo** (n=17, 10 in the book) | +0.187 | +2.96% | +0.319 | +3.16% | +1.60% (t=1.01) |

An amc print gets a full overnight of processing, so the opening auction is already the
informed price and the session that follows takes 3 points back off a book that earned
8.9 overnight. A bmo print gets two thin hours of pre-market instead, and the session goes
on repricing in the same direction: `edge_score`'s ρ for bmo names is +0.187 at the open
and +0.670 at the close.

Two checks the split has to survive, and does, partly. The amc floor book is six long and
six short, so its session loss cannot be the sample's downward drift — day-demeaning moves
it from −3.00% to −2.61%. The bmo book is eight short and two long, and day-demeaning
halves its session gain from +3.16% to +1.60%, so **half of what makes bmo look like a
hold is the day's average drift caught by a short-heavy book**, and neither bmo leg is
significant on its own.

### The same question in money, hour by hour

Rank correlation is not a return, and on the exit question the two disagree: ρ peaks at the
close while the money peaks before the open. `edge/scripts/edge_exit.py` also prices every hour
of the clock from the entry close (16:00 ET) to the next close, 24 hours later. The book is
the same one: every name with `|impact_sum| >= 3`, signed by the prediction, one unit per
name, mean **per trade**. Chart in `edge/analysis/edge-exit-hourly.html`.

| exit (ET) | hour | both | t | amc | bmo | long/short per day | short-all per day | priced |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17:00 | 1 | +4.07 | 2.78 | +7.39 | +0.09 | +2.99 | −0.57 | 38 |
| 18:00 | 2 | +4.13 | 2.92 | +7.22 | +0.43 | +3.15 | −0.62 | 38 |
| 19:00 | 3 | +4.19 | 2.86 | +7.42 | −0.13 | +2.81 | −0.51 | 37 |
| 20:00 | 4 | +4.25 | 2.92 | +7.67 | +0.13 | +3.48 | −0.68 | 38 |
| 04:00 | 12 | +4.18 | 2.43 | +7.18 | −0.32 | +2.05 | −1.60 | 35 |
| 05:00 | 13 | +3.48 | 1.93 | +6.40 | −0.90 | +1.47 | −1.81 | 35 |
| 06:00 | 14 | +3.90 | 1.89 | +6.89 | −0.59 | +2.98 | −1.98 | 33 |
| 07:00 | 15 | +5.40 | 3.30 | +7.44 | +2.67 | +3.04 | −0.61 | 37 |
| 08:00 | 16 | +5.50 | 2.88 | +8.06 | +2.09 | +3.38 | −0.76 | 37 |
| **09:00** | 17 | **+6.38** | **3.54** | **+8.45** | +3.61 | +4.73 | −0.62 | 37 |
| 09:35 | 17.5 | +4.72 | 2.69 | +7.08 | +1.89 | +4.44 | +1.05 | 38 |
| 10:00 | 18 | +4.49 | 2.52 | +6.08 | +2.58 | +3.78 | +2.51 | 38 |
| 11:00 | 19 | +4.25 | 2.25 | +4.83 | +3.55 | +3.68 | +1.90 | 38 |
| 12:00 | 20 | +4.53 | 2.22 | +4.93 | +4.05 | +4.19 | +1.75 | 38 |
| 13:00 | 21 | +4.44 | 2.26 | +5.14 | +3.60 | +4.09 | +1.91 | 38 |
| 14:00 | 22 | +4.88 | 2.56 | +5.09 | +4.63 | +4.61 | +2.03 | 38 |
| 15:00 | 23 | +5.28 | 2.49 | +5.28 | +5.29 | +4.93 | +1.78 | 38 |
| **16:00** | 24 | +5.60 | 2.52 | +5.07 | **+6.23** | +4.77 | +1.96 | 38 |

Hours 5 to 11 are the overnight void: the last price still exists, an exit does not. The
17.5 row is the close of the 09:30 bar rather than the opening print, which is why it reads
+4.72 against the +6.21 the opening auction itself pays — five minutes of session gives back
1.5 points.

Three things the clock shows that the eight-horizon table does not.

**amc is finished before the bell.** +7.39 an hour after its own print, flat through the
night, a peak of **+8.45 at 09:00**, and then a monotone bleed to +5.07 by the close. Nothing
after 09:00 pays an amc holder anything.

**bmo does not exist before 07:00.** The line sitting at zero through hour 14 is the print not
having happened, not a market that ignored it. From 07:00 it turns on and climbs without a
reversal to its best value of the whole day at the close.

**The free control is on the opposite clock.** Shorting every name and doing no research pays
−0.5 to −2.0 per day at every hour before the open and +1.7 to +2.5 at every hour after it.
The sample's downward skew — the thing that beat the shipped scorer in the first place — is
an intraday effect. Exit at the open and the control is not a rival; hold to the close and
roughly two of the +5.60 is available to anyone who shorts blind.

Costs cut the other way. At a flat 1.5% round trip the ranking of exits barely moves
(pre-open +5.11, open +4.71, close +4.30), but a fill at 09:00 in a name that trades $1m a day
is not a 1.5% round trip, and this source reports no extended-hours volume at all, so the
09:00 peak is a statement about information and not about capacity. The opening auction is the
earliest hour on the chart where the number and the fill are the same thing.

### The policy, and why it is a lead and not a finding

| exit policy | ρ | book | t | CI95 | long/short thirds | days positive |
| --- | --- | --- | --- | --- | --- | --- |
| uniform close (current) | +0.375 | +5.80% | 2.57 | [+1.38, +10.22] | +5.09%/day | 4/5 |
| uniform opening print | +0.315 | +6.21% | 2.99 | [+2.14, +10.27] | +5.58%/day | 3/5 |
| uniform pre-open | +0.360 | +6.61% | 3.17 | [+2.53, +10.70] | +5.43%/day | 5/5 |
| uniform after-hours | +0.230 | +5.16% | 2.75 | [+1.48, +8.84] | +3.26%/day | 2/5 |
| **amc at the open, bmo at the close** | **+0.461** | **+7.81%** | **4.01** | [+3.99, +11.62] | **+6.97%/day** | 4/5 |
| amc pre-open, bmo at the close | +0.456 | +7.49% | 3.89 | [+3.71, +11.27] | +6.85%/day | 5/5 |

In money rather than ρ, over the five days: per trade the hybrid pays **+7.81%** against
+5.80% for the current uniform close (+6.31% against +4.30% after a 1.5% cost), and traded as
long/short thirds it compounds to **+39.2%** over the five days against +27.2%. The uniform
pre-open exit is the only one positive on all 5 days (+29.5% compounded), and exiting into the
release is the worst of the lot at +16.6%.

The hybrid is the best of six on every column. It is also chosen from six after the
session split had been read off these same 38 events. The paired day bootstrap gives its
gain over the close as +1.87pp with a CI of [−1.30, +4.55], and the **best of the six**
beats the close in 91% of resamples — against a null where the true answer is picked
blind that is not a p-value, and 5 independent days is the resampling unit. Treat the
hybrid as the next thing to run forward, not as an established improvement.

### What the horizons rule out

Selling **immediately after the print** is the one variant the sample rejects rather than
merely failing to support. Only 46% of the eventual first-session move exists in the
after-hours window (63% for amc, 43% for bmo), ρ falls to +0.230, and for bmo names it
goes negative (−0.184). The reaction is not complete when the release hits; waiting for
the pre-open indication is worth 0.13 of ρ over exiting into the release.

The other thing the table rules out is a **tradeable** early exit at face value. Yahoo
reports no volume on extended-hours bars, so every horizon before the opening print is a
price that existed, not size that could have been hit — and six of the 22 book positions
turn over under $1m a day. The opening auction is the only pre-session horizon here that
is genuinely liquid, which is convenient, because for amc names it is also the best one.
On the liquid subset (≥$5m/day, 26 names) the gap-versus-session pattern holds:
ρ +0.243 at the open against +0.271 at the close, book +7.22% against +7.29%, and the
conviction correlation is *higher* at the open (+0.477) than at the close (+0.441).

### Forward test, two days: nothing replicates yet

09-08 and 09-09 were not in the sample any of the above was fitted on. `edge_exit.py --runs`
scores a run directory directly, with a hard cutoff at the current clock so nothing that has
not happened is reported. 09-08's eight names resolved on the 09-09 close; 09-09's 22 names
are mid-session on 09-10 as of 14:50 UTC, so their close does not exist yet. 09-08 predates
the `impact_sum` key and its number is summed from the findings, the same way
`edge_decompose.py` does it. Output in `edge/analysis/edge-exit-forward.json`.

| exit | trades | hits | per trade | t | amc | bmo |
| --- | --- | --- | --- | --- | --- | --- |
| after-hours / early pre-market | 14 | 7 | −1.42% | −0.50 | +0.67% | −2.98% |
| pre-open | 13 | 7 | −1.09% | −0.26 | −0.18% | −1.67% |
| opening print | 14 | 6 | −0.05% | −0.01 | +1.19% | −0.98% |
| open + 15 min | 13 | 7 | −0.52% | −0.14 | −0.74% | −0.39% |
| open + 60 min | 13 | 7 | −1.22% | −0.32 | −0.95% | −1.45% |
| first close | 3 | 1 | −10.33% | −0.77 | — | — |

**Every horizon available on both days is flat to negative.** Only the 09-08 close exists, on
three trades, so the −10.33% is one day and not a comparison. The ordering the pooled sample
gave — early beats late for amc, late beats early for bmo — appears on 09-08 (its book is
−1.54% at the open and −10.33% at the close, an 8.8-point gap driven almost entirely by YQ
reversing 29 points intraday) and does not appear on 09-09 (−0.16% at the open, −0.90% by
10:00, with the two largest predictions both wrong and large: NAVN at +10.0 fell 18.4% and
WLTH at −10.5 rose 8.0% by 10:00). Two days is an anecdote about an anecdote; the point is
that it is not confirmation.

Worse for the method as a whole: on 09-09 the free control paid **+3.9% to +4.5% per day**
at every hour after 08:00 while the hunt's own book paid −0.2% to −0.9%. Shorting the day
blind beat the research by roughly five points.

### The other 37 events in this repo say the opposite

`backtest/RESULTS.md` priced its 37 sealed events at both exits, from a 14:00 ET entry on the
session before the print. All three arms did **better at the close**:

| arm | return/trade, exit open | return/trade, exit close |
| --- | --- | --- |
| A naive | +0.90% | +2.16% |
| B plan-first | +0.45% | +2.24% |
| C skill | −1.16% | +0.11% |

That is an independent sample of the same size as stage E's, on overlapping calendar months,
and it puts the close ahead by 1.3 to 1.8 points per trade. It is not a direct contradiction —
different entry, different forecasts, no amc/bmo split recorded — but any claim that the first
reaction is where the information sits has to explain it, and right now nothing does. Re-pricing
those 37 events on the hourly grid is the cheapest way to settle it and has not been done.

### What the execution venue allows

Checked against Alpaca's current documentation (Placing Orders, updated 2026-08-10; 24/5
Trading, 2026-07-07; Margin and Short Selling, 2026-06-24), because an exit hour that cannot
be traded is not an exit:

- **Extended hours are limit-only.** `time_in_force` must be `day` or `gtc` with
  `extended_hours=true`; market, stop and stop-limit are rejected. So every horizon before
  09:30 on the chart is a limit order that may not fill, which is the "price existed, size
  did not" caveat made concrete.
- **The opening auction has a clean instrument**: `opg` time-in-force. But submissions between
  09:28 and 19:00 ET are *rejected*, not queued — an `opg` order must go in after 19:00 ET the
  evening before. No Routine firing during European afternoon hours can place one.
- **The close has a clean instrument too**: `cls` time-in-force, rejected between 15:50 and
  19:00 ET. A run at 13:30 ET can submit both entries and `cls` exits.
- **Shorting needs a margin account with $2,000 equity and an easy-to-borrow name**, checked
  per name per day; hard-to-borrow shorts cannot be opened at all. Fractional shorts are not
  supported, so the short leg cannot be sized fractionally.
- Overnight (20:00–04:00 ET) executes on a single ATS rather than the consolidated market, so
  a fill there is thinner than a regular-session quote suggests — on top of the six book
  positions already under $1m a day.

The practical consequence: the two horizons the pooled sample liked are the two with real
instruments, and the pre-market hours the chart peaks on are the ones with neither a market
order nor a verifiable book.

### Recycling the cash: what the metric does and does not say

The case for the early amc exit is often put as capital efficiency, and the arithmetic
that seems to support it is wrong. Return divided by hours *held* makes a 16:30 exit read
as **206% per capital-day** on half an hour of holding, and amc-at-the-open as 12.2%
against 5.2% for the close. Both are denominator artefacts. There is one entry a day and
it is always the 16:00 ET closing auction, so cash freed at 09:30 cannot be redeployed
until 16:00 whatever you do with it: the capital slot is 24 hours for every horizon, and
return per slot-day is identical to return per trade. `capital_table` in
`edge/scripts/edge_exit.py` prints both columns side by side and flags the degenerate one.

| exit | trades | held | idle | per trade | per slot-day | per exposure-day |
| --- | --- | --- | --- | --- | --- | --- |
| after-hours / early pre-market | 21 | 7.1h | 16.9h | +5.16% | +5.16% | +206.18% * |
| pre-open | 21 | 17.4h | 6.6h | +6.61% | +6.61% | +9.12% |
| opening print | 22 | 17.5h | 6.5h | +6.21% | +6.21% | +8.51% |
| midday | 21 | 20.0h | 4.0h | +4.24% | +4.24% | +5.09% |
| first close | 22 | 24.0h | 0.0h | +5.80% | +5.80% | +5.80% |
| **amc open / bmo close** | 22 | 20.5h | 3.6h | **+7.81%** | **+7.81%** | +9.61% |

\* held under four hours; the per-exposure-day figure there is arithmetic, not a result.

Two things the early exit does buy, and they are worth having without inflating them.
**Sizing certainty**: the next book is funded from settled cash rather than from proceeds
of a sale in the same auction, so position sizes do not depend on fills that have not
arrived. **Less exposure for more return**: 17.5 hours instead of 24, at +8.91% against
+5.23% for amc — that is the honest version of the capital argument, and it is a risk
statement rather than a return one.

## The number is a confidence flag, not a magnitude — and on the forward days not even that

`edge/scripts/edge_calibration.py` runs off `edge/ledger/names.csv` and asks the question
`edge_resolve.py` does not: the stage emits a *number*, in points of spot, and a number
claims a magnitude, not just an ordering. Three properties are independent, and the
answers differ.

**68 de-duplicated events, 7 days**, keeping the earlier of a repeated hunt as
`edge_direction.py` does. That is 30 events more than the 38 every earlier section here
was fitted on, because 09-08, 09-09 and 09-10 have now resolved.

### The magnitude is worth nothing at all

| | |
| --- | --- |
| regression of realised move on `impact_sum` | slope **−0.021**, t = −0.09, R² = **0.000** |
| mean absolute error, the hunt | 10.61 points |
| mean absolute error, predicting **zero** | **10.22 points** |
| hunt − zero | +0.39, 95% CI [−0.88, +1.76] |
| standard deviation of the realised move | 12.50 points |

An earlier section of this file reports slope 0.72–0.76 and pearson 0.41–0.46 on the
fitted 43 names. On 68 events the slope is indistinguishable from zero and the number
carries **no** magnitude information: a prediction of +9 says nothing more about the size
of the move than a prediction of +3. It is also, point for point, slightly *worse* than
saying nothing — not significantly, but the interval does not reach the other way either.

The consequence is a rule, not a caveat. `impact_sum` must never be read as an expected
return, never appear in a note as "we expect about X%", and never size a position. The
current sizing is equal-weight and does not read the score, which turns out to be the
only defensible choice available.

### The size still orders the sign, at about half the strength that was measured

| bucket of \|impact_sum\| | n | sign correct | mean \|move\| |
| --- | --- | --- | --- |
| < 1 | 9 | 0.333 | 8.92 |
| 1–3 | 24 | 0.417 | 8.72 |
| 3–6 | 20 | 0.650 | 12.32 |
| ≥ 6 | 15 | 0.733 | 10.63 |

Monotone, and the overall sign rate is a coin flip (36/67, 53.7%) — so the ordering is
the whole of it, exactly as the conviction section says. But the threshold-free
correlation between the rank of `|impact_sum|` and whether the sign was right is
**ρ = +0.243, within-day permutation p = 0.049**, against **+0.514, p = 0.0015** on the
fitted 38. Adding three unseen days halved it. `|pred| ≥ 3` is 24/35 (68.6%, p = 0.041)
where it was 16/21.

### On the two days run under the current one-hunter contract, it points the other way

| | events | days | conviction → sign |
| --- | --- | --- | --- |
| before 2026-09-09 (two hunters on two names a day) | 41 | 5 | **+0.494**, p = 0.0009 |
| 2026-09-09 onward (one hunter per name) | 27 | 2 | **−0.260**, p = 0.21 |

Within the double-hunt era the bucket table is nearly perfect (0.167 / 0.231 / 0.667 /
0.846 as `|pred|` rises). Within the two single-hunter days it inverts, and the two names
above 6 points were both wrong. Twenty-seven events on two days establishes nothing on
its own — but it is the only data that exists for the regime the stage now runs in, and
it does not support the +0.361 that `edge_hunter_control.py` projected.

Pooling differently gives the other answer, which is the honest state of it: taking every
**single-hunted name from every era** (n = 54, the like-for-like control), `|pred| ≥ 3`
is **17/24 = 70.8%, p = 0.064**. So the conviction floor survives a pooled single-hunter
cut and fails a within-day one on the forward days. Both are underpowered. What can be
said without hedging is that the effect is smaller than the number the execution path was
switched on against.

### It does not find volatility either

`|impact_sum|` against `|realised move|` ranks at **ρ = 0.174, p = 0.183** (0.122, p = 0.34
after dividing by the implied move). So a large prediction does not reliably land on a
name that moved at all, in either direction. Whatever the number is doing, it is not a
straddle signal, and the "trade it as an option instead" escape is not available.

### The free control, again

The mean realised move over all 68 events is **−2.71%**. Shorting every name reporting,
with no research, remains the thing to beat, and 09-08 is the day that hurt: nine events,
the highest mean `|impact_sum|` of any day (7.09), and a 22% sign rate.

### What to do with this

1. Keep `|impact_sum| >= conviction_floor` as a **gate**, which is all the evidence
   supports, and stop describing the number as points of expected move anywhere a reader
   might price off it.
2. Size from the implied move or from equal weight — never from the score.
3. Treat the conviction result as **live, not established**, until the single-hunter
   sample reaches a size where the two poolings agree. Ten more days decides it.

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
8. Resolve every run at the opening print as well as the close. `edge_resolve.py` measures
   one window and the amc names are scored on the wrong one — ρ +0.273 at the open against
   +0.156 at the close. Two columns cost nothing and the sample needs the forward test.
9. Re-price `backtest/`'s 37 events on the same hourly grid before acting on any exit rule.
   Two samples in this repo disagree about open versus close and only one of them has been
   decomposed.
10. Do not build execution on this until the forward days turn. Two out-of-sample days are
   flat to negative at every tradeable hour, and on 09-09 shorting blind beat the hunt by
   about five points a day.
11. Do not sell the amc exit as capital efficiency. Per capital-day it is identical to
   per trade under a once-daily auction entry; the gain is exposure and sizing certainty.
12. Do not exit into the release. Under half the move is there, and for bmo names the
   after-hours ranking is negative.
