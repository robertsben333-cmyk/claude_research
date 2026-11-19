# Stage E-P v3b — 2026-11-19 amc + 2026-11-20 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.**
All four judges ran on their pinned models, with no fallback: `panel-judge-v3b-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5),
`-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). All 20 searchers were `unpriced-searcher-v3b`, again with no fallback.
One day is an anecdote. v3b is judged only by `v3b_compare.py`, pooled over at least 20 run days.

- **Universe:** 24 calendar rows. MOG.B was folded by hand into MOG.A, because `share_class.py` did not fold it. That left 23 sealed baselines.
- **Sweep:** 19 of 23 names confirmed from company sources.
- **Hunted:** 20 names, the 19 confirmed plus BJ. BJ was the highest-priority unconfirmed name, and its searcher then confirmed it from BJ's own release of 2026-10-29.
- **Shed:** INTU (aggregator-only date, priority 38), IESC (probable phantom) and GEOS (no schedule release found).
- **Search:** every hunt finished (`search_complete: true`), and all 20 carry the `expectations` and `next_guide` blocks and an `evidence_type` on every finding. No name was marked `v3b fields missing` and none was unfinished.

## Panel (own v3b history; selected = panel_pct >= 80 with all four judges)

How to read the columns:
- **pct** is `panel_pct` against the v3b judges' own history. That history is still essentially stage E-P's seed, copied on 2026-11-14.
- **E-P scale** is the same judges read against stage E-P's live range, from the `--dry-run` file `edge-scores-panel-epscale.json`.
- **Judge columns:** each judge's percentile 0-100, plus L/S for its side. A `*` means the name is in that judge's own top 20%.
- **p_clears** is the four judges' mean `p_clears_real_bar`.
- **guide** is the most common `guide_direction` among the four judges.
- **E[ret]** is stage E-P's calibration curve at that percentile, not one fitted on v3b. It is gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It is a translation of the percentile, not a forecast to size on: out of sample it has correlated +0.12 with the realised return over 148 names.

