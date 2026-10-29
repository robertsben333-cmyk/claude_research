# Stage J — Japan ranking for 2026-10-29

**Funnel:** 127 scheduled, 106 eligible, 25 hunted, 25 ranked. 21 names were dropped on the ¥15m median-turnover floor.
- **Selection:** `random sample of 106 eligible, seed 'jp-2026-10-29'`. The draw was random among the eligible names and capped at 25; no judgement entered the cut. The 81 eligible names not drawn are in `universe.json` `eligible_codes`.
- **Calendar:** sheets `kessan09_1023` (as of 2026-10-22, 2,920 rows), `kessan08_1002` (as of 2026-10-01, 454 rows) and `kessan` (114 rows). `calendar_as_of` reads 2026-10-01 (the oldest sheet); every hunter re-confirmed its date on kabutan, kabuyoho or the company's IR page.
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5 (alias timeline); orchestrator flag not recorded.
- **Short register:** JPX file as of 2026-10-28. Only 5 of 25 names carry a disclosed position (3199 3.45%, 9202 3.42%, 6419 1.60%, 9474 0.69%, 9502 0.59%); the other 20 are real zeros. 信用倍率 resolved for 22 of 25 (none for 4347, 4366, 6822).

**Release times**, as each hunter found them (from prior 短信 timestamps or the IR calendar; only Takeda's was confirmed by a notice for today):
- **Inside the session (9)** — these enter at the sealed ~10:05 JST spot: 6902 11:20 (expected), 8706 11:25, 7259 13:00, 9474 13:00, 2594 14:00, 3116 14:00, 9532 14:00, 9708 14:00, 5482 14:40.
- **At or after the close (15):** 15:30 for 1946, 3199, 4347, 4502, 6349, 6471, 6810, 6822, 9202, 9551; 15:40 for 6345; 16:00 for 6419, 7962, 9502; 16:50 for 9046.
- **Unknown (1):** 4366 (its Q1 came at 14:30, the three prints before at 16:00).
- The scored file labels every row `amc`. `jp_resolve.py` reads the actual TDnet time and sets the entry basis from that, not from the label.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1946 | トーエネック Toenec (H1) | **+1.70** (p85) | no | +0.88 | 5.5 | 58 |
| 2 | 5482 | 愛知製鋼 Aichi Steel (H1) | **+1.20** (p75) | no | +0.56 | 4.0 | 57 |
| 3 | 6471 | 日本精工 NSK (H1) | **+1.00** (p70) | no | +0.56 | 3.5 | 58 |
| 4 | 6810 | マクセル Maxell (H1) | **+1.00** (p70) | no | +0.27 | 4.5 | 53 |
| 5 | 6349 | 小森コーポレーション Komori (H1) | **+0.90** (p65) | no | +0.54 | 4.5 | 56 |
| 6 | 3199 | 綿半HD Watahan (H1) | **+0.60** (p51) | no | +0.35 | 2.2 | 58 |
| 7 | 6822 | 大井電気 Oi Electric (H1) | **+0.60** (p51) | no | +0.35 | 3.5 | 55 |
| 8 | 2594 | キーコーヒー Key Coffee (H1) | **+0.50** (p44) | no | +0.13 | 1.3 | 55 |
| 9 | 4347 | ブロードメディア Broadmedia (H1) | **+0.50** (p44) | no | +0.13 | 3.3 | 52 |
| 10 | 9551 | メタウォーター Metawater (H1) | **+0.50** (p44) | no | +0.10 | 5.0 | 51 |
| 11 | 7962 | キングジム King Jim (Q1) | **+0.30** (p30) | no | +0.08 | 2.0 | 52 |
| 12 | 6345 | アイチコーポレーション Aichi Corp (H1) | **+0.10** (p13) | no | -0.16 | 2.6 | 47 |
| 13 | 4502 | 武田薬品 Takeda (H1) | **+0.05** (p10) | no | -0.04 | 2.0 | 49 |
| 14 | 8706 | 極東証券 Kyokuto Securities (H1) | **+0.00** (p4) | no | +0.00 | 1.6 | 50 |
| 15 | 6902 | デンソー Denso (H1) | **-0.10** (p13) | no | -0.21 | 3.5 | 47 |
| 16 | 9502 | 中部電力 Chubu Electric (H1) | **-0.10** (p13) | no | +0.00 | 3.5 | 50 |
| 17 | 7259 | アイシン Aisin (H1) | **-0.20** (p20) | no | -0.18 | 4.5 | 48 |
| 18 | 4366 | ダイトーケミックス Daito Chemix (H1) | **-0.30** (p30) | no | -0.22 | 5.5 | 48 |
| 19 | 9046 | 神戸電鉄 Kobe Electric Railway (H1) | **-0.30** (p30) | no | -0.13 | 2.2 | 47 |
| 20 | 9474 | ゼンリン Zenrin (H1) | **-0.30** (p30) | no | -0.21 | 3.5 | 47 |
| 21 | 9532 | 大阪ガス Osaka Gas (H1) | **-0.30** (p30) | no | -0.09 | 2.3 | 48 |
| 22 | 6419 | マースグループHD Mars Group (H1) | **-0.70** (p56) | no | -0.09 | 2.3 | 48 |
| 23 | 9708 | 帝国ホテル Imperial Hotel (H1) | **-0.75** (p59) | no | -0.07 | 1.8 | 48 |
| 24 | 3116 | トヨタ紡織 Toyota Boshoku (H1) | **-1.00** (p70) | no | -0.80 | 5.0 | 42 |
| 25 | 9202 | ANAホールディングス ANA (H1) | **-1.00** (p70) | no | -0.35 | 3.5 | 45 |

Percentiles in brackets are |impact_sum| among Opus 5.5 reference names (n=719): scale, not rank. `impact_scaled` is the hunter's second, separate measurement and is not the key.

## The four-model panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing.** All four ran on their pinned agents, no fallback, 25/25 coverage each. Selection is the market-panel rule, 3 of 4 judges in their own top 20%.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 1946     amc     yes  90 long     4  opus5: 85L* opus55: 92L* sonnet55: 94L* fable51: 88L*  4  +1.70
   2 3116     amc     yes  84 short    6  opus5: 84S* opus55: 84S* sonnet55: 91S* fable51: 75S   3  -1.34
   3 6471     amc     yes  81 long     2  opus5: 84L* opus55: 80L* sonnet55: 78L  fable51: 82L*  3  +1.19
   4 5482     amc          79 long     8  opus5: 67L  opus55: 88L* sonnet55: 85L* fable51: 75L   2  +1.09
   5 9202     amc          62 short   12  opus5: 40S  opus55: 71S  sonnet55: 70S  fable51: 65S   0  -0.69
   6 7259     amc          60 short   12  opus5: 72S  opus55: 64S  sonnet55: 40S  fable51: 63S   0  -0.65
   7 6902     amc          56 short   12  opus5: 36S  opus55: 59S  sonnet55: 59S  fable51: 70S   0  -0.57
   8 6349     amc          44 long    16  opus5: 21L  opus55: 64L  sonnet55: 53L  fable51: 37L   0  +0.44
   9 3199     amc          43 long     4  opus5: 45L  opus55: 42L  sonnet55: 48L  fable51: 37L   0  +0.43
  10 6345     amc          43 short    9  opus5: 35S  opus55: 42S  sonnet55: 58S  fable51: 37S   0  -0.40
  11 9708     amc          31 short   16  opus5: 36S  opus55: 42S  sonnet55:  4S  fable51: 44S   0  -0.36
  12 9551     amc          30 long     8  opus5: 30L  opus55: 18L  sonnet55: 41L  fable51: 32L   0  +0.32
  13 9502     amc          33 long    14  opus5: 34L  opus55: 50L  sonnet55: 38L  fable51: 10L   0  +0.32
  14 9474     amc          30 short    8  opus5: 30S  opus55: 16S  sonnet55: 37S  fable51: 37S   0  -0.30
  15 9532     amc          34 short   12  opus5: 19S  opus55: 31S  sonnet55: 34S  fable51: 54S   0  -0.28
  16 4347     amc          22 long    19  opus5: 30L  opus55: 29L  sonnet55: 38L  fable51: 10S   0  +0.27
  17 9046     amc          32 short   19  opus5: 16S  opus55: 18S  sonnet55: 32S  fable51: 63S   0  -0.23
  18 6419     amc          25 short   10  opus5: 30S  opus55: 16S  sonnet55: 38S  fable51: 15S   0  -0.22
  19 7962     amc          20 long    10  opus5: 30L  opus55: 29L  sonnet55:  7L  fable51: 15L   0  +0.22
  20 6822     amc          18 long    10  opus5: 34L  opus55: 18L  sonnet55: 13L  fable51:  8L   0  +0.16
  21 4502     amc          18 short    7  opus5: 16S  opus55: 16S  sonnet55:  9S  fable51: 29S   0  -0.16
  22 2594     amc          11 long     6  opus5:  8L  opus55:  4L  sonnet55: 18L  fable51: 14L   0  +0.14
  23 6810     amc          20 short   30  opus5: 30S  opus55:  4L  sonnet55:  9L  fable51: 65S   0  -0.09
  24 4366     amc          10 long    18  opus5: 16L  opus55:  0-  sonnet55: 13S  fable51: 37L   0  +0.08
  25 8706     amc           0 -        0  opus5:  0-  opus55:  0-  sonnet55:  0-  fable51:  0-   0  +0.00
```

(`score` is the old z-based `panel_score`; `pct` is `panel_pct`, the number to report.)

**Selected:**
- **1946 Toenec, long, 4 of 4.** The judges named the same evidence as the hunter: a full-year plan implying a flat H2 after Q1 OP +47.6% and standalone orders +31.5%, a company that raised at the H1 print in each of the last two years (+20.4% last year), a ~40% payout policy that lifts the dividend with any raise, and peers ユアテック and 北陸電工 printing the same margin driver on 10-28. The case against: the stock ran +8.2% in five days into a 15.7x margin long, and 北陸電工 beat, held its plan and fell.
- **3116 Toyota Boshoku, short, 3 of 4 (Fable 5.1 at 75).** The evidence: a 76bn OP plan, already cut once at Q1, that needs ~60bn over Q2-Q4 after a 15.9bn Q1, against an IFIS consensus still at or above plan; Toyota's August global output -5.9% and China sales -23%; and Toyota-group peer Chuo Hatsujo cutting 45% on 10-28. The last two cuts traded -5.2% and -7.4%. The case against: eight sell-side target cuts and -8% over 20 days, the yen ~158 against a 150 assumption gives room to hold, and a possible buyback absorbing Toyota Industries' 4.13% (unsourced).
- **6471 NSK, long, 3 of 4 (Sonnet 5.5 at 78).** The evidence: Q1 OP was 57.5% of the H1 guide, the guide implies Q2 and H2 quarters below Q1, the yen is weaker than the 155 assumption, September machine-tool orders were +60.4% and FANUC raised on 10-23, while consensus has sat 4.7% above guide for four weeks and the stock fell 14%. The case against: 信用倍率 28.8x, the Q1 raise lagged the Nikkei (+1.95% vs +4.03%), and the NTN merger ratio is due around 11-12.

**Where the panel and the hunters disagree most:**
- 6810 Maxell: hunter +1.00 (4th), panel short at 20 with the widest spread of the day (sd 30) — Opus 5 and Fable 5.1 short, Opus 5.5 and Sonnet 5.5 mildly long.
- 9502 Chubu Electric: hunter -0.10, panel long at 33 (the wheeling-revenue revision weighed more than the fuel time-lag).
- 6345 Aichi Corp and 4502 Takeda: hunter slightly positive, panel short.
- 4366 Daito Chemix: hunter -0.30, panel mildly long (10).
- No name clears the 2.8 conviction floor, so there is no floor-vs-panel disagreement to report.

**A sizing-rule conflict in the judge definition, recorded rather than fixed.** The Opus 5.5 judge reported that its definition (`config/panel-judge-intl.md`) tells it to make the findings add up to (2·p_up/100 − 1)·abs_move_pct, while `config/hunter-core.md` says each finding is sized on its own. It followed the judge definition, and Opus 5 and Fable 5.1 reported doing the same. The panel reads each judge against its own history, so this matters only if the rule changed recently; it should be checked by someone building, not by a Routine session.

**What the panel numbers are not:** `panel_pct` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing. The member scales now read off ~198 live sizes each, still mostly from before this market had its own history. In the four-model re-judge the judges ranked Japan **worse** than the live hunt. And on the last resolved day, 2026-10-27, the JP panel ranked at ρ −0.48 (p 0.01) with its six selected names 1 right at −6.2% mean signed: nothing about this market's panel is established, and that day argues against it.

## The finding and URL driving the top and bottom name

- **Top, 1946 Toenec (+1.70):** guidance, +2.0 — the FY plan (OP 24,000m) implies a flat H2 against Q1 OP +47.6% and orders +31.5%, and the company raised its FY at the H1 print in each of the last two years. https://kabutan.jp/stock/finance?code=1946
- **Bottom, 9202 ANA (−1.00, tied with 3116):** guidance, −1.2 — the FY plan assumes Singapore kerosene of $120 in Q2 and $90 in H2, while ANA's own surcharge filing puts the Aug–Sep average near $160, and the Q1 deck said Q2 would be folded into the H2 assumptions, against an IFIS OP consensus 9% above plan. https://www.ana.co.jp/group/investors/data/kessan/pdf/2026_07_1.pdf
- **Also bottom, 3116 Toyota Boshoku (−1.00):** guidance, −1.2 — a second cut likely with consensus still at or above plan. https://kabuyoho.jp/report?bcode=3116

## Names that could not be ranked

None. All 25 hunts returned, all 25 events were confirmed for today, and all 25 are rankable. 8706 Kyokuto ranks at exactly 0: its H1 numbers were pre-released as a 速報値 on 10-15 (−8.0% that day), so the formal print adds nothing.

## Every-day caveats

- **No option anchor; substituted.** `priced_lean_pct` and `anchor_quality` come from the JPX short register (level and change) and 信用倍率. Direction quality was 0.60 for 22 names and 0.45 for the three without a margin ratio. **The weights in `lean_components()` are priors with no Japanese measurement behind them.** Short-squeeze and short-building components resolved only where a position exists (5 names); for the other 20 the register is a real zero, so the lean is margin overhang plus run-up.
- **`lean_vs_free_control_rho`, last resolved run (2026-10-27, resolved this morning): 0.435** on 25 names, inside the 0.4–0.6 band, so the lean has not collapsed back into the run-up (10-26 read 0.70 on 5).
- **`history` is an estimated cadence**, a scale and not a record of dates. Several hunters found it wrong on this day (6810's "−4.24% on 07-28" was really +24% limit-up on 07-31; 6345's real-date median was 2.07% against the baseline's 4.31%; 9532's 04-30 row is not a print). Never cite one of its dates.
- **Signs:** 13 positive, 1 zero, 11 negative. The first resolved days were five of seven negative; this day is not.
- **Conviction floor 2.8: no name clears it.** The largest |impact_sum| is 1.70. Over the whole US sample the sign was a coin flip below the floor, so every number here is in that regime.
- **Daily price limits** (値幅制限) truncate the tail: a large finding may be right and still not be paid in full in one session.
- **Correlated exposure.** Five names are Toyota-group or auto (3116, 5482, 6902, 7259, plus the read-through in 6471); the Tokai Rika and Chuo Hatsujo prints of 10-28 drive several findings at once. Not independent draws.
- **One day is not a result.**

## Resolved this morning

- **2026-10-27:** 25/25 usable; `impact_sum` ρ −0.313 (p 0.125); free control −run_up_20d ρ 0.055; sign right 40%; `lean_vs_free_control_rho` 0.435. Panel: `panel_pct` ρ −0.483 (p 0.01), 6 selected, 1 right, mean signed −6.22%. One day; pool before reading anything.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone. This stage places no orders.
