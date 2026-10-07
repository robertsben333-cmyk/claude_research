# Stage CA — Canada researcher — 2026-10-07

**Two names ranked, both mildly negative, and neither near the conviction floor.** The
ranking key is `impact_sum`, as `edge-scores.json` reports in `ranking_key`. Both are
Q3 releases after the Toronto close on 2026-10-07, and the issuer confirmed each date.
The scored window runs from the 2026-10-07 close to the 2026-10-08 close.

| # | Ticker | Company | impact_sum (key) | Above floor 2.8 | impact_scaled (v3, not the key) | abs_move | p_up | Anchor | Date grade | Analyst band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FTG | Firan Technology Group (TSX, $1.68m/day) | **−1.00** (p50) | no | −0.55 (p40) | 5.5 | 45 | register | confirmed | none |
| 2 | RCH | Richelieu Hardware (TSX, $1.47m/day) | **−1.70** (p65) | no | −0.72 (p47) | 4.5 | 42 | register | confirmed | 1–2 |

| Funnel | Count |
| --- | --- |
| Scanner rows | 2,498 |
| Candidates in window | 8 |
| Scheduled today | 3 |
| Eligible (≥ $100k/day, not filing-only, not disputed) | 2 |
| Hunted / rankable | 2 / 2 |

`selection.method`: all 2 eligible names, at or under the cap of 20. No random draw was
needed (seed `ca-2026-10-07`). The only drop was YAY (THS Maple, TSXV, vendor_only), at
$1,204/day, far below the turnover floor.

## What drives the top and the bottom

- **FTG (top, −1.00).** The largest finding is −0.8 on the reported quarter. On the Q2
  call, management guided Q3 seasonally softer, with about one week (~8%) of production
  lost. The hunter's own arithmetic puts EPS near C$0.15–0.17 against a C$0.18 bar.
  Source: https://www.webull.com/news/15219089896776704 (Q2 2026 call transcript).
  - Partial offsets: first deliveries on two classified defence programmes (+0.5, TTM's
    A&D read-through, https://www.sec.gov/Archives/edgar/data/0001116942/000119312526336163/d132953dex991.htm)
    and a weaker Canadian dollar (+0.4, Bank of Canada).
  - **The bar is single-sourced** (TipRanks only; its USD 0.13 is the same estimate
    converted), so every size is capped small.
- **RCH (bottom, −1.70).** The largest finding is −1.5. Reaching the EPS bar of
  C$0.46–0.48 needs a Q3 EBITDA margin of about 11.8–12.0%. Richelieu's own disclosures
  show tariff pass-through diluting margin by 20–30bp a year (Q2 10.6% against 10.8%), so
  the hunter builds EPS of about 0.44–0.45. Consensus has missed in 3 of the last 4
  quarters, and the last two misses traded −8.9% and −4.2%.
  Source: https://www.newswire.ca/en/releases/archive/July2026/09/c6050.html (Q2 FY26 release).
  - The margin-target finding (−0.8) rests on the same margin evidence. The hunter says
    so, so the two are not independent.
  - This is Richelieu's first after-close release; until now it released mid-morning on
    Thursdays.

**Not ranked:** none. Both hunts confirmed the event from the issuer's own notice.

## The items this note carries every time

- **Anchor arms: options 0 · register 2.** The seal ran inside the session, at 18:34 UTC
  (14:34 ET). The zero on the options arm is therefore NOT a timing artefact: neither name
  has a listed Montréal Exchange chain, which is normal below $25m a day. This is a
  register-arm day, and `ca_resolve.py` ranks the two arms apart.
- **Calendar reconciliation:** confirmed 2 · agreed 0 · wsh_only 0 · vendor_only 1 ·
  disputed 0. `moved_off_target_by_wsh`: none. Both hunted names are WSH CONFIRMED, and the
  issuer announced them itself. RCH's notice is dated 2026-10-01; FTG's is dated 2026-09-29.
- **Short register:** sealed `register_business_date` **2026-10-06**. FTG is at 1.28% (2.7
  days to cover) and RCH at 2.24% (14.0 days to cover). `short_change_pct_pts` is **null on
  both** and will keep coming back null. See defect 1 below.
- **Consensus EPS:** none in the baseline, as always. Both hunters sourced the bar
  themselves, and neither came back `bar: unsourced`.
  - FTG: C$0.18, one source, sizes capped.
  - RCH: C$0.46–0.48, from WealthAwesome plus a Yahoo/Investing snippet, both resting on
    the same 2 analysts.
  - Neither emitted large findings against a weak bar.
- **One bilingual pass:**
  - FTG `language_note`: "Not a Quebec issuer (Toronto, Ontario), so English sources only."
  - RCH (Montréal): the French CNW notice and French search (Les Affaires, La Presse,
    Zonebourse) added nothing the English sources did not already carry.
  - No `pre_local` was asked for. `pre_lessons` equals the final set on both names,
    because `researcher_canada/LESSONS.md` is still empty.
- **Filing-only screen:** **0 dropped** today. None of the 3 scheduled rows was flagged
  `filing_only`.
- **Analyst bands:** FTG `none` (TMX shows 0 analysts) and RCH `1-2`. Both sit in the
  thin-coverage band that is this stage's thesis.
- **Conviction floor:** 0 of 2 clear 2.8. Over the whole US sample, the sign below the
  floor was a coin flip.
- **Lean:** the baseline lean is −0.39 for FTG and +1.53 for RCH. RCH's hunter reports
  that its lean comes almost entirely from a short-squeeze prior. It does not credit that
  prior at 2.24% short with thin turnover.
- **Vendor stack:** the TMX tape, register, calendar and news archive all answered, so
  this was not an outage. Yahoo did not answer the CAD/USD request, and the FX rate came
  from the Bank of Canada's daily average.

## Defects found this run (not patched here)

1. **The register snapshot cannot produce a change.** Each file in
   `researcher_canada/analysis/short-register/` stores only that day's sealed names:
   AGF.B on 09-22, BRC on 09-25, FTG and RCH today. A change therefore computes only when
   the same issuer is sealed twice, roughly once a quarter. The same gap means the files
   cannot answer whether the feed refreshes daily. `ca_priced_in.py` still prints
   "change in short interest is computable". The fix is to snapshot the whole register,
   not the day's names.
2. **`publish.sh` does not commit that snapshot.** It was left untracked, and it was
   committed by hand (`4e85f81`).
3. RCH's hunter downloaded the Q2 MD&A PDF through the TMX filing index, and
   `eu_pdftext.py` returned garbled text. The hunter did not use it.

**What this day does not establish:** anything about the hunt or about the anchor-arm
comparison. There are two names, both on one arm, both below the floor, and nothing has
resolved in Canada yet. One day is not a result.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
