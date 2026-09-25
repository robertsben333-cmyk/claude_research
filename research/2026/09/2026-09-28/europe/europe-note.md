# Stage EU — Europe ranking for Monday 2026-09-28

Sealed Fri 2026-09-25, 13:39–14:00 UTC, while the European markets were **still trading**.
Every sealed spot and run-up below is an **intraday price, not a close**. The realised move
is measured from daily bars by `eu_resolve.py`, never from the sealed spot.

## Answer first

**Nothing clears the conviction floor of 3.0 points.** The largest key is LIKE at +2.00, so
this is a day of small numbers. Across the whole US sample the sign below the floor was a
coin flip. The ranking key is `impact_sum`, as `edge-scores.json` reports it.

| # | name | market | session | `impact_sum` | pre-lessons | lean | anchor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LIKE Likewise Group | uk | bmo (confirmed) | **+2.00** | +2.0 | −0.54 | truncated zero |
| 2 | TLW Tullow Oil | uk | bmo (confirmed) | **+0.90** | +1.0 | +1.15 | **FCA 2.45%** |
| 3 | PKP PKP CARGO | pl | **amc** (sealed as bmo?) | **−0.30** | −0.2 | +0.18 | none (no register) |
| 4 | EQS Equasens | fr | bmo (confirmed) | **−1.00** | −1.5 | +0.61 | truncated zero |
| 5 | OSE OSE Immunotherapeutics | fr | amc | **−1.30** | −2.0 | +1.38 | truncated zero |
| — | SEE Seeing Machines | uk | — | not ranked | 0 | +0.56 | truncated zero |

**Top name, LIKE (+2.0).** The main finding is +3.0, on guidance. The house broker's FY26
revenue forecast of £174.1m implies second-half revenue about 2% below last year. Against
that, July was +23.9%, the year to date is +18.3%, and the largest UK competitor, Headlam,
entered administration on 8 Sep. Monday's interim is Likewise's first statement since then.
The main source is the 28 Jul fundraise RNS:
<https://www.investegate.co.uk/announcement/rns/likewise-group--like/proposed-fundraising-to-raise-up-to-29-2-million-/9692164>.
A −1.0 finding on H1 profit conversion offsets part of it; Likewise missed on profit in
Nov 2025. The hunter itself says the Headlam story is partly priced: the stock rose 10.8%
on 1 Sep on about 11x its normal volume.

**Bottom name, OSE (−1.3).** The main finding is −1.0, on financing. In June the company put
its cash runway at the end of December 2026. That runway assumed about €19.3m from the IRIS
equity line, priced at €4.83 a share, and the stock is now €2.31. The remaining warrants are
worth about €6m. The June–August draw-downs appear only in the French monthly share-count
filings. The hunter calls most of this priced (the stock is −50% since the deal) and the
sign open. A −0.3 finding on the ARTEMIA futility read slipping into Q4 is the rest.

