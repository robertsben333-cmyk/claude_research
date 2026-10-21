# Stage E-PI — intraday panel, snapshot 12:00 New York, 2026-10-21

**This is stage E-PI**: stage E-P re-run from scratch at 12:00 ET. It uses Opus 5.5 `unpriced-searcher` agents (native, 19/19) and a blind four-model panel, and it **places no orders**. All four judges ran on their pinned agents and covered 19 of 19: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5) and fable51 (claude-fable-5-1). The panel was scored with `--dry-run --stage E-PI`, so the panel history was not written. One day is an anecdote. The snapshots of one day share names and a market, so they are not independent evidence.

**Names.** This was the first snapshot of the day, because no 10:00 snapshot exists. It built and froze the day's name set: 118 calendar names (64 amc 10-21, 54 bmo 10-22) and 108 confirmed by the sweep. Ten were not confirmed and not hunted: FCFS, ZGN, AMBP, NTST, OSBC, DOW, CVBF, BMI, KRNY, NVEC. The cap is 19 names, taken by `hunt_priority` in strict order, so 89 confirmed names were shed.

**Guard.** The guard ran at 16:34 UTC (12:34 ET) and moved nothing: every hunt was written before 16:00 ET.

**Deviations, stated:**
- **The sweep ran as three parallel `edge-sweep` agents.** They covered interleaved thirds of the 118 names and were merged into `sweep.json`. One agent over 118 names would have used up the amc names' time before their release.
- **THRM's baseline was amended before any hunt.** It went from `suspect` to `unknown` with `edge_baseline_amend.py`. The searcher then found that the history gap was a matcher miss: Q2 was filed under 8-K item 2.01/7.01/8.01, not 2.02.
- **The turn's shared WebSearch budget ran out early.** Most searchers worked from direct WebFetch of primary documents (EDGAR, Yahoo, BLS, company pages) and could not search for previews, peers or alternative data. This snapshot's evidence is therefore thinner than a normal E-P run's, and that should be kept in mind when comparing it with other snapshots.
- **One of HXL's Yahoo fetches carried a quote stamped 2026-10-22 08:21 EDT.** It was a vendor timestamp. The searcher disregarded that quote and used no price from it.

**Searcher score.** 19 names are rankable on the searcher's own `impact_sum` and none clears the 2.8 floor (the largest is MOH at +2.10).

## Panel (as `panel_score.py` printed it)

`panel_pct` is the size of the mean of the four judges' own percentiles, and its direction is in `side`. A name is selected when `panel_pct` is 80 or more and all four judges are present. `E[return]` is what names at that percentile have earned on the panel's side: it is gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile into a return. It is not a separate forecast, and its out-of-sample record is weak (correlation +0.12 over 148 names).

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.60|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.30|  (live sizes before 2026-10-21, opus5 n=114 live, opus55 n=114 live, sonnet55 n=114 live, fable51 n=114 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 MEDP     amc     yes  88 short    4  opus5: 82S* opus55: 89S* sonnet55: 93S* fable51: 90S*  4  -1.81  +3.86% [+1.76, +5.82]           0.67
   2 LUV      amc     yes  85 short    2  opus5: 84S* opus55: 88S* sonnet55: 83S* fable51: 83S*  4  -1.54  +3.28% [+1.18, +5.29]           0.64
   3 KALU     amc     yes  83 long    12  opus5: 85L* opus55: 93L* sonnet55: 62L  fable51: 90L*  3  +1.81  +3.00% [+0.95, +4.98]           0.62
   4 WDFC     amc     yes  80 short    3  opus5: 78S  opus55: 84S* sonnet55: 83S* fable51: 76S   4  -1.33  +2.68% [+0.68, +4.63]           0.61
   5 CASH     amc          79 long     3  opus5: 78L  opus55: 80L  sonnet55: 75L  fable51: 84L*  4  +1.24  +2.54% [+0.59, +4.46]           0.60
   6 SPOT     bmo          78 short    7  opus5: 82S* opus55: 67S  sonnet55: 86S* fable51: 79S   3  -1.31  +2.41% [+0.54, +4.30]           0.59
   7 THRM     bmo          75 long    15  opus5: 67L  opus55: 90L* sonnet55: 54L  fable51: 90L*  2  +1.43  +2.03% [+0.38, +3.86]           0.57
   8 CRS      bmo          75 long     6  opus5: 73L  opus55: 67L  sonnet55: 82L* fable51: 79L   3  +1.19  +2.01% [+0.37, +3.83]           0.57
   9 LBRT     amc          70 long    27  opus5: 77L  opus55: 96L* sonnet55: 25L  fable51: 83L*  3  +1.28  +1.59% [+0.23, +3.29]           0.56
  10 HXL      amc          69 long     5  opus5: 63L  opus55: 71L  sonnet55: 75L  fable51: 65L   1  +0.98  +1.45% [+0.17, +3.12]           0.56
  11 MOH      amc          64 long    25  opus5: 53L  opus55: 92L* sonnet55: 82L* fable51: 28L   2  +1.03  +1.08% [-0.00, +2.64]           0.56
  12 SLG      amc          57 long    11  opus5: 49L  opus55: 73L  sonnet55: 61L  fable51: 46L   0  +0.66  +0.57% [-0.21, +2.06]           0.56
  13 KNX      amc          54 short   18  opus5: 63S  opus55: 47S  sonnet55: 75S  fable51: 28S   1  -0.76  +0.35% [-0.32, +1.75]           0.56
  14 IIIN     bmo          33 short   47  opus5: 83S* opus55: 19L  sonnet55: 10L  fable51: 76S   2  -0.44  +0.29% [-0.55, +0.86]           0.56
  15 ASIC     amc          29 short   11  opus5: 37S  opus55: 11S  sonnet55: 38S  fable51: 29S   0  -0.44  +0.29% [-0.56, +0.85]           0.56
  16 QS       amc          14 long    28  opus5:  0-  opus55: 25S  sonnet55: 38L  fable51: 45L   0  +0.24  +0.29% [-0.66, +0.81]           0.56
  17 LOB      amc           9 long    11  opus5: 10L  opus55: 25L  sonnet55:  6S  fable51:  6L   0  +0.17  +0.29% [-0.70, +0.80]           0.56
  18 ARGX     bmo           3 long    26  opus5: 40S  opus55: 13L  sonnet55: 13L  fable51: 27L   0  +0.20  +0.29% [-0.74, +0.78]           0.56
  19 EGBN     amc           2 long    43  opus5: 36S  opus55: 22L  sonnet55: 62L  fable51: 42S   0  -0.11  +0.29% [-0.75, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

Selected at 12:00: **MEDP short 88, LUV short 85, KALU long 83, WDFC short 80** (all amc). CASH long 79 and SPOT short 78 are the nearest misses. Disagreement is widest on IIIN (sd 47: opus5 and fable51 short, opus55 and sonnet55 long), EGBN (43) and LBRT (27: sonnet55 at 25 against opus55 at 96).

## Timeline

See `../edge-intraday/timeline.md`.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.  