| # | ticker | sess | sel | pct | side | sd | E-P scale | opus5 | opus55 | sonnet55 | fable51 | p_clears | guide | searcher impact_sum | E[ret] (80% band) | P(right) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GRSD | amc | **yes** | 91 | short | 5 | 89 | 88S* | 86S* | 91S* | 99S* | 40 | cut | -2.80 | +4.23% [+2.15, +6.14] | 0.69 |
| 2 | BSP | bmo | **yes** | 82 | long | 13 | 80 | 60L | 92L* | 90L* | 86L* | 54 | raise | +2.60 | +2.92% [+0.88, +4.89] | 0.62 |
| 3 | ESTC | amc | **yes** | 82 | long | 7 | 78 | 82L* | 90L* | 72L | 82L* | 51 | raise | +2.10 | +2.84% [+0.82, +4.81] | 0.62 |
| 4 | GRRR | amc | **yes** | 81 | short | 11 | 78 | 68S | 74S | 88S* | 95S* | 38 | maintain | -0.90 | +2.77% [+0.76, +4.73] | 0.61 |
| 5 | MOG.A | bmo | | 71 | long | 15 | 66 | 50L | 71L | 70L | 92L* | 56 | initiate | +2.30 | +1.63% | 0.56 |
| 6 | GAP | amc | | 66 | long | 13 | 62 | 72L | 59L | 49L | 82L* | 56 | maintain | +0.60 | +1.23% | 0.56 |
| 7 | ROST | amc | | 61 | long | 10 | 57 | 54L | 78L | 56L | 58L | 55 | maintain | +1.80 | +0.91% | 0.56 |
| 8 | KEYS | amc | | 54 | long | 11 | 49 | 48L | 56L | 72L | 41L | 50 | initiate | +1.20 | +0.36% | 0.56 |
| 9 | NGVC | amc | | 49 | short | 10 | 44 | 40S | 42S | 65S | 48S | 44 | initiate | -2.40 | +0.29% | 0.56 |
| 10 | GLOB | amc | | 48 | short | 14 | 42 | 48S | 32S | 70S | 41S | 44 | maintain | +2.10 | +0.29% | 0.56 |
| 11 | WRD | bmo | | 38 | short | 14 | 36 | 54S | 42S | 16S | 41S | 40 | unknown | -0.60 | +0.29% | 0.56 |
| 12 | RLX | bmo | | 38 | long | 16 | 34 | 48L | 21L | 24L | 58L | 50 | no_guide | +1.10 | +0.29% | 0.56 |
| 13 | POST | amc | | 35 | short | 8 | 32 | 33S | 26S | 34S | 48S | 46 | maintain | -0.30 | +0.29% | 0.56 |
| 14 | ESE | amc | | 35 | long | 26 | 32 | 20L | 56L | 65L | 0 | 47 | initiate | +0.10 | +0.29% | 0.56 |
| 15 | BULL | amc | | 32 | long | 21 | 30 | 2L | 21L | 56L | 48L | 50 | no_guide | +1.00 | +0.29% | 0.56 |
| 16 | BJ | bmo | | 22 | long | 21 | 21 | 44L | 39L | 16L | 10S | 50 | raise | -1.35 | +0.29% | 0.56 |
| 17 | BKE | bmo | | 20 | short | 14 | 18 | 18S | 14S | 43S | 4S | 48 | no_guide | -0.20 | +0.29% | 0.56 |
| 18 | EARN | amc | | 13 | long | 5 | 12 | 20L | 14L | 8L | 10L | 53 | maintain | +0.70 | +0.29% | 0.56 |
| 19 | MATW | amc | | 6 | short | 15 | 6 | 2S | 28S | 8S | 14L | 48 | initiate | -0.50 | +0.29% | 0.56 |
| 20 | FRO | bmo | | 4 | long | 3 | 4 | 4L | 3L | 8L | 0 | 49 | raise | -0.25 | +0.29% | 0.56 |

**The scale matters on three of the four selections.** On stage E-P's scale only GRSD (89) and BSP (80) clear 80. ESTC and GRRR read 78 there. Their selection rests on the v3b history, which is stage E-P's frozen seed of 2026-11-14 plus the v3b sizes since. Weights (`weight_equal`, `weight_precision_tilt`) are in `edge-scores-panel.json`. They are research only, and nothing trades them.

## The selected names

- **GRSD, short (91, four of four).**
  - *Evidence:* the FY26 guide ($165-170m revenue, $45-50m adj EBITDA) needs second-half EBITDA of $28.3-33.3m, against $9.0m and $7.7m in the two quarters just printed. Catena Media, an SEO-led US affiliate peer, pre-announced North America revenue -29% for the same quarter, blaming AI search. Leverage is about 2.7x against a 3.0x covenant. $26.5m of OddsJam consideration is current and can be partly settled in shares at $0.74. The stock's last two guide cuts went -27% and -38%.
  - *Strongest case against:* at about $26m market cap the price already expects a cut. The stock is down 59% since the last print and 42% in 20 days. The last in-line quarter with a held guide bought +19%.
  - *Further caution:* a $0.74 stock with an abs move near 26%.
- **BSP, long (82, three of four; Opus 5 at 60).**
  - *Evidence:* the FY26 guide excluded Airtable and Miro. Bending Spoons' own Miro closing 6-K says Miro will be added to the outlook at this print. Mechanically that lifts FY26 to about $3.0-3.06B, against a Street average of about $2.9B. Separately, a BofA note says the buy-side bar for Q3 revenue sits below guidance.
  - *Strongest case against:* the only confirmed prior print beat and still closed -16.5%. The acquisitions dilute margin, and about $3.5B of new debt adds interest. The put skew is +13.6 on an illiquid chain.
