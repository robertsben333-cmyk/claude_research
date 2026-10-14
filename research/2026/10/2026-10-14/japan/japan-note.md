# Stage J — Japan ranking for 2026-10-14

**Answer first.** 25 Tokyo names were hunted. None clears the 2.8 conviction floor on `impact_sum`; the largest is +1.50 (9168 Rise Consulting) and the smallest −1.00 (6086 Shin Maint). The four-model panel selects one name, **1434 JESCO (+), 4 of 4**. Its second-strongest panel score, **7608 SK Japan (−1.40)**, falls short of selection at 2 of 4.

- **Funnel:** 90 scheduled → 50 eligible above the ¥15m median 20-day turnover floor → 25 hunted.
- **Draw:** `selection.method` is "random sample of 50 eligible, seed 'jp-2026-10-14'". The 25 were drawn at random among the eligible names; the other 25 were dropped by the draw, not by judgement.
- **Calendar:** JPX sheets `kessan08_1002` (as_of 2026-10-01) and `kessan09_1009` (as_of 2026-10-08).
- **Provenance:** prompt `jp.v5`, hunters on claude-opus-5-5 (alias timeline).
- **Orders:** this stage places none.

## Ranked table (`score_report.py`)

**Stage J, 2026-10-14**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=414, impact_scaled n=404): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9168 | amc | **+1.50** (p72) | no | +0.65 (p58) | 6.5 | 55 |
| 2 | 9601 | amc | **+1.10** (p63) | no | +0.80 (p64) | 5.0 | 58 |
| 3 | 1434 | amc | **+1.00** (p60) | no | +0.32 (p38) | 8.0 | 52 |
| 4 | 156A | amc | **+0.90** (p55) | no | +0.45 (p47) | 4.5 | 55 |
| 5 | 8237 | amc | **+0.90** (p55) | no | +0.80 (p64) | 5.0 | 58 |
| 6 | 135A | amc | **+0.70** (p48) | no | +0.66 (p58) | 11.0 | 53 |
| 7 | 2471 | amc | **+0.70** (p48) | no | +0.27 (p34) | 4.5 | 53 |
| 8 | 2462 | amc | **+0.50** (p38) | no | +0.21 (p29) | 1.5 | 57 |
| 9 | 2882 | amc | **+0.50** (p38) | no | +0.20 (p28) | 2.0 | 55 |
| 10 | 505A | amc | **+0.50** (p38) | no | +0.28 (p35) | 3.5 | 54 |
| 11 | 6897 | amc | **+0.50** (p38) | no | +0.30 (p37) | 3.0 | 55 |
| 12 | 5885 | amc | **+0.40** (p32) | no | +0.33 (p39) | 5.5 | 53 |
| 13 | 2305 | amc | **+0.30** (p26) | no | +0.06 (p15) | 1.0 | 53 |
| 14 | 6505 | amc | **+0.30** (p26) | no | +0.36 (p41) | 6.0 | 53 |
| 15 | 7599 | amc | **+0.10** (p13) | no | -0.12 (p21) | 6.0 | 49 |
| 16 | 9837 | amc | **+0.10** (p13) | no | -0.06 (p15) | 2.8 | 49 |
| 17 | 3967 | amc | **+0.00** (p5) | no | -0.24 (p31) | 6.0 | 48 |
| 18 | 3083 | amc | **-0.30** (p26) | no | -0.18 (p26) | 3.0 | 47 |
| 19 | 3543 | amc | **-0.40** (p32) | no | -0.28 (p35) | 2.3 | 44 |
| 20 | 3139 | amc | **-0.50** (p38) | no | -0.40 (p43) | 4.0 | 45 |
| 21 | 3168 | amc | **-0.50** (p38) | no | -0.52 (p52) | 6.5 | 46 |
| 22 | 6183 | amc | **-0.60** (p45) | no | -0.24 (p31) | 2.4 | 45 |
| 23 | 9418 | amc | **-0.60** (p45) | no | -0.07 (p16) | 3.5 | 49 |
| 24 | 7608 | amc | **-0.80** (p51) | no | -0.42 (p45) | 7.0 | 47 |
| 25 | 6086 | amc | **-1.00** (p60) | no | -0.32 (p38) | 4.0 | 46 |

