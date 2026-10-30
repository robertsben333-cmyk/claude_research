# Stage E-P — 2026-10-30 amc + 2026-11-02 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** Since 2026-10-19 it is the only stage trading the Alpaca paper account (step 6b, after this note is published).
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), natively, 20 of 20 names each, one part, no fallback.
One day is an anecdote.

Universe: 25 calendar rows, all 2026-11-02 bmo (Monday; no Friday amc row cleared the gates). FOX folded into FOXA by hand (`share_class.py` did not fold the pair). 24 baselines sealed before any agent. The sweep confirmed 19 (15 with a company-sourced bmo session; NSSC, TSEM, L, PEG date-confirmed with the hour left to the searcher), left 4 unconfirmed (CIFR, RYAAY, III, ALX) and killed 1 phantom (XFLT, a closed-end fund). Searched: the 19 confirmed plus CIFR (highest-priority unconfirmed); every searcher confirmed its event and all four unsettled sessions came back bmo. Shed: RYAAY, III, ALX (unconfirmed, lower priority). **No searcher hit a search budget** (`hunt_status.py check`: 0 unfinished of 20). **No name clears the searcher's 2.8 floor** (largest: CIFR +2.10, CHH +2.00).

## Panel table

`panel_pct` is the mean of the judges' own percentiles, 0-100, with the side in its own column. A member cell is that judge's percentile against its own live range: L/S gives its side, `*` marks a name in that judge's own top 20%. `E[return]` is what names at this percentile have earned on the panel's side: one number per percentile, gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile; it is not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TSEM | bmo | yes | 85 | long | 6 | 79L | 96L* | 82L* | 86L* | 3 | +1.30 | +1.40 | +3.40% [+1.29, +5.41] | 0.65 | 1.0 | 1.00 |
| 2 | CHH | bmo |  | 77 | long | 6 | 70L | 72L | 86L* | 80L* | 2 | +1.07 | +2.00 | +2.26% [+0.48, +4.13] | 0.58 | 0.0 | 0.00 |
| 3 | KRYS | bmo |  | 62 | short | 12 | 70S | 63S | 42S | 74S | 0 | -0.81 | -0.80 | +0.98% [-0.05, +2.50] | 0.56 | 0.0 | 0.00 |
| 4 | NSSC | bmo |  | 54 | short | 26 | 73S | 58S | 10S | 74S | 0 | -0.81 | +0.10 | +0.36% [-0.31, +1.79] | 0.56 | 0.0 | 0.00 |
| 5 | CHKP | bmo |  | 48 | short | 22 | 65S | 64S | 10S | 52S | 0 | -0.72 | -0.60 | +0.29% [-0.45, +1.31] | 0.56 | 0.0 | 0.00 |
| 6 | TEM | bmo |  | 44 | short | 20 | 74S | 37S | 20S | 45S | 0 | -0.47 | -0.50 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.00 |
| 7 | MAR | bmo |  | 43 | short | 18 | 73S | 35S | 29S | 34S | 0 | -0.42 | -1.20 | +0.29% [-0.50, +1.03] | 0.56 | 0.0 | 0.00 |
| 8 | CIFR | bmo |  | 40 | long | 50 | 38S | 84L* | 82L* | 34L | 2 | +0.82 | +2.10 | +0.29% [-0.51, +0.94] | 0.56 | 0.0 | 0.00 |
| 9 | FOXA | bmo |  | 38 | long | 25 | 40L | 64L | 4S | 50L | 0 | +0.54 | -0.00 | +0.29% [-0.53, +0.90] | 0.56 | 0.0 | 0.00 |
| 10 | TATT | bmo |  | 36 | short | 6 | 44S | 37S | 28S | 33S | 0 | -0.42 | +0.10 | +0.29% [-0.54, +0.88] | 0.56 | 0.0 | 0.00 |
| 11 | IDXX | bmo |  | 35 | short | 9 | 46S | 42S | 29S | 23S | 0 | -0.40 | -0.70 | +0.29% [-0.55, +0.87] | 0.56 | 0.0 | 0.00 |
| 12 | AXSM | bmo |  | 33 | long | 16 | 12L | 37L | 28L | 56L | 0 | +0.35 | +0.40 | +0.29% [-0.55, +0.86] | 0.56 | 0.0 | 0.00 |
| 13 | AKR | bmo |  | 32 | long | 9 | 28L | 26L | 48L | 26L | 0 | +0.36 | +1.40 | +0.29% [-0.56, +0.86] | 0.56 | 0.0 | 0.00 |
| 14 | CNA | bmo |  | 31 | long | 13 | 38L | 37L | 39L | 9L | 0 | +0.39 | +0.70 | +0.29% [-0.56, +0.85] | 0.56 | 0.0 | 0.00 |
| 15 | ETR | bmo |  | 27 | long | 11 | 40L | 32L | 10L | 26L | 0 | +0.36 | +0.30 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.00 |
| 16 | KOS | bmo |  | 26 | short | 12 | 44S | 14S | 28S | 16S | 0 | -0.28 | -0.50 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.00 |
| 17 | EL | bmo |  | 25 | long | 5 | 24L | 29L | 29L | 16L | 0 | +0.32 | +0.60 | +0.29% [-0.57, +0.84] | 0.56 | 0.0 | 0.00 |
| 18 | LTBR | bmo |  | 15 | long | 9 | 8L | 17L | 29L | 6L | 0 | +0.18 | +1.10 | +0.29% [-0.65, +0.81] | 0.56 | 0.0 | 0.00 |
| 19 | L | bmo |  | 4 | long | 4 | 4L | 10L | 0- | 1L | 0 | +0.07 | -0.25 | +0.29% [-0.74, +0.78] | 0.56 | 0.0 | 0.00 |
| 20 | PEG | bmo |  | 3 | long | 5 | 10L | 2L | 4S | 4L | 0 | +0.07 | -0.15 | +0.29% [-0.74, +0.78] | 0.56 | 0.0 | 0.00 |

