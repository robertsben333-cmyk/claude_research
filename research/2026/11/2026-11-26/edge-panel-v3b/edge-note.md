# Stage E-P v3b — 2026-11-26 window (2026-11-26 amc + 2026-11-27 bmo)

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.** All four judges ran on their pinned models (panel-judge-v3b-opus5 / -opus55 / -sonnet55 / -fable51), with no fallback. The searcher was the native `unpriced-searcher-v3b`. **One name on one day is an anecdote.**

Today is Thanksgiving, so the US market is closed. Friday 2026-11-27 is a half-day session that closes at 13:00 ET. The window has 1 of 26 calendar rows with a session (XYF, 11-27 bmo). The thin-day check (`--include-unknown` + `session_resolve.py`) found 25 unresolved rows: 4 were killed by EDGAR, 21 were carried, and none was confirmed by a press release, so none was hunted. The sweep confirmed XYF from the company's own release (results before the US open on 11-27, call at 08:00 ET).

## Panel

| # | ticker | session | selected | panel_pct | side | sd | panel_pct (E-P scale) | opus5 | opus55 | sonnet55 | fable51 | k | searcher impact_sum | E[return] (80% band) | P(right) | mean p_clears_real_bar | guide_direction |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| 1 | XYF | bmo 11-27 | no | 41 | short | 18 | 38 (short) | 59 S | 12 S | 51 S | 42 S | 0 | -0.90 | +0.29% [-0.51, +0.96] | 0.56 | 49.5 | no_guide (4/4) |

- Nothing is selected: no name has a panel_pct of 80 or more.
- The expected return is stage E-P's calibration curve (fitted 2026-10-14 on 148 E-P names), not a curve fitted on v3b. It is gross and on the scorebord window. Below a percentile of about 50 it is flat at about +0.3%.
- Judges' three-part forecasts: p_clears_real_bar 48 / 45 / 60 / 45. Move if it clears +3.0 / +2.5 / +2.5 / +3.0. Move if it misses -6.0 / -3.0 / -6.0 / -6.0.
- The judges' raw sizes are all negative: impact_sum -1.40 / -0.24 / -0.63 / -0.80.

**Why the read is small and short.** XYF trades as a deal stub. On 2026-11-06 the controlling holder (Mangrove Coast: 47.97% of shares, about 94% of votes) proposed taking the company private at US$6.03/ADS. Spot is 5.25, about 13-15% under the bid. The main negative is the Qfin (QFIN) Q3 read-through: loan volume -40.6% YoY and Q4 net income guided -67 to -77%. Smaller negatives are the funding-partner squeeze, XYF's own deposit provision, and the buyback, which expires 2026-11-30. The case against the short: the bid acts as a floor, and the release may contain deal-progress language that tightens the spread. XYF did not follow QFIN's 7.6% fall on 11-25.

## Comparison with stage E-P

Stage E-P's `edge-scores-panel.json` exists. Both stages ranked one name, XYF.
- Neither stage selected it, so the overlap of the selected sets is empty on both sides.
- Spearman ρ between the two `panel_pct_signed` columns is undefined on one name.
- Both panels are on the short side: E-P at -38.6, v3b at -41.0 on its own history and -38.4 on E-P's scale.
- The two panels do not disagree on side or on selection.
- The searchers differ more than the panels do: v3b impact_sum -0.90 (V2 -1.70), E-P -0.40 (V2 -0.52).

## What the numbers are not

expected_return_pct is what names at that percentile have earned. Its out-of-sample record is weak. It is not a forecast to size on. p_up is recorded and decides nothing. The searcher's v3b fields are present: an expectations block, a next_guide block (`no_guide`), and an evidence_type on 10 of 10 items. `print_vs_bar_pct` is null because no Q3 consensus could be found.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
