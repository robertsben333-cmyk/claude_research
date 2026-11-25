# Stage E-P v3b — 2026-11-25 amc + 2026-11-27 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.**
All four judges ran on their named agents (`panel-judge-v3b-opus5`, `-opus55`, `-sonnet55`, `-fable51`; pinned `claude-opus-5`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1`), with no fallback. The searcher was `unpriced-searcher-v3b`, also with no fallback.
One day of three names is an anecdote. Stage v3b is judged only pooled, by `v3b_compare.py`, from 20 run days onward.

## Panel (own history `panel-history-v3b.json`; selection `panel_pct` >= 80 with all four judges)

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_pct on E-P scale | mean p_clears_real_bar | guide (mode) | searcher impact_sum | E[return] (80% band) | P(right) | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FINV | amc 11-25 | **yes** | 94 | short | 3 | 95S* | 94S* | 90S* | 97S* | 4 | 94 | 37 | cut (4/4) | -2.80 | +4.60% [+2.59, +6.40] | 0.71 | 1.0 | 1.0 |
| 2 | BMA | amc 11-25 | no | 10 | short | 14 | 18S | 18S | 14L | 17S | 0 | 9 | 43 | no_guide (3/4) | -0.40 | +0.29% [-0.69, +0.80] | 0.56 | 0 | 0 |
| 3 | XYF | bmo 11-27 | no | 3 | long | 4 | 3L | 0 | 10L | 0 | 0 | 3 | 50 | no_guide (4/4) | +0.40 | +0.29% [-0.74, +0.78] | 0.56 | 0 | 0 |

The judges' columns are each judge's own percentile (0-100) and side; `*` marks a name in that judge's own top 20%.
`E[return]` is what names at that percentile have earned on the panel's side. It is gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It comes from **stage E-P's** calibration curve (fitted 2026-10-14 on 148 E-P names), not from a curve fitted on v3b. It is a translation of the percentile, not a separate forecast, and its out-of-sample record is weak (correlation +0.12).
The weights are research; nothing trades them. `p_up` is recorded and decides nothing.
On stage E-P's scale (`edge-scores-panel-epscale.json`, a dry run against E-P's judges' live range) the numbers barely move: 94 / 9 / 3.

### FINV, selected short (panel 94, all four judges in their own top 20%)
The judges' notes rest on one item. Qfin, a closely linked peer in the same funding channel and under the same NFRA rules, guided Q4 net income down 67-77% YoY on 2026-11-24 and fell 11.2%, while FINV fell only 4.6%. They add a likely FY guide cut: the street is at RMB 11.31bn, below the 11.5bn bottom of the guide, and all four judges' `guide_direction` reads cut. Opus 5 adds the September OJK TWP90 at 5.36% for the overseas leg. **The strongest case against:** FINV sits at a 52-week low (-17.5% over 20 days), its market cap (~US$556m) is below its cash and short-term investments (~US$946m), and a $150m buyback is live, so a cut may already be priced. The option implied move is 12-17%, but the ATM spread is 67% of mid. The exit session is the Friday half day. The searcher's own key (-2.80) also clears the 2.8 floor.

### Where the panel and the searcher disagree
- **BMA**: the searcher reads -0.40 and three judges lean short. Sonnet 5.5 sits on the long side (14L), which is why the spread is 14.
- **XYF**: the searcher reads +0.40 and the panel calls it a non-result (3). The stock trades as a merger-arb spread to a $6.03/ADS take-private bid (13D, 2026-11-06).

## Comparison with stage E-P (its `edge-panel/edge-scores-panel.json`, read at the end)
- Both stages ranked the same three names: FINV, BMA and XYF.
- **Selected:** v3b {FINV}, E-P {}. Overlap 0 of 1. FINV is at 79.2 on E-P, just under its 80 line.
- **Spearman ρ of `panel_pct_signed`** (E-P −79.2 / −61.1 / −57.1 against v3b −93.9 / −9.9 / +3.2): **+1.00 on n = 3**. Same order, no information.
- Per name:
  - FINV: both short. v3b selects it at 94; E-P does not (79).
  - BMA: both short. E-P is at 61; v3b is at 10.
  - XYF: **the sides differ.** E-P is short at 57; v3b is long at 3, a non-result.
- The two searchers also disagree: E-P's searcher put FINV −0.30 and XYF −2.00; v3b's put FINV −2.80 and XYF +0.40.

## How the universe was built
The strict window held 2 names: FINV (amc 11-25) and XYF (bmo 11-27). It was a thin day, so the 33 time-not-supplied rows were checked with `session_resolve.py`:
- EDGAR killed 3: NWCL, PVL and ENLV.
- 30 were carried, and none had an announced date.
- 11 carried rows at or above $200k turnover went to the sweep, plus BMA and UCFI, which had no bars at the first seal. The other 19 were not hunted.

The sweep confirmed **BMA** from its IR page (amc 11-25). It found KT, NAT, UCFI and AEXA to be phantoms. EH, LEE, OPHI, SIDU, AREC and SRTM have no company date.

Three searchers ran; all finished their search and all carry the v3b fields (`expectations`, `next_guide`, an `evidence_type` on every item). No name was shed, none was unfinished, and none was retried.

The 29 unhunted baselines carry `priced_in.py`'s default `bmo` label, not an established session. They were moved to `baselines/_not_hunted/` because otherwise they read as a 09:30 ET print today. V2 then grounded 3 of 3 before the first print (16:00 ET).

## Standing caveats
- Nothing checked the findings for factual errors. The key is not reproducible to better than its own size: the earlier double hunt had a median gap of 2.4 points, and 4 of 12 pairs had opposite signs.
- Only FINV has an option chain, and it is wide. BMA's and XYF's anchors are historical, and all three baselines' reaction histories were flagged as untrustworthy (6-K text matches).
- Sign balance of the searchers: 2 negative, 1 positive.
- Liquidity:
  - FINV: ~$2.2m a day.
  - XYF: ~$0.5m a day, so thin.
  - BMA: liquid.
- Context labels (not used for selection):
  - FINV: retail 62 (yes); search sparse; vol 52.
  - BMA: retail 44; search quiet 0.86x; vol 38.
  - XYF: retail 63; search quiet 0.73x; vol 86.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
