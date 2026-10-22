# Stage J — Japan ranking for 2026-10-22

**Funnel:** 6 scheduled, 3 eligible, 3 hunted. Three names were dropped on the ¥15m median-turnover floor: 5204 石塚硝子 (¥13.7m), 8617 光世証券 (¥3.0m) and 9478 SEホールディングス (¥8.5m).
- **Selection:** `all 3 eligible names (at or under the cap)`. The date-seeded random draw (seed `jp-2026-10-22`) had nothing to cut.
- **Calendar:** sheets `kessan09_1016` (as of 2026-10-15), `kessan08_1002` (2026-10-01) and `kessan` (4 rows).
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5.

**Release times**, as each hunter found them:
- **3091 and 8954 at 15:30 JST.** Both are taken from prior 短信 timestamps.
- **6146 at 16:00 JST.** The jioinc preview says 中間決算は10月22日16時, and kabutan lists it as 引け後.
- None releases inside the session, so for all three the window runs from the 10-22 close to the 10-23 close.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8954 | ORIX JREIT (Aug-26 period) | **+0.30** (p28) | no | +0.13 | 1.3 | 55 |
| 2 | 3091 | Bronco Billy (Q3) | **+0.00** (p5) | no | −0.07 | 3.3 | 49 |
| 3 | 6146 | DISCO (H1) | **+0.00** (p5) | no | −0.15 | 7.5 | 49 |

3091 and 6146 tie on the key at 0.00. Their order is the scorer's tie-break and means nothing.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran on their pinned `-intl-` agents, with no fallback. The selection rule is `consensus`: 3 of 4 judges must put the name in their own top 20%.

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6146 | **yes** | 79 | short | 7 | 76S | 69S | 87S* | 83S* | 3 | −1.31 | +0.00 |
| 2 | 3091 | no | 26 | short | 17 | 43S | 2L | 30S | 32S | 0 | −0.31 | +0.00 |
| 3 | 8954 | no | 8 | long | 1 | 6L | 8L | 8L | 10L | 0 | +0.12 | +0.30 |

**The k and the stars use two different references.** The star (`*`) is drawn against each judge's live sizes only. `k` counts against the scorer's member reference, a 200-size history window whose q80s are opus5 1.40, opus55 0.92, sonnet55 0.90 and fable51 1.16.
- Opus 5 sized DISCO at −1.44, which clears its 1.40 q80, so k = 3 although only two stars print.
- Opus 5.5 sized it at −0.68, which clears neither reference.

**Selected: 6146 DISCO, short (k = 3, panel_pct 79).**
- **What the judges rest on:** all four lean on finding 1, the Oct–Dec guide against an IFIS-implied ~¥69bn ordinary profit (+13% on the quarter), when DISCO guides conservatively. In July it guided Jul–Sep below a ¥60bn+ consensus at ¥55.9bn and fell about 12%.
- **They agree the reported quarter is priced.** The 10-06 non-consolidated flash and the 10-19 Nikkei 観測 were both public, and the stock sold off on them.
- **The strongest case against:**
  - The consensus figure comes from one undated aggregator page (kabuyoho).
  - The stock is already down about 19% since 10-06 and about 42% from June, so a soft guide may be in the price.
  - TSMC held FY capex at $60–64bn, which implies a large Q4 step-up and supports a firm order outlook.
  - The interim dividend will likely be raised.

**Where the panel and the hunter disagree most.** On DISCO the hunter netted its findings to exactly 0.0: the guide risk at −1.0 against the TSMC read-through at +0.8. Every judge sized the guide risk larger and the TSMC proxy smaller, from −0.68 (Opus 5.5) to −1.5 (Fable 5.1). On 3091 the hunter's 0.00 sits against a small panel short; Opus 5.5 alone leaned long (+0.08). No name sits above the conviction floor, so there is no floor-clearer the panel skipped.

**What the numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- Member scales are still mostly the frozen E-P seed, at 132 live sizes each.
- In the four-model re-judge the judges ranked Japan *worse* than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.

## What drives the top and bottom

