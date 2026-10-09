# Stage J — Japan ranking for 2026-10-09

This is research only and no orders are placed. The ranking key is `impact_sum`, as `edge-scores.json` reports it: points of spot, signed. There is no call and no threshold label.

**Funnel:** 65 scheduled, 31 eligible, 25 hunted. 34 names fell below the ¥15m median-turnover floor.
- `selection.method`: *random sample of 31 eligible, seed `jp-2026-10-09`*. The cap is 25, so the draw was random among the eligible names. The six eligible names it left out are 2157, 4187, 6136, 6668, 8570 and 9381. That is a draw, not a judgement.
- JPX sheets read: kessan08_1002 and kessan09_1002, `calendar_as_of` 2026-10-01.
- Prompt version `jp.v6`. Hunters ran on claude-opus-5-5, per the alias timeline.
- Baselines were sealed at about 10:10 JST.
- **2026-10-12 is スポーツの日.** For an after-close release the exit is the **2026-10-13** close, a three-day weekend.

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7713 | シグマ光機 (Q1) | **+1.60** | +0.48 | 4.0 | 56 | **15:00, in session** | sealed spot |
| 2 | 6506 | 安川電機 (H1) | **+1.50** | +0.98 | 7.0 | 57 | 16:00 | close 10-09 |
| 3 | 8244 | 近鉄百貨店 (H1) | **+1.40** | +0.50 | 2.5 | 60 | 15:30 | close 10-09 |
| 4 | 6814 | 古野電気 (H1) | **+1.20** | +0.80 | 5.0 | 58 | 15:30 | close 10-09 |
| 5 | 6289 | 技研製作所 (FY) | **+1.10** | +0.48 | 6.0 | 54 | 15:30 | close 10-09 |
| 6 | 7888 | 三光合成 (Q1) | **+0.80** | +0.48 | 4.8 | 55 | 15:30 | close 10-09 |
| 7 | 8200 | リンガーハット (H1) | **+0.60** | +0.48 | 3.0 | 58 | 15:30 | close 10-09 |
| 8 | 2735 | ワッツ (FY) | **+0.40** | +0.14 | 3.5 | 52 | 15:30 | close 10-09 |
| 9 | 3201 | 日本毛織 (Q3) | **+0.30** | +0.20 | 2.0 | 55 | **15:00 (inferred), in session** | sealed spot |
| 10 | 4992 | 北興化学工業 (Q3) | **+0.25** | −0.13 | 3.3 | 48 | 15:30 | close 10-09 |
| 11 | 2698 | キャンドゥ (H1) | **+0.20** | +0.08 | 2.0 | 52 | 15:30 (inferred) | close 10-09 |
| 12 | 3046 | ジンズHD (FY) | **+0.10** | −0.34 | 8.5 | 48 | 16:00 | close 10-09 |
| 13 | 8008 | ヨンドシーHD (H1) | **+0.05** | 0.00 | 1.6 | 50 | 15:30 | close 10-09 |
| 14 | 3501 | SUMINOE (Q1) | **−0.05** | −0.08 | 2.0 | 48 | 15:30 | close 10-09 |
| 15 | 4443 | Sansan (Q1) | **−0.10** | −0.27 | 4.5 | 47 | 15:30 | close 10-09 |
| 16 | 9740 | セントラル警備保障 (H1) | **−0.10** | −0.08 | 4.0 | 49 | 15:30 | close 10-09 |
| 17 | 3222 | USMH (H1) | **−0.20** | −0.13 | 2.2 | 47 | 15:30 | close 10-09 |
| 18 | 3063 | ジェイグループHD (H1) | **−0.25** | −0.09 | 2.2 | 48 | 15:30 | close 10-09 |
| 19 | 7603 | ジーイエット (H1) | **−0.30** | −0.24 | 4.0 | 47 | 15:30 | close 10-09 |
| 20 | 3048 | ビックカメラ (FY) | **−0.50** | −0.42 | 3.5 | 44 | **12:00, in session** | sealed spot |
| 21 | 4440 | ヴィッツ (FY) | **−0.60** | −0.90 | 9.0 | 45 | **12:00, in session** | sealed spot ¥2,500 |
| 22 | 9974 | ベルク (H1) | **−0.90** | −0.35 | 3.5 | 45 | **14:00 (inferred), in session** | sealed spot ¥6,540 |
| 23 | 9270 | バリュエンスHD (FY) | **−1.40** | −1.12 | 7.0 | 42 | 16:00 | close 10-09 |
| 24 | 6264 | マルマエ (FY) | **−1.50** | −0.80 | 8.0 | 45 | 15:30 | close 10-09 |
| 25 | 4829 | 日本エンタープライズ (Q1) | **−1.90** | −0.64 | 4.0 | 42 | 16:00 | close 10-09 |

