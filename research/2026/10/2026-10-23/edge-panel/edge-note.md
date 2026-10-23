# Stage E-P — 2026-10-23 amc + 2026-10-26 bmo

**This is stage E-P: Opus 5.5 searchers, then a blind panel of four models judging their evidence.** Since 2026-10-19 this stage also trades the Alpaca paper account: it sold the previous book at step 3s, and step 6b buys the panel's selection after this note.
**All four judges ran:** Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each used its pinned agent, each covered 12 of 12 packs, and no fallback was needed.
**One day is an anecdote.** Twelve names cannot establish anything. The result is the pooled record.

## Panel table (ranked on `panel_pct`)

`panel_pct` is the mean of the four judges' percentiles, each read against that judge's own live range (n=164 earlier sizes each). Each judge's percentile is 0-100 with L/S for its side; `*` marks a judge's own top 20%. E[return] is what names at this percentile have earned on the panel's side: gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. It is the percentile translated into a return, not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MED | bmo 10-26 | **yes** | 96 | long | 2 | 96L* | 98L* | 98L* | 94L* | 4 | +2.45 | +1.80 | +4.85% [+2.93, +6.57] | 0.72 | 1.0 | 1.0 |
| 2 | BMRC | bmo 10-26 | | 66 | long | 9 | 79L | 54L | 65L | 67L | 1 | +0.80 | +0.85 | +1.28% [+0.09, +2.90] | 0.56 | 0 | 0 |
| 3 | DEA | bmo 10-26 | | 64 | short | 10 | 79S | 61S | 65S | 50S | 1 | −0.75 | −0.60 | +1.10% [+0.01, +2.67] | 0.56 | 0 | 0 |
| 4 | ARLP | bmo 10-26 | | 55 | long | 14 | 77L | 42L | 44L | 58L | 1 | +0.62 | +0.25 | +0.40% [−0.28, +1.89] | 0.56 | 0 | 0 |
| 5 | ABOS | bmo 10-26 | | 49 | short | 7 | 49S | 40S | 59S | 48S | 0 | −0.61 | −0.70 | +0.29% | 0.56 | 0 | 0 |
| 6 | BOH | bmo 10-26 | | 39 | long | 11 | 49L | 48L | 21L | 37L | 0 | +0.53 | +0.50 | +0.29% | 0.56 | 0 | 0 |
| 7 | RCBC | amc 10-23 | | 36 | long | 13 | 45L | 37L | 48L | 15L | 0 | +0.47 | +0.70 | +0.29% | 0.56 | 0 | 0 |
| 8 | BFST | bmo 10-26 | | 34 | short | 22 | 65S | 23S | 7S | 40S | 0 | −0.40 | −0.20 | +0.29% | 0.56 | 0 | 0 |
| 9 | CX | bmo 10-26 | | 31 | long | 18 | 49L | 16L | 10L | 48L | 0 | +0.41 | −0.10 | +0.29% | 0.56 | 0 | 0 |
| 10 | VZ | bmo 10-26 | | 29 | long | 17 | 2L | 34L | 32L | 48L | 0 | +0.40 | +0.15 | +0.29% | 0.56 | 0 | 0 |
| 11 | MMYT | bmo 10-26 | | 25 | long | 38 | 34L | 76L | 32S | 24L | 0 | +0.40 | +0.80 | +0.29% | 0.56 | 0 | 0 |
| 12 | HBT | bmo 10-26 | | 19 | long | 8 | 27L | 27L | 10L | 12L | 0 | +0.26 | +0.30 | +0.29% | 0.56 | 0 | 0 |

**Not ranked: LKFN.** The searcher found no company source for the 2026-10-26 date (aggregators and cadence only), so `event_confirmed` is false and it is outside the ranking. Its searcher sized it at +1.30.

The old 3-of-4 rule picks the same set: MED, 4 of 4. The searcher's own key puts no name over the 2.8 floor; MED is highest at +1.80.

## The selected name

**MED (Medifast), long, panel_pct 96, all four judges in their own top 20%.** The judges' notes rest on three items:
- **The guide.** Q3 consensus EPS of −$0.60 sits at the bottom of the company's own improved −$0.15 to −$0.65 range. The company beat its Q2 guide widely (−$0.28 against −$0.50 to −$1.00), and the stock rose +34% and +22% on its last two prints.
- **The savings.** The CFO promised on the Q2 call that this call would quantify the Catalyst cost savings, and FY consensus sits below the low end of the company's FY guide.
- **The cash floor.** About $169.8m of cash and investments and no debt, against a market cap near $132m, with a Steamboat director buying about 131k shares at $11.6–12.3 in August.

**The strongest case against:**
- Q3 is the seasonally weakest quarter. Applying last year's Q2-to-Q3 pattern gives about $65m of revenue against a $69.2m consensus.
- Short interest fell 43% into the 2026-09-30 settlement, so the squeeze fuel behind the last two rallies is much smaller.
- The event date rests on a ScanX relay of the company's announcement. The IR page returned 404, and some calendars still list early November.
- Turnover is about $1.26m a day: tradable, but thin.

## Where the panel and the searcher disagree most

- **MMYT:** searcher +0.80; panel 25 long with the widest spread of the day (sd 38). Opus 5.5 is at 76L, Sonnet 5.5 at 32S.
- **CX:** searcher −0.10; panel 31 long.
- **ARLP:** searcher +0.25; panel 55 long, led by Opus 5 at 77L.
- **VZ:** Opus 5 sits at 2L while the other three are at 32–48L.

## Stage E comparison

Stage E's `edge/` directory does not exist for this date, because stage E's Routine is stopped. There is no overlap and no ρ to report.

## What the numbers are not

- `expected_return_pct` is what past names at this percentile have earned. Its out-of-sample record is weak: correlation +0.12 with the realised return over 148 names. It is not a forecast to size on.
- `weight_equal` and `weight_precision_tilt` are research columns; nothing trades them.
- Each judge's certainty (`p_up`) is recorded and decides nothing.

## Standing caveats

- **Sign balance.** Of the 12 searcher sums, 8 lean long and 4 short. On the panel's side, 9 are long and 3 short.
- **Nothing checked the findings.** A factually wrong finding enters at full size.
- **The key is not reproducible to better than its own size.** Under the old double hunt, four of twelve paired names came back with opposite signs.
- **Most baselines are inferred, not measured.** Only VZ, MMYT, ARLP and BOH had an option chain good enough to give an implied move. MMYT, CX and RCBC carry untrustworthy reaction histories, so their searchers rebuilt the base rate.
- **Searcher hygiene.** BOH's searcher met a misdated Investing.com line quoting an "Oct 26" price and rejected it. It is not in any finding.

## Context: retail, search and volatility (not used for selection)

These columns are in `edge-context.json` and in the score_report table. They are context only. The search half failed or came back sparse for several names today.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
