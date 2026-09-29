# Stage AU — Australia researcher — 2026-09-30

**12 scheduled, 4 eligible, 4 hunted, 4 rankable, 0 above the conviction floor. Every
name scores `impact_sum` 0.00, so the day has no ranking.**
`selection.method`: all 4 eligible names (at or under the cap of 20). There was no random
draw, and seed `au-2026-09-30` was not used. `session_unresolved`: 0 of 4. The run was
sealed Tue 2026-09-29 06:40 UTC (16:40 Sydney) for Wednesday's session. Each hunter ran
one English pass with `pre_lessons` frozen. `LESSONS.md` is empty, so the freeze changed
nothing on any name, which is the correct result.

## The ranking

The ranking key is `impact_sum` (from `edge-scores.json`) and the conviction floor is
3.0. **No hunter returned a single finding.** The four rows below tie at zero and are in
scorer order (alphabetical). The order carries no information.

| rank | ASX | company | session | impact_sum | priced_lean | short % (23/09, Δ vs 16/09) | run-up 20d / 5d | turnover $k/day |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1= | AUE | Aurum Resources | amc | 0.00 | +0.70 | 0.901 (+0.19) | −10.6 / −9.0 | 294 |
| 1= | MKR | Manuka Resources | bmo | 0.00 | +1.54 | 0.056 (0.00) | −30.2 / −7.7 | 408 |
| 1= | PDI | PDI Gold | amc | 0.00 | +1.49 | 3.705 (+0.05) | +12.6 / −1.7 | 5,651 |
| 1= | USL | Unico Silver | amc | 0.00 | +0.76 | 1.284 (+0.51) | −20.3 / −16.6 | 1,259 |

Every name is ranked, and there is no top or bottom name to explain. What each hunter
found in place of a finding:

- **AUE.** The dated item is the FY26 statutory Annual Report. It restates cash already
  in the June 5B. The A$52.5m placement at A$0.55 was announced on 23 Sep, and its shares
  start trading on 30 Sep, the session before the window.
  https://announcements.asx.com.au/asxpdf/20260923/pdf/074drz7bbmyd84.pdf
- **MKR.** The dated item is the FY26 Annual Report. It was lodged after the 16:00 close
  in both 2024 and 2025 (15:51 and 16:30), so this year's likely falls outside a bmo
  window. The company targeted first gold sales by end-September and has announced none
  since the 21 Aug restart. That absence is visible to the market, and it cannot be dated
  or signed.
  https://announcements.asx.com.au/asxpdf/20260907/pdf/073t1nh130nz32.pdf
- **PDI.** The company itself committed to lodging a 12-month-to-30-June annual report by
  30 Sep, when it changed its year end.
  https://announcements.asx.com.au/asxpdf/20260504/pdf/06z6rt69n9bnwq.pdf
  The operating content is already public from the 30 Jul quarterly and the CEO's 28 Sep
  forum talk. The Bankan exploitation permit is described as "imminent" and would be a
  large binary positive, but it has no date, so the hunter put it outside the window.
- **USL.** The dated item is the Annual Report, and last year's landed at 09:06, before
  this window opens. The in-window event is the 1 Oct allotment of 78.9m placement shares
  at A$0.76, which is about 7% above spot. That timetable has been public since 24 Sep.
  The hunter could not defend a sign.
  https://announcements.asx.com.au/asxpdf/20260924/pdf/074gf9tsgvttll.pdf

## The defect, fourth run in a row and the last

**All four hunters identified the vendor's 30 Sep row as the June-year-end statutory
FY26 Annual Report**, due by the 30 Sep deadline. It is not a 4C/5B print and not a
4D/4E. This is the same defect as on 09-24, 09-25 and 09-28. It ends by itself after
today, because the deadline passes.

The classifier does not count "Annual Report to shareholders", "Full Year Statutory
Accounts" or "Half Yearly Report" headlines. As a result, the sealed history measures
quarterly-report days and not the kind of event that is actually due. Nothing in the
sealed pipeline was changed.

The pre-hunt check already proposed on 09-28 would have caught all four names. It flags
a row that is `quarterly_report_only`, has a June year end, has a vendor date in the last
ten days of September, and has no date notice.

## Market-specific facts

- **Anchor.** There is no ASX option chain, so `options` is all null. The substitute is
  ASIC's untruncated aggregated short register. The run used file **2026-09-23** against
  2026-09-16, with **`positioning.lag_sessions` = 4**. A "shorts building" reading
  describes a register four sessions old.
  - The two builds today (AUE +0.19pp, USL +0.51pp) both coincide with placements. The
    hunters read them as placees hedging, closed by delivery of the new shares rather
    than by market buying. On that reading they are not squeeze fuel, but they still feed
    the lean's `short_building` term.
- **Lean.** The weights are **stage J's priors, with no Australian measurement behind
  them**. The only resolved Australian run is 2026-09-24, with 4 names and the hunt at
  ρ=−0.21, p=0.83. It withholds `lean_vs_free_control_rho` because the rule requires at
  least five names. So no live reading of that ρ exists yet. The 2026-08-27 validation
  read **0.80** over 20 names, which means the lean is more entangled with the free
  control than Tokyo's is. On three of today's four names the lean is mostly the run-up
  term.
- **Filer-type mix (as sealed): 4 `quarterly_report_only`** (4C/5B), 0 `results`, 0
  `none_found`. The real event on all four is a statutory annual report, which is a
  third kind the classifier does not label. PDI is also a TSX reporting issuer and files
  statutory accounts that the classifier missed.
- **Vendor date shift.** Dates were shifted to Sydney time by
  `au_market.sydney_event_date()`. The `history` dates are real ASX lodgements, and the
  hunters cite them as facts.
- **Session.** Three names are amc, with a window from the 30 Sep close to the 1 Oct
  close. MKR is bmo, with a window from the 29 Sep close to the 30 Sep close. The hunters
  doubt the vendor's session on three names: MKR likely amc, and PDI and USL likely
  in-session or pre-open. None of these is flagged `session_unresolved`.

## What this day does not establish

This day establishes nothing about whether ASX names can be ranked. Four ties at zero
cannot be ranked against anything, and no name is near the floor. Below that floor the
US sign was a coin flip. **Australia's resolved record is one four-name day.** The stage
runs anchor-less, in the regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073,
p=0.45 over 104 events. One day is not a result.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
