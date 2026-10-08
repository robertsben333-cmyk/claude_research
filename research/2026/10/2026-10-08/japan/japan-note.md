# Stage J — Japan ranking for 2026-10-08

This is research only and no orders are placed. The ranking key is `impact_sum`, as `edge-scores.json` reports it: points of spot, signed. There is no call and no threshold label.

**Funnel:** 29 scheduled, 19 eligible, 19 hunted. Ten names fell below the ¥15m median-turnover floor.
- `selection.method`: *all 19 eligible names (at or under the cap of 25)*. So the date-seeded random draw (`jp-2026-10-08`) was not needed, and every eligible name was hunted.
- JPX sheets read: kessan08_1002 and kessan09_1002, `calendar_as_of` 2026-10-01.
- Prompt version `jp.v6`. Hunters ran on claude-opus-5-5 (per the alias timeline).
- Baselines were sealed at 10:05 JST.

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9983 | ファーストリテイリング (FY) | **+1.60** | +0.77 | 5.5 | 57 | 15:30 | close 10-08 |
| 2 | 9861 | 吉野家HD | **+1.50** | +0.45 | 3.2 | 57 | 16:00 | close 10-08 |
| 3 | 4763 | クリーク・アンド・リバー社 | **+1.40** | +0.60 | 5.0 | 56 | 15:30 | close 10-08 |
| 4 | 2809 | キユーピー | **+1.30** | +0.40 | 4.0 | 55 | 15:30 | close 10-08 |
| 5 | 6323 | ローツェ | **+1.10** | +0.44 | 5.5 | 54 | 15:30 | close 10-08 |
| 6 | 9716 | 乃村工藝社 | **+0.80** | +0.40 | 4.0 | 55 | 15:30 | close 10-08 |
| 7 | 8016 | オンワードHD | **+0.70** | +0.25 | 2.5 | 55 | 15:30 | close 10-08 |
| 8 | 3382 | セブン＆アイHD | **+0.40** | +0.11 | 2.8 | 52 | 15:30 (inferred) | close 10-08 |
| 9 | 4825 | ウェザーニューズ | **+0.30** | +0.10 | 5.0 | 51 | 15:30 | close 10-08 |
| 10 | 9414 | 日本BS放送 (FY) | **+0.30** | +0.16 | 4.0 | 52 | 15:30 | close 10-08 |
| 11 | 8125 | ワキタ | **+0.25** | +0.22 | 1.8 | 56 | 16:00 | close 10-08 |
| 12 | 7649 | スギHD | **+0.20** | 0.00 | 3.0 | 50 | 15:45 (expected) | close 10-08 |
| 13 | 8203 | ミスターマックスHD | **+0.20** | +0.07 | 3.5 | 51 | **15:00 (company 月次 states it), in session** | sealed spot ¥714 |
| 14 | 9765 | オオバ | **+0.10** | 0.00 | 2.2 | 50 | 16:00 (inferred) | close 10-08 |
| 15 | 7513 | コジマ (FY) | **−0.30** | −0.18 | 3.0 | 47 | 15:30 | close 10-08 |
| 16 | 8278 | フジ | **−0.40** | −0.09 | 2.3 | 48 | **15:00, in session** | sealed spot ¥1,955 |
| 17 | 9946 | ミニストップ | **−0.60** | −0.11 | 2.8 | 48 | 15:30 | close 10-08 |
| 18 | 8194 | ライフコーポレーション | **−0.80** | −0.28 | 3.5 | 46 | **11:30, in session** | sealed spot ¥2,549 |
| 19 | 3907 | シリコンスタジオ | **−1.50** | −1.30 | 6.5 | 40 | 16:00 (inferred) | close 10-08 |

**All 19 names are rankable.** No name reaches the 2.8 conviction floor; the largest |impact_sum| is 1.60. Over the whole US sample the sign below the floor was a coin flip. So treat this as an ordering of weak leans, not as signals.

