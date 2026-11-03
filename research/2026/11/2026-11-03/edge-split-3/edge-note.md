# Stage E-PS — shard 3 of 4 — 2026-11-03

This is stage E-PS, shard 3 of four, run beside stage E-P with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel on E-P's own names, sweep and baselines (source commit d441df90). **It places no orders.** One day is an anecdote.

- Names: NVTS, RVLV, FRSH (amc 2026-11-03); HUT, RIOT (bmo 2026-11-04).
- Judges: all four ran on their pinned agents — `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5), `-fable51` (claude-fable-5-1). No fallback, no retry; every member covered 5 of 5 ids.
- Guard (`intraday.py guard`): moved nothing.
- Search budget: no searcher reported a refused or exhausted search; `hunt_status.py` 0 unfinished of 5.
- Timing: fired 18:11 UTC (about an hour after the 17:07 the prompt states); claimed 18:28 UTC; searchers 18:30–18:38; panel scored 18:42 UTC. Claim-to-done ≈ 16 minutes.
- Selected: **none** (no name reached panel_pct 80).

## Panel (as `panel_score.py --dry-run --stage E-PS` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.70|, sonnet55 |1.45|, fable51 |1.80|  (live sizes before 2026-11-03, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 NVTS     amc          72 short   20  opus5: 40S  opus55: 68S  sonnet55: 86S* fable51: 94S*  2  -1.14  +1.73% [+0.28, +3.47]           0.56
   2 FRSH     amc          71 short    4  opus5: 70S  opus55: 68S  sonnet55: 70S  fable51: 77S   0  -0.92  +1.64% [+0.25, +3.36]           0.56
   3 RIOT     bmo          68 long    13  opus5: 83L* opus55: 77L  sonnet55: 50L  fable51: 62L   1  +0.99  +1.40% [+0.14, +3.04]           0.56
   4 RVLV     amc          63 short   11  opus5: 57S  opus55: 48S  sonnet55: 76S  fable51: 71S   0  -0.86  +1.04% [-0.02, +2.58]           0.56
   5 HUT      bmo          32 short   44  opus5: 40L  opus55: 36S  sonnet55: 70S  fable51: 62S   0  -0.60  +0.29% [-0.56, +0.86]           0.56
```

Searcher's own `impact_sum` (comparison arm): RIOT +2.00, HUT +1.20, FRSH +0.20, NVTS −0.50, RVLV −0.50; none clears the 2.8 floor.

Nothing checked the findings factually; the key is not reproducible to better than its own size.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
