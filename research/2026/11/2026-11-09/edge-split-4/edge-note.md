# Stage E-PS — shard 4 of 4, 2026-11-09

This is stage E-PS: shard 4 of four, run beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (source commit 856d4f8). **No orders.**
Names: QBTS, TTD, SANM, VG, BAP. Judges: all four ran on their pinned agents (opus5, opus55, sonnet55, fable51); none reported a model id. Guard moved nothing. No searcher ran out of search budget (5 of 5 `search_complete: true`). Claim 18:10 UTC to done ~18:32 UTC, about 22 minutes.
Scored `panel_score.py --dry-run --stage E-PS`; stage E-P's panel history was not written. One day is an anecdote.

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.60|, opus55 |1.92|, sonnet55 |1.68|, fable51 |2.08|  (live sizes before 2026-11-09, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 SANM     amc     yes  93 long     7  opus5: 98L* opus55: 96L* sonnet55: 81L* fable51: 96L*  4  +2.11  +4.47% [+2.44, +6.31]           0.70
   2 QBTS     bmo     yes  90 short    5  opus5: 96S* opus55: 82S* sonnet55: 88S* fable51: 92S*  4  -1.53  +4.04% [+1.94, +5.99]           0.68
   3 VG       bmo          78 long     9  opus5: 84L* opus55: 68L  sonnet55: 90L* fable51: 71L   2  +1.29  +2.39% [+0.53, +4.29]           0.59
   4 TTD      amc          42 short   29  opus5: 46S  opus55: 38S  sonnet55: 82S* fable51:  0-   1  -0.53  +0.29% [-0.50, +0.99]           0.56
   5 BAP      amc           1 long     8  opus5:  2L  opus55: 13S  sonnet55:  9L  fable51:  6L   0  +0.10  +0.29% [-0.76, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
