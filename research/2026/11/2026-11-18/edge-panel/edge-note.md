# Stage E-P — edge hunt (panel), 2026-11-18 amc + 2026-11-19 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel; it trades the book below on the live and paper Alpaca accounts.** All four members ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), 20 of 20 packs each, no fallback. One day is an anecdote.

Window: 38 names on the calendar (17 amc 11-18, 21 bmo 11-19); the sweep confirmed 34 (BEEM, LQDT, WMG, BORR unconfirmed); 20 hunted by `hunt_priority` (cap 20); 0 searches unfinished. Shed on priority: WSM SBLK NTES HP BABA EVGN TEN PANW MANU UGI WMT NJR ROAD CCIF. Baselines for RRGB and MMS amended suspect -> unknown from company sources before scoring.

## Panel table

Members' own percentiles 0-100 with side (L/S), `*` = in that judge's own top 20%. Selected = all four present and panel_pct >= 80. Expected return is the translation of the percentile (gross, scorebord window, flat at about +0.3% below 50), not a separate forecast.

| rank | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RRGB | amc | **yes** | 88 | long | 4 | 84L* | 88L* | 85L* | 96L* | 4 | +1.51 | -0.60 | +3.83% [+1.72, +5.80] | 0.67 | 1.00 | 1.25 |
| 2 | ARBE | bmo | **yes** | 85 | short | 10 | 70S | 82S* | 96S* | 94S* | 3 | -1.57 | -1.80 | +3.35% [+1.25, +5.36] | 0.65 | 1.00 | 0.75 |
| 3 | MMS | bmo |  | 78 | short | 4 | 84S* | 75S | 78S* | 75S | 2 | -1.17 | -1.20 | +2.37% [+0.52, +4.26] | 0.59 | 0.00 | 0.00 |
| 4 | SNEX | amc |  | 78 | long | 5 | 71L | 80L* | 84L* | 75L | 2 | +1.20 | +1.20 | +2.31% [+0.50, +4.19] | 0.58 | 0.00 | 0.00 |
| 5 | EVAX | bmo |  | 75 | short | 9 | 79S | 62S | 85S* | 75S | 1 | -1.24 | -1.50 | +2.02% [+0.38, +3.84] | 0.57 | 0.00 | 0.00 |
| 6 | PDD | bmo |  | 64 | short | 11 | 44S | 74S | 67S | 68S | 0 | -0.95 | -2.20 | +1.07% [-0.01, +2.63] | 0.56 | 0.00 | 0.00 |
| 7 | BBWI | bmo |  | 56 | long | 7 | 58L | 52L | 67L | 48L | 0 | +0.76 | +1.20 | +0.50% [-0.24, +1.99] | 0.56 | 0.00 | 0.00 |
| 8 | WWD | amc |  | 50 | short | 9 | 52S | 42S | 64S | 42S | 0 | -0.69 | -0.50 | +0.30% [-0.42, +1.46] | 0.56 | 0.00 | 0.00 |
| 9 | FUTU | bmo |  | 48 | long | 6 | 52L | 38L | 52L | 48L | 0 | +0.63 | +1.10 | +0.29% [-0.45, +1.30] | 0.56 | 0.00 | 0.00 |
| 10 | JOYY | amc |  | 47 | long | 6 | 41L | 46L | 57L | 42L | 0 | +0.59 | +1.10 | +0.29% [-0.46, +1.22] | 0.56 | 0.00 | 0.00 |
| 11 | CPA | amc |  | 39 | short | 5 | 42S | 30S | 42S | 42S | 0 | -0.53 | +0.00 | +0.29% [-0.52, +0.91] | 0.56 | 0.00 | 0.00 |
| 12 | MAGN | bmo |  | 31 | short | 20 | 0 | 42S | 52S | 30S | 0 | -0.49 | -1.50 | +0.29% [-0.56, +0.86] | 0.56 | 0.00 | 0.00 |
| 13 | VVV | bmo |  | 28 | short | 8 | 24S | 22S | 24S | 42S | 0 | -0.33 | +0.20 | +0.29% [-0.57, +0.85] | 0.56 | 0.00 | 0.00 |
| 14 | DAO | bmo |  | 26 | short | 10 | 41S | 14S | 28S | 24S | 0 | -0.35 | -1.00 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 15 | P | amc |  | 22 | long | 38 | 42S | 34L | 38L | 58L | 0 | +0.42 | +1.40 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 16 | UTI | amc |  | 22 | short | 37 | 33L | 30S | 72S | 18S | 0 | -0.34 | +0.90 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 17 | RERE | bmo |  | 14 | long | 20 | 20S | 33L | 24L | 20L | 0 | +0.31 | +0.80 | +0.29% [-0.66, +0.81] | 0.56 | 0.00 | 0.00 |
| 18 | KLIC | amc |  | 11 | long | 32 | 15S | 9L | 64L | 12S | 0 | -0.04 | +0.30 | +0.29% [-0.68, +0.80] | 0.56 | 0.00 | 0.00 |
| 19 | YMM | bmo |  | 9 | short | 8 | 20S | 4S | 0 | 14S | 0 | -0.17 | -0.60 | +0.29% [-0.69, +0.80] | 0.56 | 0.00 | 0.00 |
| 20 | PCYO | amc |  | 1 | long | 2 | 2S | 2L | 4L | 0 | 0 | +0.02 | +0.30 | +0.29% [-0.76, +0.78] | 0.56 | 0.00 | 0.00 |

