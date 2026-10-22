# Stage E-PS — shard 2 of 4 — 2026-10-22

This is stage E-PS, shard 2 of four: Opus 5.5 searchers (`unpriced-searcher`, us-searcher.v2) and a blind four-model panel on stage E-P's own names, sweep rows and sealed baselines (copied from commit 2d0221da). **No orders.** Scored `--dry-run --stage E-PS` against stage E-P's live judge range; the panel history was not written.

- Names: DECK, FIX, APPF (amc 2026-10-22), WRLD, ALV (bmo 2026-10-23).
- Judges: all four ran on their pinned models: opus5 (`claude-opus-5`), opus55 (`claude-opus-5-5`), sonnet55 (`claude-sonnet-5-5`), fable51 (`claude-fable-5-1`). Every judge covered all 5 packs.
- Guard (`intraday.py guard`, 16:00 ET cutoff): moved nothing. Every hunt was written before 18:12 UTC (14:12 ET).
- Searcher budget: none of the five searchers reported its search budget running out.
- Claim to done: claimed 18:02 UTC, panel scored 18:16 UTC, about 15 minutes.

## Panel table (as `panel_score.py` printed it)

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 WRLD     bmo     yes 100 long     0  opus5:100L* opus55:100L* sonnet55:100L* fable51: 99L*  4  +4.48  +5.09% [+3.29, +6.72]           0.73
   2 APPF     amc          79 long     7  opus5: 74L  opus55: 86L* sonnet55: 85L* fable51: 69L   2  +1.31  +2.45% [+0.56, +4.36]           0.59
   3 ALV      bmo          34 long    10  opus5: 26L  opus55: 23L  sonnet55: 49L  fable51: 38L   0  +0.41  +0.29% [-0.55, +0.87]           0.56
   4 FIX      amc          12 short   56  opus5: 60S  opus55: 62L  sonnet55: 23L  fable51: 73S   1  -0.29  +0.29% [-0.67, +0.80]           0.56
   5 DECK     amc           7 short   53  opus5:  9L  opus55: 60S  sonnet55: 49S  fable51: 73L   0  -0.19  +0.29% [-0.71, +0.79]           0.56
```

The expected return is gross, on the scorebord window, and it is a translation of the percentile, not a separate forecast. It is flat at about +0.3% below a percentile of 50, and out of sample it correlates only weakly with what names actually returned (+0.12).

**WRLD (selected, long, 100):** all four judges ranked it in their own top 1%. The case rests on the company's 8-K exhibit of 2026-09-21: Q2 was running "similar to" Q1, and Q1 earned $2.12 adjusted against a $0.44 consensus. Against that, the printed bar ($0.78–1.07) comes from one analyst and the sources disagree on it. Short interest is about 14–20% of float. The case against: a reserve build at the quarter end after the company loosened its lending rules, a new CEO with no CFO named yet, and two sell-offs in this same season (−17.6%, −12.8%).

APPF missed the cut by one point (79). FIX and DECK split the judges on direction, with spreads of 56 and 53.

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
