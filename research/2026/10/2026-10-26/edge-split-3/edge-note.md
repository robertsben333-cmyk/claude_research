# Stage E-PS — shard 3 of 4 — 2026-10-26

This is stage E-PS, shard 3 of four. It ran beside stage E-P on E-P's own names, sweep rows and sealed baselines (source commit `ec020c77`), with Opus 5.5 `unpriced-searcher`s and a blind four-model panel scored `--dry-run --stage E-PS` against stage E-P's live history. **No orders were placed.**

- **Names:** DQ (bmo 10-27), RMBS (amc 10-26), PSMT (amc 10-26), JBLU (bmo 10-27), CVLT (bmo 10-27). JBLU and CVLT were unconfirmed by E-P's sweep; their searchers confirmed both from company releases.
- **Searchers:** 5 of 5, all on the `unpriced-searcher` agent (not the fallback). None reported its search budget running out. 0 of 5 clear the 2.8 `impact_sum` floor.
- **Judges:** all four ran: opus5 (`claude-opus-5`), opus55 (`claude-opus-5-5`), sonnet55 (`claude-sonnet-5-5`), fable51 (`claude-fable-5-1`). Coverage was 5/5 each.
- **Guard:** it moved nothing.
- **Claim to done:** 17:21 to about 17:35 UTC, roughly 14 minutes.
- **Selected:** CVLT short (panel_pct 84) and DQ long (82).

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CVLT     bmo     yes  84 short    7  opus5: 77S  opus55: 81S* sonnet55: 80S* fable51: 96S*  4  -1.16  +3.12% [+1.05, +5.11]           0.63
   2 DQ       bmo     yes  82 long     7  opus5: 90L* opus55: 87L* sonnet55: 74L  fable51: 77L   2  +1.24  +2.92% [+0.88, +4.89]           0.62
   3 RMBS     amc          77 long    18  opus5: 76L  opus55: 94L* sonnet55: 48L  fable51: 92L*  2  +1.41  +2.30% [+0.49, +4.17]           0.58
   4 JBLU     bmo          37 long    68  opus5: 79L  opus55: 73L  sonnet55: 81S* fable51: 77L   1  +1.01  +0.29% [-0.53, +0.89]           0.56
   5 PSMT     amc          22 short    6  opus5: 32S  opus55: 18S  sonnet55: 21S  fable51: 18S   0  -0.32  +0.29% [-0.58, +0.83]           0.56
```

One day is an anecdote; judge this stage only pooled against stage E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
