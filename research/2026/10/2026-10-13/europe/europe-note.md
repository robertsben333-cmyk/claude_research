# Stage EU — Europe ranking for 2026-10-13

**The answer: there is no signal today. Five names could be ranked and none clears the 2.8
conviction floor. Every hunter's number sits between −1.0 and +0.9. GNC (Greencore) is the
top name at +0.90 and BWY (Bellway) the bottom at −1.00. The panel selected no name. A sixth
name, ENSI (EnSilica), was a phantom: its results came out on 5 October.**

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Monday 2026-10-12 at about 13:45 UTC, while the European markets were still
trading. Every sealed spot is therefore an **intraday price, not a close**. The realised move
is measured from daily bars, close(2026-10-12) → close(2026-10-13).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | uk | GNC | Greencore Group | **+0.90** (p53) | no | +0.45 (p44) | 4.5 | 55 | bmo, `session_unresolved` in the seal. The Q1, interim and Q3 updates all went out at 07:00 |
| 2 | uk | YOU | YouGov | **+0.40** (p30) | no | −0.80 (p60) | 10.0 | 46 | bmo. The issuer's notice dates it 13 Oct, and its prior results RNS went out at 07:00 |
| 3 | no | ABG | ABG Sundal Collier | **+0.20** (p16) | no | +0.21 (p26) | 3.5 | 53 | bmo. Oslo NewsWeb notice: 08:00 CEST |
| 4 | uk | BYIT | Bytes Technology | **−0.85** (p52) | no | −0.44 (p42) | 5.5 | 46 | bmo. The issuer's 17 Sep RNS dates it 13 Oct |
| 5 | uk | BWY | Bellway | **−1.00** (p57) | no | −0.48 (p45) | 8.0 | 47 | bmo, `session_unresolved` in the seal. The prior full-year results and interims went out at 07:00 |
| — | uk | ENSI | EnSilica | not ranked | — | — | 3.5 | 50 | no event: 13 Oct is an investor presentation of results released on 5 Oct |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. YOU's two numbers have opposite signs: the findings net to +0.4, but the hunter
put the name's results-day pattern into `p_up` (46). The bracketed figures are percentiles of
|value| among names sized by Opus 5.5. They describe scale, not rank.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own pinned `-intl-` agents, with no fallback, and each covered 5 of 5 packs.

| rank | ticker | selected | consensus_k | sign agreement | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | YOU | no | 1 | 4/4 | −0.76 | −1.14* | −0.41 | −0.65 | −0.88 | +0.40 |
| 2 | BYIT | no | 0 | 4/4 | −0.79 | −0.87 | −0.67 | −0.72 | −1.00 | −0.85 |
| 3 | GNC | no | 0 | 4/4 | +0.43 | +0.26 | +0.41 | +0.65 | +0.44 | +0.90 |
| 4 | BWY | no | 0 | 4/4 | −0.37 | −0.34 | −0.40 | −0.54 | −0.33 | −1.00 |
| 5 | ABG | no | 0 | 4/4 | +0.33 | +0.22 | +0.32 | +0.48 | +0.33 | +0.20 |

`*` marks a member's own top 20%. Only Opus 5 put any name there (YOU), so **no name is
selected** (the rule is 3 of 4). All four members agree on the sign of every name. On its
own, sign agreement carried nothing in the judge lab (127 of 151 names, 50%).

The members' sizes, as `impact_sum` / `abs_move_pct` / `p_up`:

| ticker | Opus 5 | Opus 5.5 | Sonnet 5.5 | Fable 5.1 |
| --- | --- | --- | --- | --- |
| YOU | −2.20 / 11.0 / 40 | −0.54 / 9.0 / 47 | −0.72 / 9.0 / 46 | −1.26 / 9.0 / 43 |
| BYIT | −1.68 / 7.0 / 38 | −0.88 / 5.5 / 42 | −0.80 / 5.0 / 42 | −1.44 / 6.0 / 38 |
| GNC | +0.50 / 5.0 / 55 | +0.54 / 4.5 / 56 | +0.72 / 4.5 / 58 | +0.63 / 4.5 / 57 |
| BWY | −0.65 / 6.5 / 45 | −0.52 / 6.5 / 46 | −0.60 / 6.0 / 45 | −0.48 / 6.0 / 46 |
| ABG | +0.42 / 3.5 / 56 | +0.42 / 3.5 / 56 | +0.54 / 4.5 / 56 | +0.48 / 4.0 / 56 |

**Where the panel and the hunter disagree most:** on YOU. The hunter's `impact_sum` is
+0.40, while all four judges are negative and Opus 5 is the most negative (−2.20). The judges
weighted the name's last three results days (−11.3%, −10.6%, −11.6%) and the 67% rise since
March more heavily than the content findings. The hunter's own `impact_scaled` (−0.80) agrees
with the judges, not with its key. No name is above the floor, so there is no unselected
floor-clearer to report.

What these numbers are not:

- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed, until Europe has about 200 panel
  names of its own.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.

## Top and bottom

**Top, GNC +0.90** (Greencore, Q4/FY26 trading update). The largest findings are each
+0.4:

- The company's own Q3 RNS said Q4 "started positively, with strong volume momentum".
- Greggs' Q3 (like-for-like +3.4% over the same 13 weeks) points to the upper half of the
  £234–242m operating-profit guide. The Vuma consensus of £237.99m sits at its midpoint.

Two things hold the number back:

- GNC is up 6.07% over the last 5 sessions.
- Shorts are building slightly: the FCA register reads 2.89%, up 0.10 points.

