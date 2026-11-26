# Stage E-P — 2026-11-26 window (11-26 amc + 11-27 bmo)

**This is stage E-P: an Opus 5.5 searcher, a blind four-model panel, and the stage that trades the Alpaca live and paper accounts.**
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), with no fallback.
One name on a holiday is an anecdote, not a result.

**Nothing is selected and nothing can be bought today.** 2026-11-26 is Thanksgiving and the US market is closed, so step 6b's `open` refuses. Friday 11-27 is a half session closing at 13:00 ET.

## Panel table

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | P(right) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | XYF | bmo | no | 39 | short | 17 | 49 S | 11 S | 56 S | 38 S | 0 | -0.59 | -0.40 | +0.29% [-0.52, +0.91] | 0.56 |

The expected return translates the percentile. Every name at the same `panel_pct` gets the same number. It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. No judge put XYF in its own top 20%.

`weight_equal` and `weight_precision_tilt` do not apply because nothing was selected.

## Why the panel sat out

- **The stock trades on a take-private bid, not on the quarter.** On 2026-11-06 the controlling holder (about 93.45% of the votes) proposed US$6.03 per ADS. Spot was US$5.25 on 11-25, 12.9% below the offer. On 11-25 peer QFIN fell about 7.6% on its print while XYF rose 0.38% (searcher's sources in `hunts/XYF.json`).
- **Peer read-through is the only negative.** QFIN, FinVolution and LexinFintech all reported or guided weak Q3 volumes and profits after XYF last spoke on 08-24. This points to a Q3 below Q2's run-rate (RMB993.6m revenue, RMB47.0m net income). All four judges leaned short on it and kept the size small, because:
  - it is a proxy, not an XYF number;
  - no source gives a bar: there is no consensus and no guide;
  - the deal spread damps any move.
- **The case against short:** credit quality is improving (delinquency rates fell quarter on quarter), and the release could carry a line on progress toward the deal.

## Searcher against panel

The searcher (-0.40, p40 of its own reference) and the panel (39, short) agree on the sign and on there being no edge. Opus 5.5 was the mildest judge (11th percentile).

## Stage E

There was no comparison with stage E. Its Routine is stopped and `<RUN>/edge/` does not exist.

## Not hunted

The thin-day check (`--include-unknown` plus `session_resolve.py`) covered 25 rows with no session:
- EDGAR killed 3;
- 22 were carried;
- the company's own press release confirmed none.

They were not hunted. Most are amc rows dated on a day the market is closed.

## What the numbers are not

`expected_return_pct` is what names at this percentile have earned in the past. Its out-of-sample record is weak (correlation +0.12 over 148 names), so it is not a forecast to size on. `p_up` is recorded and decides nothing.

---
This is a forecasting exercise over public information, not investment advice.
