# Stage EU — Europe ranking for 2026-10-20

**The answer: no name clears the 2.8 conviction floor. Every `impact_sum` value is small, from
+0.90 to −0.70. The panel selected one name, BMAX (Byggmax), on the short side, 3 of 4 judges.**
Eleven names were ranked in six markets: Sweden 5, Germany 2, and one each from the UK, France,
Denmark and Spain. All are sealed for Tuesday 20 October. EXS (Exsitec) and LIME (Lime
Technologies) tie at the top at +0.90. BMAX is at the bottom at −0.70. Every hunter found
the period's numbers unreleased and no profit warning out, and none found a decisive fact the
price does not already hold.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Monday 2026-10-19 at about 13:50–14:00 UTC, while the European markets were still
trading, so every sealed spot is an **intraday price, not a close**. The realised move is
measured from daily bars: close(2026-10-19) → close(2026-10-20), except DB1 (see below).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | EXS | Exsitec Holding | **+0.90** (p60) | no | +0.56 | 7.0 | 54 | bmo. Issuer invitation: 20 Oct 08:00 CEST |
| 2 | se | LIME | Lime Technologies | **+0.90** (p60) | no | +0.45 | 7.5 | 53 | bmo. Issuer invitation: 07:50 |
| 3 | de | DB1 | Deutsche Börse | **+0.20** (p19) | no | +0.18 | 3.0 | 53 | **amc, not the sealed `bmo?`.** Issuer calendar: ~19:00 CEST on 20 Oct |
| 4 | es | ENG | Enagás | **+0.20** (p19) | no | +0.08 | 2.0 | 52 | bmo. Issuer OIR of 14 Oct: "before the opening" |
| 5 | de | MUM | Mensch und Maschine | **0.00** (p5) | no | +0.20 | 5.0 | 52 | sealed `bmo?`. The hunter confirmed bmo: EQS releases 08:54–08:59 CET |
| 6 | se | UPSALE | Upsales Technology | **0.00** (p5) | no | +0.60 | 7.5 | 54 | bmo. Issuer release: 08:30 CEST |
| 7 | uk | BPM | B.P. Marsh & Partners | **−0.35** (p31) | no | −0.30 | 3.0 | 45 | sealed `bmo?`. The hunter confirmed bmo: notice of results, call 09:00 BST, every results RNS 07:00 |
| 8 | dk | EMBLA | Embla Medical | **−0.40** (p34) | no | −0.20 | 5.0 | 48 | bmo. Issuer notice: 07:00 CET |
| 9 | fr | OVH | OVH Groupe | **−0.50** (p41) | no | −0.44 | 11.0 | 48 | bmo. FY releases at 05:00 UTC |
| 10 | se | SCST | Scandi Standard | **−0.50** (p41) | no | −0.27 | 4.5 | 47 | bmo. Issuer invitation: 07:30 CET |
| 11 | se | BMAX | Byggmax Group | **−0.70** (p53) | no | −0.75 | 7.5 | 45 | bmo. Inferred from every prior report going out at 07:45 CET; no timestamped notice |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by Opus 5.5:
scale, not rank. EXS/LIME, DB1/ENG, MUM/UPSALE and OVH/SCST each tie, and the scorer's order
inside a tie carries no information.

**DB1's sealed window is wrong.** Deutsche Börse's own financial calendar puts the Q3
statement at about 19:00 CEST on 20 October, after the 17:30 Xetra close, with the analyst
call on 21 October. So the reaction is in close(20 Oct) → close(21 Oct), not the sealed bmo
window, which ends before the release. The hunter's `session_check` opens with "amc" and cites
the issuer URL, and all four judges sized the amc window. Check what `eu_resolve.py` takes
for this row before trusting it.

**Pre-released, or a guidance event (`already_public` / `new_in_release`):**
- **Nothing was pre-released on any of the eleven.** No profit warning, trading update with
  the period's numbers, or Ad-hoc-Mitteilung was found since each name's last report.
  BPM's 22 Sep trading update gave activity but no NAV.
- **Guidance events, the likelier large moves:**
  - **OVH:** the first FY27 guide, probably with the 2026–2030 plan targets. The stock moved
    −20.3% on last year's FY results and is down 21.5% in 20 days.
  - **MUM:** Mensch und Maschine has given its next-year targets in the Q3 release three
    years running.
  - **DB1:** a raise is already the bar, because analysts sit above guidance on every FY26 line.
  - **ENG:** possibly the first 2027 regulated-revenue figure under the final CNMC framework.
  - **EXS:** the Amesto synergy figure promised "during the third quarter".
- **No guidance at all:** Byggmax, Scandi Standard and Lime give none, so their releases are
  new numbers only.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four members ran on their own pinned `-intl-` agents, with no fallback, and each
  covered 11 of 11 packs.
- The selection rule for this market is `consensus`: a name is selected when 3 of 4 judges
  put it in their own top 20%.
