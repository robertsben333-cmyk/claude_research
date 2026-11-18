# Stage E-P v3b — 2026-11-18 amc + 2026-11-19 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.** All four judges ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1). One day is an anecdote; v3b is judged only pooled by `v3b_compare.py` from 20 run days.

**Nothing is selected today.** The highest `panel_pct` is RERE at 74 (short) on this stage's own history, 71 on stage E-P's scale; the rule is >= 80 with all four judges.

## Panel (own history, `panel-history-v3b.json`), as `panel_score.py` printed it

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 80 sizes added to the history
own top 20% starts at: opus5 |2.40|, opus55 |1.68|, sonnet55 |1.60|, fable51 |1.96|  (live sizes before 2026-11-18, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 RERE     bmo          74 short    6  opus5: 64S  opus55: 78S  sonnet55: 74S  fable51: 81S*  1  -1.09  +1.92% [+0.34, +3.71]           0.56
   2 KLIC     amc          71 long    18  opus5: 45L  opus55: 90L* sonnet55: 64L  fable51: 86L*  2  +1.09  +1.65% [+0.25, +3.37]           0.56
   3 BBWI     bmo          66 long    13  opus5: 55L  opus55: 80L  sonnet55: 79L  fable51: 52L   1  +1.01  +1.29% [+0.09, +2.90]           0.56
   4 MMS      bmo          65 short   12  opus5: 48S  opus55: 64S  sonnet55: 80S* fable51: 69S   0  -0.91  +1.18% [+0.04, +2.77]           0.56
   5 VVV      bmo          55 short    9  opus5: 42S  opus55: 58S  sonnet55: 68S  fable51: 54S   0  -0.68  +0.40% [-0.28, +1.89]           0.56
   6 BABA     bmo          55 long     6  opus5: 45L  opus55: 60L  sonnet55: 61L  fable51: 54L   0  +0.71  +0.38% [-0.29, +1.86]           0.56
   7 DAO      bmo          47 short   12  opus5: 28S  opus55: 44S  sonnet55: 56S  fable51: 60S   0  -0.55  +0.29% [-0.46, +1.22]           0.56
   8 LQDT     bmo          46 long    14  opus5: 26L  opus55: 64L  sonnet55: 50L  fable51: 46L   0  +0.58  +0.29% [-0.47, +1.19]           0.56
   9 JOYY     amc          41 long    20  opus5: 10L  opus55: 46L  sonnet55: 64L  fable51: 46L   0  +0.56  +0.29% [-0.51, +0.97]           0.56
  10 BORR     amc          40 long    14  opus5: 34L  opus55: 64L  sonnet55: 25L  fable51: 35L   0  +0.46  +0.29% [-0.52, +0.92]           0.56
  11 RRGB     amc          39 long    43  opus5: 60L  opus55: 85L* sonnet55: 43L  fable51: 32S   1  +0.68  +0.29% [-0.52, +0.91]           0.56
  12 HP       amc          38 long    15  opus5: 42L  opus55: 44L  sonnet55: 13L  fable51: 54L   0  +0.53  +0.29% [-0.53, +0.91]           0.56
  13 MAGN     bmo          36 long    17  opus5: 10L  opus55: 46L  sonnet55: 56L  fable51: 35L   0  +0.49  +0.29% [-0.54, +0.89]           0.56
  14 FUTU     bmo          30 long    16  opus5: 14L  opus55: 38L  sonnet55: 52L  fable51: 16L   0  +0.34  +0.29% [-0.56, +0.85]           0.56
  15 SBLK     amc          29 long    16  opus5:  2L  opus55: 44L  sonnet55: 32L  fable51: 39L   0  +0.43  +0.29% [-0.56, +0.85]           0.56
  16 WWD      amc          28 short   26  opus5: 11L  opus55: 23S  sonnet55: 61S  fable51: 38S   0  -0.39  +0.29% [-0.57, +0.85]           0.56
  17 TEN      bmo          24 long    12  opus5: 29L  opus55:  8L  sonnet55: 40L  fable51: 20L   0  +0.36  +0.29% [-0.58, +0.84]           0.56
  18 UTI      amc          24 long    48  opus5: 52S  opus55: 53L  sonnet55: 75L  fable51: 21L   0  +0.47  +0.29% [-0.58, +0.84]           0.56
  19 WSM      bmo          19 short   11  opus5: 20S  opus55: 30S  sonnet55:  0-  fable51: 26S   0  -0.33  +0.29% [-0.61, +0.82]           0.56
  20 P        amc          17 long    50  opus5: 68S  opus55: 53L  sonnet55: 40L  fable51: 42L   0  +0.48  +0.29% [-0.63, +0.81]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

## Panel with the v3b columns

`pct E-P scale` is the same judges' sizes read against stage E-P's judges' live range (`edge-scores-panel-epscale.json`). `p_clears` is the judges' mean `p_clears_real_bar`; `guide` the most common `guide_direction`. `E[ret]` is stage E-P's calibration curve (gross, scorebord window, flat at about +0.3% below a percentile of 50), not one fitted on v3b: the translation of the percentile, not a separate forecast.

| # | ticker | panel_pct | side | sd | pct E-P scale | p_clears | guide | consensus_k | E[ret] (80%) | p_right |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RERE | 74 | short | 6 | 71 | 40 | maintain | 1 | +1.92% [+0.34, +3.71] | 0.56 |
| 2 | KLIC | 71 | long | 18 | 68 | 57 | maintain | 2 | +1.65% [+0.25, +3.37] | 0.56 |
| 3 | BBWI | 66 | long | 13 | 63 | 57 | maintain | 1 | +1.29% [+0.09, +2.90] | 0.56 |
| 4 | MMS | 65 | short | 12 | 61 | 40 | initiate | 0 | +1.18% [+0.04, +2.77] | 0.56 |
| 5 | VVV | 55 | short | 9 | 50 | 42 | initiate | 0 | +0.40% [-0.28, +1.89] | 0.56 |
| 6 | BABA | 55 | long | 6 | 50 | 56 | maintain | 0 | +0.38% [-0.29, +1.86] | 0.56 |
| 7 | DAO | 47 | short | 12 | 43 | 44 | no_guide | 0 | +0.29% [-0.46, +1.22] | 0.56 |
| 8 | LQDT | 46 | long | 14 | 42 | 54 | raise | 0 | +0.29% [-0.47, +1.19] | 0.56 |
| 9 | JOYY | 41 | long | 20 | 38 | 54 | raise | 0 | +0.29% [-0.51, +0.97] | 0.56 |
| 10 | BORR | 40 | long | 14 | 36 | 51 | cut | 0 | +0.29% [-0.52, +0.92] | 0.56 |
| 11 | RRGB | 39 | long | 43 | 38 | 52 | cut | 1 | +0.29% [-0.52, +0.91] | 0.56 |
| 12 | HP | 38 | long | 15 | 35 | 54 | initiate | 0 | +0.29% [-0.53, +0.91] | 0.56 |
| 13 | MAGN | 36 | long | 17 | 33 | 52 | initiate | 0 | +0.29% [-0.54, +0.89] | 0.56 |
| 14 | FUTU | 30 | long | 16 | 28 | 55 | maintain | 0 | +0.29% [-0.56, +0.85] | 0.56 |
| 15 | SBLK | 29 | long | 16 | 26 | 55 | raise | 0 | +0.29% [-0.56, +0.85] | 0.56 |
| 16 | WWD | 28 | short | 26 | 25 | 47 | initiate | 0 | +0.29% [-0.57, +0.85] | 0.56 |
| 17 | TEN | 24 | long | 12 | 22 | 53 | raise | 0 | +0.29% [-0.58, +0.84] | 0.56 |
| 18 | UTI | 24 | long | 48 | 22 | 50 | initiate | 0 | +0.29% [-0.58, +0.84] | 0.56 |
| 19 | WSM | 19 | short | 11 | 18 | 46 | maintain | 0 | +0.29% [-0.61, +0.82] | 0.56 |
| 20 | P | 17 | long | 50 | 13 | 48 | raise | 0 | +0.29% [-0.63, +0.81] | 0.56 |

## Closest to selection (no name selected)

- **RERE, short, 74 (sd 6).** The tightest agreement of the day: all four judges short, Fable 5.1 in its own top 20%. Evidence the judges name: the stock trades on the next-quarter guide, not the beat (the three 2026 prints moved -10.1%, +11.6%, -11.1%); China telecom-equipment retail slowed from +31.1% in September to +6.5% in October; the Q4 street implies about +18-22% growth against a +29% comparison. Case against: ATRenew has beaten the top of its own revenue guide three quarters running, used-phone prices are rising on memory costs, and the searcher's own key is only -0.30. Judges' mean p_clears_real_bar 40.
- **KLIC, long, 71 (sd 18).** Opus 5.5 and Fable 5.1 in their own top 20%. Evidence: stock about 50% off its high and below every target; record wire-bond shipments and a new CEO saying demand is improving; ASE, Amkor and Chinese OSAT customers raising capex. Case against: put skew +19 vol points, ASMPT and Besi guiding flat, a new CEO's first guide may reset low, and the August beat-and-raise was sold.
- **BBWI, long, 66.** Guide-beating record, a 10% fall in four sessions with no company news, Simon's mall traffic. Against: put skew +8.8, a full-year guide implying a soft Q4.
- **MMS, short, 65.** The FY27 first guide likely below the street (Q4 run rate x4 is about $7.64 against $8.36), Leidos on the same VA programme calling 2027 "not a bottom line growth year", a 23% run into the print.

## Where the panel and the searcher disagree most

- **UTI**: searcher key +1.70 (third on the day), panel 24 long with the widest spread (sd 48): Opus 5 short, Sonnet 5.5 long at 75. The searcher's own scaled number is -0.56.
- **P**: searcher +1.10, panel 17 long with sd 50; Opus 5 short at 68 on the three-for-three "beat sold on cash flow" pattern.
- **RERE**: searcher -0.30, panel the day's strongest name at 74 short.
- **RRGB**: Opus 5.5 at 85 long, Fable 5.1 short; panel 39.

## Comparison with stage E-P (same afternoon, separate sweep and searchers)

Stage E-P's `edge-scores-panel.json` was on `main` when this note was written.

- Names both ranked: **13** (BBWI DAO FUTU JOYY KLIC MAGN MMS P RERE RRGB UTI VVV WWD). v3b only: BABA BORR HP LQDT SBLK TEN WSM. E-P only: ARBE CPA EVAX PCYO PDD SNEX YMM. The two sweeps ordered `hunt_priority` differently, so the 20-name cut differs.
- Selected sets: v3b none; E-P **RRGB** (88 long) and **ARBE** (not hunted here). Overlap: none.
- Spearman ρ between the two `panel_pct_signed` columns on the 13 shared names: **+0.555** (same ranks on stage E-P's scale).
- Disagreements, one line each:
  - RRGB: E-P selected at 88 long; v3b 39 long (Opus 5.5 85 long, Fable 5.1 short).
  - RERE: E-P 14 long; v3b 74 short (opposite side).
  - KLIC: E-P 11 long; v3b 71 long.
  - MAGN: E-P 31 short; v3b 37 long (opposite side).
  - UTI: E-P 22 short; v3b 24 long (opposite side).
  - MMS: E-P 78 short; v3b 65 short (same side, both below 80).

## Run notes

- Window: 38 names (17 amc 2026-11-18, 21 bmo 2026-11-19). Sweep confirmed 36 (WMG, BEEM unconfirmed). 20 hunted by `hunt_priority`, 18 shed: YMM SNEX PDD CPA PCYO UGI MANU ROAD PANW ARBE NTES EVAX NJR EVGN WMT CCIF WMG BEEM.
- All 20 searchers ran as `unpriced-searcher-v3b` (no fallback), all `search_complete: true`, all 20 hunts carry `expectations`, `next_guide` and an `evidence_type` on every item. No unfinished names.
- **Late amend:** HP, RRGB and MMS baselines carried `suspect` on a filing-cadence artefact the sweep refuted from company sources before any hunt; the amend step was missed and applied after the hunts (event-existence flag only, recorded in each baseline's `amended_by`).
- MAGN's searcher reports that the sealed baseline mislabels the 2026-08-06 bmo print as amc and records the next session's +3.03% instead of about -7.5%, so its reaction history understates the scale. Not corrected (sealed); noted here.
- 0 of 20 clear the 2.8 conviction floor on the searcher's `impact_sum`. V2 grounded written before the first print. Context labels written.
- `expected_return_pct` is stage E-P's calibration curve (148 resolved names, out-of-sample correlation +0.12), not fitted on v3b. Certainty (`p_up`) and the three-part forecast are recorded and decide nothing.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
