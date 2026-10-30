# Stage E-PS — shard 4 of 4 — 2026-10-30

This is stage E-PS, shard 4 of four, run beside stage E-P. It used Opus 5.5 `unpriced-searcher`s and a blind four-model panel on stage E-P's own names, sweep and sealed baselines. **It places no orders.** One day is an anecdote.

- Names: NSSC, KOS, FOXA, LTBR, PEG. All are bmo on 2026-11-02, the window from the 2026-10-30 close to the 2026-11-02 close.
- The fire was late. The shard was claimed at 18:12 UTC (14:12 ET) and done at about 18:25 UTC, so claim-to-done was about 13 minutes.
- All four judges ran on their pinned agents: opus5 (`claude-opus-5`), opus55 (`claude-opus-5-5`), sonnet55 (`claude-sonnet-5-5`) and fable51 (`claude-fable-5-1`). None was refused or missing.
- Guard: it moved nothing. All names are bmo.
- Search budget: no searcher reported running out. `hunt_status` found 0 of 5 unfinished.
- Searcher keys: no name clears the 2.8 floor. `impact_sum` was FOXA +1.10, KOS +1.00, NSSC +1.00, LTBR +0.80 and PEG +0.50.
- Selected by the panel: none. No name reached panel_pct >= 80.

## Panel (as `panel_score.py` printed it)

```
own top 20% starts at: opus5 |2.04|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-10-30, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 FOXA     bmo          71 long     9  opus5: 62L  opus55: 64L  sonnet55: 76L  fable51: 84L*  1  +0.86  +1.68% [+0.26, +3.40]           0.56
   2 NSSC     bmo          71 long     8  opus5: 73L  opus55: 58L  sonnet55: 79L  fable51: 72L   0  +0.94  +1.62% [+0.24, +3.33]           0.56
   3 KOS      bmo          39 long    47  opus5: 38S  opus55: 40L  sonnet55: 72L  fable51: 82L*  1  +0.63  +0.29% [-0.52, +0.91]           0.56
   4 LTBR     bmo          26 long    11  opus5: 24L  opus55: 44L  sonnet55: 20L  fable51: 17L   0  +0.31  +0.29% [-0.57, +0.84]           0.56
   5 PEG      bmo          14 long    11  opus5:  6L  opus55:  3L  sonnet55: 16L  fable51: 30L   0  +0.16  +0.29% [-0.66, +0.81]           0.56
```

The judges disagreed most on KOS (sd 47). Opus 5 took the short side because the stock was sold after 0 of its last 5 prints; the other three leaned long on production and the Brent price. E[return] translates the percentile into an expected return. It is not a forecast for this name.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
