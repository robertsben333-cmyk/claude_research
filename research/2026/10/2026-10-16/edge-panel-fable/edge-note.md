# Stage E-PF — 2026-10-16 amc + 2026-10-19 bmo

**This is stage E-PF: Fable 5.1 searchers, the same blind four-model panel as stage E-P, no orders.**
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), no fallback. Scored `--dry-run --stage E-PF`: stage E-P's panel history was not written.
Three names on one day is an anecdote. Judge this stage only pooled, against stage E-P on the same days.

Window: no amc names tonight; three bmo names on Monday 2026-10-19, all confirmed by company sources (sweep 3 of 3, 0 phantoms). Thin-day check: 20 `time-not-supplied` rows, `session_resolve.py` killed 5, carried 15, confirmed 0 by press release, so they were withheld.

## The panel

| # | ticker | session | selected | panel_pct | side | spread | Opus 5 | Opus 5.5 | Sonnet 5.5 | Fable 5.1 | k | panel_score | searcher impact_sum | E[return] at this pct (80% band) | P(right) | w_equal | w_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CLF | bmo | **yes** | 92 | long | 2 | 94L* | 93L* | 92L* | 90L* | 4 | +2.22 | +0.80 | +4.42% [+2.38, +6.27] | 0.70 | 1.0 | 1.0 |
| 2 | FITB | bmo | no | 39 | short | 18 | 68S | 38S | 25S | 23S | 0 | -0.33 | -1.00 | +0.29% [-0.52, +0.91] | 0.56 | 0 | 0 |
| 3 | DX | bmo | no | 4 | long | 19 | 29S | 19L | 18L | 7L | 0 | +0.17 | +0.20 | +0.29% [-0.74, +0.78] | 0.56 | 0 | 0 |

Percentiles are each judge's own, 0-100, against that judge's live sizes from E-P runs before today (n=73 each); `*` = in its own top 20%. The expected return is the translation of the percentile: what names at that `panel_pct` have earned on the panel's side, gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50.

## The selected name: CLF (long, 4 of 4 in their own top 20%)

Evidence the judges named: US hot-rolled coil spot ran from the ~$1,150/t the July call assumed to $1,230/st (Nucor CSP, 2026-10-05, https://gmk.center/en/news/nucor-has-raised-the-price-of-hot-rolled-coils-to-1-230-per-tonne/amp/), both EAF peers guided higher Q3 selling prices (Steel Dynamics 8-K 2026-09-17, https://www.sec.gov/Archives/edgar/data/0001022671/000110465926108777/tm2625690d1_ex99-1.htm), and the company itself said Q4 EBITDA would "even further exceed" the ~$575M Q3 guide. This name trades on the forward guide (+15.98% 2026-07-23, +21.47% 2025-10-20, −16.43% 2026-02-09). Short interest 13.8% of shares (Equibles, 2026-09-30 settlement).

Strongest case against: the option market already pays for upside (25-delta skew −12.5 vol points), Wells Fargo upgraded on the same logic on 10-06; both EAF peers missed their own consensus on costs; Stelco's Hamilton idling (BNN Bloomberg 2026-10-13) with an unquantified charge and an Ottawa legal threat. The implied move is 10.5%, so a wrong sign costs as much as a right one pays.

## Panel against searcher

- CLF: the searcher sized +0.80 (below the 2.8 floor); all four judges put it in their own top 20%. Largest disagreement of the day, in scale not sign.
- FITB: searcher −1.00, panel 39 short; Opus 5 alone near its top third (68S).
- DX: searcher +0.20, panel splits on side (Opus 5 short, three long), mean 4.

## Comparison with stages E and E-P

- Stage E (`<RUN>/edge/edge-scores.json`): not on `main` at 17:29 UTC, so no comparison line.
- Stage E-P (`<RUN>/edge-panel/edge-scores-panel.json`): present by 17:33 UTC. Both ranked CLF, DX, FITB. Selected sets identical: CLF only in both (E-P 94.5 long, E-PF 92.5 long). Spearman ρ between the two `panel_pct_signed` columns +0.50 on 3 names (E-P: CLF +94.5, FITB +15.4, DX −23.3; E-PF: CLF +92.5, DX +3.8, FITB −38.7). The two searchers disagree on the side of FITB and DX, both below any selection line. Three names: an anecdote.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on these.
- CLF: retail tilt 68 (≥50), search spike failed (Trends unreachable), 20d vol 57% (<58).
- DX: retail 57 (≥50), search failed, vol 24%.
- FITB: retail 25, search failed, vol 16%.

## What the numbers are not

`expected_return_pct` is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 over 148 names), not a forecast to size on. The weights are research; nothing trades them. `p_up` is recorded and decides nothing. V2 grounded (CLF +2.29, DX −0.17, FITB −0.29) was written before the first print. Caveats: the `fable51` judge read evidence collected by its own model family (recorded, not corrected for); nothing checks a finding for being factually wrong; the key's reproducibility is unmeasured.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
