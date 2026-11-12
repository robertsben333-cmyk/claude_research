# Stage E-P — 2026-11-12 amc + 2026-11-13 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** Step 6b trades the panel's book on the Alpaca paper account, and on a live account where its keys are present. Today the live account's secret key is missing from the environment, so the live calls refuse. Stage E's Routine is stopped.
**All four members ran on their pinned agents:** Opus 5 (`claude-opus-5`), Opus 5.5 (`claude-opus-5-5`), Sonnet 5.5 (`claude-sonnet-5-5`) and Fable 5.1 (`claude-fable-5-1`). Each covered 20/20 names in one part, with no fallback and no retry.
**One day is an anecdote.** Only the pooled record says anything.

**Universe:** 148 names (124 amc on 11-12, 24 bmo on 11-13).
- **Sweep:** time-boxed. It checked 29 names, confirmed 15 from company sources, left 7 unconfirmed and found 0 phantoms; about 119 were left unchecked.
- **Hunted (20):** the 15 confirmed names plus the top 5 unconfirmed by `hunt_priority` (NU, STN, INTR, SMFG, MFG). Each of those five searchers settled its own date: STN (6-K), INTR (IR page), MFG and SMFG (company IR calendars) from company sources, NU only from Itaú BBA's calendar, aggregators and last year's cadence.
- **Shed:** ELPC and CIG, plus every unchecked name.
- **Search status:** all 20 searches completed (`hunt_status`: 0 unfinished).

## Panel table (every rankable name)

