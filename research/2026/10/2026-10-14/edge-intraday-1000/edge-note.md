# Stage E-PI — intraday panel, snapshot 10:00 New York, 2026-10-14

**Stage E-PI**: this is stage E-P re-run from scratch at 10:00 ET. It uses Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel, and it **places no orders**. All four judges ran: `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5) and `panel-judge-fable51` (claude-fable-5-1). Each covered 17 of 17 packs, with no retries. The panel was scored with `--dry-run --stage E-PI`, so the panel history was not written. One day is an anecdote, and the snapshots of one day share names and a market, so they are not independent evidence.

**Coverage.** This was the first snapshot of the day, so it built and froze the name set. The `--window` setting gives 2026-10-14 amc plus 2026-10-15 bmo: 17 names, and the sweep confirmed all 17 with no phantom names. All 17 were hunted and nothing was excluded. The release guard ran at 14:24 UTC (10:24 ET) and moved nothing. No searcher's own `impact_sum` clears the 2.8 conviction floor.

**Panel table, as `panel_score.py` printed it:**

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.50|  (live sizes before 2026-10-14, opus5 n=44 live, opus55 n=44 live, sonnet55 n=44 live, fable51 n=44 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CMTL     amc     yes  96 short    4  opus5:100S* opus55: 98S* sonnet55: 91S* fable51: 93S*  4  -2.47  +4.78% [+2.82, +6.52]           0.72
   2 BNY      bmo          53 long    19  opus5: 23L  opus55: 61L  sonnet55: 73L  fable51: 57L   0  +0.68  +0.35% [-0.33, +1.74]           0.56
   3 CMC      bmo          49 short    5  opus5: 46S  opus55: 43S  sonnet55: 57S  fable51: 50S   0  -0.62  +0.29% [-0.44, +1.38]           0.56
   4 EDUC     amc          48 short   20  opus5: 23S  opus55: 57S  sonnet55: 75S  fable51: 39S   0  -0.51  +0.29% [-0.44, +1.33]           0.56
   5 ERIC     bmo          47 short   14  opus5: 46S  opus55: 68S  sonnet55: 43S  fable51: 30S   0  -0.57  +0.29% [-0.46, +1.22]           0.56
   6 TSM      bmo          40 long    12  opus5: 23L  opus55: 57L  sonnet55: 43L  fable51: 39L   0  +0.49  +0.29% [-0.51, +0.93]           0.56
   7 SCHW     bmo          33 long    18  opus5: 32L  opus55: 46L  sonnet55:  4L  fable51: 50L   0  +0.47  +0.29% [-0.55, +0.86]           0.56
   8 MRSH     bmo          29 long    11  opus5: 23L  opus55: 41L  sonnet55: 14L  fable51: 39L   0  +0.36  +0.29% [-0.56, +0.85]           0.56
   9 WIT      bmo          27 long     7  opus5: 27L  opus55: 39L  sonnet55: 20L  fable51: 20L   0  +0.34  +0.29% [-0.57, +0.84]           0.56
  10 FHN      bmo          26 short    7  opus5: 32S  opus55: 34S  sonnet55: 18S  fable51: 20S   0  -0.28  +0.29% [-0.57, +0.84]           0.56
  11 PLD      bmo          23 long    15  opus5:  0-  opus55: 39L  sonnet55: 20L  fable51: 34L   0  +0.33  +0.29% [-0.58, +0.83]           0.56
  12 PNC      bmo          22 long    10  opus5: 16L  opus55: 39L  sonnet55: 14L  fable51: 20L   0  +0.24  +0.29% [-0.59, +0.83]           0.56
  13 HOMB     amc          22 long     8  opus5: 14L  opus55: 34L  sonnet55: 18L  fable51: 20L   0  +0.26  +0.29% [-0.59, +0.83]           0.56
  14 BSVN     bmo          14 long     3  opus5: 14L  opus55: 18L  sonnet55: 11L  fable51: 11L   0  +0.14  +0.29% [-0.66, +0.81]           0.56
  15 EQBK     amc          13 long     4  opus5: 14L  opus55: 14L  sonnet55: 18L  fable51:  7L   0  +0.11  +0.29% [-0.67, +0.81]           0.56
  16 USB      bmo           7 short    8  opus5: 14S  opus55:  7L  sonnet55: 14S  fable51:  7S   0  -0.09  +0.29% [-0.71, +0.79]           0.56
  17 MAN      bmo           4 short   45  opus5: 73S  opus55: 41L  sonnet55: 14S  fable51: 30L   0  +0.09  +0.29% [-0.73, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

**Selected: CMTL, short, panel_pct 96.** Every judge put it in its own top 20% (spread 4). The members' notes point to three things:
- The S&S sale will most likely be reported as discontinued operations at the 31 July year-end. That would put continuing revenue near $55–60m against a consolidated consensus of $108–112m that has not been rebased. This is an inference from the held-for-sale accounting, not a stated fact.
- The common stock is a roughly $39m residual behind about $220m of accreting preferred stock.
- The Allerium book-to-bill was 0.32x, with no award announced since March.

**The case against:** the balance sheet improved (revolver undrawn, covenants suspended, a fifth straight quarter of positive operating cash flow). The consensus EPS bar is disputed (−0.28 / −0.35 / −0.51). The "miss" headline is mechanical, and a reader who rebases continuing revenue may shrug it off. Turnover is thin, and the stock is under $1.30 with a historical median reaction of about 18%. The expected return of +4.78% is what names at percentile 96 have earned historically, gross, on the scorebord window. It is a translation of the percentile, not a forecast to size on (out-of-sample correlation +0.12 over 148 names). Below a percentile of 50 the curve is flat at about +0.3%.

**Where the panel and the searcher disagree most.** On MAN the searcher has +0.3 while the panel is split: Opus 5 short at 73, Opus 5.5 long, Fable 5.1 long, and an sd of 45. On SCHW the searcher's +0.9 ranks second, but the panel has it at 33 (Sonnet 5.5 long at only 4). BNY is the panel's second name, long at 53, while the searcher has it at +0.7.

**Stage E comparison.** Not available: stage E fires at 13:04 ET, and stage E-P's 13:06 run had not been written at this snapshot.

**What the numbers are not.** `expected_return_pct` is what names at that percentile have earned, not a forecast. The weights are research, and nothing trades them. `p_up` is recorded but decides nothing. No adversary checked the findings for factual errors. Stage E-P's own V2 and context labels are not recomputed here.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
