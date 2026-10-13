# Stage J — Japan ranking for 2026-10-13

**Answer first.** 25 Tokyo names are hunted. None clears the 2.8 conviction floor on `impact_sum`, and the largest is +2.20 (9278 Bookoff). The four-model panel selects three names, all with 4/4 agreement: **6432 Takeuchi (+)**, **9278 Bookoff (+)** and **2791 Daikokuten Bussan (−)**. The panel's top and bottom are the hunters' top and bottom, so on this day the two measurements agree on the extremes.

- **Funnel:** 51 scheduled → 30 eligible above the ¥15m median 20-day turnover floor → 25 hunted.
- **Draw:** `selection.method` is "random sample of 30 eligible, seed 'jp-2026-10-13'". The 25 were drawn at random among the eligible names, and the other 5 were dropped by the draw, not by judgement.
- **Calendar:** JPX sheets `kessan08_1002` (as_of 2026-10-01) and `kessan09_1009` (as_of 2026-10-08).
- **Provenance:** prompt `jp.v5`, hunters on claude-opus-5-5 (alias timeline).
- **Orders:** this stage places none.

## Ranked table (`score_report.py`)

**Stage J, 2026-10-13**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=359, impact_scaled n=347): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9278 | amc | **+2.20** (p84) | no | +1.32 (p80) | 5.5 | 62 |
| 2 | 3087 | amc | **+2.00** (p81) | no | +0.67 (p55) | 4.2 | 58 |
| 3 | 6432 | amc | **+1.80** (p77) | no | +0.66 (p55) | 5.5 | 56 |
| 4 | 7516 | amc | **+1.00** (p58) | no | +0.49 (p49) | 3.5 | 57 |
| 5 | 7085 | amc | **+0.80** (p49) | no | +0.20 (p26) | 5.0 | 52 |
| 6 | 4714 | amc | **+0.50** (p36) | no | +0.10 (p19) | 2.6 | 52 |
| 7 | 7811 | amc | **+0.30** (p25) | no | +0.08 (p16) | 2.0 | 52 |
| 8 | 1419 | amc | **+0.20** (p17) | no | +0.08 (p16) | 2.0 | 52 |
| 9 | 3086 | amc | **+0.20** (p17) | no | +0.14 (p21) | 3.5 | 52 |
| 10 | 9661 | amc | **+0.20** (p17) | no | +0.04 (p15) | 0.7 | 53 |
| 11 | 575A | amc | **+0.05** (p11) | no | +0.00 (p7) | 2.5 | 50 |
| 12 | 9216 | amc | **+0.05** (p11) | no | +0.00 (p7) | 2.0 | 50 |
| 13 | 8267 | amc | **+0.00** (p5) | no | +0.18 (p25) | 4.5 | 52 |
| 14 | 2379 | amc | **-0.10** (p14) | no | -0.24 (p29) | 4.0 | 47 |
| 15 | 6217 | amc | **-0.10** (p14) | no | -0.28 (p33) | 7.0 | 48 |
| 16 | 7520 | amc | **-0.10** (p14) | no | -0.17 (p23) | 2.8 | 47 |
| 17 | 7725 | amc | **-0.10** (p14) | no | -0.05 (p15) | 2.5 | 49 |
| 18 | 3349 | amc | **-0.20** (p17) | no | -0.27 (p32) | 4.5 | 47 |
| 19 | 2653 | amc | **-0.25** (p20) | no | -0.12 (p20) | 1.5 | 46 |
| 20 | 1401 | amc | **-0.50** (p36) | no | -0.13 (p20) | 6.5 | 49 |
| 21 | 4343 | amc | **-0.50** (p36) | no | -0.30 (p34) | 5.0 | 47 |
| 22 | 7512 | amc | **-0.55** (p40) | no | -0.08 (p16) | 1.3 | 47 |
| 23 | 8273 | amc | **-0.60** (p42) | no | -0.32 (p36) | 2.3 | 43 |
| 24 | 3236 | amc | **-0.70** (p45) | no | -0.21 (p27) | 3.5 | 47 |
| 25 | 2791 | amc | **-1.30** (p65) | no | -0.55 (p51) | 5.5 | 45 |

`session` is when the print lands: `amc` after the close, `bmo` before the open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).
`impact_scaled` is the hunter's second, separate measurement, (2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.

**Reading the `session` column.** `session` reads `amc` for every row. The hunters found four releases inside the 15:30 JST session:
- 6432 at 14:30
- 6217, 7520 and 7811 at 15:00

For those four, `jp_resolve.py` will enter at the sealed 10:05 JST spot. Every other name releases at 15:30 or 16:00, after the close. 7725's company notice says only "15:30 or later".

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran on their pinned `panel-judge-intl-*` agents, every judge covered all 25 packs, and there were no fallbacks.

