# Stage EU — Europe ranking for 2026-11-02 (Mon)

Sealed Fri 2026-10-30 ~15:40 UTC, while the European markets were still trading: every
sealed spot and `run_up_20d_pct` is an **intraday price, not a close**. Ranking key:
`impact_sum` (from `edge-scores.json`'s `ranking_key`). Conviction floor 2.8. **No name
clears the floor.** No orders; this stage reads no broker.

## Ranked

| # | ticker | market | session | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | COFA | fr | **amc** (sealed bmo?, hunter: 17:35 Paris) | +1.30 | 4.5 | 54 | +0.36 | no | estimated |
| 2 | AAD | de | amc | +1.10 | 6.0 | 57 | +0.84 | no | estimated |
| 3 | FRAMERY | fi | bmo (09:00 EET) | +0.70 | 8.0 | 52 | +0.32 | no | estimated |
| 4 | BAKKA | no | bmo (06:00 CET) | +0.40 | 5.5 | 50 | +0.00 | no | observed_newsweb |
| 5 | LTMC | it | amc | +0.00 | 4.0 | 52 | +0.16 | no | estimated |
| 6 | ADVT | uk | bmo (07:00 London, confirmed) | −0.20 | 3.0 | 49 | −0.06 | no | observed_rns |
| 7 | ACAD | se | bmo (07:00 CET) | −0.40 | 6.0 | 47 | −0.36 | **yes** (0.6% FI) | estimated |
| 8 | GRF | es | amc (17:35 CET) | −1.50 | 6.0 | 44 | −0.72 | no (no register) | estimated |

Not ranked: **LBW** (pl) — phantom date. Lubawa's own 2026 reporting calendar (raport
bieżący 1/2026, "raport za III kwartał 2026 r. - w dniu 30 listopada 2026 r.",
https://www.parkiet.com/komunikaty-espi/art43731771-lubawa-sa-terminy-publikacji-raportow-okresowych-w-2026-roku)
puts the Q3 report on 2026-11-30.

`impact_scaled` is the hunter's second, separate measurement; it is not the key and the
floor does not apply to it.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence; the panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their pinned agents, no fallback. Selection: 3 of 4 judges in their own top 20%.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AAD | amc | **yes** | 89 | long | 10 | 72L | 96L* | 94L* | 94L* | 3 | +1.92 | +1.10 |
| 2 | FRAMERY | bmo | | 71 | long | 14 | 76L | 48L | 70L | 88L* | 1 | +1.08 | +0.70 |
| 3 | GRF | amc | | 65 | short | 11 | 69S | 75S | 46S | 68S | 0 | −0.94 | −1.50 |
| 4 | COFA | bmo? | | 58 | long | 11 | 40L | 66L | 68L | 59L | 0 | +0.79 | +1.30 |
| 5 | ACAD | bmo | | 38 | short | 13 | 54S | 23S | 28S | 48S | 0 | −0.50 | −0.40 |
| 6 | BAKKA | bmo | | 21 | short | 26 | 40S | 47S | 20L | 16S | 0 | −0.37 | +0.40 |
| 7 | LTMC | amc | | 25 | long | 12 | 12L | 18L | 26L | 44L | 0 | +0.31 | +0.00 |
| 8 | ADVT | bmo? | | 5 | short | 10 | 20S | 0- | 7L | 9S | 0 | −0.07 | −0.20 |

**AAD (selected, long, 3 of 4).** Every judge leaned on the same absence: Amadeus FiRe
pre-released both of its recent guidance changes by MAR ad-hoc (18 Oct 2024; 28 Jul 2026,
six days before H1), and as of 30 Oct — 30 days after Q3 closed — there is no ad-hoc,
which points to the FY26 operating-EBITA guide of €17–23m holding while the stock is down
28.5% in 60 sessions. Four board members bought between 4 Sep and 1 Oct (~€157k). Source
for the calendar line ("02. Nov. 2026 Veröffentlichung Zwischenmitteilung Q3/9M 2026 (nach
Börsenschluss)"): https://group.amadeus-fire.de/wp-content/uploads/2026/08/Amadeus-Fire-AG_Zwischenbericht-Q2-6M-2026.pdf.
**Strongest case against:** the finding rests on absence; the issuer moved its distribution
from EQS to pressetext, a cut could come inside the release itself, leverage is 3.5x
rolling EBITDA with the dividend cancelled, and H2 must deliver €13.5–19.5m against H1's
€3.5m. Opus 5 kept it below its top 20%.

**Disagreements.** BAKKA is the only opposite sign: the hunter +0.40 (2027 harvest guide
likely up), three of four judges short on the serial Scottish misses and 2027 feed cost.
COFA is the hunter's top name and sits fourth for the panel, with no judge putting it in
its top 20%. No above-floor name exists, so none went unselected.

**What the numbers are not.** `panel_score` ranks and does not forecast; there is no
`expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the member scales
are still mostly the frozen E-P seed until this market has about 200 panel names of its
own; and in the four-model re-judge the judges ranked Europe better than the live hunt,
but nothing about this market's panel is established.

## Top and bottom

- **Top, COFA +1.30:** Coface's own published consensus for Q3-26 (estimates as of 20 Oct,
  4 analysts) has a net loss ratio of 39.0% and net income €48m against the H1-26 run-rate
  of 37.4% and ~€54m a quarter — https://www.coface.com/investors/coface-share/analysts-consensus.
  **The window was sealed wrong for this name:** the vendor/Yahoo row said bmo, the
  issuer's own calendar says "Résultats 9M-2026 : 2 novembre 2026, après bourse" with prior
  filings timestamped 17:35 Paris, so the print lands after the 11-02 close and the move is
  in the 11-02 → 11-03 window. `eu_resolve.py` should measure both windows (session was
  unresolved).
- **Bottom, GRF −1.50:** the FY26 guide (adj EBITDA margin ≥25%, FCF pre-M&A €500–575m)
  needs ~26% margin and €409–484m FCF in H2 after 23.9% and €91m in H1; Renta 4 already
  models 24.8% — https://www.r4.com/articulos-y-analisis/valores/grifols-2t26-trimestre-en-linea-aunque-dependiente-del-2s26-para-alcanzar-los-objetivos-del-ano.
  Plus Takeda's 29 Oct IVIG/albumin warning (peer read-across) and the Canadian plasma
  collection pause from 14 Aug. The bar is one snippet-only consensus (Euroland median of
  ten, via a Benzinga ES preview that returned 403).

## Per-name: what was already public, what is new

| ticker | already public | new in the release |
| --- | --- | --- |
| COFA | H1-26 results; company-compiled consensus | Q3 loss ratio; first Q&A since the 18 Sep CNP takeover rumour (stock round-tripped) |
| AAD | FY26 guide cut on 28 Jul | whether the €17–23m guide holds (**guidance**) |
| FRAMERY | report date; no short-term outlook given | Q3 numbers against a split bar (Inderes adj EBIT 9.3m vs consensus 11.3m) |
| BAKKA | Q3 harvest volumes and DKK 42m Scottish mortality (5 Oct trading update) | **first 2027 harvest guidance** (a guidance event) |
| LTMC | FY26 guide; ADM monthly online data | Q3; first chance to comment on the 2027 gaming levy |
| ADVT | **H1 pre-released** as floors on 12 Oct (revenue ≥ £28.5m, adj EBITDA ≥ £8.0m) | exact figures, organic split, possible tender decision |
| ACAD | autumn enrolment +8% (31 Aug) | Q1 numbers; no numeric guidance given |
| GRF | H1, FY26 guide | Q3 and whether the guide holds (**guidance**) |

## What this day is and is not

- **Selection:** "all 9 eligible names (at or under the cap)", seed eu-2026-11-02. 15
  scheduled, 9 eligible, 9 hunted. by_market uk 1, de 1, fr 1, se 1, no 1, fi 1, it 1,
  es 1, pl 1, dk 0. No draw was needed; the day was under the cap of 20.
- **market_concentration:** largest market 11% (uk, tied at one each), 9 markets
  represented. No single market dominates.
- **session_unresolved:** COFA, LBW, ADVT. ADVT was confirmed bmo by the hunter (07:00
  London on every prior results RNS); COFA turned out **amc**; LBW has no release.
- **Options:** null in all ten markets; Europe runs in the anchor-less regime that priced at
  ρ=+0.073, p=0.45 over 104 events on the sealed corpus (`archive/backtest/FINDINGS.md` §33).
- **Registers:** all eight that exist read (uk FCA, de Bundesanzeiger, fr AMF, se FI,
  no Finanstilsynet, fi Finanssivalvonta, it CONSOB; dk had no name); es and pl have none.
  **Only 1 of
  9 names carries `anchor_covered: true`** (ACAD, 0.6% at Finansinspektionen, flat). Every
  other register-read name is a truncated zero at the 0.5% floor, not a measured zero.
- **Spain and Poland: 2 names** (GRF, LBW) with no positioning anchor and no day archive;
  their lean is the run-up, i.e. the free control. **Germany: 1** (AAD), which cannot reach
  `event_occurred: false`.
- **lean_vs_free_control_rho:** the last resolved European run is 2026-10-16; it reports
  se 0.60. No European run after 10-16 is resolved; the Nordic names from 10-19 onward are
  at or past the ~12-day archive window.
- The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.
- **history.basis:** only ADVT (`observed_rns`) and BAKKA (`observed_newsweb`) are real
  dated histories; the other seven are cadence estimates — a scale, not a record. Several
  hunters (FRAMERY, ACAD, GRF, COFA) measured reactions on the issuers' real release dates
  and found the baseline scale too low.
- **Conviction floor:** no name clears 2.8. Over the whole US sample the sign below the
  floor was a coin flip.
- `scripts/hunt_status.py` is absent from main, so the unfinished-search backstop could not
  run; every hunter reported `search_complete: true`.
- One day is not a result.

### Language notes worth quoting (prose; nothing ranks them)

- **LTMC:** the Italian sources did the work — the ADM-based monthly figures, the specific
  gaming-levy options in the 2027 budget, and the release-timing precedents.
- **GRF:** only Spanish sources carried Renta 4's below-guide margin estimate, the sole
  sourced Q3 bar, the Canadian reopening count and the US Biopharma IPO slipping to 2027.
- **LBW:** everything that decided the name (the company calendar, the ESPI lists) was Polish.
- **ACAD:** Swedish press carried the profit-ban political reaction history and the
  Bloomberg consensus comparisons for the last two reports.
- **ADVT, BAKKA, FRAMERY, AAD, COFA:** the local sources added nothing decisive the
  English ones did not carry.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
