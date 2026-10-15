# Stage J — Japan ranking for 2026-10-15

**Answer first.** 25 Tokyo names were hunted. Three clear the 2.8 conviction floor on `impact_sum`: **1418 インターライフ +4.50**, **5817 JMACS +3.10** and **1407 ウエストHD +3.00**. The bottom is **3547 ユニシアHD −1.00**. **1407 is contaminated:** its 決算短信 hit TDnet at 10:00 JST, six minutes before the 10:06 seal, so its hunter read the release itself. The sealed spot of 2,101 matches pre-10:00 quotes, so the window probably holds the reaction, but its number describes a known print and is not a forecast. Do not count it as evidence for the hunt. The four-model panel selects **seven** names: 1418, 1407, 5817 and 367A long; 3547, 414A and 6224 short.

- **Funnel:** 129 scheduled → 67 eligible above the ¥15m median 20-day turnover floor → 25 hunted.
- **Draw:** `selection.method` is "random sample of 67 eligible, seed 'jp-2026-10-15'". The 25 were drawn at random among the eligible names; the other 42 were dropped by the draw, not by judgement.
- **Calendar:** JPX sheets `kessan08_1002` (as_of 2026-10-01) and `kessan09_1009` (as_of 2026-10-08).
- **Provenance:** prompt `jp.v5`, hunters on claude-opus-5-5 (alias timeline), orchestrator claude-opus-5-5.
- **Orders:** this stage places none.

## Ranked table (`score_report.py`)

**Stage J, 2026-10-15**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=472, impact_scaled n=465): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1418 | amc | **+4.50** (p98) | yes | +2.70 (p97) | 9.0 | 65 |
| 2 | 5817 | amc | **+3.10** (p95) | yes | +1.98 (p93) | 9.0 | 61 |
| 3 | 1407 | amc | **+3.00** (p94) | yes | +2.88 (p97) | 8.0 | 68 |
| 4 | 367A | amc | **+2.20** (p88) | no | +1.20 (p81) | 6.0 | 60 |
| 5 | 276A | amc | **+1.00** (p63) | no | +0.60 (p59) | 10.0 | 53 |
| 6 | 8254 | amc | **+0.60** (p47) | no | +0.56 (p58) | 7.0 | 54 |
| 7 | 8887 | amc | **+0.50** (p39) | no | +0.18 (p26) | 3.0 | 53 |
| 8 | 9252 | amc | **+0.50** (p39) | no | -0.45 (p51) | 7.5 | 47 |
| 9 | 2437 | amc | **+0.40** (p33) | no | +0.10 (p19) | 5.0 | 51 |
| 10 | 6199 | amc | **+0.40** (p33) | no | -0.24 (p32) | 6.0 | 48 |
| 11 | 8233 | amc | **+0.40** (p33) | no | -0.19 (p28) | 3.2 | 47 |
| 12 | 3479 | amc | **+0.30** (p27) | no | -0.36 (p44) | 6.0 | 47 |
| 13 | 280A | amc | **+0.00** (p5) | no | -0.34 (p42) | 8.5 | 48 |
| 14 | 6521 | amc | **+0.00** (p5) | no | -0.18 (p26) | 9.0 | 49 |
| 15 | 7730 | amc | **+0.00** (p5) | no | +0.00 (p7) | 7.0 | 50 |
| 16 | 581A | amc | **-0.05** (p10) | no | +0.00 (p7) | 8.0 | 50 |
| 17 | 4413 | amc | **-0.10** (p13) | no | -0.05 (p14) | 0.8 | 47 |
| 18 | 369A | amc | **-0.20** (p19) | no | -0.16 (p24) | 8.0 | 49 |
| 19 | 2168 | amc | **-0.25** (p22) | no | -0.10 (p18) | 2.4 | 48 |
| 20 | 9628 | amc | **-0.25** (p22) | no | -0.12 (p21) | 3.0 | 48 |
| 21 | 1430 | amc | **-0.30** (p27) | no | -0.25 (p34) | 2.5 | 45 |
| 22 | 414A | amc | **-0.50** (p39) | no | -0.64 (p61) | 8.0 | 46 |
| 23 | 6224 | amc | **-0.50** (p39) | no | -0.48 (p53) | 6.0 | 46 |
| 24 | 3548 | amc | **-0.80** (p55) | no | -0.24 (p32) | 2.0 | 44 |
| 25 | 3547 | amc | **-1.00** (p63) | no | -0.96 (p74) | 6.0 | 42 |

`session` is when the print lands: `amc` after the close, `bmo` before the open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).
`impact_scaled` is the hunter's second, separate measurement, (2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.