All 25 names are rankable. **No name reaches the 2.8 conviction floor.** The largest |impact_sum| is 1.90. Across the whole US sample, the sign below the floor was a coin flip, so treat this as an ordering of weak leans, not as signals.

**Sign split:** 13 positive and 12 negative on `impact_sum`. The first resolved Japanese days were five of seven negative. Several hunters applied `LESSONS.md` rule 1 and pulled public 月次 and 進捗率 negatives toward zero; their `pre_lessons` drafts were mostly more negative.

**Releases inside the session:** five names release before the 15:30 close and enter at the sealed 10:05 spot.
- 3048 and 4440 at 12:00.
- 9974 at 14:00, inferred from its last four prints.
- 3201 and 7713 at 15:00. For 3201 the time is inferred; its Q3 last year came at 15:30.

The other twenty enter at the 10-09 close.

## The four-model panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four members ran on their pinned agents, with no fallback, and covered 25 of 25 packs.
- Selection rule: at least 3 of 4 members put the name in their own top 20%.

```
rank ticker   sel  k agree  score    sd  members (z)
   1 6264     yes  4  4/4   -1.51  0.36  opus5:-1.35* opus55:-1.22* sonnet55:-2.15* fable51:-1.67*   impact_sum -1.50
   2 9270          2  4/4   -1.38  0.47  opus5:-0.98 opus55:-1.10 sonnet55:-2.15* fable51:-1.65*     impact_sum -1.40
   3 4440          1  4/4   -0.87  0.37  opus5:-0.83 opus55:-0.92 sonnet55:-0.72 fable51:-1.67*      impact_sum -0.60
   4 6814          1  4/4   +0.85  0.24  opus5:+0.78 opus55:+0.92 sonnet55:+0.72 fable51:+1.33*      impact_sum +1.20
   5 4829          1  4/4   -0.70  0.26  opus5:-0.57 opus55:-0.49 sonnet55:-1.17* fable51:-0.83      impact_sum -1.90
   6 6506          0  4/4   +0.61  0.22  opus5:+0.57 opus55:+0.64 sonnet55:+1.08 fable51:+0.52       impact_sum +1.50
   7 8244          0  4/4   +0.57  0.29  opus5:+0.98 opus55:+0.38 sonnet55:+0.76 fable51:+0.28       impact_sum +1.40
   8 6289          0  4/4   +0.50  0.28  opus5:+0.72 opus55:+0.27 sonnet55:+0.81 fable51:+0.17       impact_sum +1.10
   9 7713          0  4/4   +0.48  0.19  opus5:+0.41 opus55:+0.31 sonnet55:+0.81 fable51:+0.56       impact_sum +1.60
  10 7603          0  4/4   -0.45  0.08  opus5:-0.52 opus55:-0.38 sonnet55:-0.54 fable51:-0.35      impact_sum -0.30
  11 3048          0  4/4   -0.45  0.10  opus5:-0.47 opus55:-0.43 sonnet55:-0.40 fable51:-0.67      impact_sum -0.50
  12 4443          0  4/4   -0.43  0.14  opus5:-0.41 opus55:-0.12 sonnet55:-0.49 fable51:-0.44      impact_sum -0.10
  13 9974          0  4/4   -0.38  0.16  opus5:-0.67 opus55:-0.23 sonnet55:-0.38 fable51:-0.39      impact_sum -0.90
  14 3046          0  3/4   -0.23  0.26  opus5:-0.10 opus55:+0.20 sonnet55:-0.36 fable51:-0.49      impact_sum +0.10
  15 7888          0  3/4   +0.21  0.18  opus5:+0.21 opus55:+0.21 sonnet55:+0.40 fable51:-0.10      impact_sum +0.80
  16 8200          0  4/4   +0.20  0.12  opus5:+0.16 opus55:+0.23 sonnet55:+0.45 fable51:+0.17      impact_sum +0.60
  17 2698          0  4/4   +0.20  0.08  opus5:+0.26 opus55:+0.12 sonnet55:+0.31 fable51:+0.14      impact_sum +0.20
  18 3201          0  4/4   +0.16  0.03  opus5:+0.16 opus55:+0.15 sonnet55:+0.23 fable51:+0.17      impact_sum +0.30
  19 9740          0  3/4   +0.11  0.22  opus5:-0.21 opus55:+0.11 sonnet55:+0.40 fable51:+0.11      impact_sum -0.10
  20 3063          0  4/4   -0.10  0.12  opus5:-0.36 opus55:-0.07 sonnet55:-0.12 fable51:-0.08      impact_sum -0.25
  21 3501          0  4/4   -0.10  0.03  opus5:-0.10 opus55:-0.09 sonnet55:-0.04 fable51:-0.14      impact_sum -0.05
  22 3222          0  3/4   -0.08  0.07  opus5:+0.00 opus55:-0.11 sonnet55:-0.04 fable51:-0.17      impact_sum -0.20
  23 8008          0  3/4   +0.07  0.06  opus5:+0.05 opus55:+0.08 sonnet55:-0.04 fable51:+0.11      impact_sum +0.05
  24 2735          0  2/4   -0.05  0.32  opus5:-0.21 opus55:+0.11 sonnet55:+0.45 fable51:-0.39      impact_sum +0.40
  25 4992          0  2/4   +0.03  0.27  opus5:+0.16 opus55:-0.10 sonnet55:+0.31 fable51:-0.39      impact_sum +0.25
```

