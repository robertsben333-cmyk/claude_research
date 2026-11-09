# Stage E-PS — shard 2 of 4 — 2026-11-09

This is stage E-PS, shard 2 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines. Five Opus 5.5 `unpriced-searcher` agents collected the evidence and a blind four-model panel judged it. Nothing was ordered.

- **Judges:** all four ran on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. None was refused, so no fallback was needed.
- **Guard** (`intraday.py guard`, at 18:25 UTC): moved nothing.
- **Search budget:** no searcher reported running out. `hunt_status.py` found 0 unfinished of 5.
- **Timing:** claimed at about 18:14 UTC and scored at 18:28 UTC, about 15 minutes.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`, so each judge is read against stage E-P's live range and the panel history was not written.
- **Selection:** no name reached `panel_pct` 80, so nothing is selected. QLYS (75, long) and PLUG (74, short) came closest.

One day is an anecdote.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 QLYS     amc          75 long    10  opus5: 72L  opus55: 70L  sonnet55: 92L* fable51: 66L   1  +1.03  +2.02% [+0.38, +3.84]           0.57
   2 PLUG     amc          74 short    7  opus5: 79S  opus55: 79S  sonnet55: 62S  fable51: 78S   1  -1.25  +1.95% [+0.35, +3.76]           0.57
   3 HIMS     amc          61 short    4  opus5: 65S  opus55: 58S  sonnet55: 56S  fable51: 66S   0  -0.82  +0.91% [-0.09, +2.40]           0.56
   4 SRRK     bmo          55 long    23  opus5: 50L  opus55: 89L* sonnet55: 56L  fable51: 25L   1  +0.67  +0.40% [-0.28, +1.89]           0.56
   5 HSAI     bmo          50 short   10  opus5: 45S  opus55: 64S  sonnet55: 56S  fable51: 37S   0  -0.62  +0.30% [-0.41, +1.49]           0.56
```

`E[return]` is what names at this percentile have earned historically: gross, on the scorebord's window, with a weak out-of-sample record. It is not a forecast to size on.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
