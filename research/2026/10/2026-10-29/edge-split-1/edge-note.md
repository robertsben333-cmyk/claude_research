# Stage E-PS — shard 1 of 4 — 2026-10-29

This is stage E-PS, shard 1 of four, run beside stage E-P. Opus 5.5 searchers looked at E-P's own names, using E-P's sweep and baselines, and a blind four-model panel judged them. No orders were placed.

- **Names:** ALHC, ATEC, AXTI, COUR and INTC, all reporting after the close on 2026-10-29.
- **Judges:** all four ran on their pinned agents: Opus 5 (`panel-judge-opus5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. None used a fallback.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`, so the panel history was not written.
- **Late-release check (guard):** moved nothing.
- **Search budget:** no searcher ran out of it. `hunt_status` reports 0 of 5 unfinished.
- **INTC baseline:** the sealed baseline failed (`bars_failed: HTTPError`). Its scale rests on the third-party implied move of ±9.2–9.4% that the searcher sourced.
- **Timing:** the session fired late. The claim was at 18:09 UTC, not the intended 17:07–17:10. Claim to done was about 15 minutes.

One day is an anecdote.

## Panel table (as printed by panel_score.py)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.50|  (live sizes before 2026-10-29, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 AXTI     amc     yes  91 long     6  opus5: 86L* opus55: 83L* sonnet55: 98L* fable51: 96L*  4  +2.03  +4.22% [+2.14, +6.13]           0.69
   2 ATEC     amc          80 short    7  opus5: 92S* opus55: 75S  sonnet55: 80S  fable51: 74S   2  -1.05  +2.60% [+0.62, +4.53]           0.60
   3 ALHC     amc          78 short    4  opus5: 80S* opus55: 75S  sonnet55: 72S  fable51: 84S*  2  -1.12  +2.32% [+0.50, +4.20]           0.58
   4 COUR     amc          66 long    21  opus5: 38L  opus55: 85L* sonnet55: 52L  fable51: 86L*  2  +0.95  +1.22% [+0.06, +2.82]           0.56
   5 INTC     amc          12 short   32  opus5: 53S  opus55: 30S  sonnet55: 30L  fable51:  4L   0  -0.09  +0.29% [-0.67, +0.81]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

One name was selected: AXTI, long, with all four judges in their own top 20%. ATEC prints as 80 short but is 79.9 unrounded, so it is not selected. The expected-return column is gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It is a translation of the percentile, not a forecast.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
