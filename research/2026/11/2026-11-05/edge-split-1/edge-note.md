# Stage E-PS — shard 1 of 4 — 2026-11-05

This is stage E-PS: one shard of stage E-P's own names, run beside stage E-P with Opus 5.5
searchers (`unpriced-searcher`, agent form) and a blind four-model panel, on E-P's own
names, sweep rows and sealed baselines (source commit 096f231f). It places no orders.
Scored `panel_score.py --dry-run --stage E-PS` against stage E-P's live history; the
history was not written.

- Names: AAOI, SG, SOUN, OMDA, FNKO (all amc 2026-11-05). OMDA's searcher was told its baseline carries `cadence_implausible`.
- Judges: all four ran on their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1). Each covered 5 of 5 packs.
- Guard (`intraday.py guard`): moved nothing (18:24 UTC, before the 16:00 ET cutoff).
- Search budget: no searcher reported its search budget running out; all five `search_complete: true`. SG and SOUN met site-side 403/429/503 refusals only.
- Claim to done: about 14 minutes (claimed ~18:15 UTC, panel scored 18:28 UTC). The fire itself was late: the session's clock read 18:14 UTC at start, against an intended 17:07-17:10.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.40|, opus55 |1.76|, sonnet55 |1.50|, fable51 |2.00|  (live sizes before 2026-11-05, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 FNKO     amc     yes  97 long     2  opus5:100L* opus55: 94L* sonnet55: 98L* fable51: 96L*  4  +2.36  +4.88% [+2.97, +6.59]           0.72
   2 SOUN     amc          80 long     3  opus5: 84L* opus55: 75L  sonnet55: 78L  fable51: 82L*  2  +1.24  +2.59% [+0.61, +4.52]           0.60
   3 OMDA     amc          75 long    14  opus5: 76L  opus55: 72L  sonnet55: 94L* fable51: 56L   1  +1.09  +1.99% [+0.37, +3.81]           0.57
   4 AAOI     amc          65 long    22  opus5: 50L  opus55: 76L  sonnet55: 95L* fable51: 40L   1  +0.90  +1.19% [+0.05, +2.78]           0.56
   5 SG       amc          38 long    34  opus5: 11S  opus55: 72L  sonnet55: 68L  fable51: 26L   0  +0.58  +0.29% [-0.52, +0.91]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

One name selected (FNKO, all four judges in their own top 20% on the long side). SOUN sits
at the edge (shown as 80, not selected, so below 80 before rounding). One day is an anecdote.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
