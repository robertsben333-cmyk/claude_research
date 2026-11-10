# Stage E-P — 2026-11-10 amc + 2026-11-11 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** The panel's book is traded on the Alpaca paper account in step 6b. Stage E's Routine is stopped, so this stage is the only one connected to the account.
**All four members ran on their pinned agents:** Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each covered 20/20 names in one part, with no fallback and no retry.
**One day is an anecdote.** Only the pooled record says anything.

## Panel table (every rankable name)

Each judge is shown as a percentile of its own live range, 0-100, with L/S for its side; `*` marks a name in that judge's own top 20%. `E[ret]` is the expected return at that panel_pct, the translation of the percentile and not a separate forecast. It is gross, on the scorebord's window, with an 80% band and the hit rate, and it is flat at about +0.3% below a percentile of 50.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[ret] [80%] | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NRGV | 2026-11-10 amc | **yes** | 89 | long | 3 | 88L* | 92L* | 85L* | 90L* | 4 | +1.56 | +2.90 | +3.93% [+1.83, +5.89] | 0.68 | 1.00 | 1.00 |
| 2 | AMPX | 2026-11-10 amc or 11-11 bmo (unsettled by sweep; searcher: likely 11-10 amc; reaction in the 11-11 session either way) |  | 79 | long | 4 | 76L | 74L | 86L* | 79L* | 2 | +1.19 | +3.10 | +2.47% [+0.56, +4.38] | 0.59 | 0.00 | 0.00 |
| 3 | STUB | 2026-11-10 amc |  | 74 | short | 9 | 84S* | 74S | 60S | 77S | 1 | -1.15 | -0.30 | +1.92% [+0.34, +3.71] | 0.56 | 0.00 | 0.00 |
| 4 | FOSL | 2026-11-10 amc |  | 73 | long | 12 | 90L* | 60L | 66L | 77L | 1 | +1.02 | +2.00 | +1.84% [+0.32, +3.62] | 0.56 | 0.00 | 0.00 |
| 5 | CRWV | 2026-11-10 amc |  | 71 | long | 21 | 98L* | 66L | 40L | 79L | 1 | +1.07 | +0.60 | +1.63% [+0.25, +3.35] | 0.56 | 0.00 | 0.00 |
| 6 | LPTH | 2026-11-10 amc |  | 69 | long | 11 | 77L | 82L* | 60L | 58L | 1 | +1.01 | +1.40 | +1.50% [+0.20, +3.18] | 0.56 | 0.00 | 0.00 |
| 7 | MRCY | 2026-11-10 amc |  | 64 | long | 8 | 60L | 76L | 55L | 66L | 0 | +0.91 | +1.40 | +1.12% [+0.01, +2.69] | 0.56 | 0.00 | 0.00 |
| 8 | RSKD | 2026-11-11 bmo |  | 59 | long | 16 | 80L* | 43L | 45L | 69L | 1 | +0.77 | +0.30 | +0.74% [-0.15, +2.21] | 0.56 | 0.00 | 0.00 |
| 9 | ODD | 2026-11-11 bmo |  | 57 | long | 34 | 0- | 68L | 71L | 90L* | 1 | +0.98 | +1.50 | +0.56% [-0.22, +2.04] | 0.56 | 0.00 | 0.00 |
| 10 | EVLV | 2026-11-10 amc |  | 38 | short | 12 | 57S | 32S | 25S | 37S | 0 | -0.44 | -0.50 | +0.29% [-0.53, +0.90] | 0.56 | 0.00 | 0.00 |
| 11 | SONO | 2026-11-10 amc |  | 28 | short | 21 | 45S | 36S | 8L | 40S | 0 | -0.50 | +0.40 | +0.29% [-0.57, +0.85] | 0.56 | 0.00 | 0.00 |
| 12 | NYAX | 2026-11-11 bmo |  | 27 | long | 12 | 24L | 43L | 32L | 10L | 0 | +0.37 | -1.10 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 13 | CAPR | 2026-11-10 amc |  | 24 | long | 30 | 24S | 40L | 55L | 24L | 0 | +0.42 | +2.50 | +0.29% [-0.58, +0.83] | 0.56 | 0.00 | 0.00 |
| 14 | FRNM | 2026-11-10 amc |  | 22 | short | 18 | 40S | 6S | 40S | 0- | 0 | -0.27 | -0.10 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 15 | FLY | 2026-11-10 amc |  | 21 | short | 23 | 36S | 10L | 8S | 49S | 0 | -0.31 | -1.50 | +0.29% [-0.59, +0.82] | 0.56 | 0.00 | 0.00 |
| 16 | ATEX | 2026-11-10 amc |  | 18 | short | 26 | 36S | 40S | 25L | 24S | 0 | -0.41 | +0.55 | +0.29% [-0.61, +0.82] | 0.56 | 0.00 | 0.00 |
| 17 | NN | 2026-11-10 amc |  | 18 | long | 12 | 32L | 0- | 25L | 16L | 0 | +0.29 | -0.10 | +0.29% [-0.62, +0.82] | 0.56 | 0.00 | 0.00 |
| 18 | REZI | 2026-11-10 amc |  | 12 | short | 36 | 32S | 0- | 40L | 58S | 0 | -0.22 | +0.50 | +0.29% [-0.67, +0.81] | 0.56 | 0.00 | 0.00 |
| 19 | RGTI | 2026-11-10 amc |  | 12 | short | 28 | 45S | 9S | 32L | 24S | 0 | -0.25 | +1.40 | +0.29% [-0.68, +0.80] | 0.56 | 0.00 | 0.00 |
| 20 | KURA | 2026-11-10 amc |  | 8 | long | 21 | 14S | 12S | 25L | 33L | 0 | +0.05 | +0.60 | +0.29% [-0.70, +0.79] | 0.56 | 0.00 | 0.00 |

