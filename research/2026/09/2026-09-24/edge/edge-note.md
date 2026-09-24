# Edge hunt — 2026-09-24 amc + 2026-09-25 bmo

**Answer first: this is a null day.** All 4 names in the window were confirmed and hunted. None clears the conviction floor of 3.0. Three hunts came back with no findings at all, and the fourth is +0.30. **No book is placed.** Ranking key (`edge-scores.json` → `ranking_key`): `impact_sum`, signed, in points of spot.

| # | ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control −run_up_20d |
|---|---|---|---|---|---|---|---|---|
| 1 | SCHL | amc 2026-09-24 | +1.50 | **+0.30** | +0.19 | – | yes · $12.9m/day · ok | +14.34 |
| 2 | COST | amc 2026-09-24 | +0.30 | **+0.00** | +0.00 | – | yes · $1,866m/day · ok | +6.48 |
| 3 | LGCY | amc 2026-09-24 | −1.00 | **+0.00** | +0.00 | – | yes · $0.38m/day · **thin** | −0.38 |
| 4 | TBN | bmo 2026-09-25 | +0.00 | **+0.00** | +0.00 | – | yes · $5.4m/day · ok | +4.53 |

The pre-lessons and V2 columns are measured next to the key. Neither is traded. V2 is calibrated today (175 ledger observations, session_close). Three names tie at 0.00, so today's order carries almost no information beyond SCHL being first.

**TBN session:** the company's calendar gives a US-morning 09-25 webcast. Aggregators and its own 8-K history point to a release on the evening of 09-24. Either way the reaction lands in the close(09-24) → close(09-25) window, so the session label does not change the measured move.

## What drives the top and bottom

- **SCHL +0.30 (top).** The only finding of the day. The FY26 10-K leaves about $6.2M of IEEPA tariff refunds unrecognised as a gain contingency. CBP's CAPE programme was paying out during Q1 (June–August), so some of that plausibly lands in adjusted Q1 results, at roughly +$0.10 to +$0.25 per share against a −$3.42 bar. Source: https://www.sec.gov/Archives/edgar/data/0000866729/000086672926000018/schl-20260531.htm. The hunter's own caveats:
  - It is a `one_off`.
  - The timing is inferred, not documented.
  - SCHL trades on the FY27 guide, not on EPS quality.

  What the price already says: the stock is −14.3% over 20 days, and short interest rose 37% into the print, to about 12.6–14% of float.
- **COST, LGCY, TBN (0.00).** Each hunter found nothing the price does not already hold:
  - **COST:** its fuel-margin lead was dropped, because Oppenheimer's preview already names "excess fuel profits". The IEEPA refund is already in the wire.
  - **LGCY:** its draft EPS-bar finding was the hunter's own margin model, and it landed inside consensus.
  - **TBN:** it is a pre-revenue developer, and every operating fact is already in a company release.

## Names that could not be ranked

None. The sweep confirmed all 4 from company sources and found 0 phantoms. The 22 `time-not-supplied` rows were checked with `session_resolve.py`:
- 4 were killed because they had already reported (HUBG, TRT, DAVA, ENLV).
- 0 were confirmed by an announcement.
- 18 were carried but not hunted.

## Floor-clearers: critical read

There are none, so there is nothing to recommend.

## Standing caveats

- **Order versus sign.** Below the floor the sign is a coin flip on the evidence so far (53% over 38 events). Above the floor, the rank of conviction predicted whether the sign was right at ρ=+0.514. SCHL's +0.30 is not a bullish view.
- **`impact_sum` is not a forecast of the move.** It ranks; it does not size.
- **Control.** `−run_up_20d_pct` orders the day SCHL > COST > TBN > LGCY. The hunt's order matches it only at the top, and with three ties it cannot be told apart from the control. The stage has not yet beaten this free control.
- **Sign balance.** 1 positive, 0 negative, 3 zero. Before reading LESSONS.md the drafts were 2 positive, 1 negative and 1 zero. LESSONS.md removed 4 of the 5 draft findings.
- **Nothing checked the findings.** There is no adversary pass and no second hunter.
- **Reproducibility.** The key is not reproducible to better than its own size: paired hunters had a median gap of 2.40 points, and 4 of 12 pairs had opposite signs.
- **Baseline measured versus inferred.** 1 of 4 names (COST, implied move 3.22%) has a live option chain. SCHL's chain is unusable, and LGCY and TBN have no options market. For those three the lean and the expected move are fallbacks.
- **Cost to trade.** All 4 are reachable long. LGCY is thin at $0.38m/day and would carry a limited-liquidity warning. The question is moot today because nothing clears the floor.
- **One day is an anecdote**, and four names cannot produce a meaningful rank correlation.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