Each judge is shown as a percentile of its own live range, 0-100, with L/S for its side; `*` marks a name in that judge's own top 20%. `E[ret]` is the expected return at that panel_pct, the translation of the percentile and not a separate forecast. It is gross, on the scorebord's window, with an 80% band and the hit rate, and it is flat at about +0.3% below a percentile of 50.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[ret] [80%] | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTFL | 2026-11-12 amc | **yes** | 93 | short | 5 | 94S* | 85S* | 95S* | 98S* | 4 | -2.05 | -1.00 | +4.49% [+2.46, +6.32] | 0.70 | 1.00 | 1.21 |
| 2 | LFTO | 2026-11-12 amc | **yes** | 88 | long | 6 | 80L* | 92L* | 95L* | 84L* | 4 | +1.58 | +3.70 | +3.77% [+1.66, +5.74] | 0.67 | 1.00 | 0.91 |
| 3 | STNE | 2026-11-12 amc | **yes** | 84 | short | 7 | 82S* | 76S | 84S* | 96S* | 3 | -1.31 | -1.80 | +3.25% [+1.16, +5.25] | 0.64 | 1.00 | 1.00 |
| 4 | CBRS | 2026-11-12 amc |  | 78 | short | 12 | 82S* | 64S | 69S | 96S* | 2 | -1.13 | +0.40 | +2.32% [+0.50, +4.20] | 0.58 | 0.00 | 0.00 |
| 5 | DLO | 2026-11-12 amc |  | 67 | short | 10 | 62S | 70S | 55S | 81S* | 1 | -0.93 | -1.60 | +1.33% [+0.11, +2.96] | 0.56 | 0.00 | 0.00 |
| 6 | ACCV | 2026-11-12 amc |  | 66 | long | 9 | 78L | 72L | 55L | 60L | 0 | +0.97 | +0.60 | +1.27% [+0.08, +2.89] | 0.56 | 0.00 | 0.00 |
| 7 | ANDG | 2026-11-12 amc |  | 52 | long | 9 | 58L | 60L | 52L | 36L | 0 | +0.63 | +1.40 | +0.32% [-0.38, +1.59] | 0.56 | 0.00 | 0.00 |
| 8 | HAWK | 2026-11-12 amc |  | 44 | long | 34 | 14S | 54L | 68L | 70L | 0 | +0.75 | -0.30 | +0.29% [-0.49, +1.08] | 0.56 | 0.00 | 0.00 |
| 9 | ARWR | 2026-11-12 amc |  | 42 | long | 12 | 25L | 44L | 60L | 38L | 0 | +0.51 | +1.30 | +0.29% [-0.51, +0.98] | 0.56 | 0.00 | 0.00 |
| 10 | SMFG | 2026-11-13 bmo |  | 33 | long | 17 | 16L | 54L | 44L | 18L | 0 | +0.37 | +1.65 | +0.29% [-0.55, +0.86] | 0.56 | 0.00 | 0.00 |
| 11 | NU | 2026-11-12 amc |  | 25 | long | 22 | 16L | 28L | 58L | 3S | 0 | +0.30 | -1.30 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 12 | MFG | 2026-11-13 bmo |  | 20 | long | 13 | 16L | 40L | 18L | 5L | 0 | +0.26 | +0.90 | +0.29% [-0.60, +0.82] | 0.56 | 0.00 | 0.00 |
| 13 | STN | 2026-11-12 amc |  | 14 | short | 6 | 10S | 24S | 7S | 18S | 0 | -0.25 | -0.20 | +0.29% [-0.66, +0.81] | 0.56 | 0.00 | 0.00 |
| 14 | CSCO | 2026-11-12 amc |  | 14 | long | 28 | 24S | 54L | 16L | 8L | 0 | +0.20 | +0.90 | +0.29% [-0.66, +0.81] | 0.56 | 0.00 | 0.00 |
| 15 | NKTR | 2026-11-12 amc |  | 12 | long | 3 | 6L | 12L | 15L | 13L | 0 | +0.17 | +0.40 | +0.29% [-0.67, +0.80] | 0.56 | 0.00 | 0.00 |
| 16 | XXI | 2026-11-13 bmo |  | 10 | long | 14 | 0- | 16L | 7S | 30L | 0 | +0.10 | +0.70 | +0.29% [-0.69, +0.80] | 0.56 | 0.00 | 0.00 |
| 17 | AMAT | 2026-11-12 amc |  | 10 | long | 17 | 9L | 18S | 22L | 24L | 0 | +0.22 | -0.20 | +0.29% [-0.69, +0.80] | 0.56 | 0.00 | 0.00 |
| 18 | BLTE | 2026-11-12 amc |  | 4 | short | 2 | 4S | 0- | 4S | 7S | 0 | -0.10 | -0.10 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |
| 19 | FLO | 2026-11-12 amc |  | 3 | short | 36 | 28L | 18S | 55S | 34L | 0 | +0.10 | +0.00 | +0.29% [-0.74, +0.78] | 0.56 | 0.00 | 0.00 |
| 20 | INTR | 2026-11-12 amc |  | 1 | short | 11 | 10S | 12L | 8L | 15S | 0 | -0.04 | -0.60 | +0.29% [-0.75, +0.78] | 0.56 | 0.00 | 0.00 |

**Selected (panel_pct >= 80, all four members present): HTFL short 93, LFTO long 88, STNE short 84.** CBRS (short, 78) is next. With three strong names, the 70-79 top-up does not apply.

**HTFL (Heartflow), short, panel_pct 93, 2026-11-12 amc.** All four judges rest on positioning:
- the stock is +51% since the August print and sits above the $50.5 average target;
- the option market pays +31.8 vol points for 25-delta puts, with put/call open interest 3.9;
- two of its last three beat-and-raise prints were sold by 12-13%.

The searcher's bar is $65.1M revenue (Earnings Whispers). Its own largest positive is that consensus implies only +1.6% sequential growth against +22% in Q2.

**Strongest case against:** a beat-and-raise is the base case. The one print that was bought (+35.7% in August) came with a raise larger than the beat. The put skew already says what the panel says, and no current short-interest figure was found.