### Selected: 6264 マルマエ (all four, negative)

The members name the same three items:
- **The company's conservative first-guide habit.** The FY2026 initial OP guide of ¥2.8bn was raised twice, to ¥4.1bn, and the stock closed −9.7% the session after that initial guide ([FY2025 短信](https://tdnet-pdf.kabutan.jp/20251010/140120251010571509.pdf)).
- **A sell-the-print record.** On actual TDnet dates the stock fell after four of the last five prints, including −12.05% on a pre-released Q3.
- **A 30.4x margin long into a ~25% rebound** off the September low.

The case against is strong: SEAJ Japan-made equipment sales were a record in August (+47.4% YoY, [SEAJ](https://www.seaj.or.jp/statistics/14972028907951.pdf)). The company also reports record semiconductor orders and is preparing up to ¥4bn of FY2027 capex. A guide above the Fusion2028 straight-line path (~¥6.15bn OP) would turn the setup around. There is also a 3.13% disclosed short across two sellers, and it is building.

### Where the panel and the hunter disagree most

- **7713, the hunter's top name (+1.60):** the panel ranks it 9th (+0.48). Every member sized it small. The evidence is one company's own July briefing remark on June orders, against a bar the hunter had to construct.
- **Opposite sign:**
  - **3046:** hunter +0.10, panel −0.23.
  - **2735:** hunter +0.40, panel −0.05.
  - **9740:** hunter −0.10, panel +0.11.
  - All three sit within ±0.4 on both measures.
- **4829, the hunter's bottom name (−1.90):** the panel puts it 5th (−0.70). Most of the hunter's sum is a reaction-pattern and positioning reading, which the judges discount.
- **No name was above the conviction floor**, so there is no floor-clearer the panel failed to select.

### What the panel numbers are not

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- Certainty (`p_up`) is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own.
- In the four-model re-judge, the judges ranked Japan and Australia **worse** than the live hunt (ρ −0.25 to −0.31 on 29 names). Nothing about this market's panel is established.

## What drives the top and the bottom

**Top, 7713 シグマ光機 (+1.60).**
- **The driving finding (+1.5):** the company's own July 16 briefing script says June orders were 非常に好調 at both the Japanese parent and the US subsidiary ([script](https://www.sigma-koki.com/asset/data/20260716_scr.pdf), [Q&A](https://www.sigma-koki.com/asset/data/20260716_QA.pdf)). That comes after Q4 OP +64.6% and against a weak year-ago Q1.
- Added to it: +0.5 of yen translation tailwind and −0.4 for the stock going in extended (+12% over 20 days, a year high on 10-07).
- No consensus exists. The bar is the company's own H1 plan read through its Q1 share history, so every size is capped.
- The release is at 15:00, in session, so the entry is the sealed spot.

**Bottom, 4829 日本エンタープライズ (−1.90).**
- **The driving finding (−1.2):** on its actual release dates the stock fell in the first session after six of its last eight prints, including both Q1s (−6.56% and −8.33%). That comes from Yahoo daily bars against kabutan release timestamps ([chart](https://query1.finance.yahoo.com/v8/finance/chart/4829.T?range=3y&interval=1d), [timestamps](https://kabutan.jp/stock/finance?code=4829)).
- Behind it: a margin long rising to 8.23x while shorts halved in the week to 10-02, falling content revenue, and new holding-company and JV costs.
- Offset: a +0.7 ad-spend base effect on a ¥5m ordinary-profit base.
- **This is mostly a reaction pattern and positioning, not an unpriced fact.** It is the kind of finding the panel discounted.

## What every note carries

- **There is no option anchor, and it is substituted.**
  - Japan has no liquid single-stock options, so `options` is null.
  - In its place, `positioning` carries the JPX disclosed short register and 信用倍率. All 25 names resolved the register: it was read as of **2026-09-29**, which is ten days old at the seal. 22 of 25 resolved the margin ratio; 2698, 7603 and 7713 have none, and their `anchor_quality.direction` is 0.45 against 0.60.
  - `baseline_quality` was 0.6 on 22 names and lower on the three without a margin ratio. It never reached 0.725 this run.
  - The lean weights are **priors** with no Japanese measurement behind them. `jp_resolve.py` ranks each component separately.
- **`lean_vs_free_control_rho` from the last resolved run (2026-10-07, resolved this morning) is 0.029** on 6 names. Earlier runs read 0.482 (10-05) and 0.679 (10-06). It has not climbed toward 1.0, so the positioning sources are still resolving and the lean is not the run-up alone. On six names the number itself is noise.
- **`history` is an estimated cadence, not a record of dates.** It is a scale, and several hunters found it misdated: 3046, 3048, 4829, 6264, 7713, 7888 and 9270 all re-measured their scale on actual TDnet release dates. In nearly every case the real reactions were larger than the baseline proxy.
- **Daily price limits (値幅制限) truncate the tail.** 4440 and 6264 carry 8–9% abs_move scales, and a limit move would cap a large finding that was right.
- **The universe is the liquid half of the day.** 34 of 65 scheduled names fell under the ¥15m turnover floor.
- **One day is not a result.** The previous resolved Japanese days ranked at ρ −0.336 (10-05), −0.126 (10-06) and −0.087 (10-07), none significant.

Each hunter's own critical read sits in its `conviction_note` and `baseline_tension` in `hunts/<code>-h1.json`.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
