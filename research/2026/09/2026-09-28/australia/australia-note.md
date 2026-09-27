# Stage AU — Australia researcher — 2026-09-28

**53 scheduled, 14 eligible, 14 hunted, 8 rankable, 0 above the conviction floor.**
`selection.method`: all 14 eligible names (at or under the cap of 20), so there was no
random draw (seed `au-2026-09-28` unused). `session_unresolved`: 1 of 14 (IPX).
Sealed Sun 2026-09-27 06:40 UTC for Monday's session. One English pass per hunter, with
`pre_lessons` frozen on every hunt. `LESSONS.md` is empty, so the freeze changed
nothing, which is the correct result.

## The ranking

Ranking key `impact_sum` (from `edge-scores.json`), conviction floor 3.0. **No name
clears it, and the largest |impact_sum| of the day is 0.6.** In practice this day is
seven zeros and three sub-point numbers.

| rank | ASX | company | session | impact_sum | priced_lean | short % (21/09) |
| ---: | --- | --- | --- | ---: | ---: | ---: |
| 1 | BML | Boab Metals | amc | +0.40 | +1.63 | 0.667 |
| 2= | AT4 | American Tungsten & Antimony | amc | 0.00 | +0.95 | 0.025 |
| 2= | MI6 | Minerals 260 | amc | 0.00 | +0.78 | 9.634 |
| 2= | SGQ | St. George Mining | amc | 0.00 | +1.68 | 0.595 |
| 2= | VMM | Viridis Mining & Minerals | amc | 0.00 | +1.25 | 1.112 |
| 6 | PEN | Peninsula Energy | amc | −0.40 | +1.48 | 1.494 |
| 7 | WC8 | Wildcat Resources | amc | −0.50 | +1.34 | 0.517 |
| 8 | PNR | Pantoro Gold | amc | −0.60 | +2.16 | 1.413 |

**Not ranked** (the hunter found no event it could confirm for this session): BCM, CHN,
GLN, HCH, IPX, KGL.

**Top, BML +0.40.** Three September-quarter deliverables are still undelivered with
three sessions left: the Project Delivery Plan with an enhanced Ore Reserve, the mining
contract award, and the first draw on the A$236m facility. They were reaffirmed on
8 Sep. Either the Plan lands inside the window, or the annual report's subsequent-events
note shows the slip. The two branches roughly cancel, so the finding adds width rather
than drift. Source: https://announcements.asx.com.au/asxpdf/20260908/pdf/073v93x3q07h0p.pdf

**Bottom, PNR −0.60.** The annual Mineral Resource and Ore Reserve statement is promised
for "end of September". It has to reconcile FY26 underground grades of 2.67–3.35 g/t
against a 5.0 g/t underground reserve grade, and the five-year plan was pushed to the
December quarter on 21 Sep. The stock ran about 10.8pp ahead of the ASX gold index into
the release while shorts covered from 2.12% to 1.41%. Source:
https://announcements.asx.com.au/asxpdf/20260730/pdf/0726h8dzz80wmp.pdf, with the
21 Sep update at https://announcements.asx.com.au/asxpdf/20260921/pdf/0749f6zytkwwch.pdf

The two other non-zero names:

- **PEN −0.40.** Davidson Kempner's "ceasing to be a substantial holder" notice leaves
  28.1m shares, about 17 sessions of volume, that can now be sold without disclosure.
  https://announcements.asx.com.au/asxpdf/20260901/pdf/073kyvxzrsbzyd.pdf
- **WC8 −0.50.** 183.6m Tranche 1 placement shares, struck at A$0.305, start trading on
  28 Sep against a A$0.29 close, so the window is their second session.
  https://announcements.asx.com.au/asxpdf/20260921/pdf/0749r4cd8q2t2c.pdf

## The defect that decided the day (third run in a row)

**Every one of the 14 hunters identified the vendor's 28 Sep row as the June-year-end
statutory FY26 Annual Report,** due by 30 Sep. It is not a 4C/5B print and not a 4D/4E.
The report restates a 30 June cash position the July Appendix 5B already published. No
issuer has lodged a date notice. The prior-year lodgements fell anywhere from 20 to
30 Sep, and several fell after the close on the 29th or on the 30th, which is outside
this window. The hunters put the odds of an in-window lodgement at between about one in
three (IPX) and near-certain (PNR).

This is the same defect that took 8 of 12 hunts on 09-24 and 6 of 6 on 09-25, and four
of today's names (AT4, HCH, KGL, SGQ) were hunted on 09-25 against the same annual report
under an earlier vendor date. It stops by itself after 30 Sep. Nothing in the sealed
pipeline was changed. A pre-hunt check would have caught it: `quarterly_report_only`
plus a June year-end plus a vendor date in the last ten days of September plus no date
notice.

## Market-specific facts

- **Anchor.** There is no ASX option chain, so `options` is all null. The substitute is
  ASIC's untruncated aggregated short register: file **2026-09-21** against 2026-09-14,
  with **`positioning.lag_sessions` = 4**. A "shorts building" reading describes a
  register four sessions old, and on a name that has already moved those four sessions
  can be the whole move. Two readings today are not positioning:
  - MI6's short doubled from 4.44% to 9.63%. That is best read as placement and index
    hedging around a A$0.88 placement and the 18 Sep index rebalance.
  - WC8's build coincided with its placement book.

  Both of those feed the lean's `short_squeeze` / `short_building` terms.
- **Lean.** The weights are **stage J's priors, with no Australian measurement behind
  them**. No Australian run has resolved, so there is no live
  `lean_vs_free_control_rho`. The 2026-08-27 validation read **0.80** over 20 names.
  Today most of the leans are the run-up term: 12 of 14 names fell over 20 days.
- **Filer-type mix (as sealed): 13 `quarterly_report_only`** (4C/5B), **1 `results`**
  (PNR), 0 `none_found`. PNR's own hunter says it lodges 5B quarterlies and no
  4D/4E, so the sealed `results` label is itself a classifier miss. The classifier also
  ignores "Annual Report to shareholders" and "Half Yearly Report" headlines. That is why
  none of the history rows measure the event actually due.
- **Vendor date shift.** Dates were shifted to Sydney time by
  `au_market.sydney_event_date()`. The `history` dates are real ASX lodgements, and the
  hunters cite them as facts.
- **Session.** 11 names are amc (window close 28 Sep → close 29 Sep) and 3 are bmo
  (BCM, IPX, KGL: close 25 Sep → close 28 Sep). IPX is `session_unresolved`.

## What this day does not establish

It establishes nothing about whether ASX names can be ranked. The day's ranked spread is
one point wide, driven by findings sized between 0.4 and 0.6 on statutory filings, and
nothing is near the conviction floor. Below that floor the US sign was a coin flip.
**Nothing has resolved in Australia.** The stage runs anchor-less, in the regime
`archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events. One day
is not a result.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
