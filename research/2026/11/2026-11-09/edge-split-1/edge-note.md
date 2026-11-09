# Stage E-PS — shard 1 of 4 — 2026-11-09

Stage E-PS, shard 1 of four, run beside stage E-P with Opus 5.5 `unpriced-searcher`s and a blind four-model panel, on E-P's own names, sweep rows and sealed baselines (source commit 856d4f8). It places no orders.

- Names: ASTS, ACHR, SKYD, OXY (amc 2026-11-09), LEGN (bmo 2026-11-10). Five searchers in one message, all returned `search_complete: true`, and none ran out of search budget. For OXY, one third-party site (stocktaper) returned an HTTP 429 and the searcher recovered the same content from OXY's own slides.
- Baseline defects: OXY's sealed baseline is `bars_failed: HTTPError` (no spot, run-up or reaction history), so the searcher used third-party price data. SKYD's sealed event-implied move of 0.99% is distorted by the 2026-10-14 warrant ex-date. ASTS and LEGN carry `cadence_implausible`.
- Guard (`intraday.py guard`, run at 18:25 UTC): moved nothing.
- Judges: all four ran on their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1). Scored `--dry-run --stage E-PS`; the panel history was not written.
- Claim to done: 18:11 to about 18:31 UTC, about 20 minutes.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ASTS     amc     yes  88 short    8  opus5: 90S* opus55: 75S  sonnet55: 91S* fable51: 95S*  3  -1.68  +3.77% [+1.66, +5.74]           0.67
   2 LEGN     bmo          63 short   15  opus5: 82S* opus55: 56S  sonnet55: 72S  fable51: 42S   1  -0.83  +1.01% [-0.04, +2.54]           0.56
   3 SKYD     amc          56 long     9  opus5: 54L  opus55: 56L  sonnet55: 70L  fable51: 45L   0  +0.71  +0.48% [-0.25, +1.97]           0.56
   4 ACHR     amc          21 short   36  opus5: 46S  opus55: 47S  sonnet55: 40L  fable51: 31S   0  -0.50  +0.29% [-0.59, +0.82]           0.56
   5 OXY      amc           6 long     2  opus5:  6L  opus55:  4L  sonnet55:  9L  fable51:  6L   0  +0.13  +0.29% [-0.71, +0.79]           0.56
```

One day is an anecdote; judge it only pooled against stage E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
