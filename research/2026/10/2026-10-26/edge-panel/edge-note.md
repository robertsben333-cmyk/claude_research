# Stage E-P — 2026-10-26 amc + 2026-10-27 bmo

**This is stage E-P: Opus 5.5 searchers, then a blind panel of four models judging their evidence.** Since 2026-10-19 this stage also trades the Alpaca paper account. Step 3s sold the previous book (MED, 438 shares, +4.58% unrealised). Step 6b buys the panel's selection after this note.
**All four judges ran:** Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each used its pinned agent, each covered 20 of 20 packs, and no fallback was needed.
**One day is an anecdote.** Twenty names cannot establish anything. The result is the pooled record.

## How the day was cut

- **Universe:** 105 names in the window (40 amc 10-26, 65 bmo 10-27), all with sealed baselines.
- **Sweep:** checked 24 of the 105 in its 12-minute budget. It company-confirmed 11, proved 0 phantoms, left 9 checked but unconfirmed (likely calendar projections) and 81 unchecked.
- **Hunted, at the cap of 20:**
  - the 11 confirmed: CLS, WHR, RMBS, AEYE, ZDGE, PSMT and BLX (amc); GLXY, DQ, CBC and SNDL (bmo);
  - the 9 highest-priority unchecked: AMKR, SOFI, JBLU, KNSA, AGYS, CNC, PII, CVLT and GLW.
- **Shed:** 85 names, by `edge_degrade_order`. Large caps among them (KO, BA, NVS, SPGI and others) were not hunted, so this is not a complete ranking of the window.
- **Events:** every searcher settled its own event from a company source. All 20 are confirmed and rankable.

## Panel table (ranked on `panel_pct`)

