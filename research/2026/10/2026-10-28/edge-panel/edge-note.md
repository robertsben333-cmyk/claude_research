# Stage E-P — 2026-10-28 amc + 2026-10-29 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** Since 2026-10-19 it is the only stage trading the Alpaca paper account (step 6b, after this note is published).
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), natively, 20 of 20 names each, with no fallback.
One day is an anecdote.

Universe: 289 names (134 amc 10-28, 155 bmo 10-29). The sweep checked 34; 30 were company-confirmed and 0 were phantoms. The 20 with the highest priority were searched (12 amc, 8 bmo). Shed: ASTL, RSI, PI, NEO, COHU, ALKT and CLB (confirmed); PHAT, SIMO and TSAT (session unsettled); 255 unchecked. Several searchers (VKTX, CYH, LENZ, HRTG, MAX) ran out of WebSearch budget mid-hunt and fell back to WebFetch on primary documents, so those hunts are thinner than usual.

## Panel table

`panel_pct` is the mean of the judges' own percentiles, 0-100, with the side in its own column. A member cell is that judge's percentile against its own live range: L/S gives its side, and `*` marks a name in that judge's own top 20%. `E[return]` is what names at this percentile have earned on the panel's side. It is one number per percentile, gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile and is not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BFLY | bmo | yes | 100 | long | 0 | 100L* | 99L* | 100L* | 100L* | 4 | +3.63 | +3.70 | +5.07% [+3.25, +6.71] | 0.73 | 1.0 | 1.25 |
| 2 | HRTG | amc | yes | 100 | long | 0 | 100L* | 99L* | 100L* | 100L* | 4 | +3.40 | +1.30 | +5.07% [+3.25, +6.71] | 0.73 | 1.0 | 1.25 |
| 3 | PRCH | amc | yes | 99 | long | 0 | 98L* | 98L* | 100L* | 98L* | 4 | +2.95 | +2.70 | +5.00% [+3.16, +6.66] | 0.73 | 1.0 | 1.0 |
| 4 | VNDA | amc | yes | 97 | short | 2 | 95S* | 99S* | 98S* | 98S* | 4 | -2.84 | -3.70 | +4.92% [+3.02, +6.61] | 0.72 | 1.0 | 1.1266187290219252 |
| 5 | CLPT | amc | yes | 97 | short | 3 | 100S* | 99S* | 91S* | 98S* | 4 | -2.71 | -1.10 | +4.87% [+2.96, +6.58] | 0.72 | 1.0 | 0.9591839355203632 |
| 6 | MVIS | amc | yes | 95 | short | 4 | 98S* | 89S* | 94S* | 97S* | 4 | -2.26 | +0.40 | +4.72% [+2.73, +6.48] | 0.72 | 1.0 | 1.0608826103154776 |
| 7 | NVCR | bmo | yes | 91 | long | 8 | 86L* | 98L* | 100L* | 79L* | 4 | +1.97 | +2.60 | +4.18% [+2.09, +6.10] | 0.69 | 1.0 | 0.75 |
| 8 | BAND | bmo | yes | 90 | long | 6 | 100L* | 86L* | 84L* | 91L* | 4 | +1.58 | +2.60 | +4.15% [+2.06, +6.08] | 0.69 | 1.0 | 0.75 |
| 9 | CYH | amc | yes | 90 | long | 6 | 80L* | 96L* | 90L* | 96L* | 4 | +1.83 | +1.30 | +4.15% [+2.06, +6.08] | 0.69 | 1.0 | 0.8775498914144731 |
| 10 | ESTA | bmo |  | 78 | long | 12 | 58L | 88L* | 82L* | 84L* | 3 | +1.24 | +3.60 | +2.39% [+0.53, +4.29] | 0.59 | 0.0 | 0.0 |
| 11 | FVRR | bmo |  | 73 | short | 8 | 64S | 86S* | 71S | 70S | 1 | -0.92 | +0.20 | +1.81% [+0.30, +3.57] | 0.56 | 0.0 | 0.0 |
| 12 | LENZ | bmo |  | 59 | short | 17 | 64S | 42S | 46S | 85S* | 1 | -0.68 | +1.20 | +0.74% [-0.15, +2.21] | 0.56 | 0.0 | 0.0 |
| 13 | MDXG | amc |  | 54 | long | 28 | 6L | 71L | 71L | 68L | 0 | +0.88 | -0.10 | +0.37% [-0.30, +1.81] | 0.56 | 0.0 | 0.0 |
| 14 | XRX | bmo |  | 50 | short | 54 | 42L | 82S* | 66S | 94S* | 2 | -1.00 | +1.20 | +0.30% [-0.42, +1.46] | 0.56 | 0.0 | 0.0 |
| 15 | MAX | amc |  | 47 | short | 68 | 86S* | 84S* | 71L | 90S* | 3 | -1.40 | -1.20 | +0.29% [-0.46, +1.26] | 0.56 | 0.0 | 0.0 |
| 16 | AWRE | amc |  | 46 | short | 9 | 39S | 42S | 62S | 41S | 0 | -0.50 | -0.10 | +0.29% [-0.47, +1.17] | 0.56 | 0.0 | 0.0 |
| 17 | HIPO | bmo |  | 44 | long | 14 | 30L | 46L | 66L | 33L | 0 | +0.45 | +0.60 | +0.29% [-0.49, +1.05] | 0.56 | 0.0 | 0.0 |
| 18 | HDSN | amc |  | 42 | long | 25 | 6L | 58L | 32L | 70L | 0 | +0.53 | +0.80 | +0.29% [-0.51, +0.98] | 0.56 | 0.0 | 0.0 |
| 19 | TDOC | amc |  | 26 | short | 17 | 42S | 19S | 0- | 41S | 0 | -0.37 | +0.80 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.0 |
| 20 | VKTX | amc |  | 13 | long | 11 | 0- | 30L | 11L | 10L | 0 | +0.19 | +0.70 | +0.29% [-0.67, +0.81] | 0.56 | 0.0 | 0.0 |

