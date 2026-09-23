# Stage CA — Canada researcher — 2026-09-23

**Empty day: nobody cleared the floor.** The TSX was open (`market_closed: null`) and 4 names were scheduled for the Toronto window. All 4 fell below the $200k/day turnover floor, so 0 were eligible and 0 were hunted. This is the normal thin-calendar case for late September, not a fault.

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,515 |
| Candidates in window | 24 |
| Scheduled today | 4 |
| Eligible (≥ $200k/day, not filing-only, not disputed) | 0 |
| Hunted | 0 |

| Ticker | Exchange | Date grade | Event shape | Turnover (USD/day) | Dropped because |
| --- | --- | --- | --- | --- | --- |
| MMY (Monument Mining) | TSXV | vendor_only | release | 139,426 | below turnover floor |
| DND (Dye & Durham) | TSX | disputed | release | 119,429 | below turnover floor (also a disputed date) |
| WILD (WildBrain) | TSX | confirmed | release | 54,642 | below turnover floor |
| SR | TSXV | vendor_only | filing_only | 9,684 | below turnover floor (also filing-only) |

- **Calendar reconciliation:** confirmed 1 · agreed 0 · wsh_only 0 · vendor_only 2 · disputed 1. `moved_off_target_by_wsh`: none.
- **Filing-only screen:** 1 of 4 scheduled rows (SR) was filing-only. The turnover floor removed it first, so the filing-only screen made no binding cut today.
- **Anchor arms:** options 0 · register 0. No names were sealed, so this day says nothing about whether the arms differ. It is not a sign that the run was sealed outside market hours: the run fired at 18:33 UTC, which is 14:33 in Toronto.
- **Short register:** no baselines were sealed, so no snapshot was stored today. `researcher_canada/analysis/short-register/` still holds only 2026-09-22. We still cannot tell whether the feed refreshes daily or restamps CIRO's twice-monthly snapshot.
- **Vendor stack:** the TMX calendar (WSH) and the news archive both answered, so this is not an outage. Yahoo did not answer the CAD/USD request, and the floor used the fallback constant 0.71. The highest turnover (MMY, $139k) sits about 30% under the floor, so no plausible exchange rate would have let a name through.
- **Consensus EPS / language_note / pre_lessons:** not applicable, because no hunter ran.

**What this day does not establish:** anything about the hunt, the anchor-arm comparison or register history. Nothing has resolved in Canada yet.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
