# Stage J — Japan ranking for 2026-10-27

**Funnel:** 29 scheduled, 25 eligible, 25 hunted, 25 ranked. Four names were dropped on the ¥15m median-turnover floor.
- **Selection:** `all 25 eligible names (at or under the cap)`. The date-seeded random draw (seed `jp-2026-10-27`) had nothing to cut, because 25 eligible is exactly the cap. No judgement entered the cut.
- **Calendar:** sheets `kessan09_1023` (as of 2026-10-22, 2,920 rows), `kessan08_1002` (as of 2026-10-01, 454 rows) and `kessan` (24 rows). Every hunter re-confirmed its date on kabutan.
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5 (alias timeline); orchestrator flag not recorded.
- **Restart:** the container restarted at about 01:28 UTC. Five hunters in flight (6337, 6988, 7102, 7175, 7309) were lost and re-launched from scratch against the same sealed baselines. No banked hunt was lost.

**Release times**, as each hunter found them (from prior 短信 timestamps or the company's IR calendar, not from a notice for today):
- **Inside the session (3):** 5344 MARUWA at 10:40, 8697 JPX at 12:00 and 4733 OBC at 15:00. These enter at the sealed ~10:06 JST spot.
  - 5344's hunter checked TDnet at 10:17 JST and found no 5344 filing, so the sealed spot is pre-release. The resolver must still check the real TDnet timestamp.
  - The scored file labels every row `amc`. `jp_resolve.py` reads the actual TDnet time and sets the entry basis from that, not from the label.
- **At or after the close (22):**
  - 15:30: 2212, 3911, 4063, 4479, 4684, 4765, 5532, 5911, 6337, 7175, 7309, 7751, 8218, 8892, 9629, 9733, 9782.
  - 15:40: 7102, 9697.
  - 16:00: 4519, 4973, 6988.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7102 | 日本車輌製造 Nippon Sharyo (H1) | **+2.00** (p87) | no | +1.80 | 7.5 | 62 |
| 2 | 6337 | テセック TESEC (H1) | **+1.90** (p85) | no | +1.40 | 7.0 | 60 |
| 3 | 4973 | 日本高純度化学 Japan Pure Chemical (H1) | **+1.00** (p68) | no | +0.84 | 6.0 | 57 |
| 4 | 9782 | ディーエムエス DMS (H1) | **+0.90** (p64) | no | +0.60 | 3.0 | 60 |
| 5 | 9697 | カプコン Capcom (H1) | **+0.70** (p55) | no | +0.45 | 4.5 | 55 |
| 6 | 7309 | シマノ Shimano (Q3) | **+0.45** (p39) | no | +0.27 | 4.5 | 53 |
| 7 | 4765 | SBIグローバルAM (H1) | **+0.30** (p29) | no | +0.09 | 1.5 | 53 |
| 8 | 8892 | エスコン ES-CON Japan (H1) | **+0.30** (p29) | no | +0.14 | 2.3 | 53 |
| 9 | 9733 | ナガセ Nagase Brothers (H1) | **+0.10** (p14) | no | +0.22 | 2.2 | 55 |
| 10 | 7175 | 今村証券 Imamura Securities (H1) | **0.00** (p5) | no | 0.00 | 1.8 | 50 |
| 11 | 4519 | 中外製薬 Chugai (Q3) | **−0.10** (p14) | no | −0.27 | 4.5 | 47 |
| 12 | 4479 | マクアケ Makuake (FY) | **−0.20** (p20) | no | −0.90 | 9.0 | 45 |
| 13 | 5344 | MARUWA (H1) | **−0.20** (p20) | no | −0.15 | 7.5 | 49 |
| 14 | 6988 | 日東電工 Nitto Denko (H1) | **−0.20** (p20) | no | −0.32 | 4.0 | 46 |
| 15 | 8218 | コメリ Komeri (H1) | **−0.20** (p20) | no | −0.09 | 2.3 | 48 |
| 16 | 8697 | 日本取引所G JPX (H1) | **−0.20** (p20) | no | −0.15 | 2.5 | 47 |
| 17 | 9629 | ピー・シー・エー PCA (H1) | **−0.20** (p20) | no | −0.16 | 4.0 | 48 |
| 18 | 2212 | 山崎製パン Yamazaki Baking (Q3) | **−0.25** (p24) | no | −0.21 | 3.5 | 47 |
| 19 | 4684 | オービック OBIC (H1) | **−0.70** (p55) | no | −0.30 | 3.0 | 45 |
| 20 | 4733 | オービックビジネスC OBC (H1) | **−0.70** (p55) | no | −0.32 | 4.0 | 46 |
| 21 | 5532 | リアルゲイト Realgate (FY) | **−0.80** (p59) | no | −0.65 | 6.5 | 45 |
| 22 | 3911 | Aiming (Q3) | **−0.95** (p65) | no | −0.84 | 7.0 | 44 |
| 23 | 5911 | 横河ブリッジHD Yokogawa Bridge (H1) | **−0.95** (p65) | no | −0.22 | 2.2 | 45 |
| 24 | 7751 | キヤノン Canon (Q3) | **−1.30** (p75) | no | −0.50 | 5.0 | 45 |
| 25 | 4063 | 信越化学 Shin-Etsu (H1) | **−1.40** (p77) | no | −0.36 | 4.5 | 46 |

Percentiles are the share of Opus 5.5 reference names with a smaller |value|. They measure size against the model's habit, not rank or probability. `impact_scaled` is the hunter's second, separate measurement and is never the key.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.
- All four members ran on their pinned `-intl-` agents, with no fallback, and covered 25 of 25 names.
- Selection rule `consensus`: 3 of 4 judges in their own top 20% on the panel's side.
- Each judge's own top 20% starts at: opus5 |1.60|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.32| (148 live sizes each).

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7102 | **yes** | 93 | long | 4 | 91L* | 97L* | 97L* | 88L* | 4 | +2.43 | +2.00 |
| 2 | 6337 | **yes** | 94 | long | 3 | 96L* | 96L* | 94L* | 88L* | 4 | +2.40 | +1.90 |
| 3 | 3911 | **yes** | 89 | short | 6 | 96S* | 88S* | 80S* | 90S* | 4 | −1.93 | −0.95 |
| 4 | 5532 | **yes** | 86 | short | 3 | 90S* | 82S* | 84S* | 89S* | 4 | −1.54 | −0.80 |
| 5 | 4479 | **yes** | 81 | short | 10 | 65S | 88S* | 78S | 90S* | 3 | −1.40 | −0.20 |
| 6 | 7751 | **yes** | 82 | short | 12 | 100S* | 80S | 66S | 82S* | 3 | −1.25 | −1.30 |
| 7 | 4733 | | 78 | short | 9 | 89S* | 68S | 71S | 85S* | 2 | −1.19 | −0.70 |
| 8 | 5344 | | 76 | short | 11 | 88S* | 79S | 59S | 79S | 2 | −1.13 | −0.20 |
| 9 | 4684 | | 78 | short | 14 | 96S* | 72S | 59S | 84S* | 2 | −1.11 | −0.70 |
| 10 | 9697 | | 73 | long | 4 | 77L | 67L | 71L | 76L | 2 | +0.97 | +0.70 |
| 11 | 4063 | | 78 | short | 9 | 91S* | 72S | 78S | 69S | 2 | −0.96 | −1.40 |
| 12 | 6988 | | 64 | short | 15 | 83S* | 66S | 42S | 66S | 1 | −0.72 | −0.20 |
| 13 | 4973 | | 62 | long | 20 | 91L* | 68L | 49L | 38L | 1 | +0.64 | +1.00 |
| 14 | 2212 | | 63 | short | 15 | 89S* | 49S | 57S | 58S | 1 | −0.58 | −0.25 |
| 15 | 9782 | | 69 | long | 5 | 72L | 72L | 71L | 61L | 0 | +0.84 | +0.90 |
| 16 | 9629 | | 63 | short | 8 | 69S | 49S | 66S | 69S | 0 | −0.75 | −0.20 |
| 17 | 5911 | | 48 | short | 13 | 69S | 49S | 42S | 34S | 0 | −0.47 | −0.95 |
| 18 | 8697 | | 46 | short | 12 | 65S | 36S | 45S | 38S | 0 | −0.45 | −0.20 |
| 19 | 4519 | | 30 | short | 29 | 55S | 36S | 18L | 49S | 0 | −0.42 | −0.10 |
| 20 | 4765 | | 35 | long | 16 | 60L | 17L | 35L | 29L | 0 | +0.28 | +0.30 |
| 21 | 8892 | | 28 | long | 20 | 60L | 4L | 22L | 24L | 0 | +0.22 | +0.30 |
| 22 | 8218 | | 26 | short | 12 | 47S | 17S | 18S | 24S | 0 | −0.22 | −0.20 |
| 23 | 7309 | | 3 | short | 20 | 20S | 4S | 18S | 29L | 0 | −0.14 | +0.45 |
| 24 | 9733 | | 1 | short | 1 | 3S | 2S | 0- | 0- | 0 | −0.03 | +0.10 |
| 25 | 7175 | | 0 | – | 0 | 0- | 0- | 0- | 0- | 0 | 0.00 | 0.00 |

`*` marks a judge's own top 20%. The panel selects 6 names: 2 long and 4 short.

**Selected names**
- **7102 Nippon Sharyo, long, 4 of 4.**
  - The case: Q1 ordinary profit was already 33.8% of the 9,300m plan, against a 19.2% five-year Q1 average. The April 短信 says the −24% guide was cut purely as a Middle East buffer from a flat-profit view. The company raised at or before H1 in 2021, 2022, 2023 and 2025, and the stock went +13.5% and +14.7% on the last two raises.
  - The case against: it held the plan at Q1 with the same progress rate and fell 10.4%. kabutan listed it on two upgrade lists (10/18, 10/25). The margin long is crowded at 7.91x.
- **6337 TESEC, long, 4 of 4.**
  - The case: Q1 operating profit is 37.5% of a plan raised in July, Q1 orders were +116%, and the plan needs only about 229m a quarter from here. Each of the last three raises was bought +10.6%, +11.3% and +14.5%.
  - The case against: part of it traded on 10/26 (+6.9% on 2–3× volume after kabutan's 10/25 upgrade list), and Q1 may have carried one-off high-margin projects.
- **3911 Aiming, short, 4 of 4.**
  - The case: what this print adds is the first FY2026 forecast and so a Q4 guide. That guide likely carries the hololive mahjong launch cost and a decaying Inazuma, after a +25% run on the 10/09 hololive news. The last three guides were sold −7.7%, −7.9% and −9.8%.
  - The case against: that is inference, not a document. The company has beaten its own operating-profit guide 6 of 6 times, Inazuma re-entered the top 20 on 10/14, and 3.69% of disclosed shorts sit in the register.
- **5532 Realgate, short, 4 of 4.**
  - The case: the FY27 +40% operating-profit path was already said on the Q3 call. Ordinary profit and EPS will trail operating profit after a 13% share raise. The last four prints all fell (−11.6%, −8.0%, −2.3%, −9.7%) into a buy-only margin long of about 6% of shares.
  - The case against: an FY27 guide well above +40% would flip it.
- **4479 Makuake, short, 3 of 4.**
  - The case: the first FY9/27 guide comes with a new mid-term plan. The company has written that it guides only on high-certainty assumptions and will keep investing upfront. Last year's investment-led guide fell 27.5%.
  - The case against: a more ambitious new mid-term plan is a real offset. The hunter's own findings net to only −0.2, so the panel sized this evidence much larger than the hunter did.
- **7751 Canon, short, 3 of 4.**
  - The case: the July plan assumed Middle East normalisation from October, and Brent has been 104–117 against 88–90 when it was set. CIPA shipments slowed and Q4 memory costs are above plan. A buyback is unlikely after the ¥200bn programme finished early. The stock outran the Nikkei by about 13 points and sits above the consensus target.
  - The case against: Q3 currency ran about ¥5bn of operating profit above the plan rates, and the street (IFIS 462.4bn) already sits below plan, so a held forecast could read as relief. Opus 5 alone put it at its own 100th percentile; Sonnet 5.5 at 66.

**Where the panel and the hunters disagree most**
- **4479:** the hunter netted −0.2 and the panel selected it short at 81. The scaled number (−0.90) sides with the panel.
- **4973:** the hunter has it third at +1.00; the panel is long but weak (62, only Opus 5 in its top 20%).
- **4063:** the hunter's bottom name at −1.40; the panel is short at 78 but not selected (only Opus 5 in its top 20%).
- **Opposite signs:** 7309 (hunter +0.45, panel short at 3) and 9733 (hunter +0.10, panel short at 1). Both are negligible on both scales.
- No name is above the conviction floor, so there is no floor-cleared name the panel failed to select.

**What these numbers are not**
- `panel_score` ranks; it does not forecast. There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales rest on 148 live sizes each, still well short of the ~200 Japanese panel names they need.
- In the four-model re-judge the judges ranked Japan and Australia *worse* than the live hunt (ρ −0.25 to −0.31 on 29 names). Nothing about this market's panel is established.

## Top and bottom name

- **Top, 7102 Nippon Sharyo (+2.00).** The driving finding (guidance, +2.5): Q1 ordinary profit is 33.8% of the full-year plan against a 19.2% Q1 average, and the April guide was cut from a flat view only as a Middle East buffer. Source: the FY3/26 決算短信, https://tdnet-pdf.kabutan.jp/20260424/140120260423509254.pdf, with the Q1 deck at https://www.n-sharyo.co.jp/finance/198R8-qtr1setumei.pdf.
- **Bottom, 4063 Shin-Etsu Chemical (−1.40).** The driving finding (guidance, −0.8): Shin-Etsu has held its forecast at each of the last three Q2 prints and fell after each (Oct 2024 −2.9%, Oct 2025 −3.7%). IFIS consensus operating profit (732.2bn) sits 4.6% above the 700bn guide, and currency gives no room for a raise (plan ¥160/$ against Jul–Sep 160.1 / 157.4 / 156.9). Source: https://kabutan.jp/stock/finance?code=4063.
  - The other negatives are small: PVC weakness at Shintech (snippet only), GlobalWafers −13.1% September revenue, and positioning (margin ratio 18.4).
  - One positive: Shin-Etsu Polymer's 10/26 raise on wafer-container demand.

**Not ranked:** none. All 25 are rankable and no hunter disputed the event.

## What this market's numbers need beside them

- **No option anchor.** It is substituted by `positioning`: JPX's disclosed short register (file 20261026, 575 codes, read for all 25 names) and 信用倍率.
  - 18 of 25 names carry a margin ratio. The other 7 are buy-only on margin or unscraped (3911, 4479, 4973, 5532, 7175, 9733, 9782), and their baselines run at `anchor_quality` 0.45 against 0.6.
  - The weights in `lean_components()` are priors with no Japanese measurement behind them.
  - The 6337 hunter flags a structural artefact. Its 1,103x margin ratio comes from a buy-only listing, not a crowded long, so most of its −1.34 baseline lean is not information.
- **`lean_vs_free_control_rho`, last resolved run.** 2026-10-23, resolved this morning: −0.071 on 8 names. Earlier runs read −1.0 (10-22, 3 names), 0.5 (10-21, 3 names), 0.4 (10-20) and 0.531 (10-15, 25 names). It has not climbed back toward 1.0, so the lean is not the run-up alone.
- **10-23 resolved this morning:** impact_sum ρ +0.335 (p 0.40) against the free control's +0.571, with signs right on 4 of 8. One day.
- **`history` is an estimated cadence, a scale and not a record of dates.** Six hunters found the baseline's estimated reaction dates 1–5 days off the real release dates (4684, 4733, 5911, 8697, 9629, 3911) and measured reactions on the real dates instead.
- **Daily price limits (値幅制限) truncate the tail.** A large finding can be right and still not be paid in full.
- **Signs:** 9 positive, 1 zero, 15 negative. The first resolved days were five of seven negative. Here too the hunters lean negative, though LESSONS rules 1 and 2 pulled most negatives toward zero; the pre-lessons drafts were more negative still.
- **Conviction floor (2.8):** no name clears it. The largest is 7102 at +2.00. Over the whole US sample the sign was a coin flip below the floor, and every name here is below it.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
