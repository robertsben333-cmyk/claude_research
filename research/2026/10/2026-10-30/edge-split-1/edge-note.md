# Stage E-PS — shard 1 of 4 — 2026-10-30 (prints 2026-11-02 bmo)

This is stage E-PS, shard 1 of four. It ran beside stage E-P with Opus 5.5 `unpriced-searcher` agents and a blind four-model panel, on E-P's own names, sweep rows and sealed baselines (copied from main at 05d32b44). It placed no orders. The panel was scored `--dry-run --stage E-PS` against stage E-P's live history, so nothing was added to `panel-history.json`.

- **Names:** AXSM, TATT, CIFR, CHH, CNA. All five report before the open on 2026-11-02. The sweep left CIFR unconfirmed; its searcher confirmed it from the company's own release.
- **Searchers:** 5 of 5 returned with `search_complete: true`. None reported running out of search budget.
- **Judges:** all four ran on their pinned models (opus5 `claude-opus-5`, opus55 `claude-opus-5-5`, sonnet55 `claude-sonnet-5-5`, fable51 `claude-fable-5-1`), with full coverage of 5 of 5 packs each.
- **Guard:** moved nothing.
- **Timing:** claimed at 18:10 UTC, panel scored at 18:25 UTC, about 16 minutes from claim to done.
- **Selection:** none of the five reaches panel_pct ≥ 80. CIFR is highest at 74 (long), with 3 of 4 judges in their own top 20%, so it is selected under the old 3-of-4 rule but not under the live mean-percentile rule.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CIFR     bmo          74 long    22  opus5: 36L  opus55: 82L* sonnet55: 82L* fable51: 95L*  3  +1.23  +1.90% [+0.33, +3.69]           0.56
   2 AXSM     bmo          58 long     9  opus5: 74L  opus55: 52L  sonnet55: 55L  fable51: 52L   0  +0.63  +0.69% [-0.17, +2.16]           0.56
   3 TATT     bmo          53 short   19  opus5: 78S  opus55: 63S  sonnet55: 28S  fable51: 43S   0  -0.63  +0.35% [-0.34, +1.71]           0.56
   4 CNA      bmo          27 long    15  opus5: 52L  opus55: 17L  sonnet55: 20L  fable51: 20L   0  +0.28  +0.29% [-0.57, +0.84]           0.56
   5 CHH      bmo           3 long    39  opus5: 54S  opus55: 17L  sonnet55: 55L  fable51:  8S   0  +0.01  +0.29% [-0.75, +0.78]           0.56
```

One day is an anecdote; judge this stage only pooled against E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
