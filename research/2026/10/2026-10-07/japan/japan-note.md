# Stage J — Japan ranking for 2026-10-07

Research only. No orders. The ranking key is `impact_sum`, as `edge-scores.json` reports it: points of spot, signed. There is no call and no threshold label.

**Funnel:** 9 scheduled / 6 eligible (6093, 8166 and 9846 fell below the ¥15m median-turnover floor) / 6 hunted.
- `selection.method` is *all 6 eligible names (at or under the cap)*, so the date-seeded random draw (`jp-2026-10-07`) was not needed.
- The JPX sheets read were kessan08 and kessan09, `calendar_as_of` 2026-10-01.
- Prompt version is `jp.v6`. Hunters ran on claude-opus-5-5 (from the alias timeline).

| # | code | name | impact_sum | impact_scaled (v3, not the key) | abs_move | p_up | release (JST) | entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3391 | ツルハHD | **+0.20** | +0.18 | 3.0 | 53 | 15:30 | close 10-07 |
| 2 | 2918 | わらべや日洋HD | **0.00** | −0.24 | 4.0 | 47 | 15:30 | close 10-07 |
| 3 | 6255 | エヌ・ピー・シー | **0.00** | −0.17 | 4.2 | 48 | 15:30 | close 10-07 |
| 4 | 5932 | 三協立山 | **−0.70** | −0.30 | 3.0 | 45 | 15:30 | close 10-07 |
| 5 | 2670 | エービーシー・マート | **−1.30** | −0.88 | 5.5 | 42 | 15:30 (company 月次 states it) | close 10-07 |
| 6 | 428A | サイプレスHD | **−1.70** | −0.48 | 6.0 | 46 | **12:00, unconfirmed (in session)** | sealed spot ¥1,755 |

All 6 names are rankable.

- **Conviction floor:** no name reaches the 2.8 floor; the largest |impact_sum| is 1.70. Across the US sample the sign was a coin flip below the floor.
- **Signs:** 1 positive, 3 negative, 2 at exactly zero. The first resolved Japanese days ran five of seven negative, and today leans the same way.
- **In-session releases:** one, 428A. Kabutan lists it as 発表時間未確認 (前回12:00). Its Q1 and Q3 came at 12:00, Q2 at 13:00 and FY25 at 15:30. If the release lands at 15:30 instead, the entry basis changes.
- **Ties:** 2918 and 6255 tie at 0.00, so their order is arbitrary.

## What drives the top and the bottom

**Top: 3391 ツルハHD (+0.20).**
- Main finding (+0.7): an H1 operating-profit beat of the company's own plan.
  - The H1 plan of ¥52.6bn needs only ¥28.4bn in Q2.
  - Tsuruha and Welcia together made ¥31.0bn in Jun–Aug 2025, and Q1 already ran ahead of the internal plan.
  - Source: https://tdnet-pdf.kabutan.jp/20260708/140120260707589226.pdf
- Offsets: weak public Q2 same-store sales (+0.7% average, −0.2), split peer prints in the northern regions (−0.2), and street FY ordinary consensus of ¥100.6bn already above the plan's ¥98.1bn (−0.1).
- The net is near zero.

**Bottom: 428A サイプレスHD (−1.70).**
- Main finding (−1.5): the first FY27 guide.
  - FY26 net income of ¥785m was pre-released on 09-25 and includes about ¥240m of deferred-tax gain.
  - The mid-term plan's roughly 30% path implies FY27 net of about ¥680–720m.
  - So kabutan's net-income headline probably reads 最終減益, even though operating profit keeps growing.
  - The stock rose +15.5% on that same net-income headline on 09-28 and has since given all of it back.
  - Sources: https://tdnet-pdf.kabutan.jp/20260925/140120260925539974.pdf and https://tdnet-pdf.kabutan.jp/20260819/140120260819523056.pdf
- Other findings: a likely 増配 under the plan's 20%+ payout floor (+0.5), Q4 margin dilution from new openings (−0.2), and a margin long of about 10 days' volume with no short side (−0.5).

**Close to the bottom: 2670 エービーシー・マート (−1.30).**
- Q2 domestic sales were +2.1% after Q1's 0.9pt gross-margin slip.
- The FY plan is likely held while consensus sits 3% above it.
- The stock ran +4.4% in two sessions on September comps (+14.9%), into a print type it has sold after 9 of the last 12 times.

## Baseline, positioning and caveats (every run)

**There is no option anchor; positioning substitutes for it.**
- The JPX short register resolved for all 6 names, but its latest file is dated **2026-09-29**, eight days old at the seal.
- Disclosed shorts:

  | code | disclosed short |
  | --- | --- |
  | 6255 | 2.93% (building) |
  | 5932 | 0.68% |
  | others | none at or above 0.5% |

- 信用倍率 resolved for 5 of 6. It is null for 428A, a buy-only 制度信用 name.
- `baseline_quality` is 0.60 on five names and 0.45 on 428A.
- The lean weights in `lean_components()` are **priors with no Japanese measurement behind them**.

**`lean_vs_free_control_rho` reads 0.90 on the last resolved run (2026-10-02, n=5).** On 10-01 (n=4) it was 0.60.
- 0.90 is close to the 1.0 that would mean the lean has collapsed back into the run-up.
- On five names this is mostly noise, but it is the highest reading yet and is worth watching.
- Today the register is zero for four of six names, so the margin-overhang and run-up terms carry most of the lean.
- 10-05 and 10-06 are not resolved yet.

**`history` is an estimated cadence: a scale, not a record of dates.** Today it was shown wrong more than once:
- 428A: the three estimated print dates did not match the real ones (01-14, 04-10, 07-10). The real release-day moves were −2.74%, −0.56% and +1.32%.
- 2670: its real 12-print median move is 4.66%, against a proxy of 3.83.
- 6255: its own 8-print median is about 6.4%, against a proxy of 4.17.

The hunters re-derived the scale from real dates where they could.

**Other caveats:**
- **Daily price limits (値幅制限) truncate the tail.** A large finding can be right and still not be paid in full.
- **Pre-released prints.** 6255 pre-released its FY8/26 actuals and FY8/27 headline guide on 09-30 (the stock rose +8.2% on 10-01). 428A pre-released FY26 on 09-25. On both, the print is mostly the refinement and the new-year guide.
- **Bars are thin.** No H1 or FY27 四季報 or IFIS number was sourced for any name, so every bar is the company plan, sometimes plus a FY consensus from kabuyoho. All sizes are capped small, which is why the whole day sits inside ±1.7.

**`pre_lessons` control.**

| code | pre_lessons → final |
| --- | --- |
| 2670 | −2.0 → −1.3 |
| 2918 | −0.5 → 0.0 |
| 3391 | −0.1 → +0.2 |
| 428A | −2.0 → −1.7 |
| 5932 | −1.3 → −0.7 |
| 6255 | −0.4 → 0.0 |

LESSONS rule 1 pulled every negative that rested on public series toward zero. Every name moved in the positive direction.

## What today does NOT establish

Six small names on one day, none above the floor, nothing resolved. One day is not a result, and no ranking claim can be read off it. Resolve with `jp_resolve.py` after the 10-08 close, before TDnet's window of about 31 days lapses.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
