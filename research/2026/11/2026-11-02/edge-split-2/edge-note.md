# Stage E-PS: shard 2 of 4, 2026-11-02

This is stage E-PS, shard 2 of four. It ran beside stage E-P on E-P's own names, sweep and sealed baselines, with Opus 5.5 searchers and a blind four-model panel. It places no orders.

- **Names:** ICHR, MTCH, ROKU and EBS report after the close on 2026-11-02; CHGG reports before the open on 2026-11-03. All five searchers ran in one message.
- **Judges:** all four ran with their pinned agents, with no fallbacks. They were panel-judge-opus5 (claude-opus-5), panel-judge-opus55 (claude-opus-5-5), panel-judge-sonnet55 (claude-sonnet-5-5) and panel-judge-fable51 (claude-fable-5-1). Each covered 5 of 5 names.
- **Guard:** moved nothing, since every hunt was written before 16:00 ET.
- **Search budget:** no searcher reported its search budget running out. Some sites refused fetches on their own side (403s and 429s).
- **Event check:** the sweep had left EBS unconfirmed. The searcher confirmed the date as 2026-11-02 after the close, from the company's 2026-10-15 call notice.
- **Time:** 20 minutes from claim to done (18:10 to about 18:31 UTC).

## Panel (as panel_score.py printed it, --dry-run --stage E-PS)

```
members opus5, opus55, sonnet55, fable51; selection panel_pct >= 80, all 4 members present; 0 sizes added to the history
own top 20% starts at: opus5 |2.00|, opus55 |1.44|, sonnet55 |1.30|, fable51 |1.54|  (live sizes before 2026-11-02, n=200 live each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score  E[return] at this pct (80% band)  P(right)
   1 ICHR     amc     yes  95 long     3  opus5: 98L* opus55: 93L* sonnet55: 91L* fable51: 99L*  4  +2.16  +4.76% [+2.78, +6.51]           0.72
   2 CHGG     bmo     yes  89 short    5  opus5: 86S* opus55: 82S* sonnet55: 93S* fable51: 96S*  4  -1.64  +3.98% [+1.88, +5.94]           0.68
   3 EBS      amc          76 long    14  opus5: 86L* opus55: 57L  sonnet55: 68L  fable51: 92L*  2  +1.08  +2.07% [+0.40, +3.90]           0.57
   4 MTCH     amc          21 short   21  opus5: 39S  opus55: 12S  sonnet55: 10L  fable51: 43S   0  -0.32  +0.29% [-0.59, +0.82]           0.56
   5 ROKU     amc           0 long     1  opus5:  0-  opus55:  2L  sonnet55:  0-  fable51:  0-   0  +0.00  +0.29% [-0.76, +0.78]           0.56
```

The panel selects two names: ICHR long and CHGG short. The searcher's own impact_sum was ICHR +1.50, EBS +0.90, ROKU +0.10, MTCH -0.50 and CHGG -1.00, so no name cleared the 2.8 floor. ROKU is a pinned merger-arb: Fox is acquiring it, and Roku gives no call and no outlook.

One day is an anecdote; judge this stage only pooled against stage E-P.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
