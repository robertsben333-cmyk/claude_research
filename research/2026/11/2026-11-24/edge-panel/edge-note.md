# Stage E-P — edge hunt (panel), 2026-11-24 amc + 2026-11-25 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel; the book it selects is placed on the live and paper Alpaca accounts at step 6b.**
All four members ran (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), on their pinned agents; all four were rate-limited (HTTP 429) on first launch and resumed after the reset, same agents, same packs.
One day is an anecdote.

## The panel table

Percentiles are each judge's own, 0-100, against its last 200 live sizes; side apart (L/S); `*` = in that judge's own top 20%. E[return] is what names at that panel_pct have earned on the panel's side: gross, scorebord window, flat at about +0.3% below a percentile of 50. It is the translation of the percentile, not a separate forecast.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80%) | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NNOX | bmo | yes | 99 | short | 1 | 100S* | 97S* | 100S* | 98S* | 4 | -2.86 | -3.50 | +5.02% [+3.18, +6.67] | 0.73 | 1.00 | 1.03 |
| 2 | QFIN | amc | yes | 96 | short | 2 | 98S* | 93S* | 94S* | 97S* | 4 | -2.15 | -1.80 | +4.79% [+2.83, +6.53] | 0.72 | 1.00 | 1.24 |
| 3 | DELL | amc | yes | 92 | long | 4 | 86L* | 97L* | 94L* | 91L* | 4 | +1.79 | +3.60 | +4.34% [+2.29, +6.22] | 0.70 | 1.00 | 0.97 |
| 4 | AMBA | amc | yes | 83 | short | 10 | 92S* | 78S | 70S | 91S* | 2 | -1.52 | -1.50 | +3.02% [+0.97, +5.00] | 0.63 | 1.00 | 0.75 |
| 5 | BBAR | amc |  | 71 | short | 7 | 62S | 68S | 78S | 78S | 0 | -1.06 | -2.00 | +1.66% [+0.25, +3.38] | 0.56 | 0.00 | 0.00 |
| 6 | NTNX | amc |  | 69 | long | 6 | 74L | 64L | 75L | 62L | 0 | +0.98 | +1.60 | +1.46% [+0.18, +3.13] | 0.56 | 0.00 | 0.00 |
| 7 | GDS | bmo |  | 61 | long | 17 | 73L | 58L | 34L | 78L* | 1 | +0.93 | +1.40 | +0.88% [-0.10, +2.36] | 0.56 | 0.00 | 0.00 |
| 8 | ADSK | amc |  | 52 | short | 14 | 68S | 30S | 50S | 62S | 0 | -0.71 | -0.95 | +0.33% [-0.36, +1.64] | 0.56 | 0.00 | 0.00 |
| 9 | WDAY | amc |  | 50 | long | 10 | 56L | 58L | 34L | 53L | 0 | +0.75 | +0.30 | +0.29% [-0.42, +1.45] | 0.56 | 0.00 | 0.00 |
| 10 | HPQ | amc |  | 45 | short | 7 | 38S | 39S | 50S | 53S | 0 | -0.56 | -0.40 | +0.29% [-0.49, +1.10] | 0.56 | 0.00 | 0.00 |
| 11 | GOTU | bmo |  | 36 | short | 4 | 38S | 40S | 30S | 35S | 0 | -0.48 | -0.80 | +0.29% [-0.54, +0.88] | 0.56 | 0.00 | 0.00 |
| 12 | LI | bmo |  | 35 | long | 15 | 48L | 52L | 14L | 26L | 0 | +0.53 | +1.30 | +0.29% [-0.54, +0.87] | 0.56 | 0.00 | 0.00 |
| 13 | URBN | amc |  | 26 | long | 35 | 30S | 54L | 56L | 22L | 0 | +0.51 | +0.40 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 14 | GASS | bmo |  | 24 | long | 13 | 35L | 6L | 17L | 38L | 0 | +0.38 | +1.10 | +0.29% [-0.58, +0.84] | 0.56 | 0.00 | 0.00 |
| 15 | BZ | bmo |  | 21 | short | 24 | 40S | 20L | 24S | 38S | 0 | -0.43 | +1.00 | +0.29% [-0.59, +0.82] | 0.56 | 0.00 | 0.00 |
| 16 | DE | bmo |  | 18 | short | 30 | 33L | 40S | 34S | 33S | 0 | -0.43 | +0.70 | +0.29% [-0.61, +0.82] | 0.56 | 0.00 | 0.00 |
| 17 | CLSK | amc |  | 12 | long | 27 | 48L | 24L | 24S | 0- | 0 | +0.15 | -0.70 | +0.29% [-0.67, +0.80] | 0.56 | 0.00 | 0.00 |
| 18 | NOAH | amc |  | 11 | short | 3 | 12S | 6S | 14S | 12S | 0 | -0.22 | -0.40 | +0.29% [-0.68, +0.80] | 0.56 | 0.00 | 0.00 |
| 19 | HDL | bmo |  | 5 | long | 3 | 10L | 3L | 2L | 4L | 0 | +0.11 | +0.10 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |
| 20 | DSX | bmo |  | 2 | long | 9 | 12S | 3L | 9L | 8L | 0 | +0.12 | +0.10 | +0.29% [-0.75, +0.78] | 0.56 | 0.00 | 0.00 |

