# Stage J — Japan researcher — 2026-09-28

**2 scheduled / 1 eligible / 1 hunted.** `selection.method`: "all 1 eligible names (at or
under the cap)", so no draw was needed. 7624 ＮａＩＴＯ fell to the ¥30m turnover floor
(¥6.4m a day). Calendar sheets: `kessan07_0904` and `kessan08_0918`, `market_closed` null.

## The ranking

| # | code | company | impact_sum | conviction | above floor (3.0) | priced_lean | baseline_quality |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 8227 | しまむら SHIMAMURA Co.,Ltd. | −0.50 | 0.50 | — | −0.25 | 0.725 |

The ranking key is `impact_sum`, as `edge-scores.json` reports it.

## What drives the number

Two findings, both from public monthly sales data, point opposite ways and roughly cancel.

- **Bottom driver: −1.5, lands on the reported quarter.**
  - Same-store sales for Jun–Aug ran −2.0%, −5.1% and +5.3%, roughly flat for the quarter.
  - That is against a Q2 last year that grew +5.5%, and Q1 SG&A was already growing +4.8% on a flat gross margin.
  - So Q2 operating profit very likely falls 5–10% year on year.
  - In September 2025 a −4% Q2 operating-profit decline opened the stock −8.5%.
  - Source: https://www.ryutsuu.biz/sales/s081842.html (2026-08-18). Also used: the June and August monthlies, and the Q1 決算短信.
- **Top driver: +1.0, lands on guidance.**
  - The September monthly (Aug 21 – Sep 20, the first month of H2) showed same-store sales +10.4%.
  - It was published 2026-09-24 and the stock moved about 1% on it.
  - Shimamura has never raised full-year guidance at H1, which caps the upside.
  - Source: https://finance.yahoo.co.jp/news/detail/9858b537314a66047cae76714f37656b71941bf7 (2026-09-25).

The hunter puts `print_vs_bar_pct` at +4.0. H1 will likely beat the company's own
unrevised H1 plan (ordinary profit ¥33.2bn), but no H1 sell-side consensus could be
sourced, so the market's real bar is unknown and both sizes are deliberately small.
Every input is already public. Shimamura's own IR site returned 403 to both `curl` and
`WebFetch`, so the segment monthlies (Avail, Birthday) were not obtained.

**Names that could not be ranked:** none. One name cannot be ranked against anything, though.

## What must be read with it

- **No option anchor, substituted.** `options` is all null.
  - The lean comes from JPX's disclosed short register and 信用倍率.
  - On 8227 the short register is a real zero: no position at or above 0.5%, and no change.
  - So the lean is `margin_overhang` −0.41 (信用倍率 6.68x, crowded margin long) plus `runup` +0.16.
  - Two of the positioning inputs resolved: the register and the margin ratio.
  - **The register file is dated 2026-09-18, ten days before the seal.** The level and the change are that stale.
  - The weights are **priors with no Japanese measurement behind them.**
- **`lean_vs_free_control_rho`: not yet computable.**
  - This fire resolved 2026-09-24. 4716 日本オラクル was confirmed on TDnet, scored −3.50 and moved **+8.15%**, so the sign was wrong. With n=1 there is no ρ.
  - 2026-09-25 (2742, 3333) is confirmed on TDnet, but its move is pending until today's Tokyo close.
  - So no Japanese run has produced a lean-vs-control check yet.
- **`history` is an estimated cadence**, not a record of dates. It gives a median absolute move of 2.91% over 11 estimated events. That is a scale, and no date in it is a fact.
- **Daily 値幅制限 limits truncate the tail**, so a large finding can be right and still not be paid in full.
- **Below the conviction floor.** 8227 sits at |0.50|, far below 3.0. Over the whole US sample the sign was a coin flip below the floor.
- **The lessons control is inert today.**
  - `pre_lessons` equals the final number (−0.5), because `researcher_japan/LESSONS.md` holds no rules until a Japanese run resolves.
  - The hunter also hit its turn limit and was resumed to write its file. The freeze was written at that point, but with the file empty that cannot have contaminated it.
- **One day is not a result.** A one-name day carries no rank information at all.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