```
rank ticker   session sel  k agree  score    sd  members (z)
   1 6432     amc     yes  4  4/4   +1.99  0.34  opus5:+1.94* opus55:+2.05* sonnet55:+2.04* fable51:+1.22*
   2 9278     amc     yes  4  4/4   +1.77  0.20  opus5:+1.76* opus55:+2.14* sonnet55:+1.77* fable51:+1.60*
   3 2791     amc     yes  4  4/4   -1.76  0.37  opus5:-1.64* opus55:-1.87* sonnet55:-2.34* fable51:-1.32*
   4 3236     amc          1  4/4   -1.01  0.30  opus5:-1.53* opus55:-1.07 sonnet55:-0.94 fable51:-0.71
   5 4343     amc          1  4/4   -0.90  0.16  opus5:-1.06* opus55:-0.62 sonnet55:-0.94 fable51:-0.86
   6 7516     amc          1  4/4   +0.82  0.47  opus5:+0.59 opus55:+1.70* sonnet55:+1.06 fable51:+0.50
   7 3087     amc          1  4/4   +0.81  0.35  opus5:+1.29* opus55:+1.07 sonnet55:+0.55 fable51:+0.44
   8 3349     amc          0  4/4   -0.70  0.09  opus5:-0.82 opus55:-0.62 sonnet55:-0.62 fable51:-0.78
   9 8273     amc          0  4/4   -0.58  0.07  opus5:-0.65 opus55:-0.62 sonnet55:-0.53 fable51:-0.47
  10 1401     amc          0  4/4   -0.43  0.21  opus5:-0.76 opus55:-0.18 sonnet55:-0.47 fable51:-0.39
  11 7512     amc          0  4/4   -0.40  0.15  opus5:-0.59 opus55:-0.45 sonnet55:-0.35 fable51:-0.19
  12 7725     amc          0  4/4   -0.24  0.11  opus5:-0.29 opus55:-0.18 sonnet55:-0.09 fable51:-0.38
  13 4714     amc          0  4/4   +0.21  0.10  opus5:+0.23 opus55:+0.36 sonnet55:+0.18 fable51:+0.08
  14 8267     amc          0  3/4   +0.17  0.12  opus5:+0.35 opus55:+0.18 sonnet55:+0.00 fable51:+0.16
  15 575A     amc          0  3/4   -0.16  0.12  opus5:-0.29 opus55:-0.09 sonnet55:-0.24 fable51:+0.00
  16 2653     amc          0  4/4   -0.14  0.02  opus5:-0.12 opus55:-0.18 sonnet55:-0.14 fable51:-0.14
  17 3086     amc          0  2/4   +0.13  0.20  opus5:-0.18 opus55:+0.27 sonnet55:+0.29 fable51:+0.00
  18 2379     amc          0  3/4   -0.11  0.19  opus5:-0.06 opus55:+0.09 sonnet55:-0.16 fable51:-0.44
  19 9216     amc          0  3/4   -0.09  0.10  opus5:+0.12 opus55:-0.09 sonnet55:-0.10 fable51:-0.16
  20 9661     amc          0  4/4   +0.09  0.04  opus5:+0.18 opus55:+0.09 sonnet55:+0.09 fable51:+0.06
  21 6217     amc          0  2/4   -0.06  0.10  opus5:-0.12 opus55:+0.09 sonnet55:-0.16 fable51:+0.00
  22 7811     amc          0  3/4   +0.05  0.09  opus5:+0.06 opus55:+0.18 sonnet55:+0.05 fable51:-0.06
  23 1419     amc          0  2/4   -0.04  0.05  opus5:-0.12 opus55:-0.09 sonnet55:+0.00 fable51:+0.00
  24 7085     amc          0  2/4   -0.03  0.26  opus5:-0.18 opus55:+0.45 sonnet55:+0.12 fable51:-0.19
  25 7520     amc          0  1/4   +0.00  0.09  opus5:+0.18 opus55:+0.00 sonnet55:-0.07 fable51:+0.00
```

### The three selected names

- **6432 Takeuchi (panel +1.99; `impact_sum` +1.80).**
  - **What the members cite:** USD/JPY ran about 159 through H1 against a 147 plan rate. The company has raised its full-year guidance at every H1 print since 2022, with a conservative H2 FX assumption each time. A 40% payout target against 39.2% today mechanically implies a dividend raise. The analogous prints moved +7.4% and +11.3%, but those dates come from the estimated cadence.
  - **Strongest case against:** IFIS full-year ordinary profit (39,875m) already sits about 9% above plan, so a raise can land below the street. Q2 orders should fall sharply quarter on quarter after one large US rental order in Q1; the last such drop cost 7.9%. The margin long is crowded at 27x.
  - **Timing:** release at 14:30, inside the session.
- **9278 Bookoff (panel +1.77; `impact_sum` +2.20).**
  - **What the members cite:** Q1 domestic existing-store sales were about 107.5% against a soft prior-year Q1 whose OP fell 57%, and the cost step-up is now lapped. The only visible consensus (IFIS Q1 ordinary 600m) sits at last year's depressed level. Margin shorts exceed longs (信用倍率 0.44). This name has bought profit beats by +9% to +13% on actual release dates.
  - **Strongest case against:** the profit step is the hunter's inference, and the bar rests on a single source. A 6.43m-record data leak (disclosed 10-09) could be quantified in the release. TOPIX transition-measure passive selling hangs over the stock.
