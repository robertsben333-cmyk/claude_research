# Stage E-P — 2026-11-23 amc + 2026-11-24 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel. The panel's book is placed on the live and paper Alpaca accounts at step 6b.**
All four members ran: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5, Fable 5.1, each on all 20 packs.
One day is an anecdote. Judge this stage only pooled.

**No name reached panel_pct 80, so nothing is selected.** Two names sit at 70-79: SYM 74 long and DKS 71 long. Under the no-strong-name top-up (`execution.panel.top_up`, since 2026-11-19), those two take the budget, equal weight, at most 33% of equity each. The script sizes it; see step 6b in the run log.

Universe 43 (18 amc, 25 bmo), 40 confirmed by the sweep (FLNC, KSS, BBY unconfirmed; CENTA folded into CENT), 20 hunted by `hunt_priority` (cap 20), 0 unfinished. Six wave-1 searchers (SYM, SMTC, CMP, TUYA, ZM, AMTM) hit the 200-per-turn WebSearch budget and were re-run to completion; the unfinished first attempts sit in `hunts/_unfinished/`.

## The panel

Member columns: each judge's own percentile 0-100 of its live range, L/S for its side, `*` where in its own top 20%. E[return] is what names at that panel_pct have earned on the panel's side: gross, on the scorebord's window, flat at about +0.3% below a percentile of 50. It is the translation of the percentile, not a separate forecast. The weights are research; nothing trades them.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SYM | amc 11-23 | no | 74 | long | 21 | 78L | 87L* | 38L | 91L* | 2 | +1.37 | +1.40 | +1.90% [+0.33, +3.69] | 0.56 | 0.0 | 0.0 |
| 2 | DKS | bmo 11-24 | no | 71 | long | 15 | 80L | 84L* | 46L | 74L | 1 | +1.18 | +0.80 | +1.62% [+0.24, +3.33] | 0.56 | 0.0 | 0.0 |
| 3 | MMED | bmo 11-24 | no | 68 | long | 7 | 56L | 74L | 74L | 68L | 0 | +1.01 | +1.70 | +1.39% [+0.14, +3.03] | 0.56 | 0.0 | 0.0 |
| 4 | HPE | amc 11-23 | no | 57 | long | 13 | 72L | 52L | 38L | 64L | 0 | +0.81 | +1.00 | +0.54% [-0.23, +2.02] | 0.56 | 0.0 | 0.0 |
| 5 | BURL | bmo 11-24 | no | 56 | short | 11 | 52S | 65S | 40S | 69S | 0 | -0.85 | -0.90 | +0.51% [-0.23, +2.00] | 0.56 | 0.0 | 0.0 |
| 6 | TIGR | bmo 11-24 | no | 50 | short | 10 | 35S | 62S | 56S | 48S | 0 | -0.64 | -1.30 | +0.29% [-0.42, +1.45] | 0.56 | 0.0 | 0.0 |
| 7 | CMP | amc 11-23 | no | 43 | short | 23 | 73S | 30S | 12S | 55S | 0 | -0.57 | -0.30 | +0.29% [-0.50, +1.02] | 0.56 | 0.0 | 0.0 |
| 8 | VALN | bmo 11-24 | no | 40 | short | 15 | 15S | 50S | 44S | 52S | 0 | -0.58 | -1.50 | +0.29% [-0.51, +0.94] | 0.56 | 0.0 | 0.0 |
| 9 | CENT | amc 11-23 | no | 40 | long | 17 | 24L | 46L | 64L | 23L | 0 | +0.48 | +0.50 | +0.29% [-0.52, +0.92] | 0.56 | 0.0 | 0.0 |
| 10 | ANF | bmo 11-24 | no | 38 | long | 47 | 39S | 82L* | 38L | 69L | 1 | +0.72 | +1.00 | +0.29% [-0.53, +0.90] | 0.56 | 0.0 | 0.0 |
| 11 | EMBC | bmo 11-24 | no | 26 | short | 46 | 58S | 39S | 53L | 60S | 0 | -0.64 | +0.80 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.0 |
| 12 | TITN | bmo 11-24 | no | 25 | long | 27 | 52L | 46L | 16L | 15S | 0 | +0.42 | +0.80 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.0 |
| 13 | TUYA | amc 11-23 | no | 20 | long | 9 | 10L | 25L | 31L | 12L | 0 | +0.28 | +0.60 | +0.29% [-0.60, +0.82] | 0.56 | 0.0 | 0.0 |
| 14 | AMTM | amc 11-23 | no | 16 | short | 33 | 44S | 30L | 0- | 52S | 0 | -0.31 | +0.00 | +0.29% [-0.64, +0.81] | 0.56 | 0.0 | 0.0 |
| 15 | BZUN | bmo 11-24 | no | 15 | long | 38 | 44L | 35L | 49S | 31L | 0 | +0.42 | -0.60 | +0.29% [-0.65, +0.81] | 0.56 | 0.0 | 0.0 |
| 16 | SMTC | amc 11-23 | no | 12 | short | 36 | 73S | 9L | 6S | 20L | 0 | +0.01 | -0.60 | +0.29% [-0.67, +0.81] | 0.56 | 0.0 | 0.0 |
| 17 | DLTR | bmo 11-24 | no | 7 | short | 35 | 24S | 42L | 6L | 50S | 0 | -0.12 | -0.50 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.0 |
| 18 | ZM | amc 11-23 | no | 5 | short | 15 | 3L | 6L | 4L | 31S | 0 | +0.10 | -0.10 | +0.29% [-0.73, +0.78] | 0.56 | 0.0 | 0.0 |
| 19 | KC | bmo 11-24 | no | 3 | long | 18 | 24S | 24L | 0- | 12L | 0 | +0.12 | +0.90 | +0.29% [-0.74, +0.78] | 0.56 | 0.0 | 0.0 |
| 20 | DY | bmo 11-24 | no | 1 | short | 24 | 15S | 28L | 31S | 15L | 0 | +0.01 | -0.40 | +0.29% [-0.76, +0.78] | 0.56 | 0.0 | 0.0 |