**Selected (panel_pct >= 80, all four judges present): BFLY L, HRTG L, PRCH L, VNDA S, CLPT S, MVIS S, NVCR L, BAND L, CYH L.** The old 3-of-4 rule picks the same nine and adds ESTA (k=3, panel_pct 78). Six of the nine are long. Judges sized near (2·p_up−1)·abs_move, so the members agree closely on the top six (sd ≤ 4).

## The selected names

- **BFLY (long, 100).** The judges all lean on the searcher's arithmetic. Embedded licensing at Q2's ~$10.8M cadence plus a flat core puts Q3 at about $30-31M, above the $26-30M guide top and the $28.8-29.9M street. They add the Merge Labs licence signed 09-01 and a rising 12.6% short. *Against:* this is an inference from a secondary transcript with no company Q3 number; core product revenue fell 5% in Q2, so a licensing-only beat is low quality.
- **HRTG (long, 100).** The June reinsurance renewal saves $63.2m a year, about $0.40 a share a quarter, with no Q3 US landfall. The searcher's build is $1.40-1.80 against a disputed $0.91-1.07 consensus, and Universal's Q3 showed the same mechanism. *Against:* Universal's own beat bought only +0.9%; policies and premiums are shrinking; Isaias (10-09) lands in Q4; Q1's 20% EPS gain sold off 20%.
- **PRCH (long, 99).** Third beat-and-raise is the base case: Q2 beat by $10M and guidance was raised twice. Texas cats were benign in Q3, and the short is about 15% of shares. *Against:* the options already price ±18.7% with calls bid. Texas filed rates average −4.3% since July, and an at-the-market share program, including the Reciprocal stake, is coming.
- **VNDA (short, 97).** The FY26 $240-290M guide needs $69-94M a quarter in H2 against about $50.5M in Q2, so a cut looks likely; last year's narrowing traded −20%. *Against:* about 13% of float is short and the stock is at its 52-week low, down 20% in 20 days; two positive Phase III readouts are on the record.
- **CLPT (short, 97).** The guide has been cut twice ($54-60M → $52-56M → $48-52M), each cut trading −14% to −16%, and holding the low end needs a +15% quarter after Q2 fell in every segment. *Against:* the short is crowded (15.2%, 6.6 days) and the stock is up 13% in five days; the consensus bar is disputed ($12.5M vs $13.7M).
- **MVIS (short, 95).** Going-concern language and a $25.6M secured convert redeemable at $3.3M a month. Q3-end cash is estimated near a $17.5M minimum-cash covenant, and the 45-day issuance ban has lapsed; the last raise cost −41% in a day. *Against:* about 20% of shares are short, the FY guide was reaffirmed after Q3 closed, and IRIS orders point to a revenue beat.
- **NVCR (long, 91).** Q3 has run about 5% above underlying Q2 in 2024 and 2025, which builds to $186-189M against a $182-183M consensus. Management said it is aiming for the high end of the guide. *Against:* this is seasonality inferred from history, the euro is 2.6% below the guide's rate, and Fable puts it just outside its own top 20% (79).
- **BAND (long, 90).** Management called the H2 cloud guide conservative because it excludes the Salesforce contact-center ramp, while consensus sits at the midpoint; short interest is 16% at 7 days. *Against:* last quarter's beat-and-raise traded −29%, and Voice grew only 9%.
- **CYH (long, 90).** HCA's Q3 (10-27) held its uninsured hit flat with Q2, which supports CYH's July guide, and UHS admissions rose 4.9%; short float is 11%. *Against:* H1 operating cash flow was −$209M against a +$300-500M FY guide, the EPS bar spans −0.04 to −0.30, and the last two prints fell 12-14%.

## Where the panel and the searcher disagree most

- **HRTG:** the searcher's +1.3 (p77) against panel_pct 100. The judges weighted the reinsurance arithmetic over the shrinking book.
- **CLPT and MVIS:** the searcher's sums are −1.1 and +0.4, but all four judges are in their own bottom 20% (short). The searcher let the crowded shorts offset the guide and financing negatives; the judges did not.
- **ESTA:** the searcher's +3.6 (p97, above the 2.8 floor) against panel_pct 78. Opus 5 discounted it to 58 for a +17 vol-point put skew and 5.5x put open interest.
- **MAX:** the members split (three short at 84-90, Sonnet long at 71), so panel_pct is only 47 against a −1.2 searcher sum.

## Stage E comparison

Stage E's `<RUN>/edge/` does not exist: its Routine is stopped since 2026-10-19. No overlap and no Spearman ρ.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, from a curve fitted on 148 resolved panel names. Its out-of-sample record is weak (correlation +0.12 with the realised return). It is not a forecast to size on. The weights here are research; the book in step 6b uses `execution.panel` (weight panel_pct − 60, cap 50% a name). `p_up` is recorded and decides nothing. Nothing was checked for factual error after the searchers, since there is no adversary pass.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
