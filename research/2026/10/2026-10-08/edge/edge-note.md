# Edge hunt — 2026-10-08 amc + 2026-10-09 bmo

**Answer first: four names ranked and none clears the conviction floor, so there is no book today.**
The whole table spans -0.90 to +0.80 points of spot. `edge-scores.json` names its ranking key as
`impact_sum`. The book selects on `impact_scaled` at 1.76 (`execution.benchmark`), and the largest
|impact_scaled| today is HOVR's 1.26. Nothing was bought.

| # | ticker | session | pre-lessons | **post-lessons (key)** | scaled | V2 | floor 2.8 | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ODC | amc 2026-10-08 | +1.40 | **+0.80** | +0.90 | not run | no | yes (long, $10.4m/day, ok) | +0.74 |
| 2 | PKE | amc 2026-10-08 | +0.90 | **+0.60** | +0.68 | not run | no | yes (long, $7.3m/day, ok) | +2.04 |
| 3 | DAL | bmo 2026-10-09 | −1.00 | **−0.90** | −0.22 | not run | no | yes (short, borrow at Alpaca, $629m/day) | −4.45 |
| 4 | HOVR | bmo 2026-10-09 | −1.30 | **−0.90** | −1.26 | not run | no | elsewhere (not lendable at Alpaca; **thin**, $0.64m/day) | +5.25 |

DAL and HOVR tie on the key. Pre-lessons, scaled and V2 are measured beside the key and are not
traded. **V2 was not written.** `edge_grounded_score.py` dated the run's first print to
2026-10-08 09:30 ET and refused. The likely cause is that it read the unconfirmed NRIX row (dated
10-08, session unknown) as a bmo print. The real first print is ODC and PKE after today's close,
which had not passed. This is recorded as a defect and was not worked around.

## What drives the top and the bottom

- **ODC, +0.80 (top).** The largest finding is a +0.8 category read-through. Church & Dwight reported
  Arm & Hammer litter consumption up 7.5% in Apr–Jun 2026
  (https://www.marketbeat.com/instant-alerts/church-dwight-q2-earnings-call-highlights-2026-07-31/).
  It is netted against −0.9 for margin and freight pressure that the CEO flagged on the Q3 call. A
  +0.6 finding is new: an 8-K accepted 2026-10-07 20:02 ET raised the revolver and removed the
  $100m cap on acquisitions
  (https://www.sec.gov/Archives/edgar/data/74046/000162828026065374/odc-20261007.htm).
  - **What the price says:** there is no option chain. The stock is −6.4% over 5 days and −0.74%
    over 20 days. There is no sell-side consensus; the bar is the company's own floor of FY net
    income above $54.0m.
- **HOVR, −0.90 (bottom, tied).** A $50m ATM has been live since 2026-09-04 (424B5:
  https://www.sec.gov/Archives/edgar/data/1930021/000121390026097676/ea0304433-424b5_newhorizon.htm),
  and the prototype timeline already slipped once at the last print, which fell 12.3%.
  - **What the price says:** no option chain, −8.1% over 5 days, −60.7% from the 52-week high. The
    hunter's own bar (a single sponsored Zacks estimate) is unsourced by the stage's standard.
- **DAL, −0.90 (bottom, tied).** Realised Q3 jet fuel ran well above the $3.15/gal Delta assumed
  in its guide (−0.5, https://www.flycraft.com/jet-fuel-price). This is offset by JetBlue's
  2026-09-10 8-K raising RASM (+0.6,
  https://www.sec.gov/Archives/edgar/data/0001158463/000115846326000089/jblu-20260910.htm).
  - **What the price says:** the option chain implies 6.36%, skew is +0.71, and the stock is
    +4.45% over 20 days.

## Not ranked

- **NRIX:** the event is not confirmed. There is no company date notice, and vendors disagree (10-08, 10-09, 10-12). No hunt.
- **GLDG:** the event is not confirmed. It files interim 6-Ks with no release and no pre-announcement, so it is not a priced earnings event. No hunt.
- **CMMB:** killed by `session_resolve.py` before the sweep (6-K filed 2026-09-30).
- **HIFS:** dropped by `session_resolve.py` before the sweep (not in the SEC ticker map).

## Critical read of the floor-clearers

None today. Every row is below the 2.8 floor, so the stage has nothing it would recommend trading.

## What the note must also say

- **Order is not sign.** Below the floor the sign has been a coin flip (53% over 38 events). Above
  it, the rank of conviction predicted whether the sign was right at ρ=+0.514. All four rows today
  are below the floor, so DAL's and HOVR's −0.90 are not bearish views.
- **`impact_sum` ranks; it does not size.** Findings that rest on one document can double-count.
- **Control.** `−run_up_20d_pct` orders the day HOVR > PKE > ODC > DAL, while the hunt orders it
  ODC > PKE > DAL = HOVR. They disagree most on HOVR (top of the control, bottom of the hunt). Over
  the resolved sample the hunt has not been shown to beat this free control.
- **Sign balance:** 2 positive, 2 negative. All four findings sets net opposing theses (see `flags`):
  - DAL and HOVR each expect the print and the stock to go opposite ways.
  - ODC splits 4/2.
  - PKE splits 3/3.
- **Nothing checked the findings.** There is no adversary pass and no second hunter, so a wrong
  fact enters the key at full size.
- **Reproducibility.** When the stage double-hunted, twelve paired names had a median gap of 2.40
  points, and 4 of 12 had opposite signs. Every number today is smaller than that gap.
- **Measured versus inferred baseline.** Two of four ranked names (DAL, PKE) have a live option
  chain. PKE's chain is indicative only, with an ATM spread of 47% of mid. ODC and HOVR fall back
  to the run-up lean and a historical median.
- **Cost to trade:**
  - DAL is deep.
  - ODC and PKE clear the turnover floor.
  - HOVR is thin at $0.64m/day and not lendable at Alpaca.
  - The bottom of the ranking is therefore the least reachable name.
- **One day is an anecdote.** Four names cannot produce a meaningful rank correlation.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects, sizes or trades on them.

- ODC: retail 32 (no), search failed, 20d vol 26% (no)
- PKE: retail 45 (no), search sparse, vol 28% (no)
- DAL: retail 26 (no), search spike 3.57x on 2026-10-07 (not quiet), vol 26% (no)
- HOVR: retail 61 (yes), search sparse, vol 37% (no)

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven
by market positioning, guidance, macro conditions, and management commentary rather than reported
results alone.
