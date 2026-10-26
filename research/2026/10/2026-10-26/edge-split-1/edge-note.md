# Stage E-PS — shard 1 of 4 — 2026-10-26

This is stage E-PS, shard 1 of four, run beside stage E-P. It used Opus 5.5 `unpriced-searcher` agents and a blind four-model panel, on stage E-P's own names, sweep and baselines (copied from main at `ec020c77`). It places **no orders**.

- **Names:** CLS, ZDGE and BLX report amc on 2026-10-26. SOFI and CNC report bmo on 2026-10-27; the sweep had not confirmed either, and each searcher confirmed its date from the company's own release.
- **Judges:** all four ran as their pinned agents: `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5) and `panel-judge-fable51` (claude-fable-5-1). Each covered all 5 packs.
- **Guard:** the late-release guard (`intraday.py guard`) moved nothing.
- **Search budget:** no searcher reported running out of its search budget.
- **Timing:** about 13 minutes from claim to scored panel (claim returned about 17:21 UTC, panel scored 17:33 UTC).
- **Scoring:** panel scored `--dry-run --stage E-PS`, so stage E-P's panel history was not written.

One day is an anecdote.

## Panel (as printed by panel_score.py)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.08|, sonnet55 |1.08|, fable51 |1.36|  (live sizes before 2026-10-26, n=176 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CLS      amc     yes  91 long     6  opus5: 95L* opus55: 94L* sonnet55: 81L* fable51: 96L*  4  +1.99  +4.27% [+2.20, +6.16]           0.69
   2 SOFI     bmo          47 short   22  opus5: 53S  opus55: 52S  sonnet55: 71S  fable51: 11S   0  -0.66  +0.29% [-0.46, +1.22]           0.56
   3 BLX      amc          16 short    9  opus5: 18S  opus55:  7S  sonnet55: 10S  fable51: 29S   0  -0.24  +0.29% [-0.64, +0.81]           0.56
   4 ZDGE     amc          10 short   54  opus5:  7S  opus55:  0-  sonnet55: 60L  fable51: 92S*  1  -0.07  +0.29% [-0.69, +0.80]           0.56
   5 CNC      bmo           1 short   43  opus5: 53L  opus55: 61S  sonnet55: 21L  fable51: 18S   0  -0.02  +0.29% [-0.76, +0.78]           0.56
```

The E[return] column is gross, on the scorebord's window, and is the same for every name at a given percentile. It sits flat at about +0.3% below a percentile of 50. It is a translation of the percentile, not a separate forecast, and its out-of-sample record is weak.

The searchers' own `impact_sum` values were CLS +1.20, CNC +0.30, SOFI +0.30, ZDGE 0.00 and BLX −0.20. None of them clears the 2.8 floor.

## Selected: CLS (long, panel_pct 91, 4 of 4 in their own top 20%)

**For:** the Q3 results come with the 2026 Investor and Analyst Day at the 2026-10-27 08:00 ET call, so multi-year targets land inside the window. Celestica has a record of beating the top of its own guide. The stock fell 24% over 20 days in a sector-wide AI sell-off with no company-specific news.

**Against:**
- Consensus EPS may not include the dilution from the August equity raise.
- Jabil beat and raised and still fell.
- The +8 put skew shows the options market paying for downside.
- The name sold off after earlier beat-and-raise prints.

## Disagreements

- **ZDGE:** the judges split widely (sd 54). Fable 5.1 puts it strongly short (92S), while Sonnet 5.5 leans long (60L).
- **CNC:** the judges split across sides (sd 43). The searcher sized it at a mild +0.3.
- **SOFI:** the searcher's findings sum to +0.3 while all four judges lean short. The scaled number agrees with the judges at −0.36.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