**How to read the table:**
- **`panel_pct`** is the mean of the four judges' percentiles. Each judge is read against its own live range (n=176 earlier sizes each).
- **Judge columns:** each judge's percentile is 0–100 with L/S for its side. `*` marks a judge's own top 20%.
- **E[return]** is what names at this percentile have earned on the panel's side. It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. It is the percentile translated into a return, not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KNSA | bmo 10-27 | **yes** | 98 | long | 1 | 97L* | 98L* | 99L* | 96L* | 4 | +2.68 | +2.90 | +4.93% [+3.04, +6.61] | 0.72 | 1.0 | 1.25 |
| 2 | CLS | amc 10-26 | **yes** | 95 | long | 4 | 98L* | 96L* | 89L* | 96L* | 4 | +2.18 | +0.60 | +4.71% [+2.72, +6.47] | 0.71 | 1.0 | 0.99 |
| 3 | GLXY | bmo 10-27 | **yes** | 92 | long | 2 | 90L* | 94L* | 92L* | 94L* | 4 | +1.92 | +2.20 | +4.42% [+2.38, +6.27] | 0.70 | 1.0 | 1.25 |
| 4 | AEYE | amc 10-26 | **yes** | 90 | long | 6 | 79L | 96L* | 92L* | 92L* | 4 | +1.81 | +1.40 | +4.04% [+1.94, +5.99] | 0.68 | 1.0 | 1.00 |
| 5 | CVLT | bmo 10-27 | **yes** | 90 | short | 6 | 90S* | 96S* | 80S* | 92S* | 4 | −1.76 | −1.20 | +4.02% [+1.92, +5.98] | 0.68 | 1.0 | 0.88 |
| 6 | DQ | bmo 10-27 | | 78 | long | 7 | 82L* | 88L* | 71L | 73L | 2 | +1.18 | +1.90 | +2.43% [+0.55, +4.33] | 0.59 | 0 | 0 |
| 7 | SOFI | bmo 10-27 | | 77 | short | 6 | 84S* | 68S | 74S | 81S* | 2 | −1.05 | −0.30 | +2.20% [+0.45, +4.06] | 0.58 | 0 | 0 |
| 8 | PSMT | amc 10-26 | | 76 | long | 6 | 69L | 86L* | 77L | 73L | 2 | +1.00 | +0.30 | +2.16% [+0.44, +4.02] | 0.58 | 0 | 0 |
| 9 | RMBS | amc 10-26 | | 76 | long | 21 | 44L | 96L* | 71L | 92L* | 2 | +1.27 | +1.10 | +2.08% [+0.40, +3.92] | 0.57 | 0 | 0 |
| 10 | JBLU | bmo 10-27 | | 75 | long | 25 | 89L* | 87L* | 32L | 92L* | 3 | +1.53 | +1.70 | +2.01% [+0.37, +3.83] | 0.57 | 0 | 0 |
| 11 | BLX | amc 10-26 | | 72 | short | 5 | 69S | 80S | 66S | 73S | 0 | −1.00 | −1.00 | +1.75% [+0.29, +3.50] | 0.56 | 0 | 0 |
| 12 | SNDL | bmo 10-27 | | 66 | short | 13 | 44S | 76S | 71S | 72S | 0 | −0.87 | −1.20 | +1.24% [+0.07, +2.85] | 0.56 | 0 | 0 |
| 13 | AGYS | amc 10-26 | | 64 | long | 22 | 32L | 74L | 92L* | 59L | 1 | +0.85 | +0.50 | +1.13% [+0.02, +2.71] | 0.56 | 0 | 0 |
| 14 | WHR | amc 10-26 | | 61 | long | 36 | 90L* | 0 | 77L | 77L | 2 | +1.05 | +0.70 | +0.90% [−0.09, +2.39] | 0.56 | 0 | 0 |
| 15 | ZDGE | amc 10-26 | | 39 | long | 58 | 48S | 93L* | 21L | 90L* | 2 | +0.91 | +2.00 | +0.29% | 0.56 | 0 | 0 |
| 16 | AMKR | amc 10-26 | | 24 | long | 47 | 26S | 79L | 18S | 62L | 0 | +0.28 | +0.10 | +0.29% | 0.56 | 0 | 0 |
| 17 | GLW | bmo 10-27 | | 14 | long | 19 | 7S | 44L | 8L | 11L | 0 | +0.20 | +1.00 | +0.29% | 0.56 | 0 | 0 |
| 18 | CNC | bmo 10-27 | | 10 | long | 38 | 48L | 34L | 8L | 51S | 0 | +0.28 | 0.00 | +0.29% | 0.56 | 0 | 0 |
| 19 | PII | bmo 10-27 | | 2 | short | 27 | 12S | 13L | 32L | 40S | 0 | −0.02 | +0.50 | +0.29% | 0.56 | 0 | 0 |
| 20 | CBC | bmo 10-27 | | 1 | long | 1 | 0 | 3L | 0 | 0 | 0 | 0.00 | +0.20 | +0.29% | 0.56 | 0 | 0 |

**Selected (mean percentile ≥ 80, all four judges present):** KNSA, CLS, GLXY and AEYE long; CVLT short.
- **The old 3-of-4 rule** picks the same five plus JBLU (k=3). Sonnet 5.5 is at 32L on JBLU while the other three are in their own top 20%.
- **Searcher's key:** it puts one name over the 2.8 floor, KNSA at +2.90.
- **Turnover:** ZDGE ($0.13m a day) is below the $200k turnover floor. AEYE ($0.59m) is thin.

## The selected names

**KNSA (Kiniksa), long, 98.**
- *For:* Q3 consensus revenue of $260.7M implies only +$17M on Q2. Every non-Q1 quarter since Q1 2025 stepped up $19–29M, and the company's own FY guide implies $261–268M a quarter for the second half. The guide was raised at both 2026 prints, and both prints moved +23–25%.
- *Against:* management flagged gross-to-net pressure from co-pay changes. The stock fell 9.9% over 5 days into the print with no news found. The bar rests on one vendor family (MarketBeat).

**CLS (Celestica), long, 95.**
- *For:* the 2026 Investor Day (10-27, 08:30 ET) falls inside the window, with a multi-year target reset. Partner read-throughs point up: Broadcom's FY27–28 AI revenue and Jabil's AI guide. The company has beaten its EPS consensus 8 quarters out of 8. The stock is −24% in 20 days on a sector-wide AI selloff.
- *Against:* no sell-side 2027–28 bar could be sourced for the Investor Day targets to be judged against. Beats were sold in January (−13%) and April (−14%). Puts are bid (skew +8.3). OpenAI financing doubts hit a named growth leg.
- The searcher sized it at only +0.60; the panel ranks it second.

