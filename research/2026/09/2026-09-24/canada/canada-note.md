# Stage CA — Canada researcher — 2026-09-24

**Empty day: nobody cleared the floor.** The TSX was open (`market_closed: null`) and 8 names were scheduled for the Toronto window. All 8 fell below the $200k/day turnover floor, so 0 were eligible and 0 were hunted. This is the normal thin-calendar case for late September, not a fault.

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,520 |
| Candidates in window | 20 |
| Scheduled today | 8 |
| Eligible (≥ $200k/day, not filing-only, not disputed) | 0 |
| Hunted | 0 |

| Ticker | Exchange | Date grade | Event shape | Turnover (USD/day) | Dropped because |
| --- | --- | --- | --- | --- | --- |
| MMY (Monument Mining) | TSXV | vendor_only | release | 114,223 | below turnover floor |
| ROS (RosCan Gold) | TSXV | vendor_only | filing_only | 22,017 | below turnover floor (also filing-only) |
| OGD (Orbit Garant Drilling) | TSX | confirmed | release | 14,422 | below turnover floor |
| SONA (Sona Nanotech) | CSE | vendor_only | filing_only | 7,461 | below turnover floor (also filing-only) |
| SR | TSXV | vendor_only | filing_only | 7,363 | below turnover floor (also filing-only) |
| FCLX (FCL-X Fire & Safety) | TSXV | vendor_only | filing_only | 6,268 | below turnover floor (also filing-only) |
| PHRM | CSE | vendor_only | filing_only | 1,727 | below turnover floor (also filing-only) |
| NEXE (NEXE Innovations) | TSXV | vendor_only | release | 1,238 | below turnover floor |

- **Calendar reconciliation:** confirmed 1 · agreed 0 · wsh_only 0 · vendor_only 7 · disputed 0. `moved_off_target_by_wsh`: 0.
- **Filing-only screen:** 5 of 8 scheduled rows (ROS, SONA, SR, FCLX, PHRM) were filing-only. The turnover floor removed all of them first, so the filing-only screen made no binding cut today.
- **Anchor arms:** options 0 · register 0. No names were sealed, so this day says nothing about whether the arms differ. It is not a sign that the run was sealed outside market hours: the run fired at 18:33 UTC, which is 14:33 in Toronto.
- **Short register:** no baselines were sealed, so no snapshot was stored today (`ca_priced_in.py` writes one only when it seals names). `researcher_canada/analysis/short-register/` still holds only 2026-09-22. We still cannot tell whether the feed refreshes daily or restamps CIRO's twice-monthly snapshot.
- **Vendor stack:** the TMX calendar (WSH confirmed OGD) and the news archive both answered, so this is not an outage. Yahoo did not answer the CAD/USD request for the second day running, and the floor used the fallback constant 0.71. The highest turnover (MMY, $114k) sits about 43% under the floor, so no plausible exchange rate would have let a name through.
- **Consensus EPS / language_note / pre_lessons:** not applicable, because no hunter ran.

**What this day does not establish:** anything about the hunt, the anchor-arm comparison or register history. Nothing has resolved in Canada yet.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
