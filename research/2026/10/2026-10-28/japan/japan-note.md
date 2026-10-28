# Stage J — Japan ranking for 2026-10-28

**Funnel:** 46 scheduled, 39 eligible, 25 hunted, 25 ranked. Seven names were dropped on the ¥15m median-turnover floor.
- **Selection:** `random sample of 39 eligible, seed 'jp-2026-10-28'`. The draw was random among the 39 eligible names and capped at 25; no judgement entered the cut. The 14 eligible names not drawn are in `universe.json` `eligible_codes`.
- **Calendar:** sheets `kessan09_1023` (as of 2026-10-22, 2,920 rows), `kessan08_1002` (as of 2026-10-01, 454 rows) and `kessan` (43 rows). The universe header reports `calendar_as_of` 2026-10-01 (the oldest sheet); every hunter re-confirmed its date on kabutan.
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5 (alias timeline); orchestrator flag not recorded.
- **Short register:** JPX file of 2026-10-27 (626 codes). 信用倍率 resolved for 21 of 25 names; 3850, 4832, 6382 and 9115 have none (two are margin-buy-only names).

**Release times**, as each hunter found them (from prior 短信 timestamps or the company IR calendar; a notice for today was seen only for 4373):
- **Inside the session (13)** — these enter at the sealed ~10:08 JST spot: 9932 11:00; 3003, 4956, 8628 11:30; 8595, 8914 12:00; 3778 12:30; 1930, 6023, 9115 13:00; 6382, 7276, 7283 15:00.
  - 4956 was already +6.3% on heavy volume at the seal with no news found; its hunter filed that as a positioning negative.
- **At or after the close (12):** 15:30 for 2002, 2664, 2760, 3850, 4373, 4832, 6501, 6526, 6701, 6807, 8871; 15:45 for 3771.
- The scored file labels every row `amc`. `jp_resolve.py` reads the actual TDnet time and sets the entry basis from that, not from the label.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2664 | カワチ薬品 Cawachi (H1) | **+1.70** (p84) | no | +0.46 | 3.8 | 56 |
| 2 | 7276 | 小糸製作所 Koito (H1) | **+1.60** (p82) | no | +0.64 | 4.0 | 58 |
| 3 | 8914 | エリアリンク Arealink (Q3) | **+1.20** (p74) | no | +0.24 | 3.0 | 54 |
| 4 | 3778 | さくらインターネット Sakura Internet (H1) | **+0.90** (p64) | no | +0.54 | 9.0 | 53 |
| 5 | 6382 | トリニティ工業 Trinity Industrial (H1) | **+0.80** (p60) | no | +0.34 | 2.8 | 56 |
| 6 | 2760 | 東京エレクトロン デバイス TED (H1) | **+0.70** (p55) | no | +0.48 | 4.0 | 56 |
| 7 | 9115 | 明海グループ Meiji Shipping (H1) | **+0.70** (p55) | no | +0.50 | 5.0 | 55 |
| 8 | 9932 | 杉本商事 Sugimoto (H1) | **+0.70** (p55) | no | +0.21 | 3.5 | 53 |
| 9 | 6501 | 日立製作所 Hitachi (H1) | **+0.50** (p44) | no | +0.44 | 5.5 | 54 |
| 10 | 6701 | 日本電気 NEC (H1) | **+0.50** (p44) | no | +0.24 | 6.0 | 52 |
| 11 | 1930 | 北陸電気工事 Hokuriku Electrical Construction (H1) | **+0.40** (p36) | no | -0.30 | 5.0 | 47 |
| 12 | 2002 | 日清製粉グループ本社 Nisshin Seifun (H1) | **+0.40** (p36) | no | +0.10 | 2.5 | 52 |
| 13 | 7283 | 愛三工業 Aisan (H1) | **+0.40** (p36) | no | +0.30 | 3.8 | 54 |
| 14 | 3003 | ヒューリック Hulic (Q3) | **+0.30** (p29) | no | +0.24 | 3.0 | 54 |
| 15 | 4373 | シンプレクス HD Simplex (H1) | **+0.30** (p29) | no | +0.32 | 4.0 | 54 |
| 16 | 6526 | ソシオネクスト Socionext (H1) | **+0.20** (p20) | no | -0.42 | 7.0 | 47 |
| 17 | 8628 | 松井証券 Matsui Securities (H1) | **+0.10** (p14) | no | +0.08 | 2.0 | 52 |
| 18 | 4956 | コニシ Konishi (H1) | **0.00** (p5) | no | -0.24 | 4.0 | 47 |
| 19 | 8595 | ＪＡＦＣＯ (H1) | **0.00** (p5) | no | -0.09 | 2.3 | 48 |
| 20 | 3771 | システムリサーチ System Research (H1) | **-0.20** (p20) | no | -0.10 | 2.6 | 48 |
| 21 | 3850 | イントラマート Intramart (H1) | **-0.20** (p20) | no | -0.06 | 3.2 | 49 |
| 22 | 4832 | ＪＦＥシステムズ JFE Systems (H1) | **-0.20** (p20) | no | -0.33 | 5.5 | 47 |
| 23 | 6807 | 日本航空電子工業 JAE (H1) | **-0.50** (p44) | no | -0.90 | 5.0 | 41 |
| 24 | 8871 | ゴールドクレスト Goldcrest (H1) | **-0.50** (p44) | no | -0.20 | 2.5 | 46 |
| 25 | 6023 | ダイハツインフィニアース Daihatsu Infinearth (H1) | **-1.00** (p69) | no | -0.36 | 6.0 | 47 |