**GLXY (Galaxy Digital), long, 92.**
- *For:* BTC was +43% and ETH +71% in Q3, after a Q2 treasury mark loss, so Q3 should swing to a large mark-to-market gain. The call is the first chance for management to speak to the CoreWeave credit scare; CoreWeave is the sole Helios tenant. Short interest has built four settlements running (6.7 days to cover).
- *Against:* the EPS bar is disputed (−$0.12, +$0.05 and −$0.44). The gains sit below operating income. The stock fell after 5 of its last 7 prints. BTC drifted to about $80k in October.

**AEYE (AudioEye), long, 90.**
- *For:* a $15m buyback was authorised a week before the print, about 15% of the market cap. The company has a record of beating its own EBITDA guide.
- *Against:* revenue consensus ($11.13m) sits above the top of the company's own range. The stock ran +14.8% in 5 sessions after the buyback. It is thin at about $0.59m a day of turnover, and Opus 5 is only at 79L.

**CVLT (Commvault), short, 90.**
- *For the short:* the stock has re-run its July setup: +13% in 20 days, six October target raises, then −19.7% on an unraised ARR guide. Rubrik ran up, beat and fell 12% in August. The memory and server shortage tightened through the quarter.
- *Against the short:* skew pays for upside (−6). A pricing-and-packaging initiative earned a performance fee by June. Peer Rubrik beat and raised every metric. The Q2 subscription guide sits below the Q1 actual, so a revenue beat is likely.

## Where the panel and the searcher disagree most

- **ZDGE:** searcher +2.00. Panel 39 long with the day's widest spread (sd 58): Opus 5.5 93L and Fable 90L, against Opus 5 48S. It is untradable at $0.13m a day in any case.
- **CLS:** searcher +0.60. Panel 95 long.
- **GLW:** searcher +1.00. Panel 14.
- **WHR:** Opus 5 is at 90L while Opus 5.5 sized it exactly zero (p_up 50).
- **JBLU:** Sonnet 5.5 is at 32L while the other three are at 87–92L.

## Stage E comparison

Stage E's `edge/` directory does not exist for this date, because stage E's Routine is stopped. There is no overlap and no ρ to report.

## What the numbers are not

- `expected_return_pct` (and `expected_edge_pct` on a selected name) is what past names at this percentile have earned. Its out-of-sample record is weak: correlation +0.12 with the realised return over 148 names. It is not a forecast to size on.
- `weight_equal` and `weight_precision_tilt` are research columns. The book is sized by `execution.panel` (`panel_pct` − 60, 50% cap), not by these.
- Each judge's certainty (`p_up`) is recorded and decides nothing.

## Standing caveats

- **Sign balance.**
  - Searcher sums: 15 lean long, 4 short and 1 is zero.
  - On the panel's side: 16 long and 4 short.
- **Nothing checked the findings.** A factually wrong finding enters at full size. Several key figures came from search snippets because pages returned 403:
  - DQ's EPS consensus;
  - ZDGE's single-source bar;
  - CVLT's StockStory estimate.
- **The key is not reproducible to better than its own size.** Under the old double hunt, four of twelve paired names came back with opposite signs.
- **Baselines.**
  - **Untrustworthy reaction histories:** BLX, DQ and SNDL. Their baselines picked up non-earnings 6-Ks, so the searchers rebuilt the base rate from confirmed prints.
  - **Option chains:** usable on most large names (CLS, AMKR, RMBS, GLXY, AGYS, CVLT, JBLU, GLW, CNC, SOFI, WHR). None on AEYE, ZDGE, PSMT, BLX, SNDL, KNSA or CBC.
- **Capacity.** ZDGE is below the turnover floor and AEYE is thin; every other name clears $1m a day.

## Context: retail, search and volatility (not used for selection)

These columns are in `edge-context.json` and in the score_report table. They are context only. The Google search half hit its time budget for many names today.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