The panel selects on all four members present and panel_pct >= 80. **Selected: NRGV long, panel_pct 89, all four members in their own top 20% (4 of 4).** It is the only name selected. The next two fall short of 80: AMPX long 79 (two members in their own top 20%), then STUB short 74.

## The selected name

**NRGV (Energy Vault), long, panel_pct 89, spread 3.** Every member names the same evidence:

- **The first FY2027 revenue guide.** The company pre-committed to it in its 2026-10-14 release, which also raised FY26 to the top half of $270-310m ([GreenStockNews repost](https://greenstocknews.com/news/nyse/nrgv/energy-vault-schedules-conference-call-to-discuss-third-quarter-2026-financial-results-raises-fy-2026-revenue-guidance-to-the-top-half-of-the-previous-range)).
- **The company's own documents point above consensus.** A $500-600m Texas hyperscaler contract lands mostly in 2027, about 40% of the ~$2B backlog converts within 12-18 months, and management guides year-end backlog toward $3B. All of that implies 2027 revenue far above the ~$306m FY27 consensus.
- **A crowded short.** 32.2M shares were short at the 10-15 settlement, about 21% of float with 9.1 days to cover.

**The strongest case against:**

- **Texas permits.** Texas has halted state environmental permits for data centres since 2026-09-21, including air permits, and ERCOT presents its audit on 12-10. That puts the 2027 timing of the off-grid gas-genset project at risk.
- **A single-source bar.** The ~$306m FY27 consensus comes from one aggregator, seen only as a search snippet.
- **A guide that cannot go down.** Q3 revenue is light by design, because most second-half revenue lands in Q4.
- **No explained cause for October's slide.** The stock fell about 28% in October after the raise with no named cause, and was down 5.4% intraday on the print day.
- **The implied move is indicative only.** Its at-the-money spread is 67% of mid.

The searcher's own `impact_sum` is +2.90, which clears the 2.8 conviction floor. This is **recommended with a named reservation**: the Texas permit halt, and a bar resting on one snippet.

## Where the panel and the searcher disagree most

- **CAPR:** the searcher sums +2.50; the panel reads 24 long and is split (Opus 5 short). The judges discounted the squeeze and tone findings that carry the searcher's sum.
- **RGTI:** the searcher sums +1.40; the panel reads 12 short (three of four members short). The judges weighted the 32% two-session run-up on peer news over the squeeze.
- **NYAX:** the searcher sums −1.10; the panel reads 27 long, all four members mildly long. They put the CEO's $8.8m purchase above the guidance-reset arithmetic.
- **STUB:** the searcher's sum is a small −0.30, but the panel reads 74 short (Opus 5 at 84). The judges sized the flat-peer read-through (Live Nation and Vivid Seats) against a stale revenue bar more heavily.
- **CRWV:** members range from 40 to 98 long (spread 21). Opus 5 puts the Core Scientific capacity data at its top; Sonnet 5.5 does not.

## Stage E comparison

Stage E's `<RUN>/edge/edge-scores.json` does not exist for 2026-11-10, because stage E's Routine is stopped. There is therefore no overlap and no Spearman ρ between its `impact_sum` and `panel_pct`.

## What the numbers are not

- **`expected_return_pct` is not a forecast to size on.** It is what names at that percentile have earned, gross, on the scorebord's window, from a curve fitted on 148 resolved panel names. Its out-of-sample record is weak: correlation +0.12 with the realised return. On a selected name, `expected_edge_pct` carries the same expectation as a signed move.
- **The weights are research.** `weight_equal` and `weight_precision_tilt` are recorded, and nothing trades them. The book's own rule is panel_pct − 60, capped at 50% a name.
- **`p_up` is certainty and decides nothing,** because it did not predict on the development names.
- **Nothing checked the findings.** There is no adversary, so a factually wrong finding reaches the judges at face value.
- **The searcher's key is noisy at its own size.** A double hunt once returned opposite signs on 4 of 12 pairs.

## Coverage, sheds and baselines

- **Universe:** 107 names. The sweep checked 43; 35 were confirmed and 7 unconfirmed (VIV, RUM, AADX, BV, AYA, BRCB, GO). EC is a phantom: a 6-K moved its results to 11-12 amc.
- **Hunted:** 20 at the cap. Fifteen lower-priority confirmed names were shed: ATRO, SKYH, KOPN, AZTA, SATL, AEBI, BGSI, AII, INMD, ANGX, PBR, ALC, GIB, ICL and FLNG. The 64 unchecked names were shed too.
- **Searches:** all 20 searchers finished. 0 unfinished, nothing retried.
- **Baselines measured by option chains:** the baseline implied move is mostly unusable today. CAPR, NRGV, ODD, SONO and FOSL all have wide ATM spreads, and several hunts set the scale from the name's own reaction history instead.
- **Borrow and liquidity:** NYAX is thin ($0.97m a day) and not lendable at Alpaca on this snapshot.
- **Sign balance of the searchers:** 14 positive, 6 negative.
- **Free control:** `-run_up_20d_pct` is in each baseline; see `edge-scores.json`.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
