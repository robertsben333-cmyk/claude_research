# Pre-registration: a multi-factor model for exiting earlier or later (US, amc and bmo)

Written 2026-11-07 22:55 UTC, before any price for this study was fetched. Thread "Model eerdere of latere US exit". Nothing below is changed after the outcomes are computed; anything added later is labelled exploratory.

## Question

Our default exit is: amc names at the next open, bmo names at 13:00 ET on the report day. Can a model built on theory, using only information available at the decision moment, tell us per name whether to exit earlier or later than that?

Earlier work in this project tested single indicators and they failed or faded out of sample (first minute, first hour, implied-move rule, pre-market volume, "winning at the open"). This study tests a combined model whose signs are fixed by theory, not by our data.

## Data

- Events: every amc and bmo earnings event in the repo's universe files (`research/*/edge*/universe.json`), 2,677 events, reaction days 31 Aug to 6 Nov 2026. Reaction day = event day for bmo, the next trading day for amc.
- Prices: Alpaca SIP 1-minute bars 04:00 to 16:00 ET on the reaction day, daily bars for the 45 sessions before, SPY the same.
- Market-wide sample: events with |gap at the open| ≥ 2% and a usable open, 13:00 and close.
- Our calls: stage E-P (`us-panel.v2` and `us-panel.v3`, never pooled), strong = panel ≥80 with four judges; the Aug-Sep backtest names kept apart.
- Stage M: the morning advice and review files (`research/*/morning/`), analyst prompt v2 from 21 Oct.

## Training and holdout

- **Training: reaction days 31 Aug to 20 Oct 2026.** Standardisation, the fitted model and thresholds come from here only.
- **Holdout: reaction days 21 Oct to 6 Nov 2026.** All verdicts are read here. (Some earlier single-factor checks in this project touched part of this period; the combined model and its signs have never been run on it.)

## Outcomes (all in % of the prior close)

g = sign of the gap at the open (open vs prior regular close). a = position side × g (+1 when our position is on the gap side).

- **Y1 (primary): open to 13:00 in the gap's direction**, g × (P13:00 − Popen) / Pprev. For amc, a × Y1 is the gain from holding to 13:00 instead of selling at the open. For bmo, −a × Y1 is the gain from selling at the open instead of 13:00.
- Y2: open to 10:00, gap side.
- Y3: 13:00 to the close, gap side (holding bmo later than 13:00).
- Y0 (amc only, earlier than the open): pre-market reference (median of the last five 1-minute bars before 09:30) to the open, in the pre-market gap's direction.

## Factors (known at 09:30, after the opening print) and the sign theory gives them

Positive sign = predicts continuation in the gap's direction after the open.

| # | Factor | Definition | Sign | Theory |
|---|---|---|---|---|
| F1 | Gap vs expected move | \|gap\| / option-implied event move (missing → neutral) | − | Overreaction to large surprises; option traders over-price post-earnings vol (Goyal & Saretto); large gaps carry more liquidity-driven price pressure |
| F2 | Competing announcements | log(1 + events reacting the same day) | + | Limited attention: more same-day announcements → slower reaction, more drift (Hirshleifer, Lim & Teoh 2009) |
| F3 | Pre-market attention | log(pre-market dollar volume / 20-day average daily dollar volume) | − | Attention-driven retail buying at the open pushes the opening price too far, then it reverses intraday (Berkman, Koch, Tuttle & Zhang 2012) |
| F4 | Size / liquidity | log 20-day average daily dollar volume | + | Liquidity-driven reversals are larger where market-making capacity is small (So & Wang 2014; Dai, Medhat, Novy-Marx & Rizova) |
| F5 | Run-up into the print | g × 20-session return to the prior close | − | Short-term reversal; a gap in the direction of a run-up is the more extended one |
| F6 | Opening overshoot | g × (open − pre-market reference) / Pprev | − | Opening-auction pressure from market orders at the open (Berkman et al.); pre-market price is the less noisy anchor (Barclay & Hendershott 2003) |
| F7 | Late pre-market drift | g × (pre-market reference − price at 08:00) / Pprev | + | Gradual information diffusion / late-informed traders (Gao, Han, Li & Zhou 2018; Hong & Stein) |
| F8 | Down gap | 1 if g < 0 | + | Bad news travels slowly; short-sale constraints slow the downside (Hong, Lim & Stein 2000) |
| F9 | bmo | 1 if bmo | + | A bmo print has had two thin pre-market hours, an amc print a full night, so less is priced at the open |
| F10 | Volatility | 20-day realised daily volatility | − | Inventory risk raises the liquidity premium, so more reversal (Dai et al.; So & Wang) |

Each factor is z-scored on the training sample (winsorised at ±3, missing → 0).

## Models

- **M-A (primary), theory composite:** sum of sign × z over F1–F10. No fitting.
- **M-B, constrained regression:** OLS of Y1 on the ten z-scores on the training sample; any factor whose coefficient has the wrong sign is dropped and the model refit once. Applied unchanged to the holdout.

## Stage M add-on (our calls with a stage M review only)

Signed so that positive = the position gains after the open (should hold longer):

| | Signal | Sign | Theory |
|---|---|---|---|
| S1 | side × analyst's expected open-to-close move | + | Analyst reads fundamentals the price has not absorbed |
| S2 | −a × (p_fade_by_1000 − 50) | + | Analyst's own fade forecast |
| S3 | side × (release read − pre-market reference) | + | Underreaction: a fundamental read beyond the price leaves room (an earlier 36-name check found the opposite sign; tested as stated) |
| S4 | side × verdict_vs_bar / 100 + side × guidance (raised +1, cut −1) + a × tape_read (undershoot +1, overshoot −1) | + | Hard surprise and guidance drive drift (PEAD); the analyst's over/undershoot read |

S = mean of the z-scored S1–S4 (z on all stage M v2 names, since stage M has no training period). Too few names to fit anything, so nothing is fitted.

## Tests and verdict rules

1. **Market-wide, holdout:** Spearman ρ of M-A with Y1, within-day permutation p (one-sided, predicted positive). **M-A passes if ρ > 0 at p < 0.05.** Same for M-B, Y2, Y3 and (amc) Y0 as secondary, Bonferroni over the four secondary rows.
2. **Rule on our calls, holdout, per version:** act only when |prediction| is above its training 67th percentile. amc: hold to 13:00 when a × pred > 0. bmo: sell at the open when a × pred < 0. Report gain vs the default per call and per day (n, mean, t, p). It counts only if the sign is positive on both v2 and v3, and the market-wide test passed.
3. **Stage M:** Spearman of S with a × Y1 (and with the gain from stage M's own advice). With roughly 70 names over 11 mornings this is reported as indicative only, and the report says so.
4. **Per-factor table** (training and holdout ρ for each factor, with the predicted sign) is descriptive, so we can see which theories hold.

Gross prices, not fills. Research, not investment advice.
