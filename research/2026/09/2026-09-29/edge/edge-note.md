# Edge hunt — 2026-09-29 amc + 2026-09-30 bmo

**Answer first: a quiet day. Six names, all confirmed and all ranked. None clears the
conviction floor of 3.0, so the benchmark book is empty. The largest absolute score
is YRD at −2.00, and YRD is untradeable at about $40k a day.** The ranking key is
`impact_sum` (the `ranking_key` in `edge-scores.json`), in signed points of spot.

| # | ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control −run_up_20d |
|---|---|---|---|---|---|---|---|---|
| 1 | JBL | bmo 09-30 | +0.80 | **+0.80** | +0.69 | – | yes, $363m/day, ok | −3.79 |
| 2 | CNXC | amc 09-29 | +1.20 | **+0.40** | +0.69 | – | yes, $46.7m/day, ok | +16.31 |
| 3 | FDS | bmo 09-30 | +1.50 | **+0.40** | +0.28 | – | yes, $210m/day, ok | +17.50 |
| 4 | CAG | bmo 09-30 | +0.30 | **+0.00** | +0.00 | – | yes, $155m/day, ok | +12.39 |
| 5 | CALM | bmo 09-30 | −0.20 | **−0.10** | +0.03 | – | yes, $64.5m/day, ok; borrow unchecked | +14.20 |
| 6 | YRD | bmo 09-30 | −3.00 | **−2.00** | −1.80 | – | **no**: ~$40k/day, below the $200k floor | +6.59 |

Pre-lessons and V2 are measured beside the key. Neither is traded. V2 is calibrated
on 181 ledger observations.

**How the tradable column was filled.** It comes from baseline spot × 20-day average
volume. `alpaca_trade.py assets` was not run, because this session's permission
classifier refused broker calls. So borrow at Alpaca is unchecked for the two
negatives. That changes nothing today, since neither clears the floor.

## Top and bottom

- **JBL, +0.80: the one counterparty document.** Akamai's 8-K of 2026-09-24
  (https://www.sec.gov/Archives/edgar/data/1086222/000119312526401048/d288154d8k.htm)
  says Akamai authorised Jabil to buy about $1.7bn of memory on consignment. The
  purchase sits under Akamai's server MSA with Jabil and is tied to Akamai's $11.6bn
  Anthropic deal. It postdates Jabil's June guide and lands on the FY27 guide.
  - What is already priced: JBL rose 4.8% on the 8-K.
  - Why it is sized small: the three prior beat-and-raise prints closed between
    −1.4% and +1.8%.
  - The hunter's two numbers: `expected_move_pct` +0.5, `print_vs_bar_pct` +2.5.
- **YRD, −2.00: second-hand and unsourced.** Two negatives drive it:
  - A second-hand Chinese press report that the Yixianghua platform suspended lending
    at the end of June (https://news.qq.com/rain/a/20260702A090J400, single source).
  - An unprovisioned RMB3.43bn related-party receivable, after an auditor change
    (https://www.sec.gov/Archives/edgar/data/1631761/000121390026072295/ea029591401ex99-1.htm).

  What the price already says: about 0.07× book, a market cap below net cash, and
  −86% from the 52-week high. The row is flagged `bar unsourced`. The hunter's own
  `expected_move_pct` is −1.0, half the sum. The sweep marked its baseline history
  untrustworthy, because the 2026-07-02 "+59.65% print" was a buyback announcement.

## Names that could not be ranked

None. All six were confirmed from company sources by the sweep, with zero phantom
rows.

## What the note must also say

- **Order is not sign.** Below the floor the sign is a coin flip on the evidence so
  far: 53% over 38 events. Above the floor, the rank of conviction predicted whether
  the sign was right at ρ=+0.514 (about +0.36 once the double-hunt inflation is
  removed). Every name today is below the floor. Read YRD's −2.00 as a rank, not as a
  bearish view.
- **`impact_sum` is not a move forecast.** It ranks; it does not size. The same fact
  in two findings is counted twice.
- **The control.** −run_up_20d_pct orders the day FDS, CNXC, CALM, CAG, YRD, JBL. The
  hunt's order is near-orthogonal to it: Spearman +0.06 over six names. JBL is top of
  the hunt and bottom of the control. The stage has not yet beaten a free control.
  That control itself went negative on the larger sample: −0.42% per trade over 105
  events.
- **Sign balance.** 3 positive, 1 zero, 2 negative. This is not the pessimism pattern.
  The hunters leaned away from negatives on three crowded shorts (CNXC 18.2%, FDS
  about 11%, CALM 11.8% of float) because of the short-interest rule.
- **Lessons moved every size down.** The pre-lessons sum exceeds the key in magnitude
  on five of six names (CNXC 1.2→0.4, FDS 1.5→0.4, YRD −3.0→−2.0). Only JBL is
  unchanged.
- **Nothing checked the findings.** There is no adversary pass and no second hunter.
  A factually wrong finding enters the key at full size.
- **Reproducibility.** When paired hunters ran, the median gap was 2.40 points and 4
  of 12 pairs had opposite signs. Every gap between adjacent names today is smaller
  than that.
- **Measured versus inferred.** 5 of 6 names have a live option chain. YRD's chain is
  unusable, so its lean is the run-up fallback and its expected move is a historical
  median.
- **Cost to trade.** Five of six names are liquid, from $46.7m to $363m a day. The
  bottom of the ranking (YRD) is not reachable at all. The book is empty because of
  the floor, not because of capacity.

## Critical read of the floor-clearers

None today, so there is nothing to recommend.

One day of six names is an anecdote. The pooled resolved sample is the result.

---
This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.
