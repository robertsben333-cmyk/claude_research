# Stage E-PS — shard 4 of 4 — 2026-10-29

This is stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (from main `a633993a`). **It places no orders.**

- Names: PTCT, SPSC, OSPN, GDYN (amc 2026-10-29), CRI (bmo 2026-10-30). GDYN was unconfirmed by the sweep; its searcher confirmed it itself (Business Wire 2026-09-29, Q3 after the close).
- Searchers: 5 `unpriced-searcher` in one message, 18:16 to 18:23 UTC. All five report `search_complete: true`; none hit the search budget (only site-side 403/429/503 errors from stocktaper, benzinga, nasdaq). 5 of 5 rankable; none clears the 2.8 `impact_sum` floor.
- Guard (`intraday.py guard`, 18:23 UTC = 14:23 ET): moved nothing.
- Judges: all four ran on their pinned agents: opus5 (`claude-opus-5`), opus55 (`claude-opus-5-5`), sonnet55 (`claude-sonnet-5-5`), fable51 (`claude-fable-5-1`). Full coverage, 5 of 5 ids each. Scored with `--dry-run --stage E-PS`, so the panel history is untouched.
- Claim to done: about 14 minutes (claim 18:15 UTC, panel scored 18:27 UTC). The fire came at 18:14 UTC, not the 17:07–17:10 the prompt states.
- **Selected: none.** The top name, PTCT, reads panel_pct 72 long: three judges put it in their own top 20%, but Sonnet 5.5 reads it at 30.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.50|  (live sizes before 2026-10-29, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 PTCT     amc          72 long    25  opus5: 86L* opus55: 92L* sonnet55: 30L  fable51: 82L*  3  +1.30  +1.75% [+0.29, +3.50]           0.56
   2 GDYN     amc          65 short    9  opus5: 72S  opus55: 54S  sonnet55: 58S  fable51: 76S   0  -0.74  +1.18% [+0.04, +2.77]           0.56
   3 SPSC     amc          46 short   13  opus5: 53S  opus55: 60S  sonnet55: 44S  fable51: 26S   0  -0.51  +0.29% [-0.47, +1.17]           0.56
   4 CRI      bmo          34 long    50  opus5: 72L  opus55: 34L  sonnet55: 77L  fable51: 48S   0  +0.62  +0.29% [-0.55, +0.87]           0.56
   5 OSPN     amc          13 long    25  opus5:  4S  opus55: 12L  sonnet55: 54L  fable51: 10S   0  +0.01  +0.29% [-0.67, +0.81]           0.56
```

E[return] is what names at that percentile have earned on the panel's side: gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. Out of sample it correlates only weakly with the realised return (+0.12). It is not a forecast to size on.

Searcher `impact_sum`: CRI +1.50, PTCT +0.80, OSPN +0.45, GDYN −1.10, SPSC −1.20.

This is one day, and one day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
