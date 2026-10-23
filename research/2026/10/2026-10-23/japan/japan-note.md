# Stage J — Japan ranking for 2026-10-23

**Funnel:** 14 scheduled, 9 eligible, 9 hunted, 8 ranked. Five names were dropped on the ¥15m median-turnover floor: 9029 ヒガシHD (¥11.0m), 9353 櫻島埠頭 (¥1.8m), 2268 B-R サーティワン (¥7.7m), 3912 モバイルファクトリー (¥14.1m) and 7422 東邦レマック (¥6.9m).
- **Selection:** `all 9 eligible names (at or under the cap)`. The date-seeded random draw (seed `jp-2026-10-23`) had nothing to cut, so no judgement entered the cut.
- **Calendar:** sheets `kessan09_1016` (as of 2026-10-15), `kessan08_1002` (2026-10-01) and `kessan` (8 rows).
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5; orchestrator claude-opus-5-5.

**Release times**, as each hunter found them (all inferred from prior 短信 timestamps, none from a notice for today):
- **Inside the session (4):** 5423 at 14:00, 2804, 7931 and 8707 at 15:00. These enter at the sealed 10:05 JST spot.
- **At or after the close (4):** 6954, 6999 and 8961 at 15:30, 3492 at 16:00. These are measured from the 10-23 close to the 10-26 close.
- 6629 has no release today (see below).

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6999 | KOA (H1) | **+2.20** (p89) | no | +1.44 | 9.0 | 58 |
| 2 | 6954 | ファナック (H1) | **+1.60** (p81) | no | +0.44 | 5.5 | 54 |
| 3 | 7931 | 未来工業 (H1) | **+1.30** (p75) | no | +0.61 | 3.8 | 58 |
| 4 | 5423 | 東京製鐵 (H1) | **+0.90** (p63) | no | +0.15 | 2.5 | 53 |
| 5 | 2804 | ブルドックソース (H1) | **0.00** (p5) | no | −0.12 | 2.0 | 47 |
| 6 | 3492 | MIRARTH REIT (Aug-26 period) | **−0.05** (p10) | no | −0.05 | 0.8 | 47 |
| 7 | 8961 | 森トラストリート (Aug-26 period) | **−0.05** (p10) | no | −0.05 | 1.3 | 48 |
| 8 | 8707 | 岩井コスモHD (H1) | **−0.10** (p14) | no | +0.00 | 2.2 | 50 |

3492 and 8961 tie on the key; their order is the scorer's tie-break and means nothing.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran on their pinned `-intl-` agents, with no fallback. Selection rule `consensus`: 3 of 4 judges in their own top 20% on the panel's side. Own top 20% starts at opus5 |1.60|, opus55 |0.96|, sonnet55 |1.08|, fable51 |1.33| (135 live sizes each).

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6999 | **yes** | 93 | long | 3 | 98L* | 92L* | 90L* | 91L* | 4 | +2.21 | +2.20 |
| 2 | 6954 | no | 75 | long | 8 | 78L | 87L* | 73L | 63L | 2 | +1.13 | +1.60 |
| 3 | 7931 | no | 71 | long | 9 | 78L | 82L* | 69L | 57L | 2 | +0.97 | +1.30 |
| 4 | 3492 | no | 42 | short | 12 | 55S | 51S | 24S | 37S | 0 | −0.51 | −0.05 |
| 5 | 5423 | no | 39 | long | 24 | 47L | 73L | 11L | 24L | 0 | +0.41 | +0.90 |
| 6 | 8961 | no | 36 | short | 10 | 50S | 37S | 24S | 30S | 0 | −0.31 | −0.05 |
| 7 | 2804 | no | 18 | long | 38 | 19S | 51L | 62L | 22S | 0 | +0.17 | 0.00 |
| 8 | 8707 | no | 1 | short | 3 | 3S | 4S | 3L | 0- | 0 | −0.04 | −0.10 |

**Selected: 6999 KOA, long (k = 4, panel_pct 93).**
- **What the judges rest on:** all four lean on the hunter's first finding. Q1 book-to-bill was 1.18 and the backlog ¥17.4bn, so the raised H1 guide needs only ¥22.1bn of Q2 sales. Yageo's September revenue (+4.5% m/m, +46% y/y) points the same way from an independent source. KOA raised at four of its last five prints, with next-session moves of +17.3, +22.2, −4.5 and +11.6, and a raise lifts the dividend through the 30% payout. Judge sizes: Opus 5 +3.6, Fable 5.1 +2.4, Opus 5.5 +1.9, Sonnet 5.5 +1.8.
- **The strongest case against:**
  - The 28% fall since 10-06 is sector beta (Murata, Taiyo Yuden, ROHM and Yageo fell 8–11% on 10-15), so the passive-component tape can override the print.
  - 信用倍率 23.85 is a crowded, underwater margin long that sells into strength.
  - FX has moved against the H2 assumptions (USD 159 / EUR 185 planned against about 156 / 175), which gives management a reason to hold.
  - The street bar is unsourced; the company plan is the only bar.
  - Disclosed shorts rose 0.14pt to 1.15%.

