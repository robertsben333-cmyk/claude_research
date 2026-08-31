# Edge hunt — 2026-08-31 amc + 2026-09-01 bmo

**One signed number per company, so the day can be ranked.** No call, no threshold, no
direction label. Sort on `edge_score` and the day is ordered.

Generated 2026-08-31, sealed baselines struck 14:05–14:12 UTC, ~30 minutes into the US
session so option chains were live and two-sided. 20 of 20 subagents spent.

## The ranking

Complete and unfiltered. `edge_score` is the ranking key on −100…+100; `edge_pct` is the
residual in points of spot. Selection is the reader's.

| # | Ticker | edge_score | edge_pct | confidence | uncert | baseline q | clusters | price lean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NIO | **+0.8** | +0.04 | 25.9 | 0.02 | 0.57 | 3 | +4.61% |
| 2 | HMR | **−0.8** | −0.04 | 14.4 | 0.02 | 0.24 | 3 | −1.22% |
| 3 | MDT | **−0.9** | −0.05 | 50.1 | 0.02 | 0.91 | 4 | +0.05% |
| 4 | MMED | **−1.0** | −0.05 | 8.2 | 0.34 | 0.19 | 7 | −0.23% |
| 5 | ZEPP | **−1.1** | −0.06 | 16.8 | 0.03 | 0.40 | 5 | −0.65% |
| 6 | CANG | **−4.9** | −0.24 | 14.4 | 0.12 | 0.24 | 4 | −2.19% |
| 7 | YEXT | **−5.1** | −0.26 | 15.2 | 0.13 | 0.40 | 4 | −1.00% |
| 8 | RZLV | **−11.5** | −0.58 | 5.0 | 0.99 | 0.07 | 4 | −0.52% |
| — | PXS | not ranked | | | | 0.24 | | no hunt (shed for budget) |
| — | RGS | not ranked | | | | 0.40 | | no hunt (date unconfirmed) |

**Read the spread before the order.** Eight names carry eight distinct scores, which is
the one thing the previous run failed to produce — it collapsed twelve names into a single
non-zero score and eleven zeros, and the bucketing did that rather than the evidence. But
the range here is `+0.04` to `−0.58` points of spot. After an adversary judged every
finding, almost nothing survived. Only two names clear a quarter-point of residual, and no
name reaches a full point, against implied moves of 4.6% (MDT), 9.8% (NIO) and 12.0%
(RZLV) where a chain exists at all.

That compression is a result, not a defect in the arithmetic. It also does not damage what
is under test: rank correlation reads **order**, not magnitude, so a tightly compressed but
strictly ordered table is exactly as falsifiable as a wide one. What it does mean is that
nobody should read `RZLV −11.5` as a forecast of a −11.5% move. It says RZLV sits last of
eight.

## Top of the ranking — NIO, +0.8

The only name with a positive score, and it is positive by a hair on one finding that the
adversary mostly dismantled.

**Driver** — NIO absorbed a RMB 10,000/vehicle purchase-tax subsidy on ES8 orders locked
through 2026-04-30 and withdrew it mid-Q2; Deutsche Bank named the withdrawal as a cause of
the June ES8 order shortfall, which reframes the 2.1% Q2 unit miss as partly the price paid
for margin rather than pure demand weakness.
<https://cnevpost.com/2026/07/02/analysts-why-nio-deliveries-missed-guidance/>

**What the price already says** — the chain leans *up*: a 25-delta skew of −9.44 vol points
on a 9.76% implied move gives a `priced_lean_pct` of **+4.61%**, the largest priced
directional statement of any name today, and NIO has the tightest chain in the window (ATM
spread 7% of mid). The finding agrees with that lean, so it takes the 0.55 agreement
discount — evidence that merely repeats what the price already says is not edge.

**The adversary broke it 78% priced, and its objection was timing.** The subsidy covered
orders locked through end-April/May, so most Q2 ES8 deliveries *carried* the cost; the June
withdrawal saves money on June-locked orders delivering largely in Q3. The RMB 180m is not
margin retained inside this print. It also caught that the RMB 180m coincidence is two
Deutsche Bank note vintages colliding — RMB 5m in the July note, RMB 180m in the August one.

