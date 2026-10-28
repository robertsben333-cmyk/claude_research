# Stage E-PS — shard 1 of 4 — 2026-10-28

This is stage E-PS, shard 1 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines (source commit `9f2b3de`), with Opus 5.5 searchers (`unpriced-searcher`, the agent itself, not the fallback) and a blind four-model panel. It places no orders.

- **Names:** MVIS, TDOC and VKTX report after today's close; LENZ and NVCR report before the open on 10-29.
- **Judges:** all four ran on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5 (`claude-opus-5-5`), Sonnet 5.5 (`claude-sonnet-5-5`) and Fable 5.1 (`claude-fable-5-1`). Every judge covered 5 of 5 packs.
- **Guard:** moved nothing.
- **Search budget:** no searcher reported running out.
- **Timing:** claimed about 18:12 UTC, panel scored 18:22 UTC. Claim to done was about 12 minutes.
- **Scoring:** `panel_score.py --dry-run --stage E-PS` read each judge against stage E-P's live range and wrote nothing to the panel history.

One day is an anecdote.

## Panel table (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.20|, sonnet55 |1.20|, fable51 |1.44|  (live sizes before 2026-10-28, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 NVCR     bmo     yes  98 long     1  opus5:100L* opus55: 97L* sonnet55:100L* fable51: 98L*  4  +2.76  +5.00% [+3.14, +6.66]           0.73
   2 MVIS     amc     yes  90 short    4  opus5: 84S* opus55: 91S* sonnet55: 94S* fable51: 92S*  4  -1.60  +4.15% [+2.06, +6.08]           0.69
   3 TDOC     amc          44 short    9  opus5: 58S  opus55: 38S  sonnet55: 42S  fable51: 37S   0  -0.40  +0.29% [-0.49, +1.06]           0.56
   4 LENZ     bmo          14 short   60  opus5: 53L  opus55: 72S  sonnet55: 74S  fable51: 37L   0  -0.20  +0.29% [-0.66, +0.81]           0.56
   5 VKTX     amc          11 long     6  opus5:  6L  opus55:  9L  sonnet55: 22L  fable51:  6L   0  +0.13  +0.29% [-0.68, +0.80]           0.56
```

**What `E[return]` is.** It is gross return on the scorebord window: what names at that percentile have earned before. It is about +0.3% for any name below the 50th percentile. Its out-of-sample record is weak (correlation +0.12), so it is not a forecast to size on.

### Searcher sums (`impact_sum`, the comparison arm)

| Name | `impact_sum` |
| --- | --- |
| NVCR | +3.00 |
| LENZ | +1.40 |
| TDOC | +0.90 |
| VKTX | +0.40 |
| MVIS | +0.25 |

On MVIS the searcher's sum is positive while the panel goes short at 90; that is the widest gap between the two.

## Selected names

**NVCR, long, 98.**
- **The case:** Q3 revenue looks likely to land above the roughly $183m consensus. Q2's base held $2.8m of one-offs, and Q3 rose 3–5% over Q2 in each of the last two years. The guide's arithmetic points to a raise, and Pax is ramping (418 prescriptions and 285 active patients in Q2; Japan approval on 1 Oct). Shorts built about 15% into the print and the skew pays for upside.
- **Against:** every positive is an inference, not a reported number. The implied beat is small (1–3%). Q2's margin was flattered by a tariff refund. The option spread is wide (59% of mid).

**MVIS, short, 90.**
- **The case:** the going-concern financing walk:
  - cash looks short of year-end needs;
  - $19.8m of scheduled note redemptions;
  - a $17.5m minimum-cash covenant;
  - $41.2m of share-sale (ATM) capacity left after the lock-up expired;
  - a revenue guide weighted to the second half.
- **Against:**
  - about 20% of shares are short (from a snippet only);
  - management reaffirmed the guide on 10-07, with Q3 already closed;
  - cost-cut and asset-sale details are due on the call.

## Data notes

- **TDOC:** the searcher labelled one rejected candidate (the Dimensional 13G) `contradicted_by_document`. Its own report says the item is only irrelevant. The file is left as written.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
