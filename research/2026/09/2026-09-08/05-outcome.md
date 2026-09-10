# Outcome — 2026-09-08

Scored 2026-09-10. Measurement convention: **close before the print → close after the
first full session following it.** TTAN and BRZE reported AMC 2026-09-08; CHWY, SAIL,
SIG and ASO reported BMO 2026-09-09. All six resolve on the same window: close
2026-09-08 → close 2026-09-09. All six reported on schedule — none delayed.

| Ticker | Panelled | Call | Expected move | Actual move | Direction hit | Band hit | Implied broken | Reversal fired | Prelim score | Prelim hit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TTAN | Yes | Neutral / No Edge | 11.5% (band 5.8–18.4%, implied 13.14%) | **−29.98%** | **Miss** | No | **Yes** | **Yes** | +25 | **Miss** |
| CHWY | Yes | Neutral / No Edge | 9.4% (band 4.7–17.4%, implied 10.65%) | **−10.83%** | Hit (near-exact) | Yes | No | No | +16 | Miss |
| SAIL | No | — | — | −1.18% | — | — | — | — | −18 | Hit |
| BRZE | No | — | — | −21.73% | — | — | — | — | −15 | Hit |
| SIG | No | — | — | **+23.96%** | — | — | — | — | +18 | Hit |
| ASO | No | — | — | +14.40% | — | — | — | — | −12 | Miss |

Day totals: panelled 1/2 (50%, Neutral-hit convention); preliminary 3/6 (50%, all
researched names).

## TTAN — the largest magnitude miss scored to date, in either direction

ServiceTitan beat on both lines — EPS $0.40 vs $0.36 consensus (+11.1%), revenue
$292.76M vs $285.14M (+2.67%, +20.9% YoY) — but GTV growth decelerated roughly 200bps to
17% YoY. The stock gapped down hard at the open and kept falling through the session to
close $81.58 → $57.12, **−29.98%**, more than 2x the 13.14% event-implied move and
far outside the panel's own 5.8–18.4% band.

This is the panel at its most confident (`certainty_tier: High`, disparity 8.7,
"aligned" — all seven personas independently leaned mildly bullish, +8 to +20) and it
was wrong by the widest margin in the ledger so far. The mechanism the panel got right
was the *risk*, not the *call*: the red-team persona's own stated downside case —
*"If the SaaS de-rate is still mid-cycle, a good quarter gets sold anyway, exactly as it
did for Salesforce and Workday this year"* — is close to exactly what happened. A real
beat on both headline lines still got crushed on a growth-deceleration read, the same
pattern that hit Salesforce and Workday earlier in the year and that this run's own
options-positioning persona flagged as the live risk to the bull case ("a clean beat
with in-line guide has no forced buyer left and gets sold into vol crush"). The red-team
persona named the correct mechanism and assigned it a direction_score of only +8 (still
net positive) and a reversal_risk of 55 — the mechanism was there in the file, just not
weighted anywhere near enough to move the panel consensus (+15) off a mild bullish lean,
let alone flip it. The deep-dive prelim read (+25) missed by the same margin, so this is
not a case where the panel underperformed a better single-analyst read — both were
wrong, and by a similar amount.

**What would have caught this:** the panel had the deceleration story on the table
(FY27 guide implying H2 growth stepping down to ~15% from 25%, called out explicitly in
the advice note's own "what would change these calls" section) but treated it as a
magnitude risk, not a direction risk. This is a fixable finding about how
`scripts/synthesize.py` weighs a named red-team mechanism against consensus direction
score, not "the market was irrational."

## CHWY — a clean print, sold anyway, landing almost exactly on the implied move

Chewy's print was, on paper, a genuinely good one: EPS in line, revenue at the high end
of its own guide, FY26 sales and margin guidance both raised and narrowed. The stock
still fell **−10.83%**, gapping down ~6% at the open and extending through the session
with no reversal. That is close to exactly the panel's own red-team mechanism: revenue
consensus already sat at the very top of management's guide, so even a beat-and-raise
had limited room to surprise, and the market read a "merely good" print as no better
than priced. The stated upside-reversal scenario for this call (a steady quarter plus
the buyback squeezing a loose short base) did not fire — the bearish lean held instead.

The call itself scores as a hit: 10.83% actual against a 9.4% expected move and 10.65%
implied move is a near-exact match, and it sits comfortably inside the 4.7–17.4% band.
The prelim read (+16) called the wrong sign; the panel's own genuine split (disparity
28.2, five of seven personas leaning down) captured the risk the single-analyst dossier
missed.

## SAIL, BRZE, SIG, ASO — the shed names, scored on prelim only

These four cleared every panel-eligibility floor but were shed by rank under
`panel.names=2`, so their stage-2 preliminary reads stand as the only forecast:

- **SAIL** (−1.18%): a near-noise move — gapped down 4.2% but rallied intraday above the
  prior close before fading. Prelim (−18) right-signed on a beat/slight-miss print.
- **BRZE** (−21.73%): beat on both lines and raised FY guidance, but a soft Q3 EPS guide
  and a slowing customer-add pace (FCF margin 12.7% → 9.6%) drove the stock down hard.
  Prelim (−15) right-signed and the strongest single preliminary call of the run.
- **SIG** (+23.96%): the day's largest move. A large EPS beat plus a meaningful FY27
  guidance raise, amplified by a >18%-of-float short base. Prelim (+18) right-signed.
- **ASO** (+14.40%): EPS beat and a raised FY guide (helped by tariff refunds) drove a
  clean gap-and-hold higher. Prelim (−12) wrong-signed — the one preliminary read this
  run to miss on an otherwise straightforward beat-and-raise.

## What this run adds to the standing findings

**High-certainty still is not out-hitting Med-certainty.** TTAN and CHWY were both
scored `certainty_tier: High`. One hit, one missed — but the miss is the largest
magnitude break in the ledger, which pulls the High-tier hit rate further from Med's,
not closer. See the updated `LEDGER.md` certainty table.

**Still zero directional calls in fifteen panelled tries.** TTAN and CHWY are the
fourteenth and fifteenth panelled calls, and both landed Neutral / No Edge, same as every
one before them. TTAN's disparity was the tightest scored yet (8.7, all seven personas
independently positive) and it *still* did not clear the ±25 Lean threshold on magnitude
— worth a direct look at whether the Lean/Strong thresholds in `scripts/synthesize.py`
are calibrated at all, given a panel this aligned has now twice (TTAN here, and closely
on ABM in the prior run) sat just under the line on a call that then moved hard.

**A specific red-team mechanism naming the right story, at the wrong weight, is now the
most common failure mode in the ledger** — not "wrong mechanism" but "right mechanism,
insufficient weight against consensus." TTAN is the sharpest example yet, following the
same shape as ABM (09-04/09-07) and CXM (09-01) where the red-team's own "what would
break my case" language matched the outcome but the headline direction score did not
move enough to reflect it.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
