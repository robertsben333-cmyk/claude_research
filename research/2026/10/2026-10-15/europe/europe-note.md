# Stage EU — Europe ranking for 2026-10-15

**The answer: no name clears the 2.8 conviction floor, and the panel selected nothing.
Fifteen names were ranked, and every `impact_sum` sits between −1.60 and +0.70. CARA
(Carasent, SE) and XPS (XPS Pensions, UK) share the top at +0.70. NEL (Nel ASA, NO) is the
bottom at −1.60, and the panel agrees: all four judges are short NEL, and it is the panel's
top name. Three UK rows were phantoms with no release on 15 October: AVCT, CAML and WTB.**

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Wednesday 2026-10-14 at about 13:45 UTC, while the European markets were still
trading. Every sealed spot is therefore an **intraday price, not a close**. The realised
move is measured from daily bars: close(2026-10-14) → close(2026-10-15) for a bmo print.

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | CARA | Carasent | **+0.70** (p49) | no | +0.56 | 7.0 | 54 | bmo. The issuer's invitation says 07:00 CEST |
| 2 | uk | XPS | XPS Pensions Group | **+0.70** (p49) | no | +0.55 | 5.5 | 55 | bmo inferred. Unresolved in the seal; prior updates went out at 07:00 |
| 3 | se | OEM_B | OEM International B | **+0.60** (p46) | no | +0.55 | 5.5 | 55 | **In session, not amc.** The vendor said amc. OEM's Q3 reports have gone out at 14:00 Stockholm since 2020 |
| 4 | se | EQT | EQT | **+0.50** (p38) | no | +0.40 | 5.0 | 54 | bmo. The issuer says about 07:00 CEST. The row came from Yahoo only |
| 5 | se | WALL_B | Wallenstam B | **+0.50** (p38) | no | +0.19 | 3.2 | 53 | bmo inferred from the issuer's pattern. Its Q2 release went out at 13:00 |
| 6 | uk | DNLM | Dunelm Group | **+0.40** (p32) | no | +0.27 | 4.5 | 53 | bmo inferred. Q1 trading update; prior releases went out at 07:00 |
| 7 | uk | ENT | Entain | **+0.20** (p18) | no | +0.32 | 4.0 | 54 | bmo inferred. Q3 trading update; prior releases went out at 07:00 |
| 8 | se | SLP_B | Swedish Logistic Property B | **+0.20** (p18) | no | +0.18 | 3.0 | 53 | bmo. The issuer says 08:00 CEST |
| 9 | se | EMIL_B | Emilshus B | **+0.10** (p13) | no | +0.21 | 3.5 | 53 | bmo. The issuer says 07:30 CEST |
| 10 | de | 2GB | 2G Energy | **+0.05** (p10) | no | +0.00 | 3.5 | 50 | **Unresolved.** No release time anywhere; it may be a website PDF |
| 11 | fi | NDA_FI | Nordea Bank | **−0.05** (p10) | no | +0.14 | 3.5 | 52 | bmo. The issuer says 07:30 EET |
| 12 | no | ENTRA | Entra | **−0.70** (p49) | no | −0.35 | 3.5 | 45 | bmo. The issuer says 07:00 CEST |
| 13 | se | ERIC_A | Ericsson A | **−0.80** (p53) | no | −0.34 | 8.5 | 48 | bmo. The issuer says about 07:00 CEST |
| 14 | se | AQ | AQ Group | **−1.00** (p61) | no | −0.42 | 7.0 | 47 | bmo. The issuer says 08:00 CEST |
| 15 | no | NEL | Nel | **−1.60** (p77) | no | −0.88 | 5.5 | 42 | bmo. The issuer says 07:00 CET |
| — | uk | AVCT | Avacta | not ranked | — | — | — | — | no event: 15 Oct is an investor presentation of interims already released on 30 Sep |
| — | uk | CAML | Central Asia Metals | not ranked | — | — | — | — | no event: 15 Oct is the Effective Date of the Cygnus scheme. Q3 ops came out 7 Oct |
| — | uk | WTB | Whitbread | not ranked | — | — | — | — | no event: the interims were brought forward to 13 Oct, before the window |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank. CARA and XPS tie on the key, and EQT and WALL_B tie
too. The scorer's order inside a tie carries no information.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own pinned `-intl-` agents, with no fallback, and each covered 15 of 15 packs. The
selection rule for this market is still `consensus`: a name is selected when 3 of 4 judges
put it in their own top 20%. Each judge's top 20% starts at Opus 5 |2.20|, Opus 5.5 |1.10|,
Sonnet 5.5 |1.30| and Fable 5.1 |1.54|.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NEL | no | 68 | short | 11 | 52S | 81S* | 64S | 74S | 0 | −1.00 | −1.60 |
| 2 | CARA | no | 56 | long | 7 | 45L | 61L | 55L | 61L | 0 | +0.68 | +0.70 |
| 3 | AQ | no | 55 | short | 11 | 68S | 52S | 39S | 61S | 0 | −0.64 | −1.00 |
| 4 | OEM_B | no | 39 | long | 13 | 19L | 55L | 36L | 45L | 0 | +0.55 | +0.60 |
| 5 | ENTRA | no | 37 | short | 19 | 68S | 26S | 19S | 36S | 0 | −0.37 | −0.70 |
| 6 | EQT | no | 20 | long | 13 | 39L | 6L | 26L | 10L | 0 | +0.30 | +0.50 |
| 7 | SLP_B | no | 19 | long | 6 | 10L | 26L | 19L | 19L | 0 | +0.29 | +0.20 |
| 8 | DNLM | no | 20 | long | 7 | 10L | 26L | 26L | 19L | 0 | +0.28 | +0.40 |
| 9 | ERIC_A | no | 22 | short | 12 | 42S | 13S | 13S | 19S | 0 | −0.26 | −0.80 |
| 10 | EMIL_B | no | 12 | short | 10 | 23S | 3L | 13S | 16S | 0 | −0.23 | +0.10 |
| 11 | XPS | no | 8 | short | 7 | 10S | 3S | 0- | 19S | 0 | −0.15 | +0.70 |
| 12 | 2GB | no | 13 | short | 19 | 45S | 6S | 6L | 6S | 0 | −0.13 | +0.05 |
| 13 | ENT | no | 2 | long | 7 | 10S | 3L | 6L | 6L | 0 | +0.12 | +0.20 |
| 14 | NDA_FI | no | 6 | short | 2 | 10S | 3S | 6S | 6S | 0 | −0.11 | −0.05 |
| 15 | WALL_B | no | 3 | long | 7 | 6L | 0- | 13L | 6S | 0 | +0.07 | +0.50 |