- Each judge's top 20% starts at Opus 5 |1.80|, Opus 5.5 |1.00|, Sonnet 5.5 |1.20| and
  Fable 5.1 |1.33|, measured on 55 live sizes each.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BMAX | **yes** | 73 | short | 24 | 84S* | 89S* | 31S | 89S* | 3 | −1.34 | −0.70 |
| 2 | OVH | no | 9 | short | 50 | 84S* | 38L | 27S | 36L | 1 | −0.00 | −0.50 |
| 3 | LIME | no | 57 | long | 20 | 71L | 80L* | 51L | 27L | 0 | +0.75 | +0.90 |
| 4 | EXS | no | 56 | long | 4 | 54L | 64L | 53L | 54L | 0 | +0.64 | +0.90 |
| 5 | EMBLA | no | 44 | short | 11 | 58S | 44S | 27S | 46S | 0 | −0.46 | −0.40 |
| 6 | SCST | no | 29 | short | 14 | 9S | 49S | 31S | 27S | 0 | −0.37 | −0.50 |
| 7 | MUM | no | 22 | short | 20 | 31S | 9L | 20S | 46S | 0 | −0.32 | 0.00 |
| 8 | BPM | no | 23 | short | 3 | 22S | 26S | 18S | 26S | 0 | −0.27 | −0.35 |
| 9 | UPSALE | no | 7 | long | 29 | 22L | 40S | 9L | 36L | 0 | +0.20 | 0.00 |
| 10 | DB1 | no | 16 | long | 9 | 9L | 29L | 18L | 7L | 0 | +0.19 | +0.20 |
| 11 | ENG | no | 6 | long | 3 | 6L | 6L | 11L | 4L | 0 | +0.08 | +0.20 |

Each member's figure is its percentile 0-100 against its own live range, with L for long and S
for short. A `*` marks a member's own top 20%.

**BMAX, selected short (Opus 5, Opus 5.5 and Fable 5.1 in their own top 20%).**
- **The evidence the members name:**
  - SCB's Swedish retail series for building and hardware stores (SNI 47.52) slowed from
    +9.3% y/y in Q2 to +6.8% in July and +3.9% in August.
  - Byggmax Sweden has trailed that series by 2.9, 5.6 and 6.9 points over the last three
    quarters.
  - Carried forward, that gives group sales of about SEK 2,000–2,035M against a 2-analyst
    consensus of SEK 2,049M (+5.1% y/y).
  - The comparable miss in Q3 2025 cost −15.7% on the day.
  - Source: the SCB database,
    https://api.scb.se/OV0104/v1/doris/sv/ssd/HA/HA0101/HA0101B/DetOms07N, quoting "butiker
    för bygg-, järn- och vvs-varor samt färger och glas" (stores for building, hardware and
    plumbing goods, and paint and glass).
- **The strongest case against:**
  - The main evidence is a sector proxy, not a company number.
  - The gross margin has risen y/y for three straight quarters and could carry EPS to the
    3.68 bar even on lower sales.
  - Clas Ohlson's September (organic +12%) says August was not the whole quarter.
  - The single EPS estimate was raised last week, and Sonnet 5.5 sized the name at only
    −0.44 for exactly these reasons.

**Where the panel and the hunters disagree most:**
- **OVH:** Opus 5 is 84S* (−1.98, on the FY27 capex and free-cash-flow guide), while Opus 5.5
  and Fable 5.1 lean long. The spread is 50, the widest of the day, and the mean nets to
  panel_pct 9. The judges agree it will move a lot (abs ~10–11) and disagree on the sign.
- **MUM:** Opus 5.5 leans long (9L) against the hunter's 0.00 and the other three judges'
  mild short.
- **UPSALE:** the hunter's `impact_sum` is 0.00, but three judges lean long and Opus 5.5
  short.
- **Not applicable today:** no name sits above the conviction floor, so there is no
  above-floor name the panel failed to select.

**What these numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- Certainty (`p_up`) is recorded and decides nothing.
- Each member's scale still rests heavily on the frozen E-P seed: 55 live sizes, against the
  roughly 200 this market needs.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing
  about this market's panel is established.

## The finding driving the top and the bottom

**Top: EXS +0.90, LIME +0.90.**
- **EXS:** the largest finding is +0.8. Management said in the Q2 report it would describe
  the Amesto cost synergies "during the third quarter", Q3 is the first full quarter with
  Amesto consolidated, and no synergy number is out yet. No Q3 consensus exists anywhere, so
  every size is capped. Source: the issuer's Q2 report on the Nasdaq Nordic feed (URLs in
  `hunts/EXS.json`).
