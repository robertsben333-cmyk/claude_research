# Stage EU — Europe ranking for 2026-11-03 (Tue)

Sealed Mon 2026-11-02 ~15:50 UTC, about an hour before the European close: every sealed
spot and `run_up_20d_pct` is an **intraday price, not a close**. Ranking key:
`impact_sum` (from `edge-scores.json`'s `ranking_key`). Conviction floor 2.8. **No name
clears the floor; the largest is FME at −1.40.** Nineteen hunts, all `search_complete`,
and not one found a sourced, unpriced number that decides a print. No orders; this stage
reads no broker.

## Ranked

All 19 are bmo. `bmo?` = sealed with `session_unresolved`; every hunter except BOSS's then
confirmed bmo from the issuer's own notice or its release-time history (BOSS: the issuer
calendar gives the date, not a time).

| # | ticker | market | session | impact_sum (key) | abs_move | p_up | impact_scaled | anchor | history | pre-released? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NOBA | se | bmo (07:30) | +0.70 | 5.0 | 53 | +0.30 | no | estimated | no |
| 2 | OKEA | no | bmo (06:00) | +0.60 | 4.5 | 50 | +0.00 | no | observed_newsweb | **yes**, 27 Oct trading update |
| 3 | VSURE | se | bmo? (08:00) | +0.50 | 5.5 | 48 | −0.22 | yes | estimated | no |
| 4 | MULTI | no | bmo (08:30) | +0.40 | 4.0 | 52 | +0.16 | no | observed_newsweb | no |
| 5 | HACK | se | bmo (07:30) | +0.30 | 6.0 | 52 | +0.24 | yes | estimated | **yes**, 12 Oct profit warning |
| 6 | SOLAR_B | dk | bmo? (~08:00) | +0.30 | 5.5 | 56 | +0.66 | no | estimated | no |
| 7 | BOSS | de | bmo | +0.20 | 4.0 | 53 | +0.24 | yes | estimated | no |
| 8 | ADV | de | bmo? | +0.00 | 0.6 | 50 | +0.00 | no | estimated | no (DPLTA-pinned) |
| 9 | DOTD | uk | bmo? (07:00) | +0.00 | 5.0 | 54 | +0.40 | no | observed_rns | **yes**, 28 Jul FY update |
| 10 | ODL | no | bmo? (07:05) | −0.00 | 5.0 | 51 | +0.10 | no | observed_newsweb | no |
| 11 | SHA0 | de | bmo | +0.00 | 3.3 | 50 | +0.00 | no | estimated | **yes**, 13 Oct |
| 12 | NOEJ | de | bmo? (07:0x) | −0.30 | 3.5 | 50 | +0.00 | yes | estimated | **yes**, 19 Oct ad-hoc |
| 13 | TUNE | uk | bmo (07:00) | −0.40 | 4.5 | 48 | −0.18 | no | observed_rns | **yes**, 16 Sep update |
| 14 | BOOZT | se | bmo | −0.50 | 4.5 | 45 | −0.45 | yes | estimated | **yes**, 28 Sep |
| 15 | SYNACT | se | bmo? (07:30) | −0.50 | 8.0 | 47 | −0.48 | yes | estimated | no |
| 16 | TMV | de | bmo (07:00) | −0.50 | 6.5 | 51 | +0.13 | yes | estimated | no |
| 17 | ZAL | de | bmo? (07:00) | −0.50 | 7.5 | 47 | −0.45 | yes | estimated | no |
| 18 | REJL_B | se | bmo (08:30) | −0.60 | 4.0 | 44 | −0.48 | no | estimated | no |
| 19 | FME | de | bmo? | −1.40 | 7.5 | 44 | −0.90 | yes | estimated | no |

Not ranked: **COFA** (fr). I dropped it as a **duplicate event**. The 2026-11-02 run
already hunted Coface's 9M-26 release, which comes out on 2 Nov at 17:35 Paris, after the
close. A bmo window on 11-03 covers the same close(11-02) → close(11-03), so a second hunt
would count one print twice. I did not draw a replacement.

