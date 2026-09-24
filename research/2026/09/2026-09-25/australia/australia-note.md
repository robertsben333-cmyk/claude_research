# Stage AU — Australia researcher — 2026-09-25

**27 scheduled, 6 eligible, 6 hunted, 0 rankable. There is no ranking today.**
`selection.method`: all 6 eligible names (at or under the cap of 20), so no random draw
was needed (seed `au-2026-09-25` unused). `session_unresolved`: 0 of 6. Sealed
2026-09-24 06:41 UTC, after the Sydney close, for Friday's session. One English pass per
hunter, with `pre_lessons` frozen on every hunt. `LESSONS.md` is empty, so the freeze
changed nothing, which is correct.

## The ranking

Ranking key `impact_sum` (from `edge-scores.json`), conviction floor 3.0. **No name is
rankable, so none clears the floor.**

| ASX | company | filer_type | session | impact_sum | priced_lean | short % (18/09) | why not ranked |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| AT4 | American Tungsten & Antimony | quarterly_report_only | amc | — | +0.68 | 0.025 | hunter found no event on this date |
| HCH | Hot Chili | quarterly_report_only | amc | — | +0.55 | 0.268 | hunter found no event on this date |
| KGL | KGL Resources | quarterly_report_only | bmo | — | −0.44 | 0.011 | hunter found no event on this date |
| LIN | Lindian Resources | quarterly_report_only | amc | — | +0.46 | 2.668 | hunter found no event on this date |
| MTM | Metallium | quarterly_report_only | bmo | — | +0.10 | 0.103 | hunter found no event on this date |
| SGQ | St. George Mining | quarterly_report_only | amc | — | +1.73 | 0.595 | hunter found no event on this date |

**There is no top or bottom name.** Every hunter returned `event_confirmed: false` and an
empty `findings` list. All six reached the same diagnosis independently: the vendor's
25 September row is the **June-year-end statutory FY26 Annual Report**, due by 30
September. It is not a scheduled print. No issuer has lodged a date notice, and each one's
own ASX archive shows prior annual reports landing anywhere from 21 to 30 September (and
MTM's a day late in 2025). A 25 September date is therefore a guess. Even if the report
lands inside the window, it restates a 30 June cash position that the July Appendix 5B
already published. Archive evidence per name is in `hunts/<T>-h1.json`, e.g.
https://www.asx.com.au/asx/v2/statistics/announcements.do?by=asxCode&asxCode=SGQ&timeframe=Y&year=2025

**This is the second day running with this defect, and today it took the whole day.** On
2026-09-24 it took 8 of 12 hunts. Late-September AU vendor rows for June-FY
`quarterly_report_only` filers are statutory annual reports, not prints. Until 30
September a pre-hunt check could have saved these hunts: `quarterly_report_only` plus a
June year-end plus a date in the last ten days of September plus no date notice. It is
recorded here and in the run log; nothing in the sealed pipeline was changed.

## Outside the window (not in any number)

- **AT4:** Del Sol completion has an End Date of 27 Sep. At completion roughly 529M
  un-escrowed consideration shares struck at A$0.04 (about 29% of the register) become
  free to trade, most likely from 29 Sep, after the window. The hunter sized it −3.0 as
  outside-window. https://announcements.asx.com.au/asxpdf/20260812/pdf/072pfw5ym3ddw8.pdf
- **KGL:** Jervois FID and the second Wheaton deposit are both targeted for Q3 CY2026,
  so they resolve by 30 Sep. Sized +1.0 as outside-window.
- **LIN:** shorts rose from 1.46% to 2.67% into its S&P/ASX 300 inclusion (effective
  21 Sep), and UBS was substantial from 16 to 22 Sep through prime-broking nominees. So the
  lean's `short_building` −2.0 on LIN is probably index plumbing, not a bear building.

## Market-specific facts

- **Anchor.** There is no ASX option chain, so `options` is all null. ASIC's untruncated
  aggregated short register: file **2026-09-18** against 2026-09-11,
  **`positioning.lag_sessions` = 3**. Any "shorts building" reading describes a register
  three sessions old, on names that have since moved (AT4 +16% over 5 days, HCH +9.5%).
- **Lean.** The weights are **stage J's priors, with no Australian measurement behind
  them**. No Australian run has resolved, so there is no live `lean_vs_free_control_rho`.
  The 2026-08-27 validation read **0.80** over 20 names. Today five of the six leans are
  almost entirely the run-up term, which is the known entanglement with the free control.
- **Filer-type mix (as sealed):** 0 `results` (4D/4E), **6 `quarterly_report_only`**
  (4C/5B), 0 `none_found`. LIN's hunter notes that the classifier also misses "Half Yearly
  Report and Accounts" and "Annual Report" headlines. This is the same classifier defect
  the 09-24 run logged.
- **Vendor date shift:** dates were shifted to Sydney via `au_market.sydney_event_date()`.
  History dates are real ASX lodgements and are cited as facts in the hunt files.
- **Tooling:** ASX announcement PDFs are encrypted and `eu_pdftext.py` cannot read them.
  Hunters used ad-hoc scratch decryptors, and two collided in the shared `/tmp/claude-0`
  directory. This is the same defect the 09-24 run logged.

## What this day does not establish

It establishes nothing about whether ASX names can be ranked. Zero names were rankable,
**nothing has resolved in Australia**, and the stage runs anchor-less, in the regime
`archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073 over 104 events. Below the
conviction floor the US sign was a coin flip, and today nothing even reached a number.
One day is not a result, and an empty day is less than that.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
