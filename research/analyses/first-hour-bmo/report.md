# Does the first hour tell us where a bmo name goes next?

*Measured 2026-11-05 on every bmo earnings event in the repo's universe files up to 2026-11-04. Hypotheses, indicators, thresholds and the decision time were fixed in `PREREG.md` before any outcome was fetched; nothing below was tuned afterwards. Alpaca SIP one-minute bars, gross, prices not fills. Research, not investment advice.*

## Short answer

**No.** None of the six first-hour indicators, and not the combined trend score, predicts what a bmo name does after 10:30 ET. On 553 bmo earnings gaps of 2% or more (37 days) the largest rank correlation with the move from 10:30 to 13:00 is ρ +0.05 (p 0.22). On all 93 panel bmo calls of `us-panel.v2` it is ρ +0.04 or less. No indicator passes the pre-registered verdict rule (predicted sign at p < 0.0083 in the market-wide tier **and** the predicted sign on our calls).

The strong calls (panel ≥80 with all four judges) lean the predicted way on v2: ρ +0.35, p 0.27, **but that is only 15 calls over 7 days, which is too small to tell anything**. On v3 there are 6 strong calls, too few even to compute a correlation, and on the backtest's 9 strong calls the sign is the opposite.

**What it means for the live exit:** keep selling bmo names at 13:00 ET. A first-hour rule would add nothing measurable, either to get out early or to hold to the close.

## Results

Outcome R1 = the move from 10:30 to 13:00 on the position's side (should we still hold at 10:30?). R3 = 13:00 to the close (should we hold past the current exit?). Spearman ρ with a within-day permutation p. In tier 1 most days have one name, so that p is not informative there.

### Primary test: the trend score (−4…+4) against R1

| Sample | n | days | ρ | p |
| --- | --- | --- | --- | --- |
| T1 strong bmo, `us-panel.v2` | 15 | 7 | +0.35 | 0.27 |
| T1 strong bmo, `us-panel.v3` | 6 | 3 | too few | |
| T1 strong bmo, backtest (Aug–Sep) | 9 | 8 | −0.21 | 0.51 |
| T2 all panel bmo calls, `us-panel.v2` | 93 | 11 | −0.06 | 0.55 |
| T2 all panel bmo calls, `us-panel.v3` | 34 | 4 | −0.09 | 0.59 |
| T2 all bmo calls, backtest | 51 | 13 | +0.20 | 0.19 |
| **T3 all bmo gaps ≥2%, gap side** | **553** | **37** | **+0.005** | **0.91** |

### Secondary indicators against R1 (Bonferroni: p < 0.0083 to count)

| Indicator | T3 market (553) | T2 v2 (93) | T2 v3 (34) | T2 backtest (51) | T1 strong v2 (15) |
| --- | --- | --- | --- | --- | --- |
| First-hour return | +0.04 (0.41) | −0.03 | +0.06 | +0.12 | +0.44 (0.24) |
| Opening range breakout | −0.02 (0.67) | +0.03 | −0.14 | +0.35 (0.010) | +0.21 |
| Price vs VWAP | −0.03 (0.65) | −0.01 | −0.24 | +0.02 | +0.14 |
| Gap held or filled | +0.05 (0.22) | +0.04 | −0.30 (0.11) | +0.35 (0.010) | +0.31 |
| Close location in first-hour range | −0.00 (0.98) | −0.06 | −0.15 | +0.14 | +0.22 |
| First-hour return, high relative volume | −0.03 (0.58) | +0.12 | −0.08 | −0.01 | |
| First-hour return, low relative volume | +0.10 (0.10) | −0.19 | +0.22 | +0.27 | |

Relative volume does not amplify the first-hour move as argued. If anything the low-volume half leans more positive, in three of four samples, and none of those correlations is significant. The two backtest correlations at p 0.010 just miss the corrected threshold, have the wrong sign or nothing on v2 and v3, and are absent market-wide. I read them as chance.

The picture is the same to the close (R2) and from 13:00 to the close (R3): market-wide every |ρ| ≤ 0.06.

### The two pre-registered decision rules (gain per call against the current exit)

| Sample | Rule A: exit at 10:30 if trend ≤ −2 | Rule B: hold to close if trend ≥ +2 |
| --- | --- | --- |
| T1 strong v2 (15) | +0.49 (t 1.67; 3 of 7 days better) | −0.45 (t −1.27) |
| T1 strong v3 (6) | 0 (no call had trend ≤ −2) | +0.40 (t 0.62) |
| T1 strong backtest (9) | −1.29 (t −1.0) | −0.88 (t −1.73) |
| T2 all calls v2 (93) | +0.18 (t 1.00) | −0.18 (t −1.30) |
| T2 all calls v3 (34) | +0.48 (t 1.37; per day t 3.2 on only 4 days) | +0.24 (t 1.02) |
| T2 all calls backtest (51) | −0.11 (t −0.42) | +0.29 (t 0.96) |
| T3 market (553) | −0.12 (t −1.34; 14 of 37 days better) | −0.05 (t −0.73) |

Rule A leans positive on live v2 and v3 calls and negative on the backtest and market-wide. Rule B is mixed. Neither clears t 2 on a sample large enough to matter. On the strong v2 calls, the four names with trend ≤ −2 (CRS, TTMI, WRLD, MED) lost a further −1.84 from 10:30 to 13:00. That is the same pattern as the 28 Oct follow-up (our losing calls kept losing that week), and it rests on four names in one week.

## Why the theory did not hold

The case against, set out in the pre-registration, fits the data: for bmo names the news is priced between 08:00 and 09:30, and after the first hour what is left looks like noise in every cut. The momentum literature (Gao et al. 2018) is about the index, and ORB evidence comes from strategies traded over years, not from a four-hour hold after one report. In our sample the median absolute move from 10:30 to 13:00 is 1.6 points, against 5.2 for the gap itself, and none of it is predictable from the hour before.

## What would change this

- **Strong calls only.** Rule A on strong v2 calls (+0.49, t 1.67) is the only cell that leans the right way where it matters. To show a 0.5 point edge at t 2 at the spread seen here (per-call sd 1.1 to 1.7) takes roughly 20 to 50 strong bmo calls of one prompt version. At about 4 a week that is two to three months. The cheapest forward test is to log the trend score at 10:30 in stage M's bmo rows, and leave the exit alone.
- **Costs.** Rule A adds a second market order at 10:30 in names with wide spreads. Any edge below about 0.3 points would not survive it.

## Data and caveats

- Universe files (stage E and E-P) list 897 bmo events. 553 have a gap ≥2% and enough minute bars: a bar within five minutes of the open, at least 20 one-minute bars in the first hour. There are 37 days because the universe files only start on 30 August and some days had no bmo names.
- The prior close is the close of the last regular 30-minute bar of the previous session, not the official closing auction. Relative volume compares 09:30–10:30 with the same hour over the previous 20 sessions.
- Panel versions follow `provenance.json` `stage_version`: `us-panel.v2` up to 28 Oct, `us-panel.v3` from 29 Oct. Backtest = the Aug–Sep blind re-judge (`research/analyses/panel-mean-pct/`), with the sign and size taken from the mean percentile.
- Prices, not fills, and gross of costs.

## Reproducing

From the repo root: `python3 scripts/events.py events.json`, then `fetch.py events.json <cache>` (needs the Alpaca keys), then `analyse.py events.json <cache>` from an output folder. Full output in `results.txt`, per-tier rows in `out/`.
