# Stage EU — Europe ranking for 2026-10-21

**The answer: one name clears the 2.8 conviction floor, MIPS (Mips AB) at +2.90, long. The
panel selected three names: MIPS long (4 of 4 judges in their own top 20%), JM short (3 of
4) and BULTEN long (3 of 4).** Twenty names were ranked from a random draw of 37 eligible,
and **15 of the 20 are Swedish**. So this is mostly a Stockholm day, and any pooled statement
about it is mostly about Swedish small and mid caps reporting on one Wednesday morning. FTK
(flatexDEGIRO) is at the bottom at −1.30.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Tuesday 2026-10-20 at about 14:00 UTC while the European markets were still
trading, so every sealed spot is an **intraday price, not a close**. The realised move is
measured from daily bars, close(2026-10-20) → close(2026-10-21) for a bmo name and
close(10-21) → close(10-22) for an amc name. Two sessions are known to be wrong (FTK and
BULTEN, below).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | MIPS | Mips | **+2.90** (p93) | **yes** | +1.19 | 8.5 | 57 | bmo. Issuer invitation: 07:30 CET |
| 2 | se | BULTEN | Bulten | **+1.90** (p83) | no | +1.28 | 8.0 | 58 | **sealed amc; the issuer says 13:30 CEST in session** (see below) |
| 3 | se | INWI | Inwido | **+1.00** (p66) | no | +0.80 | 8.0 | 55 | bmo. Issuer: 07:45 |
| 4 | se | FABG | Fabege | **+0.85** (p60) | no | +0.25 | 2.5 | 55 | bmo. Issuer: 07:30 CET |
| 5 | se | ALTRA | Altra Fastigheter | **+0.70** (p53) | no | +0.35 | 3.5 | 55 | sealed `bmo?`. MFN estimates 12:00 in session; Q1 came at 19:40, so the timing is uncertain |
| 6 | de | SAP | SAP | **+0.70** (p53) | no | +0.30 | 7.5 | 52 | amc. 22:05 CEST on 21 Oct |
| 7 | se | BERG_B | Bergman & Beving | **+0.60** (p49) | no | +0.33 | 5.5 | 53 | bmo. MFN and Finwire: 07:45 |
| 8 | se | HEBA_B | HEBA Fastighets | **+0.50** (p42) | no | +0.24 | 3.0 | 54 | in session at 12:00; the sealed window holds it |
| 9 | es | IBE | Iberdrola | **+0.35** (p31) | no | +0.21 | 2.6 | 54 | bmo. CNMC OIR of 7 Oct: before the 09:00 open |
| 10 | se | OVZON | Ovzon | **+0.30** (p28) | no | +0.15 | 7.5 | 51 | bmo. Issuer: 08:00 CEST |
| 11 | se | SALIX | Salix Group | **+0.30** (p28) | no | +0.55 | 5.5 | 55 | bmo. Issuer: 07:45 CEST |
| 12 | se | SKF_A | SKF A | **+0.05** (p11) | no | +0.00 | 5.0 | 50 | bmo. Issuer: around 07:30 |
| 13 | se | KEBNI_B | KebNi | **0.00** (p5) | no | −0.36 | 9.0 | 48 | sealed `bmo?`. Every prior report went out at 07:00 CET |
| 14 | se | NMAN | Nederman | **0.00** (p5) | no | −0.33 | 5.5 | 47 | bmo. 08:00 CET per the Q2 calendar |
| 15 | fi | TTALO | Terveystalo | **−0.10** (p14) | no | +0.00 | 4.0 | 50 | bmo. About 09:00 EEST |
| 16 | no | DNB | DNB Bank | **−0.15** (p16) | no | −0.18 | 4.5 | 48 | bmo. NewsWeb 684281: 07:30 CET |
| 17 | se | GETI_B | Getinge B | **−0.20** (p19) | no | −0.26 | 6.5 | 48 | bmo. Issuer: 08:00 CEST |
| 18 | se | SHB_A | Handelsbanken A | **−0.30** (p28) | no | −0.24 | 4.0 | 47 | bmo. Issuer: 07:00 CET |
| 19 | se | JM | JM | **−1.00** (p66) | no | −0.84 | 7.0 | 44 | bmo. Issuer: 08:00 CEST |
| 20 | de | FTK | flatexDEGIRO | **−1.30** (p73) | no | −0.70 | 7.0 | 45 | **sealed `bmo?`; the issuer says 18:00 CEST, amc** (see below) |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by Opus 5.5:
scale, not rank. ALTRA/SAP, OVZON/SALIX and KEBNI_B/NMAN tie, and the scorer's order inside a
tie carries no information.

