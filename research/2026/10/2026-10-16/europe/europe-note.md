# Stage EU — Europe ranking for 2026-10-16

**The answer: no name clears the 2.8 conviction floor, and the panel selected nothing.
Five names were ranked, all Swedish and all reporting before the open on Friday 16
October. Every `impact_sum` sits between 0.00 and +0.80. AZA (Avanza) is the top name at
+0.80. INVE_A (Investor A) and ITECH (I-Tech) share the bottom at 0.00: Investor's hunter
found nothing, and I-Tech's findings cancel out. The panel's top name is PLAZ_B (Platzer),
but only Opus 5 put it in its own top 20%.**

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Thursday 2026-10-15 at about 13:45 UTC, while Stockholm was still trading. Every
sealed spot is therefore an **intraday price, not a close**. The realised move is measured
from daily bars: close(2026-10-15) → close(2026-10-16).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | AZA | Avanza Bank Holding | **+0.80** (p56) | no | +0.12 | 3.0 | 52 | bmo. The issuer's invitation says 07:45 CEST |
| 2 | se | PLAZ_B | Platzer Fastigheter B | **+0.60** (p48) | no | +0.54 | 4.5 | 56 | bmo. The issuer's invitation says 08:00 CEST |
| 3 | se | NP3 | NP3 Fastigheter | **+0.50** (p40) | no | +0.35 | 3.5 | 55 | bmo. The issuer's calendar gives the date; its last four reports went out 06:00–07:00 UTC |
| 4 | se | INVE_A | Investor A | **0.00** (p5) | no | 0.00 | 1.5 | 50 | bmo. The issuer's invitation says 08:15 CET |
| 5 | se | ITECH | I-Tech | **0.00** (p5) | no | 0.00 | 9.0 | 50 | bmo. The issuer's MFN calendar says 08:00 |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank. INVE_A and ITECH tie at zero, and the scorer's
order inside a tie carries no information. **ITECH is the split worth seeing:** it has the
day's largest `abs_move_pct` (9.0, from its own print reactions of −28.5, −12.7, −16.7,
+3.2, +5.1 and +5.9%) and no sign.

**What the period already disclosed, per name:**

- **AZA:** the July, August and September monthly statistics pre-released brokerage and
  savings capital. The hunter's bottom-up lands on the 18-analyst Modular consensus.
- **NP3:** the full-year forecast moves mechanically with announced deals, and the
  14 October acquisition is public.
- **INVE_A:** most of its NAV is listed holdings, priced every day.
- **PLAZ_B and ITECH:** nothing was pre-released, so their Q3 numbers are entirely new.

No hunter expects a real guidance change. NP3 should get a mechanical nudge, and AZA's cost
guide should be reiterated.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their own pinned `-intl-` agents, with no fallback, and each covered 5 of 5 packs. The
selection rule for this market is `consensus`: a name is selected when 3 of 4 judges put it
in their own top 20%. Each judge's top 20% starts at Opus 5 |1.68|, Opus 5.5 |1.00|,
Sonnet 5.5 |1.10| and Fable 5.1 |1.33|, measured on 46 live sizes each.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PLAZ_B | no | 60 | long | 14 | 80L* | 44L | 65L | 50L | 1 | +0.62 | +0.60 |
| 2 | NP3 | no | 48 | long | 6 | 52L | 41L | 54L | 44L | 0 | +0.46 | +0.50 |
| 3 | AZA | no | 44 | long | 8 | 56L | 44L | 37L | 37L | 0 | +0.45 | +0.80 |
| 4 | ITECH | no | 21 | long | 38 | 33L | 44S | 41L | 54L | 0 | +0.43 | 0.00 |
| 5 | INVE_A | no | 0 | — | 0 | 0- | 0- | 0- | 0- | 0 | 0.00 | 0.00 |

Each member's figure is its percentile 0-100 against its own live range, with L for long and
S for short. A `*` marks a member's own top 20%.

- **No name was selected.** The closest is PLAZ_B, where only Opus 5 put it in its own top
  20% (+1.8, 80th percentile). The other three placed it at 44–65.
- **Where the panel and the hunter disagree most:**
  - **ITECH:** the hunter is 0.00 by offset. Three of the four judges lean mildly long.
    Opus 5.5 is short at −0.48, and the spread (sd 38) is the day's widest.
  - **AZA:** the hunter's top name at +0.80, but third in the panel. Every judge kept the
    pre-released brokerage line at zero.
- **What the numbers are not:**
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales still rest on 46 live sizes each plus the frozen E-P seed.
  - In the four-model re-judge, the judges ranked Europe better than the live hunt, but
    nothing about this market's panel is established.

## The top and bottom name

