# Stage E-P v3b — 2026-11-16 amc + 2026-11-17 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.**
All four judges ran on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5, Fable 5.1. Every judge covered all 20 names.
One day is an anecdote. v3b is judged only pooled, by `v3b_compare.py`, against the pre-registration; no read before 20 run days.

**Run facts.** This was a late retry: the first fire at 18:40 UTC stopped because the baseline sealer sent a personal contact to SEC. Main gained the `SEC_USER_AGENT` fix (`1917c874`), and the run restarted on the operator's request. The baselines were sealed 19:01 UTC (14:01 ET), after stage E-P's (18:15 UTC). Universe 70 names (43 amc 11-16, 27 bmo 11-17). The sweep confirmed 22 from company sources, left 48 unconfirmed (38 small caps never searched for time), and flagged 4 likely phantoms (PAGS XP SUPV SMWB). 20 hunted (7 amc, 13 bmo); HD and SR were shed on priority. All 20 searchers ran as `unpriced-searcher-v3b` with no fallback. All 20 hunts are `search_complete: true` and carry `expectations`, `next_guide` and an `evidence_type` on every item, so none was flagged `v3b fields missing`. HUYA's baseline was amended from `suspect` to `unknown` after its hunter launched: the 11-05 6-K was a share-pool filing, and the company's release confirms 11-17 bmo.

## Panel table

`panel_pct` is 0-100 with the side in its own column. A `*` marks a judge's own top 20%. **v3b** reads each judge against `panel-history-v3b.json`; **E-P scale** reads it against stage E-P's live range (dry run). Today they are identical, because the v3b history is still the seeded copy of E-P's. **p_clear** is the judges' mean `p_clears_real_bar`, and **guide** is the most common `guide_direction`. E[return] is stage E-P's calibration curve, **not one fitted on v3b**. It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50.

| # | ticker | sess | sel | pct v3b | pct E-P scale | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | impact_sum | E[ret] (80%) | P(right) | p_clear | guide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | OMER | amc | **yes** | 87 | 87 | long | 8 | 75L | 98L* | 91L* | 85L* | 3 | +6.00 | +3.67% [+1.57, +5.66] | 0.66 | 54 | no_guide |
| 2 | ENR | bmo | **yes** | 86 | 86 | short | 10 | 70S | 90S* | 92S* | 94S* | 3 | -2.00 | +3.57% [+1.46, +5.56] | 0.66 | 33 | initiate |
| 3 | RCAT | amc | | 76 | 76 | short | 22 | 42S | 97S* | 72S | 92S* | 2 | -2.70 | +2.07% [+0.40, +3.90] | 0.57 | 38 | cut |
| 4 | SHAZ | amc | | 74 | 74 | short | 17 | 50S | 68S | 84S* | 94S* | 2 | -0.50 | +1.96% [+0.36, +3.77] | 0.57 | 38 | unknown |
| 5 | POWL | amc | | 70 | 70 | short | 16 | 56S | 81S* | 53S | 91S* | 2 | -1.00 | +1.59% [+0.23, +3.29] | 0.56 | 41 | no_guide |
| 6 | DIS | bmo | | 56 | 56 | short | 6 | 64S | 58S | 53S | 49S | 0 | +0.00 | +0.46% | 0.56 | 38 | maintain |
| 7 | KLAR | bmo | | 44 | 44 | short | 27 | 42S | 0 | 71S | 62S | 0 | -0.70 | +0.29% | 0.56 | 40 | maintain |
| 8 | VIK | bmo | | 28 | 28 | short | 11 | 23S | 46S | 16S | 28S | 0 | +1.00 | +0.29% | 0.56 | 42 | maintain |
| 9 | OPRA | bmo | | 27 | 27 | short | 8 | 30S | 37S | 16S | 23S | 0 | -0.70 | +0.29% | 0.56 | 41 | maintain |
| 10 | AS | bmo | | 26 | 26 | long | 9 | 23L | 25L | 16L | 41L | 0 | +1.10 | +0.29% | 0.56 | 48 | raise |
| 11 | TME | bmo | | 25 | 25 | short | 11 | 34S | 6S | 30S | 32S | 0 | -0.70 | +0.29% | 0.56 | 40 | no_guide |
| 12 | INFQ | amc | | 22 | 22 | long | 32 | 44L | 26L | 30S | 49L | 0 | +1.60 | +0.29% | 0.56 | 46 | initiate |
| 13 | API | amc | | 20 | 20 | long | 6 | 14L | 28L | 24L | 14L | 0 | +1.20 | +0.29% | 0.56 | 44 | maintain |
| 14 | JD | bmo | | 18 | 18 | short | 10 | 18S | 28S | 24S | 3S | 0 | -0.70 | +0.29% | 0.56 | 42 | no_guide |
| 15 | HUYA | bmo | | 18 | 18 | short | 11 | 10S | 9S | 16S | 36S | 0 | -0.30 | +0.29% | 0.56 | 43 | no_guide |
| 16 | OCSL | bmo | | 16 | 16 | short | 7 | 6S | 21S | 24S | 14S | 0 | -0.60 | +0.29% | 0.56 | 48 | maintain |
| 17 | MNSO | bmo | | 16 | 16 | short | 31 | 37S | 37L | 29S | 36S | 0 | +0.00 | +0.29% | 0.56 | 42 | raise |
| 18 | YALA | amc | | 16 | 16 | long | 11 | 6L | 30L | 24L | 4L | 0 | +1.90 | +0.29% | 0.56 | 49 | maintain |
| 19 | WB | bmo | | 14 | 14 | long | 4 | 18L | 11L | 16L | 8L | 0 | +0.30 | +0.29% | 0.56 | 52 | no_guide |
| 20 | ESLT | bmo | | 4 | 4 | long | 10 | 6S | 11L | 16L | 8S | 0 | -0.20 | +0.29% | 0.56 | 46 | no_guide |

