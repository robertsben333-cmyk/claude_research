# Stage E-P — edge hunt with a blind four-model panel, 2026-11-13 window

**This is stage E-P: Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel.** Stage E-P trades the book through `alpaca_trade.py` (step 6b, live then paper); the book is set by the panel rule and nothing in this note sizes it.
**All four judges ran on their pinned models**: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. None was missing and no fallback was used.
**One day is an anecdote.** The panel is judged only pooled over many days.

Window: amc 2026-11-13 plus bmo 2026-11-16 (Monday). The universe had 39 names. The sweep confirmed 27 for 11-16 bmo and left 12 unconfirmed; it proved none to be a phantom. Both amc rows (ROLR, BBGI) had no company date and no Q3 8-K, so both were shed. 20 names were hunted, all bmo 11-16, by `hunt_priority` after shedding the unconfirmed names. All 20 searchers finished (`hunt_status`: 0 unfinished) and none was retried.

## Panel table

`panel_pct` is the mean of the four judges' own percentiles, reported 0-100 with the direction in `side`. A `*` marks a judge that put the name in its own top 20%. The selection rule is `panel_pct` >= 80 with all four judges present. The expected return is gross, on the scorebord window, on the panel's side. It is one number per percentile: the translation of the percentile, not a separate forecast, and it is flat at about +0.3% below a percentile of 50.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_prec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NIU | bmo 11-16 | **yes** | 98 | short | 1 | 100S* | 99S* | 96S* | 97S* | 4 | -2.40 | -5.00 | +4.96% [+3.09, +6.64] | 0.73 | 1.0 | 1.25 |
| 2 | XTNT | bmo 11-16 | **yes** | 96 | short | 3 | 98S* | 98S* | 90S* | 96S* | 4 | -2.07 | -4.50 | +4.79% [+2.83, +6.53] | 0.72 | 1.0 | 1.0 |
| 3 | LNZA | bmo 11-16 | **yes** | 85 | short | 10 | 99S* | 85S* | 72S | 82S* | 3 | -1.38 | -2.20 | +3.28% [+1.18, +5.29] | 0.64 | 1.0 | 0.75 |
| 4 | BLDP | bmo 11-16 |  | 76 | short | 13 | 92S* | 76S | 56S | 80S* | 2 | -1.19 | -1.60 | +2.10% [+0.41, +3.94] | 0.57 | 0.0 | 0.0 |
| 5 | GAME | bmo 11-16 |  | 73 | short | 15 | 50S | 69S | 91S* | 81S* | 2 | -1.10 | -0.80 | +1.82% [+0.31, +3.58] | 0.56 | 0.0 | 0.0 |
| 6 | ARMK | bmo 11-16 |  | 64 | long | 17 | 92L* | 64L | 49L | 52L | 1 | +0.80 | +1.40 | +1.12% [+0.01, +2.69] | 0.56 | 0.0 | 0.0 |
| 7 | CREX | bmo 11-16 |  | 64 | short | 18 | 88S* | 72S | 56S | 38S | 1 | -0.83 | -1.90 | +1.07% [-0.01, +2.63] | 0.56 | 0.0 | 0.0 |
| 8 | POWW | bmo 11-16 |  | 60 | long | 4 | 65L | 63L | 57L | 56L | 0 | +0.80 | +0.70 | +0.83% [-0.12, +2.29] | 0.56 | 0.0 | 0.0 |
| 9 | HTHT | bmo 11-16 |  | 47 | short | 14 | 65S | 34S | 34S | 56S | 0 | -0.59 | -0.90 | +0.29% [-0.46, +1.25] | 0.56 | 0.0 | 0.0 |
| 10 | XPEV | bmo 11-16 |  | 46 | short | 17 | 54S | 63S | 18S | 50S | 0 | -0.75 | -0.20 | +0.29% [-0.47, +1.21] | 0.56 | 0.0 | 0.0 |
| 11 | BEKE | bmo 11-16 |  | 44 | long | 8 | 48L | 43L | 54L | 33L | 0 | +0.52 | +0.90 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.0 |
| 12 | VERI | bmo 11-16 |  | 44 | short | 56 | 38S | 85S* | 98S* | 44L | 2 | -0.98 | -0.80 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.0 |
| 13 | VENU | bmo 11-16 |  | 38 | short | 21 | 35S | 72S | 34S | 13S | 0 | -0.42 | -0.60 | +0.29% [-0.52, +0.91] | 0.56 | 0.0 | 0.0 |
| 14 | BIDU | bmo 11-16 |  | 23 | long | 12 | 40L | 28L | 16L | 8L | 0 | +0.27 | +1.05 | +0.29% [-0.58, +0.83] | 0.56 | 0.0 | 0.0 |
| 15 | IQ | bmo 11-16 |  | 14 | long | 24 | 28L | 18L | 26S | 34L | 0 | +0.32 | +0.60 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.0 |
| 16 | POET | bmo 11-16 |  | 11 | short | 19 | 12L | 18S | 0- | 38S | 0 | -0.12 | +0.00 | +0.29% [-0.68, +0.80] | 0.56 | 0.0 | 0.0 |
| 17 | BXDC | bmo 11-16 |  | 9 | short | 6 | 15S | 12S | 7S | 0- | 0 | -0.15 | -0.60 | +0.29% [-0.70, +0.79] | 0.56 | 0.0 | 0.0 |
| 18 | CYPH | bmo 11-16 |  | 8 | long | 16 | 12L | 18L | 18S | 22L | 0 | +0.21 | +0.80 | +0.29% [-0.70, +0.79] | 0.56 | 0.0 | 0.0 |
| 19 | TSN | bmo 11-16 |  | 7 | short | 4 | 0- | 12S | 8S | 6S | 0 | -0.15 | +0.40 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.0 |
| 20 | QVCG | bmo 11-16 |  | 6 | long | 43 | 65L | 24L | 54S | 9S | 0 | +0.05 | +0.70 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.0 |

