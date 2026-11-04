# Stage E-PS — split panel, shard 2 of 4 — 2026-11-04

This is stage E-PS, shard 2 of four. It ran beside stage E-P on E-P's own names, sweep and baselines, with Opus 5.5 `unpriced-searcher`s and a blind four-model panel. **It places no orders.**

- Names: BYND, FSLY, ELF (amc 2026-11-04); OSCR, CORZ (bmo 2026-11-05).
- Judges: all four ran under their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5) and fable51 (claude-fable-5-1). No fallback was used.
- Guard: moved nothing.
- Search budget: no searcher ran out (hunt_status: 0 of 5 unfinished).
- Scoring: `panel_score.py --dry-run --stage E-PS`, so the panel history was not written.
- Timing: claimed at 18:09 UTC, panel scored at 18:29 UTC, about 21 minutes.
- Selection: none. FSLY was the strongest at panel_pct 77 (short), with 3 of 4 judges in their own top 20%, which is below the 80 mean-percentile bar.
- Data caveat: the CORZ searcher quotes a 2026-11-04 "close" of $12.78 (-10.25%), but the session was still open when it wrote. Read it as an intraday quote.

One day is an anecdote.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.24|, opus55 |1.70|, sonnet55 |1.50|, fable51 |1.92|  (live sizes before 2026-11-04, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 FSLY     amc          77 short   15  opus5: 90S* opus55: 52S  sonnet55: 85S* fable51: 82S*  3  -1.34  +2.26% [+0.48, +4.13]           0.58
   2 OSCR     bmo          29 long    28  opus5: 10S  opus55: 62L  sonnet55: 48L  fable51: 15L   0  +0.37  +0.29% [-0.56, +0.85]           0.56
   3 ELF      amc          24 short   44  opus5: 52S  opus55: 34L  sonnet55:  0-  fable51: 80S   1  -0.35  +0.29% [-0.58, +0.84]           0.56
   4 BYND     amc          23 short   60  opus5: 26L  opus55: 92S* sonnet55: 74S  fable51: 46L   1  -0.29  +0.29% [-0.58, +0.83]           0.56
   5 CORZ     bmo           9 short   45  opus5: 71S  opus55: 54L  sonnet55: 26S  fable51:  6L   0  -0.09  +0.29% [-0.69, +0.80]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
