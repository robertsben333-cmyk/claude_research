# Stage E-PS — shard 2 of 4 — 2026-11-05

This is stage E-PS, shard 2 of four, run beside stage E-P. It uses Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel on stage E-P's own names, sweep rows and sealed baselines (source commit `096f231f`). It places no orders.

- **Names:** INOD, KRUS, TRUP and ETON report after the close (amc) on 2026-11-05; WULF reports before the open (bmo) on 2026-11-06.
- **Searchers:** 5 of 5 returned and every one reports `search_complete: true`. None ran out of search budget.
- **Guard** (`intraday.py guard`): moved nothing.
- **Judges:** all four ran on their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). No fallback was used.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`. The panel history was not written.
- **Timing:** claimed at 18:10 UTC, panel scored at 18:29 UTC, so about 20 minutes from claim to done.
- **Searcher's own key:** 0 of 5 names clear the 2.8 floor. The largest is ETON at +2.70.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ETON     amc     yes  90 long     8  opus5: 76L  opus55: 91L* sonnet55: 94L* fable51: 98L*  3  +1.77  +4.08% [+1.99, +6.03]           0.68
   2 WULF     bmo          27 long    28  opus5: 60L  opus55: 39L  sonnet55: 17S  fable51: 27L   0  +0.42  +0.29% [-0.57, +0.84]           0.56
   3 KRUS     amc          10 short   39  opus5: 11S  opus55: 60S  sonnet55: 17S  fable51: 50L   0  -0.23  +0.29% [-0.69, +0.80]           0.56
   4 TRUP     amc          10 short   49  opus5: 11S  opus55: 34S  sonnet55: 70L  fable51: 62S   0  -0.32  +0.29% [-0.69, +0.80]           0.56
   5 INOD     amc           5 short   69  opus5: 48L  opus55: 76S  sonnet55: 70S  fable51: 80L*  0  -0.09  +0.29% [-0.73, +0.78]           0.56
```

This is one day, so it is an anecdote. Judge the stage only pooled over days, against stage E-P on the same names.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
