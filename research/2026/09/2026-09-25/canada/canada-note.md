# Stage CA — Canada researcher — 2026-09-25

**No ranking today: one name was eligible, and it has no print on this date.** The TSX was
open (`market_closed: null`). 6 names were scheduled for the Toronto window and 1 was
eligible: BRC (Blackrock Silver, TSXV, $1.23m/day). Its baseline was sealed at 18:33 UTC
(14:33 ET), before the close. The hunter then found that no results release lands on
2026-09-25 (`event_confirmed: false`). `edge_score.py` gives **0 of 1 rankable** and
**0 above the conviction floor of 3.0**. The ranking key is `impact_sum`, read from
`edge-scores.json`.

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,526 |
| Candidates in window | 14 |
| Scheduled today | 6 |
| Eligible (≥ $200k/day, not filing-only, not disputed) | 1 |
| Hunted | 1 |
| Rankable | 0 |

| Ticker | impact_sum | Anchor | Date grade | Why not ranked |
| --- | --- | --- | --- | --- |
| BRC | — (hunter: 0.0, no findings) | register | vendor_only | The hunter found no event on this date |

**Why BRC is out.** The hunter's evidence, all in `hunts/BRC-h1.json`:

- Blackrock Silver is a pre-revenue explorer with a 30 November fiscal year-end. It files its interims on SEDAR+ and does not put out a release with them.
- On the TMX filing index, its Q3 interims went in on 2024-09-27 and 2025-09-29, and neither had a same-day release. Nothing had been filed on 2026-09-25 when the hunter checked at about 18:34 UTC.
- Its newsroom (https://blackrocksilver.com/news/) has announced no results date.
- The vendor's 09-25 and an aggregator's 09-28 are both estimates from past timing, for a Q3 interim that is not due until 2026-10-30.

This is the same kind of mistake as TRT, caught by the hunt before anything else used it.

**The hunt surfaced two stage defects:**

1. **The filing-only screen missed BRC.** `ca_universe.py` gave it `event_shape: "release"` with `financial_headlines: 4`. That count is almost certainly the defect below: an issuer that has never released results was counted as a releaser. The universe screen and the history classifier probably share that headline test.
2. **The history classifier counts "Annual General Meeting Results" as a financial-results release.** All 3 rows in BRC's sealed `history` are AGM results, so the median 5.8% "reaction" measures shareholder-meeting days, not reactions to a print. This is the same family as the Oslo "Invitation to Q4 results" defect and the ASX "Results Release Date" defect. Nothing was patched in this run.

## The six items the note carries every time

- **Anchor arms: options 0 · register 1.** The seal was inside the session (14:33 ET), so the zero on the options arm is not a timing artefact. BRC simply has no Montréal chain, which is the normal case below $25m a day. The two arms are ranked separately in `ca_resolve.py`. Today there is nothing to rank on either arm.
- **Calendar reconciliation:** confirmed 0 · agreed 0 · wsh_only 0 · vendor_only 6 · disputed 0. `moved_off_target_by_wsh`: none. Every scheduled row was a single vendor with no Wall Street Horizon row, and the one row hunted turned out to be a phantom.
- **Short register:** `register_business_date` sealed is **2026-09-24**. The snapshot was stored as `researcher_canada/analysis/short-register/2026-09-25.json`. BRC's `short_change_pct_pts` is still null, because the only earlier snapshot (2026-09-22) held a single name (AGF.B). We still cannot tell whether the feed refreshes daily.
- **Consensus EPS:** none in the baseline, as always. The hunter reports `bar: none`: no revenue, no EPS guidance, and 1 analyst (Buy, C$2.10 target, per TMX) with no quarterly estimate. It emitted no findings, so the unsourced-bar-with-large-findings defect did not occur.
- **One bilingual pass:** `language_note` = "not a Quebec issuer, English sources only". No `pre_local` was requested. `pre_lessons` was an empty draft at 0, and `researcher_canada/LESSONS.md` is still empty.
- **Filing-only screen:** 3 of 6 scheduled rows were flagged `filing_only` (XXIX, FCLX, SR). The turnover floor removed all 3 first, so the screen made no binding cut. The screen should also have caught BRC and did not (defect 1). How much this screen costs is still unmeasured, and today suggests it also lets filing-only names through.

**Vendor stack:** the TMX tape, register, calendar, news archive and filing index all answered, so this was not an outage. Yahoo did not answer the CAD/USD request for the third day running, so the floor used the fallback constant 0.71. BRC's turnover of $1.23m clears the floor under any plausible rate. MMY ($105k) does not clear it either way.

**What this day does not establish:** anything about the hunt, the anchor-arm comparison or the lean. No name was ranked, and nothing has resolved in Canada yet. One day is not a result.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
