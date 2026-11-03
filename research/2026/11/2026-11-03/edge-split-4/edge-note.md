# Stage E-PS — shard 4 of 4 — 2026-11-03

Stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (main d441df90). **No orders.**

- Names: OUST, CRCT, LIME (amc 2026-11-03), SEDG, DIN (bmo 2026-11-04).
- Searchers: 5 of 5 `unpriced-searcher`, one message, all `search_complete: true`; none reported its search budget running out (OUST hit a site-side 429 from Stock Taper, not a tool limit).
- Guard (`intraday.py guard`): moved nothing.
- Judges: all four ran on their pinned agents — panel-judge-opus5 (claude-opus-5), -opus55 (claude-opus-5-5), -sonnet55 (claude-sonnet-5-5), -fable51 (claude-fable-5-1); full coverage, no retries.
- Scored `panel_score.py --dry-run --stage E-PS`; panel history untouched.
- Claim to done: 18:35:50 → ~18:51 UTC, about 15 minutes.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 LIME     amc     yes  95 long     1  opus5: 94L* opus55: 96L* sonnet55: 95L* fable51: 94L*  4  +2.12  +4.72% [+2.73, +6.48]           0.72
   2 CRCT     amc     yes  86 long     2  opus5: 86L* opus55: 88L* sonnet55: 87L* fable51: 82L*  4  +1.47  +3.46% [+1.36, +5.46]           0.65
   3 SEDG     bmo          57 short   28  opus5: 21S  opus55: 72S  sonnet55: 94S* fable51: 42S   1  -0.77  +0.59% [-0.21, +2.07]           0.56
   4 DIN      bmo          50 long     8  opus5: 49L  opus55: 41L  sonnet55: 50L  fable51: 62L   0  +0.52  +0.30% [-0.41, +1.49]           0.56
   5 OUST     amc          27 short   48  opus5: 72S  opus55: 18L  sonnet55: 24L  fable51: 77S   0  -0.37  +0.29% [-0.57, +0.84]           0.56
```

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