**Sign split.** 14 positive and 5 negative. That reverses the first resolved Japanese days, which were five of seven negative. It is consistent with `researcher_japan/LESSONS.md` rule 1, which several hunters applied to pull public 月次 and 進捗率 negatives toward zero.

**Releases inside the session.** Three names release before the 15:30 close: 8194 at 11:30, and 8203 and 8278 at 15:00. They enter at the sealed 10:05 spot. The other sixteen enter at the 10-08 close. 9946 carries a caveat: its January cut came out at 14:00, so if a revision is attached this time it could land in session.

## What drives the top and the bottom

- **Top, 9983 Fast Retailing, +1.60.** The largest finding (+1.0, guidance) is about the first FY8/27 guide. The last three full-year prints rose +5.75%, +6.09% and +6.65%, each on an initial guide at or above consensus. The stock is down 23% from its July peak while broker targets and the IFIS consensus held. The FY27 guide has no sourced consensus, so the size is capped.
  - Source: https://www.nikkei.com/article/DGXZRST0569462X01C25A0000000/
  - Counterweight filed: −0.5 for weak-yen margin pressure making the guide cautious.
- **Bottom, 3907 シリコンスタジオ, −1.50.** The whole sum comes from one finding (−1.5, positioning/reaction history). On the 12 confirmed print dates since 2023-10, the next session fell 11 times, with a median of about −7.5%. The baseline's cadence-estimated dates miss most of those real print days. The finding is sized well under that median because the stock already fell 14.9% in the five sessions before the print.
  - Source (print-date table): https://kabuyoho.jp/sp/report?bcode=3907
  - Prices: https://query1.finance.yahoo.com/v8/finance/chart/3907.T

## Things every note must say

- **The lean against the free control.** `lean_vs_free_control_rho` on the last three resolved runs: 0.9 (10-02), 0.482 (10-05, 11 names) and 0.679 (10-06, 7 names). The 10-05 and 10-06 runs were resolved by this session. The check has not collapsed to 1.0, but 10-02's 0.9 is close, and each figure rests on 5–11 names.
  - The same resolves ranked `impact_sum` at ρ −0.336 (p 0.32) on 10-05 and −0.126 (p 0.79) on 10-06. Signs were right on 45% and 14% of names.
- **The lean's weights are priors** with no Japanese measurement behind them. Components that resolved today:
  - The JPX short register (file of 2026-09-29, 598 codes) resolved for all 19.
  - 信用倍率 resolved for 18 of 19. 3907 is 制度信用 buy-only, so its ratio is undefined and its `baseline_quality` is 0.45 against 0.6 for the rest.
- **Hunters flagged three places where the lean misreads the position.**
  - 3382: 6.28% of its 6.87% disclosed short is SMBC Nikko's hedge for the August accelerated buyback, so the +3.0 squeeze lean is spurious.
  - 8278 (0.16) and 9861 (0.38): the short-heavy margin book is mostly 株主優待 record-date cross trades, not squeeze fuel.
- **`history` is an estimated cadence, not a record of dates.** It is a scale only. At least six hunters (3907, 4763, 6323, 8016, 9765, 8125) found the estimated dates off the real release dates. They re-measured on real dates and found larger median moves than the baseline proxy, which is why several `abs_move_pct` sit above it. This bias was already measured in Europe (`scale_is_lower_bound`).
- **Daily price limits (値幅制限)** truncate the tail, so a large finding can be right and still not be paid in full.
- **No option anchor.** `options` is null everywhere and is substituted by positioning. None of it says what the market expects from *this* print. The anchor-less backtest result (ρ=+0.073, p=0.45 over 104 events) has been made testable, not refuted.
- **Housekeeping.** The 9765 and 9861 hunters left scratch downloads under `hunts/h9765/` and `hunts/h9861/`, because the dispatch prompt asked for an "own subfolder". They are not hunts. `edge_score.py` reads only `hunts/*.json`, so they cannot enter the scores. Removing them was not permitted in this session.

**One day is not a result.** Nineteen names with no floor-clearer, on a ranker that has not yet shown a positive rank correlation on any resolved Japanese day.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
