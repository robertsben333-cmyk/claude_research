# Stage E-PS — shard 2 of 4 — 2026-10-28

Stage E-PS, shard 2 of four, run beside stage E-P with Opus 5.5 `unpriced-searcher` agents and a blind
four-model panel on E-P's own names, sweep rows and sealed baselines (source commit 9f2b3de6). No orders.
Panel scored `--dry-run --stage E-PS` against stage E-P's live history; nothing written to it.

- Names: MDXG, PRCH, MAX (amc 2026-10-28), BFLY, HIPO (bmo 2026-10-29).
- Searchers: 5 of 5 returned (agent form, not the fallback); none reported its search budget running out.
- Guard (`intraday.py guard`, 18:21 UTC): moved nothing.
- Judges: all four ran on their pinned agents — opus5 (claude-opus-5), opus55 (claude-opus-5-5),
  sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1). No fallback, no refusal.
- Claim 18:12 UTC to panel scored 18:27 UTC: about 15 minutes.

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.20|, sonnet55 |1.20|, fable51 |1.44|  (live sizes before 2026-10-28, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 BFLY     bmo     yes  99 long     0  opus5:100L* opus55: 99L* sonnet55:100L* fable51: 99L*  4  +2.86  +5.05% [+3.22, +6.69]           0.73
   2 PRCH     amc     yes  98 long     1  opus5: 97L* opus55: 98L* sonnet55:100L* fable51: 99L*  4  +2.73  +4.99% [+3.13, +6.66]           0.73
   3 MAX      amc     yes  86 short    5  opus5: 94S* opus55: 84S* sonnet55: 79S  fable51: 85S*  3  -1.25  +3.42% [+1.31, +5.42]           0.65
   4 MDXG     amc          45 long    37  opus5: 18S  opus55: 75L  sonnet55: 60L  fable51: 62L   0  +0.65  +0.29% [-0.49, +1.10]           0.56
   5 HIPO     bmo          28 long    49  opus5: 53S  opus55: 64L  sonnet55: 71L  fable51: 29L   0  +0.53  +0.29% [-0.57, +0.85]           0.56
```

E[return] is gross, on the scorebord window, one number per percentile. One day is an anecdote; this
shard is judged only pooled against stage E-P over many days.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by
market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
