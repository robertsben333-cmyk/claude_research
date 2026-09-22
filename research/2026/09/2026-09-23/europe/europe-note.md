# Stage EU — Europe ranking for 2026-09-23

Sealed 2026-09-22 13:43 UTC, while the European markets were still open. Nine names, ten
markets screened, one isolated hunter each. **Research only — this stage places no orders
and reads no broker.**

The ranking key is `impact_sum`, as `edge-scores.json` reports in its own `ranking_key`
field. It is a signed number in points of spot. It is **not a call, not a threshold and
not a direction label**, and nothing below should be read as one.

## The ranking

| # | ticker | market | company | `impact_sum` | lean | session | history |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | QDT | fr | Quadient SA | **+3.70** | +0.155 | amc | estimated |
| 2 | CWR | uk | Ceres Power Holdings | **+3.50** | +0.909 | bmo? | observed |
| 3 | BOKU | uk | Boku, Inc. | +0.90 | −0.166 | bmo? | observed |
| 4 | PHIL | it | Philogen SpA | 0.00 | +0.095 | **bmo? — disputed** | estimated |
| 5 | RSW | uk | Renishaw plc | −0.90 | −0.432 | bmo | observed |
| 6 | KOO | uk | Kooth PLC | −1.40 | −1.221 | bmo | observed |
| 7 | JDG | uk | Judges Scientific | −1.80 | **+2.295** | bmo | observed |
| 8 | KWS | de | KWS SAAT SE & Co KGaA | −2.70 | −0.175 | bmo | estimated |
| 9 | W7L | uk | Warpaint London PLC | **−6.20** | −0.012 | bmo | observed |

**Three names clear the conviction floor of 3.0**: QDT (+3.70), CWR (+3.50) and W7L
(−6.20). Over the whole US sample the sign of `impact_sum` **below** the floor was a coin
flip (53%), and the conviction floor is the only rule in this family that has ever cleared
a family-wise correction. The six names between BOKU and KWS should be read as a ranking,
not as six predictions.

### The finding driving the top name

**QDT, +3.70.** Quadient committed, in its own communiqué of 2026-07-20, to give a status
update on the strategic review of its Lockers business **on this release** — advisers
already mandated: *"Quadient prévoit de faire un point sur cette revue stratégique à
l'occasion de la publication de ses résultats du premier semestre 2026, le 23 septembre
2026. Rothschild & Co, Société Générale et Darrois Villey Maillot Brochier ont été
mandatés…"* ("Quadient expects to provide an update on this strategic review at the time
of the publication of its first-half 2026 results, on 23 September 2026. Rothschild & Co,
Société Générale and Darrois Villey Maillot Brochier have been mandated…").
<https://invest.quadient.com/fr/newsroom/3329438>

The hunter sized it at +2.5 of the +3.70 and **emitted 1.5 points below its own finding
sum**, because the term is bimodal rather than directional: this print slot took −17.82%
(2025-09-24) and −14.20% (2026-03-25) and paid +3.01% for its one guidance confirmation.
Read the number as "most to resolve", not "most likely to rise".

### The finding driving the bottom name

**W7L, −6.20.** Warpaint's FY25 annual report discloses Group sales for the four months to
30 April 2026 of ≈£26.1m against £32.6m — down 20%, already including Barry M — while the
same document identifies £5.7m of non-repeating 2025 losses that soften the comparative.
<https://cdn.prod.website-files.com/624aac5eec2229318e2db5e8/6a0f1d8d188670864b239a43_260522%20Warpaint%20Annual%20Report%202025%20WEB.pdf>

The larger of its two −3.0 findings came from the **domestic-source pass**: options granted
2026-06-17 cut the adjusted-EPS CAGR vesting hurdle to *">5 per cent. over the three
financial years commencing 1 January 2026"* from *">10 per cent."* in the superseded
December 2024 grant — a figure that sits only in note 23 of a 108-page annual report.
<https://www.investegate.co.uk/announcement/rns/warpaint-london--w7l/grant-of-options-and-director-pdmr-shareholding/9624151>