**Where the panel and the hunter disagree most.**
- **3492 MIRARTH:** the hunter is near zero (−0.05), but every judge sized the reserve-funded first Aug-2027 DPU guide more negatively (Opus 5 −0.9, Fable 5.1 −0.48, Opus 5.5 −0.5). The panel ranks it 4th, the hunter 6th.
- **5423 Tokyo Steel:** the hunter's +0.90 rests on a buyback option with the guide pre-released. The judges split widely on it, with a spread of 24.
- **2804 Bull-Dog:** split by sign, with Opus 5 and Fable 5.1 short and Opus 5.5 and Sonnet 5.5 long (sd 38).
- No name sits above the conviction floor, so there is no floor-clearer the panel skipped.

**What the numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- In the four-model re-judge the judges ranked Japan *worse* than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.

## What drives the top and bottom

**Top, 6999 KOA (+2.20).**
- **The main finding (+2.0, guidance; range −2.0 to +8.0):** the backlog and book-to-bill arithmetic above makes an H1 beat and a further FY raise more likely than a hold. Source: https://tdnet-pdf.kabutan.jp/20260723/140120260722597196.pdf, independent: https://winvest.tw/News/Detail/95386.
- **Smaller findings:**
  - Falling silver and palladium against a ¥3.1bn precious-metal headwind in the July bridge (+0.7).
  - Adverse FX (−0.5).
  - The Taicang relocation gain is already in the forecast (0.0).

**Bottom, 8707 IwaiCosmo (−0.10).**
- **The only non-zero finding (−0.1):** the 10-16 disclosure of a vendor-side leak of 4,611 customers' names and e-mails. Source: https://tdnet-pdf.kabutan.jp/20261016/140120261016552374.pdf.
- **Everything else is pre-released:**
  - H1 went out to the million yen on 10-16 (https://tdnet-pdf.kabutan.jp/20261016/140120261015551021.pdf).
  - The 65-yen interim dividend was pre-announced on 09-18.
  - The company publishes no full-year forecast, so there is nothing to revise.
- This is a near-zero, not a short.

**Names that could not be ranked:**
- **6629 テクノホライゾン** has no event in the window. A TDnet notice of 2026-10-16 moved its H1 results to 2026-10-30, to consolidate two acquired companies for the first time (https://tdnet-pdf.kabutan.jp/20261016/140120261014550849.pdf). The JPX sheet the universe read is dated 2026-10-01, before the change.
- The hunter returned no findings and the scorer left 6629 unranked. The sealed baseline is unchanged; a retrospective `event_occurred: false` belongs to the resolve.

## Standing caveats

- **No option anchor; substituted by positioning.**
  - JPX short register (as of 2026-10-22): 2804 1.48% (two sellers, flat), 3492 0.87% (covering slightly), 6999 1.15% (building, +0.14pt). The other six are absent from the register, a real zero truncated at 0.5%.
  - 信用倍率 resolved for all nine. Crowded longs: 3492 543, 6999 23.85, 6954 21.41, 8707 7.84. Short-heavy: 7931 0.45, 2804 0.65.
  - `baseline_quality` read 0.60 on all nine, against 0.725 on the 2026-09-11 universe.
  - The lean's component weights are **priors** with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`:** the last resolved runs are 10-19 (0.2) and 10-20 (0.4), and 10-15 (25 names) read 0.531. It has not climbed back toward 1.0, so the positioning sources are still resolving. 10-21 and 10-22 are not yet resolved.
- **`history` is an estimated cadence**: a scale for how much the name moves, not a record of dates. The 6954 hunter found it puts several reactions on the wrong dates (−4.53% shown where the real Q1 reaction was −14.31%), so no date in it is cited here as a fact.
- **Signs on the key:** 4 positive, 1 exactly zero, 3 negative, all three negatives at or below 0.10 in size. The first resolved days were five of seven negative.
- **Conviction floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign below the floor was a coin flip.
- **Price limits:** the daily 値幅制限 truncates the tail. That matters most for KOA, whose 9% scale and +17/+22% raise reactions sit near a limit move.
- **One day is not a result.** Eight names on one day establish nothing about whether these companies can be ranked; ρ comes only from pooled resolved days.

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._
