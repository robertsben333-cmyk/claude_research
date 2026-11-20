# Stage EU — Europe ranking for 2026-11-23 (Mon)

Sealed on Friday 2026-11-20, about 14:40 UTC, while the European markets were still open. The sealed spots are intraday prices, not closes. The event date is Monday 2026-11-23, the next European session.

**Answer first: a three-name day with one strong call.** VER (Verve Group, Stockholm) is the hunter's only sizeable number, at **impact_sum −2.60**. That is below the 2.8 conviction floor. **All four judges put VER short in their own top 20%** (panel_pct 100, sd 0), so the panel selects it. NYKD and CER are near-nulls. The IBKR handoff names VER short at panel_pct 100. VER's 20-day median turnover is about $188k, below the executor's `min_turnover_usd` of $200k, and the handoff therefore carries no name: the executor buys nothing today.

## Ranked on `impact_sum` (the key, per `edge-scores.json`)

| # | ticker | market | session | impact_sum | floor | impact_scaled | abs_move | p_up | already public | new in release |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NYKD | no | bmo (hunter: confirmed by the company's own invitation) | +0.30 (p31) | no | +0.00 | 5.5 | 50 | NOK 286m placement (27 Aug); adverse tax ruling (25 Sep) | first cash-runway statement since both events |
| 2 | CER | uk | bmo (hunter: 07:00 RNS pattern) | +0.20 (p22) | no | −0.14 | 7.0 | 49 | **FY26 pre-released** in the 14 Sep trading update (revenue £46–48m against £52.8m consensus, −12.5% that day) | FY27 outlook and the order book |
| 3 | VER | se | bmo (hunter: 06:00 CET pattern, no timestamp yet) | **−2.60 (p95)** | no | −1.44 | 12.0 | 44 | FY26 guide reaffirmed at Q2 (revenue EUR 680–730m, adj. EBITDA 145–175m) | **likely guidance change**: revenue guide arithmetically out of reach |

Brackets: percentile of |value| among Opus 5.5 reference names. This is a scale, not a rank.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran; there were no fallbacks.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 VER      bmo?    yes 100 short    0  opus5:100S* opus55:100S* sonnet55: 99S* fable51:100S*  4  -4.25
   2 NYKD     bmo?          3 long    20  opus5: 36L  opus55: 12S  sonnet55: 14S  fable51:  0-   0  -0.07
   3 CER      bmo?          4 long    48  opus5:  7S  opus55: 18L  sonnet55: 70L  fable51: 64S   0  +0.03
