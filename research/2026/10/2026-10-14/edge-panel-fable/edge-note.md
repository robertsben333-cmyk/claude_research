# Stage E-PF — 2026-10-14 amc + 2026-10-15 bmo

**This is stage E-PF: Fable 5.1 searchers (`unpriced-searcher-fable`, claude-fable-5-1), the same blind four-model panel as stage E-P, no orders.** All four members ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) and judged 8 of 8 packs. The panel was scored `--dry-run --stage E-PF`: each judge is read against stage E-P's live range from runs before today, and the panel history was not written. **One day is an anecdote**, and the `fable51` judge here read evidence its own model family collected; recorded, not corrected.

**Run note: 8 of 17 names.** The Routine's own session sealed all 17 baselines and hunted 8 (CMC, CMTL, EDUC, EQBK, ERIC, HOMB, MAN, WIT) before it stopped at a usage limit. A second session resumed at 18:20 UTC and, on the operator's instruction, ran no further searchers, so the hunted set is exactly what the first session produced. **Not ranked, no hunt:** TSM, SCHW, PLD, BNY, USB, PNC, MRSH, FHN, BSVN. All four amc names are in; five of the 13 bmo names are missing.

**Headline: the panel selects one name, CMTL short** (`panel_pct` 94, all four in their own top 20%, spread 2), the same name and side as stage E-P (93). The Fable searcher's own key puts no name over the 2.8 floor (largest ERIC +0.90) and sizes CMTL at **0.00**.

## The panel table, as `panel_score.py` printed it

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.50|  (live sizes before 2026-10-14, opus5 n=44 live, opus55 n=44 live, sonnet55 n=44 live, fable51 n=44 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 CMTL     amc     yes  94 short    2  opus5: 96S* opus55: 98S* sonnet55: 91S* fable51: 93S*  4  -2.49  +4.65% [+2.66, +6.43]           0.71
   2 MAN      bmo          52 long    24  opus5: 54L  opus55: 64L  sonnet55: 14L  fable51: 77L   1  +0.77  +0.33% [-0.36, +1.64]           0.56
   3 WIT      bmo          51 long    18  opus5: 66L  opus55: 43L  sonnet55: 70L  fable51: 25L   0  +0.60  +0.31% [-0.39, +1.55]           0.56
   4 ERIC     bmo          41 long    39  opus5: 36L  opus55: 77L  sonnet55: 20S  fable51: 70L   0  +0.77  +0.29% [-0.51, +0.96]           0.56
   5 CMC      bmo          22 long    33  opus5: 32S  opus55: 36L  sonnet55: 57L  fable51: 25L   0  +0.34  +0.29% [-0.59, +0.83]           0.56
   6 HOMB     amc          21 long    10  opus5: 30L  opus55:  7L  sonnet55: 32L  fable51: 16L   0  +0.33  +0.29% [-0.59, +0.82]           0.56
   7 EDUC     amc          18 short    9  opus5: 14S  opus55: 16S  sonnet55: 32S  fable51:  9S   0  -0.16  +0.29% [-0.62, +0.82]           0.56
   8 EQBK     amc           8 short    9  opus5: 23S  opus55:  0-  sonnet55: 11S  fable51:  0-   0  -0.05  +0.29% [-0.70, +0.79]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

Expected return is gross, on the scorebord window, and is the translation of the percentile, flat at about +0.3% below 50. It is not a forecast to size on (out-of-sample correlation +0.12 over 148 names).

## Selected: CMTL, short (amc tonight)

The judges size the same two items as in stage E-P, now from Fable's evidence: a likely held-for-sale/discontinued-operations presentation at a year-end after a signed sale, which Opus 5 puts at continuing revenue near $56-61m against a consolidated bar of about $109m that every aggregator still carries, and Allerium's 0.32x book-to-bill with no award announced since March, on a $1.27 stock with an 18% median reaction that fell on six of its last seven prints. Sizes: Opus 5 −3.50, Opus 5.5 −2.88, Fable 5.1 −2.88. Against it: the on-time filing and the lender prepayments, and the searcher itself netted its findings to 0.00 with `impact_scaled` −1.60. No usable option chain, a ~$38m residual equity, retail tilt 80: the expected return is an upper bound on what size could have got.

## Where the panel and the searcher disagree most

- **CMTL**: searcher 0.00, panel 94 short.
- **MAN**: searcher −0.00, panel 52 long (spread 24; Sonnet 5.5 at 14 against Fable 5.1 at 77).
- **ERIC**: searcher +0.90, panel 41 long with the widest spread of the day (39): Opus 5.5 77L and Fable 5.1 70L against Sonnet 5.5 20S. Opus 5 netted a Q3 beat from the finished-goods build against a weak first Q4 margin guide.

## Against stage E and stage E-P

**Stage E-P** (`edge-panel/edge-scores-panel.json`) exists. On the 8 names both ranked: **the selected sets are identical (CMTL short in both)**; Spearman ρ between the two `panel_pct_signed` columns **+0.548** (n=8); between the two searchers' `impact_sum` only +0.22. Largest differences: WIT (E-PF 51 long, E-P 20 short), ERIC (41 long against 46 short), MAN (52 long against 72 long), EDUC (18 short against 44 short).

**Stage E** (`edge/edge-scores.json`): Spearman ρ stage E `impact_sum` vs this panel +0.275, vs this searcher −0.18 (n=8). The free control `−run_up_20d_pct` ranks at −0.24 against the panel.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct` on CMTL) is what names at that percentile have earned, not a forecast. The weights are research, nothing trades them. `p_up` is recorded and decides nothing. Below the floor the searcher's sign is a coin flip on the evidence so far; `impact_sum` ranks and does not size. Nothing checked the findings for factual error. Eight names, five of 13 bmo names missing, one day: compare this stage with E-P only pooled.

## Context: retail, search and volatility (not used for selection)

Written to `edge-context.json`; see `score_report.py` below. Context only.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
