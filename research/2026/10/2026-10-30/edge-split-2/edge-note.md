# Stage E-PS — shard 2 of 4 — 2026-10-30

This is stage E-PS, shard 2 of four, run beside stage E-P with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel on E-P's own names, sweep and baselines (source commit 05d32b44). **No orders.** One day is an anecdote.

- Names: KRYS, EL, IDXX, MAR, L, all bmo 2026-11-02 (window: close Fri 10-30 to close Mon 11-02). L's session was unconfirmed by the sweep; its searcher settled it as bmo (7 of 7 prior prints bmo by 8-K time; CNA reports before the open the same day).
- Judges: all four ran as the named agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5), `-fable51` (claude-fable-5-1). No fallbacks were needed and every pack was covered by every judge.
- Guard: moved nothing (no amc names).
- Search budget: 0 of 5 searchers ran out (`hunt_status`: 0 unfinished).
- Timing: claimed 18:11 UTC (the Routine fired about an hour after the scheduled 17:07); searchers done 18:18; panel scored 18:22, so about 12 minutes from claim to done.
- Selected: none. No name reaches panel_pct 80, and no name's searcher `impact_sum` clears the 2.8 floor.

## Panel (as printed by `panel_score.py --dry-run --stage E-PS`)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.04|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-10-30, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 IDXX     bmo          62 short   10  opus5: 53S  opus55: 62S  sonnet55: 55S  fable51: 78S   0  -0.65  +0.96% [-0.06, +2.47]           0.56
   2 KRYS     bmo          57 short   19  opus5: 74S  opus55: 63S  sonnet55: 67S  fable51: 26S   0  -0.74  +0.59% [-0.21, +2.07]           0.56
   3 L        bmo          29 short   13  opus5: 36S  opus55: 14S  sonnet55: 18S  fable51: 46S   0  -0.31  +0.29% [-0.56, +0.85]           0.56
   4 MAR      bmo          10 short   21  opus5:  4S  opus55: 12L  sonnet55:  4S  fable51: 46S   0  -0.10  +0.29% [-0.68, +0.80]           0.56
   5 EL       bmo           4 short   25  opus5: 28S  opus55: 29L  sonnet55: 29S  fable51: 10L   0  -0.06  +0.29% [-0.73, +0.78]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

The E[return] column is the frozen calibration curve read at each name's percentile. It is not a forecast for any individual name.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
