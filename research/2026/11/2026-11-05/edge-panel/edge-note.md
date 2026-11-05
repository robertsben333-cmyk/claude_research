# Stage E-P — 2026-11-05 amc + 2026-11-06 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel. Since 2026-10-19 it trades the Alpaca paper account (steps 3s and 6b), on the panel's rule only.**
Members that ran: all four, each as its pinned agent: `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5), `panel-judge-fable51` (claude-fable-5-1). No fallback. All four were stopped by the account's 5-hour usage limit at about 18:43 UTC. Opus 5, Sonnet 5.5 and Fable 5.1 had already written 20/20. Opus 5.5 was resumed at 20:43 UTC and finished 20/20 at 20:45 UTC. Every judge covered 20 of 20 packs.
One day is an anecdote.

**The order of steps changed today, on purpose.** The panel finished at 15:45 New York, so the book was bought (step 6b) BEFORE this note was written, to make the 16:00 ET close. Skill order is note first.

Universe: 314 names (257 amc 11-05, 57 bmo 11-06; GTN.A folded; UA folded into UAA by the sweep). The sweep checked 35 names: 25 company-confirmed, 9 unconfirmed (OPEN MNKD SRPT YELP PLSE TBCH XPOF FIGS SERV), 0 phantoms, and 279 were not checked. Cap 20: the 9 unconfirmed names and the 5 lowest on hunt_priority were shed (ARLO NRDS BLMN IRTC CGC). All 20 searchers finished (`search_complete: true`, 0 unfinished, none retried).

## Panel table (every rankable name)

Member percentiles are each judge's own 0-100 percentile against its last 200 live sizes, with the side as L/S (`*` = in that judge's own top 20%). `E[ret]` is the expected return at this panel_pct: gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50. It translates the percentile and is not a separate forecast.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[ret] (80% band) | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ETON | amc | **yes** | 92 | long | 5 | 84L* | 94L* | 98L* | 94L* | 4 | +1.94 | +2.10 | +4.38% [+2.34, +6.25] | 0.70 | 1 | 1.11 |
| 2 | OMDA | amc | **yes** | 92 | long | 3 | 94L* | 87L* | 92L* | 94L* | 4 | +1.76 | +2.70 | +4.37% [+2.32, +6.24] | 0.70 | 1 | 1.25 |
| 3 | FNKO | amc | **yes** | 87 | long | 8 | 78L | 94L* | 95L* | 81L* | 3 | +1.71 | +2.60 | +3.66% [+1.56, +5.64] | 0.66 | 1 | 0.89 |
| 4 | HNST | amc | **yes** | 83 | long | 9 | 76L | 94L* | 90L* | 72L | 2 | +1.32 | +1.50 | +3.11% [+1.04, +5.09] | 0.63 | 1 | 0.80 |
| 5 | AAOI | amc |  | 73 | long | 18 | 48L | 87L* | 92L* | 66L | 2 | +1.20 | -0.70 | +1.84% [+0.32, +3.62] | 0.56 | 0 | 0.00 |
| 6 | SOUN | amc |  | 71 | long | 22 | 78L* | 34L | 94L* | 76L | 2 | +1.21 | +2.30 | +1.64% [+0.25, +3.36] | 0.56 | 0 | 0.00 |
| 7 | GRND | amc |  | 70 | short | 4 | 75S | 64S | 73S | 66S | 0 | -0.91 | -0.60 | +1.53% [+0.21, +3.22] | 0.56 | 0 | 0.00 |
| 8 | TMDX | amc |  | 70 | long | 14 | 62L | 90L* | 52L | 76L | 1 | +1.00 | +1.30 | +1.53% [+0.21, +3.22] | 0.56 | 0 | 0.00 |
| 9 | INOD | amc |  | 59 | short | 11 | 48S | 50S | 74S | 66S | 0 | -0.78 | +0.70 | +0.75% [-0.15, +2.22] | 0.56 | 0 | 0.00 |
| 10 | TRUP | amc |  | 48 | short | 24 | 75S | 34S | 17S | 66S | 0 | -0.66 | -0.30 | +0.29% [-0.44, +1.33] | 0.56 | 0 | 0.00 |
| 11 | OKLO | bmo |  | 47 | long | 27 | 62L | 64L | 62L | 0- | 0 | +0.77 | +0.40 | +0.29% [-0.46, +1.24] | 0.56 | 0 | 0.00 |
| 12 | SG | amc |  | 40 | long | 46 | 64L | 56L | 78L | 39S | 0 | +0.79 | +1.25 | +0.29% [-0.52, +0.92] | 0.56 | 0 | 0.00 |
| 13 | CELC | amc |  | 26 | long | 28 | 11L | 22L | 74L | 0- | 0 | +0.27 | +0.60 | +0.29% [-0.57, +0.84] | 0.56 | 0 | 0.00 |
| 14 | WULF | bmo |  | 24 | short | 30 | 23L | 51S | 17S | 50S | 0 | -0.42 | +1.40 | +0.29% [-0.58, +0.83] | 0.56 | 0 | 0.00 |
| 15 | CARG | amc |  | 16 | short | 36 | 22S | 52S | 42L | 34S | 0 | -0.39 | -0.10 | +0.29% [-0.64, +0.81] | 0.56 | 0 | 0.00 |
| 16 | CRSR | amc |  | 11 | short | 51 | 23L | 76S | 52L | 42S | 0 | -0.12 | +1.90 | +0.29% [-0.68, +0.80] | 0.56 | 0 | 0.00 |
| 17 | UAA | bmo |  | 10 | short | 16 | 11L | 26S | 0- | 27S | 0 | -0.16 | +0.10 | +0.29% [-0.68, +0.80] | 0.56 | 0 | 0.00 |
| 18 | TNDM | amc |  | 6 | short | 57 | 10S | 19S | 83L* | 76S | 0 | -0.24 | +1.40 | +0.29% [-0.72, +0.79] | 0.56 | 0 | 0.00 |
| 19 | UMAC | amc |  | 5 | long | 44 | 15S | 29L | 61L | 54S | 0 | +0.03 | -0.20 | +0.29% [-0.72, +0.78] | 0.56 | 0 | 0.00 |
| 20 | KRUS | amc |  | 3 | short | 28 | 12S | 34S | 42L | 7S | 0 | -0.21 | +1.30 | +0.29% [-0.74, +0.78] | 0.56 | 0 | 0.00 |

## The book (step 6b, sent 20:45:29 UTC = 15:45 ET)

All four selected names were bought long at market and filled: ETON 87 @ 47.48, OMDA 220 @ 18.71, FNKO 573 @ 6.10, HNST 684 @ 4.42. Gross about $14,740, 99.7% of $14,769 equity. Weights are `panel_pct − 60` (32 / 32 / 27 / 23), so no name hit the 50% cap. Mean execution cost against the mid was +0.185. ETON's quote was 40.44 × 53.93 at submission, a 28.6% spread, and it filled at +0.625 against the mid. Exits are dated 2026-11-06: all four are amc, so they go out at the open.

Step 3s sold CAVA (short 100) and U (long 154) from 2026-11-04's book at market, before the packs were built. Both legs were dated to exit 11-05 and were still held at about 13:38 ET.

## The selected names

**ETON (92, long, 4 of 4).** All four judges name the same item: the first full quarter of Hemangeol. Worked from the company's own patient-count and net-price figures, Q3 revenue comes to about $43-46M against a $42.2M consensus, and a third full-year raise this year looks likely. The name has bought its raises: +44% on the Q2 print. *Against:* the sizing is the searcher's own arithmetic on company figures, and Earnings Whispers already frames the same question. The $10M Libervant upfront may be expensed against the 35% EBITDA-margin guide. The option spread is 75% of mid, so the 20% implied move is indicative only.

**OMDA (92, long, 4 of 4).** All four judges name the same arithmetic: 1,091k members in the Q2 10-Q, at a flat ~$83 of revenue per member per quarter, implies about $89-91M. Consensus is $85.8M, which assumes a sequential decline. Short interest is building (6.7 days to cover), and Hinge Health had a record selling season three days earlier. *Against:* the Q2 call was read only through summaries, so a one-off catch-up in Q2 revenue cannot be ruled out, and that is the main risk to the arithmetic. Q1's beat-and-raise still fell 9.6%. Employer GLP-1 coverage cuts for 2027 are a sourced negative for the call. The event date rests on aggregator copies of the company notice; the company's IR page returned 403.

**FNKO (87, long, 3 of 4 in their own top 20%).** Consensus sits exactly on a "roughly flat" guide that Funko has beaten at the top end for three prints, each bought +10 to +18%. Gross-profit arithmetic points to EBITDA at or above the $25-30M top end. JAKKS and Hasbro reported strongly on the same licences after Funko last spoke. Short interest is about 14% of Class A, and an activist holds about 23% economic exposure. *Against:* the soft implied Q4 (−9% to +1%), a fully drawn revolver with debt going current if it is not refinanced by 31 December, a new 12.5% Section 301 toy tariff above the guide's 10-12% assumption, and no tariff-refund windfall this quarter. The short figure is a search snippet.

**HNST (83, long, 2 of 4 in their own top 20%).** The raised full-year EBITDA guide leaves only $4.6-6.6M for H2, below H2 2025 on a higher margin base, and full-year street revenue (~$309M) sits below the company's own $319-325M guide. So a second raise is the base case. *Against:* the Q3 bar is disputed between two aggregators. Kimberly-Clark reported retailer destocking. Diaper revenue keeps falling after two distribution losses. Opus 5 and Fable 5.1 have it outside their own top 20% (76 and 72), so this is the weakest of the four selections.

All four selected names are amc and long, and three of the four turn on the same pattern: guide arithmetic says the bar is set too low. That is one correlated bet, not four independent ones.

## Where the panel and the searcher disagree most

- **AAOI:** searcher −0.70 against panel 73 long. Opus 5.5 and Sonnet 5.5 have it in their own top 20% long; the searcher's lessons pass flipped its draft from +0.6 to −0.7.
- **CRSR:** searcher +1.90 against panel 11 short. The judges split 2 long, 2 short.
- **KRUS:** searcher +1.30 against panel 3 short.
- **TNDM:** searcher +1.40 against panel 6 short. Sonnet 5.5 puts it in its own top 20% long and the other three lean short; spread 57.
- **WULF:** searcher +1.40 against panel 24 short.
- **INOD:** searcher +0.70 against panel 59 short.

## Stage E comparison

Stage E's `edge/` does not exist for 2026-11-05: its Routine is stopped. So there is no overlap or Spearman ρ against stage E today.

## What the numbers are not

- **`expected_return_pct`** (and `expected_edge_pct`, which on a selected name carries the same expectation as a signed move) is what names at that percentile have earned. Its out-of-sample record is weak: a correlation of +0.12 with the realised return over 148 names. It is not a forecast to size on.
- **The weights** (`w_eq`, `w_tilt`) are research and nothing trades them; the book uses `panel_pct − 60`.
- **Certainty** (`p_up`) is recorded and decides nothing, because it did not predict on the development names.
- **The searcher's `impact_sum`** ranks the comparison arm. No name clears the 2.8 floor today; the largest is OMDA at +2.70.
- **Nothing checked the findings** beyond the four judges' reading of them, so a factually wrong item enters at full size.
- **The judges were interrupted.** The 5-hour usage limit stopped all four mid-run. Three had finished their files; Opus 5.5 resumed from its own saved context two hours later, after the searchers' window. Its inputs did not change, but the interruption is recorded.
- **The baselines** were sealed at 18:08-18:12 UTC. The book was bought at 20:45 UTC, and prices had drifted a median 1.11% from the sealed spot (worst ETON −3.99%).

## Context: retail, search and volatility (not used for selection)

These labels are context only; nothing selects, sizes or trades on them. See `score_report.py`'s table: retail ≥50, search quiet and vol ≥58, per name.

## Unfinished searches

None. All 20 searchers returned `search_complete: true`.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
