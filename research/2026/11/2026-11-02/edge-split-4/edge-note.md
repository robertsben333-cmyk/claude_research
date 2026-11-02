# Stage E-PS — shard 4 of 4 — 2026-11-02

Stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 searchers (unpriced-searcher) and a blind four-model panel on E-P's own names, sweep and baselines (source commit 550315c5). No orders placed.

- Names: BETA (bmo 11-03), INSP (amc 11-02), SHOP (bmo 11-03), VRTX (amc 11-02), BRCC (amc 11-02; the sweep left it unconfirmed, the searcher confirmed it from the company's 2026-10-13 release).
- Judges: all four ran on their pinned agents — opus5, opus55, sonnet55, fable51. No fallback used.
- Guard: moved nothing (all hunts written before 16:00 ET).
- Search budget: no searcher reported a refused or exhausted search; 5 of 5 search_complete.
- Claim to done: about 13 minutes (claimed 18:21 UTC, scored 18:33 UTC).
- VRTX's sealed baseline was bars_failed; its searcher rebuilt spot and history from cited sources.

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-11-02, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 INSP     amc     yes  97 long     2  opus5: 99L* opus55: 94L* sonnet55: 96L* fable51: 99L*  4  +2.60  +4.88% [+2.97, +6.59]           0.72
   2 SHOP     bmo          54 short    2  opus5: 53S  opus55: 56S  sonnet55: 53S  fable51: 56S   0  -0.65  +0.37% [-0.30, +1.83]           0.56
   3 BRCC     amc          42 long    72  opus5: 82S* opus55: 68L  sonnet55: 94L* fable51: 88L*  2  +1.17  +0.29% [-0.50, +0.99]           0.56
   4 BETA     bmo          25 short   48  opus5: 46S  opus55: 64S  sonnet55: 57L  fable51: 46S   0  -0.57  +0.29% [-0.57, +0.84]           0.56
   5 VRTX     amc          17 short   18  opus5: 39S  opus55: 14S  sonnet55: 10L  fable51: 26S   0  -0.28  +0.29% [-0.63, +0.82]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
