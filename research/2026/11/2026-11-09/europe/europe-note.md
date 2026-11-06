# Stage EU — Europe ranking for 2026-11-09 (Mon)

I sealed the baselines on Fri 2026-11-06 at about 14:45 UTC (15:45 Amsterdam), roughly two
hours before the European close. Every sealed spot and every `run_up_20d_pct` is an
**intraday price, not a close**. The ranking key is `impact_sum`, read from the
`ranking_key` field of `edge-scores.json`. The conviction floor is 2.8.

**No name clears the floor.** The top of the ranking is IOT (SECO, Milan) at +2.10 and the
bottom is TEN (Ten Square Games, Warsaw) at −0.90.

- All 16 names were hunted. There were 16 eligible names against a cap of 20, so there was
  no random draw. Every hunt finished its search (`search_complete`).
- 13 names are ranked. Three have **no event in the window**:
  - **ALCLS**: Cellectis has not announced a Q3 date, and it releases after the US close.
  - **EGLA** is a phantom date. Its board meets on **2026-11-16**, per the issuer's 2026
    calendar and its IR page.
  - **REC** is a duplicate. Record plc's interims came out on 11-06 (ranked in that run);
    11-09 is only an investor presentation.
- **The four-model panel selected one name: IOT, long, 3 of 4 judges (`panel_pct` 88).**
- **Six names release after the sealed window.** PAT, NTG, DOV, PHN, NWL and TEN release
  after the 11-09 close or before the 11-10 open, per the issuers' own release-time
  history. So most of the day's real reactions fall in close(11-09) → close(11-10), not in
  the sealed bmo window. `session_check` opens with `amc` on each of them, which is what
  `eu_resolve.py` reads.

This stage places no orders and reads no broker.

## Ranked