**Top, 8954 ORIX JREIT (+0.30).**
- **The main finding (+0.3, guidance; range −0.8 to +1.2).** The Feb-2027 DPU forecast of ¥2,450 was set in April. That was before the ¥29.4bn Toyosu Prime Square acquisition, which closed 2026-09-30 inside the period, and the forecast also leans on an ¥805m reserve drawdown. A raised forward DPU path and a first Aug-2027 guide are more likely than not.
- **Source:** https://tdnet-pdf.kabutan.jp/20260826/140120260826526425.pdf
- **The other two findings:**
  - Aug-2026 DPU should print slightly above forecast (+0.1), from https://tdnet-pdf.kabutan.jp/20251021/140120251021576479.pdf.
  - kabutan's automated headline will likely read 経常減益 as the sale gain rolls off (−0.1). Peers split on that headline: Nomura Master Fund fell 4.58% after it, from https://kabutan.jp/stock/news?code=3462&b=k202610160007.
- **Why it stays small:** this name sold its last beat-and-raise (−1.69% on 2026-04-22). The REIT tape is weak (ETF about −5.8% over 20 days). 信用倍率 is 328, a crowded margin long.

**Bottom, 6146 DISCO (0.00).**
- **The finding that drives it (−1.0, guidance).** The IFIS consensus via kabuyoho implies Oct–Dec ordinary profit of about ¥69.0bn: the 9M figure of ¥181.3bn less H1 ¥112.4bn. That is about 13% above the ~¥61bn Q2 that the Nikkei 観測 implies, against a company that guided below consensus in July.
- **Source:** https://kabuyoho.jp/sp/report?bcode=6146
- **What offsets it:**
  - TSMC's Q4 guide and its held capex imply a step-up (+0.8), from https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000726/a3q26e_withguidancexfinal.htm.
  - An interim dividend raise is likely (+0.2), from https://www.disco.co.jp/jp/ir/library/doc/fr/fr20260723.pdf.
  - The quarter itself is pre-released and was sized 0.0, per https://kabutan.jp/stock/news?code=6146&b=n202610070754.

**3091 Bronco Billy (0.00).**
- **For it (+0.5):** a probable Q3 beat on an easy comps base, against a plan-implied operating profit of about ¥1.0bn, per https://tdnet-pdf.kabutan.jp/20251021/140120251021576231.pdf.
- **Against it (−0.5):** the company has never revised at Q3. The stock is at an all-time high, above Tokai Tokyo's ¥2,800 target, which sets up a 出尽くし reaction, per https://kabutan.jp/stock/finance?code=3091.
- **The street bar is unsourced,** so both sizes are capped.

**Names that could not be ranked:** none. All three were rankable.

## Standing caveats

- **No option anchor; substituted by positioning.**
  - JPX short register (as of 2026-10-21): 3091 0.78%, one seller, down from 0.82%, so covering slightly. 6146 and 8954 are absent from the register, a real zero truncated at 0.5%.
  - 信用倍率 resolved for all three: 3091 0.82 (the short side is the bigger one), 6146 11.16 (crowded long), 8954 328 (extreme long overhang).
  - Leans: 3091 +0.32, 6146 −0.59, 8954 −0.95.
  - `baseline_quality` read 0.60 on all three today, against 0.725 on the 2026-09-11 universe.
  - The lean's component weights are **priors** with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`:**
  - **Small runs:** this session resolved 10-19 (4 names) at 0.2 and 10-20 (4 names) at 0.4.
  - **Last full run:** 2026-10-15 (25 names) at 0.531, after 0.789 on 10-14 and 0.406 on 10-13.
  - It has not climbed back to 1.0, so the positioning sources are still resolving.
- **`history` is an estimated cadence**: a scale for how much the name moves, not a record of dates. No date in it is cited here as a fact.
- **Signs:** 1 positive and 2 exactly zero on the key, none negative. On `impact_scaled` it is 1 positive and 2 negative. The first resolved days were five of seven negative.
- **Conviction floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign below the floor was a coin flip.
- **Price limits:** the daily 値幅制限 truncates the tail. That matters only for DISCO, whose 7.5% scale is well inside its limit.
- **One day is not a result.** Three names cannot be ranked meaningfully against each other, and ρ is withheld below five at resolution.

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._
