# Stage E-PS — shard 1 of 4 — 2026-11-03

This is stage E-PS, shard 1 of four, run beside stage E-P with Opus 5.5 searchers
(`unpriced-searcher`) and a blind four-model panel, on E-P's own names, sweep rows and
sealed baselines (main `d441df90`). **No orders.** Scored `--dry-run` against stage E-P's
panel history; nothing written to it.

- Names: DUOL, TREE, MQ, TOST (amc 2026-11-03), XPEL (bmo 2026-11-04).
- Searchers: 5 of 5 returned, all `search_complete: true`; none reported its search budget
  running out (only site-side 403/429/503 refusals).
- Judges: all four ran on their pinned agents — opus5 (`claude-opus-5`), opus55
  (`claude-opus-5-5`), sonnet55 (`claude-sonnet-5-5`), fable51 (`claude-fable-5-1`);
  5 of 5 packs covered by each.
- Guard (`intraday.py guard`): moved nothing.
- Claim 18:27 UTC, panel scored 18:40 UTC: about 13 minutes claim-to-done.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.70|, sonnet55 |1.45|, fable51 |1.80|  (live sizes before 2026-11-03, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 TREE     amc     yes  99 long     1  opus5:100L* opus55: 98L* sonnet55: 98L* fable51: 99L*  4  +3.00  +5.02% [+3.18, +6.67]           0.73
   2 MQ       amc          76 short    7  opus5: 82S* opus55: 68S  sonnet55: 70S  fable51: 84S*  2  -1.09  +2.07% [+0.40, +3.90]           0.57
   3 DUOL     amc          42 short   50  opus5: 90S* opus55: 40L  sonnet55: 50S  fable51: 70S   1  -0.73  +0.29% [-0.50, +1.01]           0.56
   4 TOST     amc          42 long    25  opus5: 20L  opus55: 66L  sonnet55: 70L  fable51: 14L   0  +0.56  +0.29% [-0.50, +1.00]           0.56
   5 XPEL     bmo          17 short   27  opus5: 36S  opus55:  0-  sonnet55: 50S  fable51: 16L   0  -0.23  +0.29% [-0.63, +0.82]           0.56
```

Searcher `impact_sum`: TREE +4.40, TOST +1.60, DUOL +0.20, MQ −0.50, XPEL −0.80.
The expected return is the calibration curve's translation of the percentile, gross, not a
forecast for this name. One day is an anecdote; judge this stage only pooled against E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