`session` is when the print lands: `amc` after the close, `bmo` before the open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).
`impact_scaled` is the hunter's second, separate measurement, (2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.

**Reading the `session` column.** It reads `amc` for every row, but the hunters found **5 releases inside the 15:30 JST session**:
- 9837 at 11:30
- 2882 and 7608 at 12:00
- 6897 and 9601 at 14:00

For those five, `jp_resolve.py` will enter at the sealed 10:05 JST spot. Of the rest, 14 release at 15:30 and 6 at 16:00 (135A, 3083, 3967, 505A, 6505, 9418). Release times for 3083 (16:00) and 6897 (14:00) are the hunters' inference from earlier prints, not an announced time.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran on their pinned `panel-judge-intl-*` agents and every judge covered all 25 packs (`check` exit 0). There were no fallbacks.

```
rank ticker   session sel  k agree  score    sd  members (z)
   1 1434     amc     yes  4  4/4   +1.40  0.18  opus5:+1.45* opus55:+1.71* sonnet55:+1.21* fable51:+1.35*
   2 7608     amc          2  4/4   -1.40  0.48  opus5:-1.93* opus55:-0.96 sonnet55:-0.90 fable51:-1.83*
   3 9168     amc          2  4/4   +1.09  0.23  opus5:+1.21* opus55:+0.96 sonnet55:+1.21* fable51:+0.66
   4 3139     amc          1  4/4   -0.87  0.20  opus5:-0.85 opus55:-0.54 sonnet55:-1.08* fable51:-0.90
   5 3083     amc          1  4/4   -0.75  0.52  opus5:-0.15 opus55:-1.61* sonnet55:-0.67 fable51:-0.83
   6 3168     amc          1  4/4   -0.70  0.54  opus5:-0.68 opus55:-0.21 sonnet55:-0.72 fable51:-1.69*
   7 6505     amc          1  4/4   +0.55  0.52  opus5:+0.68 opus55:+0.43 sonnet55:+1.62* fable51:+0.26
   8 8237     amc          1  4/4   +0.52  0.38  opus5:+0.79 opus55:+0.21 sonnet55:+0.25 fable51:+1.13*
   9 7599     amc          1  2/4   -0.13  0.61  opus5:+0.41 opus55:+0.21 sonnet55:-0.47 fable51:-1.13*
  10 135A     amc          1  2/4   -0.13  0.78  opus5:-0.79 opus55:+0.54 sonnet55:+0.63 fable51:-1.13*
  11 6897     amc          0  4/4   +0.75  0.23  opus5:+0.76 opus55:+0.86 sonnet55:+0.27 fable51:+0.75
  12 156A     amc          0  4/4   +0.74  0.15  opus5:+0.85 opus55:+0.64 sonnet55:+0.63 fable51:+0.99
  13 3967     amc          0  4/4   -0.72  0.29  opus5:-0.97 opus55:-0.32 sonnet55:-0.47 fable51:-0.98
  14 6086     amc          0  4/4   -0.63  0.23  opus5:-0.91 opus55:-0.75 sonnet55:-0.30 fable51:-0.51
  15 2471     amc          0  4/4   +0.60  0.23  opus5:+0.73 opus55:+0.86 sonnet55:+0.25 fable51:+0.47
  16 6183     amc          0  4/4   -0.55  0.12  opus5:-0.77 opus55:-0.54 sonnet55:-0.57 fable51:-0.45
  17 3543     amc          0  4/4   -0.53  0.12  opus5:-0.64 opus55:-0.43 sonnet55:-0.63 fable51:-0.38
  18 2882     amc          0  4/4   +0.51  0.06  opus5:+0.48 opus55:+0.59 sonnet55:+0.55 fable51:+0.45
  19 505A     amc          0  4/4   +0.49  0.16  opus5:+0.45 opus55:+0.27 sonnet55:+0.71 fable51:+0.53
  20 9418     amc          0  4/4   -0.48  0.17  opus5:-0.42 opus55:-0.54 sonnet55:-0.30 fable51:-0.75
  21 5885     amc          0  4/4   +0.47  0.09  opus5:+0.57 opus55:+0.54 sonnet55:+0.36 fable51:+0.39
  22 9601     amc          0  4/4   +0.40  0.24  opus5:+0.27 opus55:+0.54 sonnet55:+0.81 fable51:+0.19
  23 2462     amc          0  4/4   +0.28  0.14  opus5:+0.30 opus55:+0.59 sonnet55:+0.25 fable51:+0.26
  24 9837     amc          0  3/4   -0.25  0.14  opus5:-0.39 opus55:-0.21 sonnet55:+0.00 fable51:-0.28
  25 2305     amc          0  4/4   +0.18  0.15  opus5:+0.15 opus55:+0.48 sonnet55:+0.20 fable51:+0.09
```

