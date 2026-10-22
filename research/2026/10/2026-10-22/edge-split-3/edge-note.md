# Stage E-PS — split panel, shard 3 of 4 — 2026-10-22

Stage E-PS, shard 3 of four: Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel on stage E-P's own names, sweep rows and sealed baselines (copied from `main` at 2d0221d). **No orders placed.** Scored `panel_score.py --dry-run --stage E-PS`: each judge read against stage E-P's live range from runs before today; E-P's panel history untouched.

- Names: JAKK, FPH, RNG (amc 2026-10-22), INFY, AXP (bmo 2026-10-23). All five searchers launched in one message, all returned; none reported its search budget running out.
- INFY's searcher was told `baseline_history_trustworthy: false` / `cadence_implausible`.
- Guard (`intraday.py guard`, cutoff 16:00 ET): moved nothing.
- Judges: all four ran on their pinned agents — panel-judge-opus5 (claude-opus-5), -opus55 (claude-opus-5-5), -sonnet55 (claude-sonnet-5-5), -fable51 (claude-fable-5-1). Full coverage, no relaunch.
- Claim 18:03 UTC → panel scored 18:16 UTC, about 13 minutes.
- Searcher `impact_sum`: JAKK +0.70, RNG +0.40, INFY −0.00, AXP −0.10, FPH −1.90; none clears the 2.8 floor.

## Panel

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 FPH      amc     yes  82 short   11  opus5: 96S* opus55: 69S  sonnet55: 88S* fable51: 73S   3  -1.38  +2.84% [+0.82, +4.81]           0.62
   2 RNG      amc          67 long    19  opus5: 76L  opus55: 76L  sonnet55: 34L  fable51: 81L*  1  +1.13  +1.31% [+0.11, +2.94]           0.56
   3 AXP      bmo          38 short   16  opus5: 56S  opus55: 43S  sonnet55: 11S  fable51: 41S   0  -0.54  +0.29% [-0.53, +0.90]           0.56
   4 JAKK     amc          32 long    12  opus5: 43L  opus55: 41L  sonnet55: 34L  fable51: 12L   0  +0.47  +0.29% [-0.55, +0.86]           0.56
   5 INFY     bmo           8 short    8  opus5: 13S  opus55: 14S  sonnet55:  5L  fable51: 12S   0  -0.20  +0.29% [-0.70, +0.79]           0.56
```

One selected (FPH short, panel_pct 82). One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