## Selection — and it was not a draw

`selection.method` is **"all 9 eligible names (at or under the cap)"**. 23 names were
scheduled across the ten markets, 14 were dropped, 9 survived — under the cap of 20, so
**no random draw ran at all** and no name was excluded by chance. The floor is $200k/day
of turnover, converted at an FX rate struck at seal time and written into the universe
file.

`by_market` and `eligible_by_market` are identical: **uk 6, de 1, fr 1, it 1**, and
**se / dk / no / fi / es / pl contributed nothing**. `selection.market_concentration`:
largest market **uk at 66.7%**, 4 of 10 markets represented.

**So this is a UK day with three passengers, and every pooled number below is two-thirds
one market.** That is the seasonal pattern the ten-market expansion was justified against —
late September is the UK's month; October is when the seven new markets carry 456 forward
events against 114 for UK+DE+FR. Nothing about today refutes that and nothing about today
confirms it.

`TIME` (Time Finance) was in the previous run's universe for this same date and is dropped
today at **$189,238/day against the $200,000 floor**. The floor was not lowered to keep it.
231 Swedish (NGM) and 326 Polish (NewConnect) rows were filtered as off-primary-exchange
before the floor was applied; they do not take Yahoo's `.ST`/`.WA` tape and would have been
screened on somebody else's numbers.

No market was closed: `market_closed` is null on all ten.

## What this day cannot see

**There is no option anchor, in any of the ten markets.** `options` is null on all nine
baselines. No European single-stock chain is retrievable free from this container — Yahoo
returns zero expiries for `.L`, `.DE`, `.PA` and `.MI` against 21 for AAPL on the same
crumb. So Europe runs in the **anchor-less regime**, which is the regime
`archive/backtest/FINDINGS.md` §33 priced at **ρ=+0.073, p=0.45 over 104 events** — the
single most discouraging number in this repo. Say it beside any European result.

**Only 3 of 9 names carry a positioning anchor.** All four relevant registers read at seal
time — FCA 419 rows (as of 2026-09-19), Bundesanzeiger 287 (09-21), AMF 74 (09-21), CONSOB
48 (09-21) — but a register that reads and does not name an issuer is a **truncated zero at
the 0.5% SSR threshold, not a disclosure**. `anchor_covered` is true only for **BOKU
(0.27%), CWR (13.21%) and JDG (1.67%)**. The other six are
`register_read_no_position` and their `anchor_quality.direction` is held to 0.15 rather
than 0.45.

For those six the consequence is structural and every one of their hunters said so
unprompted: with both positioning components at zero, **`priced_lean_pct` is entirely the
run-up term — which is also the free control this stage is measured against.** On KWS,
QDT, PHIL, KOO, RSW and W7L the lean and the benchmark are one number wearing two hats, and
nothing built on the run-up can beat the control on those names.

**No name came from Spain or Poland**, so nothing today is anchor-less *and* unconfirmable
by construction. **One name (KWS, Germany) sits in a market where `event_occurred: false`
can never be reached** — EQS-News has no whole-day query, so a German phantom cannot be
caught after the fact. Its hunter did the right thing and confirmed the event affirmatively
from the issuer twice, including KWS's own statement dated 2026-09-09 that it will publish
on 23 September at 07:00 CEST.

**The lean's weights are priors borrowed from the US runs and have been measured nowhere in
Europe.** `eu_resolve.py` ranks every component separately so measurement can replace them.

The KOO hunt put a number on what that costs, unprompted, and it is the most useful single
sentence in the nine: its dominant negative finding is the run-up restated, so stripped of
that finding **its research nets to −1.2 + 1.3 = +0.1**. On an anchor-less name a negative
`impact_sum` and "short the run-up and do no research" are nearly the same object, and −1.40
overstates what the hunt added. That arithmetic is not available for the other five
uncovered names, but the problem is.

