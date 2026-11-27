# Stage EU — Europe ranking for 2026-11-30 (Mon)

Sealed Friday 2026-11-27 at about 14:40 UTC, while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The event date is Monday 2026-11-30.

**Answer first: a thin five-name day, and one of the five is a phantom. Of the four names that rank, one is a solvency collapse and three are ordinary prints with nothing large found.**

- **NORSE** (Norse Atlantic, Oslo) is the only name above the 2.8 conviction floor, at `impact_sum` −13.00.
  - The panel selects it short at panel_pct 100, with all four judges in their own top 20%.
  - The number does not come from an earnings surprise. Its operating subsidiary filed for bankruptcy at 13:00 UTC on 27 Nov, all 12 aircraft leases were terminated, and the stock sits in the Oslo Recovery Box at about 0.011 NOK.
- **The IBKR handoff carries one name: SELL NORSE.** A short in a Recovery Box stock at 0.011 NOK is very unlikely to be borrowable, and a suspension is possible. See the handoff section.
- **One day is not a result.**

## Ranked on `impact_sum` (the key, per `edge-scores.json` `ranking_key`)

| # | ticker | mkt | session (hunter's check) | impact_sum | floor | impact_scaled | abs_move | p_up | already public | new in release |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIVE | se | **amc**: ~18:00 CET 30 Nov, per the issuer's 20 Nov release, which moved the report from 26 Nov | +0.80 (p65) | no | −0.52 | 13.0 | 48 | Q2; July SEK 700m raise; LiDAR, ALL.SPACE and Tachyon production orders | Q3 (not pre-released); Q4 revenue-inflection wording |
| 2 | CAPT | no | bmo?: Q1 and Q2 both at 05:30 UTC; 23 Nov notice sets 30 Nov | +0.60 (p55) | no | +0.60 | 5.0 | 56 | **Q3 largely pre-guided** (79% booked at $113,681/day, 1 Sep); 24 Nov prospectus | **Q4-to-date bookings**; dividend |
| 3 | EAH | uk | bmo: 07:30 convention, date from the 6 Nov RNS | −0.60 (p55) | no | +0.00 | 5.0 | 50 | **H1 pre-released** 6 Nov (−12.1% that day); FY guide: revenue below consensus, EBITDA and EPS in line | whether the guide is repeated; China H2 trading |
| 4 | NORSE | no | bmo (Q3 still on the 20 Nov calendar; may be postponed) | **−13.00** (p100) | **yes** | −15.30 | 45.0 | 33 | Critical financing (25 Nov); flights suspended (26 Nov); leases terminated and subsidiary bankruptcy (27 Nov) | status of the listed parent; Q3 accounts, if published |

