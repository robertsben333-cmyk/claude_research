# Stage E-PS — split panel, shard 4 of 4 — 2026-10-22

This is stage E-PS, a one-day test. It reruns stage E-P's own names, sweep rows and sealed baselines in shards of five, to see whether a session carrying five names gives different evidence and a different panel call than E-P's single session. This shard ran five Opus 5.5 `unpriced-searcher`s and a blind four-model panel. **It places no orders.** The panel was scored `--dry-run --stage E-PS` against stage E-P's live range, and the panel history was not written.

- **Names:** MXL, SAM and VTMX report amc on 2026-10-22. RCI and E report bmo on 2026-10-23.
- **Searchers:** all 5 returned by 18:15 UTC. None reported its search budget running out. All five confirmed their own event; MXL and SAM had been UNCHECKED in E-P's sweep.
- **Guard** (`intraday.py guard`): moved nothing.
- **Judges:** all four ran, on their pinned models: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5) and fable51 (claude-fable-5-1). None was refused and none needed a retry.
- **Timing:** claimed at 18:04 UTC, scored at 18:19 UTC, so about 15 minutes from claim to done.
- **Selected:** 1 of 5, MXL long, at panel_pct 94.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 MXL      amc     yes  94 long     2  opus5: 96L* opus55: 91L* sonnet55: 92L* fable51: 96L*  4  +2.36  +4.63% [+2.63, +6.42]           0.71
   2 E        bmo          66 long    12  opus5: 65L  opus55: 49L  sonnet55: 65L  fable51: 82L*  1  +0.89  +1.22% [+0.06, +2.82]           0.56
   3 SAM      amc          61 short   25  opus5: 88S* opus55: 56S  sonnet55: 23S  fable51: 77S   2  -0.96  +0.88% [-0.10, +2.36]           0.56
   4 RCI      bmo          60 long    13  opus5: 69L  opus55: 45L  sonnet55: 49L  fable51: 77L   1  +0.81  +0.83% [-0.12, +2.30]           0.56
   5 VTMX     amc          19 long    47  opus5: 60S  opus55: 56L  sonnet55: 49L  fable51: 30L   0  +0.50  +0.29% [-0.61, +0.82]           0.56
```

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
