# Stage E-PS — shard 2 of 4 — 2026-10-26

**This is stage E-PS, shard 2 of four.** It ran beside stage E-P on E-P's own names, sweep rows and sealed baselines, with Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel. **It places no orders.**
- Judges: all four ran on their pinned agents and covered all 5 packs: Opus 5 (`claude-opus-5`), Opus 5.5 (`claude-opus-5-5`), Sonnet 5.5 (`claude-sonnet-5-5`) and Fable 5.1 (`claude-fable-5-1`). The panel was scored `--dry-run` against stage E-P's live history, so no history was written.
- Guard: `intraday.py guard` moved nothing.
- Search budget: no searcher reported its search budget running out.
- Timing: claimed 17:21 UTC, panel scored 17:36 UTC, so about 15 minutes from claim to done.
- Event dates: the sweep had left AMKR and PII unconfirmed. Each searcher settled its own name from the company's release: AMKR reports amc 2026-10-26 and PII reports bmo 2026-10-27.
- One day is an anecdote.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.08|, sonnet55 |1.08|, fable51 |1.36|  (live sizes before 2026-10-26, n=176 each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 GLXY     bmo     yes  80 long    19  opus5: 47L  opus55: 90L* sonnet55: 90L* fable51: 94L*  3  +1.68  +2.63% [+0.64, +4.57]           0.60
   2 PII      bmo          51 short    6  opus5: 53S  opus55: 44S  sonnet55: 48S  fable51: 59S   0  -0.61  +0.32% [-0.39, +1.56]           0.56
   3 SNDL     bmo          48 short   17  opus5: 74S  opus55: 27S  sonnet55: 48S  fable51: 43S   0  -0.53  +0.29% [-0.45, +1.31]           0.56
   4 WHR      amc          37 short   37  opus5: 58S  opus55: 79S  sonnet55: 21L  fable51: 34S   0  -0.62  +0.29% [-0.53, +0.90]           0.56
   5 AMKR     amc          30 long    71  opus5: 90L* opus55: 44L  sonnet55: 76L  fable51: 89S*  1  +0.74  +0.29% [-0.56, +0.85]           0.56
```

**How to read the expected return.** E[return] is the gross return that names at this percentile have earned, measured on the scorebord window. Below a percentile of 50 it is flat at about +0.3%. Its out-of-sample record is weak, so it is not a forecast to size on.

## Searcher `impact_sum` (edge_score.py)

| Ticker | `impact_sum` | Scaled |
| --- | ---: | ---: |
| GLXY | +1.60 | +1.32 |
| WHR | +0.90 | +0.54 |
| AMKR | +0.60 | −0.48 |
| PII | −0.50 | −0.64 |
| SNDL | −1.20 | −0.36 |

None of the five clears the 2.8 floor.

## Selected: GLXY (long, panel_pct 80, exactly at the cut)

**The case for.** Q3 crypto marks against a consensus that still models a loss: BTC rose about 43% and ETH about 57–71% over the quarter. Short interest is 17% of Class A shares at 6.7 days to cover. The Helios lease is running at guide.

**The case against.** Opus 5 sat at its own 47th percentile. It argued that marks on continuously quoted assets are priced in real time, so a stale loss consensus is analyst inattention rather than unpriced information. Two further risks:
- CoreWeave, the sole Helios tenant, is under credit stress.
- A revenue miss on lower exchange volumes would repeat the line that took the stock −13.9% last quarter.

## Widest disagreement: AMKR

The judges split on AMKR. Opus 5 put it in its own top 20% long, on ASE's Q3 beat against a put skew that already prices the iPhone cut. Fable 5.1 put it in its own top 20% short, on the iPhone-driven Q4 guide risk.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
