# Stage E-PS — shard 3 of 4 — 2026-11-05

This is stage E-PS, shard 3 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel. **It places no orders.**

- **Names:** TMDX, TNDM, GRND and CRSR (amc 2026-11-05), and OKLO (bmo 2026-11-06).
- **Judges:** all four ran as their pinned agents: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). No judge wrote its model into its output. Coverage was 5 of 5 for every judge.
- **Guard:** moved nothing.
- **Searchers:** 5 of 5 finished, `search_complete: true`, and none reported running out of search budget.
- **Timing:** the fire was late. The claim came at 18:12 UTC, against a planned 17:07 to 17:10, and the panel was scored at 18:28 UTC. Claim to done was about 17 minutes.
- **Judge note:** on TMDX the Opus 5 judge reinstated three sell-side items (Evercore, Stifel, Needham). The searcher had rejected them as 2025 stories relabelled as 2026. They carry most of that judge's −2.24 on TMDX.

## Panel (as `panel_score.py --dry-run --stage E-PS` printed it)

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CRSR     amc     yes  90 long     6  opus5: 96L* opus55: 88L* sonnet55: 94L* fable51: 80L*  4  +1.70  +4.07% [+1.97, +6.02]           0.68
   2 GRND     amc          35 short   50  opus5: 90S* opus55: 45S  sonnet55: 46L  fable51: 53S   1  -0.62  +0.29% [-0.54, +0.87]           0.56
   3 OKLO     bmo          15 short   31  opus5: 36S  opus55: 38L  sonnet55: 36S  fable51: 27S   0  -0.39  +0.29% [-0.65, +0.81]           0.56
   4 TMDX     amc           8 long    58  opus5: 78S  opus55: 39L  sonnet55: 78L  fable51:  9S   0  +0.12  +0.29% [-0.71, +0.79]           0.56
   5 TNDM     amc           3 long    58  opus5: 78L  opus55: 50S  sonnet55: 56S  fable51: 40L   1  -0.03  +0.29% [-0.74, +0.78]           0.56
```

The searchers' own `impact_sum` values were TMDX +2.70, CRSR +1.80, GRND +0.20, OKLO −0.50 and TNDM −0.70. None clears the 2.8 floor.

One day is an anecdote. E[return] translates the percentile; it is not a forecast for this name.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