## Selected names

**RRGB (Red Robin), long, panel_pct 88, all four judges in their own top 20%.** The full Q3 release was moved by the company from Nov 4 to tonight (call 16:30 ET; https://finviz.com/news/413576/red-robin-announces-preliminary-third-quarter-comparable-restaurant-revenue-reschedules-earnings-call-to-november-18-2026). The judges' notes rest on: the October refinancing (replacing $167.2M at 11.5% with a $90M term loan at SOFR+325, about $12M a year less interest by the searcher's arithmetic, unmodelled while two EPS estimates disagree by about 20%); the pre-released +3.9% comp with unseen flow-through; 9.5% short at 7.1 days to cover; prior full prints bought hard. **Strongest case against:** the FY EBITDA guide must come down mechanically for 108 refranchised restaurants with no sourced new range; peers say Q4 started soft and traffic slipped to -1.7%; record beef costs; the NT 10-Q and delay carry one-offs of unknown size. The searcher's own findings summed to -0.60, the opposite sign to the panel.

**ARBE (Arbe Robotics), short, panel_pct 85, three of four in their own top 20% (Opus 5 at 70).** The reaffirmed FY26 $4-6M revenue guide needs H2 of $2.8-4.8M against H1 $1.2M, a June-30 backlog of $1.0M and a HiRain production start pushed to early 2027; last year's Q3 release cut the guide and the stock fell 10.3% (https://www.prnewswire.com/il/news-releases/arbe-announces-second-quarter-2026-financial-results-302844826.html). **Strongest case against:** analyst FY already sits at the guide's low end (~$4.15M), the stock is 7% off its 52-week low and near net cash after the September raise, and short interest is 8.7% of shares at 14 days to cover, so any held guide or escrow news meets a crowded short.

## Where the panel and the searcher disagree most

- RRGB: searcher -0.60, panel 88 long. The judges weight the refinancing and short base over the guide-reset risk.
- UTI: searcher +0.90, panel 22 short with the widest spread (sd 37): Opus 5 long, Sonnet 5.5 strongly short.
- P (Everpure): searcher +1.40 (the day's top key), panel only 22 long with sd 38; Opus 5 short.
- MMS: searcher -1.20, panel 78 short (just below selection); Opus 5 in its own top 20% on the Leidos VA read-through.

## Stage E comparison

Stage E's `edge-scores.json` does not exist for today (its Routine is stopped), so there is no overlap or Spearman ρ to report.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names); it is not a forecast to size on. The weight columns are research. `p_up` is recorded and decides nothing. No searcher name clears the 2.8 conviction floor on `impact_sum`. V2 grounded is in `edge-scores-grounded.json`, written before the first print.

## Not ranked

BABA BEEM BORR CCIF EVGN HP LQDT MANU NJR NTES PANW ROAD SBLK TEN UGI WMG WMT WSM: no hunt (unconfirmed or shed on priority).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
