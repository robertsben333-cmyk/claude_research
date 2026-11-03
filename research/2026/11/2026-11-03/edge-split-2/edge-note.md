# Stage E-PS — split panel, shard 2 of 4 — 2026-11-03

Stage E-PS runs beside stage E-P on E-P's own names, sweep and sealed baselines (source commit d441df9). This shard took five names (SMCI, TARS, W, CAR, ALAB). Each name had one Opus 5.5 `unpriced-searcher`, all launched in one message, and a blind four-model panel judged the evidence. **No orders.**

- **Judges:** all four ran on their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5) and fable51 (claude-fable-5-1). Each covered 4 of 4 packs.
- **Guard:** it moved nothing. Every hunt was written before 16:00 ET.
- **Search budget:** no searcher reported running out (search_complete true on 5 of 5). TARS and W hit site-level 403/429 refusals only.
- **SMCI:** `edge_score.py` did not rank it ("event date does not fit the filing cadence"), so it was neither packed nor judged.
- **Timing:** claimed 18:27 UTC, done about 18:42 UTC (15 minutes).

## Panel (as `panel_score.py --dry-run --stage E-PS` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.70|, sonnet55 |1.45|, fable51 |1.80|
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CAR      amc          68 short   18  opus5: 82S* opus55: 78S  sonnet55: 74S  fable51: 38S   1  -1.09  +1.40% [+0.14, +3.04]           0.56
   2 ALAB     amc          48 long    21  opus5: 49L  opus55: 48L  sonnet55: 76L  fable51: 17L   0  +0.56  +0.29% [-0.45, +1.28]           0.56
   3 TARS     amc          45 long    20  opus5: 16L  opus55: 48L  sonnet55: 46L  fable51: 70L   0  +0.49  +0.29% [-0.49, +1.10]           0.56
   4 W        bmo          16 long    18  opus5:  1L  opus55: 16L  sonnet55: 46L  fable51:  0-   0  +0.13  +0.29% [-0.65, +0.81]           0.56
```

Nothing is selected. One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