Each member's figure is its percentile 0-100 against its own live range, with L for long and
S for short. A `*` marks a member's own top 20%.

- **No name was selected.** The closest is NEL. Only Opus 5.5 put it in its own top 20%
  (81). The other three placed it at 52-74.
- **Where the panel and the hunter disagree most:**
  - **XPS:** the hunter is +0.70, joint top. The panel is short at panel_pct 8. Every judge
    discounted the "consensus is beatable" inference against both co-CEOs' discretionary
    sale in the middle of the half. Opus 5 also noted that the "mid-to-high single digits"
    guide exists only in an auto-summary.
  - **EMIL_B:** the hunter is +0.10. Three of the four judges are mildly short.
  - **WALL_B:** the hunter is +0.50. The panel is flat at panel_pct 3. The derivative gain
    is real, but it sits on a line this stock does not trade on.
- **What the numbers are not:**
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales still rest on 31 live sizes each plus the frozen E-P seed.
  - In the four-model re-judge, the judges ranked Europe better than the live hunt, but
    nothing about this market's panel is established.

## The top and bottom name

- **CARA (+0.70).** Carasent's Q3 numbers have not been pre-released. The stock trades on
  organic growth against its 15% target: Q1 grew 7% organically and the stock fell 5.0%;
  Q2 grew 11% and it rose 7.25%. Q2 organic ARR was +15%, with 6 MSEK signed but not yet
  live (https://view.news.eu.nasdaq.com/view?id=b89e71c743995a333e230517752530fad&lang=en&src=listed).
  A board member also bought about 1.5 MSEK of shares in August, per the FI insider register.
  The bar is unsourced, so every finding is capped small.
- **NEL (−1.60).**
  - **Backlog at risk:** the Q2 report flagged NOK 296m of PEM backlog as at "significant
    risk of delay or cancellation", and Q3 is the first update on it.
  - **Revenue comparison:** Q3 2025 revenue of NOK 303m was helped by alkaline milestones.
  - **Cash:** the Iwatani payment and Herøya capex drain cash in the quarter.
  - **Run-up:** the stock is +8.9% over five days on orders that are already public.
  - **History:** it fell on 7 of its last 9 results days.

  The Rheinmetall MoU and the Collins orders are already public. Release notice:
  https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=683767

## Phantoms, and two calendar defects they expose

All three phantoms came from `uk_rns_calendar.py`, the RNS-notice source added on
2026-10-06. Each will need `event_occurred: false` after the window, with the
source in `event_occurred_note`.

- **CAML:** the parser read "result in an Effective Date for the Cygnus Transaction of
  15 October 2026", a sentence in the 7 Oct Q3 Operations Update, as a results date. That
  is a parser defect: a scheme "Effective Date" sentence should never classify as results.
- **AVCT:** a "Notice of Interim Results Investor Meeting" was read as a results date.
- **WTB:** the Q1 statement's 15 Oct date was correct when it was published. The company
  then brought the interims forward to 13 Oct.

## What the reader must carry

**Selection.** `all 18 eligible names (at or under the cap)`: there was no random draw,
because 18 eligible names is under the cap of 20.
- `by_market`: se 8, uk 6, no 2, de 1, fi 1. Nothing came from fr, dk, it, es or pl.
- 28 rows were scheduled and 10 fell below the $100k floor.
- **Market concentration:** se is 44% of the day, and 9 of the 15 ranked names are Nordic.

**Calendar sources:**
- The UK RNS calendar added seven names: CAML, ENT, XPS, AVCT, DNLM, NWT and WTB. Three of
  the six that were hunted were phantoms.
- Yahoo added EQT. Inderes added PCOM_B, which did not reach the eligible list.
- Every calendar source read.

**Session-unresolved in the seal:** 2GB, EQT and all six UK names. The hunters settled EQT
from the issuer. They inferred XPS, DNLM and ENT from 07:00 history. 2GB is still unknown.
OEM_B was sealed amc, but its hunter places the release in session on 10-15 (see the table).

**Anchors:**
- `options` is null in all ten markets, so Europe runs in the anchor-less regime: ρ=+0.073,
  p=0.45 over 104 events on the sealed corpus.
- Short registers resolved for all five markets on the day: uk, de, se, no and fi.
- **7 of 18 names carry `anchor_covered: true`:** the six UK names plus AQ. Among the 15
  ranked names that is 4 (AQ, DNLM, ENT, XPS).
- **One anchor is wrong.** The NEL hunter found that Finanstilsynet lists the issuer as
  "NEL" at 0.59% (Tages Capital), but the seal read 0.0. The Norwegian join in
  `eu_positioning` likely needs an ISIN match, and other Norwegian names may be affected.

**Weak legs:**
- Spain and Poland contributed 0 names today.
- Germany contributed 1 name (2GB), which cannot reach `event_occurred: false`.
- The Nordic se/fi names must be resolved within about a week, or they resolve null.

**`lean_vs_free_control_rho`:** the last resolved run, 2026-10-08, reads uk 1.0 on 3 names.
That is too few to mean anything. The lean's weights are priors borrowed from the US runs,
measured nowhere in Europe.

**History basis:**
- **Estimated cadence**, a scale and not a record of dates: 2GB, AQ, CARA, EMIL_B, EQT,
  ERIC_A, NDA_FI, OEM_B, SLP_B and WALL_B.
- **Observed:** the UK names and ENTRA/NEL.
- Several hunters re-measured on the issuer's real dates and found the estimate far too
  small. ERIC_A's real median move is about 7.8% against 2.18% estimated; AQ's is about 6%
  against 2.5%.

**Already public / new in release:**
- 2GB pre-released H1 on 29 Sep and reiterated its guide twice.
- ENTRA's leases, NEL's Q3 orders and EQT's Coller step-up are all public.
- Likely guidance-type lines in the release:
  - ERIC_A's Q4 margin guide.
  - XPS's FY27 "in line" or "ahead".
  - EQT XI's activation.
  - Nordea's buyback decision.
  - EMIL_B's mechanical forecast nudge.

**Language notes.** These are prose, not evidence:
- Swedish wires carried the only sourced bars for AQ (Handelsbanken and Nordea), Nordea
  (the Infront table via Inderes, in Finnish) and Ericsson (the Infront breakdown).
- The FI insider register carried the insider trades for AQ, CARA and EMIL_B.
- The UK names' domestic RNS record caught the WTB brought-forward date, which vendor
  calendars still miss.

**Floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign was a coin
flip below it.

**One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
