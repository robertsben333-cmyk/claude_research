# Edge hunt (panel v3b): 2026-11-27 amc + 2026-11-30 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts. It places no orders.**
All four judges ran as their pinned agents, with no fallbacks: `panel-judge-v3b-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). The searcher was `unpriced-searcher-v3b`, run as the agent itself, not the fallback.
This is one day with four names, so it is an anecdote. Judge v3b only through `v3b_compare.py`, pooled over many days.

The run fired on the Friday after Thanksgiving, after the 13:00 ET early close. Nothing confirmed prints in today's amc leg. All four names report on Monday 2026-11-30 before the open.

## The panel (each judge read against its own v3b history)

| # | ticker | session | selected | panel_pct | side | sd | E-P-scale pct | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum (searcher) | E[return] | p_right | w_equal | w_tilt | mean p_clears_real_bar | guide (modal) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HMR | 11-30 bmo | **yes** | 99 | short | 2 | 98 | 100 S* | 100 S* | 96 S* | 100 S* | 4 | -3.08 | -3.80 | +5.0% | 0.73 | 1.0 | 1.25 | 32 | no_guide (4/4) |
| 2 | CHA | 11-30 bmo | **yes** | 84 | long | 10 | 84 | 100 L* | 76 L | 84 L* | 77 L | 2 | +1.26 | +3.00 | +3.2% | 0.64 | 1.0 | 0.75 | 53 | raise (4/4) |
| 3 | BOSC | 11-30 bmo | no | 68 | long | 11 | 63 | 86 L* | 58 L | 69 L | 59 L | 1 | +0.81 | +1.80 | +1.4% | 0.56 | 0 | 0 | 55 | maintain (4/4) |
| 4 | NAT | 11-30 bmo | no | 51 | long | 19 | 48 | 76 L | 24 L | 46 L | 58 L | 0 | +0.64 | +1.90 | +0.3% | 0.56 | 0 | 0 | 50 | raise (4/4) |

`*` means the name is in that judge's own top 20%. A name is selected when `panel_pct` >= 80 and all four judges are present, as in stage E-P.

The E-P-scale column reads the v3b judges against stage E-P's judges' live range, in a dry run (`edge-scores-panel-epscale.json`). It selects the same two names.

`E[return]` is how much names at that percentile have earned, gross, on the scorebord window. It is a translation of the percentile, not a separate forecast:
- It comes from **stage E-P's calibration curve**, fitted 2026-10-14 on 148 resolved E-P names. It is not fitted on v3b.
- Its out-of-sample correlation with the realised return is weak (+0.12).
- Below a percentile of 50 it is flat at about +0.3%.

The weights are research only, and this stage trades nothing.

## Not ranked
- **PWRL**: baseline sealed. The sweep found no results date (an N-2 fund that reports NAV "upon audit"), so it was not hunted.
- **Phantoms**: 15 time-not-supplied rows were dropped as phantoms (KT, AIV, HTT, AREC, LOT, CBAT, CURR, SIDU, CELU, NORD, AAME, SCLX, GDC, IPST, PWRL). See `sweep.json`.

## Selected names

**HMR (short, 99, all four judges in their own top 20%).** The main evidence is the expectations block.
- The stock rose +57% over four sessions into the print, from 0.93 to 1.46. There was no release or filing to explain it, and tanker peers moved only +3.5% to +5.3%. The float is about 6.0m shares, insiders hold 89.8%, and days to cover is 0.14.
- The stock sold its last two prints: Q2 2026 beat revenue by 19% and moved -10.8%.
- The quarter being reported is weak. Ardmore's MR spot rates fell 48% q/q. In September the CEO spoke of a "massive decline in volume" in product tankers.
- The judges' mean `p_clears_real_bar` is 32.
- **Case against:** Q4 commentary will include October's record crude rates, and the revenue bar ($21.5–22.4m) is set below Q2's $29.0m. With a squeezable float that has no catalyst, the stock can also keep running.
- Sources: Q2 results https://finviz.com/news/387320/heidmar-maritime-holdings-corp-reports-results-for-the-second-quarter-ended-june-30-2026 ; date https://finviz.com/news/421211/heidmar-announces-date-for-the-third-quarter-2026-financial-results-conference-call-and-webcast

**CHA (long, 84; Opus 5 and Sonnet 5.5 have it in their top 20%).**
- The -21% five-day path in the sealed tape is mostly the US$1.95 special dividend, which went ex on 11-23. With the dividend added back, the stock is about -7%.
- The board declared that dividend and a 50% payout policy on 11-12. That came after Q3 had closed and 18 days before the report.
- The EPS bar implies a 12–13% net margin, against 14.3% in Q2. Q4 laps a -25.5% comparison.
- All four judges expect the guide to be raised (`raise`).
- **Case against:**
  - The EPS consensus is disputed ($0.33 / $0.34 / $0.36).
  - Luckin's same-store sales were -11.1%.
  - Mixue is at a post-IPO low.
  - October catering sales were +0.7%.
  - The judges' mean `p_clears_real_bar` is only 53.
- Source: https://www.globenewswire.com/news-release/2026/11/23/3408151/0/en/chagee-to-announce-third-quarter-2026-financial-results-on-november-30-2026.html
- Note that the CHA baseline was amended from `suspect` to `unknown` after the searchers and before scoring. The 6-K matcher had read the 11-12 dividend announcement as a print, and the company's own release confirms the date. The other three names stayed `unknown`, so the amendment was applied symmetrically.

## Where the panel and the searcher disagree most
- **NAT**: the searcher has +1.9 (p90 of its scale), but the panel puts it at 51. Opus 5.5 is at 24. The judges weighed sector shares selling record Q4 books (TNK -3.06%, DHT +1.8%) against the Q4 booking step-up.
- **CHA**: the searcher has +3.0 (above the floor), and the panel puts it at 84 with a spread of 10. Only two judges have it in their top 20%.

## Comparison with stage E-P (`edge-panel/edge-scores-panel.json`, read at the end)
- **Names both ranked:** HMR, BOSC, NAT. Stage E-P's sweep did not confirm CHA (it found no company date), so stage E-P has no hunt for it.
- **Selected:**
  - v3b: {HMR, CHA}.
  - E-P: {HMR, BOSC}.
  - Overlap: HMR.
- **Spearman ρ of `panel_pct_signed` on the 3 common names:** +1.00, with the same order (HMR < NAT < BOSC). Three names is not a measurement.
- **Disagreements, one line each:**
  - **BOSC**: E-P has 83 long and selects it; v3b has 68 long and does not. The v3b judges weighted the next guide being only reaffirmed on 11-17, and the street's Q4 of $15.0m against $11m of scheduled Q4 backlog.
  - **CHA**: v3b selects it at 84 long. E-P did not hunt it, because its sweep found no company date.
  - **NAT**: both are long and neither selects it. E-P has 18 and v3b has 51.
  - **HMR**: both short and both selected (98.4 and 98.8).

## Searcher table (score_report.py)
See the run's closing reply.
- `impact_sum`: CHA +3.00, NAT +1.90, BOSC +1.80, HMR -3.80. HMR and CHA clear the 2.8 floor.
- V2 grounded: CHA +4.14, NAT +1.88, BOSC +1.41, HMR -10.92.

## v3b fields
All 4 hunts carry `expectations`, `next_guide` and an `evidence_type` on every finding (45 of 45 findings). No hunt is marked `v3b fields missing`. All 4 have `search_complete: true`.

## What the numbers are not
- `expected_return_pct` is stage E-P's curve applied to a v3b percentile, not a forecast to size on.
- `p_up` decides nothing.
- The v3b panel history is still mostly the seed copied from stage E-P, so for about the first ten run days the scale is E-P's.
- No orders were placed and no `alpaca_trade.py` call was made.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
