# Stage CA — Canada researcher — 2026-09-22 (Toronto session of 2026-09-22 amc / 2026-09-23 bmo)

**Empty day: nobody to rank.** The TSX was open (`market_closed: null`), 2 names were scheduled,
and **both fell below the $200k/day turnover floor**, so 0 were eligible and 0 were hunted.
That is the "scheduled but nothing clears the floor" case, a normal late-September outcome,
not a fault.

| Funnel | |
| --- | --- |
| Scanner rows | 2505 |
| Candidates in window | 17 |
| Scheduled today | 2 |
| Eligible | 0 |
| Hunted | 0 |

Dropped:

- **MMY**, Monument Mining (TSXV), `vendor_only`, release, turnover $147,072 < $200,000
- **SR**, Strategic Resources (TSXV), `vendor_only`, **filing_only**, turnover $9,227 < $200,000

## The five items this stage reports every time

- **Anchor arms:** options 0 / register 0. No baselines were sealed because nobody was
  eligible. The seal *would* have been inside 09:30–16:00 ET (the universe was built at
  18:36 UTC = 14:36 ET), so an empty options arm today says nothing about chain quoting.
- **Calendar reconciliation:** confirmed 0 · agreed 0 · wsh_only 0 · vendor_only 2 ·
  disputed 0. `moved_off_target_by_wsh`: none. Wall Street Horizon confirmed neither
  scheduled name.
- **Short register:** not sealed today (no names), so there is no `register_business_date`
  for this run. `researcher_canada/analysis/short-register/2026-09-22.json` already existed
  from an earlier session. It holds one row (AGF.B) with every field null. It is not a
  usable first snapshot, so `short_change_pct_pts` stays uncomputable on the next run.
- **Consensus EPS:** none in any baseline, as always; no hunter ran, so no `bar: unsourced`
  question arises.
- **Filing-only cut:** 1 of 2 scheduled names (SR) was `filing_only`, but it was already
  below the turnover floor, so the filing-only screen **cost no name today**.

**Vendor stack:** the TMX GraphQL calls answered (WSH reconciliation and news archive
populated `financial_headlines`/`news_rows`). One separate degradation: **the CAD→USD rate
was a fallback constant 0.71 because Yahoo did not answer.** MMY's floor miss ($147k) is
far enough under $200k that no plausible rate would flip it.

**What this day does not establish:** nothing at all about the hunt, either anchor arm or
the calendar grades. There is no ranking, and nothing has resolved in Canada yet.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
