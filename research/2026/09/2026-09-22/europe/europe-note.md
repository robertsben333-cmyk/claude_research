# Stage EU — Europe researcher — ranking for 2026-09-22

**Nine names, ranked on `impact_sum`. Two clear the conviction floor: OXB +3.20 and SAA
+3.10. Both are driven by an activist stake-building disclosure filed in the twenty-four
hours before the print — and that is one exposure, not two.** Read the concentration
warning below before treating the top of this board as two independent calls.

Sealed 2026-09-21 13:39 UTC, for prints landing before the London and Paris opens on
2026-09-22. Research only. **No orders were placed and no broker was contacted.**

## The ranking

`ranking_key` is `impact_sum` — the hunters' signed per-finding sizes, added up, in
points of spot. No call, no direction label, no threshold. Cut it wherever you like.

| # | ticker | market | company | impact_sum | above floor | lean | 20d run-up | turnover/day | analysts | anchor |
| --: | --- | --- | --- | --: | :-: | --: | --: | --: | --: | :-: |
| 1 | OXB | uk | Oxford BioMedica | **+3.20** | **yes** | +1.51 | −10.22% | $3.8m | 8 | disclosed 6.86% |
| 2 | SAA | uk | M&C Saatchi | **+3.10** | **yes** | +0.01 | +2.23% | $0.26m | 5 | disclosed 0.20% |
| 3 | KGF | uk | Kingfisher | +2.70 | – | +1.64 | −4.79% | $15.96m | 18 | disclosed 10.69% |
| 4 | ABCA | **fr** | ABC arbitrage | +2.30 | – | −0.09 | +1.74% | $0.28m | 2 | **truncated zero** |
| 5 | LUCE | uk | Luceco | +1.40 | – | −0.12 | +4.04% | $0.67m | 5 | disclosed 0.80% |
| 6 | MAB1 | uk | Mortgage Advice Bureau | +1.40 | – | +1.64 | −26.16% | $1.77m | 3 | disclosed 2.05% |
| 7 | PRTC | uk | PureTech Health | −0.80 | – | +1.25 | +3.40% | $1.19m | 4 | disclosed 1.70% |
| 8 | FNX | uk | Fonix | −1.30 | – | +0.11 | −2.27% | $0.23m | 2 | **truncated zero** |
| 9 | SMIN | uk | Smiths Group | −1.40 | – | −0.84 | −1.31% | $31.23m | 14 | disclosed 1.83% |

**9 of 9 names are rankable.** Nothing was killed for a missing hunt, an unconfirmed
event or a suspect plausibility flag.

### What drives the top name

**OXB +3.20**, and +2.2 of it is one finding, found in the domestic pass:

> Irenic Capital Management — a New York strategic activist whose signature campaign is
> to push a company into a sale — disclosed a 5.41% interest in Oxford BioMedica on the
> morning of 21 September (RNS 10:43), 5.35 percentage points of it through CFDs,
> threshold crossed 17 September, no previous notification.

<https://www.investegate.co.uk/announcement/rns/oxford-biomedica--oxb/holding-s-in-company/9782141>

That lands on a name the FCA register already shows with a **6.86% disclosed net short**,
the second-largest on the board, into a print the hunter confirmed off the issuer's own
7 August "Notice of Results" RNS.

### What drives the bottom name

**SMIN −1.40**, and −1.8 of it is a scale correction rather than a story:

> The scale of a Smiths FULL results print is 3–10%, not the ~1% the baseline carries,
> and both of the last two were negative. FY25 preliminary results 23 Sep 2025,
> 2378p → 2298p = −3.36%; HY26 20 Mar 2026, 2350p → 2118p = −9.87%. The two light
> trading statements in between moved −0.98% and +0.32%.

<https://www.investegate.co.uk/company/SMIN>

## Read this before quoting anything above

### One market, and very nearly one stock market story

`selection.market_concentration`: **largest market `uk` at 0.889**, two markets
represented. Eight of the ten contributed nothing — Germany, Sweden, Denmark, Norway,
Finland, Italy and Spain had **zero** scheduled rows and Poland had one that failed the
turnover floor. This is a UK day with a single French passenger. **Any pooled statement
about "Europe" from this run is a statement about London.**

