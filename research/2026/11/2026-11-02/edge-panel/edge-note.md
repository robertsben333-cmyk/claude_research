# Stage E-P — 2026-11-02 amc + 2026-11-03 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** Since 2026-10-19 it is the only stage trading the Alpaca paper account (step 6b, after this note is published).
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), natively, 20 of 20 names each, one part, no fallback.
One day is an anecdote.

Universe: 199 names (103 amc 11-02, 96 bmo 11-03), all baselines sealed before any agent (AAPL, PLTR, VRTX sealed empty: `bars_failed: HTTPError`; their searchers sourced spot and implied move themselves). The sweep was time-boxed and checked 20: 16 company-confirmed, 4 unconfirmed (EBS, HLF, BRCC, PLTR), 0 phantoms, 179 unchecked and shed. All 20 checked names were searched (cap 20); every searcher confirmed its event from a company release, including the four the sweep could not (AAPL rests on Apple-focused outlets quoting Apple's IR page, not on a fetched Apple page). **One searcher hit the per-turn WebSearch budget (IBTA)**; it was marked unfinished, set aside in `hunts/_unfinished/`, and relaunched in a later turn, where it finished. `hunt_status.py check`: 0 unfinished of 20. Share classes on the calendar (CRD.A/B, LBTYA/B/K) were not folded by `edge_universe.py`; none was hunted.

## Panel table

`panel_pct` is the mean of the judges' own percentiles, 0-100, with the side in its own column. A member cell is that judge's percentile against its own live range: L/S gives its side, `*` marks a name in that judge's own top 20%. `E[return]` is what names at this percentile have earned on the panel's side: one number per percentile, gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile; it is not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LIFE | amc | yes | 97 | long | 3 | 92L* | 96L* | 100L* | 99L* | 4 | +2.62 | +1.00 | +4.88% [+2.97, +6.59] | 0.72 | 1.0 | 0.89 |
| 2 | ICHR | amc | yes | 96 | long | 4 | 98L* | 98L* | 89L* | 98L* | 4 | +2.52 | +3.50 | +4.79% [+2.83, +6.53] | 0.72 | 1.0 | 1.16 |
| 3 | DOCN | bmo | yes | 94 | long | 5 | 97L* | 96L* | 86L* | 98L* | 4 | +2.33 | +1.35 | +4.64% [+2.64, +6.43] | 0.71 | 1.0 | 1.00 |
| 4 | CHGG | bmo | yes | 92 | short | 3 | 97S* | 93S* | 88S* | 90S* | 4 | -1.75 | -2.00 | +4.37% [+2.32, +6.24] | 0.70 | 1.0 | 1.04 |
| 5 | UPST | bmo | yes | 90 | short | 2 | 90S* | 89S* | 93S* | 90S* | 4 | -1.71 | -1.20 | +4.16% [+2.08, +6.09] | 0.69 | 1.0 | 1.25 |
| 6 | IBTA | amc | yes | 88 | short | 6 | 80S* | 94S* | 84S* | 94S* | 4 | -1.57 | +0.20 | +3.78% [+1.68, +5.75] | 0.67 | 1.0 | 0.90 |
| 7 | VITL | bmo | yes | 88 | short | 3 | 90S* | 88S* | 84S* | 90S* | 4 | -1.61 | +0.00 | +3.78% [+1.68, +5.75] | 0.67 | 1.0 | 1.21 |
| 8 | INSP | amc | yes | 86 | long | 4 | 92L* | 86L* | 84L* | 82L* | 4 | +1.37 | +1.80 | +3.48% [+1.37, +5.48] | 0.65 | 1.0 | 1.00 |
| 9 | HLF | amc | yes | 81 | short | 13 | 92S* | 70S | 68S | 96S* | 2 | -1.33 | -0.90 | +2.79% [+0.77, +4.74] | 0.61 | 1.0 | 0.75 |
| 10 | AEHR | amc |  | 77 | long | 22 | 39L | 90L* | 84L* | 94L* | 3 | +1.45 | +0.70 | +2.23% [+0.46, +4.09] | 0.58 | 0.0 | 0.00 |
| 11 | PLTR | amc |  | 67 | long | 10 | 52L | 78L* | 72L | 65L | 1 | +0.85 | +2.00 | +1.33% [+0.11, +2.96] | 0.56 | 0.0 | 0.00 |
| 12 | EBS | amc |  | 63 | long | 8 | 52L | 61L | 68L | 72L | 0 | +0.74 | +1.50 | +1.05% [-0.02, +2.60] | 0.56 | 0.0 | 0.00 |
| 13 | HNGE | amc |  | 54 | short | 57 | 96S* | 76S | 44L | 88S* | 2 | -1.31 | -2.00 | +0.36% [-0.31, +1.79] | 0.56 | 0.0 | 0.00 |
| 14 | AAPL | amc |  | 44 | short | 10 | 53S | 42S | 30S | 52S | 0 | -0.56 | -1.80 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.00 |
| 15 | BRCC | amc |  | 26 | short | 56 | 60S | 80S* | 66L | 30S | 1 | -0.58 | +0.60 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.00 |
| 16 | MTCH | amc |  | 23 | long | 28 | 24S | 42L | 44L | 30L | 0 | +0.41 | +0.50 | +0.29% [-0.58, +0.83] | 0.56 | 0.0 | 0.00 |
| 17 | SHOP | bmo |  | 22 | short | 18 | 8S | 52S | 10S | 18S | 0 | -0.23 | -0.40 | +0.29% [-0.59, +0.83] | 0.56 | 0.0 | 0.00 |
| 18 | VRTX | amc |  | 5 | long | 24 | 21S | 4L | 44L | 8S | 0 | -0.04 | -0.10 | +0.29% [-0.73, +0.78] | 0.56 | 0.0 | 0.00 |
| 19 | BETA | bmo |  | 2 | long | 12 | 20L | 0- | 0- | 13S | 0 | +0.00 | +0.70 | +0.29% [-0.75, +0.78] | 0.56 | 0.0 | 0.00 |
| 20 | ROKU | amc |  | 0 | short | 0 | 0S | 0- | 0- | 0- | 0 | +0.00 | +0.10 | +0.29% [-0.76, +0.78] | 0.56 | 0.0 | 0.00 |

**Selected (panel_pct >= 80, all four judges present): LIFE long 97, ICHR long 96, DOCN long 94, CHGG short 92, UPST short 90, IBTA short 88, VITL short 88, INSP long 86, HLF short 81.** Nine names, four long and five short — an unusually wide day. The old 3-of-4 rule selects the first eight; HLF is 2 of 4 (Opus 5 and Fable 5.1 in their own top 20%, Opus 5.5 and Sonnet 5.5 at 68-70). Next: AEHR 77 (3 of 4, Opus 5 at 39), PLTR 67.

## The selected names

- **LIFE (Ethos Technologies), long 97.** Q2 guided $114-118m and printed $189.6m; Q3 guide $160-164m sits 15% below the Q2 run-rate while consensus ($163-168m) hugs the guide, the shape that bought +32% and +21% on the last two prints; the FY guide implies a Q4 below run-rate. Short interest tripled to ~13% of Class A. *Against:* +19% in 20 days, ~46% since the last print, above the average target; EBITDA margin guided down; an EPS bar that disagrees ($0.30 vs $0.09).
- **ICHR, long 96.** Lam (largest customer) printed a record quarter and guided December up; UCTT (same customers) beat the top of its range and guided Q4 +9% on 10-27, and ICHR did not re-rate with it; the stock is −40% in 20 days with no 8-K. The searcher's +3.5 is the only name above the 2.8 floor. *Against:* component shortages at Lam and ICHR's own Q2 part shortage, and ICHR faded 8-10% a session after the UCTT print for a reason no one found.
- **DOCN, long 94.** The CFO reaffirmed Q3, FY and >50% 2027 growth by release on 09-10; the stock is −33% in 20 days with no company news, alongside the CoreWeave/Nebius credit scare; hyperscaler prints and GPU rental prices rose. *Against:* capex and margin pressure, a cut FCF margin, +8.3 put skew, consensus disputed ($306.8m vs $312.8m).
- **CHGG, short 92.** The Q3 guide implies Academic revenue down ~23% q/q, gross margin to 48-49% and EBITDA to $1-2m, so a Q4 guide near breakeven; Skilling growth fell from +9% to +2% and its separate guide was dropped; Coursera guided consumer weaker on 10-29. *Against:* debt-free with ~$38m cash on a ~$78m cap and $120.7m of buyback authority; Chegg beat its guide on both 2026 prints; one-analyst consensus.
- **UPST, short 90.** Q3 originations were pre-released ($4,117.8m, −2.6% q/q); at Q2's take rate that is ~$356m against ~$365m consensus; a reaffirmed FY guide implies a Q4 below the $383-386m street. *Against:* ~26% of float short at a 52-week low with +16.8 put skew, a squeeze path on any reaffirm; the CEO bought 50,000 shares in September.
- **IBTA, short 88.** The price has roughly doubled since the Q2 print to a 52-week high above every target, insiders have sold under plans and filed Form 144s through October, shorts are covering, and DoorDash buying Instacart consolidates two of its publishers. *Against:* Ibotta beat the top of its guide three quarters running; Instacart's Q3 ad revenue beat; a ±25% history.
- **VITL, short 88.** The FY guide needs H2 revenue ≥$421.8m against H1 $353.2m; Cal-Maine's specialty eggs fell in price and volume; wholesale eggs remain oversupplied; cash $21.2m. *Against:* ~20% of float short, a September take-private report (Axios; $15-25 cited) the company never addressed, a stock already −76% from its high.
- **INSP, long 86.** Consensus sits at the guide midpoint after four straight revenue beats; the CFO was cautious about narrowing a wide FY range whose only consensus sits below the midpoint; 15.9% of float short and building, −6.8% in 5 days. *Against:* a ~30% re-rating since the pre-Q2 level, above most targets; a disputed EPS bar.
- **HLF, short 81 (2 of 4).** The first Q4 guide, set by an interim CEO, has to lap India's GST cut against a record ~$250m India Q4 2025 while China and EMEA shrink; the EPS bar is split ($0.62 vs $0.73). *Against:* the quarter was reaffirmed mid-way, a $250m buyback, revenue at or above guide two quarters running; two judges at only 68-70.

## Where the panel and the searcher disagree most

- **LIFE:** searcher +1.00 (below the floor) against panel_pct 97, every judge in its own top 20%. The searcher netted the guide-gap finding (+3.5) against the tape (−3.0); the judges weighed the guide construction more.
- **DOCN, CHGG, UPST, VITL:** searcher +1.35, −2.0, −1.2, 0.0 against 88-94. VITL is the starkest: the searcher's findings net to zero and all four judges put it in their own top 20% short.
- **HNGE:** searcher −2.0; Opus 5 96S and Fable 88S, but Sonnet 44L, so the panel lands at 54 (sd 57).
- **AEHR:** three judges in their own top 20% long (84-94), Opus 5 at 39, so 77 and not selected.

## Stage E comparison

Stage E's `<RUN>/edge/` does not exist: its Routine is stopped since 2026-10-19. No overlap and no Spearman ρ.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 resolved names) — not a forecast to size on. The weights are research. `p_up` is recorded and decides nothing. Nothing checked the findings for factual error (no adversary, one searcher per name), and the key is not reproducible to better than its own size. Searcher sign balance: 12 positive, 7 negative, 1 zero; one name (ICHR) clears the 2.8 floor. Nine selected names on one day is a correlated book: five shorts on stretched or broken names and three of four longs on beaten-down semis/cloud/insurtech; read it as one bet on the panel, not nine.

## Context: retail, search and volatility (not used for selection)

From `edge-context.json`, when written (context only; nothing ranks, selects or sizes on it). The per-name table is in the score_report output in the closing reply.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
