# Stage E-PS, shard 4 of 4, for 2026-10-26

This is stage E-PS. It ran beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 `unpriced-searcher` agents and a blind four-model panel. It places no orders. One day is an anecdote.

- **Names:** AEYE (amc), AGYS (amc), CBC (bmo 10-27), KNSA (bmo 10-27), GLW (bmo 10-27). All five searchers returned. The searchers confirmed the three events the sweep had left unchecked: AGYS, KNSA and GLW.
- **Judges:** all four ran: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1). Each used its named agent, with no fallback.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`. The panel history was not written.
- **Guard:** moved nothing.
- **Search budget:** no searcher reported it running out. AEYE hit 403/503 on its transcript and aggregator pages.
- **Timing:** claimed 17:13 UTC, panel scored 17:34 UTC, so about 21 minutes from claim to done.

## Panel (as printed by panel_score.py)

```
own top 20% starts at: opus5 |1.80|, opus55 |1.08|, sonnet55 |1.08|, fable51 |1.36|  (live sizes before 2026-10-26, n=176 each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 KNSA     bmo     yes  99 long     0  opus5: 98L* opus55: 98L* sonnet55: 99L* fable51: 99L*  4  +3.01  +5.00% [+3.16, +6.66]           0.73
   2 AEYE     amc          77 long     6  opus5: 77L  opus55: 77L  sonnet55: 86L* fable51: 68L   1  +1.08  +2.23% [+0.46, +4.09]           0.58
   3 AGYS     amc          54 short   44  opus5: 82S* opus55: 84S* sonnet55: 21L  fable51: 73S   2  -1.13  +0.37% [-0.30, +1.83]           0.56
   4 GLW      bmo          18 long    36  opus5: 42S  opus55: 52L  sonnet55: 21L  fable51: 40L   0  +0.42  +0.29% [-0.62, +0.82]           0.56
   5 CBC      bmo          11 short    6  opus5:  7S  opus55: 11S  sonnet55: 21S  fable51:  5S   0  -0.16  +0.29% [-0.68, +0.80]           0.56
```

`E[return]` is gross, on the scorebord window. It translates the percentile into a return; it is not a separate forecast, and it is flat at about +0.3% below a percentile of 50. Its out-of-sample record is weak.

## KNSA (selected, long)

The case for the long:

- **Low revenue bar.** The $260.2M consensus (MarketBeat) implies a sequential ARCALYST add of +$16.6M. Every non-Q1 quarter since 2025 has added more, per the company's 8-K exhibits.
- **Likely guidance raise.** The FY guide of $980–995M implies a second half below the Q2 run-rate, and the company raised the guide at each of the last three prints.
- **Positioning.** Short interest is 10% of float, and the stock fell 9.9% in the five sessions before the print.

The strongest case against: Q3 2025 beat on revenue and raised guidance, but missed EPS and fell 2.9%. The revenue consensus also rests on one feed.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