## The two names the book holds (70-79 top-up, no selected name)

**SYM (amc tonight), 74 long.** Opus 5.5 (87) and Fable 5.1 (91) put it in their own top 20%, and Opus 5 at 78 is just below it. The case rests on the 2026-10-29 8-K: Walmart's new agreement, about $6.0B initial commitment that "could increase Symbotic's future backlog by an amount up to $6.92B" against a backlog flat near $22.5B for a year ([8-K](https://www.sec.gov/Archives/edgar/data/0001837240/000119312526437874/d182210d8k.htm)). It was signed after the fiscal quarter closed, so tonight's call is the first time timing and conversion get quantified. The stock trades below its pre-announcement price, and 17.5M shares were short at the 10-30 settlement, about 10 days to cover ([equibles](https://equibles.com/stocks/sym/shortinterest)). **Strongest case against:** management's own conversion arithmetic (about 15% of backlog converting in 12 months, fewer Q4 starts) points the FQ1 guide below a ~$817.5M consensus, which has only one source. Beats were sold on the last two prints (−14.9%, −7.7%), and puts are priced 8.7 vol points over calls. Sonnet 5.5 sat at 38: the judges disagree on size, sd 21.

**DKS (bmo 11-24), 71 long.** Opus 5 (80) and Opus 5.5 (84) are in their own top 20%. The main item is JD Sports' North America like-for-like sales: −2.2% over the 13 weeks to 31 Oct against −6.8% the quarter before, nearly DKS's Q3 window and a direct read on the Foot Locker line. Next is open-market buying: the CFO bought $1.0M on 9-22 and the Foot Locker International president $0.5M on 9-30. Census sporting-goods sales were about +9% YoY over Aug-Oct. **Strongest case against:** Nike's Jordan retro allocation cut hits Foot Locker's US mix (Williams estimates a 40-50% allocation cut in FY27), and the Williams Sell call expects the low end of the FY26 guide to be at risk. That call moved the stock −8% in five days. The FY27 Jordan headwind itself is outside the window. Sonnet 5.5 sat at 46.

## Where the panel and the searcher disagree most

- **SMTC:** searcher −0.6 (findings) / +0.52 (scaled); panel 12 short, but split: Opus 5 73 short against Opus 5.5 9 long and Fable 5.1 20 long. Today's +18% intraday run into the print is the disputed item.
- **ANF:** searcher +1.0; panel 38 long with sd 47, because Opus 5 is short (39S) while Opus 5.5 is in its own top 20% long (82L*).
- **EMBC:** searcher +0.8; panel 26 short (Opus 5, Opus 5.5 and Fable 5.1 short on the FY27 consensus against the implied run-rate; Sonnet 5.5 long).
- **TIGR / VALN:** searcher −1.3 / −1.5, the day's most negative sums; panel only 50 and 40 short.

## Stage E

Stage E wrote no `edge/` for 2026-11-23; its Routine is stopped. There is no comparison and no Spearman ρ for today.

## What the numbers are not

`expected_return_pct` is what names at that percentile have earned. Its out-of-sample record is weak (correlation +0.12 with the realised return over 148 names), so do not size on it. The weights are research. Certainty (`p_up`) is recorded and decides nothing. Nothing checked the searchers' findings for factual errors, and the per-finding key is not reproducible to better than its own size. Baselines: FPI histories (TUYA, KC, TIGR, BZUN, VALN) are empty because `SEC_USER_AGENT` is not set here and `www.sec.gov` answered 403.

## Context: retail, search and volatility (not used for selection)

See `edge-context.json` and the score report: the labels are context only and the panel decides nothing on them.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
