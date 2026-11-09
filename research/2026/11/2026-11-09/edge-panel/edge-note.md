# Stage E-P — 2026-11-09 amc + 2026-11-10 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel; the panel's book is traded on the Alpaca PAPER account (step 6b).** All four members ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), one part, no fallback, no retry; each covered 20 of 20 packs. One day is an anecdote.

Universe 168 names (119 amc 11-09, 49 bmo 11-10); the sweep checked 28, confirmed 22, left 6 unconfirmed (ONTO ZETA SE HRB JBS WIX) and 140 unchecked, found no phantoms. 20 hunted (cap): TDG and VOD shed as the lowest-priority confirmed names. All 20 rankable; no search was cut off (hunt_status: 0 unfinished of 20). PLUG's baseline was amended `suspect` -> `unknown` before any searcher (the cadence matcher took the 15 Oct preliminary 8-K as a print). OXY's sealed baseline is `bars_failed` (missed before its searcher ran; not re-sealed after, see run log), so its scale comes from the searcher's OptionSlam figure.

## The panel

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | QBTS | bmo | yes | 90 | short | 5 | 90S* | 92S* | 82S* | 96S* | 4 | -1.74 | -1.60 | +4.11% [+2.02, +6.06] | 0.69 | 1.00 | 1.00 |
| 2 | ASTS | amc | yes | 88 | short | 2 | 91S* | 89S* | 88S* | 85S* | 4 | -1.54 | -2.00 | +3.86% [+1.76, +5.82] | 0.67 | 1.00 | 1.25 |
| 3 | HSAI | bmo | yes | 81 | short | 12 | 88S* | 72S | 67S | 96S* | 2 | -1.32 | -2.20 | +2.73% [+0.72, +4.68] | 0.61 | 1.00 | 0.75 |
| 4 | SRRK | bmo |  | 77 | long | 5 | 72L | 75L | 76L | 85L* | 1 | +1.14 | +2.30 | +2.27% [+0.48, +4.15] | 0.58 | 0.00 | 0.00 |
| 5 | LCID | amc |  | 69 | short | 23 | 31S | 82S* | 92S* | 71S | 2 | -1.22 | -0.60 | +1.49% [+0.19, +3.16] | 0.56 | 0.00 | 0.00 |
| 6 | LQDA | bmo |  | 67 | short | 7 | 72S | 56S | 73S | 68S | 0 | -1.01 | +0.50 | +1.34% [+0.12, +2.97] | 0.56 | 0.00 | 0.00 |
| 7 | PLUG | amc |  | 66 | short | 7 | 56S | 68S | 68S | 74S | 0 | -0.91 | -1.60 | +1.29% [+0.09, +2.90] | 0.56 | 0.00 | 0.00 |
| 8 | SANM | amc |  | 66 | long | 20 | 56L | 74L | 40L | 92L* | 1 | +0.95 | +1.00 | +1.22% [+0.06, +2.82] | 0.56 | 0.00 | 0.00 |
| 9 | VG | bmo |  | 66 | long | 6 | 62L | 76L | 64L | 61L | 0 | +0.89 | +1.80 | +1.22% [+0.06, +2.82] | 0.56 | 0.00 | 0.00 |
| 10 | HIMS | amc |  | 61 | short | 14 | 71S | 58S | 40S | 76S | 0 | -0.89 | +0.60 | +0.91% [-0.09, +2.40] | 0.56 | 0.00 | 0.00 |
| 11 | ACHR | amc |  | 58 | short | 16 | 48S | 38S | 76S | 71S | 0 | -0.87 | -0.40 | +0.68% [-0.18, +2.15] | 0.56 | 0.00 | 0.00 |
| 12 | LEGN | bmo |  | 55 | short | 8 | 70S | 50S | 50S | 52S | 0 | -0.67 | -1.50 | +0.40% [-0.28, +1.89] | 0.56 | 0.00 | 0.00 |
| 13 | QLYS | amc |  | 48 | long | 23 | 61L | 56L | 9L | 68L | 0 | +0.77 | +1.10 | +0.29% [-0.44, +1.34] | 0.56 | 0.00 | 0.00 |
| 14 | TTWO | amc |  | 42 | short | 20 | 70S | 24S | 22S | 52S | 0 | -0.52 | +0.10 | +0.29% [-0.50, +0.99] | 0.56 | 0.00 | 0.00 |
| 15 | TTD | amc |  | 33 | short | 44 | 64S | 36L | 77S | 25S | 0 | -0.66 | +2.00 | +0.29% [-0.55, +0.86] | 0.56 | 0.00 | 0.00 |
| 16 | BAP | amc |  | 29 | short | 12 | 42S | 18S | 16S | 40S | 0 | -0.40 | -0.20 | +0.29% [-0.56, +0.85] | 0.56 | 0.00 | 0.00 |
| 17 | SKYD | amc |  | 24 | long | 8 | 14L | 30L | 16L | 34L | 0 | +0.31 | +0.70 | +0.29% [-0.58, +0.83] | 0.56 | 0.00 | 0.00 |
| 18 | OXY | amc |  | 22 | long | 8 | 16L | 36L | 22L | 16L | 0 | +0.27 | +0.45 | +0.29% [-0.58, +0.83] | 0.56 | 0.00 | 0.00 |
| 19 | RKLB | amc |  | 22 | short | 17 | 49S | 8S | 8S | 22S | 0 | -0.23 | -0.10 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 20 | ONON | bmo |  | 12 | short | 17 | 8L | 8S | 8S | 40S | 0 | -0.12 | -0.60 | +0.29% [-0.67, +0.80] | 0.56 | 0.00 | 0.00 |
Percentiles are each judge's own: the share of that judge's live sizes from runs before today with a smaller |impact_sum| (`*` = in its own top 20%). The expected return is the translation of the percentile, what names at that `panel_pct` have earned on the panel's side, gross, on the scorebord's window, flat at about +0.3% below a percentile of 50; it is not a separate forecast.