**Selected (panel_pct >= 80, all four judges): NNOX short (99), QFIN short (96), DELL long (92), AMBA short (83).** BBAR (71 short) is the nearest miss. NNOX is not lendable at Alpaca on this snapshot (check borrow at IBKR), so the book drops it before the split.

## The selected names

**NNOX — short, 99, 4 of 4.** All four judges cite the same mechanism: a $50M Yorkville standby equity facility (signed 2026-11-12, about 3x the ~$17M market cap, priced at 97% of the lowest VWAP, resale 424B5 on 11-23), a 07:00 ET 11-25 special meeting voting a 1:20-1:50 reverse split and 200M more authorised shares against 80.4M outstanding, going-concern doubt, and a possible impairment; the Q2 precedent (pre-released quarter, still about -19%). Case against: Q3 revenue was pre-released, the stock is at its 52-week low after -35% since the SEPA, market cap is below cash, and an announced opex cut could land. Untradable short at Alpaca today.

**QFIN — short, 96, 4 of 4.** Management's own August statements (C-M2 rising, 2-3 quarters to normalise, funding costs up ~25bp, "extra cautious"), a first guide from a CEO who was chief risk officer, the 2026-09-30 marketing rules, and four straight guide-cut selloffs (-8% to -19%). Case against: about 1.9x forward earnings, liquid assets ~2.4x the market cap with the buyback suspended (a restart would be a large positive), stock -76% from its high; the Q4 bar is unsourced.

**DELL — long, 92, 4 of 4.** A Q3 guide ($6.50) below Q2's actual after 47% and 68% beats of its own guide; Nvidia, Lenovo ISG, CoreWeave, SMCI and Wistron all ran strong over Dell's quarter; a 41% de-rating in 20 days on macro news. Case against: IDC/Gartner have Dell PC units about -25% against a +15% client guide, a possible first AI backlog decline, HPE guiding its AI margin down for FY27 (the stock fell ~12% intraday on that), and memory costs into Q4.

**AMBA — short, 83, 2 of 4 in own top 20% (Opus 5 92, Fable 91; Opus 5.5 78, Sonnet 70).** Management flagged Q4 memory-supply risk, Himax and Mobileye guided Q4 down, inventory days 157, and the name fell after 6 of its last 7 prints. Case against: upside skew (calls bid), an unconfirmed NXP takeover tail, a SOX crash this week that may dominate the reaction, and no sourced Q4 consensus.

## Where the panel and the searcher disagree most

Spearman rho between the searcher's impact_sum and panel_pct_signed: **+0.88 over 20 names**, so they mostly agree.
- AMBA: searcher -1.50 (rank 17 of 20) against panel 83 short, selected; the judges weighted the Q4 memory guide more than the searcher did.
- QFIN: searcher -1.80 against panel 96 short; same direction, the panel more confident.
- GASS / BZ / LI: searcher +1.10 / +1.00 / +1.30, panel 24 / 21 / 35; the judges call these near non-results.

## Stage E comparison

Stage E's `<RUN>/edge/edge-scores.json` does not exist for this date (stage E's Routine is stopped), so no overlap or rho against it.

## Run notes

- Window: 24 calendar rows; sweep confirmed 16, 1 phantom (PSNY), 20 hunted (4 unconfirmed by priority: DELL, URBN, BBAR, GASS, all confirmed by their searchers); shed OMSE, YSG, ADXN, PSNY.
- The first wave of 8 searchers in one turn exhausted the shared 200-call WebSearch budget; 7 came back unfinished and were relaunched in later turns. Final: 20 of 20 `search_complete`, none unfinished.
- SEC_USER_AGENT is unset in this environment, so foreign issuers' 6-K reaction histories were empty; searchers rebuilt them from confirmed releases.
- Searcher conviction floor (2.8): DELL +3.60 and NNOX -3.50 clear it (comparison arm only).

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct` on a selected name) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names); it is not a forecast to size on. The weights in the table are research. `p_up` is recorded and decides nothing. Nothing checked the searchers' findings for factual error. The book rule is `execution.panel` in `config/pipeline.yaml`, applied by `alpaca_trade.py`.

## Context: retail, search and volatility (not used for selection)

See `edge-context.json` (run with --no-search for time; search spike not run). Context only.

## Book placed (step 6b)

Live ($3,228 equity): QFIN short 271 @ 4.6801, DELL long 3 @ 295.777, AMBA short 17 @ 47.25; gross $2,958 (91.6%). Paper ($22,135): QFIN short 1,864 @ 4.68, DELL long 26 @ 295.73, AMBA short 118 @ 47.08; gross $21,985 (99.3%). NNOX dropped (not shortable at Alpaca); top-up not applied (3 strong names). DELL is 27.5% live against 34.8% paper because of whole shares.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
