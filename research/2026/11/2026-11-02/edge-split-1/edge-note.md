# Stage E-PS — shard 1 of 4 — 2026-11-02

This is stage E-PS, shard 1 of four, run beside stage E-P. It uses Opus 5.5 searchers and a blind four-model panel on E-P's own names, sweep and baselines (source commit 550315c5), and places no orders. One day is an anecdote.

- **Names:** AEHR, HNGE, AAPL and PLTR report amc on 2026-11-02. UPST reports bmo on 2026-11-03.
- **Searchers:** five `unpriced-searcher` agents, launched in one message at about 18:16 UTC. All five returned `search_complete: true` and none reported running out of search budget. stocktaper.com returned its own HTTP 429 to two of them; that was the site's limit, not ours.
- **PLTR:** stage E-P's sweep left it unconfirmed. The searcher confirmed it from Palantir's own Business Wire release of 2026-10-12: amc on 11-02.
- **Guard:** moved nothing.
- **Judges:** all four ran, each on its pinned model: `panel-judge-opus5` (claude-opus-5), `-opus55` (claude-opus-5-5), `-sonnet55` (claude-sonnet-5-5) and `-fable51` (claude-fable-5-1). Each judge covered all five packs, and no fallback was used.
- **Scoring:** `panel_score.py --dry-run --stage E-PS`. Nothing was written to the panel history.
- **Timing:** claimed at 18:13 UTC, panel scored at 18:31 UTC, so about 18 minutes from claim to done.

## Panel (as printed by panel_score.py)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-11-02, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 AEHR     amc     yes  99 long     1  opus5:100L* opus55: 98L* sonnet55:100L* fable51: 99L*  4  +3.74  +5.05% [+3.22, +6.69]           0.73
   2 PLTR     amc          80 long    11  opus5: 96L* opus55: 68L  sonnet55: 84L* fable51: 72L   2  +1.12  +2.59% [+0.61, +4.52]           0.60
   3 UPST     bmo          78 short   13  opus5: 56S  opus55: 88S* sonnet55: 88S* fable51: 80S*  3  -1.33  +2.37% [+0.52, +4.26]           0.59
   4 HNGE     amc          50 short   54  opus5: 86S* opus55: 76S  sonnet55: 44L  fable51: 80S*  2  -1.12  +0.29% [-0.43, +1.43]           0.56
   5 AAPL     amc          46 short   14  opus5: 65S  opus55: 33S  sonnet55: 56S  fable51: 32S   0  -0.48  +0.29% [-0.47, +1.20]           0.56
```

The `selected` column shows only AEHR. PLTR's mean percentile rounds to 80 but did not clear the cut.

## The searcher's own key

| ticker | impact_sum |
| --- | --- |
| AEHR | +5.00 (above the 2.8 floor) |
| PLTR | +0.90 |
| UPST | +0.25 |
| AAPL | −0.65 |
| HNGE | −1.30 |

UPST is the one name where the searcher's key and the panel take opposite sides.

## AEHR, the selected name

**Case for long:**
- Aehr's own releases add up to about $128.6M of orders: the $100.6M effective backlog in the 2026-07-14 8-K, a $22M AI wafer-level order in August and about $6M of Sonoma follow-on orders in October.
- That already covers the low end of the $130–150M FY27 revenue guide.
- 18% of the float is short, after a 49% 20-day slide that began with Teradyne's Titan HP launch.

**Strongest case against:**
- The +11.75 put skew already pays for downside.
- Teradyne describes hyperscaler programmes as back-half loaded into 2027.
- Oppenheimer's public rebuttal on 10-14 did not stop the slide.
- Q1 needs a steep sequential revenue ramp.

These numbers are not a forecast to size on. E[return] is what names at that percentile have earned, gross, and its out-of-sample record is weak.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
