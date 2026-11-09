# Can 1-minute data tell when an earnings move is priced in?

*Pre-registered test, 2026-11-09. Pre-registration: `PREREG.md` (one amendment, made before any outcome was computed). Alpaca SIP 1-minute bars with volume, after-hours + pre-market + regular session, 2,556 US earnings events, reaction days 31 Aug to 6 Nov 2026. Gross, in % of the prior close.*

## Short answer

**No. Not with this approach, and not well enough to change an exit.** I built a "settled" detector: abnormal volume that has decayed to under 30% of its own peak. I also built a direction signal for whatever is not yet priced: the recent trend plus the price against the VWAP since the release. Neither did what a "priced in" model needs to do on the holdout days.

| Hypothesis | Holdout result (21 Oct to 6 Nov, 13 days) | Verdict |
| --- | --- | --- |
| H1: while volume is still elevated, the path predicts the rest of the move to 13:00 | ρ +0.037, p 0.008 (n 7,911 observations from about 1,100 events). The sign matches development (+0.007) | **Fails** the pre-set bar of \|ρ\| ≥ 0.05. Real but tiny, and p is flattered because one event appears at many checkpoints |
| H2: once volume has decayed, the rest is unpredictable | ρ +0.013, p 0.44. But the gap between active and settled is −0.02 to +0.05 (95% interval over days), so the two states are not different | **Not supported.** It is unpredictable everywhere, so "settled" adds nothing |
| H3: exit when settled, or when the signal turns against us (otherwise amc open, bmo 13:00) | Market-wide +0.01 pp a position (n 1,105 events, t over days 0.57) | **Fails** |
| H3 on our calls | E-P v2 +0.37 (n 134, t 1.26, p 0.21); v3 −0.28 (n 120, t −1.04). Strong only: v2 +0.94 (n 33, p 0.27), v3 −0.52 (n 22, p 0.44) | The two versions point in opposite directions, and both samples are too small to tell |

The result does not depend on the threshold: at 0.2 and at 0.5 the market-wide gain is +0.02 and +0.01 (t over days 0.04 and −0.24).

## What was new compared with earlier work

Earlier threads tested one feature at one fixed moment: the first minute, the pre-market at 09:30, the first hour at 10:30, and the 10-factor model. This test used the **full path from the release onward**: after-hours from 16:00 for amc, the pre-market, then the regular session, all with real volume. It also tried to detect a **state** ("the reaction has stopped") rather than read a fixed clock time. It still finds nothing. The data adds no clock-independent signal that the earlier tests had missed.

## How long the move takes to arrive (descriptive)

This is the share of the reaction-day close-to-close move that is already in the price, for events with a close move of at least 4%. The figure is the median, with the interquartile range in brackets.

| amc | 16:30 the evening before | 09:25 | 09:35 | 10:00 | 11:00 | 13:00 | 15:30 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| share | 0.48 [0.05, 0.81] | 0.62 [0.30, 0.95] | 0.70 | 0.78 [0.54, 0.99] | 0.87 | 0.94 [0.79, 1.07] | 0.98 |

| bmo | 07:00 | 09:25 | 09:35 | 10:00 | 11:00 | 13:00 | 15:30 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| share | 0.34 | 0.60 | 0.66 | 0.72 [0.47, 0.94] | 0.84 | 0.90 [0.75, 1.08] | 0.98 |

The typical move is "priced" by late morning. But the range across events is wide at every moment, and the 1-minute path cannot tell in advance which events will still move. Caveat: this table selects on the final move, so it overstates how steady the build-up looks.

## One thing worth knowing

Direction drifted with the season. In development (Aug to mid-Oct, mostly small caps), moves tended to fade toward 13:00 (mean −0.47 when settled). In the holdout (mostly large caps), they kept going (+0.33, t over days 1.6). Any rule tuned on one period would have been wrong in the other. That is the same pattern earlier exit tests in this project hit.

## What I would do