Brackets are the percentile of |impact_sum| among Opus 5.5 reference names (n=674): a scale, not a rank. `impact_scaled` is the hunter's second, separate measurement and is not the key.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing.** All four members ran as their pinned `panel-judge-intl-*` agents, no fallback, 25/25 coverage each. Selection is the market rule, 3 of 4 judges in their own top 20% on the panel's side. Each judge's top 20% currently starts at |1.80| (Opus 5), |1.00| (Opus 5.5), |1.00| (Sonnet 5.5) and |1.44| (Fable 5.1), read against 173 live JP sizes each.

```
rank ticker   sel pct side    sd  members (own percentile, L/S)                             k  score  impact_sum
   1 6807     yes  94 short    5  opus5: 87S* opus55: 92S* sonnet55: 99S* fable51: 96S*  4  -2.09  -0.50
   2 4832     yes  76 short    7  opus5: 64S  opus55: 80S* sonnet55: 81S* fable51: 79S   3  -1.08  -0.20
   3 6526          78 short    5  opus5: 85S* opus55: 75S  sonnet55: 71S  fable51: 79S   2  -1.10  +0.20
   4 6023          73 short    9  opus5: 78S  opus55: 79S  sonnet55: 57S  fable51: 79S   1  -1.10  -1.00
   5 3778          70 long    14  opus5: 49L  opus55: 70L  sonnet55: 88L* fable51: 71L   1  +0.87  +0.90
   6 2664          62 long    14  opus5: 50L  opus55: 79L  sonnet55: 46L  fable51: 73L   0  +0.80  +1.70
   7 7276          64 long     5  opus5: 68L  opus55: 64L  sonnet55: 69L  fable51: 56L   0  +0.70  +1.60
   8 2760          61 long     3  opus5: 58L  opus55: 66L  sonnet55: 61L  fable51: 58L   0  +0.68  +0.70
   9 6501          42 long     9  opus5: 41L  opus55: 56L  sonnet55: 40L  fable51: 31L   0  +0.43  +0.50
  10 6382          41 long     6  opus5: 33L  opus55: 40L  sonnet55: 48L  fable51: 43L   0  +0.41  +0.80
  11 8871          37 short    4  opus5: 39S  opus55: 32S  sonnet55: 34S  fable51: 43S   0  -0.36  -0.50
  12 8595          38 short   10  opus5: 36S  opus55: 26S  sonnet55: 38S  fable51: 53S   0  -0.36   0.00
  13 8914          30 long    13  opus5:  8L  opus55: 39L  sonnet55: 39L  fable51: 32L   0  +0.35  +1.20
  14 6701          34 long    11  opus5: 38L  opus55: 30L  sonnet55: 48L  fable51: 19L   0  +0.34  +0.50
  15 4956          26 short   26  opus5: 34S  opus55: 28S  sonnet55: 15L  fable51: 56S   0  -0.30   0.00
  16 3850          28 short    9  opus5: 33S  opus55: 28S  sonnet55: 13S  fable51: 36S   0  -0.28  -0.20
  17 1930          13 short   34  opus5: 27S  opus55: 45L  sonnet55: 28S  fable51: 43S   0  -0.25  +0.40
  18 9115          18 long    22  opus5: 14S  opus55: 17L  sonnet55: 48L  fable51: 19L   0  +0.21  +0.70
  19 3003          19 long    10  opus5:  8L  opus55: 26L  sonnet55: 32L  fable51: 12L   0  +0.18  +0.30
  20 3771          20 short   10  opus5: 14S  opus55: 11S  sonnet55: 16S  fable51: 36S   0  -0.17  -0.20
  21 9932           6 short    6  opus5:  6S  opus55:  4L  sonnet55:  7S  fable51: 14S   0  -0.10  +0.70
  22 7283          11 long    13  opus5:  2S  opus55: 17L  sonnet55: 28L  fable51:  0-   0  +0.09  +0.40
  23 8628           5 short    3  opus5:  9S  opus55:  2S  sonnet55:  4S  fable51:  7S   0  -0.07  +0.10
  24 4373          10 long    19  opus5:  9S  opus55:  5S  sonnet55: 40L  fable51: 14L   0  +0.03  +0.30
  25 2002           8 short   15  opus5:  6S  opus55:  5L  sonnet55:  4L  fable51: 32S   0  -0.02  +0.40
```

