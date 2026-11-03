# Stage E-P — 2026-11-03 amc + 2026-11-04 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel. Its book goes to the Alpaca paper account at step 6b.** All four members ran on their pinned agents: Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1. Each judged 20 of 20 ids in one part, with no fallback and no retry. One day is an anecdote.

- **Universe:** 265 names, 135 amc on 11-03 and 130 bmo on 11-04. GEF.B and HVT.A were folded into GEF and HVT.
- **Sweep:** checked 22 names against company releases and confirmed 21.
- **Hunted:** 20. CRCL was shed as the lowest priority (34), VRNS was unconfirmed, and 243 names went unchecked.
- **Searches:** 20 of 20 finished, so no name is unfinished.
- **Sessions:** OUST and LIME were settled as amc, and DIN as bmo, from the companies' own releases.
- **SMCI baseline:** amended from suspect to unknown after the hunts. The "print" it had on 10-20 was the FQ1 pre-announcement 8-K, not results (see the run log).

## Panel table

Each percentile is the judge's own, 0-100, measured against its last 200 live sizes. `*` means the name is in that judge's own top 20%. L is long and S is short.

**E[return] is what names at that panel_pct have earned on the panel's side.** It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. It translates the percentile; it is not a separate forecast.

| # | ticker | sess | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_prec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TREE | amc | **yes** | 95 | 1 | 5 | 98L* | 96L* | 87L* | 99L* | 4 | +2.36 | +4.5 | +4.74% [+2.76, +6.50] | 0.72 | 1.0 | 1.0450072275368576 |
| 2 | SEDG | bmo | **yes** | 87 | -1 | 5 | 94S* | 80S | 86S* | 87S* | 3 | -1.46 | -0.9 | +3.61% [+1.51, +5.60] | 0.66 | 1.0 | 0.9549927724631425 |
| 3 | CRCT | amc | **yes** | 86 | 1 | 3 | 86L* | 84L* | 92L* | 83L* | 4 | +1.45 | +1.4 | +3.52% [+1.42, +5.52] | 0.65 | 1.0 | 1.25 |
| 4 | DUOL | amc | **yes** | 81 | -1 | 13 | 99S* | 66S | 73S | 87S* | 2 | -1.22 | -0.5 | +2.79% [+0.77, +4.74] | 0.61 | 1.0 | 0.75 |
| 5 | ALAB | amc |  | 78 | 1 | 5 | 76L | 74L | 87L* | 74L | 1 | +1.11 | +0.7 | +2.37% [+0.52, +4.26] | 0.59 | 0.0 | 0.0 |
| 6 | FRSH | amc |  | 68 | -1 | 14 | 82S* | 60S | 50S | 80S* | 2 | -0.99 | -1.2 | +1.41% [+0.15, +3.06] | 0.56 | 0.0 | 0.0 |
| 7 | TARS | amc |  | 68 | 1 | 4 | 66L | 74L | 64L | 68L | 0 | +0.85 | +1.0 | +1.40% [+0.15, +3.05] | 0.56 | 0.0 | 0.0 |
| 8 | XPEL | bmo |  | 64 | 1 | 11 | 77L | 53L | 73L | 54L | 0 | +0.79 | +0.7 | +1.12% [+0.01, +2.69] | 0.56 | 0.0 | 0.0 |
| 9 | MQ | amc |  | 62 | -1 | 19 | 84S* | 38S | 50S | 77S | 1 | -0.80 | -0.5 | +0.96% [-0.06, +2.48] | 0.56 | 0.0 | 0.0 |
| 10 | LIME | amc |  | 58 | 1 | 17 | 76L | 32L | 54L | 70L | 0 | +0.77 | +0.9 | +0.63% [-0.19, +2.11] | 0.56 | 0.0 | 0.0 |
| 11 | OUST | amc |  | 57 | 1 | 18 | 69L | 78L | 50L | 31L | 0 | +0.67 | +1.9 | +0.56% [-0.22, +2.04] | 0.56 | 0.0 | 0.0 |
| 12 | W | bmo |  | 43 | -1 | 36 | 72S | 52S | 18L | 68S | 0 | -0.75 | -0.4 | +0.29% [-0.50, +1.04] | 0.56 | 0.0 | 0.0 |
| 13 | CAR | amc |  | 41 | -1 | 14 | 62S | 46S | 26S | 31S | 0 | -0.46 | -0.8 | +0.29% [-0.51, +0.97] | 0.56 | 0.0 | 0.0 |
| 14 | TOST | amc |  | 36 | -1 | 31 | 72S | 28S | 10L | 54S | 0 | -0.52 | -0.5 | +0.29% [-0.54, +0.88] | 0.56 | 0.0 | 0.0 |
| 15 | HUT | bmo |  | 34 | -1 | 38 | 44S | 16L | 18S | 90S* | 1 | -0.38 | +0.1 | +0.29% [-0.55, +0.87] | 0.56 | 0.0 | 0.0 |
| 16 | DIN | bmo |  | 33 | -1 | 13 | 40S | 24S | 18S | 52S | 0 | -0.39 | -0.1 | +0.29% [-0.55, +0.86] | 0.56 | 0.0 | 0.0 |
| 17 | SMCI | amc |  | 24 | 1 | 59 | 69S | 13L | 73L | 78L | 0 | +0.53 | +1.3 | +0.29% [-0.58, +0.83] | 0.56 | 0.0 | 0.0 |
| 18 | RVLV | amc |  | 13 | -1 | 52 | 72S | 38L | 40L | 58S | 0 | -0.18 | +0.2 | +0.29% [-0.67, +0.81] | 0.56 | 0.0 | 0.0 |
| 19 | RIOT | bmo |  | 6 | -1 | 19 | 6L | 16L | 18S | 30S | 0 | -0.04 | +0.0 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.0 |
| 20 | NVTS | amc |  | 4 | -1 | 53 | 72S | 52L | 40S | 42L | 0 | +0.07 | +1.0 | +0.29% [-0.73, +0.78] | 0.56 | 0.0 | 0.0 |

