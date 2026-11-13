# Stage EU — Europe researcher, event date 2026-11-16

Sealed 2026-11-13 ~15:40 UTC (16:40 Amsterdam), while the European markets were still trading (the fire came ~56 min after its scheduled 14:35 UTC). The sealed spots are **intraday prices, not closes**. The scored window is close(2026-11-13) → close(2026-11-16) for bmo names and close(2026-11-16) → close(2026-11-17) for amc names, measured by `eu_resolve.py` from daily bars. Ranking key: `impact_sum` (from `edge-scores.json`). Conviction floor: 2.8.

**Answer first:** no name reaches the 2.8 floor; it is a small, quiet UK-heavy Monday. The hunters' top is **N91 +0.60** and bottom **APN −1.30**. The four-model panel **selects one name, MEGP short** (3 of 4 judges in their own top 20%, `panel_pct` 81). It is the only name at or above the IBKR handoff rule (`panel_pct` >= 70 with four judges). Below the floor the sign was a coin flip over the whole US sample. One day is not a result.

## Ranked table

| # | ticker | mkt | session | impact_sum | abs_move | p_up | impact_scaled | anchor | history |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | N91 | uk | bmo (07:00 pattern; issuer RNS 13 Oct dates it) | +0.60 | 5.0 | 51 | +0.10 | yes (0.20%) | observed_rns |
| 2 | CBF | pl | sealed bmo? → **amc** (17:16 / 17:57 history) | +0.40 | 4.5 | 51 | +0.09 | no (no register) | est. |
| 3 | BYG | uk | **amc** (issuer RNS: "at the close of the market") | +0.20 | 4.0 | 48 | −0.16 | yes (4.98%) | observed_rns |
| 4 | SRE | uk | bmo? (07:00 pattern; issuer RNS 5 Oct dates it) | +0.10 | 3.0 | 50 | +0.00 | yes (2.44%) | observed_rns |
| 5 | GPW | pl | bmo (no timestamp; H1 summarised by 09:12) | +0.05 | 3.0 | 51 | +0.06 | no (no register) | est. |
| 6 | LGEN | uk | bmo? (07:00 pattern; HY26 calendar dates a Q3 TU) | −0.70 | 2.3 | 45 | −0.23 | yes (4.72%) | observed_rns |
| 7 | MEGP | uk | bmo? (07:00 pattern; notice of 11 Nov) | −1.20 | 8.0 | 46 | −0.64 | yes (2.98%) | observed_rns |
| 8 | APN | uk | bmo (Notice of Results 12 Oct; 07:00 pattern) | −1.30 | 4.0 | 44 | −0.48 | yes (0.47%) | observed_rns |

`impact_scaled` = (2·p_up/100 − 1)·abs_move is the hunter's second, separate measurement. It is not the key and nothing is ranked on it. BYG differs in sign between the two (findings sum small positive, p_up 48 on the reaction history and the activist premium at risk).

