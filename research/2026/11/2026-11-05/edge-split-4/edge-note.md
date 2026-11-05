# Stage E-PS — shard 4 of 4 — 2026-11-05

This is stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (source commit 096f231f). **No orders placed.**

- Names: UMAC, CELC, CARG, HNST (amc 2026-11-05), UAA (bmo 2026-11-06).
- Searchers: 5 of 5 `unpriced-searcher`, one message, all `search_complete: true`; none reported its search budget running out.
- Judges: all four ran as their own pinned agents (panel-judge-opus5 / -opus55 / -sonnet55 / -fable51), no fallback, 5 of 5 ids each.
- Guard (`intraday.py guard`): moved nothing.
- Claim 18:16 UTC → panel scored 18:28 UTC: about 12 minutes.
- Scored `panel_score.py --dry-run --stage E-PS`; panel history untouched.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 HNST     amc     yes  93 long     8  opus5: 99L* opus55: 80L  sonnet55: 93L* fable51: 99L*  4  +2.12  +4.44% [+2.40, +6.28]           0.70
   2 UMAC     amc          77 long     6  opus5: 78L  opus55: 84L* sonnet55: 68L  fable51: 77L   2  +1.25  +2.20% [+0.45, +4.06]           0.58
   3 CARG     amc          64 short    8  opus5: 71S  opus55: 61S  sonnet55: 74S  fable51: 52S   0  -0.86  +1.14% [+0.02, +2.72]           0.56
   4 UAA      bmo          59 short   12  opus5: 45S  opus55: 64S  sonnet55: 52S  fable51: 76S   0  -0.73  +0.74% [-0.15, +2.21]           0.56
   5 CELC     amc          55 long     4  opus5: 50L  opus55: 56L  sonnet55: 62L  fable51: 53L   0  +0.70  +0.41% [-0.27, +1.91]           0.56
```

One day is an anecdote; judge this stage pooled against stage E-P over many days.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
