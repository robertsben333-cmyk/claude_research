# Stage E-PI — intraday panel, snapshot 12:00 New York, 2026-10-14

**Stage E-PI**: this is stage E-P re-run from scratch at the 12:00 ET slot. It uses Opus 5.5 `unpriced-searcher` searchers and a blind four-model panel, and it **places no orders**. All four judges ran: `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5) and `panel-judge-fable51` (claude-fable-5-1). Each covered 7 of 7 packs, with no retries. The panel was scored with `--dry-run --stage E-PI`, so the panel history was not written. One day is an anecdote, and the snapshots of one day share names and a market, so they are not independent evidence.

**Coverage: 7 of 17 names, and why.** The snapshot fired at 15:58 UTC (11:58 ET) with the names frozen by the 10:00 snapshot, re-sealed all 17 baselines and hunted 7 of them (CMC, EDUC, EQBK, ERIC, HOMB, MAN, WIT) before its session stopped at a usage limit. A second session resumed at 18:20 UTC. On the operator's instruction the ten missing searchers were not completed, so every hunt in this snapshot was searched around the 12:00 slot and the snapshot stays comparable with the others. **Not ranked, no hunt:** TSM, SCHW, PLD, BNY, USB, PNC, MRSH, FHN, BSVN and CMTL. CMTL, the name both the 10:00 snapshot and stage E-P select, is therefore absent here; in the timeline `·` for these names means "not hunted", not a guard removal. The release guard ran at 18:22 UTC (14:22 ET) and moved nothing. No searcher's own `impact_sum` clears the 2.8 conviction floor (largest ERIC +1.10).

**Panel table, as `panel_score.py` printed it:**

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.10|, opus55 |1.10|, sonnet55 |1.20|, fable51 |1.50|  (live sizes before 2026-10-14, opus5 n=44 live, opus55 n=44 live, sonnet55 n=44 live, fable51 n=44 live)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ERIC     bmo          74 long     6  opus5: 75L  opus55: 64L  sonnet55: 75L  fable51: 82L*  2  +1.09  +1.90% [+0.33, +3.69]           0.56
   2 EDUC     amc          45 short   12  opus5: 36S  opus55: 57S  sonnet55: 57S  fable51: 32S   0  -0.58  +0.29% [-0.48, +1.13]           0.56
   3 HOMB     amc          31 long    21  opus5:  7L  opus55: 23L  sonnet55: 32L  fable51: 64L   0  +0.31  +0.29% [-0.56, +0.86]           0.56
   4 CMC      bmo          26 short   13  opus5: 36S  opus55: 41S  sonnet55: 11S  fable51: 16S   0  -0.33  +0.29% [-0.57, +0.84]           0.56
   5 WIT      bmo          26 short   16  opus5: 43S  opus55: 39S  sonnet55:  4S  fable51: 16S   0  -0.31  +0.29% [-0.57, +0.84]           0.56
   6 MAN      bmo          17 long    20  opus5: 14S  opus55: 36L  sonnet55: 14L  fable51: 32L   0  +0.27  +0.29% [-0.63, +0.82]           0.56
   7 EQBK     amc          14 short    2  opus5: 16S  opus55: 14S  sonnet55: 11S  fable51: 16S   0  -0.20  +0.29% [-0.66, +0.81]           0.56
E[return]: what a name at this panel_pct has earned on the panel's side (one number per percentile, scorebord window, gross); curve fitted 2026-10-14T08:30:16+00:00 on 148 resolved panel names.
```

**Selected: none.** The closest is **ERIC, long at 74** (spread 6, Fable 5.1 in its own top 20% at 82, Opus 5 and Sonnet 5.5 at 75). The judges point to the Infront consensus gross margin sitting about 110bp below the company's own guided Networks path, a SEK 5bn finished-goods build that points at Q3 deliveries, and ADR short interest at 10.2 days to cover. The case against is the component-cost line: DRAM and NAND contract prices rising into the new CEO's first Q4 margin guide, the item that took the stock down 12.6% last quarter. At 10:00 the panel had ERIC at 47 **short** and stage E-P's 13:06 run at 46 short, so this is the snapshot's one real side flip, on different searcher evidence of the same name.

**Where the panel and the searcher disagree most.** On WIT the searcher's key is −0.00 and the panel 26 short (Opus 5 −1.00 on a +7.2% five-day ADR run into a guide consensus already at −2% to 0% cc). On HOMB the searcher has +0.40 and the panel is spread (sd 21): Fable 5.1 long at 64, Opus 5 at 7. On MAN the panel is split again (Opus 5 short, the others long).

**Stage E comparison.** Stage E (13:04 ET) and stage E-P (13:06 ET) ran after this slot; their sizes are in the timeline's E-P column and in `edge/` and `edge-panel/`. On the 7 names here, stage E-P has MAN at 72 long against 17 long here, ERIC at 46 short against 74 long.

**What the numbers are not.** `expected_return_pct` is what names at that percentile have earned, not a forecast; below a percentile of 50 the curve is flat at about +0.3%. The weights are research, and nothing trades them. `p_up` is recorded but decides nothing. No adversary checked the findings for factual errors. Stage E-P's own V2 and context labels are not recomputed here.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
