# Stage E-PS — shard 1 of 4 — 2026-11-04

This is stage E-PS, shard 1 of four. It runs beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel. **No orders.**

- **Names:** SEZL, WOLF and FIG (amc 2026-11-04); LMND and CELH (bmo 2026-11-05).
- **Judges:** all four ran on their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). None was missing.
- **Guard:** `intraday.py guard` moved nothing.
- **Searchers:** all 5 finished, with 0 unfinished and none reporting that its search budget ran out.
- **Timing:** claimed at 18:12 UTC; the panel was scored at 18:27 UTC, about 16 minutes from claim to done.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`, read against stage E-P's live history before today. The panel history was not written.

One day is an anecdote.

## Panel table, as `panel_score.py` printed it

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.24|, opus55 |1.70|, sonnet55 |1.50|, fable51 |1.92|  (live sizes before 2026-11-04, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 WOLF     amc     yes  81 long    14  opus5: 92L* opus55: 88L* sonnet55: 85L* fable51: 56L   3  +1.44  +2.70% [+0.70, +4.65]           0.61
   2 CELH     bmo          76 short    6  opus5: 83S* opus55: 72S  sonnet55: 68S  fable51: 82S*  2  -1.20  +2.18% [+0.44, +4.03]           0.58
   3 FIG      amc          74 long     5  opus5: 68L  opus55: 69L  sonnet55: 78L  fable51: 80L   0  +1.04  +1.88% [+0.33, +3.66]           0.56
   4 LMND     bmo          63 short   22  opus5: 30S  opus55: 64S  sonnet55: 62S  fable51: 94S*  1  -0.77  +1.01% [-0.04, +2.54]           0.56
   5 SEZL     amc          47 long    24  opus5:  7L  opus55: 61L  sonnet55: 68L  fable51: 52L   0  +0.73  +0.29% [-0.46, +1.25]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

Only WOLF is selected: panel_pct 81, long, with three of four judges in their own top 20%. CELH (76, short) and FIG (74, long) fall just short.

E[return] is gross and on the scorebord's window. It is what names at that percentile have earned, at about +0.3% below a percentile of 50. It is not a forecast to size on.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
