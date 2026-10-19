# Stage E-PI — intraday panel, snapshot 12:00 New York, 2026-10-19

This is stage E-PI: Opus 5.5 `unpriced-searcher` per name, a blind four-model panel (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1, all four ran on their pinned ids, 19/19 names each), scored `panel_score.py --dry-run --stage E-PI` (panel history untouched). **No orders.** One day is an anecdote, and the snapshots of one day share names and a market, so they are not independent evidence.

- **Names:** frozen by the 10:00 snapshot (38 in the window, CBSH unconfirmed). Same 19 hunted as at 10:00 (budget cap, shed by lowest `hunt_priority` from the frozen sweep): 9 amc 2026-10-19, 10 bmo 2026-10-20. 18 confirmed names shed for budget appear as unrankable (no hunt).
- **Baselines** re-sealed 16:01-16:03 UTC (12:01 ET).
- **Guard:** run 16:20 UTC, moved nothing (every amc hunt written before 16:00 ET).
- **Independence breach, handled:** the first VICR searcher read `edge-intraday-1000/hunts/VICR.json` from disk before searching. That hunt is kept in `_contaminated/VICR.json` and not scored; VICR was re-run with an explicit read restriction (as were GPC and MMM). The other hunts were launched without that restriction; none names an earlier snapshot path in its output, which is not proof none read one.
- **Searchers disagree on one macro fact**: most say the Fed hiked 25bp on 2026-09-16; HBCP's says rates were held since Dec 2025. Left as filed.
- `searcher impact_sum`: no name clears the 2.8 floor (largest EFX −2.60).

## Panel (as `panel_score.py` printed it)

E[return] is the expected return at that percentile on the panel's side: gross, scorebord window, about +0.3% flat below a percentile of 50; a translation of the percentile, not a separate forecast (out-of-sample correlation +0.12 over 148 names).

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.92|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.33|  (live sizes before 2026-10-19, opus5 n=76 live, opus55 n=76 live, sonnet55 n=76 live, fable51 n=76 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 EFX      bmo     yes  94 short    3  opus5: 95S* opus55: 99S* sonnet55: 91S* fable51: 92S*  4  -2.60  +4.63% [+2.63, +6.42]           0.71
   2 AERO     amc     yes  87 short    6  opus5: 82S* opus55: 95S* sonnet55: 91S* fable51: 82S*  4  -1.87  +3.67% [+1.57, +5.66]           0.66
   3 RLI      amc          70 long    23  opus5: 32L  opus55: 91L* sonnet55: 82L* fable51: 76L   3  +1.24  +1.56% [+0.22, +3.25]           0.56
   4 HAS      bmo          62 long    19  opus5: 32L  opus55: 79L  sonnet55: 78L  fable51: 62L   1  +0.95  +1.00% [-0.04, +2.53]           0.56
   5 GPC      bmo          62 short   11  opus5: 50S  opus55: 71S  sonnet55: 53S  fable51: 75S   1  -0.79  +0.98% [-0.05, +2.50]           0.56
   6 WASH     amc          60 short   12  opus5: 55S  opus55: 79S  sonnet55: 62S  fable51: 45S   0  -0.74  +0.83% [-0.12, +2.30]           0.56
   7 VMI      bmo          50 short   14  opus5: 68S  opus55: 29S  sonnet55: 53S  fable51: 49S   0  -0.59  +0.29% [-0.43, +1.43]           0.56
   8 MMM      bmo          40 long    43  opus5: 41L  opus55: 79L  sonnet55: 70L  fable51: 32S   0  +0.66  +0.29% [-0.52, +0.92]           0.56
   9 SYF      bmo          37 short   18  opus5: 55S  opus55: 13S  sonnet55: 26S  fable51: 54S   0  -0.48  +0.29% [-0.53, +0.89]           0.56
  10 ALLY     bmo          33 short   43  opus5: 41L  opus55: 58S  sonnet55: 53S  fable51: 62S   0  -0.64  +0.29% [-0.55, +0.86]           0.56
  11 HBCP     amc          33 long    21  opus5: 12L  opus55: 67L  sonnet55: 30L  fable51: 22L   0  +0.36  +0.29% [-0.55, +0.86]           0.56
  12 SFBS     amc          32 long    20  opus5: 18L  opus55: 67L  sonnet55: 17L  fable51: 28L   0  +0.31  +0.29% [-0.55, +0.86]           0.56
  13 VICR     bmo          31 long    45  opus5: 43L  opus55: 71L  sonnet55: 53L  fable51: 45S   0  +0.57  +0.29% [-0.56, +0.85]           0.56
  14 MSCI     bmo          26 long    24  opus5: 14L  opus55: 67L  sonnet55:  9L  fable51: 14L   0  +0.23  +0.29% [-0.57, +0.84]           0.56
  15 RBB      amc          23 long    13  opus5: 16L  opus55: 46L  sonnet55: 17L  fable51: 14L   0  +0.25  +0.29% [-0.58, +0.83]           0.56
  16 SMBK     amc          14 short    9  opus5: 12S  opus55: 29S  sonnet55:  9S  fable51:  5S   0  -0.11  +0.29% [-0.66, +0.81]           0.56
  17 CCBG     bmo          11 long    10  opus5: 12L  opus55:  0-  sonnet55: 26L  fable51:  7L   0  +0.14  +0.29% [-0.68, +0.80]           0.56
  18 WAL      amc           7 short   34  opus5: 33L  opus55: 58S  sonnet55: 17S  fable51: 14L   0  +0.01  +0.29% [-0.71, +0.79]           0.56
  19 KARO     amc           6 short   19  opus5: 32S  opus55: 13S  sonnet55:  0-  fable51: 20L   0  -0.06  +0.29% [-0.72, +0.79]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

## Selected

- **EFX short (94, 4 of 4 in own top 20%).** Evidence: the July guide was built on ~6.6% mortgage rates against ~7.4% PMMS now, MBA applications at a 20-month low, FY consensus down only 0.6%; the name sold weak mortgage guides before (−3.9/−8.2/−8.4%); +15% off the 9/30 low into the print. Case against: VantageScore open to all GSE lenders (management's $40-50m margin), stock already ~32% off its high, calls slightly richer than puts.
- **AERO short (87, 4 of 4).** Evidence: the 4Q/FY guide in the company's own 6-K assumes $3.00/gal fuel against Delta's ~$4.25 4Q assumption; a Q3 fuel overrun; unresolved pilot contract. Case against: the stock is up ~6% since Delta cut on 10-09, so a reset may be expected; traffic ran ahead of the capacity guide; Citi on fare pass-through.

## Panel vs searcher, widest gaps

- RLI: searcher +0.40, panel long 70 (three judges in or near their top 20%; Opus 5 at 32 after admitting Travelers' cat counter-evidence).
- VMI: searcher −0.20, panel short 50 (Opus 5 at 68S on the guide's steel pin).
- VICR: searcher +1.50 on the re-run, panel long 31, judges split 3L/1S.

## Stage E

Not compared here: this snapshot reads no stage E or E-P files; the timeline carries E-P's 13:06 run once it exists.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