**Two sealed windows are wrong, and both are documented by the issuer:**
- **FTK is amc, not the sealed `bmo?`.** flatexDEGIRO's IR calendar puts the Q3 statement at
  18:00 CEST on 21 October, after the 17:30 Xetra close, with the call at 09:00 on 22 October.
  Q1 and Q2 went out at the same hour on EQS. The sealed window (close 10-20 → close 10-21)
  contains no release. The hunter's `session_check` opens with "amc" and all four judges
  sized the amc window.
- **BULTEN is in session, not the sealed amc.** Bulten's own invitation puts the Q3 report at
  13:30 CEST on 21 October, during trading
  (https://view.news.eu.nasdaq.com/view?id=b93d3dcc25844ef8ee613991aee357832&lang=en&src=listed).
  The reaction is in close(10-20) → close(10-21), and the sealed amc window would mostly miss
  it. The hunter's `session_check` opens with "bmo".
- **Check what `eu_resolve.py` takes for both rows before trusting them.**
- ALTRA's 12:00 is an MFN estimate. If it lands after 17:30, the amc window applies instead.

**Pre-released, or a guidance event (`already_public` / `new_in_release`):**
- **TTALO pre-released the quarter.** It issued a profit warning on 2026-10-20 at 13:45
  EEST, during the session before the window and about three hours before the seal:
  - the FY26 adjusted EBIT guide was cut to EUR 110–120m from 120–140m;
  - Q3 adjusted EBIT came in at about 17.8m against a 24.0m consensus;
  - the stock fell −7.4% intraday.
  The report on 21 October restates a known period, which is why its sizes are near zero.
  Source: https://view.news.eu.nasdaq.com/view?id=b403775a2e57535c4a36db0160b80b04f&lang=en&src=listed.
- **DNB pre-released its one-offs** (−534m from the AT1 FX effect and +151m from basis swaps,
  on 2 October). They are in the consensus.
- **The other eighteen pre-released nothing.** None has a profit warning or trading update
  with the period's numbers since its last report. Several hunters read monthly KPIs that
  partly pre-release volumes, for example FTK's Q3 trade count against consensus.
- **Guidance events, the likelier large moves:**
  - **FTK:** consensus sits near the top of the €200–230m net-income guide, so a reiteration
    reads as a cut.
  - **SAP:** a narrowing toward the upper half of the 23–25% cloud-revenue guide is plausible.
  - **IBE:** it raised at 9M last year and says it will meet FY "con holgura" (comfortably).
  - **BULTEN:** new post-divestment targets were flagged for "the autumn", timing unconfirmed.
- **No numeric guidance at all:** most of the Swedish names, which is why their whole quarter
  is new.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four members ran on their own pinned `-intl-` agents, with no fallback, and each
  covered 20 of 20 packs.
- The selection rule for this market is `consensus`: a name is selected when 3 of 4 judges
  put it in their own top 20%.
- Each judge's top 20% starts at Opus 5 |1.80|, Opus 5.5 |0.91|, Sonnet 5.5 |1.08| and
  Fable 5.1 |1.32|, measured on 66 live sizes each.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MIPS | **yes** | 92 | long | 8 | 97L* | 98L* | 79L | 92L* | 4 | +2.11 | +2.90 |
| 2 | JM | **yes** | 85 | short | 7 | 88S* | 94S* | 82S* | 76S | 3 | −1.47 | −1.00 |
| 3 | BULTEN | **yes** | 83 | long | 9 | 94L* | 89L* | 79L | 71L | 3 | +1.34 | +1.90 |
| 4 | SALIX | no | 74 | long | 13 | 86L* | 86L* | 59L | 64L | 2 | +0.99 | +0.30 |
| 5 | FTK | no | 70 | short | 13 | 91S* | 58S | 67S | 64S | 1 | −0.78 | −1.30 |
| 6 | FABG | no | 54 | long | 22 | 79L | 65L | 18L | 54L | 1 | +0.68 | +0.85 |
| 7 | INWI | no | 63 | long | 13 | 50L | 83L* | 54L | 64L | 0 | +0.73 | +1.00 |
| 8 | BERG_B | no | 50 | long | 17 | 42L | 74L | 27L | 56L | 0 | +0.59 | +0.60 |
| 9 | ALTRA | no | 28 | long | 11 | 35L | 38L | 30L | 9L | 0 | +0.42 | +0.70 |
| 10 | NMAN | no | 37 | short | 13 | 35S | 58S | 23S | 32S | 0 | −0.41 | 0.00 |
| 11 | HEBA_B | no | 31 | long | 16 | 56L | 33L | 12L | 21L | 0 | +0.33 | +0.50 |
| 12 | SAP | no | 26 | long | 14 | 47L | 9L | 18L | 32L | 0 | +0.32 | +0.70 |
| 13 | SHB_A | no | 27 | short | 12 | 47S | 27S | 17S | 18S | 0 | −0.27 | −0.30 |
| 14 | SKF_A | no | 15 | short | 6 | 4S | 20S | 17S | 20S | 0 | −0.24 | +0.05 |
| 15 | GETI_B | no | 21 | short | 18 | 47S | 9S | 2S | 27S | 0 | −0.23 | −0.20 |
| 16 | TTALO | no | 11 | long | 3 | 14L | 6L | 12L | 11L | 0 | +0.18 | −0.10 |
| 17 | KEBNI_B | no | 3 | long | 46 | 35L | 64S | 12S | 54L | 0 | +0.13 | 0.00 |
| 18 | DNB | no | 10 | short | 6 | 4S | 21S | 8S | 8S | 0 | −0.12 | −0.15 |
| 19 | IBE | no | 7 | long | 3 | 9L | 9L | 2L | 8L | 0 | +0.10 | +0.35 |
| 20 | OVZON | no | 4 | short | 13 | 9L | 0 | 26S | 0 | 0 | +0.00 | +0.30 |

Each member's figure is its percentile 0-100 against its own live range, with L for long and S
for short. A `*` marks a member's own top 20%.

**MIPS, selected long (all four judges lean long; three are in their own top 20%).**
- **The evidence the members name:**
  - FactSet consensus from six analysts (Finwire/Börsvärlden, 2026-10-19) is sales of
    216 MSEK. Rebuilding Q3 from the company's own numbers gives about 225–230 MSEK: the
    two-year organic stack from Q2, about +4% FX, and about 40 MSEK from Koroyd.
  - The disclosed short is 9.48% and still building: Marshall Wace went from 0.52% to 1.13%
    and Wellington from 0.61% to 0.90%.
  - The stock gapped +27.8% on its last sales beat.
  - The Q3 one-off is only the known patent settlement, and legal costs stop.
- **The strongest case against:**
  - The beat is an inference from the company's own numbers, not a disclosed figure.
  - It is unclear whether the 58 MSEK EBIT bar includes the USD 3.25m settlement.
  - Taiwanese bike makers' September sales were weak (Merida −26% y/y).
  - The crowded short also means many holders already know the bull case.

**JM, selected short (all four lean short; three in their own top 20%).**
- **The evidence the members name:**
  - JM published its own Modular consensus: revenue 2,544 and EBIT 90.7. That implies Q3
    revenue of 0.90× Q2, against JM's own 0.70× in 2024 and 0.84× in 2025.
  - No investor-project sale was announced in Q3, against 236 investor units in Q3 2025.
  - The Q2 drag from low-margin repurchased units is still there.
  - JM missed badly on Q3 2025 (−11.6% on the day) and Q2 2026 (−12.0%).
- **The strongest case against:**
  - The short is crowded at 11.66%, and covering slightly, so a beat has squeeze fuel.
  - Stockholm tenant-owned apartment prices rose 2.0% in September.
  - SEB and DNB Carnegie cut targets in early October, so the bar is fresh.
  - The stock rose 8% in the five sessions before the print.

**BULTEN, selected long (all four lean long; k=3).** The `*` marks in the table come from the
live-percentile reference, while `consensus_k` counts against `member_reference` q80 (200
sizes, seed included). Sonnet 5.5's +0.96 sits exactly on its q80 of 0.96, which makes the
third member. It is the most marginal of the three selections.
- **The evidence the members name:**
  - The comparison is easy: Q3 2025 for the businesses Bulten keeps was crushed by the
    cyberattack at JLR, its largest customer (EBIT SEK 12m). JLR's Jul–Sep 2026 wholesales
    were +24.5% y/y.
  - The CEO and the Chair bought about SEK 17m of stock from 26 Aug to 3 Sep, per the
    Finansinspektionen insider register.
- **The strongest case against:**
  - No Q3 consensus exists anywhere, so the bar is unsourced.
  - The stock is up 62% since 30 June.
  - The CFO resigned eight days before the print.
  - Fable 5.1 did not file one Kepler item that appears to be a relabelled 2025 article.
  - **The sealed session is wrong**: the judges sized the in-session window.

**Where the panel and the hunters disagree most:**
- **SALIX:** the hunter's sum is only +0.30, but Opus 5 and Opus 5.5 put it in their own top
  20% long, on the H1 run-rate far above the one public broker's FY estimate.
- **FTK:** the hunter's −1.30 is the day's second-largest |impact_sum|, but only Opus 5
  is in its own top 20%, so it is not selected.
- **KEBNI_B:** the spread is 46, the widest of the day. Opus 5 and Fable 5.1 lean long,
  Opus 5.5 and Sonnet 5.5 short.
- **TTALO and SKF_A** carry opposite small signs between the panel and the hunter. All are
  near zero.
- **MIPS is the only above-floor name, and the panel selected it.**

**What these numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- Certainty (`p_up`) is recorded and decides nothing.
- Each member's scale still rests heavily on the frozen E-P seed: 66 live sizes, against the
  roughly 200 this market needs.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing
  about this market's panel is established.

## The finding driving the top and the bottom

**Top: MIPS +2.90.** The largest finding is +2.0 on the reported quarter: Q3 sales of
about 225–230 MSEK against the 216 MSEK FactSet bar. This is the hunter's own inference from
the company's numbers. The bar source is Finwire/Börsvärlden (2026-10-19), with URLs in
`hunts/MIPS.json`. The crowded, still-building 9.48% short adds +0.8.

**Bottom: FTK −1.30.** Two −0.8 findings drive it.
- **Trade mix.** Cash products fell to 0.66 of trades from 0.70 in Q2, which points to
  commission per trade below the consensus €4.585. Source: the company's monthly KPI
  workbook,
  https://s206.q4cdn.com/770226284/files/doc_downloads/monthly-kpis/2026/10/flatexDEGIRO_Monthly-KPI-Report_Jan-2022-to-September-2026.xlsx.
- **Guide against consensus.** FY consensus net income of €222.7m sits near the top of the
  €200–230m guide. Source: the company-compiled consensus,
  https://s206.q4cdn.com/770226284/files/doc_downloads/2026/10/261015-flatexDEGIRO_company-compiled-consensus_Q3-2026.pdf.
- **The offset:** insider buying (+0.5) and the €100m buyback (+0.4).

## Names that could not be ranked

None: all 20 of 20 are rankable.

## What must be said every time

- **Selection:** `selection.method` was "random sample of 37 eligible, seed 'eu-2026-10-21'".
  - 62 rows were scheduled; 37 cleared the $100k turnover floor and 25 were dropped.
  - The draw was random among the eligible names, at the cap of 20.
  - `eligible_by_market`: se 24, no 3, uk 2, de 2, dk 2, fi 2, fr 1, es 1, it 0, pl 0.
  - `by_market` (hunted): se 15, de 2, no 1, fi 1, es 1; uk, fr, dk, it and pl 0.
- **Concentration: the largest market is Sweden at 75% (15 of 20), across 5 markets.**
  - That is a correlated exposure the scorer cannot see.
  - Three Swedish property companies (FABG, ALTRA, HEBA_B) and two Nordic banks (SHB_A, and
    DNB in Norway) share a rates read.
  - October is Sweden's month, as the 2026-10-22 precedent showed.
- **Calendar sources:**
  - **Vendor:** TradingView, for every market.
  - **UK:** the RNS calendar read; it added PBEE, LIO and BKS and confirmed GELN. No UK name
    survived the draw.
  - **Issuer calendars, all read:** EQS (added FTK), Inderes (SE added 5, FI added 4),
    Nasdaq Nordic financial calendar, Euronext Oslo and bankier (PL, 0 for the date).
  - **Yahoo's firm dates read `unavailable` on all ten markets** ("quote endpoint failed on
    every batch"), the same as the previous runs.
- **`session_unresolved` at seal:** ALTRA, FTK and KEBNI_B.
  - **FTK turned out to be amc.**
  - KEBNI_B was confirmed bmo by pattern.
  - ALTRA is estimated in session.
  - **BULTEN was sealed amc with confidence and is in session.**
- **Option anchor:** `options` is null in all ten markets, and Europe runs in the anchor-less
  regime that priced at ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
  - The SAP hunter found a substitute: SAP's NYSE ADR straddle for 23 October prices about a
    6.5% event move.
- **Short registers resolved:** se (as of 2026-10-20), de (2026-10-19), no (2026-10-19) and
  fi (2026-10-16). es has no register at all.
- **Anchor coverage: 6 of 20 carry `anchor_covered: true`** (ALTRA 2.28%, BULTEN 0.39%,
  FABG 2.04%, FTK 0.5%, JM 11.66%, MIPS 9.48%).
  - The other fourteen read a truncated zero or no register, which is not an anchor.
  - Both panel-selected Swedish names with a large short (JM, MIPS) are anchored.
- **Weak legs:**
  - **Spain or Poland: 1 name, IBE.** It has no positioning anchor, its lean is the run-up and
    therefore the free control, and it can never be confirmed or killed after the fact.
  - **Germany: 2 names, SAP and FTK.** They cannot reach `event_occurred: false` either.
- **`lean_vs_free_control_rho`:** the latest resolved European run on disk (2026-10-08) reads
  1.0 for uk on 3 names and nothing else measurable. That is not a measurement. The lean's
  weights are priors borrowed from the US runs, measured nowhere in Europe.
- **`history.basis`:** only DNB is observed (`observed_newsweb`). The other nineteen are
  `estimated_from_cadence`, a scale and not a record of dates.
  - Hunters found the estimated scale too low on most names with real report-day tables:
    INWI ~9% observed against 2.38% estimated, JM ~7% against 3.31%, GETI_B 5.65% against
    2.34%, MIPS 8.2% against 4.21%, and BULTEN ~7.5% against 2.32%.
  - SKF_A's estimated dates are mostly wrong.
- **Conviction floor:** one name, MIPS (+2.90), sits above 2.8. Over the whole US sample the
  sign was a coin flip below the floor.
- **Resolution timing:** the 15 Swedish names and TTALO must be resolved within about a week
  (the Nasdaq Nordic feed window), or their rows resolve null for ever.
- One day is not a result.

**`language_note` highlights (prose, nothing ranks it):**
- **Swedish sources** carried most of the day's bars and reaction tables:
  - the Modular/FactSet consensus tables (ALTRA, FABG, GETI_B, JM, MIPS, SHB_A, BERG_B);
  - the per-name report-day reaction tables that set `abs_move_pct`;
  - the Finansinspektionen insider buys (BULTEN, BERG_B);
  - SB1's INWI estimate;
  - Arctic's FABG note.
- **Spanish sources** for IBE carried the "con holgura" quote and the 7 Oct CNMC filing.
- **Finnish sources** (the Inderes forum and preview) carried TTALO's consensus and the
  Danske attribution for the 19 Oct fall.
- **German sources** carried the ODDO and Deutsche Bank FTK calls and UBS's SAP slowdown
  call.
- **DNB:** the Norwegian press added nothing.
- **Issuer filings** were bilingual everywhere and added nothing language-specific.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
