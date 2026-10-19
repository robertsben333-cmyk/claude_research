# Stage E-P — 2026-10-16 amc + 2026-10-19 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.**
All four judges ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1); none missing, no fallback.
Three names on one day is an anecdote, not a result.

## The panel

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CLF | 2026-10-19 bmo | **yes** | 94 | long | 1.0 | 94L* | 96L* | 93L* | 94L* | 4 | +2.81 | +1.90 | +4.68% [+2.69, +6.45] | 0.71 | 1.0 | 1.0 |
| 2 | DX | 2026-10-19 bmo | no | 23 | short | 7.2 | 15S | 18S | 27S | 33S | 0 | −0.27 | −0.20 | +0.29% [−0.58, +0.83] | 0.56 | 0 | 0 |
| 3 | FITB | 2026-10-19 bmo | no | 15 | long | 11.6 | 4L | 4L | 30L | 23L | 0 | +0.23 | +0.60 | +0.29% [−0.65, +0.81] | 0.56 | 0 | 0 |

Percentiles are each judge's own, against its live range before today (n=73 each); `*` = in that judge's own top 20%.
Selection: all four present and panel_pct ≥ 80 (the 3-of-4 verdict agrees on every row).
The expected return translates the percentile: it is the same for every name at that percentile, gross, on the scorebord window.
It is flat at about +0.3% below a percentile of 50, and it is not a forecast to size on.

## CLF — selected, 4 of 4

All four judges rest on the same item. US hot-rolled coil spot ran from about $1,130 to $1,220/st after the July Q3 guide, which assumed only +$55/t (Nucor and Kallanish prices, cited in the hunt). Cliffs' contract and index book lags spot, so the **Q4 guide** can clear the roughly $725m implied Q4 consensus. The guide is the line this name has paid on: +15.98% on 2026-07-23, +21.5% last October, −16% on the Q4 2025 miss. Wells Fargo's 10-06 contract-reset note supports it. A 13.89%-of-float short (4.7 days to cover, MarketBeat settlement 09-30) and call-bid skew (−15.6 vol points) add the squeeze mechanism.

**The case against.**
- The thesis rests on a public weekly price series, which is a proxy and not a company number. The Wells Fargo note is wire copy.
- The Stelco/Ottawa dispute is live and two-sided. CLF fell 9% on 09-28 and 4% on 10-15 against 1–2% for peers.
- Q3 North American auto production is pacing −0.6% (Omdia), while about half of the guided +300kt shipment step-up was meant to come from auto.
- The option market already prices about 10.6% with calls bid, so part of the upside is held.
- The searcher's own sum, +1.90, is under the 2.8 floor; the panel is far more confident than its searcher.
- Flags: findings split 4 positive / 3 negative, and 3 findings worth −0.50 are dated after the exit and kept out of the key.

## Panel against searcher

- **CLF:** the searcher's +1.90 (p83 among Opus 5.5 sizes) sits below the floor, while the panel puts it at p94. The judges sized the same evidence +2.2 to +3.5.
- **FITB:** the searcher's +0.60 is its second-largest, but Opus 5 and Opus 5.5 put it at their own 4th percentile. The quarter was pre-announced at the upper end on 09-15, and the name sold a beat in July.
- **DX:** all five read it as a small short. Peer book-value pre-releases (ORC −16.6%, IVR −16.1%) imply DX's book is roughly priced at 0.97×.

## Against stage E

Stage E's `edge-scores.json` did not exist on `main` when this note was written, about 17:40 UTC. Stage E had published nothing for 2026-10-16, not even a STARTED heartbeat, so there is no overlap or ρ to report. Its Routine lives on another account, so whether it fired cannot be checked from here.

## The free control

`-run_up_20d_pct` ranks DX +10.43, FITB +4.87, CLF +2.68. That is the exact reverse of both the searcher's order and the panel's order. The control is not stable either (−0.42% per trade over 105 pooled events), but a note without it claims more than it should.

## Standing caveats

- **Sign balance:** 2 long-leaning, 1 short-leaning.
- **Option anchors:** 2 of 3 names have a live option chain (CLF 12.33%, FITB 7.0%). DX has none, so its lean is the run-up fallback.
- **Below the floor the searcher's sign is a coin flip.** No name clears 2.8 today. `impact_sum` ranks; it does not size.
- **Nothing checked the findings for factual error.** There is no adversary, and the key is not reproducible to better than its own size: double-hunt pairs had a median gap of 2.40 points, with 4 of 12 opposite in sign.
- **No tradable column.** It comes from `alpaca_trade.py assets`, and this stage runs no `alpaca_trade.py` command in any form. All three names are large or mid caps with deep turnover.
- **What the numbers are not.**
  - `expected_return_pct` is what names at that percentile have earned. Its out-of-sample record is weak: correlation +0.12 over 148 names.
  - The weights are research; nothing trades them.
  - `p_up` is recorded and decides nothing.
- **The same three names were judged twice today.** The 12:00 intraday snapshot selected CLF at 95L too. That snapshot and this run used separately sealed baselines, separate searchers and separate judges, but they share the evidence pool, so they are not independent confirmations.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks or selects on these.

- CLF: retail 68 (≥50 yes), search failed, vol 56.8 (≥58 no)
- FITB: retail 25 (no), search failed, vol 15.7 (no)
- DX: retail 57 (yes), search failed, vol 23.9 (no)

V2 grounded (written before the first print): CLF +3.39, FITB +0.22, DX −0.30.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
