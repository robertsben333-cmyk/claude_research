# Stage E-PS — shard 2 of 4 — 2026-10-29

This is stage E-PS, shard 2 of 4. It ran beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (source commit a633993a). It placed no orders.

- **Names:** CDNA, COLM, SUPN, STOK, AMZN, all amc 2026-10-29.
- **Timing:** claimed at 18:12 UTC and done at about 18:25 UTC (about 13 minutes). This session fired about an hour after stage E-P's 17:06 UTC.
- **Searchers:** 5 of 5 `unpriced-searcher` returned with `search_complete: true`. None reported its search budget running out; the only failures were site-level 403/429/503 errors.
- **Guard:** moved nothing (all hunts were written before 16:00 ET).
- **Judges:** all four ran on their pinned agents, with no fallbacks: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1).
- **Caveats:**
  - AMZN's sealed baseline had `bars_failed`, so its searcher rebuilt the price inputs itself.
  - SUPN is pegged to INDV through the merger closing on 2026-11-02, so its own print carries only about 43.5% weight.
  - STOK's event was unconfirmed in the sweep; its searcher confirmed it through the company's own release.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CDNA     amc     yes  99 long     1  opus5:100L* opus55: 98L* sonnet55: 98L* fable51:100L*  4  +3.05  +5.02% [+3.18, +6.67]           0.73
   2 AMZN     amc          78 long     4  opus5: 79L  opus55: 80L* sonnet55: 72L  fable51: 82L*  2  +1.15  +2.37% [+0.52, +4.26]           0.59
   3 STOK     amc          58 long    19  opus5: 74L  opus55: 56L  sonnet55: 27L  fable51: 74L   0  +0.76  +0.60% [-0.20, +2.08]           0.56
   4 COLM     amc          31 short   16  opus5: 10S  opus55: 48S  sonnet55: 20S  fable51: 46S   0  -0.37  +0.29% [-0.56, +0.86]           0.56
   5 SUPN     amc          15 long    10  opus5: 30L  opus55: 10L  sonnet55:  3L  fable51: 16L   0  +0.21  +0.29% [-0.65, +0.81]           0.56
```

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