```

`sel` = 3 of 4 judges in their own top 20% (the market panels' rule). `pct` = `panel_pct`, the size of the mean of the four signed percentiles, each read against that judge's own live range (n=200 each). The judges' own sizes for VER: Opus 5 −5.5, Opus 5.5 −2.64, Fable 5.1 −3.36.

**VER, selected 4 of 4, short.** The judges named these evidence items:
- **The revenue guide.** H1 reported revenue was EUR 289.5m and Bloomberg consensus for Q3 is EUR 169m (Inderes has 165). To reach even the EUR 680m low end, Q4 would need about EUR 221m, +14% on Q4'25's 193.8m. Organic growth was 3.5% in Q2, and the 2025 acquisitions are fully in the base by Q4. The Inderes preview still expects the guide to be reiterated, so a cut is not the modelled case. On this line the stock moved −23.4% (Aug 2025), −17.1% (Nov 2025) and −17.7% (Aug 2026). ([Q2 report](https://view.news.eu.nasdaq.com/view?id=b60a60801b527feb510e022e654d2d5a8&lang=en&src=listed))
- **Financing.** Management said in August that the securitisation expansion would be signed "within the next few weeks", and it is still unannounced. The 2025/2029 FRN was quoted at 82, but that is one thin quote and snippet-grade. The covenant caps NIBD/EBITDA at 4.50x, against 4.1x reported.
- **The CFO.** He was replaced with immediate effect on 3 Nov, so this is the new CFO's first report.

**The strongest case against VER:**
- The CEO bought about EUR 0.4m of shares on 19–23 Oct, after Q3 had closed and before the closed period. Under MAR that bounds the "they already knew" story.
- PubMatic (+17% Q3 revenue, a beat) and Magnite (political ad spend near 3x its forecast) point to a strong open-internet Q3 against a soft Q3'25 base.
- The stock is down about 25% over 20 days, so a "not as bad as feared" relief move is live.
- The sealed `priced_lean_pct` is +1.24, so the free control says bounce.
- The Swedish register shows nothing at the 0.5% floor. That is a truncated zero, not an anchor.

**Where the panel and the hunter disagree:**
- **CER:** the judges split 2 long and 2 short, with sd 48, the widest of the day. The hunter has it at +0.2.
- **NYKD:** three judges lean slightly short or flat, against the hunter's +0.3. All of them are near zero.
- **VER:** sits below the conviction floor (−2.60 against 2.8), yet the panel selects it unanimously.

**What these numbers are not:**
- `panel_score` ranks and does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The EU panel has no measured edge yet: on 2026-10-21 it read ρ +0.22, p 0.19 on 45 names. Nothing about this market's panel is established.

## What drives the top and the bottom

- **Top, NYKD +0.30:**
  - Three small items: the first runway statement after the placement and the tax ruling (+0.2); the non-cash tax write-down on the ~USD 33m receivable (−0.1, disclosed 25 Sep); and a boilerplate change from "novel immunotherapies" to "cancer vaccines" since 5 Nov (+0.2, inference from wording only).
  - There is no consensus and no bar, so every size is capped small. ([invitation, NewsWeb 686560](https://newsweb.oslobors.no/message/686560))
- **Bottom, VER −2.60:** the revenue-guide arithmetic above (−2.5) and financing (−1.0), offset by peers (+0.8), CEO buying (+0.7) and the new CFO (−0.6).
- **CER +0.20:**
  - Positive: a NED bought £138k at 690p on 21 Oct, after year-end (+0.5); JPMorgan AM sold below 5% by 23 Oct, so that overhang is finished (+0.3); and a final-dividend raise looks likely (+0.3).
  - Negative: the stock retraced nearly all of the September warning with no news (−0.8), and no contract-win RNS has come out since January (−0.2). ([results notice](https://www.investegate.co.uk/announcement/rns/cerillion--cer/notice-of-final-results-and-investor-presentation/9875780))

Not ranked: none. All three events are confirmed by the issuer's own calendar or notice.

## The day's composition and its caveats

- **The draw:** `selection.method` is "all 3 eligible names (at or under the cap)", so the random draw was not needed (seed `eu-2026-11-23`). 10 were scheduled and 3 were eligible above the $100k floor.
  - `by_market`: uk 1, se 1, no 1.
  - `selection.market_concentration`: the largest market is the UK at 33%, across 3 markets. No market dominates, but three names cannot be ranked against each other in any meaningful way.
- **Calendar sources:**
  - Yahoo read in all ten markets.
  - The UK RNS calendar read: 5 dated, confirming CER, CAR and DSW.
  - Issuer calendars read for de, se, dk, fi and no.
  - **bankier (pl) returned HTTP 403.**
- **Session:** all three were `session_unresolved` at seal (bmo assumed). Each hunter confirmed bmo, from the issuer's own invitation (NYKD) or from the release-time pattern (CER at 07:00, VER at 06:00). Getting the session wrong roughly halves the move.
- **Option anchor:** `options` is null in all ten markets, so Europe runs in the anchor-less regime (ρ +0.073, p 0.45 over 104 events on the sealed corpus).
- **Short registers:**
  - The no, se and uk registers all read.
  - **`anchor_covered: true` for 1 of 3 names, CER**: FCA, 1.73% net short, −0.1 pt.
  - NYKD and VER read 0.0%, which is a truncated zero below the 0.5% floor, not an anchor.
- **Spain/Poland:** 0 names. **Germany:** 0 names.
- **`lean_vs_free_control_rho`:** the most recent resolved European run (2026-10-16) reported it only for se, at 0.60. The lean's weights are priors borrowed from the US runs and have been measured nowhere in Europe.
- **History basis:**
  - VER is `estimated_from_cadence`. That is a scale, not a record of dates.
  - CER (`observed_rns`) and NYKD (`observed_newsweb`) carry observed histories.
- **Conviction floor:** no name clears 2.8. Over the whole US sample, the sign below the floor was a coin flip.
- **language_note:**
  - NYKD: the Norwegian sources added nothing, because Nykode publishes in English only.
  - CER: the domestic RNS record carried nothing the wires did not.
  - VER: the Swedish filings are translations. A Danish-language Inderes forum carried retail colour, one post on the falling bond and one suggesting the −7% on 3 Nov "looked like someone knew". That is colour, not evidence.
- **Nordic resolve deadline:** VER must be resolved within about a week, or the Nasdaq Nordic feed window passes.
- **One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
