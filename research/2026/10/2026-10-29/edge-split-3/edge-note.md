# Stage E-PS — shard 3 of 4 — 2026-10-29

This is stage E-PS, shard 3 of 4. It runs beside stage E-P on E-P's own names, sweep rows and sealed baselines (source commit `a633993a`), with Opus 5.5 `unpriced-searcher`s and a blind four-model panel. It places **no orders**. The panel is scored with `--dry-run --stage E-PS` against stage E-P's history, which was not written to.

- **Names:** MIAX, REAL, FND and PINS (amc 2026-10-29) and CPRI (bmo 2026-10-30). All five searchers were launched in one message.
- **Search budget:** no searcher reported running out (`hunt_status`: 0 unfinished of 5). Some sites refused requests themselves (tickflow, Stock Taper 429; Benzinga, Chartmill 403).
- **Sweep-unconfirmed names:** the sweep had left REAL and PINS unconfirmed. Both searchers confirmed the amc 2026-10-29 event from the companies' own notices.
- **Guard:** `intraday.py guard` moved nothing; the cutoff was 16:00 ET and it ran at 18:21 UTC.
- **Judges:** all four ran on their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). No fallback was used.
- **Searchers' own key:** `impact_sum` was PINS +1.50, FND +0.70, MIAX +0.40, REAL +0.40, CPRI 0.00. None cleared the 2.8 floor.
- **Timing:** claimed at 18:12 UTC and done at about 18:27 UTC, so claim to done took about 15 minutes.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.50|  (live sizes before 2026-10-29, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 REAL     amc     yes  86 short    6  opus5: 81S* opus55: 96S* sonnet55: 79S  fable51: 88S*  3  -1.35  +3.46% [+1.36, +5.46]           0.65
   2 MIAX     amc          75 short    8  opus5: 67S  opus55: 73S  sonnet55: 88S* fable51: 74S   1  -0.94  +2.03% [+0.38, +3.86]           0.57
   3 PINS     amc          52 long    18  opus5: 58L  opus55: 22L  sonnet55: 62L  fable51: 67L   0  +0.66  +0.33% [-0.36, +1.63]           0.56
   4 FND      amc          47 long    22  opus5: 80L  opus55: 48L  sonnet55: 16L  fable51: 44L   0  +0.51  +0.29% [-0.46, +1.25]           0.56
   5 CPRI     bmo           3 long    50  opus5: 42L  opus55: 56S  sonnet55: 62L  fable51: 36S   0  +0.01  +0.29% [-0.74, +0.78]           0.56
```

One day is an anecdote. Judge this stage only pooled against stage E-P on the same names.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