## Selected names

**QBTS, short, panel_pct 90 (4 of 4 in their own top 20%).** Every judge rests on the same two documents: on the 6 Aug Q2 call the CFO said both 2026 annealing systems ship in Q4 with "carryover revenue … into 2027" and system revenue recognised over about two quarters, and the 10-Q puts only 57% of the $40.7m RPO inside 12 months; the Street's Q4 (~$32.2m) and FY (~$42.5m) have not moved since June. Q3 was guided "up modestly" from $3.08m against a $4.0–4.4m consensus, no Q3 system or QCaaS booking was announced, and a ~17% IonQ-sympathy run-up on 6 Nov raised the bar. **Case against:** 79m shares short (~21%, 5 days to cover and rising) is a squeeze into any clean booking headline; the put skew (+7.6) already pays the downside; the "Street not reset" claim rests on aggregator snapshots, not a named analyst.

**ASTS, short, panel_pct 88 (4 of 4).** No BlueBird has launched since 5 Aug (BlueBirds 14–16 at the Cape since ~10 Oct, no date), and the 6 Nov 8-K reframes external launches as "over 100 satellites… between 2027 and 2028", which puts the ~45-in-orbit-by-early-2027 target at risk; the FY26 $150–200m revenue guide needs a Q4 about 34% above the record quarter; the Blacklift rocket commitment (> $1.3bn, $400m cash plus 10–14m shares) reaches the capex and cash guide on this call; the stock gapped ~15% on the Rakuten JV into the entry. **Case against:** 22–24% of float short; the stock is −28% over 20 days and 72% off its high; a firm launch date or a government award on the call is real upside; the convert risk is a pattern, not a filing.

**HSAI, short, panel_pct 81 (2 of 4; Opus 5.5 at 72, Sonnet 5.5 at 67).** Subtracting Gasgoo's Jan–Jul from its Jan–Aug China lidar table gives Hesai 126,767 units in August (25.3% share against 33.7% year to date), leaving a large September needed for the 800–850k Q3 unit guide; the FY 3–3.5M unit target needs a Q4 of at least 1.05M, so a guide cut is the risk; margin fell from 42.2% to 39.7% and RoboSense blamed raw materials. **Case against:** the only consensus found sits below the guide floor, so even a low-end print reads as a beat; skew −3.6 pays the upside; the August arithmetic is the searcher's inference from two vendor tables, and the two judges outside their top 20% are the two that weight that inference least. Weakest of the three by spread (sd 12).

## Where panel and searcher disagree most

- **LCID**: searcher −0.6, panel 69 short with the day's widest spread (sd 23): Opus 5 at 31 (the extreme put skew and 64% short already pay the bear case), Sonnet 5.5 at 92.
- **SANM**: searcher +1.0, panel 66 long, Fable 5.1 at 92 (AMD's same-quarter guide), Sonnet 5.5 at 40.
- **QLYS**: searcher +1.1, panel 48 long; Sonnet 5.5 near zero (9).
- **TTD**: searcher +2.0 (the day's largest positive sum), panel 33 short with members on both sides (sd 44): the scaled number was near zero because the run-up bought the read-through.

## Stage E comparison

Stage E's `edge/` does not exist for this date (its Routine is stopped), so there is no overlap or Spearman ρ to report.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names); it is not a forecast to size on. The weights in the table are research; the book uses `execution.panel` (panel_pct − 60, 50% cap). Certainty (`p_up`) is recorded and decides nothing. Nothing checked the findings for factual error (no adversary pass), and the key is not reproducible to better than its own size. Sign balance of the searcher: 10 positive, 10 negative; of the panel: 6 long, 14 short. No searcher `impact_sum` clears the 2.8 floor today (largest |sum| HSAI −2.2, TTD +2.0, ASTS −2.0). All three selected names are shorts on crowded books (QBTS ~21%, ASTS ~23%, HSAI ~5% short), which is the correlated risk of the day.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
