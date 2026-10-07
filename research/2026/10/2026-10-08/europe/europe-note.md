# Stage EU — Europe ranking for 2026-10-08

**The answer: six names, and no hunt found anything decisive. None of the six is near the
2.8 conviction floor; the largest is TSCO at −1.20. Treat this as a day with no signal.
One sealed window is wrong: ALLIX reports after the close, not before the open (see
below).**

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on 2026-10-07 at about 13:45 UTC, while the European markets were still trading, so
every sealed spot is an **intraday price, not a close**. The realised move is measured from
daily bars, close(2026-10-07) to close(2026-10-08), except for ALLIX.

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | uk | FAN | Volution Group plc | **+0.30** (p18) | no | +0.18 | 4.5 | 52 | bmo, confirmed (07:00 London) |
| 2 | uk | NFG | Next 15 Group plc | **+0.20** (p14) | no | +0.13 | 6.5 | 51 | bmo, confirmed (07:00 BST, Notice of Results) |
| 3 | de | SZU | Südzucker AG | **+0.20** (p14) | no | +0.21 | 3.5 | 53 | bmo **by cadence only**, `session_unresolved` in the baseline |
| 4 | fi | ADMCM | Admicom Oyj | **−0.30** (p18) | no | −0.48 | 6.0 | 46 | bmo, confirmed (about 08:00 EET) |
| 5 | fr | ALLIX | Wallix Group SA | **−0.40** (p22) | no | −0.55 | 5.5 | 45 | **amc, not the sealed bmo**: `session_unresolved` in the baseline, the hunter found it is after the close |
| 6 | uk | TSCO | Tesco PLC | **−1.20** (p54) | no | −0.50 | 5.0 | 45 | bmo, confirmed (07:00 London) |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank.

## The ALLIX window is wrong in the seal

ALLIX was sealed `bmo`/`session_unresolved` for 2026-10-08. The hunter found three sources
saying it reports **after the close** that day:

- the company's 16 July release ("Prochaine publication : Résultats semestriel 2026, le
  8 octobre 2026");
- ABC Bourse's calendar ("Résultats du 1er semestre — Après clôture");
- the AMF timestamps of the two previous half-year releases, 18:30 and 18:45 Paris.

The reaction therefore lands in **close(10-08) → close(10-09)**. The sealed window contains
no event. The baseline stays sealed. The hunter's `session_check` opens with `amc`, so the
resolver should measure that window, and the post-mortem must check that it did.

## Bottom name: TSCO, −1.20

