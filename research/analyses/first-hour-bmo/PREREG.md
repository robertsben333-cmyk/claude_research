# First-hour indicators on strong bmo calls: arguments and pre-registration

*Written 2026-11-05 ~17:15 UTC, before any outcome was fetched or looked at. Thread "Test first-hour indicators on strong bmo calls" (Xavier). Research only, no orders.*

## The question

A bmo name is bought or shorted at 13:30 ET the day before its report and sold at 13:00 ET on the report day. By 10:30 ET on the report day the first hour of regular trading is known. Can what the first hour looks like tell us whether the move keeps going our way after 10:30, so that we either (a) get out at 10:30 when the hour says the trend is against us, or (b) hold past 13:00 to the close when the hour says the trend is with us?

All indicators are oriented on the position's side `s` (+1 long, −1 short), so "positive" always means "good for us".

## Theoretical arguments, indicator by indicator

**1. First-hour return (open → 10:30) on our side: intraday momentum.** Gao, Han, Li and Zhou (2018) find the first half-hour return predicts the last half-hour return, driven by informed traders and by late-trading investors who rebalance in the same direction. On an earnings day the information is company-specific and large, and institutions that need days to build a position spread their orders over the session, so a first hour that already moves our way should keep moving. *Why it may fail:* the evidence is strongest at index level; for single names the post-open fade we measured on 28 Oct (gaps give back about 0.65 by 10:00, then recover) is a reversal, not a continuation.

**2. Opening range breakout (first 30 minutes).** The 09:30–10:00 high and low are where the opening auction's disagreement is settled. A price at 10:30 beyond the range on our side means the side that lost the opening argument has given up; "stocks in play" on news are where ORB rules have historically worked (Zarattini, Barbon and Aziz 2024 on stocks with high relative volume). *Why it may fail:* a range break at 10:30 is largely the same information as indicator 1.

**3. Price versus session VWAP at 10:30.** VWAP is the benchmark most institutional execution is measured against. If price is above VWAP, the average buyer since the open is in profit and VWAP-benchmarked buy programmes keep paying up; below VWAP, sellers are in control. It is the "who is winning the day so far" measure weighted by size, not by time, so it can disagree with indicator 1 when the move came on thin volume.

**4. Gap retention and gap fill.** A bmo report is mostly priced in the pre-market, so the opening gap is the market's first verdict. If the gap has held through the first hour (less than half given back), the verdict stands and post-earnings drift (Bernard and Thomas 1989; drift is front-loaded) should continue it. A gap that has filled completely by 10:30 means the market rejected the overnight read and the move is now going the other way. Oriented on our side: a gap with us that holds is good, a gap against us that holds is bad, a gap against us that fills is good.

**5. Relative volume in the first hour (vs the same hour over the previous 20 sessions).** High volume says the move is carried by real participation rather than a thin quote; high-volume price moves tend to persist (Llorente et al. 2002 for informed trading; Gervais, Kaniel and Mingelgrin 2001 for the high-volume premium). So relative volume should not have a direction of its own but should *amplify* indicator 1: a first-hour move our way on heavy volume continues more than the same move on light volume. *Why it may fail:* heavy volume can also be capitulation, the end of a move.

**6. Where 10:30 sits in the first-hour range (close location).** A price at the top of the first-hour range (on our side) means buyers were still in control at the end of the hour; at the bottom, the hour ended in selling. It is a cheap measure of the last part of the hour, which is the most recent information.

**What argues against all of them.** For bmo names most of the information is absorbed between 08:00 and 09:30. What is left after 10:30 may be noise, and our own earlier work found nothing in the first minute and only a short-lived fade in the first half hour. Indicators 1, 2, 3 and 6 are strongly correlated; they mostly measure one thing ("the first hour went our way"), so finding one of them "significant" among six is likely luck.

## Pre-registered tests

**Decision moment:** 10:30 ET on the report day (the close of the 10:29 one-minute bar).

**Outcomes:**
- **R1** = s × (price 13:00 / price 10:30 − 1), in %. Is it worth holding from 10:30 to the current exit?
- **R2** = s × (close / price 10:30 − 1). Is it worth holding to the close?
- **R3** = s × (close / price 13:00 − 1). Is it worth holding past the current exit?

**Indicators at 10:30** (all oriented by s):
- `fh_ret` = s × (P10:30 / open − 1)
- `orb` = +1 if P10:30 beyond the 09:30–10:00 range on our side, −1 beyond it on the other side, 0 inside
- `vwap` = s × (P10:30 / VWAP 09:30–10:30 − 1)
- `gap_state` = +1 gap with us and ≥50% retained, or gap against us and fully filled; −1 gap against us and ≥50% retained, or gap with us fully filled; 0 otherwise (only gaps ≥1%)
- `rvol` = first-hour volume / mean first-hour volume of the previous 20 sessions; tested as `fh_ret` split at the median of `rvol`
- `clv` = position of P10:30 in the 09:30–10:30 high–low range, 0 to 1, oriented so 1 = our side
- **`trend` (the primary composite)** = sign(fh_ret) + orb + sign(vwap) + (2·clv − 1 rounded to −1/0/+1), range −4…+4

**Primary hypothesis (one test, no correction):** `trend` ranks R1 positively on strong bmo calls. Spearman ρ, permutation p within day. Also reported: the decision rule *"exit at 10:30 if trend ≤ −2, else hold to 13:00"* against always holding to 13:00 (per call difference, t, and per-day t), and *"hold to the close if trend ≥ +2, else exit 13:00"* against 13:00 (R3).

**Secondary hypotheses (six, Bonferroni, so p < 0.0083 to count):** each of `fh_ret`, `orb`, `vwap`, `gap_state`, `clv` ranks R1 positively; `fh_ret` ranks R1 more strongly in the high-`rvol` half than in the low half. Same for R2 and R3 reported descriptively.

**Samples, tested separately and never pooled for a verdict:**
1. **Strong bmo calls** (the target): stage E-P, `panel_pct` ≥ 80 with all four judges, session bmo, per prompt version (`us-panel.v2`, `us-panel.v3`), plus the Aug–Sep blind backtest's ≥80 bmo names (`research/analyses/panel-mean-pct/`). Expected about 15 (v2), about 7 (v3) and a handful (backtest): **far too small to confirm anything on its own.** Reported for direction only.
2. **All panel-scored bmo calls**, per prompt version (about 96 v2, 42 v3), on the panel's side. Tests whether the indicators work on our kind of names.
3. **All bmo earnings events in the repo's universe files** with an opening gap ≥ 2%, position on the gap's side. Tests whether the mechanism exists at all. Biggest n, and the only tier that can reject an indicator.

**Verdict rule:** an indicator counts as a signal only if it has the predicted sign in tier 3 at the corrected threshold **and** the predicted sign in tier 2. Nothing in tier 1 can establish a result; it can only show whether strong calls look different.

**Data:** Alpaca SIP one-minute bars (split-adjusted) for the report day, 30-minute bars for the previous 20 sessions (relative volume), previous regular close from the 15:59 bar of the prior session. Prices, not fills; no costs.

**What I will not do:** change thresholds, the decision time or the composite after seeing outcomes. Anything found that way is reported as in-sample and labelled so.