**Selected (panel_pct >= 80, all four present):**

| Name | Side | panel_pct | Judges in their own top 20% | Under the old 3-of-4 rule |
| --- | --- | --- | --- | --- |
| TREE | long | 95 | 4 of 4 | selected |
| SEDG | short | 87 | 3 of 4 | selected |
| CRCT | long | 86 | 4 of 4 | selected |
| DUOL | short | 81 | 2 of 4 | not selected |

The next name is ALAB at 78.

## Selected names

**TREE, long, 95.**
- **Evidence:** both direct insurance lead-gen peers beat their own Q3 guides after TREE last spoke. MediaAlpha reported revenue of $375.9m against a $330-355m guide, and EverQuote $218.1m against $198-208m. Both guided Q4 firm. TREE's consensus still sits on its own guide midpoint ($329.8m), and the stock moved only +5.7% and +3.3% on the peers' +20.6% and +17.4% days. Short interest is about 10% of float.
- **Strongest case against:** TREE fell about 20% on each of its last two prints despite beating revenue, both times on insurance profit quality. Insurance profit grew 25% on revenue up 42% in Q2, and the H2 margin was guided flat. The peer strength is partly priced.

**SEDG, short, 87.**
- **Evidence:** Enphase (10-27) guided Q4 to $225-255m against about $300m consensus. Its European sell-through fell 12% quarter on quarter and the US fell 35% year on year. SEDG's Q4 consensus is still $319-343m. Northland cut its SEDG Q4 estimate to $300m, and German rooftop registrations did not recover in September.
- **Strongest case against:** about 18% of float is short, and last year's Q3 print squeezed +28.9%. The put skew is +23.9 vol points, so much of the bad news is already paid for. Peer SMA guided its H2 home-inverter revenue up.

**CRCT, long, 86.**
- **Evidence:** the Maker 5 went on sale on 4 September, inside Q3, against a consensus that implies products revenue down 1-4%. The EPS bar of $0.03-0.05 is well below the Q2 run-rate. A $300m undrawn revolver adds capital-return capacity. Three Sell ratings and about 8% short interest sit on a name that has risen after 6 of its last 7 prints.
- **Strongest case against:** revenue missed in both Q1 and Q2, and last year's Q3 fell 5.2% on an EPS beat. Accessories and materials keep eroding, and the EPS bar itself is disputed.

**DUOL, short, 81.**
- **Evidence:** holding the full-year bookings guide implies Q4 bookings of about $380m, roughly +12%, after +8-9% in Q2 and Q3. That is the line the stock has sold on (-9.4%, -14.0%, -25.5%). Max may be sunset, which dilutes revenue per subscriber. Coursera guided weak and fell about 8%.
- **Strongest case against:** 18.2% of float is short with 8.5 days to cover. DA Davidson's user panel shows Q3 daily users up 26-28% against a guide of over 20%. The judges' spread is wide (sd 13): Opus 5 put it at 99, Opus 5.5 at 66 and Sonnet 5.5 at 73.

## Where the panel and the searcher disagree most

- **OUST:** the searcher's sum is +1.9, its second largest, but the panel puts it at 57. Fable 5.1 reads it at only 31.
- **MQ:** the searcher has -0.5, but the panel is short at 62. Opus 5 reads it at 84S, on the 2027 Cash App framing.
- **SEDG and DUOL:** the searcher's sums are only -0.9 and -0.5, yet both are selected shorts. The judges size the negative guide lines larger than the searcher's netting does.
- **SMCI:** the searcher has +1.3, but the panel is split at 24 (sd 59). Opus 5 is short at 69, and Fable 5.1 and Sonnet 5.5 are long.

## Stage E comparison

Stage E's `edge/` directory does not exist for this date, because its Routine is stopped. There is no overlap and no Spearman ρ to report.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct` on selected names) is what names at that percentile have earned. Its out-of-sample record is weak: a correlation of +0.12 with the realised return over 148 names. It is not a forecast to size on.

The weights are research. The book uses `execution.panel`'s own linear rule. `p_up` is recorded and decides nothing.

Nothing at this panel_pct has been measured on a single day.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
