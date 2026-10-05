# Stage J — Japan ranking for 2026-10-05

Research only. No orders. Ranked on `impact_sum`, the key `edge-scores.json` reports, in points of spot, signed. There is no call and no threshold label.

**Funnel:** 15 scheduled / 11 eligible (4 below the ¥15m median-turnover floor) / 11 hunted.
`selection.method`: *all 11 eligible names (at or under the cap)*. The date-seeded random draw (`jp-2026-10-05`) was not needed, so every eligible name was hunted. `calendar_as_of` is 2026-10-01. Prompt `jp.v6`; hunters on claude-opus-5-5 (alias timeline).

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3498 | 霞ヶ関キャピタル | **+1.70** | +0.78 | 6.5 | 56 | 15:30 | close 10-05 |
| 2 | 3186 | ネクステージ | **+1.20** | +1.12 | 7.0 | 58 | 15:30 | close 10-05 |
| 3 | 6474 | 不二越 | **+1.00** | +0.63 | 4.5 | 57 | 15:00 (in session) | sealed spot ¥5,740 |
| 4 | 1376 | カネコ種苗 | **+0.80** | +0.25 | 2.5 | 55 | 13:00 (inferred, in session) | sealed spot ¥1,550 |
| 5 | 8923 | トーセイ | **+0.50** | +0.14 | 3.5 | 52 | 14:30 (in session) | sealed spot ¥1,723 |
| 6 | 3612 | ワールド | **+0.40** | +0.15 | 2.5 | 53 | 15:30 | close 10-05 |
| 7 | 7630 | 壱番屋 | **+0.20** | +0.03 | 1.5 | 51 | 15:30 | close 10-05 |
| 8 | 3148 | クリエイトＳＤ | **−0.10** | −0.09 | 2.2 | 48 | 15:30 | close 10-05 |
| 9 | 9793 | ダイセキ | **−0.30** | −0.34 | 4.3 | 46 | 15:30 | close 10-05 |
| 10 | 2753 | あみやき亭 | **−0.60** | −0.18 | 1.8 | 45 | **09:00, before the seal** | sealed spot ¥1,317 (post-release) |
| 11 | 7679 | 薬王堂HD | **−1.20** | −0.63 | 4.5 | 43 | 15:30 | close 10-05 |

All 11 names are rankable.

- **None clears the 2.8 conviction floor**; the largest |impact_sum| is 1.70. Across the US sample the sign was a coin flip below the floor.
- **Signs:** 7 positive, 4 negative. The first resolved Japanese days ran five of seven negative.
- **In-session releases: four.**
  - 6474 at 15:00, 8923 at 14:30 and 1376 at 13:00 (1376's time is inferred from its last three releases, not confirmed).
  - 2753 released at **09:00 JST, an hour before the 10:05 seal**. Its sealed spot (−4.22% on the prior close) already holds the first reaction, so its scored window is residual drift only. `jp_resolve.py` will label the entry `sealed_spot_before_release`, but that price is post-release. Read 2753 apart from the rest.

## What drives the top and the bottom

- **Top: 3498 霞ヶ関キャピタル (+1.70).**
  - **Main finding, +1.0:** the first FY27 guide. FY26 was already pre-released on 09-17. The company guided above its own mid-term path last year. Its 2026-07-06 FAQ moves Dubai profits into FY27 and reaffirms the FY29 net-profit target of ¥50bn. The bar is about ¥25–27bn of net profit. Source: https://tdnet-pdf.kabutan.jp/20260706/140120260706587998.pdf
  - **Smaller positives:** a likely dividend step-up (+0.3), the pre-released FY26 (+0.2), and prime-broker shorts at 7.39% (+0.2).
  - **Not in the window:** last year a ¥34.5bn equity raise followed the print by three weeks (−15%). It is filed under `outside_window` at −3.0.
- **Bottom: 7679 薬王堂HD (−1.20).**
  - **Main finding, −1.5:** a full-year cut is likely with this release. The FY operating-profit plan of ¥5.52bn needs H2 up about 30% YoY. Q2 same-store sales ran 96.8 / 98.9 / 101.9, and Q1 SG&A grew faster than sales. The January 2026 cut traded −4.15%.
  - **Offsets:** a recovering September 月次 (+0.5) and PER 7.65 / PBR 0.76 at the bottom of the range (+0.6).
  - **Source:** the hunt file `hunts/7679-h1.json`, which cites the company's 短信 and 月次.

## Baseline, positioning and caveats (every run)

- **No option anchor; positioning substitutes for it.**
  - The JPX short register resolved for all 11 names; the latest file is dated 2026-09-29.
  - 信用倍率 resolved for all 11.
  - `baseline_quality` is 0.60 on every name today, against 0.725 on the 09-11 validation universe. Only one name, 3498 at 7.39%, carries a disclosed short above 1%.
  - The lean weights in `lean_components()` are **priors with no Japanese measurement behind them**.
- **`lean_vs_free_control_rho` from the last resolved run (2026-10-01, n=4) is 0.60.** On 09-30 (n=5) it was 0.80 and on 09-29 (n=4) it was −0.40. That is noise on four or five names, but it is still below 1.0, so the positioning terms are still resolving. 10-02 is not resolved yet; its window closes at today's close.
- **`history` is an estimated cadence: a scale, not a record of dates.** Hunters re-derived the scale from real release dates where they could:
  - 3148: 2.6% observed against a 1.69 proxy.
  - 6474: about 5.8% against 3.43.
- **Daily price limits (値幅制限) truncate the tail.** A large finding can be right and still not be paid in full.
- **Bars are thin.** No analyst covers 3148, 1376 or 7679. Several other bars rest on a single aggregator, kabuyoho/IFIS. Sizes are capped small for that reason, which is why the whole day sits inside ±1.7.
- **7630 trades on a deal, not on earnings.** Since 2026-08-31 the stock has traded as a takeover candidate: House Foods (51%) is exploring a sale. That damps the earnings reaction.
- **`pre_lessons` control.**
  - **Changed:** 1376 +0.7→+0.8, 2753 −1.0→−0.6, 3186 +1.5→+1.2, 6474 +0.8→+1.0, 7630 0.0→+0.2, 7679 −1.6→−1.2, 9793 −0.8→−0.3.
  - **Unchanged:** 3148, 3498, 3612 and 8923.
  - LESSONS rule 1 pulled every negative that rested on public series toward zero.
- **Process defect.** Two hunters (7630 and 7679) collided on a same-named file in a shared scratch directory. 7679 caught it and logged the contaminated reading under `rejected_candidates`. Its final findings cite Yakuodo's own documents.

## What today does NOT establish

Eleven names on one day, all small, none above the floor, nothing resolved. One day is not a result, and no ranking claim can be read off it. Resolve with `jp_resolve.py` after the 10-06 close and before TDnet's ~31-day window lapses.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