Sources:
[Greencore RNS list on Investegate](https://www.investegate.co.uk/company/GNC) and the
issuer's 28 Aug notice moving the date from 8 Oct to 13 Oct. The reason for the move is
unexplained, and the hunter sized it at 0.

**Bottom, BWY −1.00** (Bellway, FY26 results plus the first FY27 guide). FY26 was
pre-released on 11 Aug, so the move lives in three lines:

- **FY27 volume guide:** the order book is 21% smaller (4,206 homes against 5,307). Zoopla
  shows sales agreed −9% and the five-year fix at 5.2%. Sized −1.0.
- **FY27 margin guide:** incentives are up and build costs are rising again. This is the line
  on which BWY fell 17.5% at the interims. Sized −1.0.
- **Offsets, +0.5 each:** a likely top-up above the £50m "initial tranche" of returns, and the
  first company read on the 28 Sep "Your First Home" scheme.

Source:
[11 Aug trading update](https://www.investegate.co.uk/announcement/rns/bellway--bwy/trading-update/9714330).

**One finding worth reading on BYIT (−0.85).** Camissa, a South African holder, cut its stake
from 14.51% to 10.93%, about 2.4m shares against roughly 0.4m a day of turnover. The latest
TR-1 was filed on 12 Oct. The hunter found it only in the domestic RNS record and in no
English wire copy. Opus 5 called it the one genuinely fresh primary-document finding of the
day.

## Not ranked

**ENSI (EnSilica).** The hunter found no results release on 13 Oct (`event_confirmed: false`).
The audited FY26 results went out by RNS at 07:00 on
[2026-10-05](https://www.investegate.co.uk/announcement/rns/ensilica--ensi/final-results/9805308).
13 Oct is an Investor Meet Company presentation at 11:00 BST, according to the issuer's own
[1 Oct notice](https://www.investegate.co.uk/announcement/rns/ensilica--ensi/notice-of-results-and-investor-presentation/9800277).
The row came from the UK RNS calendar (`calendar_source: rns`), which read the presentation
date as a results date. It is the same family of fault as the two phantoms on 2026-10-12, where the
`rns` calendar read a date that was not a results date: two days running, so the classifier in
`uk_rns_calendar.py` should be taught to tell a presentation notice from a results notice.

## What the day is, and what it is not

- **Selection:** all 6 eligible names were hunted (at or under the cap of 20), so there was no
  random draw. 11 rows were scheduled across ten markets and 5 fell below the $100k floor.
- **Concentration:** UK 5, Norway 1, every other market 0. `market_concentration` puts the UK
  at 83%, so this is a UK day and any pooled statement about it is a statement about the UK.
- **Calendar sources:** the UK RNS calendar read 8 rows dated for the target and added GNC and
  ENSI. Yahoo's calendar was **unavailable** on every batch in all ten markets. The issuer
  calendars read for DE (EQS), NO (Euronext Oslo, 1 dated), SE/DK/FI (Inderes and the Nasdaq
  fincal) and PL (bankier).
- **`session_unresolved`:** BWY, GNC and ENSI. Each window was assumed to be bmo. For BWY and
  GNC the hunters back it with the issuer's habit of releasing at 07:00, but not with a
  timestamp for this release. Getting the session wrong roughly halves the move.
- **Option anchor:** `options` is null in all ten markets, and Europe runs in the anchor-less
  regime that `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45.
- **Short registers:** the FCA (UK, as of 2026-10-09) and Finanstilsynet (NO) both read.
  **4 of 6 names carry `anchor_covered: true`**: BWY 3.44%, BYIT 5.06%, GNC 2.89% and YOU 1.57%.
  ABG and ENSI were read and are not named, which is a truncated zero, not an anchor.
- **Weak legs:** **0 names came from Spain or Poland**, and 0 from Germany.
- **Lean against the free control:** from the last resolved run (2026-10-08) the UK read 1.0 on
  n=3, which is meaningless at that size. The lean's weights are priors borrowed from the US
  runs and measured nowhere in Europe.
- **`history.basis`:** observed for every name today (`observed_rns` for the UK,
  `observed_newsweb` for ABG). No name rests on a cadence estimate.
- **Conviction floor:** no name sits above 2.8. Over the whole US sample the sign was a coin
  flip below the floor, so every row here should be read that way.
- **What is already public, and what the release adds:**

  | name | already public | new in the release |
  | --- | --- | --- |
  | BWY | FY26 numbers (11 Aug) | first FY27 guide; total FY27 returns |
  | BYIT | the whole H1 and a raised FY27 guide (17 Sep, +12% that day) | H2 commentary; a likely new buyback |
  | YOU | FY26 in line with the £52–56m guide (6 Aug) | first FY27 guide; a strategy update replacing the Capital Markets Day that never happened; buyback size |
  | GNC | nothing pre-released for the period | full Q4/FY26 trading |
  | ABG | nothing pre-released for the period | Q3 numbers |

  On the first resolved days, a likely guidance change separated 9.0% moves from 2.3% ones.
  So BWY and YOU (abs_move 8–10) carry the guidance-event size, and ABG (3.5) does not.
- **Language notes:**
  - ABG: the Norwegian sources added only an Investtech technical column on E24 (sized −0.1).
    ABG files in English only.
  - BYIT: the UK domestic sources (RNS and the FCA register) carried the Camissa sell-down and
    the short rebuild, which no English wire copy did.
  - The other names: nothing the English sources did not already carry.
- **One day is not a result.** Five names cannot establish anything.

Provenance: `provenance.json`. Hunters: `uk.v7` and `nordic.v5` on claude-opus-5-5. The
orchestrating session ran on claude-opus-5-5.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
