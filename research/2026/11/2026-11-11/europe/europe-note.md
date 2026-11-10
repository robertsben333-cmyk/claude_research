# Stage EU — Europe researcher, event date 2026-11-11

Sealed 2026-11-10 ~14:46 UTC, while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The scored window is close(2026-11-10) → close(2026-11-11) for bmo names, which `eu_resolve.py` measures from daily bars. Ranking key: `impact_sum` (from `edge-scores.json`). Conviction floor: 2.8.

**Answer first:** no name reaches the 2.8 floor. The day's largest hunter number is FNM at +1.90. The four-model panel selects two names: **FNM long** (all four judges at the top of their own range) and **EIN short** (4 of 4). Over the whole US sample, the sign below the floor was a coin flip, and one day is not a result.

## Ranked table

| # | ticker | mkt | session | impact_sum | abs_move | p_up | impact_scaled | anchor | history |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FNM | se | bmo | +1.90 | 9.0 | 58 | +1.44 | no | est. |
| 2 | BNR | de | bmo? | +1.30 | 5.0 | 55 | +0.50 | yes | est. |
| 3 | ADN1 | de | bmo? | +0.80 | 5.5 | 51 | +0.11 | no | est. |
| 4 | CRE | uk | bmo? | +0.50 | 4.0 | 58 | +0.64 | yes | observed_rns |
| 5 | VWS | dk | bmo | +0.50 | 8.0 | 52 | +0.32 | yes | est. |
| 6 | GYC | de | bmo? | +0.40 | 5.0 | 52 | +0.20 | no | est. |
| 7 | ICG | uk | bmo | +0.35 | 4.0 | 52 | +0.16 | yes | observed_rns |
| 8 | DIGIS | es | bmo? | +0.30 | 4.5 | 52 | +0.18 | no (es: none) | est. |
| 9 | PST | it | bmo? → **amc** | +0.10 | 3.0 | 51 | +0.06 | no | est. |
| 10 | ALZCUR | se | bmo? | +0.00 | 4.5 | 48 | −0.18 | no | est. |
| 11 | RWAY | it | bmo? (in-session) | +0.00 | 2.3 | 51 | +0.05 | no | est. |
| 12 | KWS | de | bmo? | −0.15 | 3.5 | 46 | −0.28 | no | est. |
| 13 | DFDS | dk | bmo | −0.40 | 8.0 | 48 | −0.32 | yes | est. |
| 14 | BEAMMW_B | se | bmo? | −0.50 | 7.5 | 48 | −0.30 | no | est. |
| 15 | FNTN | de | amc | −0.60 | 4.0 | 47 | −0.24 | yes | est. |
| 16 | RBREW | dk | bmo? → **amc** | −1.00 | 5.5 | 46 | −0.44 | yes | est. |
| 17 | EIN | de | bmo? | −1.30 | 6.0 | 42 | −0.96 | no | est. |
| 18 | PRT | it | bmo? → **amc** | −1.40 | 7.5 | 46 | −0.60 | no | est. |
| 19 | V1NC | de | bmo? | −1.40 | 6.0 | 45 | −0.60 | no | est. |

`impact_scaled` is the hunter's second, separate measurement: (2·p_up/100 − 1)·abs_move. It is not the key, and nothing should be ranked on it.

**Not ranked:** OKEA (no) is a **phantom**. Oslo NewsWeb shows its Q3 2026 results went out on 2026-11-03 at 05:00 UTC (messageId 685404), and nothing is published or scheduled for 11-11. It should resolve as `event_occurred: false`.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran, with no fallback. Selection rule: 3 of 4 judges put the name in their own top 20%. Two caveats on how the judges read their inputs:

