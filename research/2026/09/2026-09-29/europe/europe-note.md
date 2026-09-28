# Stage EU — Europe ranking for Tuesday 2026-09-29

Sealed Mon 2026-09-28, 13:39–13:50 UTC, while the European markets were **still trading**.
Every sealed spot and run-up is an **intraday price, not a close**. The realised move is
measured from daily bars by `eu_resolve.py`, never from the sealed spot.

## Answer first

**Nothing clears the conviction floor of 3.0 points.** The largest key is CARD at −1.10.
This is a day of small numbers, and across the whole US sample the sign was a coin flip
below the floor. The ranking key is `impact_sum`, as `edge-scores.json` reports it.

| # | name | market | session | `impact_sum` | pre-lessons | `abs_move_pct` | `p_up` | lean | anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2GB 2G Energy | de | bmo (08:30 pattern) | **+0.70** | +0.5 | 7.0 | 55 | −0.23 | truncated zero |
| 2 | BAG A.G. Barr | uk | bmo (confirmed) | **0.00** | +0.1 | 3.5 | 50 | −0.01 | truncated zero |
| 3 | GNFT Genfit | fr | **amc** (sealed bmo?) | **0.00** | 0.0 | 6.0 | 50 | +1.56 | register unreadable |
| 4 | HBH Hornbach Holding | de | bmo (confirmed) | **−0.10** | −0.15 | 3.0 | 48 | −0.04 | truncated zero |
| 5 | ADX Audax Renovables | es | bmo (CNMV-confirmed) | **−0.25** | −0.2 | 4.0 | 47 | +0.36 | none (no register) |
| 6 | SERI Seri Industrial | it | **amc** (sealed bmo?) | **−0.25** | −0.3 | 2.5 | 45 | +0.09 | truncated zero |
| 7 | CBG Close Brothers | uk | bmo (calendar) | **−0.30** | −0.2 | 6.5 | 48 | +2.32 | **FCA 4.11%** |
| 8 | MTEC Made Tech | uk | bmo (confirmed) | **−0.70** | −1.0 | 6.0 | 44 | −0.95 | truncated zero |
| 9 | CARD Card Factory | uk | bmo (confirmed) | **−1.10** | −1.5 | 8.0 | 43 | +1.77 | **FCA 2.48%** |
| — | MTL Metals Exploration | uk | bmo if it lands | not ranked | 0.0 | 3.0 | 48 | −0.03 | truncated zero |

**Top name, 2GB (+0.70).** The hunter found no hard unpriced fact. The +0.70 is the net of
two findings.

- **+1.3, positioning.** A single, widely syndicated Parmantier Sell note (25 Sep) lowered
  the public H1 bar just before the print: "Sehr schwaches erstes Halbjahr erwartet: Umsatz
  von € 140–150 Mio. …, EBIT um die Nulllinie" (very weak first half expected: revenue of
  €140–150m, EBIT around break-even). Source:
  <https://www.eqs-news.com/news/research/original-research-2g-energy-ag-von-parmantier-cie-gmbh-verkaufen/2a94ff5b-b1c2-4b14-b6f3-866f43429fe6_de>.
  The stock then fell 10.6% over 24–25 Sep. The last three scheduled releases led with
  orders and closed up 6.7% to 7.9%.
- **−0.6, guidance.** The FY26 guide of €490m needs roughly +50% H2 revenue. Management
  narrowed guidance at the H1 report in Sep 2025 and cut it in Oct 2025, so a trim is a
  real minority risk.

The bar rests on that one note, so `print_vs_bar_pct` is 0.

**Bottom name, CARD (−1.10).** Card Factory's interim is the first restatement of the FY27
guide since 28 April, which was "in line with" the company-compiled consensus of £58.2m
adjusted PBT. Since then the high street ran −1.5% (May), −6.2% (June) and −3.8% (July).
- Guide source: <https://www.investegate.co.uk/announcement/rns/card-factory--card/preliminary-results/9540520>.
- Footfall sources: BRC <https://brc.org.uk/news-and-events/news/corporate-affairs/2026/ungated/footfall-hit-by-record-sunshine/> and Retail Gazette <https://www.retailgazette.co.uk/blog/2026/08/footfall-brc-july-2026/>.

The hunter treats the macro-to-company link as a hypothesis and sizes the guidance finding
at −1.3, against a −9% median move for a real guidance change. A +0.2 finding offsets part
of it: Aberforth absorbed the Wellcome Trust's exit, taking its stake to 14.7% on 21 Sep.
The name is short 2.48% on the FCA register, flat.

**Not ranked: MTL, date unconfirmed.** Metals Exploration has no Notice of Results. Its AIM
Rule 18 deadline is 30 Sep, so the interims could land on 29 or 30 Sep. The hunter set
`event_confirmed: false` and the scorer held the name out.

## Session: two names were sealed on the wrong window