**Selected: NIU, XTNT and LNZA, all short.** Session for all three: bmo 2026-11-16.

### The selected names

**NIU (98, short; all four judges in their own top 20%, spread 1).** The judges' notes rest on one piece of arithmetic from the company's own figures. NIU published its Q3 unit volume on Oct 5 (+15.4%). Applied to the Q2 revenue-per-unit trend (China -9.2% year on year, mix shifting), it gives Q3 revenue of about RMB 1.79bn. That is below the low end of NIU's own RMB 1,863-2,033m guide, for a third straight quarter. Aima's Q3 gross margin (-1.9 points on the prior quarter) corroborates the margin pressure. The last two prints with this shape fell 14.8% and 17.1%.
*Strongest case against:* the revenue figure is the searcher's own extrapolation, not a reported number, and no consensus could be sourced. The stock is at a 52-week low after an 8% 20-day fall. The Q4 guide will show strong year-on-year growth off a weak Q4 2025 (RMB 676m).
*Tradable:* **no**. Turnover is $0.19m a day, below the $0.2m floor.

**XTNT (96, short; four of four).** H1 revenue of $43.9m against the FY guide of $99-103m (cut on 2026-08-11) needs H2 of $55-59m. The 10-Q assures HEMOBLAST supply only through Q3, and the supplier can terminate on 30 days' notice. Two analysts still sit near FY $102m. The judges also cite soft orthobiologics peers (Alphatec, Bioventus) and a covenant reset tested for the first time in Q3.
*Strongest case against:* the stock is at its 52-week low, 41% below its August print. The Q3 revenue bar is disputed ($25.5m against about $27m). HEMOBLAST's switch to gross revenue reporting could make Q3 look like a sequential beat.
*Tradable:* **no**. Turnover is $0.04m a day.

**LNZA (85, short; three of four in their own top 20%, Sonnet 5.5 at 72).** Three points carry the judges' notes:
- a roughly $170m non-cash fair-value loss on the Shougang LanzaTech stake (2553.HK, HK$44.10 to HK$11.79 over the quarter), which puts GAAP EPS near -$13 against a single-source -$0.81;
- a FY guide of $50-55m that implies a Q4 two to three times the roughly $9m run rate, with no certified-ethanol sale announced;
- thinning cash after the LanzaJet recapitalisation.