**LFTO (Liftoff Mobile), long, panel_pct 88, 2026-11-12 amc.** Three counterparties reported strong Jul-Sep app user-acquisition (UA) spending after Liftoff's 12 Aug call:
- AppLovin came in about $100M above the top of its guide (https://mobilegamer.biz/applovin-posts-record-revenue-of-2-2bn-in-q3-up-55/);
- Unity Vector grew +40% q/q;
- Digital Turbine raised its guide on 11-09 (https://finviz.com/news/419425/digital-turbine-reports-strong-fiscal-2027-second-quarter-financial-results).

Against them, Liftoff guided Q3 flat at $217-222M and called that guide "prudent" (https://www.sec.gov/Archives/edgar/data/0001850351/000162828026056173/fy26q2earningsrelease.htm). Its full-year guide implies an undemanding Q4. Short interest is 3.49M shares at 5.7 days to cover on a float held thin by Blackstone and GA. It is the only name of the day whose searcher `impact_sum` (+3.7) clears the 2.8 conviction floor.

**Strongest case against:** last quarter's 5.6% beat was sold 20.6% on the guide. The stock has run about +27% off its 30 Oct low. The Blackstone/GA lock-up expires at the end of November, outside the window. The option-implied move of about 25% comes off a chain whose ATM spread is 63% of mid.

**STNE (StoneCo), short, panel_pct 84, 2026-11-12 amc.** The FY26 guide looks arithmetically out of reach:
- H1 adjusted EPS was R$4.58, so the low end of the R$10.80-11.40 guide needs R$3.11 a quarter;
- Itaú BBA and Safra previews sit near R$2.30-2.40 (Finsiders, 2026-11-03);
- the US$ consensus still sits above the guide's translated top.

The 2027 guide was set before Lula's 26 Oct re-election and the hawkish Copom hold. In Q2, 15-90 day NPLs rose to 6.00% from 4.97%. Guidance is the line that took this name −19% in March.

**Strongest case against:** the stock is −31% over 20 days at about 3-4x earnings, and UBS has already cut to Neutral. More than R$2B of buyback was promised for 2026, at about half the last program's price. Opus 5.5 kept it out of its own top 20% (76).

## Where the panel and the searcher disagree most

- **CBRS:** the searcher has +0.4, the panel 78 short. All four judges weighted the Q4 capacity constraint, the core-vs-GAAP "miss" headline and two sold prints over the upside skew; Opus 5 and Fable 5.1 had it in their own top 20%.
- **NU:** the searcher has −1.3, the panel 25 long. Three judges read the washed-out positioning and the low bar as offsetting the credit negatives.
- **SMFG:** the searcher has +1.65, the panel 33 long. Opus 5 and Fable 5.1 put it near their 16th-18th percentile on a bar that rests on snippets.
- **ARWR** (+1.3 against 42 long) and **MFG** (+0.9 against 20 long): the same pattern, where the judges shrank moderately sized positives.

## Stage E

Stage E's `<RUN>/edge/` does not exist for this date, because its Routine is stopped. There is no overlap or ρ to report.

## What the numbers are not

- **Expected return:** `expected_return_pct` (and `expected_edge_pct`, the same expectation as a signed move) is what names at that percentile have earned, gross, on the scorebord window. Its out-of-sample record is weak, a correlation of +0.12 with the realised return over 148 names, so it is not a forecast to size on.
- **Weights:** they are research. The book is sized by `execution.panel` in `alpaca_trade.py` (panel_pct − 60, 50% cap a name), not by these columns.
- **Certainty:** `p_up` is recorded and decides nothing.
- **Unchecked findings:** nothing checked the searchers' findings for factual errors, and the key is not reproducible to better than its own size.

## Not ranked

128 universe names were not hunted: ~119 unchecked by the sweep, 2 unconfirmed and shed (ELPC, CIG), and the rest of the tail. All sit in `edge-scores.json` as `rankable: false` ("no hunt"). There were no unfinished searches.

## Context: retail, search and volatility (not used for selection)

The three labels are in `edge-context.json` and in the `score_report.py` table. They are context only; nothing ranks, selects or trades on them.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