The largest finding is **−0.8 on market share**. Worldpanel shows Tesco losing share for
four reports in a row: 27.8% against 28.1% a year ago, with sales up about 1.7–1.8% while
the market grew about 2.5%
(https://www.globalbankingandfinance.com/uk-grocery-inflation-edges-higher-over-last-month-worldpanel/).
UK retail-investor previews (HL, IG) still describe the half as continued share gains.

There is also **−0.5 on guidance**, with a wide range (−3.5 to +3.0). Grocery inflation has
eased to about 2.1–2.3%, and the company-compiled consensus of £3.25bn sits in the top half
of the £3.0–3.3bn guide. A **+0.1 buyback** finding offsets a little: £200m of the £750m
programme remains.

No H1 profit consensus was found, so `print_vs_bar_pct` is capped small. The FCA short
position is 0.21% and being covered.

## Top name: FAN, +0.30

FY26 was pre-released on 23 July (adjusted EPS of about 38.0p, 4% above consensus), so the
move is in the first FY27 outlook. The findings are all peer or macro read-throughs and
roughly cancel:

| finding | size |
| --- | --- |
| Genuit's UK ventilation orders up 6% (https://www.investegate.co.uk/announcement/rns/genuit-group--gen/half-year-report/9714341) | +0.4 |
| Systemair Nordic organic growth +8% | +0.4 |
| UK construction PMI, housing at 37.6 | −0.4 |
| Input-cost inflation | −0.2 |
| getAir acquisition (largely priced) | +0.1 |

## The other three

- **NFG +0.20.** The H1 FY27 numbers are new on the day. The real unknown is an update on
  the Mach49 arbitration, which carries a going-concern material uncertainty. It is sized at
  0.0 with a range of ±12, because it raises the size of the move, not its sign.
  Richard Griffiths has raised his stake from 11.05% to 15.05%, which is +0.3 and mostly
  priced.
- **SZU +0.20.** The half-year was pre-released by a MAR ad-hoc on 28 September (H1
  operating EBITDA €303m, guide narrowed to €540–680m), so `print_vs_bar` is 0. Two findings
  about the first word on the 2026 campaign roughly cancel:
  - a poor beet crop, "historische Missernte" (VSZ): −0.3;
  - ICE raw sugar up 18% since 30 September: +0.5.
- **ADMCM −0.30.** The bar is Inderes's printing of the 4-analyst Bloomberg consensus:
  revenue €9.6m, EBITDA €3.7m. The largest finding is −1.0 on guidance. The ARR guide floor
  needs +€1.8m in H2, after ARR *fell* in H1, and growth guidance has been cut twice in
  twelve months. Margin and buyback findings partly offset it: +0.4 each.

## Already public, and what is new in the release

| name | already public | new in the release |
| --- | --- | --- |
| FAN | the whole FY26 period (pre-close, 23 Jul) | FY27 outlook |
| NFG | Q1–Q4-month trading "in line" (8 Jul) | H1 numbers, Mach49 |
| SZU | H1 EBITDA and a narrowed guide (ad-hoc, 28 Sep) | the 2026 campaign comment |
| TSCO | Q1 sales and the FY profit guide | Q2 sales, H1 profit, a probably narrowed guide |
| ADMCM | the guidance cut of 8 Jun | Q3 numbers; a guidance change is plausible |
| ALLIX | H1 revenue (16 Jul) | H1 operating result and cash flow |

A guidance change is likely or plausible for TSCO and ADMCM, and both hunters raised
`abs_move_pct` for it. On the first resolved days, a pre-release or a guidance change
decided the size of the move while the emitted sizes barely differed. Read the realised
moves against this table.

## What this day is and is not

- **Selection:** "all 6 eligible names (at or under the cap)". There were 9 scheduled and
  6 eligible at the $100k floor, so no random draw was needed. Eligible and hunted by
  market: uk 3, de 1, fr 1, fi 1; zero in se, dk, no, it, es and pl.
- **Concentration:** the largest market is the UK at 50% (3 of 6), across 4 markets. Half
  the day is one market.
- **Calendar sources:**
  - The UK RNS calendar was read and confirmed TSCO, NFG and FAN.
  - Yahoo was read in all ten markets and agreed with the vendor on TSCO, FAN, NFG and SZU.
  - The issuer calendars (EQS, Inderes, Nasdaq fincal, Euronext Oslo, bankier) were all
    read. Inderes joined ADMCM.
  - No source read `unavailable` or `read_short`.
- **`session_unresolved`:** SZU and ALLIX. ALLIX turned out to be amc (above). SZU's bmo
  rests on the issuer's cadence: its last release was at 07:00 CEST.
- **Options:** `options` is null in all ten markets, so Europe runs in the **anchor-less
  regime**, the one priced at ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers:** de, fi, fr and uk all resolved. **`anchor_covered: true` on 3 of 6**
  (TSCO, NFG, FAN, all UK). SZU, ALLIX and ADMCM read a truncated zero, not an anchor.
- **Spain and Poland:** none of the six names, so no name today lacks a register entirely.
  **Germany: 1 (SZU)**, which cannot reach `event_occurred: false`. Neither can France
  (ALLIX), since 2026-09-28.
- **`lean_vs_free_control_rho`:** the latest resolved run that reports it (sealed for
  2026-09-30) reads uk **0.40**. The lean's weights are priors borrowed from the US runs and
  have been measured nowhere in Europe.
- **History basis:** **estimated** `history.basis` (`estimated_from_cadence`) for SZU,
  ALLIX and ADMCM. That is a scale, not a record of dates. Observed RNS history exists for
  TSCO, NFG and FAN only.
- **Conviction floor:** 0 of 6 clear 2.8. Over the whole US sample, the sign was a coin
  flip below the floor.
- **ADMCM must be resolved within about a week.** The Nasdaq Nordic feed only pages back
  about twelve days.
- **One day is not a result.**

## Language notes, quoted and not ranked

- **ALLIX:** the event date, the broker estimates, the KKR take-private rumour, the
  "après clôture" listing and the CEO's share sales all came only from French sources.
- **SZU:** the crop-failure detail (WVZ, VSZ, the Rain campaign), Barclays' read of the
  ad-hoc via dpa-AFX, and the sugar-tax draft came only from German sources.
- **ADMCM:** the bar itself, the company's own numbers on the billing headwind and its
  customers, and Inderes's expectation of a reiterated guide came from Finnish sources.
- **NFG:** the Investegate record carried the full run of Griffiths holding notices, where
  English search returned only July's.
- **FAN** and **TSCO:** the domestic UK sources added little beyond the primary documents.

Hunter versions are in `provenance.json` (uk.v7, de.v7, fr.v7, nordic.v5), all on
claude-opus-5-5. Each hunt froze a `pre_lessons` draft. The language-pass control
(`pre_local`) was retired on 2026-09-22 and is not part of this run.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
