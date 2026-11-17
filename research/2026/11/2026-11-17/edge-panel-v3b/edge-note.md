# Stage E-P v3b — 2026-11-17 amc + 2026-11-18 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.** All four judges ran on their pinned models (panel-judge-v3b-opus5 / -opus55 / -sonnet55 / -fable51; no fallback, no judge missing). One day is an anecdote: the comparison with stage E-P is judged only by `v3b_compare.py`, pooled, from 20 run days.

- Window: 32 names (12 amc 2026-11-17, 20 bmo 2026-11-18). This stage's own sweep confirmed 29 (KNDI phantom, CAAP and CISS unconfirmed); SQM's release hour is unsettled (call 11-18 10:00 ET, reaction lands in the 11-18 session either way).
- Hunted 20 by `hunt_priority` (cap 20); shed TJX IRIX ZTO NVDA GLNG HAFN GBDC GLAD ZIM.
- Searchers: `unpriced-searcher-v3b` named agent on all 20, no fallback. All 20 `search_complete: true`, none retried. **All 20 carry the v3b fields** (`expectations`, `next_guide`, `evidence_type` on every finding).
- Packs: 20, one file. Coverage 20/20 for every judge.

## The panel (own history, `panel-history-v3b.json`)

Selected: **BRBR, short** (panel_pct 89, all four judges in their own top 20% on the short side). Nothing else reaches 80.

| # | ticker | session | sel | panel_pct | side | sd | pct on E-P scale | members (own pct, L/S, * = own top 20%) | k | E[return] | P(right) | judges' mean p_clears_real_bar | most common guide_direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BRBR | bmo | yes | 89 | short | 5 | 88 | opus5:91S* opus55:81S* sonnet55:94S* fable51:91S* | 4 | +3.98% | 0.679 | 39 | initiate |
| 2 | GLBE | bmo |  | 75 | short | 5 | 73 | opus5:70S opus55:70S sonnet55:77S fable51:83S* | 1 | +2.01% | 0.566 | 39 | raise |
| 3 | KRNT | bmo |  | 63 | short | 2 | 60 | opus5:61S opus55:62S sonnet55:61S fable51:67S | 0 | +1.03% | 0.56 | 38 | maintain |
| 4 | FEAM | amc |  | 61 | short | 21 | 59 | opus5:32S opus55:55S sonnet55:92S* fable51:66S | 1 | +0.91% | 0.56 | 40 | maintain |
| 5 | PONY | bmo |  | 61 | long | 17 | 58 | opus5:39L opus55:84L* sonnet55:70L fable51:50L | 1 | +0.86% | 0.56 | 52 | maintain |
| 6 | LZB | amc |  | 60 | short | 2 | 58 | opus5:61S opus55:62S sonnet55:61S fable51:57S | 0 | +0.83% | 0.56 | 44 | cut |
| 7 | JMIA | bmo |  | 56 | long | 14 | 53 | opus5:67L opus55:42L sonnet55:44L fable51:72L | 0 | +0.48% | 0.56 | 55 | maintain |
| 8 | ENRD | bmo |  | 53 | short | 12 | 50 | opus5:43S opus55:50S sonnet55:74S fable51:44S | 0 | +0.34% | 0.56 | 42 | maintain |
| 9 | IIIV | amc |  | 52 | short | 12 | 49 | opus5:68S opus55:44S sonnet55:56S fable51:38S | 0 | +0.32% | 0.56 | 42 | initiate |
| 10 | DLB | amc |  | 49 | short | 17 | 46 | opus5:48S opus55:72S sonnet55:50S fable51:24S | 0 | +0.29% | 0.56 | 43 | initiate |
| 11 | CSHR | bmo |  | 38 | long | 14 | 36 | opus5:30L opus55:60L sonnet55:42L fable51:24L | 0 | +0.29% | 0.56 | 53 | no_guide |
| 12 | AUNA | amc |  | 34 | long | 10 | 31 | opus5:36L opus55:42L sonnet55:42L fable51:18L | 0 | +0.29% | 0.56 | 56 | maintain |
| 13 | PRE | bmo |  | 28 | long | 19 | 26 | opus5:26L opus55:50L sonnet55:2S fable51:38L | 0 | +0.29% | 0.56 | 48 | maintain |
| 14 | ICCM | bmo |  | 28 | short | 28 | 26 | opus5:10L opus55:12S sonnet55:64S fable51:44S | 0 | +0.29% | 0.56 | 41 | no_guide |
| 15 | SQM | amc |  | 17 | long | 15 | 15 | opus5:35L opus55:27L sonnet55:4S fable51:9L | 0 | +0.29% | 0.56 | 51 | cut |
| 16 | LOW | bmo |  | 16 | long | 18 | 15 | opus5:9L opus55:47L sonnet55:4L fable51:4L | 0 | +0.29% | 0.56 | 52 | maintain |
| 17 | JJSF | bmo |  | 11 | long | 31 | 10 | opus5:26L opus55:50L sonnet55:34S fable51:0S | 0 | +0.29% | 0.56 | 49 | maintain |
| 18 | ZKH | bmo |  | 8 | long | 19 | 7 | opus5:20S opus55:24L sonnet55:25L fable51:0S | 0 | +0.29% | 0.56 | 50 | maintain |
| 19 | TGT | bmo |  | 4 | short | 28 | 4 | opus5:35S opus55:34L sonnet55:25S fable51:9L | 0 | +0.29% | 0.56 | 47 | maintain |
| 20 | BLSH | bmo |  | 3 | long | 40 | 3 | opus5:23S opus55:34L sonnet55:48S fable51:50L | 0 | +0.29% | 0.56 | 44 | maintain |

