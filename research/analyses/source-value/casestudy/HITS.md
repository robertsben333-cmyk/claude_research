# Large-cap hits: what the right calls rested on (written before the misses were looked at)

`scripts/casestudy.py hits`, 2026-10-05. A hit: the live hunt or the four-model median had a
view, the sign was right, and the move exceeded half the priced move. **6 of the 26 large caps
(> $10bn) with a view are hits** (8 of 33 mid caps). These are anecdotes and are labelled as
such; only the rules below are tested.

| print | call | move / priced | what the call rested on |
|---|---|---|---|
| DELL 09-01 amc | up | +8.7 / 9.3 | Two direct server-assembler peers had reported the OVERLAPPING quarter with margin upside, plus IDC industry data for two of the quarter's three months. Other-company read-across on the same period, quantified, dated in window. |
| PANW 09-01 amc | down | −4.4 / 7.8 | A one-day +12.8% run-up on an M&A rumour (price item, widely reported) plus the company's OWN release arithmetic: the share count implied by its guide makes the first FY27 EPS guide mechanically lower. Own primary document, not widely read. |
| LULU 09-03 amc | down | −19.4 / 9.4 | The company's guide was set on 4 June; a viral brand crisis in China came 11-13 days LATER, so the guide predates in-window bad news; a competitor's record China launch (other-company, in window). Large magnitude claim. |
| SUNB 09-08 bmo | up (median4 +0.07, barely) | +7.3 / 9.8 | Mixed: an own buyback slowdown (down) against a well-supported volume set-up (up). A coin-flip view, not a reasoned call. |
| AZO 09-21 bmo | up | +5.6 / 8.4 | Peer prints whose measuring periods ENDED before AZO's quarter (timing mismatch the market priced as read-across), plus a LIFO detail in AZO's own 10-Q. Other-company timing, own primary document. |
| NKE 10-01 amc | down | −7.4 / 9.2 | Wholesale partners (JD Sports NA, Pou Sheng, Topsports) reporting sell-through weakness over the window after Nike last spoke; arithmetic showing consensus at the ceiling of Nike's own framework. Customer/supplier read-across on the same period. |

## Common features

1. **Other companies reporting the same period** (peers, customers, wholesale partners,
   industry data), quantified and dated inside the window: DELL, AZO, NKE, LULU (competitor).
2. **Something dated after the company last spoke** that its guide could not include: LULU
   (viral crisis after the guide), NKE (partner sell-through and tariff change after the
   guide), PANW (rumour run-up after the last print).
3. **A detail in the company's own primary document that is not widely read**: PANW share
   count, AZO LIFO reserve.

## Rules derived (frozen in `rules.json` before the misses are opened)

- **R1 same-period read-across**: the net vote of the print's voting items of subtype
  `oth_peer_results`, `oth_customer_supplier`, `G:other_company` or `med_industry_report`
  that are quantified and dated in the window.
- **R2 corroborated read-across**: R1 with at least two such items.
- **R3 unread own-document detail**: the net vote of voting `own_periodic_report` /
  `own_results_release` / `own_guidance_targets` items that read the primary document, are
  quantified and are NOT already widely reported.
- **R4 fresh, not widely reported, not the company's own**: the net vote of voting items
  outside the company-own group that are dated in the window, quantified and not widely
  reported.
- **R5 R1 or R3**: the net vote of R1's and R3's items together.
- **R6 large claims**: the net vote of voting items that claim a large move (relative to
  the priced move), are quantified and are not widely reported.

Derived from the 6 large-cap hits; scored (`rules-test.json`) on every large cap NOT among
them (misses and no-view prints), on the mid caps, on the small and micro caps, and on the
forward days when they exist. A rule is never scored on a print it was derived from.