## Bottom of the ranking — RZLV, −11.5

Largest residual in the window and simultaneously the **lowest confidence (5.0)** and
**highest hunter dispersion (0.99)** — the two isolated hunters landed −7.0 and −12.5
unweighted. Baseline quality is 0.07: no 25-delta skew, zero recoverable prior earnings
reactions, ATM spread 40% of mid. This is the least well-characterised name of the ten.

**Driver** — Reward Loyalty UK Limited (CH 10701520), bought for $239,557,869 cash on
2026-02-10 and sold to US investors as adding "approximately $90 million of EBITDA-accretive
revenue", filed audited group accounts at Companies House on 2026-07-25 showing turnover of
GBP 52.89m and gross profit around GBP 21m — a ~40%-margin business, not a 90%-margin
software asset. <https://uk.globaldatabase.com/company/reward-loyalty-uk-limited>

**What the price already says** — no skew and no reaction history, so `priced_lean_pct` falls
back to −0.05 × the 20-day run-up, giving a weak −0.52%. Worth stating plainly: on this name
the lean is *inferred from a run-up rather than measured from a chain*, and the 0.55
agreement discount still applied. That is the scorer working as specified, but it is much
weaker evidence of what is priced than the rule assumes.

**The adversary let this one through at 30% priced** — the strongest survival of any RZLV
finding — while noting the gap was checkable before the deal from the prior-year accounts,
and that Fuzzy Panda's 2025-09-29 report already alleged this exact strategy.

## The single most interesting finding, and whether it broke

**CANG's disclosure blackout survived best of anything today: 40% priced, the lowest figure
in the run.** Cango has published no monthly operational/bitcoin-production update since
2026-06-10 (May data) — an 82-day gap against a monthly cadence held since mid-2025, while
peer Canaan kept publishing. The last public data point is 31.67 EH/s and a 1,065.11 BTC
treasury as of 2026-05-31. <http://www.cangoonline.com/newsroom/corporate-news>

The structural argument is what makes it good: a miner going silent on the metric its equity
story rests on, in the exact months its own disclosed cash cost ($68,061/coin, April) sat
above spot BTC, is not usually withholding good news.

**The adversary did not break it, but it refused the sign.** Its exact words: *"I concede the
pattern-level observation is unpublished; I do not concede it carries a sign."* It supplied
innocent explanations that are themselves published — the EGM, the two consolidation
releases, and management's own Q1 statement that it is "not setting a hard hashrate target"
and managing to margin rather than scale, i.e. the company had already said it was
de-emphasising the metric. It also noted the release format had mutated three times through
2026, which reads as a company reshaping disclosure rather than going dark.

And it raised what none of the five CANG findings addressed: the +43.7% 20-day run-up is
almost fully explained by BTC going ~$63k → ~$79k in the same window. A ~$96m equity with no
options market whose marginal holder trades BTC beta may simply not reprice on a June quarter
marked to a $58.5k quarter-end.

## What the adversary pass changed

**51 of 51 findings judged. Zero unjudged.** This matters mechanically: an unjudged finding
defaults to mostly-priced, so on the previous run — where adversaries were pointed only at
the bullish findings — the default silently favoured whichever side went unattacked. Every
finding on both sides was judged this time.

The pass was not a rubber stamp. It found six substantive errors in the hunters' work:

| Ticker | What the adversary established |
| --- | --- |
| NIO | "Consecutive guidance misses" is **one miss counted twice** — April 29,356 + May 37,705 = 67,061; the Q2 guide less that *is* the claimed "June guide" of 42,900–47,900. NIO never issued one. |
| RZLV | The Google finding is **self-defeating** — Rezolve *acquired* Subsquid on 2025-10-09, so Google's docs naming Subsquid supports the release. The same hunter used SQD as evidence against Rezolve in one finding and as Rezolve's own impaired asset in another. |
| ZEPP | **Quarter mismatch** — the +35–40% DRAM figure is a 3Q26 contract price and cannot sit in an Apr–Jun COGS; the Q2-relevant number is +55–60%. And management disclosed the memory risk on the day the stock fell 28.6%. |
| MMED | The short-interest hook's **premise is false** — StockAnalysis prints "Short % of Float 21.09%" and Finviz 22.59%; MarketBeat, the hunter's own source, is the outlier dividing by shares outstanding. |
| HMR | The float finding, if acted on, **corrects the price the wrong way** — both major screeners already publish a float *smaller* than the prospectus figure treated as hidden. And the Q-Shipping "fleet-flat" claim is a category error: those nine vessels are technical, not commercial, management. |
| MDT | The consensus input is **cherry-picked low** — $9.47bn is the Zacks panel; the figure in today's preview is $9.55bn, inside the hunter's own guidance-implied range. |

