# Edge hunt — 2026-09-30 amc + 2026-10-01 bmo

**Answer first: nothing clears the conviction floor today.** Six names, all six confirmed and rankable. The largest |impact_sum| is 1.30, well under the 3.0 floor, so the book rule selects no name. The whole ranked table spans 1.6 points of spot, which is less than the reproducibility gap between two hunters (median 2.40). Read the order below as a near-null day, not as six views.

Ranking key (`edge-scores.json` → `ranking_key`): **`impact_sum`**, signed, in points of spot.

| # | ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control (−run_up_20d) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BSET | amc 2026-09-30 | +3.00 | **+1.30** | +0.81 | – | yes, long; **thin** at $0.40m/day | +4.27 |
| 2 | MKC | bmo 2026-10-01 | +1.50 | **+0.80** | +0.35 | – | yes, long; $149.9m/day | +12.99 |
| 3 | PRGS | amc 2026-09-30 | +1.50 | **+0.30** | +0.16 | – | yes, long; $20.1m/day | +10.95 |
| 4 | AYI | bmo 2026-10-01 | −0.40 | **0.00** | 0.00 | – | yes; $96.4m/day | +5.15 |
| 4 | MU | amc 2026-09-30 | −1.50 | **0.00** | 0.00 | – | yes; $25.7bn/day | −14.77 |
| 6 | ACN | bmo 2026-10-01 | −0.70 | **−0.30** | −0.48 | – | yes, short; Alpaca lends it; $898m/day | +3.49 |

The pre-lessons and V2 columns are measured beside the key and are not traded. V2 is calibrated today on 181 shadow-ledger observations. The tradable column comes from `alpaca_trade.py assets`, with borrow checked live, because there is no `alpaca-plan.json`.

## What drives the top and bottom

- **BSET, +1.30.** The top finding is +1.0 on an IEEPA tariff refund that likely lands in the quarter ended in August and is not in the $0.13 EPS bar. The CEO said on the 2026-07-02 call that they had "seen some" refunds, with no amount given. An EDGAR full-text search finds nothing booked through the Q2 10-Q. Peers that booked refunds rose this summer: HOFT and FLXS. The amount is **unsourced**, an inferred $1.5–3.5m pretax. The second finding is +0.3 on backlog conversion. The price says: stock −4.3% over 20 days, no usable option chain, short interest 0.6%.
- **MKC, +0.80.** Management reaffirmed the FY26 outlook at Barclays on 2026-09-09, nine days after Q3 closed (https://www.investing.com/news/transcripts/mccormick-at-barclays-conference-unilever-deal-sets-global-flavor-push-93CH-4894111). That makes the guide-cut tail unlikely, and it is the tail the +6.75 put skew and the 7.4% implied move are paying for. UBS publicly expects a reaffirm too, which limits how unpriced this is.
- **ACN, −0.30.** Two findings. The first is −0.7: the Middle East backdrop worsened after the Q4 guide was set, when the ceasefire collapsed on 2026-07-08 (https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire), and that bears mostly on FY27. The second is +0.4: Q4 federal awards, including the $821m War Data Platform order (https://defensescoop.com/2026/07/09/war-data-platform-integration-accenture-task-order/), sit against a bookings bar that has only one source. The call skew is −12.9 vol points and the stock is up about 50% off its June low, so the price leans the other way.
- **MU and AYI, 0.00: honest zeros.** Both hunters dropped their only draft findings under LESSONS rule 5, which says macro-to-company transmission is a hypothesis. For MU that was a CQ4 DRAM slowdown against the FQ1 guide consensus; for AYI, input-cost squeeze and peer channel reads. MU's option market leans up (skew −12, run-up +14.8%).

## Names that could not be ranked

None. Two related facts:

- MKC.V was folded into MKC as a share class.
- The window's 22 `time-not-supplied` calendar rows were checked with `session_resolve.py` because the day was thin. Two were killed (HUBG and SA filed results recently), none was confirmed by an announcement, and 20 were not hunted. The measured phantom rate for such rows is 20/20 (09-17) and 8/8 (08-31).

## The critical read of the floor-clearers

There are none. On the nearest miss: BSET's size is 77% `one_off`, a tariff refund of unsourced amount. That is the line the market has repeatedly refused to re-rate on. It is also thin, and it sits in the same IEEPA-refund cluster that ranked four names together on 2026-09-10. **Not recommended.** It is under the floor, and even above it the row would carry that reservation.

## What the note must also say

- **Order versus sign.** Every name here is below the floor. Below it the sign has been a coin flip (53% over 38 events). Above it, the rank of conviction predicted sign-correctness at ρ=+0.514 on the fitted sample, and more like +0.36 under one hunter per name. So −0.30 on ACN is not a bearish view. `impact_sum` ranks the day and is not a forecast of the move.
- **Control.** −run_up_20d orders the day MKC, PRGS, AYI, BSET, ACN, MU. The hunt's order overlaps it heavily: MKC and PRGS high, MU and ACN low. The main difference is BSET at the top. The stage has not yet been shown to beat this free control, and over 105 pooled events the control itself returned −0.42% per trade.
- **Sign balance.** 3 hunts net positive, 1 net negative, 2 zero. The pre-lessons drafts were 3 positive and 3 negative. LESSONS pulled every name toward zero: the absolute sum fell from 8.6 to 2.7.
- **Nothing checked the findings.** There is no adversary pass and no second hunter. A factually wrong finding enters the key at full size.
- **Reproducibility.** When pairs were measured, two hunters on one name differed by a median 2.40 points, and 4 of 12 pairs had opposite signs. That is larger than today's entire range.
- **Baseline measured versus inferred.** 5 of 6 names have a live option chain; BSET's is unusable, so its lean and expected move are the historical fallback. PRGS's chain is thin (ATM spread 20% of mid). The sweep marked PRGS's baseline history untrustworthy. The hunter checked it: the 2026-07-22 row is the Domo-deal and Q3 pre-announcement 8-K, not a print.
- **Cost to trade.** Every name clears the $200k turnover floor. BSET is thin, so a headline return on it overstates what size could have got. It is moot today because nothing clears the floor.
- **Execution today.** No orders were placed or sold by this session. The permission classifier refused the broker call at step 0b, and with no floor-clearer there was no book to buy at step 7.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