- The Sonnet 5.5 judge says it applied the shared core and `LESSONS.md` without opening the per-market hunter definitions.
- The Opus 5 and Opus 5.5 judges read some definitions only in part.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FNM | **yes** | 100 | long | 0 | 100L* | 100L* | 100L* | 100L* | 4 | +4.27 | +1.90 |
| 2 | EIN | **yes** | 88 | short | 5 | 80S* | 94S* | 90S* | 90S* | 4 | −1.61 | −1.30 |
| 3 | V1NC | | 86 | short | 6 | 80S | 79S | 94S* | 90S* | 2 | −1.39 | −1.40 |
| 4 | PRT | | 79 | short | 10 | 68S | 72S | 94S* | 80S* | 2 | −1.13 | −1.40 |
| 5 | RBREW | | 66 | short | 17 | 39S | 68S | 72S | 85S* | 1 | −0.97 | −1.00 |
| 6 | DFDS | | 60 | short | 14 | 44S | 62S | 52S | 80S* | 1 | −0.80 | −0.40 |
| 7 | VWS | | 39 | long | 28 | 0- | 34L | 80L | 42L | 1 | +0.48 | +0.50 |
| 8 | BNR | | 66 | long | 13 | 44L | 79L | 72L | 72L | 0 | +1.03 | +1.30 |
| 9 | BEAMMW_B | | 56 | short | 19 | 28S | 52S | 78S | 66S | 0 | −0.80 | −0.50 |
| 10 | CRE | | 58 | long | 5 | 64L | 52L | 61L | 53L | 0 | +0.80 | +0.50 |
| 11 | FNTN | | 49 | short | 12 | 36S | 48S | 68S | 45S | 0 | −0.62 | −0.60 |
| 12 | ADN1 | | 44 | long | 5 | 37L | 50L | 42L | 50L | 0 | +0.59 | +0.80 |
| 13 | ICG | | 40 | long | 17 | 20L | 26L | 60L | 53L | 0 | +0.52 | +0.35 |
| 14 | GYC | | 34 | long | 15 | 42L | 27L | 52L | 14L | 0 | +0.45 | +0.40 |
| 15 | KWS | | 24 | short | 15 | 7S | 12S | 33S | 45S | 0 | −0.28 | −0.15 |
| 16 | DIGIS | | 19 | long | 8 | 11L | 18L | 16L | 32L | 0 | +0.24 | +0.30 |
| 17 | RWAY | | 8 | long | 5 | 14L | 4L | 3L | 14L | 0 | +0.13 | +0.00 |
| 18 | PST | | 3 | long | 3 | 0- | 0- | 6L | 4L | 0 | +0.04 | +0.10 |
| 19 | ALZCUR | | 2 | short | 4 | 0- | 8S | 0- | 0- | 0 | +0.00 | +0.00 |

Where each judge's own top 20% starts: opus5 |1.17|, opus55 |0.90|, sonnet55 |0.70|, fable51 |0.96|, each on 200 live sizes.

