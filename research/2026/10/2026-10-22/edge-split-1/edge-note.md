# Stage E-PS — split panel, shard 1 of 4 — 2026-10-22

This is stage E-PS, shard 1 of four: Opus 5.5 searchers and a blind four-model panel on stage E-P's own names, sweep and baselines (source commit 2d0221da). **No orders placed.** Scored `panel_score.py --dry-run --stage E-PS`: stage E-P's panel history was not written.

- Names: BE, BWMX, WDC (amc 2026-10-22); BAH, SLB (bmo 2026-10-23). 5 of 5 searchers returned; none reported its search budget running out.
- Judges: all four ran on their pinned agents — panel-judge-opus5 (claude-opus-5), -opus55 (claude-opus-5-5), -sonnet55 (claude-sonnet-5-5), -fable51 (claude-fable-5-1). Full coverage, no relaunch.
- Guard (`intraday.py guard`): moved nothing; every hunt was written before 16:00 ET.
- Claim to done: about 14 minutes (claimed 18:01 UTC, panel scored 18:15 UTC).
- Selected: BE (panel_pct 85, long, 4 of 4 present). The searcher's own impact_sum cleared the 2.8 floor on no name.

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.36|  (live sizes before 2026-10-22, opus5 n=144 live, opus55 n=144 live, sonnet55 n=144 live, fable51 n=144 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 BE       amc     yes  85 long     6  opus5: 90L* opus55: 91L* sonnet55: 76L  fable51: 85L*  4  +1.63  +3.40% [+1.29, +5.41]           0.65
   2 WDC      amc          65 long    11  opus5: 76L  opus55: 74L  sonnet55: 59L  fable51: 50L   1  +0.86  +1.18% [+0.04, +2.77]           0.56
   3 SLB      bmo          48 long     7  opus5: 45L  opus55: 39L  sonnet55: 59L  fable51: 50L   0  +0.61  +0.29% [-0.44, +1.33]           0.56
   4 BWMX     amc          32 long    10  opus5: 43L  opus55: 35L  sonnet55: 34L  fable51: 15L   0  +0.44  +0.29% [-0.56, +0.86]           0.56
   5 BAH      bmo          26 short   45  opus5: 59S  opus55: 33S  sonnet55: 49L  fable51: 60S   0  -0.59  +0.29% [-0.57, +0.84]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

One day is an anecdote; judge this only pooled, against stage E-P on the same names.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