The MMED two-hunter split was resolved cleanly in h2's favour: a lock-up expiry is a supply
event when the unlocked holder wants cash, and Medtronic cannot take cash without breaking
§355. Its FY27 guidance still assumes twelve months of Diabetes consolidation.

One validation worth recording: **MDT has the highest confidence in the table (50.1) and an
edge of −0.9.** The most efficiently priced name in the window — $117bn cap, 22,901 contracts
open interest, ATM spread 15% of mid, a flat −0.21 skew — produced near-zero edge at high
confidence. Knowing confidently that there is nothing there is the correct output for that
name, and the machinery delivered it.

## Names that could not be ranked

- **RGS (Regis)** — the only row of ten the sweep could not confirm. A real fiscal-Q4/FY2026
  print is genuinely due, but Regis has filed no 8-K since 2026-05-13 and lists no upcoming
  event; 2026-09-01 is a vendor projection, and the equivalent FY2025 release fell 2025-09-03.
  Shed rather than spend an Opus/high hunter on a print that may not be scheduled.
- **PXS (Pyxis Tankers)** — confirmed for tonight, but shed for budget. Lowest confirmed
  `hunt_priority` (47), and a 2.33% median / 4.87% maximum historical reaction leaves a
  genuine finding almost nowhere to express itself.

Both sit out of the ranking carrying `rankable: false` rather than sorting to the top on a
0.0. Neither is a failure; both are recorded budget decisions.

## Caveats that bound everything above

**One day is an anecdote.** Eight rankable names cannot produce a meaningful rank
correlation, and nothing here should be read as evidence the method works. The pooled figure
across many days is the result. Falsify with:

```bash
python3 scripts/edge_resolve.py --run research/2026/08/2026-08-31/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'    # the real number
```

The **normalised** correlation is the skill measure — sorting a 12%-implied de-SPAC above a
4.6%-implied medtech is easy and means nothing.

**Six of eight hunts leaned negative before the adversary, and all eight are ≤ +0.8 after
it.** A day of illiquid small caps into a print, with hunters told to find what the market
has missed, has an obvious bias toward finding problems. I flag this as a likely artefact of
the instruction rather than a fact about the day. If it recurs across many days, the hunter
prompt is generating pessimism, not detecting it.

**Coverage tracks market cap.** `backtest/FINDINGS.md` §27 measured news coverage as a
near-monotonic function of size. Seven of ten names here have no listed options at all, so
for those the "baseline" is a historical median rather than a priced expectation, and
`priced_lean_pct` falls back to a run-up heuristic. Only MDT, NIO and RZLV had a real chain.

**Session note.** CANG's session was unestablished at the start and is now resolved: a
9:00 p.m. ET call means the release is post-close tonight, with the reaction in the
2026-09-01 session. Verified not out as of ~16:30 UTC. YEXT and HMR are both company-confirmed
BMO despite nearly all prior prints being AMC, so their baseline reaction histories measure a
different release convention.

**Two process defects found and recorded.** An earlier edge hunt today had written to this
same directory over a *different* window under the old categorical contract; left in place its
twelve names would have entered this ranking as zeros, sorting above every negative name. It
is archived intact at `edge/_run1-bmo/`. And the `priced-in-adversary` agent definition grants
no `Write` tool, so none of the six adversaries could write its own output file — each returned
JSON in-message, transcribed here verbatim and marked with `_persisted_by`. That is a fix for
the agent definition, not a workaround to keep repeating.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
