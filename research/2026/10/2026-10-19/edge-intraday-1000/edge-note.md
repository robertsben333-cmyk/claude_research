# Stage E-PI — intraday panel, snapshot 10:00 New York, 2026-10-19

This is stage E-PI: stage E-P re-run from scratch at 10:00 New York (fired 13:58 UTC). Opus 5.5 `unpriced-searcher`s collected the evidence, and a blind four-model panel sized it. **No orders were placed**; `alpaca_trade.py` was not run in any form, and the V2 shadow ledger was not run either.

- **Judges:** all four ran and covered all 19 names: `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5), `panel-judge-fable51` (claude-fable-5-1).
- **Panel scoring:** `panel_score.py --dry-run --stage E-PI`. Stage E-P's panel history was not written; each judge is read against its 76 live sizes from before today.
- **Names:** the window held 38: 17 amc tonight (2026-10-19) and 21 bmo tomorrow morning (2026-10-20). The sweep confirmed 37; CBSH was unconfirmed (calendar sites disagree, no 8-K).
- **Shed for budget:** 18 confirmed names were shed under the cap of 19 hunted names, lowest `hunt_priority` first: GE RTX GM NOC STLD WRB HAL KEY CCK AGNC WTFC ZION BOKF FNB AUB UCB PEBO MBWM. They appear in `edge-scores.json` as not ranked, "no hunt". This snapshot froze the day's name set (`edge-intraday/names.json`).
- **Release guard:** ran at 14:35 UTC and moved nothing; every hunt was written long before any release.
- **Searcher scores:** no name clears the 2.8 conviction floor on the searcher's own `impact_sum`. The largest are AERO and EFX at −2.5.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.92|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.33|  (live sizes before 2026-10-19, opus5 n=76 live, opus55 n=76 live, sonnet55 n=76 live, fable51 n=76 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 EFX      bmo     yes  90 short    1  opus5: 88S* opus55: 92S* sonnet55: 90S* fable51: 90S*  4  -1.88  +4.07% [+1.97, +6.02]           0.68
   2 AERO     amc     yes  89 short    2  opus5: 88S* opus55: 92S* sonnet55: 90S* fable51: 86S*  4  -1.90  +3.92% [+1.82, +5.88]           0.68
   3 RLI      amc          74 long    12  opus5: 60L  opus55: 92L* sonnet55: 70L  fable51: 75L   2  +0.98  +1.94% [+0.35, +3.75]           0.56
   4 HAS      bmo          74 long    15  opus5: 50L  opus55: 75L  sonnet55: 91L* fable51: 80L*  2  +1.10  +1.92% [+0.34, +3.71]           0.56
   5 WAL      amc          64 long    16  opus5: 46L  opus55: 87L* sonnet55: 53L  fable51: 71L   1  +0.78  +1.12% [+0.02, +2.70]           0.56
   6 KARO     amc          62 short   27  opus5: 64S  opus55: 84S* sonnet55: 17S  fable51: 82S*  2  -1.12  +0.96% [-0.06, +2.47]           0.56
   7 RBB      amc          46 long    14  opus5: 29L  opus55: 67L  sonnet55: 40L  fable51: 49L   0  +0.56  +0.29% [-0.47, +1.17]           0.56
   8 MSCI     bmo          45 short    9  opus5: 32S  opus55: 54S  sonnet55: 53S  fable51: 43S   0  -0.57  +0.29% [-0.48, +1.13]           0.56
   9 WASH     amc          45 short   14  opus5: 50S  opus55: 46S  sonnet55: 62S  fable51: 22S   0  -0.57  +0.29% [-0.48, +1.11]           0.56
  10 VICR     bmo          42 short   50  opus5: 79S  opus55: 43L  sonnet55: 78S  fable51: 54S   2  -0.92  +0.29% [-0.50, +0.99]           0.56
  11 MMM      bmo          40 long    17  opus5: 43L  opus55: 40L  sonnet55: 62L  fable51: 13L   0  +0.41  +0.29% [-0.52, +0.92]           0.56
  12 SFBS     amc          34 long    19  opus5: 13L  opus55: 43L  sonnet55: 62L  fable51: 20L   0  +0.35  +0.29% [-0.55, +0.87]           0.56
  13 SYF      bmo          33 long    23  opus5: 41L  opus55: 67L  sonnet55: 17L  fable51:  7L   0  +0.36  +0.29% [-0.55, +0.86]           0.56
  14 GPC      bmo          30 long    11  opus5: 22L  opus55: 46L  sonnet55: 17L  fable51: 33L   0  +0.37  +0.29% [-0.56, +0.85]           0.56
  15 SMBK     amc          29 long    14  opus5: 16L  opus55: 47L  sonnet55: 40L  fable51: 14L   0  +0.37  +0.29% [-0.56, +0.85]           0.56
  16 ALLY     bmo          13 long    28  opus5: 22L  opus55: 49L  sonnet55: 30S  fable51: 10L   0  +0.26  +0.29% [-0.67, +0.81]           0.56
  17 HBCP     amc          12 long     4  opus5: 12L  opus55: 14L  sonnet55: 17L  fable51:  7L   0  +0.16  +0.29% [-0.67, +0.81]           0.56
  18 CCBG     bmo           4 long     6  opus5:  0-  opus55:  4S  sonnet55:  9L  fable51: 12L   0  +0.06  +0.29% [-0.73, +0.78]           0.56
  19 VMI      bmo           4 short   40  opus5: 12S  opus55: 16S  sonnet55: 62L  fable51: 49S   0  -0.13  +0.29% [-0.74, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

**Selected (panel_pct ≥ 80, all four judges present): EFX short (90) and AERO short (89).** Every judge put both names in its own top 20% on the short side.

- **EFX (bmo 10-20):** the July FY guide assumed a 30-year mortgage rate near 6.6%. The rate reached 7.4% in October, rate-and-term refi locks fell 47% year on year, and management acknowledged the volume hit on 09-14. A trimmed Q4/FY guide is the line this stock trades on.
  - *Case against:* much of this is already priced, and the options market pays for upside (25-delta skew −3.2). A bi-merge decision from the regulator is still pending and could land either way.
- **AERO (amc 10-19):** the standing Q4 guide assumes $3.00/gal fuel and a peso at 17.6, against Delta's roughly $4.25 and the peso near 18.3. Q3 margin is likely at or below the low end of the guide.
  - *Case against:* management pre-warned on fuel twice, fares pass part of the cost through, and the last two prints were bought, including the fuel-hit Q2.

**Where the panel and the searcher disagree most:**
- **VICR:** the searcher had 0.0, the panel 42S, but the judges split (Opus 5.5 long, the other three short; sd 50).
- **KARO:** the searcher had 0.0, the panel 62S (Sonnet 5.5 only 17S).
- **RLI and HAS:** the panel reads them more long (74L) than the searcher's +0.5 / +0.9.

**What these numbers are not.** `E[return]` is what past panel names at this percentile have earned on the panel's side, gross, on the scorebord window, flat at about +0.3% below a percentile of 50. Its out-of-sample record is weak (correlation +0.12 over 148 names), so it is not a forecast to size on. The day's snapshots share names and a market, so they are not independent evidence. One day is an anecdote.

Timeline: `../edge-intraday/timeline.md`.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
