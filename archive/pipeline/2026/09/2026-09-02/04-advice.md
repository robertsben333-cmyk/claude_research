# Daily earnings advice — 2026-09-02

Window: after the US close on Wednesday 2 September 2026 through before the US open on Thursday 3
September 2026. 6 names deep-researched (stage 2); 2 panelled (stage 3, top 2 of 6 by panel_priority
per `panel.names=2`).

## The calls

```
AI — C3.ai, Inc.
CALL       Neutral / No Edge   score -10.0   P(down) 53.3%   certainty High
MOVE       unsigned band 5.7% – 21.8%   (event-implied ≈ ±13.2%, judged rich)
REASON     Panel genuinely aligned on a weak bearish tilt (continued revenue decline, KPI/PR cadence
           deteriorating) that is offset almost exactly by a mechanical squeeze setup (34.65% of float
           short, no preliminary-results warning this cycle) — the two forces cancel rather than one
           dominating.
CAVEAT     Reversal risk High (64/100): an in-line print with a reaffirmed FY27 guide could ignite a
           squeeze regardless of the fundamentals; a guide cut would confirm the bear case instead.
DOSSIER    03-panel/AI-dossier.md
```

```
SNOW — Snowflake Inc.
CALL       Neutral / No Edge   score -1.0   P(up) 50.4%   certainty High
MOVE       unsigned band 7.0% – 38.3%   (event-implied ≈ ±12.0%, judged cheap)
REASON     Panel splits roughly 4 mildly bullish / 3 mildly bearish and nets to essentially zero.
           Company-specific KPIs (RPO +38%, record NRR) are genuinely strong; the bearish lean comes
           from positioning and cross-asset read-through, not the business — five of seven personas
           independently called the implied move cheap, and this week's two nearest comps (MongoDB,
           Datadog) both beat-and-raised and still sold off 13-21%.
CAVEAT     Reversal risk Med (60/100) with a fat-tailed history (max realised move 36.48%); the "good
           number, bad reaction" comp precedent this week is the live risk to the bull case.
DOSSIER    03-panel/SNOW-dossier.md
```

Neither panelled name clears a directional bar today. Both calls are genuine, evidence-driven Neutrals
— high panel agreement (disparity 28.6 and 30.0, both "aligned") landing on a near-zero consensus, not
a conviction-gate override and not a hedge. See §4 in each dossier for the exact panel math.

## Ranked field

All 6 deep-researched names, by stage-2 `panel_priority` (0.45×|prelim direction| + 0.35×evidence
completeness + 0.20×change expectation):

| Ticker | Company | Priority | Implied move | Prelim direction (stage 2) | Evidence completeness | Panelled |
| --- | --- | --- | --- | --- | --- | --- |
| AI | C3.ai, Inc. | 55.0 | ±13.2%* | -22 | 82 | **Yes — Neutral / No Edge** |
| SNOW | Snowflake Inc. | 49.9 | ±12.0%* | -10 | 84 | **Yes — Neutral / No Edge** |
| VSXY | Victoria's Secret & Co. | 49.8 | ±14.5% | +12 | 84 | No |
| AVGO | Broadcom Inc. | 49.1 | ±8.4% | +6 | 84 | No |
| PVH | PVH Corp. | 47.75 | ±9.2% | -15 | 80 | No |
| NTAP | NetApp, Inc. | 47.6 | ±12.1% | -10 | 82 | No |

*AI and SNOW implied moves shown are the stage-3 refreshed values (stage 2 had 13.64% and 12.94%
respectively, sourced hours earlier). VSXY/AVGO/PVH/NTAP figures are stage-2 values, not refreshed —
they were not panelled and their preliminary direction scores are the stage-2 dossier's own read, not a
panel verdict; do not treat them as calibrated calls. Full dossiers for all 6 names are at
`02-dossiers/<TICKER>.md`.

## What would change these calls

- **AI:** a reaffirmed or raised FY27 $210-240M guide plus any credible pipeline/federal-bookings
  commentary → bullish (squeeze case). A cut to that range or free cash burn worse than Q4's -$54.8M →
  bearish (confirms deterioration).
- **SNOW:** a Q3 guide implying ~33%+ product-revenue growth with another FY27 raise materially above
  $5.84B, i.e. no deceleration to point at → bullish (squeeze through the 52-week high). A beat that
  still reads as deceleration from Q1's 34% → bearish, echoing this week's MongoDB/Datadog reactions.
- **Both:** neither call rests on a data gap that would resolve before the print — both are genuine
  splits in the evidence itself, not thin coverage waiting on one more source.

## Coverage and caveats

- Both panels ran full 7/7 seats. AI's forensics persona ran long (~5 minutes vs ~3 for its
  siblings) but returned a valid verdict before the panel was finalised — no seat was actually empty.
- **Data-quality note (SNOW):** the historical_moves_pct anchor handed to the SNOW panel was labelled
  "most recent last" but was actually ordered most-recent-first (the +36.48% figure is the 27 May 2026
  print, not the -14.7% one). Five of seven SNOW personas caught this independently via their own
  sourcing and explicitly said it did not affect their calls. `synthesize.py`'s aggregate statistics
  (mean/median/max) are order-independent, so the synthesis itself is unaffected — this is a labelling
  error in the anchor packet, not a numeric one, and it is corrected in `03-panel/SNOW.json`'s anchors.
- No budget degradation was needed: `panel.names=2` is already the current config value (itself a
  standing reduction from 3, applied 2026-08-13), and both panels completed at full 7-persona strength
  within budget.
- Both spot prices and implied moves were refreshed today ahead of the panel, per the skill's
  price-sensitive-anchor rule; both refreshed spot quotes came from WebSearch snippets rather than a
  direct feed (SNOW's in particular showed some intraday scatter across sources, $319-$328) — treat
  spot as approximate, not tick-precise.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by
market positioning, guidance, macro conditions, and management commentary rather than reported results
alone.