`expected_return_pct` is **stage E-P's calibration curve** (fitted 2026-10-14 on 148 resolved E-P names), not one fitted on v3b: it is the translation of the percentile, gross, on the scorebord window, flat at about +0.3% below a percentile of 50, with a weak out-of-sample record (correlation +0.12). It is not a forecast to size on. The searcher's own `impact_sum` is in the score_report table below; `p_up` is recorded and decides nothing.

Panel output as printed by the second `panel_score.py` call:

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 80 sizes added to the history
own top 20% starts at: opus5 |2.52|, opus55 |1.68|, sonnet55 |1.60|, fable51 |2.00|  (live sizes before 2026-11-17, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 BRBR     bmo     yes  89 short    5  opus5: 91S* opus55: 81S* sonnet55: 94S* fable51: 91S*  4  -1.66  +3.98% [+1.88, +5.94]           0.68
   2 GLBE     bmo          75 short    5  opus5: 70S  opus55: 70S  sonnet55: 77S  fable51: 83S*  1  -1.12  +2.01% [+0.37, +3.83]           0.57
   3 KRNT     bmo          63 short    2  opus5: 61S  opus55: 62S  sonnet55: 61S  fable51: 67S   0  -0.85  +1.03% [-0.03, +2.57]           0.56
   4 FEAM     amc          61 short   21  opus5: 32S  opus55: 55S  sonnet55: 92S* fable51: 66S   1  -0.78  +0.91% [-0.09, +2.40]           0.56
   5 PONY     bmo          61 long    17  opus5: 39L  opus55: 84L* sonnet55: 70L  fable51: 50L   1  +0.79  +0.86% [-0.11, +2.34]           0.56
   6 LZB      amc          60 short    2  opus5: 61S  opus55: 62S  sonnet55: 61S  fable51: 57S   0  -0.77  +0.83% [-0.12, +2.29]           0.56
   7 JMIA     bmo          56 long    14  opus5: 67L  opus55: 42L  sonnet55: 44L  fable51: 72L   0  +0.73  +0.48% [-0.25, +1.97]           0.56
   8 ENRD     bmo          53 short   12  opus5: 43S  opus55: 50S  sonnet55: 74S  fable51: 44S   0  -0.63  +0.34% [-0.34, +1.69]           0.56
   9 IIIV     amc          52 short   12  opus5: 68S  opus55: 44S  sonnet55: 56S  fable51: 38S   0  -0.56  +0.32% [-0.38, +1.58]           0.56
  10 DLB      amc          49 short   17  opus5: 48S  opus55: 72S  sonnet55: 50S  fable51: 24S   0  -0.64  +0.29% [-0.44, +1.36]           0.56
  11 CSHR     bmo          38 long    14  opus5: 30L  opus55: 60L  sonnet55: 42L  fable51: 24L   0  +0.43  +0.29% [-0.52, +0.91]           0.56
  12 AUNA     amc          34 long    10  opus5: 36L  opus55: 42L  sonnet55: 42L  fable51: 18L   0  +0.43  +0.29% [-0.55, +0.87]           0.56
  13 PRE      bmo          28 long    19  opus5: 26L  opus55: 50L  sonnet55:  2S  fable51: 38L   0  +0.43  +0.29% [-0.57, +0.85]           0.56
  14 ICCM     bmo          28 short   28  opus5: 10L  opus55: 12S  sonnet55: 64S  fable51: 44S   0  -0.39  +0.29% [-0.57, +0.85]           0.56
  15 SQM      amc          17 long    15  opus5: 35L  opus55: 27L  sonnet55:  4S  fable51:  9L   0  +0.24  +0.29% [-0.63, +0.81]           0.56
  16 LOW      bmo          16 long    18  opus5:  9L  opus55: 47L  sonnet55:  4L  fable51:  4L   0  +0.14  +0.29% [-0.64, +0.81]           0.56
  17 JJSF     bmo          11 long    31  opus5: 26L  opus55: 50L  sonnet55: 34S  fable51:  0-   0  +0.19  +0.29% [-0.68, +0.80]           0.56
  18 ZKH      bmo           8 long    19  opus5: 20S  opus55: 24L  sonnet55: 25L  fable51:  0-   0  +0.14  +0.29% [-0.71, +0.79]           0.56
  19 TGT      bmo           4 short   28  opus5: 35S  opus55: 34L  sonnet55: 25S  fable51:  9L   0  -0.05  +0.29% [-0.73, +0.78]           0.56
  20 BLSH     bmo           3 long    40  opus5: 23S  opus55: 34L  sonnet55: 48S  fable51: 50L   0  +0.01  +0.29% [-0.74, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

## The selected name

**BRBR (BellRing Brands), short, panel_pct 89.** All four judges size it the same way: a first FY27 guide from a new CEO (Mike Axelrod, since 2026-07-29) against a street FY27 EPS of about +25% (single source, S&P Global via stockanalysis.com), into a stock that ran +14.7% over 20 days, with six of its last seven prints down. Opus 5 -3.4, Opus 5.5 -1.7, Sonnet 5.5 -2.72, Fable 5.1 -2.6 (impact_sum); p_up 40-45; abs_move about 17%. Judges' mean p_clears_real_bar 39%, guide_direction "initiate".
**Case against:** the searcher's own sum was +0.40 (p_up 52), because five analysts cut targets into the print (two below spot), short interest rose 19% to 12.7% of shares outstanding, and peer Simply Good Foods rose 11.4% on its own reset FY27 guide on 2026-10-28. The FY27 consensus has one source. A guide that only resets to the street, after the target cuts, could squeeze a 12.7% short.

## Where the panel and the searcher disagree most

- BRBR: searcher +0.40 (long lean), panel short 89. The judges weight the guide initiation and run-up; the searcher netted them against target cuts and shorts.
- PONY: searcher +2.60 (p95, the day's largest positive), panel long 61, not selected: Opus 5 and Fable 5.1 sit at 39 and 50.
- IIIV: searcher +0.40, panel short 52 (Opus 5 alone at 68S, -1.98).
- ICCM: searcher -2.40, panel short only 28 (Opus 5 leans long).
- GLBE: the only name above the searcher's 2.8 floor (-2.80); panel short 75, not selected.

## Comparison with stage E-P (same day, its own sweep and searchers)

```
v3b 20 ep 20 both 18
ep only ['ZIM', 'ZTO'] v3b only ['AUNA', 'LOW']
rho panel_pct_signed v3b vs EP on 18 names: 0.059
select keys ['selected_consensus', 'selected_mean_pct', 'selected']
selected v3b [] | v3b on epscale [] | EP [] | overlap []
BRBR  v3b  89.2 short | epscale  88.1 | EP   6.6 short  
GLBE  v3b  75.0 short | epscale  73.0 | EP  60.1 long  SIDE  
KRNT  v3b  62.9 short | epscale  60.4 | EP  13.6 short  
FEAM  v3b  61.2 short | epscale  59.4 | EP  82.4 short  
PONY  v3b  60.6 long  | epscale  58.4 | EP  33.6 long   
LZB   v3b  60.1 short | epscale  57.8 | EP  61.6 short  
JMIA  v3b  56.1 long  | epscale  53.0 | EP  83.8 short SIDE  
ENRD  v3b  52.8 short | epscale  50.2 | EP  74.2 short  
IIIV  v3b  51.5 short | epscale  48.8 | EP  42.1 long  SIDE  
DLB   v3b  48.6 short | epscale  46.0 | EP  30.2 short  
CSHR  v3b  38.5 long  | epscale  35.6 | EP  14.2 long   
PRE   v3b  27.9 long  | epscale  25.5 | EP  52.1 long   
ICCM  v3b  27.6 short | epscale  26.5 | EP  83.5 short  
SQM   v3b  16.8 long  | epscale  15.1 | EP  44.1 short SIDE  
JJSF  v3b  10.6 long  | epscale   9.8 | EP  43.5 long   
ZKH   v3b   7.5 long  | epscale   6.9 | EP  16.8 long   
TGT   v3b   4.1 short | epscale   4.0 | EP  35.2 long  SIDE  
BLSH  v3b   3.0 long  | epscale   3.1 | EP  64.4 short SIDE
```

- Names both ranked: 18 (E-P only: ZIM, ZTO; v3b only: AUNA, LOW, because the two sweeps gave different hunt_priority).
- **Selected sets do not overlap.** v3b: BRBR short. E-P: FEAM, ICCM, JMIA (all short).
- **Spearman ρ between the two `panel_pct_signed` columns: +0.06 on 18 names.** The two panels barely agree on today's order.
- Disagree on side (6): GLBE (v3b short 75 / E-P long 60), JMIA (v3b long 56 / E-P short 84, selected), IIIV, SQM, TGT, BLSH.
- Disagree on selection: BRBR (v3b 89 / E-P 7, both short); FEAM (E-P 82 / v3b 61, both short); ICCM (E-P 84 / v3b 28, both short); JMIA (E-P 84 short / v3b 56 long).
- The E-P-scale scoring (`edge-scores-panel-epscale.json`) selects the same single name, BRBR (88), so today's gap is in the judging, not in the v3b history's scale.

## Searcher table

```
**Stage E-P v3b (searcher), 2026-11-17**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
V2 at `session_close`, matrix as of 2026-11-17T18:12:06+00:00.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=957, impact_scaled n=974): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up | V2 grounded | retail ≥50 | search quiet | vol ≥58 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PONY | bmo | **+2.60** (p95) | no | +1.08 (p87) | 9.0 | 56 | +3.33 | yes (63) | n/a (sparse) | yes (59) |
| 2 | CSHR | bmo | **+1.40** (p82) | no | +0.36 (p53) | 6.0 | 53 | +1.80 | yes (64) | n/a (sparse) | yes (68) |
| 3 | JMIA | bmo | **+1.30** (p80) | no | +0.62 (p72) | 15.5 | 52 | +1.49 | yes (72) | n/a (failed) | yes (62) |
| 4 | AUNA | amc | **+0.40** (p39) | no | -0.10 (p20) | 5.0 | 49 | -0.05 | yes (56) | yes (0.88x) | no (42) |
| 5 | BRBR | bmo | **+0.40** (p39) | no | +0.68 (p75) | 17.0 | 52 | +0.82 | yes (74) | n/a (sparse) | yes (61) |
| 6 | IIIV | amc | **+0.40** (p39) | no | -0.88 (p83) | 11.0 | 46 | -0.03 | yes (56) | n/a (sparse) | no (36) |
| 7 | TGT | bmo | **+0.40** (p39) | no | +0.42 (p58) | 7.0 | 53 | +0.25 | no (32) | no (1.03x) | no (40) |
| 8 | BLSH | bmo | **+0.30** (p31) | no | +0.23 (p37) | 11.5 | 51 | -1.33 | yes (60) | yes (0.92x) | yes (91) |
| 9 | JJSF | bmo | **+0.10** (p14) | no | +0.42 (p58) | 7.0 | 53 | -0.03 | no (42) | n/a (sparse) | no (30) |
| 10 | LOW | bmo | **+0.05** (p9) | no | +0.23 (p37) | 3.8 | 53 | -0.09 | no (28) | yes (0.84x) | no (42) |
| 11 | SQM | amc | **-0.00** (p4) | no | +0.14 (p26) | 7.0 | 51 | -0.73 | no (36) | n/a (sparse) | no (49) |
| 12 | ZKH | bmo | **-0.30** (p31) | no | +0.80 (p80) | 10.0 | 54 | -0.78 | yes (67) | n/a (sparse) | yes (95) |
| 13 | ENRD | bmo | **-0.50** (p46) | no | -0.72 (p77) | 9.0 | 46 | -0.34 | yes (64) | n/a (failed) | yes (86) |
| 14 | PRE | bmo | **-0.50** (p46) | no | +0.00 (p6) | 8.0 | 50 | -0.18 | yes (70) | n/a (failed) | yes (74) |
| 15 | KRNT | bmo | **-1.00** (p72) | no | -0.26 (p41) | 6.5 | 48 | -1.45 | yes (52) | n/a (sparse) | no (40) |
| 16 | DLB | amc | **-1.30** (p80) | no | -0.51 (p66) | 8.5 | 47 | -0.98 | no (34) | n/a (sparse) | no (23) |
| 17 | LZB | amc | **-1.30** (p80) | no | -1.25 (p90) | 12.5 | 45 | -0.93 | yes (57) | no (1.07x) | no (42) |
| 18 | ICCM | bmo | **-2.40** (p94) | no | -0.90 (p84) | 9.0 | 45 | -5.05 | yes (98) | n/a (failed) | yes (111) |
| 19 | FEAM | amc | **-2.50** (p94) | no | -1.20 (p90) | 15.0 | 46 | -6.71 | yes (78) | n/a (failed) | yes (100) |
| 20 | GLBE | bmo | **-2.80** (p96) | yes | -0.88 (p83) | 11.0 | 46 | -2.52 | no (43) | n/a (failed) | no (43) |

Not ranked: CAAP: no hunt

Not ranked: CISS: no hunt

Not ranked: GBDC: no hunt

Not ranked: GLAD: no hunt

Not ranked: GLNG: no hunt

Not ranked: HAFN: no hunt

Not ranked: IRIX: no hunt

Not ranked: KNDI: no hunt

Not ranked: NVDA: no hunt

Not ranked: TJX: no hunt

Not ranked: ZIM: no hunt

Not ranked: ZTO: no hunt

`session` is when the print lands: `amc` after the close, `bmo` before the open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).
`impact_scaled` is the hunter's second, separate measurement, (2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.
`retail`, `search` and `vol` are context for the reader, shown for every name whatever its score: retail tilt ≥ 50, a Google search spike under 1.0x on the last complete day, and 20-day realised volatility ≥ 58% annualised. Nothing ranks, selects, sizes or trades on them.
```

## Standing caveats

- Nothing checked the findings: no adversary, no second searcher. A factually wrong finding reaches the judges at face value.
- The key is not reproducible to better than its own size (the double hunt measured a 2.40-point median gap with opposite signs on 4 of 12 pairs).
- Sign balance of the searcher's sums: 10 positive, 1 zero, 9 negative.
- Most names have no usable option chain, so the baseline's expected move is a historical median, not a priced one; several searchers rebuilt the reaction history because the baseline's was built from non-earnings 6-Ks.
- Context labels (retail, search, volatility) are in the searcher table; context only, nothing selects on them.
- V2 grounded was written before the first print (`edge-scores-grounded.json`).
- This stage places no orders, and `alpaca_trade.py` was not run in any form.

This is a forecasting exercise over public information. It is research, not investment advice.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