*Strongest case against:* the ISCC EU certification the guide depended on came through in October. The market looked through the mirror-image $208m gain at Q2 (+2.09%). The stock is -19.5% over five days, 2.8% above its 52-week low.
*Tradable:* **elsewhere**. Alpaca does not lend it on this snapshot (check borrow at IBKR), and it is thin at $0.25m a day.

**What that means for the book:** all three selected names fail Alpaca's tradability checks today: two are below the turnover floor and the third cannot be shorted at Alpaca. So the panel's book is likely empty unless the plan finds otherwise; step 6b's plan output decides it and the run log records it. A one-name top-up applies only when exactly one strong name is in the book.

### Where the panel and the searcher disagree most

- **VERI**: searcher -0.80; panel 44 short with a spread of 56. Opus 5.5 (85S) and Sonnet 5.5 (98S) put it in their own top 20% short, while Fable 5.1 leans long (44L). The convertible maturity on 11-15 makes the move large and the direction close to a coin flip.
- **QVCG**: searcher +0.70; panel 6 long with a spread of 43. Opus 5 sized the July monthly operating report as a real +2.0 finding (65L); Sonnet 5.5 and Fable 5.1 went slightly short. The release hour is unsettled: an after-close 10-Q would put the reaction outside the window.
- **ARMK**: searcher +1.40, its largest positive; panel 64 long. Only Opus 5 (92L) put it in its top 20%.
- **GAME**: searcher -0.80; panel 73 short. Sonnet 5.5 (91S) and Fable 5.1 (81S) put it in their top 20%; Opus 5 sits at 50. It is below the turnover floor in any case.

### Stage E comparison

Stage E's `edge-scores.json` does not exist for this date. Stage E's Routine has been stopped since 2026-10-19, so there is no ρ against it. Within this run, the searcher's own `impact_sum` and the panel's signed `panel_pct` rank at Spearman ρ = **+0.96** over the 20 names: the panel reordered the middle of the day and mostly kept its extremes.

### What the numbers are not

- `expected_return_pct` (and `expected_edge_pct` on a selected name) is what names at that percentile have earned. Its out-of-sample record is weak (correlation +0.12 with the realised return over 148 names). It is not a forecast to size on.
- The weights are research; nothing trades them. The book follows `execution.panel` in `alpaca_trade.py`.
- Certainty (`p_up`) is recorded and decides nothing.
- The searcher's `impact_sum` is not a return forecast. Below the 2.8 floor its sign is a coin flip on the evidence so far. Only NIU (-5.0) and XTNT (-4.5) clear it.
- Nothing checked the findings for being factually wrong: there is no adversary. The key has not been shown to reproduce to better than its own size; when the stage still double-hunted, four of twelve paired names came back with opposite signs.

### Standing sections

- **Sign balance (searcher):** 8 positive, 1 zero (POET), 11 negative. Panel: 8 long, 12 short. Opus 5 noted its own 13/6/1 negative lean as the pessimism artefact `LESSONS.md` warns about.
- **Baseline quality:** a usable option chain existed only for the large caps (TSN with an event-implied 5.32% move and +2.76 put skew; BEKE 5.19% with +4.09 put skew; ARMK, HTHT and POET with thin chains). Most names run on the historical-reaction fallback. Twelve baselines had untrustworthy 6-K reaction histories (BIDU, BEKE, HTHT, XPEV, IQ, BLDP, POET, NIU, QVCG and others), and their searchers rebuilt the base rate from confirmed prints.
- **Capacity:** of the 20 hunted names, GAME, CREX, XTNT and NIU are below the $0.2m turnover floor. VENU, VERI and LNZA are thin. IQ and LNZA are not lendable at Alpaca on this snapshot. The day's two strongest convictions are untradeable at Alpaca.
- **Unsettled session:** QVCG. The company says only "Monday Nov 16" for the 10-Q; past filings landed at 08:34, 14:25 and 16:18 ET.
- **Not hunted:** CYCU, USDE, DTST, TRNR, EDBL, XXII and PERI were confirmed but cut on priority. TOYO, XTND, NKLR, SMID, ROLR, BBGI, ELWT, CMCT, VIDA, CSAI, EHLD and PDCC were cut as unconfirmed. Unfinished research: none.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects or sizes on them. The per-name values are in the stage E-P score_report table in the run's closing reply and in `edge-context.json`.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