`selection.method` is *all 9 eligible names* — 22 vendor rows scheduled, 13 dropped on
the **$200k/day** floor, 9 survivors, which is at or under the cap of 20, so **no random
draw was needed**. The draw is deliberately not stratified by market; the concentration
is reported instead of being engineered away.

### The two floor-clearing names share one exposure

OXB's +2.2 finding is an activist TR-1 filed 2026-09-21 at 10:43. SAA's +1.5 finding is
an activist TR-1 filed 2026-09-21 at 17:25 (Harwood/Rockwood/Oryx crossing 9%, having
publicly urged a break-up since March). **Both names clear the floor on the same kind of
event, disclosed on the same channel, on the same day.** The scorer cannot see that they
are correlated — it is the same shape as the four US names the IEEPA tariff refunds
ranked together on 2026-09-10. If UK activist disclosure flow is what this board is
measuring, then this is one observation and not two.

### The anchor

- **`options` is null in all ten markets.** No European single-stock chain proved
  retrievable — Yahoo returns zero expiries for `.L`, `.DE` and `.PA`, and Eurex's free
  file carries no settlement prices, no open interest and no underlying map. Europe runs
  in the same anchor-less regime as Japan, which is the regime `archive/backtest/FINDINGS.md`
  §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Two registers were needed and both read**: the FCA (419 disclosed positions, as of
  2026-09-19) and the AMF (74 issuers with an open position, as of 2026-09-17).
- **7 of 9 names carry `anchor_covered: true`.** ABCA and FNX are
  `register_read_no_position` — a **truncated zero** at the 0.5% per-holder SSR
  threshold, which is not a disclosure that nobody is short. They take
  `anchor_quality.direction` 0.15 where a real disclosure earns 0.45, and their
  `priced_lean_pct` (−0.09 and +0.11) is essentially the 20-day run-up, **which is also
  the free control this stage is measured against** — so neither can beat the benchmark
  with anything that uses it.
- **Every weight in the lean is a prior borrowed from the US runs and measured nowhere
  in Europe.** Two hunters said so independently and unprompted: PRTC's rejected the
  lean's +1.02 "short squeeze" component as not credible on a 1.70% disclosed short that
  is *covering* into the print, and FNX's called its own lean "the free control wearing a
  different name".
- **Zero names from Spain or Poland**, which have no register and no day archive, and
  **zero from Germany**, which cannot reach `event_occurred: false`. On this particular
  day the weak legs cost nothing, because none of them reported.
- Prior `lean_vs_free_control_rho`, UK, from 2026-09-16: **0.40**. That run used
  **synthetic findings** on four names and is a plumbing test, not a measurement. There
  is still no resolved European run anywhere in this repo.

### Sessions and event reality

All nine are `bmo`. Three were sealed `session_unresolved: true` — **PRTC, SAA and
SMIN** — and **all three were settled by their hunter against a primary document**, not
left on the 339-of-379 base rate:

- SMIN — Smiths' own financial calendar, "Announcement of FY2026 Annual Results", 22 September.
- SAA — Notice of Half Year Results RNS, 17 Sep 12:23, results Tuesday 22 September with a 9:00am analyst presentation.
- PRTC — Notice of Results RNS, 4 Sep 07:01:23, plus Form 25 (11 May) and 15F-12B (21 May) on EDGAR proving the Nasdaq channel is closed, so no US after-hours release is possible.

All nine carry `event_confirmed: true` from the issuer's own calendar or RNS rather than
the vendor. Given the US stage's 20-of-20 phantom rate on `time-not-supplied` rows, that
is the single most reassuring line in this note — and it is consistent with the measured
**2.2% UK vendor phantom rate**, not a contradiction of it.

**`history.basis`**: eight names are `observed_rns` — real dated announcement history.
**ABCA alone is `estimated_from_cadence`**, which is a scale for how big this name's
prints usually are and **never** evidence that a print will happen on a date. Reading a
cadence prior as confirmation is how TRT was ranked, traded and never reported. ABCA's
hunter did not rely on it: it settled the date three ways off the issuer's own 2026
calendar release.

### The conviction floor

