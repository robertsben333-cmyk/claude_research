# Stage AU — Australia researcher — 2026-09-24

**34 scheduled, 12 eligible, 12 hunted, 4 rankable.** `selection.method`: all 12 eligible
names (at or under the cap of 20), so there was no random draw today (seed `au-2026-09-24`
unused). `session_unresolved`: 0 of 12. Sealed 2026-09-23 06:38 UTC, after the Sydney close.
One English pass per hunter, `pre_lessons` frozen on every hunt; `LESSONS.md` is empty so
it changed nothing, which is correct.

## The ranking

Ranking key `impact_sum` (from `edge-scores.json`). Conviction floor 3.0: **no name clears it.**

| # | ASX | company | filer_type | session | impact_sum | conviction | priced_lean | event |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 1 | AAR | Astral Resources | quarterly_report_only | amc | 0.00 | 0.00 | +0.49 | annual report, cadence prior only |
| 2 | SOL | Soul Pattinson | results | bmo | 0.00 | 0.00 | +1.80 | **company-announced** 14/09 |
| 3 | PMV | Premier Investments | results | bmo | −0.50 | 0.50 | +0.95 | FY26 result, strong evidence |
| 4 | PEN | Peninsula Energy | quarterly_report_only | amc | −1.00 | 1.00 | +1.34 | annual report, date ~50% per hunter |

AAR and SOL tie at zero; their order is arbitrary and carries no information.

**Not ranked: 8 names, all because the hunter could not confirm an event on this date.**
BCM, CHN, CXO, GLN, PNR, RML, VMM, WIA. None is a proven phantom; each is a vendor row that
maps onto the June-year-end **statutory annual report**, due by 30 September. Prior-year
lodgements landed anywhere from 23 to 30 September, so a 24 September date is a guess.

## What drives the ends

- **Top (AAR, 0.00):** no finding. The hunter concluded the event is a non-price-sensitive
  annual report whose one hard number (about A$65m cash at 30 June) was in the 27 July
  quarterly. Source: https://www.proactiveinvestors.com/companies/news/1096038/astral-resources-builds-momentum-at-mandilla-during-june-quarter-as-drilling-resource-growth-and-dfs-work-advance-1096038.html
  — AAR was marked `event_confirmed: true` on the cadence pattern alone (25/09/2024,
  25/09/2025). **That is the TRT reasoning CLAUDE.md warns against**, and it is the only
  reason AAR is ranked while seven identical cases are not. It changes nothing at 0.00, but
  the resolver should check it.
- **Bottom (PEN, −1.00):** the first annual accounts with market cap (~A$151m) far below
  book (US$203.2m net assets at 31/12/2025, when directors saw "no indicators for
  impairment"); guidance withdrawn 22 July, life-of-mine plan withdrawn since August 2025,
  so a Lance impairment test and possible write-down. Inference, not a company statement;
  range −4.0 to +1.5. Source: https://announcements.asx.com.au/asxpdf/20260309/pdf/06x6v3y9831dvg.pdf
- **PMV (−0.50):** Myer's 22/09 release disclosed its first 8 weeks of FY27 (Myer Apparel
  Brands comps −5.9%); Premier customarily gives first-weeks trading at its result and
  Lew promised Smiggle growth in FY27. A read-through across different categories, cut
  against by Myer's September/Father's Day improvement. Source:
  https://www.investing.com/news/company-news/myer-fy26-slides-record-sales-top-4b-but-profits-slip-on-margins-93CH-4912105

## Market-specific facts

- **Anchor.** No ASX option chain; `options` is all null. The baseline carries ASIC's
  untruncated aggregated short register, file **2026-09-17** against 2026-09-10:
  **`positioning.lag_sessions` = 3**. A "shorts building" reading describes three sessions
  ago. PNR's +0.26pp build is most likely S&P/ASX 200 deletion arbitrage (effective 21/09),
  and the stock is +15% since the register date.
- **Lean.** Weights are **stage J's priors with no Australian measurement**. No Australian
  run has resolved, so there is no live `lean_vs_free_control_rho`; the 2026-08-27
  validation read **0.80** over 20 names, more entangled with the free control than
  Tokyo's 0.45–0.59. The short-squeeze term pushed SOL (+1.80) and CHN (+2.54) highest; no
  hunter found anything supporting it on any name.
- **Filer-type mix (as sealed):** 4 `results` (CXO, PMV, PNR, SOL), 8
  `quarterly_report_only`, 0 `none_found`. **Two of the four are misclassified** per their
  hunters: CXO lodges an "Annual Report to Shareholders" and "Half-year Report", no 4E, and
  its results median of 9.09% rests on one row (about 4.4% with the missed rows); PNR's six
  "results" rows are Quarterly Results Presentations lodged with the 5B, so its 10.91%
  median measures quarterlies. Only SOL and PMV are genuine profit results today.
- **Dates.** Every row is `converted from the vendor's UTC instant to Sydney time`. Histories
  are observed ASX lodgement dates and are cited as facts. 7 of 12 are `amc` per the vendor,
  so their window is close 24/09 → close 25/09; WIA is vendor-`bmo` but both its prior
  annual reports went after the close.

## What this day does not establish

Anything. Two genuine profit prints, two below-floor negatives, no name above the conviction
floor (over the US sample the sign below it was a coin flip). Nothing has resolved in
Australia; the stage runs anchor-less in the regime `archive/backtest/FINDINGS.md` §33
priced at ρ=+0.073, p=0.45 over 104 events, and one day is not a result.

**The day's real finding is a calendar defect:** in late September the vendor dates June
year-end cash-flow filers at their annual-report deadline, which is neither a profit print
nor a 5B. Eight of twelve hunts were spent on it. See the run log.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