**GNFT and SERI release after the close, so the sealed bmo window almost certainly
contains no release.** For both, read the amc window, close(09-29) → close(09-30), at
resolve time.
- **Genfit:** every scheduled results filing in the AMF flux landed after the 17:35 close.
  H1 2024 and H1 2025 were both at 20:10Z.
- **Seri:** the issuer releases board outcomes in the evening. The half-year board is on
  29/09, per the issuer's calendar and Borsa Italiana's CDA_today.pdf.

**The other sessions:**
- **Sealed `session_unresolved`, settled bmo by the hunters:** 2GB (08:30 CET pattern, the
  exact time not announced), CBG (issuer calendar plus consistent 07:00 RNS), ADX (CNMV OIR
  42760: "antes de la apertura de mercado", before the market opens) and MTL (07:00 if it
  lands).
- **Vendor-flagged bmo, confirmed by the issuer's own notice:** BAG, CARD, HBH and MTEC.

## Selection and instrumentation

- **Funnel:** 31 scheduled → 10 eligible above $200k/day → 10 hunted. `selection.method`:
  "all 10 eligible names (at or under the cap)", so no random draw was needed.
  - `by_market`: uk 5, de 2, fr 1, it 1, es 1; se/dk/no/fi/pl 0.
- **`market_concentration`: the UK is 0.50 of the day across 5 markets.** Half the day is
  one market, which is a correlated exposure the scorer cannot see.
- **Options:** `options` is null for all ten names. Europe runs in the anchor-less regime
  that `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers by market:**

  | market | register | state |
  | --- | --- | --- |
  | uk | FCA | read, as of 2026-09-25 |
  | de | Bundesanzeiger | read |
  | it | CONSOB | read |
  | fr | AMF | **unreadable today**: data.gouv.fr reset on every retry and there was no cache for the day, so GNFT sealed with no positioning anchor |
  | es | none | no register reachable |

  **`anchor_covered: true` on 2 of 10: CARD (2.48%) and CBG (4.11%, +0.20pp, building).**
  The other seven that were read are truncated zeros, not measurements.
- **Spain and Poland: 1 name (ADX).** It has no positioning anchor, and its lean is the
  run-up, which is the free control.
- **Kills that cannot be reached:**
  - **Germany: 2 names (2GB, HBH).** `event_occurred: false` is unreachable.
  - **Italy and France:** it is unreachable by design for these too.
  - **ADX may be the exception.** The ADX hunter reports that the CNMV
    `resultado-oir` / `resultado-ip` listing pages returned 200 with dated filings, so Spain
    may be confirmable after all. That is **unverified by code** and nothing here relies
    on it.
- **`history.basis`:** it is `observed_rns` for the five UK names. It is an
  **estimated cadence** for 2GB, HBH, GNFT, SERI and ADX, which is a scale and not a
  record of dates.
- **`lean_vs_free_control_rho`, pooled per run from the previous resolved runs:** 0.69
  (09-22), 0.943 (09-23), 0.70 (09-24). The 09-25 file carries none. The lean's weights are
  priors borrowed from the US runs and have been measured nowhere in Europe.

## What each release carries (`already_public` / `new_in_release`)

- **Pre-released periods, where the move should be small unless the guide moves:**
  - **BAG:** H1 trading update on 4 Aug.
  - **HBH:** Q2 and 6M by ad-hoc on 7 Sep, with the FY guide maintained.
  - **MTEC:** FY26 trading update on 30 Jun; the FY27 guide was raised on 18 Aug.
  - **MTL:** Q2 update on 16 Jul.
- **New numbers with a live guide question:**
  - **CARD:** nothing pre-released since April.
  - **CBG:** first FY27 guide, and the dividend under the motor-finance tribunal.
  - **2GB:** H1 has never been pre-released.
  - **ADX:** Q1 adjusted EBITDA was +0.6% against a double-digit 2026 guide.
- **SERI is a special case.** A merger into its parent and a delisting were announced on
  6 Aug, with a withdrawal price of €2.556 against a spot of €2.325. The stock trades on
  that gap, not on results.

## `language_note` highlights (prose, not ranked)

- **HBH:** only the German consumer and regional press (t-online, ms-aktuell) carried the
  clearance sale at 111 Hellweg/BayWa stores. That is Hornbach's home market, during its Q3.
- **ADX:** only the Spanish CNMV filings carried the release timing and the buyback
  suspension "por fines corporativos" (for corporate purposes).
- **SERI:** almost everything came only from Italian sources: the covenant breaches, the
  liquidation petition with a 20 Oct hearing, and the rules for the withdrawal exit.
- **GNFT:** the French sources settled the session and showed short interest building to
  about 1.1%.
- **UK names:** the domestic RNS sources mainly carried the bar (CBG's consensus PDF) and
  holder changes.

## What this is and is not

One day is not a result. Nine small keys, none above the floor, half of them from one market.
The pre-lessons control is live on 7 of 10 names. Resolve from 2026-09-30 for the bmo names
and from 2026-10-01 for GNFT and SERI, because Yahoo's `.PA`/`.DE` closes lag.

No orders were placed or considered. This stage reads no broker.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
