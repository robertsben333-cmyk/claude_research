# Stage E-PS — shard 3 of 4 — 2026-11-09

Stage E-PS, shard 3 of four, run beside stage E-P with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel on E-P's own names, sweep and baselines (from main 856d4f8). **No orders.** Scored `--dry-run --stage E-PS` against stage E-P's live judge range; the panel history was not written.

- Names: LQDA (bmo 11-10), RKLB (amc), LCID (amc), TTWO (amc), ONON (bmo 11-10). All five searchers in one message.
- Searchers: 5 of 5 returned with `search_complete: true`; none reported its search budget running out (only site-level 403/429s).
- Guard (`intraday.py guard`, 18:25:55 UTC): moved nothing.
- Judges: all four ran on their pinned agents — opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1); no fallbacks, full coverage.
- Claim to done: about 20 minutes (claimed ~18:12 UTC, scored 18:29 UTC).
- Searchers' own `impact_sum`: none clears the 2.8 floor (RKLB +0.50, LQDA −0.30, TTWO −0.50, LCID −0.60, ONON −0.70).

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.60|, opus55 |1.92|, sonnet55 |1.68|, fable51 |2.08|  (live sizes before 2026-11-09, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 LCID     amc     yes  87 short    9  opus5: 76S  opus55: 82S* sonnet55: 91S* fable51:100S*  3  -1.52  +3.66% [+1.56, +5.64]           0.66
   2 LQDA     bmo          78 short    1  opus5: 80S* opus55: 79S  sonnet55: 77S  fable51: 78S   2  -1.26  +2.43% [+0.55, +4.33]           0.59
   3 RKLB     amc          49 long    10  opus5: 56L  opus55: 40L  sonnet55: 62L  fable51: 40L   0  +0.63  +0.29% [-0.43, +1.41]           0.56
   4 TTWO     amc          42 short   36  opus5: 60S  opus55: 48S  sonnet55: 17L  fable51: 78S   0  -0.72  +0.29% [-0.50, +1.00]           0.56
   5 ONON     bmo           6 short    9  opus5: 14S  opus55:  9S  sonnet55:  9L  fable51:  8S   0  -0.14  +0.29% [-0.72, +0.79]           0.56
```

One day is an anecdote; judge this stage only pooled against stage E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
