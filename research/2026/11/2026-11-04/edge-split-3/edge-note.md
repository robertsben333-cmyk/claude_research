# Stage E-PS, shard 3 of 4: 2026-11-04

This is stage E-PS, shard 3 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel. **It places no orders.**

- **Names:** LEU (amc), CHYM (amc), JOBY (amc), NVAX (bmo), EOSE (bmo).
- **Judges:** all four ran as their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1).
- **Guard:** it moved nothing.
- **Search budget:** no searcher ran out; all five wrote `search_complete: true`.
- **Timing:** claimed 18:12 UTC, panel scored 18:27 UTC, so about 17 minutes from claim to done.
- **Scoring:** `--dry-run --stage E-PS` against E-P's history, which was not written.
- **Selected:** none. The highest name is LEU at panel_pct 72 long, and all four judges put it in the 70s on the long side.

One day is an anecdote.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 LEU      amc          72 long     3  opus5: 76L  opus55: 72L  sonnet55: 70L  fable51: 70L   0  +1.01  +1.74% [+0.28, +3.49]           0.56
   2 JOBY     amc          18 long    37  opus5: 56L  opus55: 38S  sonnet55: 48L  fable51:  6L   0  +0.29  +0.29% [-0.62, +0.82]           0.56
   3 EOSE     bmo          10 short   48  opus5: 17L  opus55: 65S  sonnet55: 55L  fable51: 46S   0  -0.17  +0.29% [-0.69, +0.80]           0.56
   4 NVAX     bmo           4 long    22  opus5: 12S  opus55: 20S  sonnet55: 34L  fable51: 18L   0  +0.03  +0.29% [-0.73, +0.78]           0.56
   5 CHYM     amc           4 long    39  opus5: 13L  opus55: 44S  sonnet55: 62L  fable51: 18S   0  -0.02  +0.29% [-0.74, +0.78]           0.56
```

E[return] is gross, measured over the scorebord's window, and flat at about +0.3% below a percentile of 50. It is the translation of the percentile, not a separate forecast.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
