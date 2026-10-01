# Edge hunt (Sonnet) — 2026-10-01 amc + 2026-10-02 bmo

1. **This is stage E-S. The hunters ran on Sonnet, the sweep and orchestration on Opus, and no orders were placed.** This is an operator re-run. The 17:06 UTC fire's pushes were refused with a 403, so none of that output reached origin, and none of it was reused.
2. **Comparison with stage E** (`research/2026/10/2026-10-01/edge/edge-scores.json`). Both stages ranked the same single name, NKE.
   - `impact_sum`: stage E (Opus hunter) **−0.38**, stage E-S (Sonnet hunter) **+0.84**. Opposite signs, and both are under the 3.0 floor.
   - Spearman ρ between the two `impact_sum` columns is **undefined on n=1**.
3. **One day is an anecdote twice over.** Neither ranking has a resolved outcome yet, and agreement or disagreement between the two is not evidence that either is right.

**The two runs did not see the same baseline, and that difference is not the hunter model.** This run sealed at **19:18 UTC**, about 2h11m after stage E's seal at 17:07 UTC.

| | stage E | stage E-S |
| --- | --- | --- |
| sealed (UTC) | 17:07:44 | 19:18:51 |
| spot | 35.945 | 35.915 |
| straddle implied move | 9.22% | 8.91% |
| 25-delta skew (put − call, vol points) | **+2.03** (downside paid) | **−11.22** (upside paid) |
| `priced_lean_pct` | −0.94 | **+5.00** |

The Sonnet hunter's largest finding (+1.6, positioning) cites the −11.22 skew as calls bid against a record short. Stage E's hunter never saw that skew. **Part of the sign flip is therefore the later baseline, not the model**, and this day cannot separate the two.

## Ranked table

The ranking key is `impact_sum`, as `edge-scores.json` names it.

| ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control (−run_up_20d) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NKE | amc 2026-10-01 | +0.84 | **+0.84** | not run (E-S skips V2) | no | unknown: E-S runs no `alpaca_trade.py`. Turnover ≈ $1,249m/day (spot 35.915 × 20-day average volume 34.78m, from the baseline tape), ok | +6.08 |

Pre-lessons is measured beside the key. Nothing in this stage is traded.

- **Universe:** 1 of 19 calendar rows in the window, the same as stage E. The thin-day `--include-unknown` check was skipped for time. Stage E's check found nothing it could carry into the window.
- **Sweep:** confirmed 1 of 1 from the company release (amc, ~16:15 ET), 0 phantom. It flagged the 2026-06-23 history row as a non-earnings item 2.02; the Q4 print was on 06-30.
- **Hunt:** one hunter, sealed 19:21 UTC, well before the print.

## What drives it

- **+1.6, positioning.** Short interest is a record ~87m shares (>7% of float, against <3% a year ago). The stock is 52% off its high and 1.5% above its 52-week low. Calls are richer than puts at the time of this seal. Source: https://finance.yahoo.com/markets/stocks/articles/nke-ticks-higher-ahead-q1-080734899.html
- **−0.76, guidance.** The sell-side cut ahead of the print and is sized small because it is mostly priced. UBS models a Q2 guide of 31–43c against ~53c consensus. Piper Sandler has Q1 at $0.37 against $0.43. BofA went to Underperform on 09-25. Source: https://sgbonline.com/exec-nike-faces-stock-price-cuts-amid-concerns-over-upcoming-q127-report/

**The hunter's numbers.** `abs_move_pct` 10.5, `p_up` 54, `expected_move_pct` +0.84, `print_vs_bar_pct` +1.0 against a bar of EPS ~$0.43–0.44 and revenue ~$11.3bn. `LESSONS.md` changed nothing, so pre_lessons equals the key.

**What the hunter could not reach.** Two call-transcript fetches returned 403. It found no IEEPA refund update for Q1, and no China peer (Anta, Li Ning) read-through was retrieved.

**Compared with stage E's hunter.** Stage E's hunter filed five findings to this hunter's two: tariff-rate relief, wholesale sell-through, China retail, the EPS ceiling, and the bar cut. Both hunters identified the bar cut and the record short. They differed in how much weight they gave the squeeze.

## Standing caveats

- **Order and sign.** Below the floor the sign is a coin flip on the evidence so far (53% over 38 events). Above it, the rank of conviction predicted sign-correctness at ρ=+0.514. Do not read +0.84 as a bullish view. `impact_sum` ranks and does not size; it is not a forecast of the move.
- **Control.** `-run_up_20d_pct` is +6.08. With one name there is no ordering to compare against it.
- **Sign balance:** 1 hunt leaned positive, 0 negative.
- **Nothing checked the findings.** There is no adversary pass and no second hunter.
- **Reproducibility.** The key is not reproducible to better than its own size: twelve double-hunted pairs had a median gap of 2.40, and four of the twelve had opposite signs. Today's Opus/Sonnet pair adds one more opposite-sign pair, confounded by the baseline.
- **Baseline:** 1 of 1 names had a live option chain, so the expected move is priced, not inferred.
- **Capacity:** not a constraint on this name.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