- **AZA (+0.80).** The live line is cost phasing. Avanza's own 2026 guide (+9% ex-expansion
  plus SEK 50m for Denmark, after H1 ran +14%) implies Q3 costs of about SEK 355–365m,
  against the −373m consensus.
  - Guide: https://view.news.eu.nasdaq.com/view?id=b6cab79bab2ace0ee44e817e0355fd05f&lang=en&src=listed
  - Consensus: https://www.placera.se/telegram/avanza-bank-avanza-vantas-redovisa-935-miljoner-i-rorelseresultat-modular-finance-20261012

  Two smaller findings add to it. Analysts have under-forecast net interest income before:
  Q2 was 486 against 454 ("Räntenettot blev 486 miljoner kronor jämfört med
  analytikersnittet på 454 miljoner kronor", i.e. "net interest income came in at
  SEK 486m against the analyst average of SEK 454m"). And the FI aggregate short rose to
  4.85% from 4.63% on 14 October. Recent beats were sold, so `p_up` is 52.
- **INVE_A (0.00).** The hunter found no findings. The NAV can be computed from listed
  prices, and the Q3 statement is the light version with no guidance. The last five report
  days moved within about 0.5 points of OMXSPI. Release notice:
  https://www.placera.se/pressmeddelanden/invitation-to-investors-q3-2026-webcast-20261002
- **ITECH (0.00).** The findings cancel:
  - +1.0 for the largest customer: Chugoku Marine Paints reported Apr–Jun recurring profit
    up 56% ("中国塗、4-6月期(1Q)経常は56％増益で着地", https://kabutan.jp/stock/news?code=4617).
  - +0.3 for USD/SEK.
  - −0.8 for likely catch-up inside the record Q2. This is an inference.
  - −0.3 for buying into the print on about 2.5x normal volume.
  - −0.2 for regulatory costs.

## What the reader must carry

**Selection.** `all 5 eligible names (at or under the cap)`: there was no random draw,
because 5 eligible names is under the cap of 20.
- `by_market`: se 5. Nothing came from uk, de, fr, dk, no, fi, it, es or pl.
- 7 rows were scheduled and 2 fell below the $100k floor.
- **Market concentration: se is 100% of the day.** This is one market's day, and four of
  the five names are rate-sensitive Swedish financials or property companies. They are
  one correlated exposure, which the scorer cannot see.
- ITECH sits at $0.10m/day, just over the $100k floor.

**The universe needed one retry.** The first build hit a truncated-JSON error on the German
vendor read, which recorded an `error` in place of Germany's `per_market` entry. A single
rebuild read Germany cleanly (428 rows, 0 scheduled) and returned the same five names.

**Calendar sources:**
- The UK RNS calendar read 0 rows for 16 October.
- Yahoo agreed with the vendor on AZA, NP3 and PLAZ_B. Inderes joined 9 Swedish rows.
- On the retry, Yahoo was `unavailable` for Germany. Every other source read.

**Session-unresolved:** none. All five were sealed bmo, and every hunter confirmed it from the
issuer.

**Anchors:**
- `options` is null in all ten markets, so Europe runs in the anchor-less regime: ρ=+0.073,
  p=0.45 over 104 events on the sealed corpus.
- Only the Swedish register (FI, as of 2026-10-15, 335 rows) was needed today, and it read.
- **2 of 5 names carry `anchor_covered: true`:** AZA (4.85%) and NP3 (0.63%). INVE_A, ITECH
  and PLAZ_B are truncated zeros, not anchors. For those three, `priced_lean_pct` is the
  run-up alone.

**Weak legs:** Spain and Poland contributed 0 names, and Germany contributed 0.

**Reaction history and calendar quality:**
- **`history.basis` is `estimated_from_cadence` for all five names.** That is a scale, not a
  record of dates. Two hunters checked it against the real report dates in the Nasdaq Nordic
  feed and found it wrong:
  - NP3's observed print-day moves are 3.82, 1.55, −1.15, 3.29, 2.12 and −0.37.
  - PLAZ_B's observed moves are +3.5, −2.8, +2.8, +1.4, +2.6 and +6.7.
  - ITECH has no history at all.
- Two hunters also found the baseline's analyst band too thin. Investor is cited by at least
  four houses, and Platzer by at least five.
- Platzer's Yahoo consensus row (Q2 EPS 1.97) contradicts the company's own reported Q2
  figure of −0.46 per share, so it was not used as a bar.

**Previous resolved run:** the last resolved European run is 2026-10-08. Its only per-market
`lean_vs_free_control_rho` is UK 1.0 on 3 names. No Swedish figure exists yet. The runs from
10-12 to 10-15 are not resolved. **The 10-14 and 10-15 runs carry Swedish and Finnish names
and must be resolved within about a week**, inside the Nasdaq Nordic feed's window.

**The lean's weights are priors** borrowed from the US runs and measured nowhere in Europe.

**`language_note` highlights** (prose, not evidence):
- AZA: the Modular consensus line items and the NII-beat history came only through Swedish
  Finwire copy on Placera.
- PLAZ_B: Pareto's buyback-after-asset-swap catalyst ("möjligheten till nya aktieåterköp
  efter tillgångsbytet", i.e. "the possibility of new share buybacks after the asset swap")
  appeared only in Swedish.
- NP3: Wallenstam's Swedish-only Q3 release carried the peer valuation read-through.
- ITECH: the one non-English input that mattered was Japanese, not Swedish.
- INVE_A: nothing the English sources did not already carry.

**Floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign was a coin
flip below it.

**One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