**Reading the `session` column.** It reads `amc` for every row, but the hunters found **4 releases inside the 15:30 JST session**:
- 1407 at 10:00, before the seal (see above)
- 6521 at 12:00
- 1430 at 13:00
- 5817 at 14:00

For those, `jp_resolve.py` enters at the sealed 10:05 JST spot. Of the rest, 15 release at 15:30, 5 at 16:00 (1418, 280A, 414A, 4413, 9628) and one at 16:30 (3547). Most of the times are the hunters' inference from earlier prints, not an announced time for today; 276A's 15:30 is the company's own notice.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran on their pinned `panel-judge-intl-*` agents and every judge covered all 25 packs (`check` exit 0). There were no fallbacks. Selection is the market panels' consensus rule: 3 of 4 judges in their own top 20% on the panel's side. `pct` is the size of the mean of the four judges' signed percentiles, each read against that judge's own live range (94 live sizes each before today); side is the direction.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 1418     amc     yes  99 long     1  opus5: 98L* opus55:100L* sonnet55:100L* fable51: 98L*  4  +3.92
   2 1407     amc     yes  98 long     1  opus5: 99L* opus55: 98L* sonnet55: 99L* fable51: 97L*  4  +3.06
   3 5817     amc     yes  93 long     3  opus5: 88L* opus55: 97L* sonnet55: 93L* fable51: 93L*  4  +2.48
   4 3547     amc     yes  90 short    5  opus5: 86S* opus55: 94S* sonnet55: 85S* fable51: 97S*  4  -1.93
   5 414A     amc     yes  89 short    6  opus5: 81S* opus55: 86S* sonnet55: 90S* fable51: 97S*  4  -1.61
   6 367A     amc     yes  84 long     4  opus5: 81L* opus55: 89L* sonnet55: 80L  fable51: 85L*  4  +1.50
   7 6224     amc     yes  76 short   10  opus5: 78S  opus55: 60S  sonnet55: 80S  fable51: 85S*  3  -1.24
   8 280A     amc          63 short   22  opus5: 84S* opus55: 47S  sonnet55: 85S* fable51: 36S   2  -1.04
   9 9252     amc          64 short   19  opus5: 78S  opus55: 60S  sonnet55: 36S  fable51: 84S*  2  -0.96
  10 581A     amc          63 short   18  opus5: 45S  opus55: 46S  sonnet55: 80S  fable51: 81S*  2  -0.91
  11 6521     amc          68 long    13  opus5: 66L  opus55: 74L  sonnet55: 48L  fable51: 83L*  1  +0.99
  12 276A     amc          38 long    44  opus5: 52L  opus55: 30S  sonnet55: 92L* fable51: 36L   1  +0.62
  13 369A     amc          59 short   13  opus5: 42S  opus55: 79S  sonnet55: 60S  fable51: 55S   0  -0.70
  14 2168     amc          41 short   12  opus5: 21S  opus55: 42S  sonnet55: 48S  fable51: 54S   0  -0.50
  15 1430     amc          37 short   10  opus5: 21S  opus55: 42S  sonnet55: 48S  fable51: 36S   0  -0.44
  16 7730     amc          36 short    7  opus5: 30S  opus55: 42S  sonnet55: 29S  fable51: 46S   0  -0.40
  17 2437     amc          26 long    24  opus5: 14S  opus55: 33L  sonnet55: 48L  fable51: 36L   0  +0.38
  18 3548     amc          36 short   11  opus5: 22S  opus55: 36S  sonnet55: 33S  fable51: 52S   0  -0.38
  19 8254     amc          25 long    33  opus5: 21S  opus55: 60L  sonnet55: 11L  fable51: 52L   0  +0.35
  20 9628     amc          20 short   20  opus5: 14L  opus55: 34S  sonnet55: 26S  fable51: 36S   0  -0.31
  21 3479     amc          28 short   18  opus5:  5S  opus55: 34S  sonnet55: 19S  fable51: 55S   0  -0.28
  22 8233     amc          18 long    19  opus5: 14L  opus55: 40L  sonnet55: 29L  fable51: 11S   0  +0.27
  23 8887     amc          22 long     8  opus5: 21L  opus55: 34L  sonnet55: 19L  fable51: 12L   0  +0.25
  24 4413     amc          19 short    7  opus5: 14S  opus55: 31S  sonnet55: 15S  fable51: 15S   0  -0.22
  25 6199     amc           8 long    24  opus5: 14S  opus55: 10L  sonnet55: 11S  fable51: 46L   0  +0.01
