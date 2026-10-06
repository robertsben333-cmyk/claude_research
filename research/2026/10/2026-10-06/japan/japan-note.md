# Stage J — Japan ranking for 2026-10-06

Research only. No orders. Ranked on `impact_sum`, the key `edge-scores.json` reports, in points of spot, signed. There is no call and no threshold label.

**Funnel:** 9 scheduled / 7 eligible (3396 フェリシモ and 6496 中北製作所 below the ¥15m median-turnover floor) / 7 hunted.
`selection.method`: *all 7 eligible names (at or under the cap)*. The date-seeded random draw (`jp-2026-10-06`) was not needed, so every eligible name was hunted. `calendar_as_of` is 2026-10-01. Prompt `jp.v6`; hunters on claude-opus-5-5 (alias timeline).

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6469 | 放電精密加工研究所 | **+1.90** | +1.30 | 6.5 | 60 | 16:00 | close 10-06 |
| 2 | 8011 | 三陽商会 | **+1.00** | +0.45 | 3.2 | 57 | 11:00 (in session) | sealed spot ¥1,331 |
| 3 | 1377 | サカタのタネ | **+0.60** | +0.25 | 2.5 | 55 | 15:30 | close 10-06 |
| 4 | 2659 | サンエー | **+0.60** | +0.42 | 3.5 | 56 | 15:00 (in session) | sealed spot ¥3,195 |
| 5 | 2734 | サーラコーポレーション | **0.00** | 0.00 | 2.3 | 50 | 15:00 (in session, uncertain: H1 was 15:30) | sealed spot ¥1,159 |
| 6 | 2726 | パルグループHD | **−0.30** | −0.33 | 5.5 | 47 | 15:30 | close 10-06 |
| 7 | 5243 | note | **−1.20** | −1.20 | 10.0 | 44 | 15:30 | close 10-06 |

All 7 names are rankable. 1377 and 2659 tie at +0.60.

- **None clears the 2.8 conviction floor**; the largest |impact_sum| is 1.90. Across the US sample the sign was a coin flip below the floor.
- **Signs:** 4 positive, 1 zero, 2 negative. The first resolved Japanese days ran five of seven negative.
- **In-session releases: three** (8011 at 11:00, 2659 and 2734 at 15:00), all after the 10:05 JST seal, so all three enter at the sealed spot. 6469 releases at 16:00, after the close.

## What drives the top and the bottom

- **Top: 6469 放電精密加工研究所 (+1.90).**
  - **Main finding, +2.0 (range −3 to +6):** Q1 operating profit of ¥561m is already 69% of the revised H1 plan of ¥810m, which leaves ¥249m for Jun–Aug on flat sales. The company beat its own revised H1 plan by 90% last year and has revised its full year at every H1 print since 2023. What the release adds is the size of a full-year raise against a single IFIS recurring estimate of ¥1,400m. Source: https://tdnet-pdf.kabutan.jp/20260707/140120260706588054.pdf
  - **Smaller findings:** MHI read-through +0.4 (search snippet only, `snippet_only`); a run-up into the print on 37x plan EPS −0.5. Last year's H1 beat with a cautious FY raise traded −3.1%.
- **Bottom: 5243 note (−1.20).**
  - **Main finding, −2.5 (range −10 to +2):** the stock is +40% in 20 days, and the last leg, +28% over 9/29–10/02, came on the Himeji school-board adoption, which the company provides free. 信用倍率 is 979x and shorts are 0.90%, so there is no squeeze fuel. The last two prints after +24% and +29% run-ups closed −16.3% and +3.2%. Source: https://kabutan.jp/disclosures/pdf/20260929/140120260929542242/
  - **Offset, +1.0:** the company raised its forecast at Q3 in both of the last two years, and the plan implies H2 run-rate profit below Q2's. Source: https://tdnet-pdf.kabutan.jp/20260814/140120260814520256.pdf
  - The negative mostly agrees with the baseline lean (−3.0), which already carries the run-up and the margin overhang, so it is not something the baseline missed.

## Baseline, positioning and caveats (every run)

- **No option anchor; positioning substitutes for it.**
  - The JPX short register resolved for all 7 names, but its latest file is dated **2026-09-29**, a week old.
  - 信用倍率 resolved for 6 of 7; 6469 is a buy-only 制度信用 name with no margin shorts.
  - `baseline_quality` is 0.725 on six names and 0.688 on 6469.
  - The lean weights in `lean_components()` are **priors with no Japanese measurement behind them**.
- **`lean_vs_free_control_rho` from the last resolved run (2026-10-02, resolved this session, n=5) is 0.90.** Before that: 10-01 0.60 (n=4), 09-30 0.80 (n=5), 09-29 −0.40 (n=4). On five names this is noise, but 0.9 is close to the 1.0 that would mean the lean is the run-up alone again. Watch it: a stale short register (see above) is one way the positioning terms stop moving and the run-up takes over. 10-02 itself ranked at ρ=0.4, p=0.51 on 5/5 confirmed names.
- **`history` is an estimated cadence: a scale, not a record of dates.** Hunters re-derived the scale from real release dates where they could. 5243: a median of about 13.7% on true dates against a 6.26 proxy. 2734: 2.3 used against a 3.29 proxy.
- **Daily price limits (値幅制限) truncate the tail.** A large finding can be right and still not be paid in full; this matters most for 5243 on a 10% scale.
- **Bars are thin.** No analyst consensus exists for 5243 or 8011. 1377, 2659 and 6469 rest on one broker or one aggregator, kabuyoho/IFIS. 四季報 was unreachable for every hunter. Sizes are capped small for that reason.
- **8011's H1 was pre-released on 08-28.** The stock has fallen about 26% since, partly on two activists selling into the 08-31 buyback. The print turns on whether the full-year plan holds.
- **`pre_lessons` control.**
  - **Changed:** 2659 +0.3→+0.6, 2726 −0.7→−0.3, 2734 −0.2→0.0, 5243 −1.7→−1.2, 8011 +1.1→+1.0.
  - **Unchanged:** 1377 and 6469.
  - LESSONS rule 1 again pulled negatives that rested on public series toward zero.

## What today does NOT establish

Seven names on one day, all small, none above the floor, nothing resolved. One day is not a result, and no ranking claim can be read off it. Resolve with `jp_resolve.py` after the 10-07 close and before TDnet's ~31-day window lapses.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