**Not ranked: SEE, a phantom date.** Management told Proactive on 24 Sep that the FY26
audited results are now expected "by the end of November alongside completion of the
longer-term extension" of the Magna convertible notes
(<https://www.proactiveinvestors.com/companies/news/1099046/seeing-machines-buys-time-on-magna-financing-as-automotive-momentum-builds-1099046.html>).
No Notice of Results RNS was filed, although one preceded the finals in each of FY23–FY25.
The vendor's 2026-09-28 row is wrong. Because SEE is a UK name, `eu_resolve.py` can
confirm the absence against Investegate.

## Sessions: what was assumed and what was found

- Four names were sealed `session_unresolved` (defaulted bmo): EQS, PKP, SEE and TLW. The
  hunters settled three of them:
  - **TLW is bmo**: the 5 Aug RNS dates the interims to 28 Sep, and every Tullow results
    RNS went out at 07:00.
  - **EQS is bmo**: the issuer's agenda reads "28/09/2026 : Résultats 1er semestre 2026
    (avant bourse)" ("before market").
  - **PKP is amc, not bmo.** Its periodic reports go out after the 17:00 Warsaw close:
    17:08, about 21:07 and 00:09 on the last three. The reaction window is therefore close
    09-28 → close 09-29. **Read `move_amc_window_pct` for PKP at resolve.** The baseline
    stays sealed as it was.
  - SEE is moot (see above).
- OSE is amc from the vendor flag, and the issuer's page confirms it. Its window is also
  09-28 → 09-29.
- LIKE is bmo from the vendor flag and the Notice of Results.

## What the day is made of

- **Selection:** "all 6 eligible names (at or under the cap)". 15 scheduled, 6 eligible
  above the $200k/day floor, 6 hunted. There was no random draw, because the day sat under
  the cap of 20.
  - `eligible_by_market` and `by_market` are the same: uk 3, fr 2, pl 1, and 0 for de, se,
    dk, no, fi, it and es. Italy had 2 scheduled and neither cleared the floor.
- **`market_concentration`:** the UK is 50% of the day, spread over 3 markets. The day is
  half one market, so any pooled statement is half a UK statement.
- **Spain and Poland:** 1 name, PKP. It has no positioning anchor, so its lean is the
  run-up and therefore the free control. Its print can never be confirmed or killed after
  the fact; the hunter's check of the issuer's own calendar is the only confirmation it
  will get. **Germany:** 0 names.
- **Options:** null in all ten markets. Europe runs in the anchor-less regime, which
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45.
- **Short registers:** the UK (FCA, as of 2026-09-24, 420 issuers) and France (AMF, as of
  2026-09-21, 74 issuers) both resolved. Poland has no register.
  - **Only 1 of 6 names carries `anchor_covered: true`: TLW, at 2.45% (+0.01pp).**
  - LIKE, SEE, EQS and OSE were read and are not named. Their 0.0 is the 0.5% truncation
    floor, not a measurement.
- **The UK register only reads because of a same-day fix.** The FCA renamed its date
  column to "Position date (of latest position date notified)". `eu_positioning.load_uk()`
  looked the column up by its exact old name, and the whole register failed with a
  `NoneType` comparison. Its string compare of DD/MM/YYYY dates also ordered them wrongly.
  - The first seal had all three UK names as `register_unreadable`.
  - The loader was fixed and the day was **re-sealed before any hunter read a baseline**.
  - UK baselines from 09-22 to 09-25 were checked and were not affected.
- **`history.basis`:** observed (`observed_rns`) for LIKE, SEE and TLW. **Estimated from
  cadence** for EQS, OSE and PKP. An estimate is a scale, not a record of dates. A cadence
  prior is how TRT got ranked, traded and never reported.
- **The lean's weights** are priors borrowed from the US runs and have been measured
  nowhere in Europe.
- **`lean_vs_free_control_rho`:** no real European run has resolved. The only resolved
  files, 09-16 and 09-17, are the synthetic validation runs, so there is no per-market
  figure to quote.
- **`pre_lessons` control:** 6 names froze a draft, and the lessons file moved 4 of them
  (TLW, PKP, EQS and OSE).
- **Language pass:** 0 names, which is expected. The `pre_local` freeze was retired on
  2026-09-22.

## Language notes worth keeping (prose, ranks nothing)

- **EQS:**
  - The E-CONNECT division's 36% margin base and the component-cost warning are only in
    the French segment tables.
  - The size of ASCA, the subsidiary whose site burned, comes only from the French company
    register: €28.4m revenue and €9.67m operating profit, via pappers.
- **PKP:** the session timing, the per-operator UTK volume shares, and the "odwrócenie
  odpisów" (reversal of write-downs) behind the Q2 2025 profit are all Polish-only.
- **OSE:** the IRIS draw-downs appear only in the French monthly share-count filings.
- **UK names:** the "local" half is about where the sources sit, not language. For LIKE,
  the Headlam closures came through the domestic trade press. For SEE, the load-bearing
  fact was in a Proactive interview and not in the RNS.

## Critical read

- **LIKE:** the biggest number of the day, and one broker is the whole bar. The upside
  rests on an arithmetic gap in a stale forecast. That is exactly the kind of thing a
  single house broker revises quietly, so the hunter's own caveat is fair.
- **TLW:** both findings land on one guidance line, and both are mostly Brent. Brent fell
  about 7% on 25 Sep, and the weekend oil move will dominate Monday. +0.9 is small for
  good reason.
- **EQS:** the finding rests on the hunter's own model of segment data against an
  unsourced H1 bar. On sourcing, the ASCA-fire offset is the better-evidenced of the two
  findings.
- **OSE and PKP:** both are equity-financing stories whose real resolution sits outside the
  window: the IRIS runway and a larger raise for OSE; the 15 Oct creditors' council and the
  12 PLN rights issue for PKP.
- **One day is not a result.** Five rankable names cannot say anything about ranking.
  ρ on five names is barely informative.

**UK resolve timing:** Yahoo's `.L` closes lag one session and `.PA`/`.WA` lag more, so
resolve this run from Wednesday 2026-09-30 at the earliest. OSE and PKP need the 09-29 close.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
