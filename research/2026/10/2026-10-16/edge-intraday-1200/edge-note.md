# Stage E-PI — intraday panel, snapshot 12:00 New York, 2026-10-16

This is stage E-PI: stage E-P re-run from scratch at 12:00 ET, with Opus 5.5 `unpriced-searcher` agents and a blind four-model panel (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1, all four present, no fallback). It places no orders. This is the day's first snapshot: no 10:00 snapshot exists on disk, so this one built the universe and the sweep and froze the names.

- Window: 2026-10-16 amc plus 2026-10-19 bmo. 3 of 46 calendar rows: FITB, CLF and DX, all Monday bmo. There are no amc names tonight, so the release guard moved nothing.
- Thin-day check: running with `--include-unknown` gave 23 rows. `session_resolve` killed 5 (HDB, IBN, PAC and PBAM had already reported; HIFS had no CIK), carried 15 and confirmed none by press release. The unknown rows were withheld.
- The sweep confirmed 3 of 3 names from company releases. Baselines: FITB implied move 7.34%, CLF 12.44%, DX no option chain.
- The panel was scored with `--dry-run --stage E-PI`. The panel history was not written.

## Panel, as panel_score.py printed it

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.92|, opus55 |1.00|, sonnet55 |1.00|, fable51 |1.33|  (live sizes before 2026-10-16, opus5 n=73 live, opus55 n=73 live, sonnet55 n=73 live, fable51 n=73 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CLF      bmo     yes  95 long     2  opus5: 94L* opus55: 94L* sonnet55: 97L* fable51: 93L*  4  +2.58  +4.73% [+2.75, +6.49]           0.72
   2 FITB     bmo          26 long    10  opus5: 20L  opus55: 41L  sonnet55: 27L  fable51: 15L   0  +0.30  +0.29% [-0.57, +0.84]           0.56
   3 DX       bmo           9 long     6  opus5: 12L  opus55:  4L  sonnet55: 18L  fable51:  3L   0  +0.14  +0.29% [-0.69, +0.80]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

**CLF** is selected, 4 of 4, at a mean percentile of 95, long. The evidence:
- US HRC spot kept rising after the July guide: Nucor CSP went from $1,135 to $1,240 a short ton by 12 Oct, and SMU had $1,280 a short ton for the week of 15 Oct. That is about $100 a short ton above the level the "Q4 exceeds Q3" guide was set on.
- About 15% of the float is short, and the skew already pays for upside.

The case against:
- Stelco is idling Hamilton, Canada has a 50% counter-tariff on US steel, and Stellantis North American shipments fell 12% year on year.
- The evidence agrees with the skew rather than beating it.
- The 5-day drift is -5.2%.
- The dated short interest is from April.

The searcher's own impact_sum is +2.70, below the 2.8 floor.

FITB (+0.10) and DX (0.00) are near non-results; every judge put them below its own median.

The expected return is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. It is what names at that percentile have earned, with a weak out-of-sample record (+0.12 correlation over 148 names). It is not a forecast to size on. Nothing checked the findings for factual errors.

One day is an anecdote. The snapshots of one day share their names and their market, so they are not independent evidence.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