| # | ticker | market | session (checked) | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history | pre-released / guide change? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | IOT | it | bmo? → **in-session 11-09** (~10:00–11:45 board-day filings; call 14:30) | +2.10 | 8.0 | 57 | +1.12 | no | estimated | Q3 not pre-released (guided ~€60m); **first Q4 guide is new** |
| 2 | PAT | de | bmo? → **amc 11-09** (17:37–17:42 pattern; 2025's 9M raise came intraday) | +1.80 | 5.5 | 59 | +0.99 | no | estimated | no; guide raise is the base case |
| 3 | NWL | it | bmo? → **10-11 bmo** (08:05 the day after the board) | +1.20 | 7.0 | 54 | +0.56 | no | estimated | no; Tosano deal public 11-05 |
| 4 | HNR1 | de | bmo (07:30 pattern) | +1.00 | 4.0 | 56 | +0.48 | no | estimated | no; guide raise plausible; 2027 target at the 11-25 investor day |
| 5 | NTG | dk | bmo? → **amc 11-09** (17:01–17:05 pattern) | +0.55 | 3.0 | 52 | +0.12 | yes (1.18%, 0.1% threshold) | estimated | **yes**: Q3 pre-released and guide raised 10-26 |
| 6 | PHN | it | bmo? → **amc 11-09** (17:40–18:38 pattern) | +0.20 | 8.5 | 53 | +0.51 | no | estimated | no |
| 7 | UCG | it | bmo (date moved to 11-09 by issuer notice; call 10:00 CET) | +0.20 | 4.5 | 52 | +0.18 | no | estimated | no; third guide raise plausible |
| 8 | G1A | de | bmo (pattern) | +0.00 | 3.5 | 47 | −0.21 | yes (0.51%, stale) | estimated | no Ad-hoc, so likely in line |
| 9 | KNOS | uk | bmo (07:00) | −0.05 | 5.0 | 51 | +0.10 | yes (0.21%) | observed_rns | direction pre-signalled by 08-18 upgrade |
| 10 | DOV | it | bmo? → **amc 11-09** (18:15–21:59 pattern) | −0.10 | 6.0 | 48 | −0.24 | no | estimated | FY26 guide already cut 10-08 |
| 11 | HYQ | de | bmo (07:10 pattern) | −0.60 | 4.5 | 47 | −0.27 | yes (2.65%, covering) | estimated | **yes**: Q3 GP/EBIT ad-hoc 10-26; only guide language new |
| 12 | ALM | es | bmo (pattern; 10:00 call) | −0.70 | 4.5 | 45 | −0.45 | no (no register) | estimated | no; low-end steer likeliest |
| 13 | TEN | pl | amc (17:03–17:04 pattern) | −0.90 | 5.0 | 46 | −0.40 | no (no register) | estimated | **yes**: Q3 bookings public 10-05 |
| — | ALCLS | fr | no release in window; amc issuer | not ranked | 4.0 | 50 | — | no | estimated | no Q3 date announced |
| — | EGLA | it | **phantom**: board 2026-11-16 | not ranked | 2.0 | 50 | — | no | estimated | — |
| — | REC | uk | **duplicate**: interims 2026-11-06 | not ranked | 0 | 50 | — | no | observed_rns | printed in the 11-06 run |

`bmo?` marks a name sealed with `session_unresolved`.

- **NWL** releases at about 08:05 on 11-10, before the open. Its reaction is close(11-09) →
  close(11-10), which is also the window the amc reading gives.
- **IOT** releases inside the 11-09 session, so the sealed window holds its whole reaction.
- **UCG**'s board meets on Sunday 11-08, so its release lands before the 11-09 open either way.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.**

- All four members ran on their pinned agents, 13 of 13 names each, with no fallback.
- `selected` means 3 of 4 judges put the name in their own top 20% on the panel's side.
- `pct` (`panel_pct`) is 0–100: the size of the mean of the four judges' signed
  percentiles. Each judge's percentile is read against that judge's own live range.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | IOT | **yes** | 88 | long | 16 | 94L* | 98L* | 61L | 97L* | 3 | +2.23 | +2.10 |
| 2 | PAT | | 75 | long | 18 | 58L | 93L* | 55L | 94L* | 2 | +1.34 | +1.80 |
| 3 | HNR1 | | 74 | long | 14 | 61L | 96L* | 70L | 66L | 1 | +0.96 | +1.00 |
| 4 | TEN | | 66 | short | 14 | 48S | 86S* | 60S | 68S | 1 | −0.91 | −0.90 |
| 5 | HYQ | | 60 | short | 17 | 34S | 78S | 57S | 72S | 0 | −0.93 | −0.60 |
| 6 | NWL | | 59 | long | 8 | 52L | 72L | 61L | 53L | 0 | +0.82 | +1.20 |
| 7 | G1A | | 44 | short | 13 | 56S | 50S | 22S | 45S | 0 | −0.65 | +0.00 |
| 8 | ALM | | 45 | short | 8 | 50S | 54S | 32S | 45S | 0 | −0.63 | −0.70 |
| 9 | UCG | | 39 | long | 17 | 10L | 54L | 50L | 42L | 0 | +0.60 | +0.20 |
| 10 | PHN | | 35 | long | 24 | 56L | 4L | 61L | 20L | 0 | +0.51 | +0.20 |
| 11 | DOV | | 16 | long | 24 | 20S | 45L | 16L | 23L | 0 | +0.29 | −0.10 |
| 12 | NTG | | 27 | long | 16 | 16L | 54L | 25L | 12L | 0 | +0.28 | +0.55 |
| 13 | KNOS | | 10 | long | 4 | 6L | 17L | 8L | 12L | 0 | +0.16 | −0.05 |

`*` = in that judge's own top 20%. Own-top-20% thresholds: opus5 |1.20|, opus55 |0.84|,
sonnet55 |0.72|, fable51 |0.96|. Each rests on 200 live sizes of this market's history.

**IOT (selected, long, 3 of 4).**
- **The case for:** every judge rested on the same items.
  - The Q4 guide is a genuine scheduled guidance event from a company that guides one
    quarter ahead.
  - SECO's own H1 deck shows order intake up 55% year to date to July and a book-to-bill
    of 1.4x ([source](https://www.emarketstorage.it/sites/default/files/comunicati/2026-09/20260908_188854.pdf)).
  - Advantech's accelerating Q3 is an independent series pointing the same way.
  - The stock fell 6.2% in the five sessions into the print.
- **The strongest case against** is the one Sonnet 5.5 sized lowest:
  - Q1 2026 printed at the low end of its guide, and the stock fell 3.5% and then 4.4%.
  - The 60-session run-up is +24%, so an in-line €60m quarter may not be enough.
  - There is no sourced EBITDA consensus.
  - The −8.6% on 11-04 has no filing or news behind it.

**Where the panel and the hunters disagree most:**
- **G1A:** the hunter netted to 0.00; the panel leans short at 44. Opus 5 sized the
  missing Ad-hoc at −0.72.
- **DOV:** the hunter is −0.10; three judges lean long. Opus 5 leans short, so the spread
  is 24.
- **PHN:** the panel spread is 24. Opus 5.5 is at the 4th percentile and Opus 5 and Sonnet
  5.5 at the 56th–61st.

**What these numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- This market's member scales are still young.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.

## The top and the bottom

**Top, IOT +2.10.** The largest finding (+1.2, lands on guidance) is SECO's own H1 deck:
"Order intake +55% YoY and book-to-bill consistently above 1x build backlog and revenue
visibility" (original in English;
[source](https://www.emarketstorage.it/sites/default/files/comunicati/2026-09/20260908_188854.pdf)).
- Q3 was guided at about €60m and not pre-released.
- The release carries the first Q4 guide, against €51.2m a year earlier.
- `language_note`: the CFO's "circa 1x" leverage line after the quarter close appeared only
  in the Italian refinancing release body, and the release timestamps that settled the
  session came from the Italian filings.

**Bottom, TEN −0.90.** The largest finding (−0.5) is the monthly split in the Polish ESPI
bookings report 16/2026
([source](https://www.biznesradar.pl/a/159553,ten-square-games-sa-16-2026-informacja-o-kwartalnych-przychodach-platnosciach-ze-sprzedazy-3q-2026)).
- September group bookings were PLN 31.1m against 34.6m in August.
- Fishing Clash fell 19% month on month despite the stated marketing push.
- Medal Hunter took only 1.2m and 1.4m in its first two full months.
- The release will comment on October trading from that soft base.
- The quarter's bookings are already public, so that line is sized 0.
- There is no PAP consensus and no positioning anchor.

## What the day is, and is not

- **Selection:** "all 16 eligible names (at or under the cap)", seed `eu-2026-11-09`. There
  was no draw, because eligible (16) did not exceed the cap (20).
  - 22 rows were scheduled and 6 fell below the $100k floor.
  - Hunted by market: uk 2, de 4, fr 1, dk 1, it 6, es 1, pl 1; se, no and fi 0.
- **`selection.market_concentration`:** the largest market is Italy, at 6 of 16 (37.5%),
  across seven markets. Three of the six Italian names are no-event or after-window
  (EGLA phantom; DOV and PHN amc).
- **`session_unresolved` at the seal:** HYQ, PAT, NTG, ALCLS, DOV, EGLA, IOT, NWL, PHN,
  UCG, REC. Each hunter settled its session in `session_check`. Six came back as releasing
  after the sealed window, which is a reminder that the vendor's bmo flag is a guess.
- **Options:** `options` is null in all ten markets. Europe runs in the anchor-less regime
  (`archive/backtest/FINDINGS.md` §33: ρ=+0.073, p=0.45 over 104 events).
- **Short registers:**
  - Read: uk, de, fr, dk, it.
  - Unreachable by construction: es, pl.
  - No names today: se, no, fi.
  - **4 of 16 names carry `anchor_covered: true`**: G1A, HYQ, NTG and KNOS. Every other
    covered market's "0.0" is the 0.5% disclosure floor, not a measurement.
  - Denmark's register publishes from 0.1%, so NTG's 1.18% is not on the same scale.
- **Spain and Poland:** 2 names (ALM, TEN). They have no positioning anchor; their lean is
  the run-up, which is also the free control. Neither can be confirmed or killed after the
  fact.
- **Germany:** 4 names (G1A, HNR1, HYQ, PAT), none of which can reach
  `event_occurred: false`. Italy and France cannot either (Italy: eMarket STORAGE is not
  universal; EGLA files through 1INFO and is absent from it).
- **`lean_vs_free_control_rho`:** the most recent resolved run (2026-10-16) carries it only
  for se, at 0.60.
- **The lean's weights** are priors borrowed from the US runs and measured nowhere in Europe.
- **`history.basis`:** estimated (cadence) for every name except KNOS and REC
  (`observed_rns`). Several hunters found the cadence dates wrong:
  - G1A: FY on 03-09, not 02-09.
  - IOT: the Q3 2025 print was on 11-07, not 11-05.

  A cadence prior is a scale, never evidence that a print happened on a date.
- **Conviction floor:** no name is above 2.8. Over the whole US sample the sign was a coin
  flip below the floor.
- **Already public:**
  - HYQ: the Q3 ad-hoc of 10-26.
  - NTG: Q3 and the guide raise, 10-26.
  - TEN: Q3 bookings, 10-05.
  - KNOS: the direction, via the 08-18 upgrade.
- **Likely guidance change:** IOT (first Q4 guide), PAT and HNR1 (raise plausible), ALM
  (low-end steer), UCG (third raise plausible).
- **Resolve:** after 11-10 for the six amc names. Germany, Spain and Poland can never be
  killed; there are no Nordic names except NTG (resolve by ~11-16).
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