`impact_scaled` is the hunter's second, separate measurement. It is not the key, and the
floor does not apply to it. **Likely guidance change** (`new_in_release`): FME (the new
CEO's first print, a possible 2027 reset), ZAL (a possible narrowing of the FY guide) and
TMV (cash statement at risk). Seven names had already pre-released the period. On the
first resolved days, that single fact separated a 3.1% move from a 7.4% move.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran
on their pinned `-intl-` agents, with no fallback. The Sonnet 5.5 judge says it sized from
the shared core and the lessons file without opening the three market hunter definitions.
The other three read them. Selection: 3 of 4 judges in their own top 20%. Own-top-20%
thresholds: opus5 |1.40|, opus55 |0.84|, sonnet55 |0.72|, fable51 |0.96|, each on 200 live
sizes.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FME | bmo? | **yes** | 81 | short | 12 | 86S* | 62S | 93S* | 86S* | 3 | −1.43 | −1.40 |
| 2 | VSURE | bmo? | | 61 | short | 24 | 74S | 20S | 72S | 78S | 1 | −0.99 | +0.50 |
| 3 | ZAL | bmo? | | 65 | short | 18 | 52S | 44S | 76S | 88S* | 1 | −0.85 | −0.50 |
| 4 | SYNACT | bmo? | | 64 | short | 14 | 56S | 49S | 86S* | 66S | 1 | −0.79 | −0.50 |
| 5 | BOOZT | bmo | | 56 | short | 12 | 62S | 38S | 56S | 70S | 0 | −0.77 | −0.50 |
| 6 | REJL_B | bmo | | 49 | short | 13 | 48S | 68S | 48S | 31S | 0 | −0.61 | −0.60 |
| 7 | NOBA | bmo | | 43 | long | 13 | 22L | 42L | 56L | 52L | 0 | +0.60 | +0.70 |
| 8 | OKEA | bmo | | 33 | long | 9 | 20L | 32L | 42L | 40L | 0 | +0.44 | +0.60 |
| 9 | ODL | bmo? | | 16 | short | 18 | 18S | 32S | 14L | 27S | 0 | −0.30 | −0.00 |
| 10 | TUNE | bmo | | 20 | short | 2 | 22S | 18S | 20S | 20S | 0 | −0.29 | −0.40 |
| 11 | SOLAR_B | bmo? | | 15 | long | 5 | 21L | 17L | 14L | 8L | 0 | +0.23 | +0.30 |
| 12 | DOTD | bmo? | | 9 | long | 15 | 12L | 20L | 20L | 16S | 0 | +0.22 | +0.00 |
| 13 | TMV | bmo | | 2 | short | 53 | 52L | 24S | 72S | 52L | 0 | +0.15 | −0.50 |
| 14 | BOSS | bmo | | 8 | long | 10 | 20L | 16L | 7S | 5L | 0 | +0.14 | +0.20 |
| 15 | MULTI | bmo | | 3 | long | 5 | 4L | 8L | 7L | 5S | 0 | +0.12 | +0.40 |
| 16 | NOEJ | bmo? | | 7 | long | 5 | 0- | 6L | 14L | 7L | 0 | +0.10 | −0.30 |
| 17 | HACK | bmo | | 4 | short | 24 | 20S | 24L | 14L | 35S | 0 | −0.01 | +0.30 |
| 18 | ADV | bmo? | | 0 | - | 0 | 0- | 0- | 0- | 0- | 0 | +0.00 | +0.00 |
| 19 | SHA0 | bmo | | 0 | - | 0 | 0- | 0- | 0- | 0- | 0 | +0.00 | +0.00 |

**FME, selected short (3 of 4; Opus 5.5 at 62S did not clear its own top 20%).** The judges
leaned on the same items as the hunter. This is Shervin Korangy's first print, three weeks
after a board-forced CEO change. The deputy supervisory board chair said the old CEO had
"keine neuen Ideen, keine Vision" ("no new ideas, no vision"), and Citi reads that as a
shift from margins to growth and reinvestment
(https://www.boerse-online.de/dpa-afx/roundup-chefwechsel-bei-fresenius-medical-care-aktie-unter-druck-556948.html).
The stock has fully retraced the −6.85% it fell on the CEO change, and the FY2027 Vara
consensus of 10-22 still has operating income up about 3%. The name also sold a 10% OI beat
in August (−7.58%).

The strongest case against: the reset is inference from board and sell-side language, not
a company statement. Q3 itself probably beats the EUR 518m bar slightly, because H1 ran
ahead and the TDAPA headwind was halved. The CMS 2027 rule came in better than its draft.
Disclosed shorts are only 2.55%, flat. Fresenius SE's remaining stake is an overhang, but
it falls after the window.

**Disagreements.** VSURE is the sharpest. The hunter is +0.50, leaning on short-squeeze
fuel (3.41% short is about 12% of the free float). Three judges are short at 72–78: most of
the +27.7% 20-day run-up is premium from the FT's CVC take-private story, Verisure has
filed nothing since, and the name sold 3 of 4 prints. TMV splits 2–2 (sd 53). HACK and
NOEJ flip sign at near-zero sizes. No name above the floor went unselected, because none
cleared it.

**What the numbers are not.** `panel_score` ranks and does not forecast. Off the US there
is no `expected_edge_pct`. Certainty (`p_up`) is recorded and decides nothing. The member
scales are still mostly the frozen E-P seed until Europe has about 200 panel names of its
own. In the four-model re-judge the judges ranked Europe better than the live hunt, but
nothing about this market's panel is established.

## What the day is, before any pooled number

- **Selection:** a random sample of 43 eligible names, seed `eu-2026-11-03`, drew 20 at
  the cap of 20. By market: de 7, se 6, no 3, uk 2, fr 1, dk 1. Eligible by market: se 13,
  de 11, no 8, dk 4, uk 3, fr 2, fi 1, it 1. Largest market de at 35%, six markets in all.
  Not one market's day, but German and Swedish names are 13 of the 19 hunted.
- **Correlated pair: MULTI and REJL_B are one exposure.** Multiconsult is a fixed-ratio
  merger target, 0.9725 Rejlers B per share, approved by both meetings on 19 Oct, and both
  report at 08:30 the same morning. Their hunters lean opposite ways (+0.4 and −0.6) on
  what is effectively one combined share. Do not count them as two independent events.
- **Spain and Poland: 0 names.** No name came from either market without a register or
  archive. Germany has 7 (6 ranked), none of which can ever reach `event_occurred: false`.
  The Nordic names (SE 6, DK 1) can be killed only inside the Nasdaq feed's roughly 12-day
  window, so **resolve this run by about 2026-11-12**.
- **Options:** `options` is null in all ten markets, so Europe runs in the anchor-less
  regime (`archive/backtest/FINDINGS.md` §33: ρ=+0.073, p=0.45 over 104 events).
- **Short registers:** de, dk, fr, no, se and uk all read (uk as of 10-30, se 11-02, dk
  10-31). **9 of 19 hunted names carry `anchor_covered: true`** (BOSS, FME, NOEJ, TMV, ZAL,
  BOOZT, HACK, SYNACT, VSURE). The other 10 are truncated zeros, not anchors.
- **History basis:** only the 2 UK names (DOTD, TUNE: `observed_rns`) and 3 Norwegian names
  (MULTI, ODL, OKEA: `observed_newsweb`) are observed. The other 14 are
  `estimated_from_cadence`: a scale, not a record of dates. Three hunters (NOBA, SOLAR_B,
  TMV) found that the baseline's estimated reaction dates were not real print days. In
  every case the observed print-day moves were larger than the estimate (TMV median about
  6% against 2.82%).
- **Lean:** the weights are priors borrowed from the US runs and measured nowhere in Europe.
  `lean_vs_free_control_rho` from the last resolved run (2026-10-16): se 0.60 on 5 names.
- **No European run has resolved since 2026-10-16.** The 10-19 → 11-02 runs are still
  unresolved, and the Nordic rows of 10-19 → 10-23 are already past the feed's roughly
  12-day window, so their Nordic confirmations will come back null. Resolution was not part
  of this fire. It is flagged in the run log for the next session.
- **Floor:** no name is above 2.8. Over the whole US sample the sign was a coin flip below
  the floor, so read this ranking as an ordering of very small numbers.
- **`pre_lessons`:** every hunt froze a draft before reading `LESSONS.md`. The file mostly
  raised `abs_move_pct` (understatement is the systematic error) and trimmed proxy findings.
  Two hunts did not change at all (BOOZT, and ADV except for `abs_move`).
- **Language notes worth quoting:** FME's main finding rests on German dpa-AFX and
  Börsen-Zeitung reporting (JPMorgan: Q3 "als schwierig befürchtet", feared to be
  difficult). NOEJ's cash-flow guide figure (EUR 10–20m) appeared only in German press.
  REJL_B's only bar is SB1's Swedish Finwire forecast, 27% below consensus. ADV's appraisal
  docket (hearing cancelled 28 Aug) came only from a German blog. The Nordic and UK
  filings are bilingual or English, and most hunters there found nothing the English
  sources lacked.

One day is not a result.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
