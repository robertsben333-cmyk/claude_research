# Stage E-PS — shard 4 of 4 — 2026-10-27

This is stage E-PS, shard 4 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel. **It places no orders.**

- **Names:** RBBN, LU and SLDE (amc 2026-10-27); OTLY and DMC (bmo 2026-10-28). All five were confirmed by E-P's sweep.
- **Judges:** all four ran on their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). Each covered 5 of 5 names, and none needed a fallback or a relaunch.
- **Scoring:** `panel_score.py --dry-run --stage E-PS` read each judge against stage E-P's live range from earlier runs. It wrote nothing to the panel history.
- **Guard:** `intraday.py guard` moved nothing; every hunt was written before 16:00 ET.
- **Search budget:** none of the five searchers reported its budget running out.
- **Timing:** claimed at 17:22 UTC, panel scored at 17:35 UTC, so about 13 minutes from claim to done.
- **Selected: RBBN, short, panel_pct 87.** OTLY (long, 79) fell just under the 80 cut.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.19|, sonnet55 |1.15|, fable51 |1.44|  (live sizes before 2026-10-27, opus5 n=196 live, opus55 n=196 live, sonnet55 n=196 live, fable51 n=196 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 RBBN     amc     yes  87 short    8  opus5: 80S* opus55: 97S* sonnet55: 79S  fable51: 92S*  3  -1.48  +3.67% [+1.57, +5.66]           0.66
   2 OTLY     bmo          79 long    25  opus5: 91L* opus55: 97L* sonnet55: 91L* fable51: 36L   3  +1.79  +2.45% [+0.56, +4.36]           0.59
   3 LU       amc          47 short   22  opus5: 39S  opus55: 21S  sonnet55: 47S  fable51: 81S*  1  -0.47  +0.29% [-0.46, +1.24]           0.56
   4 SLDE     amc          15 long    57  opus5: 76S  opus55: 50L  sonnet55: 74L  fable51: 11L   0  +0.41  +0.29% [-0.66, +0.81]           0.56
   5 DMC      bmo           1 long    36  opus5: 54S  opus55: 11L  sonnet55: 47L  fable51:  2S   0  +0.03  +0.29% [-0.76, +0.78]           0.56
```

The searcher's own `impact_sum`, which does not rank the day: OTLY +0.70, SLDE +0.10, DMC −0.50, LU −0.50, RBBN −1.00. None clears the 2.8 floor.

One day is an anecdote. Judge this stage only pooled against stage E-P over many days.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
