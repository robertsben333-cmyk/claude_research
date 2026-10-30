# Stage E-PS — shard 3 of 4 — 2026-10-30 (prints 2026-11-02 bmo)

This is stage E-PS, shard 3 of four, run beside stage E-P with Opus 5.5 `unpriced-searcher`s and a blind four-model panel on E-P's own names, sweep and baselines (source commit 05d32b44). **No orders placed.**

- Names: TEM, TSEM, CHKP, AKR, ETR (all bmo 2026-11-02). 5 of 5 searchers returned, all `search_complete: true`; none reported a search budget running out.
- Judges: all four ran on their pinned agents (panel-judge-opus5 / claude-opus-5, -opus55 / claude-opus-5-5, -sonnet55 / claude-sonnet-5-5, -fable51 / claude-fable-5-1), full coverage, no retries. Scored `--dry-run --stage E-PS`; E-P's panel history untouched.
- Guard (`intraday.py guard`): moved nothing.
- The session fired late: claimed at 18:12 UTC (14:12 ET), done about 18:26 UTC — claim to done about 14 minutes.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CHKP     bmo     yes  86 short    4  opus5: 89S* opus55: 91S* sonnet55: 82S* fable51: 84S*  4  -1.48  +3.52% [+1.42, +5.52]           0.65
   2 TSEM     bmo     yes  84 long     8  opus5: 88L* opus55: 76L  sonnet55: 76L  fable51: 94L*  2  +1.29  +3.18% [+1.10, +5.17]           0.64
   3 TEM      bmo          33 long    22  opus5:  4S  opus55: 37L  sonnet55: 54L  fable51: 46L   0  +0.47  +0.29% [-0.55, +0.86]           0.56
   4 AKR      bmo          31 long     6  opus5: 28L  opus55: 40L  sonnet55: 29L  fable51: 26L   0  +0.36  +0.29% [-0.56, +0.85]           0.56
   5 ETR      bmo          25 long    11  opus5: 12L  opus55: 32L  sonnet55: 39L  fable51: 17L   0  +0.32  +0.29% [-0.57, +0.84]           0.56
```

One day is an anecdote; judge this stage only pooled against stage E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
