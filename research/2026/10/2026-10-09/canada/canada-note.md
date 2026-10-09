# Stage CA — Canada researcher — 2026-10-09

**One name was hunted and it ranks at zero. The main result today is a screen defect,
not a ranking.** The ranking key is `impact_sum`, as `edge-scores.json` reports in
`ranking_key`. GoldMining (GOLD) is calendared for fiscal Q3 after the 2026-10-09 close.
The scored window runs from the 2026-10-09 close to the **2026-10-13** close, because
2026-10-12 is Thanksgiving and the TSX is shut.

| # | Ticker | Company | impact_sum (key) | Above floor 2.8 | impact_scaled (v3, not the key) | abs_move | p_up | Anchor | Date grade | Analyst band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GOLD | GoldMining Inc. (TSX, $0.18m/day) | **+0.00** (p4) | no | +0.00 (p6) | 2.4 | 50 | register | agreed (WSH UNC) | 1–2 |

## Panel

**Four blind judges re-sized the hunter's evidence: Opus 5, Opus 5.5, Sonnet 5.5 and
Fable 5.1.** All four ran on their pinned agents, with no fallback. The panel ranks beside
`impact_sum` and replaces nothing.

| rank | ticker | selected | consensus_k | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GOLD | no | 0 | 0/4 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

- No name was selected, and the panel agrees with the hunter: every member filed nothing.
- Their `abs_move_pct` came back between 2.5 and 3.2, and every `p_up` was 50.
- What the panel numbers are not:
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales are still mostly the frozen E-P seed.
  - Nothing about this market's panel is established.

## What drives the name, and why it should not have been hunted

**GOLD (0.00, no findings).** The hunter's central claim is that GoldMining is a
**filing-only reporter for its interims**:

- Its last six interims went onto SEDAR+ and EDGAR with no same-day news release:
  2024-10-11, 2025-04-11, 2025-07-14, 2025-10-10, 2026-04-10 and 2026-07-14.
- Only the annual results get a release.
- So the universe's `event_shape: "release"` is wrong for this name, and the
  `filing_only` screen let it through.
- Every past result in the sealed `history` is an annual-filing release, plus one row
  that is not a print at all: "2026 Annual Meeting Voting Results" (2026-05-15, −6.71%).
  That is the same classifier defect stage EU found in Oslo. It inflates the scale and
  does not touch the key.

**The bar is unsourced, so every size is capped at 0.** Two aggregators disagree on EPS:
−0.02 (Earnings Whispers, seen only in a search snippet) and −0.03
(https://wealthawesome.com/will-goldmining-inc-gold-beat-earnings-estimates-in-its-next-report-10072026-earnings).
There is no company guidance for this pre-revenue explorer. The bar being unsourced came
with zero findings, which is the contract working rather than a defect.

**The only recent company news is already in the price.** The Yarumalito drill result was
released on 2026-10-06
(https://www.sec.gov/Archives/edgar/data/0001538847/000143774926032098/ex_1022557.htm)
and has traded through three sessions, so it went into `rejected_candidates`.

**The date is uncertain.** Wall Street Horizon has it as UNC after the close; Earnings
Whispers says before the open on 10-09; a snippet showed 10-13 before the open. The Q3
filing was not on SEDAR+ or EDGAR at seal.

`language_note`: not a Québec issuer, English sources only.

## Funnel and the six things this stage reports every time

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,507 |
| Candidates in window | 4 |
| Scheduled today | 2 |
| Eligible (≥ $100k/day, not filing-only, not disputed) | 1 |
| Hunted / rankable | 1 / 1 |

- **Selection:** `selection.method` was all 1 eligible names (at or under the cap of 20),
  seed `ca-2026-10-09`, so no random draw was needed. The one drop was YAY (THS Maple,
  TSXV, vendor_only, $1,203/day, below the floor).
- **Anchor arms:** options 0, register 1. The seal ran at 18:34 UTC = 14:34 ET, inside
  the session, so the zero options count is because GOLD has no Montreal chain, not
  because of the seal time. The two arms are ranked apart in `ca_resolve.py`.
- **Calendar reconciliation:**
  - confirmed 0, agreed 1, wsh_only 0, vendor_only 1, disputed 0.
  - `moved_off_target_by_wsh`: none.
  - The two calendars disagree on 172 of 277 forward dates.
- **Short register:**
  - `register_business_date` sealed: 2026-10-08.
  - GOLD reads 0.29% short and 2.46 days to cover.
  - `short_change_pct_pts` is null. A 2026-10-07 snapshot exists but does not contain
    GOLD, so there is still no history for this name.
- **No consensus EPS in the baseline:**
  - The hunter could not source one either; it got two disagreeing aggregator snippets.
  - It returned `bar` as unsourced/disputed with zero findings, which is the contract
    working rather than a defect.
- **Filing-only drops:**
  - **0 today**, so the screen dropped no one.
  - The hunter's evidence says GOLD itself is filing-only for its interims, so the screen
    missed at least one name.
  - Nobody has yet measured what this cut costs, and today it under-cut rather than
    over-cut.
- **One vendor stack:** the register, filings, archive and calendar all answered (TMX);
  there was no outage.
- **Conviction floor and coverage:**
  - Nothing is above the floor of 2.8. Over the whole US sample the sign below the floor
    was a coin flip.
  - Analyst band: 1–2 (two analysts, both Buy).

**What this day does NOT establish:**

- Nothing has resolved in Canada, and one name is not a ranking.
- If the Q3 filing appears with no release, `ca_resolve.py` may confirm it by the SEDAR+
  filing route, but the name should be read as a screen miss, not a data point about the
  hunt.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
