# Stage EU — Europe ranking for 2026-10-19

**The answer: no name clears the 2.8 conviction floor. All four `impact_sum` values are small
and negative, from −0.60 to −1.20. The panel selected one name, ITM (ITM Power), on the short
side, 3 of 4 judges.** Four names were ranked, three UK and one Swedish, all reporting before
the open on Monday 19 October. BKS (Beeks) and TSTL (Tristel) tie at the top at −0.60. AIRA
(AI Revenue Assistant) is at the bottom at −1.20. Every hunter found the period's numbers
already public, so the reaction will turn on the first outlook statement.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were
sealed on Friday 2026-10-16 at about 13:45 UTC, while the European markets were still
trading. Every sealed spot is therefore an **intraday price, not a close**. The realised move
is measured from daily bars: close(2026-10-16) → close(2026-10-19).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | uk | BKS | Beeks Financial Cloud | **−0.60** (p48) | no | −0.48 | 6.0 | 46 | bmo. Notice of Results; every prior results RNS 07:00 |
| 2 | uk | TSTL | Tristel | **−0.60** (p48) | no | −0.24 | 4.0 | 47 | bmo. Notice of Results; 09:30 analyst briefing |
| 3 | uk | ITM | ITM Power | **−1.10** (p68) | no | −0.68 | 8.5 | 46 | sealed `bmo?`. The hunter confirmed bmo: 09:00 presentation, every results RNS 07:00 |
| 4 | se | AIRA | AI Revenue Assistant Software | **−1.20** (p70) | no | −0.80 | 10.0 | 46 | sealed `bmo?`. The hunter confirmed bmo: issuer says 08:30 CEST |

`impact_scaled` is the hunter's second, separate measurement. It is not the key and no floor
applies to it. The bracketed figures are percentiles of |value| among names sized by
Opus 5.5. They describe scale, not rank. BKS and TSTL tie, and the scorer's order inside a
tie carries no information.

**What was already public, per name (`already_public`):**
- **BKS:** the FY26 trading update of 15 July gave revenue c.£40.0m, underlying EBITDA
  c.£16.0m and net cash c.£0.63m.
- **TSTL:** the 22 July update gave revenue £51.1m and adjusted PBT of at least £11.5m.
- **ITM:** revenue (17 Feb), cash (9 Apr) and the EBITDA-loss upgrade (8 Oct) are all out.
- **AIRA:** nothing was pre-released, but there is no estimate anywhere to beat. The only
  coverage, a commissioned Kalqyl note, publishes none.

**What is new in the release (`new_in_release`):**
- BKS, TSTL and ITM each give their **first FY27 outlook**. For ITM it is the first FY27
  guide ever, and ITM says it never guides beyond the current year.
- TSTL's results are also its new CEO's first, with a promised "vision".
- AIRA's Q3 is the last quarter before Aira for Fortnox launches commercially.

No hunter could source a FY27 consensus, so every outlook-dependent finding is capped small.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters'
evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran on
their own pinned `-intl-` agents, with no fallback, and each covered 4 of 4 packs. The
selection rule for this market is `consensus`: a name is selected when 3 of 4 judges put it
in their own top 20%. Each judge's top 20% starts at Opus 5 |1.68|, Opus 5.5 |0.91|,
Sonnet 5.5 |1.08| and Fable 5.1 |1.32|, measured on 51 live sizes each.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ITM | **yes** | 80 | short | 11 | 86S* | 61S | 88S* | 86S* | 3 | −1.33 | −1.10 |
| 2 | AIRA | no | 82 | short | 11 | 67S | 92S* | 92S* | 78S | 2 | −1.28 | −1.20 |
| 3 | BKS | no | 68 | short | 18 | 80S* | 37S | 76S | 76S | 1 | −0.99 | −0.60 |
| 4 | TSTL | no | 36 | short | 17 | 20S | 31S | 65S | 28S | 0 | −0.30 | −0.60 |

Each member's figure is its percentile 0-100 against its own live range, with L for long and
S for short. A `*` marks a member's own top 20%. Every judge put every name on the short side.