**Selected (panel_pct >= 80, all four judges present): TSEM long (85).** The old 3-of-4 rule selects the same one name. Next: CHH 77 (2 of 4 in own top), KRYS 62 short, NSSC 54 short. A one-name book.

## The selected name

- **TSEM (long, 85; Opus 5.5, Sonnet 5.5 and Fable 5.1 in their own top 20%, Opus 5 at 79; sd 6).** The judges' notes all rest on the Q4 guide: the company's own statements (a >$1B annualised silicon-photonics run rate in Q4, wafer-start capacity ~3x Q2 by year-end), customer advances up from $27.5M to $321M in H1, NewPhotonics volume shipments (6-K 09-17) and Semtech paying for dedicated SiGe capacity (6-K 10-13), against a Q4 bar (~$575-579M) the searcher found unmoved since August. AXT's record indium-phosphide quarter (10-29) eases a supply constraint Tower itself named. The stock fell 13.5% on 10-30 and 32% over 20 sessions in the chip rout after Intel's warning, with no Tower-specific news. Session settled bmo by the searcher from the last 6-K's EDGAR acceptance time (07:04 ET on a 10:00 ET call day) and a press preview; the company's date notice does not give the hour. *Against:* the 25-delta skew pays **+20.7 vol points for downside**, the most extreme in the universe, and every judge cited it as the reason its lean stops where it does; Intel's PC/memory warning hits the ~38% consumer-exposed base (RF mobile −35.5% y/y); Q3 EPS consensus is disputed ($0.98-1.07); and the reason offered for the option market being wrong — a skew struck on a sector-panic day — is the kind LESSONS rule 7 has charged for before.

## Where the panel and the searcher disagree most

- **CIFR:** searcher +2.10 (the day's largest) against panel_pct 40 with an sd of 50: Opus 5.5 and Sonnet 5.5 put it in their own top 20% long (84L, 82L), Opus 5 on the other side (38S), Fable 34L. A crowded short and a rent-start catalyst against Google-warrant dilution; the judges split on which dominates.
- **CHH:** searcher +2.00 against panel_pct 77; two of four in their own top 20%.
- **NSSC:** searcher +0.10 against panel_pct 54 short; Opus 5 and Fable 5.1 at 73-74S on lapped pricing and slowing recurring revenue, Sonnet 5.5 at 10S.
- **MAR and TEM:** searcher −1.20 and −0.50; Opus 5 at 73-74S, the other three at 20-37, so the panel lands at 43-44.

## Stage E comparison

Stage E's `<RUN>/edge/` does not exist: its Routine is stopped since 2026-10-19. No overlap and no Spearman ρ.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names) — not a forecast to size on. The weights are research. `p_up` is recorded and decides nothing. Nothing checked the findings for factual error (no adversary, one searcher per name), and the key is not reproducible to better than its own size (four of twelve double-hunted pairs once came back with opposite signs). Searcher sign balance: 11 positive, 1 zero (FOXA), 8 negative. Below the 2.8 floor the searcher's sign has been a coin flip, and no name clears it today. The free control `-run_up_20d_pct` is in `edge-scores.json`. Option chains: 14 of 24 sealed baselines carry an implied move (MAR ETR IDXX EL FOXA TSEM CHKP TEM KRYS AXSM CHH CIFR KOS NSSC); several of those are flagged by their searchers as indicative only (wide at-the-money spreads: AXSM, KOS, NSSC, CHH, ETR). Every name clears the $200k turnover floor; the thinnest hunted are LTBR ($3.5m/day) and TATT ($3.7m/day).

## Context: retail, search and volatility (not used for selection)

From `edge-context.json` (context only; nothing ranks, selects or sizes on it). TSEM: retail tilt 52.7 (≥50), search sparse, 20-day vol 89.8% annualised (≥58). The full per-name table is in the score_report output in the closing reply.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