## Three things a reader would otherwise get wrong

**1. PHIL's session is disputed, and its zero is a finding rather than an empty hunt.**
`session_unresolved` is true on **PHIL, BOKU and CWR** — the vendor gave no session and all
three defaulted to `bmo`. For PHIL the hunter then settled it the other way: CET publication
timestamps on three consecutive prior Philogen releases (19:40, 19:41, 18:58) put them after
the 17:30 Milan close, corroborated by volume landing on the following session on 9 of 12
observed board dates. If that is right, **the scored `close(09-22) → close(09-23)` window
contains no print at all**, which is exactly why the emitted number is 0.00 and not a small
uncertain one. `eu_resolve.py` measures both windows for all three rows.

**2. The cadence-estimated history understates event scale — measured, not asserted.**
`history.basis` is `observed_rns` for the six UK names and **`estimated_from_cadence` for
KWS, QDT and PHIL**. Only UK (`observed_rns`) and Norwegian (`observed_newsweb`) names carry
real dated announcement history anywhere in this stage. Today the gap is visible in the
data: median |move| across the six observed names is **2.61 – 10.50%** with maxima of
15–32%, against **1.82 – 2.09%** for the three estimated ones. On KWS exactly **one of eight**
cadence-estimated dates is a real print day. Two hunters, in two markets, reached that
conclusion independently. A cadence prior is a scale; reading one as evidence that a print
happened is how TRT got ranked, traded and never reported.

**3. The free control has a blind spot on W7L that the 5-day fix does not cover.**
`run_up_20d_pct` reads **+0.24%** and `run_up_5d_pct` **−0.67%** on a stock that bottomed at
177.0p on 2026-07-20 and closed 215p today — **+21.5%**. Both windows say "flat" because the
move is *older* than twenty days. Stage J's `run_up_5d_pct` was added for the mirror case, a
move *newer* than twenty days, and a shorter window cannot catch this one. The bottom-ranked
name is therefore being compared against a control that is mis-struck on that name.

## The language control

`diagnostics.impact_sum_pre_local` is a real freeze in all nine hunts — the English pass was
frozen before the second pass ran, in that order, which is load-bearing.

**The UK's six deltas are `source_locality`, not language, and `eu_resolve.py` refuses to
pool them with the other three.** Averaging them would report the mean of two different
experiments. Today only **three names (QDT, KWS, PHIL) carry a genuine language delta**, and
three names is noise.

Sizes moved a long way in both directions — W7L −1.7 → −6.2, KWS −4.2 → −2.7, KOO −3.2 →
−1.4, CWR 0.0 → +3.5, JDG −2.0 → −1.8 — so the second pass is doing something rather than
nothing. What it is doing cannot be read off one day. **Nothing pools on nine names.**

## No prior European run has resolved

There is no pooled `lean_vs_free_control_rho` to report, because **nothing has ever resolved
in Europe on real findings**. The only two resolved European days are the synthetic
validation runs: 2026-09-16 (uk, n=4, `lean_vs_free_control_rho` **0.40**) and 2026-09-17
(fr, n=3, **1.00** with 0 of 3 names `anchor_covered`). That French 1.00 is the failure mode
this note warns about, observed: with no name carrying a disclosure, the lean collapsed
exactly into the free control. Both ran on fabricated findings and neither says anything
about whether the hunt works.

The previous run for this same event date (2026-09-19, three markets, 2 of 9 names hunted)
is preserved at `_run1-2026-09-19-seal/` with a README. **Do not pool its two names with
these nine** — they were scored against a seal struck three sessions earlier.

## One day is not a result

Nine names, one market two-thirds of them, no option anchor, three positioning anchors, no
resolved European history to calibrate against, and a scorer whose own US record is
ρ=+0.243 (p=0.156) shipped against ρ=+0.407 raw. This is one day. It is not evidence about
the method, in either direction, and it will not be until many days pool.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