`*` marks a member's own top 20%. The `impact_sum` column is the ranked table above.

### The one selected name

- **1434 JESCO Holdings (panel +1.40, 4/4; `impact_sum` +1.00, hunter #3).**
  - **What the members cite:**
    - The dividend is set by a 30% payout policy, and 9M EPS of 157.35 is already at the 158.57 plan. Applying the stated payout to the actual year implies a year-end dividend of roughly 57–65 yen against the 48-yen plan, while yield screens still quote 2.9%.
    - The FY26 beat is mechanical: 9M ordinary profit is already 100.2% of the never-revised plan.
    - The order backlog is +75% (12,933m against 7,398m), which supports a growth guide for FY27.
    - The stock is down 36% from May at about 8x likely EPS.
  - **Strongest case against:**
    - FY26 profit is inflated by two property sales. A FY27 guide set from the mid-term path could read as a decline, and the last flat guide gapped −9.75%.
    - Margin longs sit at 32.7x after piling in at 1,750–1,940.
  - **Timing:** this is a full-year print at 15:30, after the close. The FY27 guide is the swing item.

### Where the panel and the hunters disagree most

- **7608 SK Japan:** panel #2 at −1.40 (Opus 5 −2.55 and Fable in their own top 20%), against hunter #24 at −0.80. The judges weighted the yen/freight margin squeeze against a record-high stock more heavily. Two of four is not a selection.
- **Opposite or split signs:**
  - 135A VRAIN: hunter +0.70, panel −0.13, 2/4 agree.
  - 7599 IDOM: hunter +0.10, panel −0.13, 2/4 agree.
  - 9837 Morito: hunter +0.10, panel −0.25.
  - 3967 Eltes: hunter 0.00, panel −0.72 with all four negative.
- **9601 Shochiku:** the hunter's #2 (+1.10) is panel #22 (+0.40). No member puts it in its top 20%, because the single IFIS bar already sits about 50% above the plan.
- **No name clears the floor**, so there is no "above-floor name the panel did not select" case.
- **Opus 5 disagreed with the hunter's drops:**
  - It reinstated 9168's Q1 utilisation shortfall (86% against a 92% plan) as in-window evidence, where the hunter had put it in `outside_window`. Fable did the same.
  - It flagged the 5885 "Summer Dragon" campaign notice (posted only on the corporate site, not on TDnet) as the cleanest genuinely unpriced company statement of the day.

### What the panel numbers are not

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own.
- In the four-model re-judge the judges ranked Japan and Australia worse than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.
- The last resolved Japanese panel day, 2026-10-09, ranked at ρ 0.471 (p 0.018) against 0.535 for `impact_sum`, and its one selected name was wrong (−1.43%). One day each.

## Finding and URL behind the top and bottom names

- **Top, 9168 Rise Consulting (+1.50):** the company's FY OP plan of ¥946m sits about 25% above the one-analyst IFIS consensus of ¥755m, which has not moved in four weeks. Q1 OP was ¥240m, 25.3% of plan and "above plan" per the company. A held plan at H1 therefore reads as relief against the street. Holding the plan has been worth +3 to +5% on this name; the tail is a cut, which has cost about −17% twice. Sized +1.4. https://kabuyoho.jp/sp/reportAnalyst?bcode=9168
- **Bottom, 6086 Shin Maint Holdings (−1.00):** the company's own FY26 H1 deck credits last year's record Q2 (Jun–Aug 2025, 経常 +23.6%) to the 猛暑 lifting air-conditioning requests, which are 30% of sales. Summer 2026 was far less hot (anomaly +1.02°C against +2.36°C; 7,529 against 9,385 猛暑日 station-days), so Q2 faces a heat-inflated comparison. Sized −0.8. https://tdnet-pdf.kabutan.jp/20251010/140120251010571284.pdf (weather: https://weather-jwa.jp/?p=16259)

## Names that could not be ranked

None. All 25 are rankable, every hunter confirmed the 2026-10-14 date, and no hunt came back empty.

## What this run carries every time

- **No option anchor, substituted by positioning.** Japan has no liquid single-stock options, so `options` is null. The baseline's `priced_lean_pct` is built from:
  - the JPX disclosed short register (level and change)
  - 信用倍率

  The weights in `lean_components()` are **priors with no Japanese measurement behind them**; `jp_resolve.py` ranks each component separately.
- **What resolved today:**
  - **The register read, but it is stale.** It was read for all 25 names (`covered: true`), but its `as_of` is **2026-09-29, fifteen days before the run**, the same file the 10-13 run used. Five names carry a disclosed position:
    - 3139 at 1.51% (+0.09)
    - 8237 at 0.82% (+0.12)
    - 7599 at 0.68% (−0.04)
    - 5885 at 0.51% (+0.04)
    - 6183 at 0.49% (−0.02)

    The other 20 are real zeros below the 0.5% threshold.
  - **信用倍率 resolved for 19 of 25.** It was null for 3083, 3967, 505A, 6086, 6897 and 9168, most of them buy-only (制度信用 only) names with no margin short side.
- **`lean_vs_free_control_rho` from the last resolved run.** The 2026-10-09 run was resolved in this session: 25 of 25 usable, ρ `impact_sum` 0.535 (p 0.0073) against −0.112 for the free control. **`lean_vs_free_control_rho` read 0.367**, down from 0.474 on 10-08 and below the 0.446–0.59 band measured at launch. That is the lean moving *away* from the run-up, not collapsing back into it.
- **`history` is an estimated cadence** (`estimated_from_cadence` on all 25), a scale and not a record of dates. Several hunters found estimated dates that were not print days and recomputed reactions on actual release dates: 135A, 3543, 6086, 6183 and 8237. The baseline's +8.07% "H1 reaction" for 8237 was really −0.39%.
- **Sign count on `impact_sum`:**
  - 16 positive, 8 negative, 1 zero (3967).
  - The first resolved Japanese days were five of seven negative; today leans the other way, and every hunt was checked against LESSONS rule 2.
- **Conviction floor (2.8):** no name is above it. Over the whole US sample the sign was a coin flip below the floor, and every name here is below it.
- **Daily price limits (値幅制限)** truncate the tail, so a large finding may be right and still not be paid in full. 135A's hunter capped `abs_move_pct` at 11 against a 14.3% limit band.
- **One day is not a result.** Twenty-five names on one day, all below the floor and inside ±1.5, establish nothing about whether these companies can be ranked. Judge the stage only pooled, and the panel only pooled.

## Critical read of the day

- **A quiet day.** Most names are H1 or Q1 prints of companies that do not revise mid-year, and in many of them the quarter is visible in public 月次 or 進捗率. LESSONS rule 1 shrank those findings, and the hunters said so.
- **What the largest numbers rest on:**
  - **The company bar against a single-analyst street** (9168, 9601, 8237). That is a thin bar, and on 9601 the panel declined to follow it.
  - **A payout-policy dividend** (1434), the one item all four judges put in their own top 20%.
- **The recurring negative is the reaction function:** names that have sold their last prints, against crowded margin longs (6183, 3543, 7608). Treat it with care: LESSONS open question 4 records a run-in short that was wrong.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
