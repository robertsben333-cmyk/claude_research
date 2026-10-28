# Stage E-PS — shard 4 of 4 — 2026-10-28

Stage E-PS, shard 4 of four, run beside stage E-P with Opus 5.5 `unpriced-searcher`s and a blind four-model panel on E-P's own names, sweep and baselines (source commit 9f2b3de6). **No orders.**

- Names: VNDA, AWRE, CYH (amc 2026-10-28); FVRR, BAND (bmo 2026-10-29).
- Fired late: claim at ~18:11 UTC (14:11 ET), not 17:07–17:10 UTC.
- Judges: all four ran on their pinned agents (opus5 claude-opus-5, opus55 claude-opus-5-5, sonnet55 claude-sonnet-5-5, fable51 claude-fable-5-1). Scored `--dry-run --stage E-PS`; panel history untouched.
- Guard (`intraday.py guard`): moved nothing; all amc hunts were written before 16:00 ET.
- Search budget: no searcher reported it running out. Several hit 403/503 on IR, Nasdaq and Benzinga pages and fell back to snippets.
- FVRR baseline carried `cadence_implausible`; its searcher rebuilt the base rate from confirmed prints only.
- Claim-to-done: about 16 minutes (18:11 to ~18:27 UTC).

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 BAND     bmo     yes  98 long     2  opus5:100L* opus55: 98L* sonnet55: 96L* fable51:100L*  4  +2.79  +4.98% [+3.11, +6.65]           0.73
   2 VNDA     amc     yes  91 short    5  opus5: 92S* opus55: 84S* sonnet55: 92S* fable51: 97S*  4  -1.68  +4.24% [+2.17, +6.15]           0.69
   3 CYH      amc     yes  91 short    5  opus5: 87S* opus55: 94S* sonnet55: 86S* fable51: 98S*  4  -1.56  +4.23% [+2.15, +6.14]           0.69
   4 AWRE     amc          78 short   12  opus5: 86S* opus55: 58S  sonnet55: 80S  fable51: 88S*  2  -1.18  +2.38% [+0.53, +4.28]           0.59
   5 FVRR     bmo          13 short   48  opus5: 38L  opus55: 26S  sonnet55: 22L  fable51: 84S*  1  -0.00  +0.29% [-0.67, +0.81]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

One day is an anecdote; the comparison with stage E-P is judged pooled over days.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
