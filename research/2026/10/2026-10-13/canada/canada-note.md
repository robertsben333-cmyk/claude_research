# Stage CA — Canada researcher — 2026-10-13

**No name is ranked today.** One name was hunted, and the hunter returned
`event_confirmed: false`, so `edge_score.py` marks it not rankable. The ranking key is
`impact_sum`, as `edge-scores.json` reports in `ranking_key`.

| # | Ticker | Company | impact_sum (key) | Above floor 2.8 | impact_scaled (v3, not the key) | abs_move | p_up | Anchor | Date grade | Analyst band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| — | GOLD | GoldMining Inc. (TSX, $0.18m/day) | not ranked: the hunter found no event on this date (0 findings) | — | — | 2.5 | 50 | register | agreed (WSH UNC) | 1–2 |

## Panel

**The panel did not run, because there was nothing to judge.** `market_panel.py packs`
built 0 packs, since no name was rankable. No judges were spawned and no
`edge-scores-panel.json` was written.

## GOLD, and why it is the same event as 2026-10-09

**This is the same event the 2026-10-09 run hunted.** That run hunted GOLD for its unfiled
Q3 FY2026 interim.
- Since then, Wall Street Horizon's unconfirmed (UNC) date has moved from 10-09 to 10-13.
- TMX's SEDAR+ index shows no Q3 filing between 10-05 and 10-13. The only filing in that
  span is the 10-06 drill news release.
- At most one of the two runs can resolve against a real print. Never pool both.

**The hunter's case is that GoldMining is filing-only for its interims.** The universe
tagged the event as a release (`event_shape: release`), which is wrong for this issuer.
- Its last four interim quarters were filed on SEDAR+ and as an EDGAR 6-K, with no press
  release: Q3 FY2024 (2024-10-11), Q3 FY2025 (2025-10-10), Q1 FY2026 (2026-04-10) and
  Q2 FY2026 (2026-07-14).
- So the `filing_only` screen missed it, for the second run in a row.

**There is no bar.** This is a pre-revenue explorer with no guidance and no consensus, so
`bar` is unsourced and there are no findings to size. That is the contract working, not a
defect.

**Liquidity is not a near-term issue, and the one dated financing item is outside the
window.** The Q2 MD&A shows working capital of C$82.1m and states the company has enough
for 12 months. The US$50m ATM expires on 2026-12-08, after the window, so it was filed
under `outside_window` at size 0
(https://www.sec.gov/Archives/edgar/data/1538847/000143774926023556/ex_985515.htm).

**The baseline's history is contaminated.** All four rows are annual 40-F filing notices,
or the 2026-05-14 AGM voting-results release (−6.71%), which counts a non-print as a
print. This classifier defect is still not fixed. It inflates the scale and does not touch
the key.

`language_note`: not a Québec issuer, English sources only. `pre_lessons` equals the
final answer: 0 findings, and `LESSONS.md` is empty.

## Funnel and the six things this stage reports every time

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,501 |
| Candidates in window | 7 |
| Scheduled today | 3 |
| Eligible (≥ $100k/day, not filing-only, not disputed) | 1 |
| Hunted / rankable | 1 / 0 |

- **Selection:**
  - `selection.method`: all 1 eligible name (the cap is 20), seed `ca-2026-10-13`, so
    there was no random draw.
  - Dropped below the floor: YAY ($1,200/day, vendor_only) and INEO ($2,740/day,
    vendor_only).
- **Anchor arms:** options 0, register 1.
  - The seal was at 18:34 UTC = 14:34 ET, inside the session.
  - The zero on the options arm is because GOLD has no Montreal chain, not because of the
    seal time.
  - The two arms are ranked apart in `ca_resolve.py`.
- **Calendar reconciliation:**
  - confirmed 0, agreed 1, wsh_only 0, vendor_only 2, disputed 0.
  - `moved_off_target_by_wsh`: none.
  - The two calendars disagree on 172 of 277 forward dates. Today shows the cost: an
    "agreed" date can be one vendor's UNC estimate rolled forward, and the other vendor
    copying it.
- **Short register:**
  - `register_business_date` sealed: 2026-10-12. That is the Thanksgiving holiday itself,
    one business day after the 2026-10-09 run's 10-08.
  - GOLD reads 0.27% short and 2.44 days to cover.
  - `short_change_pct_pts` is −0.02 against the 2026-10-09 snapshot. This is the first
    non-null change for this name.
  - So far the feed looks like it refreshes daily rather than twice a month, but one
    pair does not settle that.
- **No consensus EPS:**
  - None was in the baseline, and the hunter could not source one either.
  - `bar` is unsourced, and there are zero findings, so there is no oversized-unsourced
    defect.
- **Filing-only drops:**
  - 0 today.
  - GOLD should have been one, on the hunter's evidence, so the screen under-cut again.
- **One vendor stack:** the register, filings, archive and calendar all answered (TMX).
  There was no outage.
- **Conviction floor:** nothing is above 2.8, and nothing is ranked.

**What this day does NOT establish:** anything about the hunt. No Canadian day has
resolved, nothing ranked today, and the only hunted name is a screen miss carried over
from 10-09.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