```

Own top 20% starts at |1.60| (Opus 5), |1.10| (Opus 5.5), |1.08| (Sonnet 5.5) and |1.20| (Fable 5.1).

### The seven selected names

- **1418 インターライフ (long, 4/4, pct 99; `impact_sum` +4.50, hunter #1).** Q1 OP of ¥918m is already 76.5% of the ¥1,200m FY plan (48% at the same point a year ago), and Q1 NP of ¥604m plus a ¥283m securities gain booked in Q2 roughly equals the ¥800m NP plan. The plan has not been revised and the stock has been flat since July. The same setup last October brought a revision plus a dividend raise and went limit-up (+20.3%). **Against:** the company could raise NP only on the one-off and hold OP, citing materials costs, and 信用倍率 ~38 means margin longs sell into any pop. There is no consensus and no 四季報 number.
- **1407 ウエストHD (long, 4/4, pct 98; `impact_sum` +3.00).** The FY27 first guide is 8–11% above IFIS on every line on top of a 19.5% FY26 経常 beat. **This is the release, read after it was public**: the judges sized a print they could see. Against: the IFIS bar fell 13.8% in late September, so the informed street number may sit above the published one; battery-station grid-connection caps; 信用倍率 99.
- **5817 JMACS (long, 4/4, pct 93; +3.10).** H1 OP is very likely above the full-year plan already (Q1 was 69% of it), from a company that under-guided FY26 by about 3x, and its 39%-of-sales customer 泉州電業 raised its forecast in September. Last year the same headline drew +14.6% with no revision. Releases at 14:00, so it is scored from the 10:05 spot. **Against:** a revision is a coin flip, the stock ran +16.8% in 20 days, and retail is crowded long.
- **3547 ユニシアHD (short, 4/4, pct 90; −1.00).** In four years the company has never revised at Q3, the IFIS number sits above the plan, and last year's identical setup (strong Q3, plan held) fell 12.7% on "通期予想据え置きをマイナス視". **Against:** a raise at Q2 this year bought +12.1%, so an early revision is a real upside tail (the hunter put it at ~20%).
- **414A オーバーラップHD (short, 4/4, pct 89; −0.50).** The 44-yen dividend is 56% of revised EPS against a 40% payout policy, and last year the next year's dividend was left 未定, so a cut or 未定 is likelier than 44 on a stock held for its 5.4% yield. 信用倍率 655x, and all four post-IPO prints fell the next day. **Against:** a growth guide on delayed volumes and the Pokémon art book, at PER 10.5.
- **367A プリモGHD (long, 4/4, pct 84; +2.20).** The Murakami family built 12.35% with a filed purpose of higher dividends, buybacks or going private, and the company moved ¥2.0bn of cash to the parent from capital surplus. The FY27 dividend and any buyback land in the same batch as the first FY27 guide. **Against:** a conservative guide on a stronger yen with no buyback.
- **6224 ＪＲＣ (short, 3/4, pct 76; −0.50).** By the internal plan, H1 OP lands 3–10% short, and last October a 1.4% H1 miss cost −19.3%. The crowded margin long has no short side. **Against:** Q2 roughly doubles year on year off a weak base, and 光通信 keeps adding.

### Where the panel and the hunters disagree most

- **3547 and 414A:** hunter −1.00 and −0.50 (neither near the floor), but all four judges put them in their own top 20% short. The judges sized the reaction-function precedent harder than LESSONS rule 1 let the hunters.
- **280A TMH:** hunter 0.00, but the panel is short at −1.04, with Opus 5 and Sonnet 5.5 in their top 20%. Two of four is not a selection.
- **Opposite signs:**
  - 6199: hunter +0.40, panel split 2 long / 2 short.
  - 9252: hunter +0.50, panel short (−0.96).
  - 3479: hunter +0.30, panel short (−0.28).
  - 6521: hunter 0.00, panel long (+0.99).
- **Above the floor and not selected:** none. All three floor names were selected 4/4.

### What the panel numbers are not

- `panel_score` and `pct` rank; they do not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales rest on 94 live Japanese sizes each, still short of the ~200 the panel needs.
- In the four-model re-judge the judges ranked Japan and Australia worse than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.
- The last resolved Japanese panel day, 2026-10-13 (resolved in this session), ranked at ρ 0.118 (p 0.565) against 0.27 for `impact_sum`; its three selected names went 2 of 3 at +3.37% mean. One day.
- **Seven selected today is unusually many**, and one of them (1407) is the contaminated name.

## Finding and URL behind the top and bottom names

- **Top, 1418 インターライフ (+4.50):** a full-year upward revision is near-certain at this Q2 print and was not pre-released. Q1 OP was ¥918m (76.5% of the ¥1,200m plan), Q1 NP ¥604m, and a ¥283m securities gain is booked in Q2 under the 07-28 notice, so NP already about equals the ¥800m plan before any Q2 operating profit. Sized +4.0. https://tdnet-pdf.kabutan.jp/20260728/140120260727500157.pdf
- **Bottom, 3547 ユニシアHD (−1.00):** the company has changed its full-year forecast only at Q2 or in mid-November in each of the last four years, never at Q3. The IFIS consensus (OP ¥1,400m) sits above the ¥1,340m plan, so a held plan lands below the street, and last year's identical setup fell 12.7%. Sized −1.5. https://kabutan.jp/stock/finance?code=3547 (last year's reaction: https://kabutan.jp/stock/news?code=3547&b=n202510170125)

## Names that could not be ranked

None by the scorer: all 25 are rankable, every hunter confirmed the 2026-10-15 date, and no hunt came back empty. **1407 stays in the file but should be read as release-preceded-seal** (`release_preceded_seal: true` in its hunt). Two names are not ordinary earnings events and their hunters said so:
- **4413 ボードルア** is pinned by Bain's completed TOB at ¥2,970 (squeeze-out pending).
- **8254 さいか屋** is a 整理銘柄 whose price will be set by AFC-HD's share-exchange ratio, possibly announced today.

## What this run carries every time

- **No option anchor, substituted by positioning.** Japan has no liquid single-stock options, so `options` is null. `priced_lean_pct` is built from:
  - the JPX disclosed short register (level and change)
  - 信用倍率

  The weights in `lean_components()` are **priors with no Japanese measurement behind them**; `jp_resolve.py` ranks each component separately.
- **What resolved today:**
  - **The register is current:** `as_of` 2026-10-14, read for all 25 names. Five names carry a disclosed position: 2437 1.89%, 6521 1.69%, 1407 1.32%, 280A 1.28% and 5817 0.90%. The other 20 are real zeros below the 0.5% threshold.
  - **信用倍率 resolved for 15 of 25.** The ten nulls are mostly buy-only (制度信用) names with no margin short side, plus 8254, which as a 整理銘柄 is cash-only.
- **`lean_vs_free_control_rho` from the last resolved run:** the 2026-10-13 run was resolved in this session. 25 of 25 were usable, ρ `impact_sum` 0.27 (p 0.199) against −0.277 for the free control, and sign right 56%. **`lean_vs_free_control_rho` read 0.406**, inside the 0.4–0.5 band expected (0.367 on 10-09). The lean has not collapsed back into the run-up.
- **`history` is an estimated cadence** (`estimated_from_cadence` on all 25), a scale and not a record of dates. Hunters on 2168, 6199 and 9628 found that estimated dates missed the real prints and recomputed reactions on the true dates; 6199's baseline row for Q3 (+3.54%) was really −3.15%.
- **Sign count on `impact_sum`:**
  - 12 positive, 10 negative, 3 at zero.
  - The first resolved Japanese days were five of seven negative; today is roughly balanced.
- **Conviction floor (2.8):** 1418, 5817 and 1407 sit above it (1407 contaminated). Over the whole US sample the sign was a coin flip below the floor.
- **Daily price limits (値幅制限)** truncate the tail, so a large finding may be right and still not be paid in full. 1418 went limit-up on the same setup last year, so its upside is capped by the limit, not by the finding.
- **Market backdrop:** the Nikkei was down about 3.7–3.9% by the 10:05 seal, which is in every sealed spot. Several hunters noted it and none filed it.
- **One day is not a result.** Twenty-five names on one day establish nothing about whether these companies can be ranked. Judge the stage only pooled, and the panel only pooled.

## Critical read of the floor-clearers

- **1418:** the strongest unpriced setup of the day, resting on the company's own filings and arithmetic. The bar is the stale company plan alone: no consensus, no 四季報. The risk is that the revision is NP-only.
- **5817:** the same shape (H1 above the FY plan, no consensus). Its 14:00 release puts the reaction inside the session, and the +16.8% run-in makes it the more crowded of the two.
- **1407:** not a forecast, as above. If it resolves right, that says nothing about the hunt.
- **What the selection rests on:** the panel's four extra names all rest on precedent on the same line (3547, 6224, 414A) or on a shareholder's filed intent (367A). That is reaction-function evidence, which LESSONS open question 4 warns has been wrong before.

## Process notes

- Hunters were rolled rather than released in fixed waves of 5. At the end, 9252 and 9628 were launched together, briefly putting 7 hunters in flight against `max_concurrent_subagents` 5.
- Early hunters overwrote each other's downloads in the shared scratchpad. Later hunters were each given their own subfolder.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
