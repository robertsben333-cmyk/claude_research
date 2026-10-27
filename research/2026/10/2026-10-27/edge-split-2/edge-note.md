# Stage E-PS — shard 2 of 4 — 2026-10-27

This is stage E-PS, shard 2 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines (source commit a0955166), with Opus 5.5 `unpriced-searcher`s and a blind four-model panel. **It places no orders.** The panel is scored `--dry-run` against stage E-P's live history from runs before today, so these percentiles sit on E-P's scale.

- Names: BOOM, ENPH, INTA, BRSP (amc 2026-10-27), JMKE (bmo 2026-10-28). Five searchers ran in one message; all five returned, none reported running out of search budget.
- Judges: all four ran as their pinned agents (opus5 `claude-opus-5`, opus55 `claude-opus-5-5`, sonnet55 `claude-sonnet-5-5`, fable51 `claude-fable-5-1`); 5 of 5 ids in every file; none missing.
- Guard (`intraday.py guard`, 16:00 ET cutoff): moved nothing.
- Searcher key: 0 of 5 names clear the 2.8 conviction floor.
- Claim 17:22 UTC, panel scored 17:34 UTC: about 12 minutes claim-to-done (17:09 fire; the first claim waited for E-P's sweep until about 17:19).
- **Panel: 0 of 5 selected.** The highest are BOOM, INTA and ENPH at a mean percentile of 67-68 on the short side, below the 80 gate.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.19|, sonnet55 |1.15|, fable51 |1.44|  (live sizes before 2026-10-27, opus5 n=196 live, opus55 n=196 live, sonnet55 n=196 live, fable51 n=196 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 BOOM     amc          68 short   23  opus5: 63S  opus55: 35S  sonnet55: 80S* fable51: 96S*  2  -1.00  +1.43% [+0.16, +3.09]           0.56
   2 INTA     amc          68 short   18  opus5: 94S* opus55: 73S  sonnet55: 47S  fable51: 58S   1  -0.86  +1.41% [+0.15, +3.06]           0.56
   3 ENPH     amc          67 short   28  opus5: 18S  opus55: 83S* sonnet55: 79S  fable51: 87S*  2  -1.16  +1.30% [+0.10, +2.92]           0.56
   4 BRSP     amc          42 long    13  opus5: 31L  opus55: 52L  sonnet55: 57L  fable51: 26L   0  +0.48  +0.29% [-0.50, +0.98]           0.56
   5 JMKE     bmo          30 long    44  opus5: 76L  opus55: 42L  sonnet55: 43S  fable51: 44L   0  +0.51  +0.29% [-0.56, +0.85]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

E[return] is what names at that percentile have earned on the panel's side: gross, on the scorebord window, flat at about +0.3% below a percentile of 50. It translates the percentile and is not a separate forecast. Its out-of-sample record is weak (correlation +0.12).

One day is an anecdote. Judge the stage only pooled over days, against stage E-P on the same names.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