**Not ranked: POLR** (Polar Capital). The hunter found no results event in the window. The interims went out by RNS at 07:00 on 2026-11-24 (https://www.investegate.co.uk/announcement/rns/polar-capital-holdings--polr/unaudited-interim-results/9889872). The vendor's 30 Nov row is an RNS Reach retail investor webinar of those already-public results (https://www.investegate.co.uk/announcement/rns/polar-capital-holdings--polr/notice-of-investor-presentation/9837652). This is a vendor-calendar phantom of the same kind as NORAM and RVRC yesterday.

**SIVE's two measurements disagree in sign.** Its findings sum to +0.80, but `impact_scaled` is −0.52, because the hunter's `p_up` of 48 carries the two prior prints that were sold (−11.7% and −24.4%).

**What drives the top and the bottom name:**
- **SIVE (top, +0.80):**
  - The largest finding (+0.7) is the LiDAR, ALL.SPACE and Tachyon production orders shipping from Q4, which the report can point to if it reaffirms the Q4 revenue inflection (https://view.news.eu.nasdaq.com/view?id=b0469d64a5351eea457c34d906bbea2e4&lang=en&src=listed).
  - Two items offset it: a likely 20–30% year-on-year revenue decline (−0.5) and the US stopgap budget delaying defence programmes (−0.4).
- **NORSE (bottom, −13.00):** the parent's solvency step is the likeliest decisive news in the window, sized at −15 (https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=687671). It carries a small upside tail for a takeover rescue, but equity ranks behind the USD 52m 15% senior secured bond and the lessors.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four members ran, with no fallback.
- Each judge's own top 20% starts at |0.96| (Opus 5), |0.68| (Opus 5.5), |0.60| (Sonnet 5.5) and |0.80| (Fable 5.1), measured on 200 live sizes each.

| rank | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NORSE | bmo | **yes** | 100 | short | 0 | 100S* | 100S* | 100S* | 100S* | 4 | −13.34 | −13.00 |
| 2 | CAPT | bmo? | no | 68 | long | 8 | 66L | 59L | 80L* | 68L | 1 | +0.80 | +0.60 |
| 3 | SIVE | amc | no | 28 | long | 68 | 61L | 68L | 72L | 89S* | 0 | +0.72 | +0.80 |
| 4 | EAH | bmo | no | 49 | long | 14 | 58L | 68L | 36L | 36L | 0 | +0.49 | −0.60 |

`*` = in that judge's own top 20%.

- **SIVE is the panel's split name.** Three judges lean long and Fable 5.1 is in its own top 20% on the short side (−1.2). The mean percentile therefore collapses to 28, with sd 68.
- **EAH flips sign between the hunter (−0.60) and every judge (+0.30 to +0.60).** All four judges weighted the post-warning drift onto a repeated guide above the hog-price proxy.
- **NORSE is the judges' unanimous outlier**, at −6.5 to −12.9. Opus 5 explains why it is not sized to the full downside: the 27 Nov filing was public before Friday's close, which is the window's entry price.

## IBKR handoff

`ibkr-handoff.json` was written at 14:49 UTC and published before this note. The rule is `panel_pct` ≥ 70 with all four judges.

| side | ticker | mkt | panel_pct | qty (offline plan) | price | value | weight |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SELL | NORSE | no | 100 | 2,261,668 | 0.0115 NOK (sealed spot) | 2,430.71 | 24.3% |

Not taken: CAPT, panel_pct 68.2, below the 70 floor.

**Caveat for the operator.** NORSE is in Oslo Børs' Recovery Box after a −95% month and a subsidiary bankruptcy filing. Borrow for a short is very unlikely, and the parent may be suspended or file over the weekend, in which case the window carries no tradeable price. The executor's rules decide what happens. This session did not change the rule or the handoff.

## The day, and what it cannot tell you

- **Selection:** all 5 eligible names (at or under the cap of 20). There was no random draw today because 5 ≤ 20; the draw is random among eligible names by design. 28 rows were scheduled and 23 dropped. `by_market`: uk 2, no 2, se 1, and zero from de, fr, dk, fi, it, es and pl.
- **`selection.market_concentration`:** the largest market is uk at 40%, with three markets represented. One of the two UK names is the phantom, so Oslo is 2 of the 4 ranked names.
- **Calendar sources:**
  - The UK RNS calendar added XAR, LST and POLR; POLR is the phantom.
  - The Yahoo firm dates agreed with the vendor on SIVE and NORSE.
  - The issuer calendars read for DE (EQS), SE/DK/FI (Inderes, Nasdaq fincal) and NO (Euronext Oslo).
  - **bankier.pl returned HTTP 403**, so the Polish issuer calendar was unavailable.
- **Session:**
  - CAPT and POLR were sealed `session_unresolved`. CAPT's hunter settles it bmo on the issuer's 05:30 UTC pattern.
  - **SIVE is amc**, so its reaction falls in close(11-30) → close(12-01), not a bmo window.
  - EAH's 07:30 is a convention, with no timestamp yet.
- **Options:** `options` is null in all ten markets. Europe runs in the anchor-less regime that priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers:** read for uk, no and se. **2 of 5 names carry `anchor_covered: true`** (POLR 0.88%, SIVE 7.41%). The other three are truncated zeros, not anchors.
- **Spain and Poland: 0 names today.** **Germany: 0.** So no ranked name is in a market where `event_occurred: false` is structurally unreachable.
- **`history.basis`:**
  - SIVE's is an **estimated** cadence, a scale and not a record of dates. Its date and session come from the issuer's own release instead.
  - EAH and POLR are `observed_rns`, and CAPT and NORSE are `observed_newsweb`.
- **Prior run's `lean_vs_free_control_rho`:** the last resolved European run is 2026-10-16, where Sweden read 0.6. **No European run has been resolved since 2026-10-16.**
- **Lean weights:** the lean's weights are priors borrowed from the US runs and measured nowhere in Europe.
- **Conviction floor:** only NORSE clears 2.8. Over the whole US sample, the sign was a coin flip below the floor.
- **`language_note`:**
  - NORSE: e24, in Norwegian, carried the subsidiary bankruptcy, the unpaid wages ("Lønnen som skulle vært utbetalt onsdag, uteble") and the JP Morgan engagement while English searches returned nothing.
  - CAPT, SIVE and EAH: nothing the English sources did not already carry.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