`pct` is `panel_pct` (0-100, size of the mean of the four signed own-percentiles), `side` its direction, `sd` the spread, `*` a member in its own top 20%, `k` the consensus count, `score` the old `panel_score`.

**6807 JAE — selected, short, 4 of 4.** Every judge's note names the same evidence: JAE revises only at the H1 print and has cut there in two of the last three years (last year's cut, OP ¥18.5bn → ¥10.0bn, was limit-down, −17.8%); Q1 OP was ¥327m against an H1 plan of ¥3.8bn (ordinary progress 9.9% against a 38.9% five-year average); and IFIS consensus (OP ¥10,676m) sits about 12% above the company's ¥9,500m OP plan (ordinary ¥10,588m against ¥8,500m, 25% above), so even a held guide lands under the street (https://kabuyoho.jp/report?bcode=6807). The stock has fallen after each of its last seven prints. Strongest case against: Simplex holds 14.87% and was still buying on 10/16 after the weak Q1, and Kyocera's 33% is under a standstill, so roughly 48% of votes are locked up; the yen (~158) is weaker than the plan's 153; and the hunter netted these into −0.5 where the judges put −1.8 to −4.3.

**4832 JFE Systems — selected, short, 3 of 4 (Opus 5 at 64S missed its own top 20%).** The judges name the guidance risk: Q1 OP ¥802m was 12.2% of the ¥6.6bn plan (ordinary 13.0% against a five-year 21.3%), orders −12.7% and backlog −9.9%, and the company cut at last year's Q2 print for −11.5% (https://tdnet-pdf.kabutan.jp/20260729/140120260729501921.pdf). There is no IFIS consensus and no margin short side. Strongest case against: the plan was back-loaded on purpose (the interim dividend was cut 28→22 yen in April, implying a weak H1 by design), the company called Q1 on plan, and last year it ended up beating its initial guide despite the cut.

**Where panel and hunter disagree most:**
- 6807: hunter −0.50 (rank 23 of 25), panel 94 short and the day's strongest selection. The hunter's +1.0 Simplex lock-up finding offset a −2.0 cut finding; no judge gave that offset as much weight.
- 6526 Socionext: hunter +0.20, panel 78 short (2 of 4). Judges sized the FX "upward revision" as landing at or below an IFIS number already ~30% over plan, with the last three H1 prints at −6.5%, −14.9%, −20.1%.
- 1930, 9932, 2002: hunter mildly positive, panel mildly short; all small.
- 8914 Arealink: hunter +1.20 (rank 3), panel only 30 long.
- No name sits above the 2.8 conviction floor, so there is no above-floor disagreement.

