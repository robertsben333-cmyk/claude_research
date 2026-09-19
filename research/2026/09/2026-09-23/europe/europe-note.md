# Stage EU — Europe ranking for 2026-09-23

**Two names were hunted and seven were not. This is a stage test, not a day's ranking,
and nothing in it should be read as a result.** It is the first run in which a German
and a French name have been through this stage with real research rather than synthetic
findings; both confirmation paths, the French short register and the new day archives
were exercised on the way.

| # | mkt | ticker | company | `impact_sum` | conviction | session | lean | anchor | turnover/day |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FR | QDT | Quadient SA | **+0.90** | 0.90 | amc | −0.09 | none | $0.51m |
| 2 | DE | KWS | KWS SAAT SE & Co KGaA | **−2.10** | 2.10 | bmo | −0.22 | none | $1.04m |
| — | UK | BOKU, CWR, JDG, KOO, RSW, TIME, W7L | | not ranked | | | | | |

`ranking_key` is `impact_sum`, as `edge-scores.json` reports it. **Neither name clears
the conviction floor of 3.0 points**, and over the whole US sample the sign below that
floor was a coin flip — so neither number here is a call, and the day has no top or
bottom worth emphasising.

## Why seven names are missing, and what that costs

The session that ran this stage **cannot spawn subagents**, so the nine hunts could not
be fanned out to `unpriced-hunter-uk/fr/de`. Rather than run nine shallow hunts in one
context, the two names the test was for — the first German and the first French name in
this stage's history — were hunted properly by the session itself, and the seven UK
names were left unhunted and appear as `not ranked: no hunt`. This is a **shed against
`europe_hunt.degrade_order`**, recorded here and in the run log.

Two things that costs, and they should be read before the numbers above:

- **A two-name ranking is not a ranking.** Spearman on two points does not exist.
- **The two hunts are not isolated from each other or from the guidance file.** Both
  were run in one context, so they are not independent, and the session had read
  `researcher_europe/LESSONS.md` before either hunt began. **`pre_lessons` is therefore
  equal to the emitted set by construction in both hunts and is not a measurement.**
  `impact_sum_pre_local` is a real freeze — the English pass genuinely preceded the
  local one in both cases — but a two-name delta is noise and must not be pooled.

## The two hunts, in one line each

**QDT (Quadient, amc) +0.90.** The print carries a scheduled binary the hunt cannot
resolve: the update on the Lockers strategic review is due *with* these results, with
Rothschild, Société Générale and Darrois appointed. What the tape says is that the
market has stopped paying for it — +6.0% on 96k shares on the 20 July announcement,
and back to €12.52 against €12.00 the session before. Two smaller findings: Janus
Henderson crossed above **5.05%** of capital and voting rights on 23 July (AMF
declaration 226C1172, a French-language PDF with no press account found), and the Digital
line is already out — Q2 bookings +20% LFL pre-released on 24 August, which the market
paid ~+7% for over three sessions and has since given back. **Driving finding and URL**:
https://www.globenewswire.com/news-release/2026/07/20/3329438/0/en/quadient-announces-a-strategic-review-of-its-lockers-solution.html

**KWS (KWS SAAT, bmo) −2.10.** The FY 2025/26 outturn is largely known after the 9M
numbers, so the news is the FY 2026/27 guide, and both findings are about it: European
sugarbeet area is contracting again into the 2027 campaign — EU sugar price −30% y/y
(€767→€529/t), German area −12.6% to ~338,700 ha, Südzucker asking growers to stop,
a materially lower guaranteed beet price in the new 2027/28 model — and Russia, which
KWS itself named in the February cut. **Driving finding and URL**:
https://www.agrarheute.com/markt/sinkende-preise-zuckerkonzerne-raten-landwirten-weniger-zuckerrueben-anzubauen-637632

Both hunts held their emitted number **inside** the sum of their findings, for the
reason `LESSONS.md` gives: KWS's negative agrees with the only directional number in its
baseline, and Quadient's positive sits on a name whose last two prints moved −17.8% and
−15%.

## The universe and the draw

`selection.method`: **all 9 eligible names (at or under the cap)** — no draw was needed,
so nothing was dropped at random. 22 rows scheduled across the three markets, 13 dropped
below the turnover floor or with no tape, 9 eligible: **uk 7, de 1, fr 1**.

**The floor was $200k/day for the first time** (it was $1m until 2026-09-19, moved on the
operator's instruction for cross-market comparability). Quadient at $0.51m/day is a name
the old floor would have excluded, so **the French leg of this test exists because of that
change**. KWS at $1.04m/day would have cleared either.

## What a reader has to know about these baselines

- **`options` is null on every name, in all three markets.** Europe has no retrievable
  single-stock option chain, so this stage runs in the same anchor-less regime as Japan —
  the regime that produced ρ=+0.073, p=0.45 over 104 events on the sealed backtest corpus
  (`archive/backtest/FINDINGS.md` §33). Nothing here refutes that.
- **All three short registers resolved for this run**: FCA 419 issuers (as of 31 August),
  Bundesanzeiger 283 positions (17 September) and — for the first time — **the AMF's, 74
  issuers (16 September)**. France's register was recorded as unreachable until
  2026-09-19; it is intermittent, not blocked.
- **And neither hunted name is named by its register.** `anchor_covered` is false for
  both: their disclosed net short is the 0.5% truncation floor, not a measurement, so
  `priced_lean_pct` for both is the 20-day run-up alone — which is also the free control.
  Two of the nine baselines do carry a real disclosed short (CWR 13.21%, JDG 1.67%), and
  neither was hunted.
- **`history.basis` is `estimated_from_cadence` for both hunted names** — the dates are
  inferred by stepping the vendor's cadence backwards, so they are a **scale** for how far
  the name travels and not a record that a print happened on those dates. The seven UK
  baselines carry `observed_rns` dates from Investegate. This repo has already ranked,
  traded and lost money on a cadence prior read as evidence.
- **The lean's weights are priors borrowed from the US runs** and are measured nowhere in
  Europe. `eu_resolve.py` ranks each component separately so measurement can replace them.
- **No name carries `session_unresolved`** — both hunted sessions were additionally
  confirmed against the issuer's own calendar (KWS's Finanzkalender: 23 September, 07:00
  CEST; Quadient's financial calendar: 23 September, after close).
- **`lean_vs_free_control_rho` from the previous resolved run**: there is none. No
  European run has resolved.

## Resolving this run

Not before **2026-09-25**, and not because of the archives — those are current. Yahoo's
European daily closes lag: measured on 2026-09-19, `.PA` and `.DE` carried timestamps for
09-17 and 09-18 with null closes, and `.L` was one session behind. `eu_resolve.py` marks
every such row `move_pending` and refuses to confirm a date that has not happened yet, so
a premature run reports nothing rather than killing names that have not reported.

**One day is not a result, and two names are not a day.**

---

*This is research, not investment advice. It is a forecasting exercise over public
information. No orders are placed by this stage and none may be.*
