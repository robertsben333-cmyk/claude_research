# Pre-registration: earnings-day technical indicators on top of the E-P panel

Written 2026-11-15 16:20 UTC, before any indicator was computed or joined to an outcome.

## Question
Do technical indicators that practitioners and the literature propose around earnings add anything to
stage E-P's panel? Secondary: do they predict the raw move at all, market-wide, in our window?

## Samples (never pooled)
- **v3 (primary):** us-panel.v3, run days 2026-10-29 .. 2026-11-12, four judges, 218 names
  (rows from /mnt/project-files/quant-selection-score/rows.json; 13 Nov run excluded).
- **v2 (direction check):** us-panel.v2, run days 2026-10-14 .. 2026-10-28, 186 names.
- **Market-wide:** every name with an E-P baseline on those run days, priced on the same window,
  split into the v3 period and the v2 period.

Window (scorebord): entry 13:30 ET on the run day; amc exit at the next session's open; bmo exit 13:00 ET
on the report day. Gross. `ret` = return on the panel's side; `mv` = raw move.

## Indicators (all known before 13:30 ET on the run day) and hypothesised sign on the raw move
| # | Indicator | Source | Hypothesis on mv | Basis |
|---|---|---|---|---|
| D1 | 5-day run-up to prior close | daily bars | negative | So & Wang 2014, pre-EA reversal |
| D2 | 20-day run-up to prior close | daily bars | negative | repo's free control, reversal |
| D3 | RSI(14), daily, prior close | daily bars | negative | practitioner overbought/oversold |
| D4 | Close vs 50-day SMA, % | daily bars | positive | practitioner trend filter |
| D5 | Previous earnings reaction (last print move) | baseline history | positive | Bernard & Thomas 1989, PEAD/serial correlation of EA returns |
| D6 | 25-delta skew (put IV − call IV) | sealed baseline | negative | Xing, Zhang & Zhao 2010; Jin, Livnat & Zhang 2012 |
| D7 | Put/call open-interest ratio | sealed baseline | negative | Pan & Poteshman 2006 (volume; OI is our proxy) |
| D8 | Run-day return, prior close to 13:30 ET | 5-min bars | positive | informed pre-EA trading / intraday momentum |
| D9 | Price vs run-day VWAP at 13:30 ET, % | 5-min bars | positive | practitioner VWAP bias |
| D10 | Abnormal volume, 5 days to prior close vs prior 60 days (log) | daily bars | positive | Frazzini & Lamont 2007, EA premium/attention |
| D11 | Short interest, days to cover (latest settlement published by run day, settlement+11 cal. days) | Nasdaq | negative | Boehmer, Jones & Zhang 2008 |
| S1 | Implied move / median historical reaction | sealed baseline | negative on **ret** (panel does worse where options are rich) | practitioner "IV crush" |
| C  | Composite: mean of hypothesis-signed within-day ranks of D1..D11 (available ones) | | positive | one combined test |

## Tests
1. **Adds to the panel (primary):** within-day Spearman ρ of (side × hypothesis-signed indicator) with `ret`,
   p from 5,000 within-day shuffles. S1 is tested unsigned against `ret`.
   Also an OLS of `ret` on day-demeaned panel_pct and day-demeaned signed indicator rank, day-clustered t,
   to show it adds beyond pct.
2. **Stand-alone (secondary):** within-day Spearman ρ of hypothesis-signed indicator with `mv`, market-wide.

## Verdict rule
- **Adds:** v3 permutation p < 0.05 after Holm over the 12 tests (D1..D11, S1), same sign in v2 panel test,
  and same sign market-wide in the v3 period.
- **Lead:** same sign in v3, v2 and market-wide (v3 period) with v3 p < 0.10 unadjusted. Forward-test only.
- Otherwise nothing. The composite C is reported on the same rule without the Holm step.
- No live change in any case; this thread proposes, it does not switch.

## Already ruled out elsewhere (not redone)
First-minute and first-hour bars for exit timing, 1-min tape priced-in detector, 10-factor exit model,
judge disagreement, sealed expected move (sign flips v2/v3).

## Addendum, 2026-11-15 16:12 UTC (Xavier: "not just on panel_pct but also on entry/exit")
Written before any indicator was correlated with any outcome. Same indicators, same within-day permutation test,
same verdict rule (Holm over the 12 per leg), each leg tested separately:
- **Entry leg:** run-day 13:30 ET to the run-day close. Positive (on our side) means 13:30 beat a closing entry.
- **amc exit leg:** next-session open to its close. Positive means holding past the open would have paid.
- **bmo early leg:** report-day open to 13:00 ET. Positive means holding from the open to 13:00 paid.
- **bmo late leg:** report-day 13:00 ET to close. Positive means holding past 13:00 paid.
For the panel, legs are signed to the panel's side; market-wide, legs are raw and the indicator is
hypothesis-signed. These are a different question from the move itself, so the hypothesised sign is
**continuation** (same sign as the move hypothesis); a two-sided p is reported regardless.
