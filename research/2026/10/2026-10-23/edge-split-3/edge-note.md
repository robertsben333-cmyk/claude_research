# Stage E-PS: split panel, shard 3 of 4, for 2026-10-23 (prints on 2026-10-26)

This is stage E-PS, shard 3 of 4. It ran beside stage E-P with Opus 5.5 searchers and a blind four-model panel. It used E-P's own names, sweep and baselines (copied from e55276cd). **It places no orders.**

- **Names:** MMYT, CX and BOH. All three report bmo on 2026-10-26, so the window runs from the 10-23 close to the 10-26 close.
- **Judges:** all four ran on their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5) and fable51 (claude-fable-5-1). No fallbacks were needed.
- **Guard:** it moved nothing, since all three names are bmo.
- **Search budget:** no searcher reported running out.
- **Timing:** claim to done took about 21 minutes (17:11 to 17:33 UTC).

One day is an anecdote.

## Panel table (as `panel_score.py` printed it, `--dry-run --stage E-PS`)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |1.80|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.44|  (live sizes before 2026-10-23, n=164 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CX       bmo     yes  80 long     3  opus5: 83L* opus55: 82L* sonnet55: 75L  fable51: 80L   3  +1.24  +2.61% [+0.62, +4.55]           0.60
   2 MMYT     bmo          49 short   27  opus5: 13S  opus55: 60S  sonnet55: 85S* fable51: 39S   1  -0.62  +0.29% [-0.43, +1.41]           0.56
   3 BOH      bmo          48 long    17  opus5: 55L  opus55: 48L  sonnet55: 21L  fable51: 68L   0  +0.70  +0.29% [-0.45, +1.29]           0.56
```

The expected return is the translation of the percentile, not a separate forecast. It is gross, measured on the scorebord's window, and flat at about +0.3% below a percentile of 50.

**Searcher `impact_sum`:** CX +1.20, BOH +0.90, MMYT +0.50. None clears the 2.8 floor.

**CX is selected, and only just, at a panel_pct of exactly 80.** The main evidence is the 2H guide's MXN 18.25-18.50 FX assumption against a spot rate of about 17.1-17.8, while consensus sits at the guide floor. Mexican construction output also supports it. The strongest case against:
- Analysts can already model spot FX.
- The peso weakened again by late September.
- Brent was above $100.
- Cemex sold a Q2 beat-and-raise down 3.6%.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
