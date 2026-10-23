# Stage E-PS — shard 1 of 4 — 2026-10-23

This is stage E-PS, shard 1 of four, run beside stage E-P with Opus 5.5 searchers
(`unpriced-searcher`) and a blind four-model panel, on E-P's own names, sweep and sealed
baselines (source commit e55276cd). No orders. Scored `--dry-run` against E-P's panel history.

- Names: RCBC (amc 10-23), ARLP, DEA, LKFN (bmo 10-26). LKFN: the sweep left it unconfirmed and
  the searcher found no company source either (aggregator + cadence only).
- Judges: all four ran on their pinned agents (opus5 claude-opus-5, opus55 claude-opus-5-5,
  sonnet55 claude-sonnet-5-5, fable51 claude-fable-5-1); full coverage, no relaunch.
- Guard: moved nothing. No searcher reported its search budget running out.
- Claim to done: claim 17:11 UTC, panel scored 17:25 UTC, about 15 minutes.
- No name selected (none at panel_pct >= 80). One day is an anecdote.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 DEA      bmo          70 short    6  opus5: 69S  opus55: 61S  sonnet55: 75S  fable51: 76S   0  -0.98  +1.56% [+0.22, +3.25]           0.56
   2 LKFN     bmo          70 long    11  opus5: 77L  opus55: 76L  sonnet55: 76L  fable51: 50L   1  +1.03  +1.53% [+0.21, +3.21]           0.56
   3 RCBC     amc          55 long    12  opus5: 60L  opus55: 48L  sonnet55: 73L  fable51: 40L   0  +0.74  +0.38% [-0.28, +1.88]           0.56
   4 ARLP     bmo          38 long    22  opus5: 37L  opus55: 46L  sonnet55: 65L  fable51:  5L   0  +0.50  +0.29% [-0.53, +0.90]           0.56
```

E[return] is what names at that percentile have earned (gross, scorebord window, flat near
+0.3% below 50), with a weak out-of-sample record; not a forecast to size on.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