`weight_equal` is 1/2 on each selected name; nothing trades either weight. The retail, search and volatility context labels are in `edge-context.json` and the score report; the panel decides nothing on them.

## Selected names

**OMER (long, panel_pct 87, amc today).** The searcher's evidence includes a company statement from 2026-10-16: in the release in which the CHMP upheld its negative opinion, Omeros said it is ending EU compassionate use because of "increasing demand for YARTEMLEA drug supply in the U.S. commercial market". No preview found picked it up. Ordering accounts went from 30 to 73 by 30 June. The NTAP add-on payment started 1 October. Short interest is about 17% of float with 7.8 days to cover. Three judges put it in their own top 20%, and Opus 5 at its 75th percentile. *Strongest case against:* the revenue bar is disputed ($30.9M at Earnings Whispers against $35.5–38.0M elsewhere), and against the high figure the searcher's own ~$33M estimate is a miss. The 25-delta skew of +10.65 pays for downside. The ATM spread is 72% of mid, so the 16% implied move is only indicative.

**ENR (short, panel_pct 86, bmo 11-17).** The quarter is pre-guided ($1.25–1.35 against consensus $1.30–1.31, whisper $1.35), so the move turns on the first FY27 guide. The street's FY27 of $3.34 is about flat on FY26, while FY26 carries a one-time $64.1m tariff-refund benefit in cost of goods (10-Q). Last November's first guide came in 7% under the street and the stock fell 18.5%. The stock is up about 25% since August and sits above its $22 mean target. *Strongest case against:* short interest is about 11–12% of float with 7.6 days to cover, so a clean guide has squeeze fuel. The baseline has no skew, and the ATM spread is 62% of mid.

## Where the panel and the searcher disagree most

- **YALA**: the searcher +1.90 (p89 of Opus 5.5 sizes), the panel long at only 16. The judges read the quarter as near-guide, with the Q4 guide likely below the street.
- **VIK**: the searcher +1.00, the panel short at 28. The judges weighted the worsening Rhine drought and the +19 put skew over the peer beats.
- **SHAZ**: the searcher -0.50, the panel short at 74 (Fable 94S, Sonnet 84S). The judges sized the Q3 billing shortfall and the disputed Q4 bar larger than the searcher did.
- **DIS / MNSO**: the searcher at 0.00, the panel short at 56 and 16, on the run-up into the print.
- **INFQ**: the judges split (sonnet55 short, three long), the widest spread of the day (sd 32).

## Comparison with stage E-P (same day, `edge-panel/edge-scores-panel.json`)

- **The universes differ.** Both stages ran their own sweep. Only **8 names were ranked by both** (API INFQ KLAR OMER OPRA POWL RCAT YALA). E-P's sweep hunted 12 small caps this stage did not hunt (AYTU DUOT ELTK FTLF GLAS IMDX NXB POCI STEM TMS WRAP XBP); this sweep confirmed 12 larger bmo names E-P did not (AS DIS ENR ESLT HUYA JD MNSO OCSL SHAZ TME VIK WB). A comparison on one day is therefore 8 names.
- **Selected:** v3b {ENR, OMER}; E-P {IMDX, KLAR, NXB, OMER, RCAT, STEM, TMS}. **Overlap: OMER.**
- **Spearman ρ of `panel_pct_signed` on the 8 common names: +0.83.**
- Side or selection disagreements on common names:
  - **INFQ**: v3b long 22, E-P short 46 (side).
  - **KLAR**: v3b short 44 (Opus 5.5 at 0), E-P short 81 and selected (selection).
  - **RCAT**: v3b short 76, E-P short 82 and selected (selection).
  - **POWL**: v3b short 70, E-P short 77; neither selected.
  - **API / YALA**: same side, v3b much weaker (20 / 16 against 46 / 43).
  - **ENR** is selected by v3b and was not hunted by E-P.

## Searcher table and standing notes

The searcher's `impact_sum` (ranked) is in `edge-scores.json`; `impact_scaled` is in `edge-scores-scaled.json`. V2 was written before the first print (`edge-scores-grounded.json`). OMER is the only name over the 2.8 floor.

- **Sign balance:** 7 of 20 hunts are positive, 11 negative and 2 zero. The panel leans short on 13 of 20.
- **Options:** the option chains that exist are mostly wide (OMER 72% of mid, ENR 62%, OPRA 104%). Several names have no usable chain, so their baseline lean is the run-up fallback.
- **Reaction histories:** many baseline histories for foreign private issuers were 6-K noise (`cadence_implausible` on RCAT INFQ KLAR AS MNSO TME VIK OPRA JD ESLT WB). The searchers rebuilt the reaction history from confirmed prints and said so in each hunt.
- **Nothing checked the findings:** there is no adversary pass and no second searcher.
- **Reproducibility:** the key is not reproducible to better than its own size (median gap 2.40 points between double hunts, 4 of 12 opposite signs, historically).
- **What the numbers are not:** `expected_return_pct` and `expected_edge_pct` are what names at that percentile have earned under stage E-P, with a weak out-of-sample record (correlation +0.12 over 148 names). They are not a forecast to size on. `p_up` is recorded and decides nothing. This stage places no orders.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
