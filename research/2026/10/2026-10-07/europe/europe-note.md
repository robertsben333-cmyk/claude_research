# Stage EU — Europe ranking for 2026-10-07

**Answer first: two names, and neither hunt found anything the market has not priced.
Both sit far below the 2.8 conviction floor. Read this as a day with no signal.**

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`). Sealed 2026-10-06, about
13:50 UTC, while the European markets were still open. So the sealed spots are
**intraday prices, not closes**. The realised move will be measured from daily bars,
close(2026-10-06) to close(2026-10-07).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | uk | NET | Netcall plc | **+0.10** (p8) | no | +0.12 | 3.0 | 52 | bmo, **session_unresolved** in the baseline |
| 2 | se | INDU_A | Industrivärden AB A | **+0.00** (p4) | no | +0.00 | 1.6 | 50 | bmo (release expected inside the session) |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no
floor applies to it.

## Top name: NET, +0.10

The largest finding is **+0.5 on `guidance`**. The only genuinely new line expected in the
release is a qualitative FY27 current-trading statement.

- The 2026-07-21 trading update already gave the year's numbers: revenue £57.7m, adjusted
  EBITDA £12.1m, net cash £21.0m. All three were in line with company-stated consensus.
  Source: https://www.investegate.co.uk/announcement/rns/netcall--net/fy26-trading-update/9678454
- The same update reported total ACV +27% and a "record" FY27 pipeline. Against LSEG FY27e
  revenue of £67.2m (quoted by Edison:
  https://www.edisongroup.com/research/fy26-trading-statement/BM-3766/), that makes an "in
  line" outlook statement more likely than a cautious one.

Two findings pull the other way:

- **BGF is selling.** It cut its stake from 4.94% to 3.99%, crossing on 2026-09-28: −0.3.
- **The September run-up may be read-across, not anticipation.** It coincides with
  Accel-KKR's bid for AIM peer Eleco, but that link rests on the dates lining up, not on any
  document: −0.2.

The date is confirmed by the issuer's Notice of Results RNS:
https://www.investegate.co.uk/announcement/rns/netcall--net/notice-of-results/9795279.
That notice gives no release time. Every earlier Netcall results RNS was stamped 07:00, so
bmo is the expected session but **not a confirmed one**.

## Bottom name: INDU_A, 0.00, no findings

Industrivärden is an investment company. Its NAV can be rebuilt every day from public
holdings and prices. The hunter's rebuild matched the reported NAV to within about 1 SEK at
30 June and at 31 August, and puts 30 September at about 516 SEK per share.

The only trade during the quarter, about 351 MSEK of Handelsbanken A, was disclosed on
2026-07-21: https://www.placera.se/telegram/shb-industrivarden-kopt-2-5-mln-aktier-20260721.
The date is confirmed by the issuer's own calendar:
https://www.inderes.se/releases/rapporttillfallen-och-arsstamma-i-industrivarden-2026.
Earlier interim reports were released at 09:00–10:00 CEST, inside the window.

The hunter also checked FI's insider register for undisclosed portfolio trades. That check
was **inconclusive**: the queries returned no rows at all, which is not the same as a clean
result.

## Names that could not be ranked

None. Both eligible names were hunted and scored. Two names cannot meaningfully be ranked
against each other, so this is a record and not a ranking.

## What this day is, and what it is not

**Selection**
- Method: "all 2 eligible names (at or under the cap)". 7 were scheduled and 2 cleared the
  $100k/day floor.
  - `by_market`: uk 1, se 1, every other market 0.
  - No random draw was needed. Had there been more eligible names than the cap, the draw
    would have been random among them.
- `market_concentration`: the largest market is 50% of the day, across 2 markets.
- Calendar sources: Netcall's date was confirmed by the issuer's RNS. Industrivärden's
  appears in the vendor feed, Inderes and the Nasdaq Nordic financial calendar.
  - All ten markets' calendars read. None was `unavailable` and none was `market_closed`.

**Anchors and instrumentation**
- **`options` is null in all ten markets.** Europe runs in the anchor-less regime that
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45.
- **Short registers resolved for both markets** (UK FCA: 424 rows; SE FI: 337 rows).
  **`anchor_covered: true` on 0 of 2 names.** Neither issuer appears on its register, so
  both read as truncated zeros under the 0.5% disclosure threshold, not as measured
  positions.
- **Spain/Poland: 0 names. Germany: 0 names.** So no name today is structurally unable to
  be confirmed or killed afterwards.
  - **Sweden can reach `event_occurred: false` only inside the Nasdaq feed's roughly
    12-day window.** Resolve this run within a week.
- `history.basis`:
  - NET is `observed_rns`.
  - **INDU_A is `estimated_from_cadence`.** That history is a scale, not a record of dates.
- `lean_vs_free_control_rho`: no resolved European run carries it yet. The 2026-10-01
  resolution had one usable row and computed no statistics.
- The lean's weights are priors borrowed from the US runs. They have been measured nowhere
  in Europe.

**Release timing**
- `already_public`: **both names had largely pre-released the period.**
  - NET's FY numbers came out on 2026-07-21.
  - INDU_A's NAV can be computed daily and its August NAV was published on 2026-09-01.
- `new_in_release`:
  - NET: the qualitative FY27 outlook statement.
  - INDU_A: nothing material, because an investment company gives no guidance.
  - Neither name faces a likely numeric guidance change.

**Conviction**
- Neither name clears the conviction floor. Over the whole US sample the sign was a coin
  flip below it.

**Language and sources**
- NET (`language_note`): the UK domestic sources (RNS/TR-1) added the BGF disposal. They
  also showed that Liontrust's move to 5.455% was an administrative fund transfer, not a
  purchase.
- INDU_A (`language_note`): the Swedish filings are bilingual and added nothing. Only the
  Swedish press carried the record premium-to-NAV argument. That is a one-year valuation
  view, sized at 0.

**One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