**FNM (selected, long).** Volvo CE is Ferronordic's supplier. Its Q3 report of 2026-10-23 shows North America deliveries of 1,911 against 1,352 (+41%) and orders up 80%. That came a week after the only sourceable bar: ABG's commissioned preview, which expects sales of SEK 1,178m and adjusted EBIT of SEK 46m (https://www.volvogroup.com/content/dam/volvo-group/markets/master/news/2026/oct/5449150-volvo-group---report-on-the-third-quarter-2026.pdf). ABG under-called Q2 by 34% on sales (https://borsvarlden.com/artiklar/ferronordic-earnings-beat-across-the-board-abg). The case against:

- The deliveries go to Volvo's dealers. They are partly a reversal of 2025 destocking and partly a possible inventory build at Rudd, which could show up as weak cash flow.
- Management pre-tempered the quarter: "quarters will vary".
- Diesel is +68% year on year.
- Turnover is thin at $122k a day, and the single bar is commissioned research.

**EIN (selected, short).**

- On the company's own numbers the EUR 1.2bn revenue guide is under strain: H1 grew +0.9%, so H2 needs about +6.9% (https://www.einhell.com/fileadmin/com/investor-relations/reports/interim-reports/en/einhell-half-year-financial-report-2-2026.pdf).
- Bunnings, which carries Einhell's Australian business, said on 29 Oct that growth "has moderated" (https://www.raskmedia.com.au/2026/10/29/wesfarmers-asxwes-share-price-falls-4-after-weakening-sales-in-agm-update/).
- The name has sold its last confirmations.

The case against: Hornbach's Jun–Aug sales rose +7.3% (https://retail-news.de/hornbach-q2-2026-27-umsatz-ebit-prognose/), a 9.7% H1 margin keeps the pre-tax guide reachable, no ad-hoc has been filed, and the stock already fell from about 75 to about 62 after H1. EIN has no positioning anchor; the German register does not name it.

**Where the panel and the hunter disagree most:** nothing crosses the floor, so there is no unselected floor-clearer.

- **V1NC and PRT** carry the hunter's largest negatives (−1.40 each). Both sit near the top of the panel at 86 and 79, but only 2 of 4 judges put each in their own top 20%.
- **BNR** is the hunter's #2 (+1.30), but no judge puts it in its top 20%.
- **VWS** is the widest disagreement (sd 28): Opus 5 sizes it at exactly zero, and Sonnet 5.5 puts it at its 80th percentile.

**What these numbers are not.** `panel_score` ranks; it does not forecast. There is no `expected_edge_pct` off the US. `p_up` is recorded and decides nothing. Each member's scale is still mostly the frozen E-P seed until Europe has about 200 panel names of its own. The EU panel has no measured edge: ρ +0.22, p 0.19 on 45 names (2026-10-21). In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established.

## Bottom names in the hunter ranking

- **V1NC (−1.40).** There is no Q3 order announcement, although the company published one for June (https://vincorion.com/en/wp-json/wp/v2/posts?per_page=30&_fields=date,link,title). Order intake was the line behind the +9.9% on the H1 day. Rheinmetall's cut on 5 Nov delays the Bundeswehr Boxer order (https://www.rheinmetall.com/de/media/news-watch/news/2026/2026-11-05-rheinmetall-pressemitteilung-quartalsmitteilung-q3). Revenue was pre-released on 7 Oct.
- **PRT (−1.40).** Kepler Cheuvreux nearly doubled its FY26 net-debt estimate, from €26m to €50m, on an inventory build (https://www.teleborsa.it/News/2026/11/04/esprinet-kepler-cheuvreux-taglia-target-price-e-vede-aumento-debito-con-accumulo-scorte-133.html). IDC has Q3 PC units −20.1%.

## Session corrections: read these before resolving

The sweep does not run in this stage, so sessions marked `bmo?` were assumed. Three hunters cite timestamps showing the release lands **outside** the sealed bmo window. All three need both windows measured, and the post-close window is the one that holds the print:

- **PRT** (Esprinet): the board meets on 11 Nov and past releases went out at about 18:10 CET. Window: close 11 Nov → close 12 Nov.
- **RBREW** (Royal Unibrew): Q3 2025 went out at 17:06 CET, H1 2026 at 17:11 and the annual report at 17:28. Window: close 11 Nov → close 12 Nov.
- **PST** (Poste Italiane): the 11 Nov date is the board meeting. The release lands around 07:00 on **12 Nov**, so the sealed window holds no print.

Two more need care:

- **RWAY** (Rai Way) releases inside the 11 Nov session at about 15:30–16:30 CET, with the call at 18:00. The sealed window holds only about an hour of reaction.
- **FNTN** was sealed amc (close 11 Nov → close 12 Nov), so it is not on the same day as the rest.

The other names marked `bmo?` were confirmed bmo by their hunters, from the issuer's own calendar plus earlier release stamps: ADN1, ALZCUR, BEAMMW_B, BNR, CRE, DIGIS, EIN, GYC, KWS and V1NC.

## What this day is, and what it is not

- **Selection:** a random sample of 20 from 40 eligible names, seed `eu-2026-11-11`. 71 names were scheduled across the ten markets above the $100k floor.
  - Hunted by market (`by_market`): de 7, se 3, dk 3, it 3, uk 2, no 1, es 1; fr 0, fi 0, pl 0.
  - Eligible by market: de 13, se 7, it 6, dk 5, uk 4, no 3, fi 1, es 1.
  - **Warsaw was shut** (Independence Day, `market_closed: exchange holiday`).
- **Market concentration:** Germany is the largest market at 35% of the names (7 of 20), and 7 markets are represented. That is not one market's day, but the German names share a macro read.
- **Calendar sources:**

  | source | names |
  | --- | --- |
  | vendor + EQS events | 5 |
  | vendor + Inderes | 5 |
  | vendor only | 4 |
  | EQS events only | 2 |
  | Euronext Oslo | 1 (OKEA, the phantom) |
  | Inderes only | 1 |
  | RNS | 1 |
  | vendor + RNS | 1 |

- **Options:** null in all ten markets. Europe runs in the anchor-less regime, which on the sealed US corpus produced ρ +0.073, p 0.45 over 104 events.
- **Short registers:**
  - Resolved: de, dk (as of 30-10), it, no, se and uk.
  - es: none reachable. fr: no names today.
  - **7 of 20 names carry `anchor_covered: true`**: BNR, CRE, DFDS, FNTN, ICG, RBREW and VWS. PRT's baseline reads 0.0 / not covered, but its hunter found Citadel at 0.59% in the CONSOB file (the baseline's issuer-name join failed). The sealed baseline is left as sealed.
  - Every other zero is a truncated zero at the 0.5% threshold, not an anchor.
  - Danish shorts are on a 0.1% scale and are not comparable with anyone else's.
- **Spain and Poland:** 1 name (DIGIS, es) has no positioning anchor and can never be confirmed or killed after the fact. Poland was closed.
- **Germany:** 7 names cannot reach `event_occurred: false` (EQS has no whole-day query). Italy (3) cannot either.
- **Nordic resolve deadline:** the Nordic names (SE ×3, DK ×3) must be resolved within about a week, because of the Nasdaq Nordic feed's paging limit.
- **History basis:** UK (CRE, ICG) is `observed_rns` and OKEA is `observed_newsweb`. **The other 17 are `estimated_from_cadence`**: a scale, not a record of dates. VWS and FNTN's hunters both found their baseline's reaction history mis-dated; FNTN's counted an ex-dividend day as a print.
- **Lean:** `lean_vs_free_control_rho` in the last resolved run (2026-10-16) was se 0.60, the only market reported. The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.
- **Already public vs new in release** (number of items per hunter, in the hunts):
  - Pre-released: ALZCUR's Q3 revenue (August licence payment) and V1NC's Q3 revenue (7 Oct ad-hoc).
  - Disclosed beforehand: VWS's order miss (1 Oct).
  - Likely guidance changes, the line where hunters put the move: EIN (revenue guide strain), BNR (narrowing toward the upper half), GYC (possible raise on the LEG stake), VWS (consensus above the guide midpoint), and RBREW and FNTN (both narrowing lower).
- **What the local-language sources added (`language_note` highlights):**
  - BNR: the German dpa-AFX notes carried the only sourced Q3 bar.
  - PRT, PST and RWAY: Italian sources carried the release timestamps that corrected the session, plus PRT's Citadel short.
  - DIGIS: only the issuer's Spanish IR page carried the correct date.
  - BEAMMW_B: the Swedish insider register showed a founder converting 567k A shares to B before the closed period.
  - The Nordic issuers otherwise added nothing beyond their English filings, as expected.
- **Controls:** the `pre_lessons` freeze ran on all 20 hunts. The `pre_local` control is retired, so `eu_resolve.py`'s language-pass section will report 0 names.
- **Provenance:** uk.v7, de.v7, nordic.v5, it.v5, es.v5, all on claude-opus-5-5 (from the alias timeline).
- **One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
