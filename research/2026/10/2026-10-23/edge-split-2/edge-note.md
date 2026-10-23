# Stage E-PS — shard 2 of 4 — 2026-10-23

This is stage E-PS, shard 2 of four. It ran beside stage E-P with Opus 5.5 searchers (`unpriced-searcher`, named agent) and a blind four-model panel, on E-P's own names, sweep and baselines (copied at e55276cd). It places no orders.

- **Names:** MED, BMRC, HBT. All three report bmo on 2026-10-26; BMRC's session was settled as Monday pre-market by its searcher.
- **Judges:** all four ran on their pinned models: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). Each covered all three packs, and none reported its own model id.
- **Guard:** moved nothing.
- **Search budget:** no searcher reported running out.
- **Claim to done:** claimed 17:15 UTC, panel scored 17:35 UTC, about 20 minutes.
- **Selected:** none. Panel scored `--dry-run --stage E-PS`; panel history untouched.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 MED      bmo          68 long    24  opus5: 27L  opus55: 73L  sonnet55: 92L* fable51: 79L   2  +1.07  +1.39% [+0.14, +3.03]           0.56
   2 BMRC     bmo           9 short   27  opus5: 55S  opus55:  3L  sonnet55:  8L  fable51:  9L   0  +0.14  +0.29% [-0.70, +0.79]           0.56
   3 HBT      bmo           3 long    23  opus5: 34S  opus55: 27L  sonnet55:  2L  fable51: 17L   0  +0.18  +0.29% [-0.74, +0.78]           0.56
```

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
