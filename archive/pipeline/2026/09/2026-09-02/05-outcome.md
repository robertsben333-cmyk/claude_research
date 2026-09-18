# Outcome — 2026-09-02

Scored 2026-09-04. Measurement: close before the print → close after the first full
session following it, applied identically to every name below (both the AMC names that
reported the evening of 09-02 and the BMO name that reported before the 09-03 open share
the same 09-02 → 09-03 window).

| Ticker | Panelled | Call | Expected move | Actual move | Direction | Band hit | Reversal fired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI | Yes | Neutral / No Edge | ±11.3% | **+3.61%** | Hit (below expected) | No | Yes |
| SNOW | Yes | Neutral / No Edge | ±14.0% | **+16.56%** | Miss (moved hard, no view) | Yes | No |
| AVGO | No (prelim +6) | — | — | **−2.74%** | Prelim miss | — | — |
| PVH | No (prelim −15) | — | — | **+0.24%** | Prelim miss (near-noise) | — | — |
| NTAP | No (prelim −10) | — | — | **+2.55%** | Prelim miss | — | — |
| VSXY | No (prelim +12) | — | — | **−13.17%** | Prelim miss | — | — |

## AI — hit, and the panel's own bull case actually fired

Adjusted EPS −$0.20, beat consensus of roughly −$0.25 to −$0.26; revenue $52.4M, a
narrow beat, down ~25% y/y. Q2 FY27 revenue guided to $51–55M vs. ~$56.6M consensus —
below Street — and several outlets initially framed this as a several-percent
after-hours decline. By Thursday's regular close the stock was actually up 3.61%,
comfortably below the 11.3% unsigned expected move and below the low end of its own
5.7–21.8% band. The Neutral call scores a hit under the below-expected-move convention.
Unusually, the red-team persona's "reversal case" here was itself the *bullish* thesis —
a heavily shorted, seller-exhausted setup (34.65% of float short, 9.65 days to cover)
where an in-line Q1 with a reaffirmed FY27 range would be enough to force covering even
on a soft Q2 guide — and that is close to what happened: the weak guide did not sink the
stock. Stage-2 preliminary (−22, bearish) called the wrong direction, though on a move
this small the sign flip is low-information.

## SNOW — miss, the day's largest panelled magnitude break

Adjusted EPS $0.62 vs. $0.45 consensus (beat), revenue $1.55B vs. ~$1.48B consensus
(beat, product revenue +37% y/y). Full-year product revenue guidance raised to $6.07B
(36% growth) from $5.84B (31% growth) — an acceleration, not a deceleration. The stock
had sold off ~4% into the print, then jumped ~22% after hours and settled at +16.56% by
Thursday's close, breaking the 14.0% unsigned expected move. The Neutral call is a miss
under the below-expected-move convention, though it lands inside its wide 7.0–38.3%
band. The red-team's specific reversal case — a beat-and-raise that sells off anyway
because the buyside bar (implied ~33%+ growth) sits above the sell-side bar — did not
fire: 36% guided growth against a 34% prior print read as acceleration, not
deceleration, and the stock ripped instead of fading. Stage-2 preliminary (−10, bearish)
called the wrong direction.

## AVGO — preliminary miss (not panelled)

EPS beat consensus by ~35.5%, revenue beat by ~86% y/y — an enormous beat on both
lines — but Q4 FY26 revenue guidance ($34.8B) landed just below the ~$35.03B consensus,
and that alone was enough to send shares down as much as ~6–7% intraday before a partial
recovery to close −2.74%. Preliminary read (+6, weakly bullish) called the wrong
direction, though it was weakly held to begin with.

## PVH — preliminary miss, near-noise (not panelled)

EPS beat consensus, but ~$1.80 of the $3.70 print was a one-time tariff-refund benefit,
and revenue was roughly flat to slightly light. Full-year outlook reaffirmed alongside a
$439M non-cash goodwill impairment. Stock closed +0.24% — essentially flat. Preliminary
read (−15, bearish) is a technical miss on sign, but a move this close to zero carries
little information, the same caveat noted for BILL on 2026-08-19.

## NTAP — preliminary miss (not panelled)

A clean beat-and-raise — EPS beat by ~21.5%, revenue beat by ~10.2%, both full-year
guides raised — with an initial sell-the-news dip that recovered to close +2.55%.
Preliminary read (−10, bearish) called the wrong direction.

## VSXY — preliminary miss (not panelled)

EPS beat consensus, but the beat leaned heavily on >$140M of one-time tariff refunds in
Q2 operating income, revenue slightly missed consensus, and the Q3 operating-income
guide disappointed even as full-year sales/EPS guidance was raised headline-wise. Shares
gapped down at Thursday's open and kept falling to close −13.17% near the day's low —
the largest single-name preliminary miss (by magnitude) across all three runs scored
today. Preliminary read (+12, bullish) called the wrong direction.

## Where the process failed

**The preliminary read went 0-for-6 today — its worst day since scoring began.** Every
one of AI, SNOW, AVGO, PVH, NTAP and VSXY moved opposite to its preliminary direction
score (PVH is a near-zero technical miss). Combined with 08-27 (3/5) and 09-01 (3/6),
the preliminary read's running hit rate across every researched name to date has fallen
from 62.5% (5/8, as of the last ledger update) to 44% (11/25) with this batch folded in
— and the panel's own hit rate over the same stretch has landed at exactly the same 44%
(4/9). The earlier narrative — "the cheap stage-2 read keeps calling direction better
than the panel" — does not survive a larger sample. Both are now roughly a coin flip.

**A pattern across all three runs scored today: beat-and-raise prints that still sell
off, and reaffirmed-or-mixed prints that still rally, are far more common than either
the preliminary read or the panel's own certainty tiers suggest.** AVGO, MRVL, RBRK
(08-27) and CRDO, MDB (09-01) all beat and, in most cases, raised guidance, and all
still fell — margin or forward-guide detail below the headline consistently mattered
more than the beat/miss framing that both the preliminary score and much of the panel's
own commentary lean on.

**Certainty tiering is still running backwards with a larger sample.** AI and SNOW were
both tagged High-certainty; AI hit (barely, on a near-zero move) and SNOW missed by the
day's largest panelled magnitude. Across all 9 panelled calls scored to date, High
certainty now stands at 2 hits of 5 (40%) versus Med certainty's 2 of 4 (50%) — not a
large gap, but the direction has not once favoured High since this was first flagged on
2026-08-26, and the sample is now large enough that `scripts/synthesize.py`'s certainty
logic deserves a direct look rather than more waiting.

---

*This is a forecasting research exercise over public information. It is not investment
advice.*