Keep the static exits (amc at the open, bmo at 13:00). I would stop looking for exit timing in the 1-minute price and volume path. Five studies now point the same way, and this one covered the full extended-hours path with real volume. If the question comes back, the remaining untested inputs are not in the tape: the opening auction imbalance (paid data), options flow, and the content of the release itself against what was priced.

## Caveats

- Alpaca SIP prices, not our fills. The spread is not counted.
- Observations within an event are correlated. Per-day t and the day bootstrap are the honest measures, and both are given.
- The holdout was touched by earlier studies with other features. These features were never computed on it.
- 13 holdout days, all in one earnings season.

## Reproducing

`scripts/fetch.py ev.json cache` (event list from `exit-model/scripts/events.py`), `scripts/build.py ev.json cache rows.json`, `scripts/analyse.py rows.json [threshold]`. Outputs: `results.txt`, `results_0.2.txt`, `results_0.5.txt`.

*Research, not investment advice.*

---

# Version 2 (2026-11-09 evening): spreads and order flow from quotes and trades

*Pre-registration: `PREREG-v2.md`, written before any quote or trade was fetched. Alpaca SIP quotes and trades in 5-minute windows. One row per event per decision moment: amc at 09:25, bmo at 09:25 and bmo at 12:55. Market-wide rows need a move of at least 2% at the decision. Development: 289 rows (31 Aug to 20 Oct). Holdout: 1,348 rows (21 Oct to 6 Nov, 13 days). Output: `results2.txt`.*

## Short answer

**Still no.** The quotes and trades do not tell which way the rest of the move goes, and an exit rule built on them earns nothing. One measure says something about how much the price will still move, but not in the direction I wrote down in advance.

| Hypothesis | Holdout | Verdict |
| --- | --- | --- |
| HA: a wider spread than normal means more move to come | ρ −0.115, p 0.001 (n 978). **Opposite sign** to the prediction. Mostly bmo at 09:25 (−0.29) | **Fails as written.** The likely reason: pre-market spreads on a normal day are wide because hardly anyone trades. On an earnings morning, heavy trading narrows them, so a "narrow" spread just means a busy stock |
| HB: order imbalance (buyer- vs seller-initiated volume) predicts direction | ρ +0.006, p 0.84 (n 1,316). Development +0.071 | **Fails** |
| HB: retail imbalance (sub-penny off-exchange trades, Boehmer et al.) predicts direction | ρ +0.002, p 0.95 (n 1,052) | **Fails** |
| HC: exit rule on order imbalance | Market-wide: amc −0.11, bmo 09:25 +0.01, bmo 12:55 +0.02 (all \|t\| < 0.6). Calls: E-P v2 −0.17 (n 140, p 0.50), v3 −0.04 (n 129, p 0.91) | **Fails** |
| HC: exit rule on retail imbalance | amc −0.42 (n 192, t over days −2.9: it **costs** money); calls v2 −0.09, v3 +0.08 | **Fails** |

No cut by liquidity changes the direction result. Every |ρ| is at most 0.03 in both halves.

## The one lead, and it is about size

**Spread decay**, the spread at the decision divided by the spread earlier the same day, does predict how much the price still moves. That holds in development (ρ +0.12, n 265) and in the holdout (ρ +0.18, n 1,135), and still holds after allowing for the size of the move so far (partial ρ +0.13 and +0.19). Put simply: if the spread has not narrowed since the morning, more movement is coming. It is exploratory, because I pre-registered the abnormal-spread measure, not this one. And it says nothing about direction, so it cannot improve the exit on average. Its use would be risk: holding a smaller position, or exiting earlier, on names that have not settled. That is a sizing question, not a return question.

## What this adds to version 1

Version 1 used bars and volume. Version 2 used real quotes and trades, at the right moments, with one row per event. Both fail on direction, in the same way, on the same holdout. So within this data, "priced in" can be measured as "how much is still left to move", roughly. Which way that remainder goes cannot be predicted from the tape.

*Research, not investment advice.*
