# Stage J — Japan ranking for 2026-10-02

Research only. No orders. Ranked on `impact_sum` (the key `edge-scores.json` reports), points of spot, signed. No call, no threshold label.

**Funnel:** 9 scheduled / 5 eligible (4 below the ¥15m median-turnover floor) / 5 hunted.
`selection.method`: *all 5 eligible names (at or under the cap 25)* — the date-seeded random draw (`jp-2026-10-02`) was not needed, so every eligible name was hunted. Prompt `jp.v6`, hunters on claude-opus-5-5 (alias timeline).

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | window |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3321 | ミタチ産業 | **+0.60** | +0.40 | 3.3 | 56 | 15:30 | close 10-02 → close 10-05 |
| 2 | 7611 | ハイデイ日高 | **+0.40** | +0.12 | 3.0 | 52 | 15:00 (in session) | 10:05 sealed spot ¥2,932 → close 10-05 |
| 3 | 7965 | 象印マホービン | **+0.10** | +0.00 | 2.0 | 50 | 15:30 | close 10-02 → close 10-05 |
| 4 | 6279 | 瑞光 | **−0.25** | −0.16 | 4.0 | 48 | 16:00 | close 10-02 → close 10-05 |
| 5 | 4394 | エクスモーション | **−1.00** | −0.91 | 6.5 | 43 | 15:30 | close 10-02 → close 10-05 |

5 of 5 rankable. **None clears the 3.0 conviction floor** (largest |impact_sum| 1.00); over the whole US sample the sign below the floor was a coin flip, and the 3.0 floor was set on Opus 5's scale and has not been re-derived for this prompt. Signs: 3 positive, 2 negative (the first resolved Japanese days ran five of seven negative). One name (7611) releases inside the 15:30 session; the other four at or after the close.

## What drives the top and the bottom

- **Top, 3321 ミタチ産業 (+0.60).** +0.8 on the Q1 progress rate. The 09-16 revision already raised H1 OP guidance to ¥1,400m, but that guide is still 11% below last year's actual H1 of ¥1,573m, and the company has a record of guiding low and raising repeatedly. Source: https://kabuyoho.jp/sp/report?bcode=3321. Offset: −0.6 for crowded margin longs (信用倍率 18.4, after a +10.75% 20-day run-up).
- **Bottom, 4394 エクスモーション (−1.00).** −2.0 on its reaction function, rebuilt on true release dates: the stock fell the next session after 10 of its last 12 prints. The only two that rose came with new shareholder returns, and those levers are already spent this year. It also goes in after +85% since 07-02 on a theme run. Source: https://irbank.net/4394/ir. Offset: +1.0 for a possible upward revision, since H1 was 48.5% of plan against a 5-year average of 43.7%. **This lean agrees with the baseline's run-up lean (−1.31), so it is partly the free control wearing another name.**

## Baseline, positioning and caveats (every run)

- **No option anchor; substituted by positioning.** The JPX short register (2026-09-29, 598 codes) resolved for all 5. Margin ratio 信用倍率 resolved for 4 of 5: 4394 is buy-only on margin, so its ratio is undefined. `baseline_quality.direction` is 0.60 for four names and 0.45 for 4394. The lean weights in `lean_components()` are **priors with no Japanese measurement behind them**.
- **`lean_vs_free_control_rho` from the last resolved run (2026-09-30, n=5): 0.80**, up from −0.40 on 09-29 (n=4). On five names that is noise, but it is above the 0.446–0.59 band and drifting toward 1.0, so it is the number to watch. If it settles near 1.0, the positioning terms have stopped resolving and the lean is the run-up again. Today two of the five baselines carry a lean that the hunters argue against:
  - 7965's +0.72, mostly margin overhang from 信用倍率 0.07, is most likely 優待クロス hedges ahead of the November record date, not squeezable shorts.
  - 4394's −1.31 is all run-up.
- **`history` is an estimated cadence, a scale and not a record of dates.** Three hunters showed it is wrong as a scale today:
  - 4394: the true Q3 FY25 date was 10-03, a −0.36% move, against the estimated 10-01 at −3.03%.
  - 6279: several estimated dates fall on the wrong session.
  - 7965: its two measurable Q3 reactions were under 1%, so the hunter set its scale below the 3.59 proxy.

  All three re-derived the scale from real release dates.
- **No independent bar on any name.** For 7611 the IFIS consensus equals the company plan. 7965 has one analyst. 3321, 4394 and 6279 have no consensus reachable. So every size is capped small, which is why the whole day sits inside ±1.
- **Daily price limits (値幅制限) truncate the tail**, so a large finding can be right and still not be paid in full.
- **The `pre_lessons` control was live on three names:**

  | code | pre_lessons sum | final sum | changed |
  | --- | --- | --- | --- |
  | 4394 | −1.5 | −1.0 | yes |
  | 6279 | −0.7 | −0.25 | yes |
  | 7611 | +0.3 | +0.4 | yes |
  | 3321 | +0.6 | +0.6 | no |
  | 7965 | +0.1 | +0.1 | no |

  On 3321 the sizes moved but the sum came out equal. LESSONS rule 1, which pulls negatives that rest on public series toward 50, moved every changed name toward positive.

## What today does NOT establish

Five names on one day, all small, none above the floor, nothing resolved. One day is not a result, and no ranking claim can be read off it. Resolve with `jp_resolve.py` after the 10-05 close and before TDnet's ~31-day window lapses.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
