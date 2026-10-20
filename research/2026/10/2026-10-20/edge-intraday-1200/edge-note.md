# Stage E-PI — intraday panel, snapshot 12:00 New York, 2026-10-20

This is stage E-PI: Opus 5.5 `unpriced-searcher` per name and a blind four-model panel, scored `--dry-run --stage E-PI` (stage E-P's panel history untouched). **No orders.** One day is an anecdote, and this day's snapshots share names and a market, so they are not independent evidence.

- **Snapshot:** first of the day (the 10:00 slot did not run), so this snapshot built the universe (45 names: 22 amc 2026-10-20, 23 bmo 2026-10-21), ran one `edge-sweep` (43 confirmed; ISRG and HCSG vendor-only, unconfirmed) and froze the names to `edge-intraday/names.json`.
- **Hunted (cap 19, by hunt_priority):** PEGA IART LRN WGO NP ALK LAD MHO UAL WFRD ABT ELV TMO NFLX OZK COF WAB DHR CB. Shed for budget: NTRS NPB TDY MCB OFG SF BKU EWBC QCRH HWC ORRF ONB AMX BWB MCO NLY NEE CME FCCO T ELS PM ADC UNF.
- **Baselines amended before any searcher** (company sources, via the sweep): NP suspect -> fits_cadence; IART suspect -> unknown.
- **Guard:** ran 16:33 UTC (12:33 ET), moved nothing; every amc hunt was written before 16:00 ET.
- **Judges:** all four ran on their pinned ids (opus5 claude-opus-5, opus55 claude-opus-5-5, sonnet55 claude-sonnet-5-5, fable51 claude-fable-5-1), 19/19 each. Searchers: `unpriced-searcher`, native agent, claude-opus-5-5.
- **Searcher key:** no name clears the 2.8 conviction floor (largest NP +1.45).
- **Selected (panel_pct >= 80, all four present):** ALK short 82, NP long 81. PEGA short 79 just misses.

E[return] is what names at that percentile have earned on the panel's side, gross, on the scorebord window; flat at about +0.3% below a percentile of 50, and a weak out-of-sample record (correlation +0.12 over 148 names). It is a translation of the percentile, not a forecast to size on.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.92|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.33|  (live sizes before 2026-10-20, opus5 n=95 live, opus55 n=95 live, sonnet55 n=95 live, fable51 n=95 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ALK      amc     yes  82 short    5  opus5: 79S  opus55: 76S  sonnet55: 90S* fable51: 82S*  3  -1.29  +2.84% [+0.82, +4.81]           0.62
   2 NP       amc     yes  81 long     5  opus5: 79L  opus55: 86L* sonnet55: 86L* fable51: 74L   4  +1.36  +2.80% [+0.78, +4.76]           0.61
   3 PEGA     amc          79 short    4  opus5: 86S* opus55: 79S  sonnet55: 78S  fable51: 74S   3  -1.13  +2.51% [+0.58, +4.43]           0.60
   4 WFRD     amc          72 long     6  opus5: 62L  opus55: 76L  sonnet55: 78L  fable51: 70L   1  +1.01  +1.70% [+0.27, +3.43]           0.56
   5 NFLX     amc          61 short   15  opus5: 65S  opus55: 42S  sonnet55: 82S* fable51: 56S   1  -0.82  +0.91% [-0.08, +2.41]           0.56
   6 ABT      bmo          47 short    5  opus5: 43S  opus55: 42S  sonnet55: 56S  fable51: 46S   0  -0.53  +0.29% [-0.46, +1.24]           0.56
   7 LAD      bmo          46 long    22  opus5: 57L  opus55: 70L  sonnet55: 10L  fable51: 44L   0  +0.63  +0.29% [-0.48, +1.14]           0.56
   8 OZK      amc          42 long     8  opus5: 52L  opus55: 30L  sonnet55: 40L  fable51: 46L   0  +0.51  +0.29% [-0.50, +1.00]           0.56
   9 LRN      amc          38 long    49  opus5: 42S  opus55: 41L  sonnet55: 78L  fable51: 77L   2  +0.75  +0.29% [-0.53, +0.91]           0.56
  10 TMO      bmo          26 long    13  opus5: 23L  opus55: 30L  sonnet55:  7L  fable51: 44L   0  +0.27  +0.29% [-0.57, +0.84]           0.56
  11 UAL      amc          19 long    18  opus5: 39L  opus55: 30L  sonnet55: 15L  fable51:  8S   0  +0.26  +0.29% [-0.61, +0.82]           0.56
  12 MHO      bmo          15 long    22  opus5: 48L  opus55: 10L  sonnet55: 15S  fable51: 16L   0  +0.18  +0.29% [-0.65, +0.81]           0.56
  13 CB       amc          11 long    15  opus5: 12S  opus55: 17L  sonnet55: 10L  fable51: 30L   0  +0.18  +0.29% [-0.68, +0.80]           0.56
  14 WGO      bmo          10 short   52  opus5: 79L  opus55: 30S  sonnet55: 56S  fable51: 34S   0  -0.36  +0.29% [-0.68, +0.80]           0.56
  15 ELV      bmo           9 long    39  opus5: 53S  opus55: 17L  sonnet55: 56L  fable51: 16L   0  +0.22  +0.29% [-0.69, +0.80]           0.56
  16 IART     bmo           9 long    26  opus5: 25S  opus55: 46L  sonnet55: 15L  fable51:  0-   0  +0.12  +0.29% [-0.69, +0.80]           0.56
  17 DHR      bmo           4 short   20  opus5: 34S  opus55: 13L  sonnet55: 10S  fable51: 15L   0  -0.01  +0.29% [-0.73, +0.78]           0.56
  18 COF      amc           3 long    22  opus5: 23S  opus55: 37L  sonnet55:  7S  fable51:  5L   0  +0.02  +0.29% [-0.74, +0.78]           0.56
  19 WAB      bmo           0 -        0  opus5:  0-  opus55:  0-  sonnet55:  0-  fable51:  0-   0  +0.00
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