Two names clear 3.0 — OXB and SAA. Over the whole US sample **the sign of `impact_sum`
below the floor is a coin flip (53%)**, and above the median conviction it is 74%. So
rows 3 through 9 of the table above rank, but nothing in this repo says their direction
is better than chance. The floor is emphasis in this note, never a filter on
`edge-scores.json`.

### The controls

- **Lessons control**: 9 of 9 names carry a `pre_lessons` freeze; **8 of 9 moved**. The
  largest was LUCE (+0.1 → +1.4, a 1.3-point lift); SMIN is the one the file did not
  move at all. Two names moved *down* on it (ABCA −0.3, PRTC −0.2), which is the sign
  the file is doing something other than inflating every number.
- **Language/locality control**: 9 of 9 carry a `pre_local` freeze and **9 of 9 moved**.
  **Every name here is UK or French, and the UK's second pass varies *source locality*,
  not language** — `eu_resolve.py` refuses to pool a UK delta with a German or French
  one, and with eight UK names against one French one there is nothing here to pool
  anyway.
- The largest locality delta this stage has produced is **SAA: `pre_local` −2.0 flipping
  to +2.4**, a sign reversal. The English pass found M&C Saatchi's unannounced Australia
  closure and read it as a disaster; the domestic pass found the break-up activist and
  re-read the same closure as the first step of the break-up. Whether that is skill or a
  coin landing twice is exactly what resolution is for.
- **Nothing pools on one day.** Nine names, one market, no resolved history. A delta on
  this sample is noise.

### Two defects in this run, recorded rather than smoothed

1. **The run spans 4.5 hours and the two waves did not have the same information.** An
   account rate limit killed wave 1's five hunters (after they had written their files)
   and delayed wave 2 from ~14:00 to ~18:35 UTC. The baselines are unaffected — sealed
   once at 13:39, before any hunter, and nothing downstream revises them. But wave 2
   could see the 2026-09-21 London close and wave 1 could not, and this is not
   hypothetical: **SAA's largest finding rests on a TR-1 published at 17:25, a document
   that did not exist when wave 1 ran.** SAA and OXB are ranked 1 and 2 against each
   other on unequal information.
2. **KGF's baseline short figure is not reproducible.** Its hunter fetched the live FCA
   aggregated CSV at 13:52 UTC and read **9.31% at position date 2026-08-05** where the
   sealed baseline reads **10.69% at 2026-09-16** — and every top row of that FCA file
   carries the same 2026-08-05 date, so the FCA's own "current" snapshot is roughly six
   weeks stale. The direction is unaffected and the baseline stays sealed, but the
   register that substitutes for Europe's missing option anchor is less current than the
   baseline claims.

Separately: **ABCA's `print_vs_bar_pct` is +25.0**, an outlier by an order of magnitude.
It is struck against an H1 share of an unrevised FY consensus for an arbitrage firm whose
earnings are inherently volatile, on two analysts. It does **not** affect the rank —
`impact_sum` is the key — but do not quote that field for this name without reading the
hunter's stated basis.

### The sealed spot is not a close

This stage fires at 13:30 UTC, about two hours before the 17:30 CET close, on the
operator's instruction of 2026-09-19. Every `spot` and `run_up_20d_pct` above is an
**intraday price struck at 13:39 UTC on 2026-09-21**. `eu_resolve.py` takes the realised
move from daily bars, close(2026-09-21) → close(2026-09-22), never from the sealed spot,
so the measurement is unaffected — and the free control is struck at the same instant as
the hunt, so the two stay comparable.

### When this has to be resolved

All nine are UK or French, and both markets have a real day archive with a date query
(Investegate back to 1999; the AMF's `info-financiere.gouv.fr` flux, 536,868 records back
to 2012). **There is no Nordic name here, so the ~12-day Nasdaq Nordic window does not
apply and this run does not expire.** Note that Yahoo's European daily closes lag — one
session for `.L`, about two for `.PA` — so this cannot be resolved on the morning of
2026-09-23; rows will carry `move_pending`.

### One day is not a result

Nine names, one market, one day, no resolved European run in existence. Nothing here
establishes that the hunt ranks anything. It becomes evidence only when several days have
pooled and been scored against the realised move with a permutation p — and when the
share of that number coming from a single market, and from a single week of UK activist
filings, is stated alongside it.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.*