**Not ranked:** SLR (es). The hunter found **no date notice** on the CNMV OIR register (latest filing 21/10/2026) although every standalone Solaria results release 2024–2026 had one 5–21 days ahead; the one without a notice (9M 2025) came out at 08:23 on the morning of that year's Capital Markets Day, and this year's CMD is **Thursday 19 Nov 2026** (OIR filed 21/10/2026, https://www.cnmv.es/portal/otra-informacion-relevante/resultado-oir?nif=A83511501&lang=en). The 16 Nov vendor date is most likely a guess. Spain has no day archive, so the resolver cannot record `event_occurred: false`; the hunter puts a no-notice Monday release at 10–15%.

**Session corrections from the hunters:** CBF was sealed `bmo?` and releases after the close (Q2'26 filing stamped 17:16 on 2 Sep 2026; Q3'25 PAP story 17:57 on 5 Nov 2025), so its reaction is close(11-16) → close(11-17) and the sealed bmo window probably holds none of it. BYG was sealed amc and the issuer's RNS of 21 Oct confirms it (https://www.investegate.co.uk/announcement/rns/big-yellow-group--byg/notification-of-half-year-results/9833752).

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing. All four members ran on their pinned agents, no fallback, no retry. Each judge's own top 20% starts at |1.10| (Opus 5), |0.72| (Opus 5.5), |0.60| (Sonnet 5.5), |0.90| (Fable 5.1), read on 200 live sizes each.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MEGP | yes | 81 | short | 13 | 91S* | 82S* | 60S | 94S* | 3 | −1.43 | −1.20 |
| 2 | APN | | 65 | short | 6 | 70S | 68S | 56S | 66S | 0 | −0.89 | −1.30 |
| 3 | N91 | | 52 | long | 8 | 50L | 66L | 44L | 48L | 0 | +0.61 | +0.60 |
| 4 | LGEN | | 43 | short | 7 | 35S | 42S | 54S | 42S | 0 | −0.50 | −0.70 |
| 5 | CBF | | 29 | long | 16 | 17L | 11L | 48L | 41L | 0 | +0.36 | +0.40 |
| 6 | BYG | | 25 | long | 13 | 42L | 32L | 13L | 13L | 0 | +0.28 | +0.20 |
| 7 | SRE | | 10 | long | 2 | 10L | 11L | 13L | 8L | 0 | +0.14 | +0.10 |
| 8 | GPW | | 5 | long | 12 | 12S | 18L | 13L | 0- | 0 | +0.10 | +0.05 |

**MEGP (selected, short).** The judges name the same evidence the hunter filed: the 16 Nov trading update (issuer notice, https://www.investegate.co.uk/announcement/rns/me-group-international--megp/notice-of-trading-update/9868816) is the first FY27 outlook on a two-analyst name whose Edison FY27e (£78.2m PBT, +12%) has not been cut since July (https://www.edisongroup.com/research/recovery-on-track-after-aprils-setback/BM-3683/), while INSEE's October French household confidence fell to 80, the lowest since 2013, in the market the company blamed for its June warning (https://www.insee.fr/fr/statistiques/fichier/version-html/9098942/IR260_Camme_oct26.pdf). **The strongest case against:** the FY26 guide (£69–74m) needs only £36.3–41.3m of H2 profit against £44.2m a year earlier, May/June vending revenue was positive, the stock has already fallen 15.7% over 20 days (−6.2% and −2.3% on 9–10 Nov on 3–5x volume with no RNS), and the FCA net short is 2.98% and flat — so part of a cautious outlook may be priced. Sonnet 5.5 sized it only at its 60th percentile.

**Panel vs hunter:** they agree on sign for every name; the panel lifts MEGP above APN, which the hunter had as the day's most negative (APN's period and FY27 guide were pre-released on 26 Aug, which every judge discounted).

What the numbers are not: `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; the member scales are still mostly the frozen E-P seed until Europe has about 200 panel names of its own; and in the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established (2026-10-21: ρ +0.22, p 0.19 on 45 names).

## Selection and instrumentation

- `selection.method`: **all 9 eligible names** (at or under the cap of 20), so no random draw was needed today. 19 scheduled, 9 above the $100k floor. `by_market`: **uk 6, pl 2, es 1**; de, fr, se, dk, no, fi, it 0.
- `market_concentration`: **uk is 67% of the day** (3 markets represented). Any pooled statement about this day is mostly a UK statement.
- Calendar sources: the UK RNS calendar added MEGP and LGEN and confirmed BYG, SRE, N91, APN; Yahoo agreed on N91, BYG, SRE; Inderes added CLBIO, NIO (se) and HOVE, FYNBK (dk), none of which cleared the turnover floor; **bankier (pl) was unavailable** (HTTP 403).
- `session_unresolved`: CBF, LGEN, MEGP, SLR, SRE. The hunters' session checks: LGEN, MEGP, SRE bmo by the issuer's 07:00 pattern (not a stamp on this release); CBF amc.
- `options` is null in all ten markets: Europe runs in the **anchor-less regime** (ρ=+0.073, p=0.45 over 104 events in the sealed corpus).
- Short registers: FCA read (as of 2026-11-11, 428 rows); **all 6 UK names carry `anchor_covered: true`**; the 3 Polish/Spanish names carry none.
- **3 of 9 names came from Poland (2) and Spain (1)**, which have no short register and no day archive: their `priced_lean_pct` is the run-up, i.e. the free control, and they cannot be confirmed or killed after the fact. No German names today.
- `lean_vs_free_control_rho` from the most recent resolved European run on disk (2026-10-16): se 0.60. The lean's weights are priors borrowed from the US runs, measured nowhere in Europe.
- `history.basis`: the six UK names are `observed_rns`; CBF, GPW and SLR are **estimated from cadence** — a scale, not a record of dates.
- Pre-released / new in the release: **APN** (FY26 revenue and EBITDA and the FY27 guide pre-released 26 Aug; consensus sits on the guide) and **SRE** (half's rent roll and cost of debt in the 5 Oct update) are largely pre-released; **N91** (AUM pre-released 13 Oct; flows new); **GPW** (turnover public monthly). **MEGP** (first FY27 outlook), **BYG** (no Q2 statement; first board word on strategy since the activists), **CBF** (no pre-release) and **LGEN** (a new type of Q3 update) carry genuinely new lines; a likely guidance change is plausible only at MEGP.

Language notes worth quoting: GPW and CBF — the Polish sources carried nearly every load-bearing fact (dates, session timestamps, the ESOP EBITDA target, insider filings); SLR — the Spanish regulatory channel settled the date question while English aggregators carried only the unsupported 16 Nov date; UK names — domestic RNS added only small details (APN's "prudent to maintain" wording and consensus table, N91's staff-vehicle purchases).

This is research, not investment advice. It is a forecasting exercise over public information and must not be presented as advice.