- **2791 Daikokuten Bussan (panel −1.76; `impact_sum` −1.30).**
  - **What the members cite:** the company publishes no 月次, so the weak entry run-rate is not visible to the market:
    - Q4 FY26 underlying OP was about 1.52bn.
    - Same-store sales ran 96.6–98.3% from February to May.
    - The Q1 comparison is a rice-driven 103%.

    The stock fell after all four previous Q1 prints (mean −9.5%), and 信用倍率 is 8.5x with no disclosed short.
  - **Strongest case against:** the stock is already down 13% since 2026-09-08, consensus sits below plan, and a flat Q1 against a flat H1 guide would read as a bottoming. The four-print pattern is only four observations.

### Where the panel and the hunters disagree most

- **No opposite signs on the names that matter.** The only name the panel scores at about zero against a hunter positive is 7520 (panel +0.00 against `impact_sum` −0.10, 1/4 agree). Opus 5 resolved that hunter's two contradicting findings to positive.
- **3236 Properst:** the panel puts it 4th (−1.01; Opus 5 −2.6 and in its own top 20%), while the hunter has it 24th at −0.70. The judges weighted the building buy-only margin long more heavily than the hunter did.
- **3087 Doutor:** the hunter's #2 (+2.00) is panel #7 (+0.81). Only Opus 5 puts it in its top 20%, because the IFIS bar already sits above any plausible raise.
- **No name clears the floor**, so there is no "above-floor name the panel did not select" case.

### What the panel numbers are not

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own.
- In the four-model re-judge the judges ranked Japan and Australia worse than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.

## Finding and URL behind the top and bottom names

- **Top, 9278 Bookoff (+2.20):** Q1 FY5/27 domestic BOOKOFF direct existing-store sales were 104.5 / 110.2 / 107.8% (June to August). That comes against last year's soft Q1 and a lapped cost step-up, so the hunter puts Q1 OP at about 0.9–1.2bn against the IFIS Q1 ordinary bar of 600m. Sized +2.5. https://tdnet-pdf.kabutan.jp/20261006/140120261006546551.pdf
- **Bottom, 2791 Daikokuten Bussan (−1.30):** the company's own FY26 deck shows Q4 OP of 1,036m (about 1.52bn before a 487m asset-retirement charge) and same-store sales of 96.6–98.3% from February to May. Against 103% June/July comparisons, Q1 likely lands below the roughly 1.65bn pace the flat H1 guide implies. Sized −0.9. https://www.e-dkt.co.jp/ir/pdfs/library/presentation202605.pdf

## Names that could not be ranked

None. All 25 are rankable, all 25 hunters confirmed the 2026-10-13 date, and no hunt came back empty.

## What this run carries every time

- **No option anchor, substituted by positioning.** Japan has no liquid single-stock options, so `options` is null. The baseline's `priced_lean_pct` is built from:
  - the JPX disclosed short register (level and change)
  - 信用倍率

  The weights in `lean_components()` are **priors with no Japanese measurement behind them**; `jp_resolve.py` ranks each component separately.
- **What resolved today:**
  - **The register read, but it is stale.** It was read for all 25 names (`covered: true`), but its `as_of` is **2026-09-29, two weeks before the run**. Only 2 of 25 names carry a disclosed position (7725 at 1.71%, 3086 at 1.38%); the rest are real zeros below the 0.5% threshold.
  - **信用倍率 resolved for 20 of 25.** It was null for 5, most of them buy-only (貸借非対応) names, where several hunters note the ratio is mechanically skewed.
- **`lean_vs_free_control_rho` from the last resolved run (2026-10-08) is 0.474**, inside the 0.446–0.59 band measured at launch. The lean has not collapsed back into the run-up.
- **`history` is an estimated cadence** (`estimated_from_cadence` on all 25), a scale and not a record of dates. Several hunters found estimated dates that were not print days (7725, 7085, 1419) and set their scale from actual release dates instead.
- **Release times as the hunters found them:** 4 in session (14:30 6432; 15:00 6217, 7520, 7811). The other 21 are at 15:30 or 16:00 (16:00: 1401, 4714, 9661).
- **Sign count on `impact_sum`:** 12 positive, 12 negative, 1 zero (8267). The first resolved Japanese days were five of seven negative; this day is not tilted.
- **Conviction floor (2.8):** no name is above it. Over the whole US sample the sign was a coin flip below the floor, and every name here is below it.
- **Daily price limits (値幅制限)** truncate the tail, so a large finding may be right and still not be paid in full.
- **One day is not a result.** Twenty-five names on one day, all below the floor and mostly within ±0.6, establish nothing about whether these companies can be ranked. Judge the stage only pooled, and the panel only pooled.

## Critical read of the day

- **Most findings are small for the same reason:** the quarter is visible in public 月次, so LESSONS rule 1 shrank them.
- **The three largest panel names are the three where the hunter found something the monthly series does not show:**
  - a guidance/FX habit (6432)
  - a profit step the sales series does not pin (9278)
  - a company with no 月次 at all (2791)

  That is the hypothesis the stage is testing. A single day cannot confirm it.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