- **ESTC, long (82, three of four).**
  - *Evidence:* the stock is -20% in 20 days on a software sell-off and co-founder supply, with no estimate cuts (Citi raised its target to $132). Management has raised the FY27 guide by more than the quarter's beat in each of the last two quarters.
  - *Strongest case against:* Datadog (-14%) and Dynatrace (-15.6%) were sold on beats this month. IGV has had five one-day drops of 3% or more since mid-October. Every finding is a proxy, an inference or already public.
- **GRRR, short (81, two of four in their own top; Sonnet 5.5 and Fable 5.1 drive it).**
  - *Evidence:* the Street is above the company on every forward period: Q4 $76.7M against a $60-70M plan, FY27 $575M against $450-500M. The Lind financing of Oct 29 is VWAP-priced paper at an 11% discount. The Series B convertible was reset to $8, with up to 22.1M underlying shares, about 80% of shares outstanding.
  - *Strongest case against:* short interest is about 24% of shares outstanding and up 37% in a month. The stock sits 2.5% above its 52-week low. The last two quarters beat the company's own plan.

## Where the panel and the searcher disagree most

- **GLOB:** the searcher is at +2.10 long, and the panel is short at 48. The judges weighted the Disney cost-savings news (Disney is about 9% of revenue) and Globant's guide-cut history over the call-side skew.
- **BJ:** the searcher is at -1.35, while the panel is weakly long at 22. The searcher's `impact_sum` and its own `expected_move_pct` (0) already disagree.
- **GRRR:** the searcher is at -0.90 (p68), but the panel selects it short at 81.
- **MOG.A and NGVC:** the searcher has them at +2.30 and -2.40 (p94 each), while the panel has them only at 71 and 49.

## Comparison with stage E-P (same day, its own sweep and searchers)

- **Coverage:** stage E-P's `edge-scores-panel.json` exists; all four of its judges ran. 19 names were ranked by both stages. BJ was ranked only by v3b, and INTU only by stage E-P.
- **Selected:** v3b has BSP, ESTC, GRRR and GRSD; stage E-P has GRSD. The overlap is GRSD alone.
- **Agreement:** the Spearman ρ between the two `panel_pct_signed` columns is **+0.47** over the 19 shared names.
- **Names where the two panels disagree on side or selection:**
  - **ESTC:** v3b 82 long (selected), against E-P 13 short.
  - **MOG.A:** v3b 71 long, against E-P 14 short.
  - **GLOB:** v3b 48 short, against E-P 56 long.
  - **WRD:** v3b 38 short, against E-P 10 long.
  - **RLX:** v3b 38 long, against E-P 7 short.
  - **BKE:** v3b 20 short, against E-P 11 long.
  - **MATW:** v3b 6 short, against E-P 6 long.
  - **BSP:** v3b 82 long (selected), against E-P 79 long (not selected).
  - **GRRR:** v3b 81 short (selected), against E-P 52 short.

  Two of these differences come from the searchers, because each stage ran its own searchers on its own sweep, so they are not only a prompt effect at the judge level.

## What the numbers are not

`expected_return_pct` is what names at that percentile have earned under stage E-P's curve, with a weak out-of-sample record. It is not a v3b fit, and not a forecast to size on. `p_up` and `p_clears_real_bar` are recorded and decide nothing.

## Process notes

- **Hand fold:** MOG.B was folded into MOG.A by hand, because `share_class.py` did not fold it.
- **Untrustworthy reaction histories:** the sweep flagged FRO, WRD, GRSD, BSP, BULL, GLOB, RLX and GRRR. Each searcher was told, and each rebuilt its base rate from confirmed releases.
- **Not run:** V2 `edge_grounded_score.py` was written before the first print. Since this stage places no orders, no `alpaca_trade.py` call and no shadow-ledger ingest was made.
- **Search coverage:** the searchers met 403s and 503s on individual sites (MarketBeat, Nasdaq, Chartmill and others). None was a budget or rate-limit refusal.

---
This is a forecasting exercise over public information. It is research, not investment advice.
