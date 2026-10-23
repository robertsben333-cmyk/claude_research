# Stage E-PS — shard 4 of 4 — 2026-10-23

This is stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (source commit `e55276cd`). **No orders.**

- Names: ABOS, BFST, VZ (all bmo, 2026-10-26). Three names, not five: the plan held fewer than twenty.
- Searchers: 3 of 3 `unpriced-searcher` (Opus 5.5) returned; none reported its search budget running out.
- Judges: all four ran on their pinned agents (`panel-judge-opus5` claude-opus-5, `-opus55` claude-opus-5-5, `-sonnet55` claude-sonnet-5-5, `-fable51` claude-fable-5-1); coverage 3 of 3 for each.
- Guard (`intraday.py guard`): moved nothing.
- Claim to done: claim returned about 17:15 UTC, panel scored 17:24 UTC, about 10 minutes.
- Scored `panel_score.py --dry-run --stage E-PS`: panel history untouched.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.44|  (live sizes before 2026-10-23, n=164 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ABOS     bmo          64 short    5  opus5: 59S  opus55: 73S  sonnet55: 65S  fable51: 60S   0  -0.83  +1.13% [+0.02, +2.71]           0.56
   2 VZ       bmo          36 long    13  opus5: 18L  opus55: 54L  sonnet55: 32L  fable51: 40L   0  +0.48  +0.29% [-0.54, +0.88]           0.56
   3 BFST     bmo          26 short   27  opus5: 43S  opus55: 34S  sonnet55: 20L  fable51: 48S   0  -0.44  +0.29% [-0.57, +0.84]           0.56
```

Nothing selected. The expected return is the translation of the percentile (gross, scorebord window, flat at about +0.3% below 50), not a forecast. Searcher `impact_sum`: ABOS −1.10, VZ −0.40, BFST −0.25; none clears the 2.8 floor.

One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
