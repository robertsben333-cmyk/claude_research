# Stage EU — Europe ranking for 2026-09-25

Sealed 2026-09-24 at about 13:45 UTC, while the European markets were still trading. Every
sealed spot and every `run_up_*` is therefore an **intraday price, not a close**. The resolver
takes the realised move from daily bars and never from the sealed spot.
Ranking key: `impact_sum`, read from `edge-scores.json`'s own `ranking_key` field. Research only; no orders.

## The answer

**Nothing to rank today.** Two names cleared the $200k turnover floor. One of them does not
report on the 25th, and the other reports after the close, so its reaction falls outside the
window it was sealed on. One rankable name is not a ranking.

| # | name | market | impact_sum | what drives it |
| --- | --- | --- | --- | --- |
| 1 | VGO VIGO Photonics | pl | **+0.50** | Q2 revenue is already out: 34.7m PLN, +70.8% y/y. Margin is the one line the pre-release left open. The case for a record EBITDA is arithmetic on the cost base, not a document, and no EBITDA bar can be sourced, so the finding is capped. |
| — | CHG CHAPTERS Group | de | not ranked | **Phantom date.** The issuer's calendar puts the H1 report anywhere in 1–31 October. |

Neither name clears the conviction floor of 3.0. Across the whole US sample the sign was a
coin flip below that floor.

**VGO +0.50.** The revenue pre-release is ESPI 22/2026, 2026-07-08
(https://www.bankier.pl/wiadomosc/VIGO-PHOTONICS-S-A-Informacja-o-przychodach-Q2-2026-r-9165051.html):
*"skonsolidowane przychody Emitenta wyniosły 34 670 375,00 zł, wobec 20 300 486,00 zł w II kwartale 2025 r. (+70,79% r/r.)"*
(consolidated revenue was PLN 34.67m, against PLN 20.30m in Q2 2025, +70.79% y/y). The Q2 2025
EBITDA base of 0.5m PLN comes from the one covering broker, Ipopema
(https://vigophotonics.com/app/uploads/sites/2/2026/05/20260514_ipopema_securities_vgo_pl_ra-1.pdf).
A margin beat has been paid on this name before: Q1 2026 adj. EBITDA of 3.3m came in against a
1.1m forecast, and the stock rose +5.80% the next session. The revenue pre-release itself moved
only +1.85%.

**The session is wrong in the sealed window, and this matters more than the number.** The
vendor left the time blank and the universe defaulted to `bmo`. The date is confirmed by the
issuer's Kalendarium: *"25 września 2026 raport półroczny za I półrocze 2026 roku"*
(https://vigophotonics.com/pl/relacje-inwestorskie/kalendarium/). But every quarterly and
half-year report in the last four has gone out after the 17:00 CEST close: 17:03, 19:57, 17:10
and 18:21 (Bankier ESPI timestamps, URLs in the hunt file). So the reaction lands on **Monday
2026-09-28**. The sealed bmo window (close 09-24 → close 09-25) should hold approximately
nothing from the print, and the +0.50 is sized for the amc window. `eu_resolve.py` measures both
windows on a `session_unresolved` row. **Read `move_amc_window_pct` for VGO, not the bmo move.**
The baseline stays sealed as it was.

**CHG, not ranked.** The German Finanzkalender reads *"Veröffentlichung Halbjahresbericht 2026 — 1. Oktober – 31. Oktober"*
(https://www.chaptersgroup.de/finanzkalender/). An 8 September release says the same, and the H1
figures were already pre-released by ad-hoc that day, when the FY26 outlook was raised.
Germany cannot reach `event_occurred: false` in `eu_resolve.py`, because EQS has no whole-day
query. So this kill rests on the hunt and the issuer's calendar, not on the resolver. The EQS
search returned nothing after 2026-09-08.

## What the day is, stated plainly

- **Selection:** "all 2 eligible names (at or under the cap)". There was no random draw: 21
  scheduled, 19 dropped below the floor. Scheduled by market: uk 8, it 4, pl 5, de 2, fr 2, and
  zero in se/dk/no/fi/es. Hunted: `by_market` de 1, pl 1.
- **Market concentration:** the largest market's share is 0.5 across two markets. That is
  meaningless on two names.
- **`session_unresolved`:** both names. For VGO the hunter settled it as amc, with sources. For
  CHG it is moot.
- **Options:** null in all ten markets. Europe runs in the anchor-less regime, the one priced at
  ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers:** DE resolved (Bundesanzeiger, as of 2026-09-23, 285 rows) and does not
  name CHG. That is a truncated zero, not an anchor. PL has no register. **`anchor_covered`: 0
  of 2.**
- **Spain/Poland:** 1 of 2 names (VGO) comes from Poland. It has no positioning anchor, so its
  `priced_lean_pct` of −0.38 is the 20-day run-up, which is also the free control, and its
  print can never be confirmed or killed by the resolver. **Germany:** 1 of 2 (CHG), which
  cannot reach `event_occurred: false` either. Today's two names come from the two weakest-
  instrumented market types in the stage.
- **`lean_vs_free_control_rho`:** there is no previous real resolved European run. The only
  resolved files, 2026-09-16 and 09-17, are validation runs on synthetic findings (UK 0.40 on
  09-16), so nothing to quote.
- **Lean weights** are priors borrowed from the US runs and have been measured nowhere in
  Europe.
- **`history.basis`:** `estimated_from_cadence` for both. That is a scale, not a record of
  dates, and CHG's vendor date is exactly the kind of cadence prior that turns out empty.
- **Language pass:** VGO's `language_note` is substantive. The release-time evidence that
  settled the session, the Ipopema base quarter, the Strupiński lawsuit, TFI PZU's EGM
  requisition and the China dual-use impact analysis all came from Polish-only sources. CHG's
  says the German sources added nothing, because the issuer publishes every item in both
  languages. `eu_resolve.py`'s pre_local section will read 0 names; that control was retired on
  2026-09-22.
- **One day is not a result**, and a one-name day is not even a ranking.

---

*This is a research and forecasting exercise over public information. It is not investment
advice and must not be read as a recommendation to buy or sell any security.*