**ITM (selected, short).** The judges' sizes were Opus 5 −2.2, Sonnet 5.5 −1.4, Fable 5.1 −1.5
and Opus 5.5 −0.65. They lean on the hunter's backlog roll-forward from the issuer's own RNS
record: since the January interims (backlog £152m) only one order, MorGen's 20 MW POSEIDON
at FID, has turned firm. That constrains the first FY27 revenue guide
(https://www.investegate.co.uk/company/ITM). The Hydropulse 150 MW build-own-operate heads of
terms bring project-finance needs into the first FY27 cash guide
(https://www.investegate.co.uk/announcement/rns/itm-power--itm/hydropulse-signs-heads-of-terms-for-150-mw-project/9816832).

**The strongest case against** has three parts:
- The 8 Oct guidance update already cut the FY26 EBITDA loss 27% below guide, which lowers
  the FY27 base (https://www.investegate.co.uk/announcement/rns/itm-power--itm/notice-of-preliminary-results-and-guidance-update/9812291).
- The 20-day drawdown (−12.5%) is milder than the sector's (Plug −30.6%, Ceres −23%).
- The disclosed short is covering, from 2.42% to 2.22%.

Opus 5.5 kept ITM out of its top 20% (61st percentile). The FY27 bar is an S&P snippet, not a
sourced consensus.

**Where the panel and the hunter disagree most:**
- **AIRA** has the day's highest `panel_pct` (82) but only k=2. Opus 5 and Fable 5.1 sized
  it large and close to a coin flip (abs 11–14, p_up 44–45).
- **BKS:** Opus 5 is alone in its top 20% at −1.8, on the cash-flow line. Opus 5.5 sees
  almost nothing (−0.39).
- **No name sits above the floor**, so there is no hunter-selected name for the panel to
  have passed over.

**What the numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales still rest on 51 live sizes each plus the frozen E-P seed.
- In the four-model re-judge, the judges ranked Europe better than the live hunt, but
  nothing about this market's panel is established.

## The top and bottom name

- **BKS and TSTL (−0.60, tied at the top).**
  - **BKS:** the findings nearly cancel. +0.6: exit ACMRR of £34.0m covers about 76% of the
    only published FY27 revenue estimate, which is the same coverage FY26 had going in.
    −1.0: the audited cash-flow statement will show the full drain behind net cash falling
    from £6.96m to £0.63m. Both rest on the trading update
    (https://www.investegate.co.uk/announcement/rns/beeks-financial-cloud-group--bks/fy26-trading-update/9668956).
    The stock fell 20% into the print with no RNS. That fall is sized at 0, because no cause
    was found. Beeks has fallen on each of its last five results-type releases.
  - **TSTL:** the pre-released period is sized at 0. Two −0.3 inferences remain:
    - Implied H2 FY26 growth slowed to about 6% from 14% in H1.
    - The new CEO's first "vision" is unknown
      (https://www.investegate.co.uk/announcement/rns/tristel--tstl/notice-of-results/9797743).
- **AIRA (−1.20, bottom).** A stock at about 60x Q2 ARR (SEK 1.77m) reports the last quarter
  before Aira for Fortnox is commercial. The hunter has three findings:
  - −1.0: the print cannot validate the Fortnox story the stock ran on
    (https://mfn.se/a/aira/aira-oppnar-early-access-till-aira-for-fortnox-med-guldbiljetter).
  - −1.0: cash of SEK 14.3m at end-June against about SEK 5.3m a quarter of burn plus
    capitalised development
    (https://storage.mfn.se/235f4e56-c739-42ab-b9e1-4f1649ae481b/aira-interim-report-q2-2026.pdf).
    The Q3 cash estimate of about SEK 9–10m is the hunter's arithmetic, not a sourced figure.
  - +0.8: the release could carry the first count of early-access demand.

## What the reader must carry

**Selection.** `all 4 eligible names (at or under the cap)`: there was no random draw,
because 4 eligible names is under the cap of 20.
- `by_market`: uk 3, se 1. Nothing came from de, fr, dk, no, fi, it, es or pl.
- 8 rows were scheduled and 4 were dropped (below the $100k floor or otherwise ineligible).
- **Market concentration: uk is 75% of the day**, across 2 markets.

**Calendar sources:**
- **Yahoo's calendar endpoint failed on every batch in all ten markets.** The day therefore
  rests on the TradingView vendor feed, the UK RNS calendar and the issuer calendars.
- The UK RNS calendar dated 3 names for the 19th. It added ITM and confirmed BKS and TSTL.
- Inderes added AIRA and TRAC_B in Sweden. TRAC_B did not survive the eligibility screen.

**Session-unresolved:** AIRA and ITM were sealed `bmo?`. Both hunters then confirmed bmo
from the issuers' own notices, so the resolver will measure both windows for them anyway.

**Anchors:**
- `options` is null in all ten markets, so Europe runs in the anchor-less regime: ρ=+0.073,
  p=0.45 over 104 events on the sealed corpus.
- The UK register (FCA, as of 2026-10-15, 424 rows) and the Swedish one (FI, as of
  2026-10-16, 335 rows) both read.
- **1 of 4 names carries `anchor_covered: true`:** ITM (2.22%, down from 2.42%). BKS, TSTL
  and AIRA are truncated zeros, not anchors. For those three, `priced_lean_pct` is the
  run-up alone.

**Weak legs:** Spain and Poland contributed 0 names, and Germany contributed 0.

**Reaction history:**
- `history.basis` is `observed_rns` for BKS, ITM and TSTL, which are real dated history.
- AIRA's is `estimated_from_cadence` with 0 rows. That is a scale, not a record. AIRA has one
  prior print in the hunter's record (Q2, −4.2%).

**Previous resolved run:** the last resolved European run is 2026-10-08. Its only per-market
`lean_vs_free_control_rho` is UK 1.0 on 3 names. No Swedish figure exists yet. **AIRA must be
resolved within about a week**, inside the Nasdaq Nordic feed's window. AIRA publishes
through MFN, and the hunter found the Nasdaq Nordic feed returns nothing for this issuer, so
its confirmation may resolve null.

**The lean's weights are priors** borrowed from the US runs and measured nowhere in Europe.

**`language_note` highlights** (prose, not evidence):
- AIRA: only the Swedish sources showed that the Dagens Industri piece is paid content
  ("Innehåll från Aira Annons", i.e. "content from Aira, advertisement"). Only the Swedish
  Kalqyl initiation states that it carries no estimates ("har valt att avvakta med
  finansiella estimat", i.e. "has chosen to hold off on financial estimates").
- ITM: German retail press covered it heavily, but none of it was load-bearing.
- BKS and TSTL: nothing the English sources did not already carry.

**Floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign was a coin
flip below it.

**One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