What the panel numbers are not: `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the member scales are 173 live JP sizes per judge plus the frozen E-P seed until this market has about 200 panel names of its own; and in the four-model re-judge the judges ranked Japan and Australia **worse** than the live hunt (ρ −0.25 to −0.31 on 29 names), so nothing about this market's panel is established.

## Top and bottom name

- **Top, 2664 Cawachi (+1.70).** Most of it is a +1.0 guidance finding. Cawachi has revised its full-year forecast at the H1 print in each of the last three years, in the direction of the H1 gap (2023 up 16.7%, +3.98% next day: https://f.irbank.net/pdf/20231026/140120231026571929.pdf). Q1 ordinary profit was 48.9% of the H1 plan against 40–42% in the two prior years, and the full-year plan implies H2 OP −41% (https://tdnet-pdf.kabutan.jp/20260729/140120260727500251.pdf). No analyst coverage, no 月次. Against it: the stock is up 38% since the plan and sold its Q1 beat (−1.7% next day). The panel has it at 62 long and did not select it.
- **Bottom, 6023 Daihatsu Infinearth (−1.00).** The largest item is −0.7 of positioning: a 29.8x margin long into a −10% theme drawdown, and the last two H1 prints with the plan held fell 5–7% (https://kabutan.jp/stock/news?code=6023). Next is −0.5: the company filed a 業績予想の修正 about a week before the H1 print in 2020, 2021, 2022 and 2025 and has filed none this year, so H1 probably lands inside the plan (https://irbank.net/6023/ir). Against it: Q1 OP was 22.9% of the raised FY plan, ahead of its own seasonality. The panel has it at 73 short (1 of 4).

## Names that could not be ranked

None. All 25 hunts confirmed their event, and `edge_score.py` ranked 25 of 25.

## What every note must say

- **Positioning substitute, not an option anchor.** Japan has no liquid single-stock options, so `options` is null. The baseline's `priced_lean_pct` and `anchor_quality` come from JPX's short register (level and change) and 信用倍率. Today the register named a position at or above 0.5% for 5 of 25 names (2664, 3003, 3771, 3778, 6526; none above 1.65%); the rest are true zeros. Margin ratio resolved for 21 of 25.
- **The weights in `lean_components()` are priors** with no Japanese measurement behind them; `jp_resolve.py` ranks each component separately.
- **`lean_vs_free_control_rho`, last two resolved runs:** 2026-10-26 (resolved this morning) **0.70 on 5 names**, with `short_squeeze` and `short_building` unrankable because none of the five carried a register position; 2026-10-23 −0.071 on 8. Five names is noise, but 0.70 is the direction to watch: when the register is empty the lean is mostly margin overhang and run-up, and it drifts back toward the free control. The 10-26 day itself: impact_sum ρ 0.0 (p 1.0), free control 0.4, sign right 1 of 5.
- **`history` is an estimated cadence**, a scale and not a record of dates. Five hunters (2002, 6023, 6526, 8628, 9115) found the baseline's cadence dates wrong against the real release dates and recomputed reactions from Yahoo bars; none of those dates is cited as fact.
- **Signs:** 17 positive, 2 zero, 6 negative. That is the reverse of the first resolved days (five of seven negative). The panel leans the other way: 13 of 25 names on the short side, and both selections short.
- **Conviction floor:** no name clears 2.8 (largest |impact_sum| 1.70). Over the whole US sample the sign was a coin flip below the floor, so every row here sits in the regime where the key has not shown direction.
- **Price limits:** the daily 値幅制限 truncates large moves, so a large finding (6807's limit-down precedent is the obvious case) can be right and still not be paid in full in the window.
- **No release-time notice:** 13 names release inside the session and are measured from the sealed spot; the release times are inferred from prior prints.
- **One day is not a result.** 25 names, no name above the floor, a panel whose re-judge ranked Japan worse than the hunt.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
