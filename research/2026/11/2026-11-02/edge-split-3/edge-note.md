# Stage E-PS — shard 3 of 4 — 2026-11-02

Stage E-PS, shard 3 of four, run beside stage E-P with Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model panel on E-P's own names, sweep and baselines (E-P commit 550315c5). **No orders.**

- Names: LIFE, IBTA, HLF (amc 2026-11-02); VITL, DOCN (bmo 2026-11-03). All five searchers in one message; all returned `search_complete: true`. None reported its search budget running out (third-party sites only refused with 403/429/503).
- HLF: the sweep left it unconfirmed; its searcher confirmed 2026-11-02 amc from Herbalife's own release (https://ir.herbalife.com/news-events/press-releases/detail/958/herbalife-to-announce-third-quarter-2026-results-on).
- Judges: all four ran on their pinned agents: opus5 (claude-opus-5), opus55 (claude-opus-5-5), sonnet55 (claude-sonnet-5-5), fable51 (claude-fable-5-1). No fallback was used.
- Guard (`intraday.py guard`, 18:29 UTC = 13:29 ET): moved nothing.
- Claim 18:20 UTC (split.json) → done 18:33 UTC: 13 minutes. (The STARTED log line says 18:13; that was the time the claim call was sent, not the time it returned.)
- Scored `--dry-run --stage E-PS`, so 0 sizes were added to the panel history.

## Panel (as `panel_score.py` printed it)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-11-02, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 VITL     bmo     yes  94 short    1  opus5: 92S* opus55: 94S* sonnet55: 96S* fable51: 96S*  4  -2.10  +4.67% [+2.67, +6.44]           0.71
   2 DOCN     bmo     yes  90 long     2  opus5: 90L* opus55: 93L* sonnet55: 88L* fable51: 90L*  4  +1.66  +4.13% [+2.03, +6.07]           0.69
   3 IBTA     amc     yes  82 long    15  opus5: 88L* opus55: 90L* sonnet55: 95L* fable51: 56L   3  +1.58  +2.98% [+0.93, +4.95]           0.62
   4 LIFE     amc          72 long    42  opus5:  0S  opus55: 96L* sonnet55: 98L* fable51: 92L*  3  +2.08  +1.69% [+0.26, +3.42]           0.56
   5 HLF      amc          67 short    6  opus5: 74S  opus55: 61S  sonnet55: 72S  fable51: 62S   0  -0.84  +1.34% [+0.12, +2.98]           0.56
```

One day is an anecdote; this shard is judged only pooled against stage E-P over many days.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
