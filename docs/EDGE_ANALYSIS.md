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

## What `impact_sum` is, precisely — and the sizing correction of 2026-09-09

The 2026-09-09 edge-hunt run caught a discrepancy between this file and the code, and
resolving it changed the code rather than the prose.

`scripts/edge_score.py` used to re-size every finding to the **mean** of the hunter's
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
news. `scripts/edge_exit.py` re-resolves all 38 de-duplicated events at eight exit
horizons against the same unchanged entry, off 5-minute Yahoo bars with
`includePrePost=true`. Output in `docs/edge-exit.json`.

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

### The policy, and why it is a lead and not a finding

| exit policy | ρ | book | t | CI95 | long/short thirds | days positive |
| --- | --- | --- | --- | --- | --- | --- |
| uniform close (current) | +0.375 | +5.80% | 2.57 | [+1.38, +10.22] | +5.09%/day | 4/5 |
| uniform opening print | +0.315 | +6.21% | 2.99 | [+2.14, +10.27] | +5.58%/day | 3/5 |
| uniform pre-open | +0.360 | +6.61% | 3.17 | [+2.53, +10.70] | +5.43%/day | 5/5 |
| uniform after-hours | +0.230 | +5.16% | 2.75 | [+1.48, +8.84] | +3.26%/day | 2/5 |
| **amc at the open, bmo at the close** | **+0.461** | **+7.81%** | **4.01** | [+3.99, +11.62] | **+6.97%/day** | 4/5 |
| amc pre-open, bmo at the close | +0.456 | +7.49% | 3.89 | [+3.71, +11.27] | +6.85%/day | 5/5 |

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
9. Do not exit into the release. Under half the move is there, and for bmo names the
   after-hours ranking is negative.