- **LIME:** two arithmetic findings put reported ARR at or above the 10–11% bar set by Pareto
  and SB1:
  - **SEK translation, +0.7.** EUR/SEK averaged 11.24 in September against 10.96 in June, and
    about 31% of revenue is outside Sweden. Source:
    https://query1.finance.yahoo.com/v8/finance/chart/EURSEK=X?range=2y&interval=1d.
  - **Easy comparison, +0.5.** Q3-25 added only +9.1 MSEK of ARR.
  - **The offset, −0.6.** The CEO's July warning on order intake.
  - **The bar** was found only in Swedish copy: Pareto, "ARR väntas växa 10 procent" (ARR is
    expected to grow 10 percent),
    https://www.borskollen.se/nyheter/28/pareto-hojer-riktkursen-for-lime-till-275-kronor-upprepar-kop.

**Bottom: BMAX −0.70.** The −2.0 SCB sector-slowdown finding described in the panel section,
partly offset by +0.8 for the gross margin and +0.5 for the Clas Ohlson read.

## Names that could not be ranked

None: all 11 of 11 are rankable.

## What must be said every time

- **Selection:** `selection.method` was "all 11 eligible names (at or under the cap)", seed
  `eu-2026-10-20`.
  - 23 rows were scheduled; 11 cleared the $100k turnover floor and 12 were dropped.
  - `by_market`: se 5, de 2, uk 1, fr 1, dk 1, es 1; no, fi, it and pl 0.
  - No random draw was needed because the day was under the cap of 20.
- **Concentration:** the largest market is Sweden at 45.5% (5 of 11), across 6 markets. That
  is a correlated exposure the scorer cannot see, so a pooled statement about this day is
  partly a statement about Swedish small caps.
- **Calendar sources:**
  - **Vendor:** TradingView, for every market.
  - **UK:** the RNS calendar read and confirmed BPM.
  - **Issuer calendars, all read:** EQS (added DB1), Inderes and Nasdaq Nordic (SE/DK/FI),
    Euronext Oslo (NO) and bankier (PL).
  - **Yahoo's firm dates read `unavailable` on all ten markets** ("quote endpoint failed on
    every batch"), the same as the previous two runs.
- **`session_unresolved` at seal:** BPM, DB1 and MUM.
  - BPM and MUM were confirmed bmo by the issuer's own notices.
  - **DB1 is amc** (see above).
  - BMAX's 07:45 is inferred from pattern, not a notice.
- **Option anchor:** `options` is null in all ten markets. Europe runs in the anchor-less
  regime that priced at ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers resolved:** uk (as of 2026-10-16), de (2026-10-16), fr (2026-10-15) and
  se (2026-10-19).
  - **dk read as_of 27-08-2026 in the baseline.** The EMBLA hunter found the live register
    current, but it lists Danish ISINs and Embla's is Icelandic (IS0000000040), so Embla's
    0.0 is not a measurement of this issuer.
  - es has no register at all.
- **Anchor coverage: only BMAX carries `anchor_covered: true` (1 of 11; FI aggregate 0.28%,
  unchanged).** The other ten read a truncated zero or no register at all, which is not an
  anchor.
- **Weak legs:**
  - **Spain or Poland: 1 name, ENG.** It has no positioning anchor, its lean is the run-up and
    therefore the free control, and it can never be confirmed or killed after the fact.
  - **Germany: 2 names, DB1 and MUM.** They cannot reach `event_occurred: false` either.
  - **France (OVH)** cannot reach it either since 2026-09-28.
- **`lean_vs_free_control_rho`:** the previous resolved European run (2026-10-08) reads 1.0
  for uk on 3 names and nothing for de/fr/fi on one name each. That is not a measurement. The
  lean's weights are priors borrowed from the US runs, measured nowhere in Europe.
- **`history.basis`:** only BPM is observed (`observed_rns`). The other ten are
  `estimated_from_cadence`, a scale and not a record of dates.
  - Several hunters found the estimated dates wrong, notably EMBLA, whose real recent prints
    were 2025-10-21, 2026-02-03, 2026-04-28 and 2026-07-21.
  - The estimated medians understate the scale: OVH 5.83% estimated against −20.3% and −16.7%
    on real report days, and EXS 2.34% against a ~5.5% observed median.
- **Conviction floor:** no name sits above 2.8. Over the whole US sample the sign was a coin
  flip below the floor.
- **Resolution timing:** the five Swedish names and EMBLA must be resolved within about a week
  (the Nasdaq Nordic feed window), or their rows resolve null for ever.
- One day is not a result.

**`language_note` highlights (prose, nothing ranks it):**
- **Swedish sources** carried the only stated bar for LIME (Pareto, SB1) and UPSALE (Kalqyl),
  the SCB series behind BMAX, and SCST's owner contest (EFN on Grupo Lusiaves, Lantmännen and
  Qviberg, plus the FI insider register).
- **French sources** for OVH carried the TP ICAP Midcap Sell rating, the server price grid
  (+28% / +51% on renewals) and the explicit capex raise from 30–32% to 33–35%.
- **Spanish sources** for ENG: the CNMC note is the primary source for the 6.46% rate.
- **German sources** for MUM carried the CFO interview's €2.5m figure and LBBW's estimates.
- **DB1, BPM and EMBLA:** the local-language sources added nothing.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
