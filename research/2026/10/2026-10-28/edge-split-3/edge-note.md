# Stage E-PS — shard 3 of 4 — 2026-10-28

This is stage E-PS, shard 3 of four. It ran beside stage E-P with Opus 5.5 `unpriced-searcher` agents and a blind four-model panel, on E-P's own names, sweep and sealed baselines (source commit 9f2b3de6). **It places no orders.**

- **Names:** CLPT, HDSN and HRTG (amc 2026-10-28); ESTA and XRX (bmo 2026-10-29). Five searchers ran in one message and all five returned. None reported its search budget running out.
- **Judges:** all four ran on their pinned agents, with no fallback and no retry: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). Each judge returned all five ids.
- **Guard:** `intraday.py guard` moved nothing. Every hunt was written before 16:00 ET.
- **Timing:** about 13 minutes from claim to scored panel (claimed 18:13 UTC, scored about 18:25 UTC). The shard was claimed about an hour after the scheduled 17:07 to 17:10 UTC fire.
- **Scoring:** `panel_score.py --run <SHARD> --dry-run --stage E-PS`, so stage E-P's panel history was not written.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.20|, sonnet55 |1.20|, fable51 |1.44|  (live sizes before 2026-10-28, opus5 n=200 live, opus55 n=200 live, sonnet55 n=200 live, fable51 n=200 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 HRTG     amc     yes 100 long     0  opus5:100L* opus55:100L* sonnet55:100L* fable51:100L*  4  +4.65  +5.11% [+3.31, +6.73]           0.73
   2 CLPT     amc     yes  97 short    2  opus5:100S* opus55: 94S* sonnet55: 96S* fable51: 97S*  4  -2.21  +4.89% [+2.98, +6.59]           0.72
   3 HDSN     amc          52 short   38  opus5: 80S* opus55: 58S  sonnet55: 79S  fable51: 12L   0  -0.80  +0.32% [-0.38, +1.58]           0.56
   4 ESTA     bmo          39 long    42  opus5: 30S  opus55: 69L  sonnet55: 42L  fable51: 76L   0  +0.57  +0.29% [-0.52, +0.91]           0.56
   5 XRX      bmo          10 short   48  opus5: 53L  opus55: 69S  sonnet55: 42S  fable51: 20L   0  -0.04  +0.29% [-0.69, +0.80]           0.56
```

The searchers' own `impact_sum`: HRTG +4.10 (the only one above the 2.8 floor), HDSN +1.20, ESTA +1.00, XRX −0.20, CLPT −0.30.

Nothing checked the findings for factual errors. These are five names on one day: an anecdote, to be judged only pooled against stage E-P.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
