# Stage E-P — 2026-10-14 amc + 2026-10-15 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.** All four
members ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) and judged
16 of 16 packs; none reported a model id, so the pinned ids are recorded. **One day is an
anecdote.**

**Run note.** The Routine's own session stopped at a usage limit after 16 of 17
searchers. A second session resumed at 18:17 UTC, shed PNC (its searcher never finished,
so PNC is not ranked: no hunt), scored, ran the four judges and `panel_score.py`. Nothing
else was changed or re-run.

**Headline: the panel selects one name, CMTL short** (`panel_pct` 93, all four members in
their own top 20%, spread 3). The searcher's key puts no name over the 2.8 conviction
floor (largest |impact_sum| 1.40, PLD and SCHW).

## The panel table

Percentiles 0-100 of each judge's own live range (n=44 live sizes per judge, before
today); L = long, S = short, `*` = in that judge's own top 20%. Selection: `panel_pct`
≥ 80 with all four present. Expected return is gross, on the scorebord window, and is the
translation of the percentile: every name at the same `panel_pct` carries the same
number, flat at about +0.3% below a percentile of 50.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | P(right) | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CMTL | amc 10-14 | **yes** | 93 | short | 3 | 96S* | 89S* | 91S* | 96S* | 4 | -2.26 | -0.80 | +4.44% [+2.40, +6.28] | 0.70 | 1.0 | 1.0 |
| 2 | MAN | bmo | no | 72 | long | 7 | 61L | 75L | 70L | 80L | 1 | +0.85 | +1.05 | +1.70% [+0.27, +3.43] | 0.56 | 0 | 0 |
| 3 | PLD | bmo | no | 60 | long | 12 | 43L | 64L | 77L | 54L | 0 | +0.67 | +1.40 | +0.78% [-0.14, +2.25] | 0.56 | 0 | 0 |
| 4 | TSM | bmo | no | 50 | long | 17 | 30L | 64L | 70L | 39L | 0 | +0.60 | +0.20 | +0.30% [-0.41, +1.50] | 0.56 | 0 | 0 |
| 5 | ERIC | bmo | no | 46 | short | 30 | 66S | 36S | 0 | 80S | 0 | -0.60 | +0.20 | +0.29% [-0.48, +1.14] | 0.56 | 0 | 0 |
| 6 | EDUC | amc 10-14 | no | 44 | short | 22 | 16S | 41S | 77S | 43S | 0 | -0.49 | -0.70 | +0.29% [-0.49, +1.08] | 0.56 | 0 | 0 |
| 7 | SCHW | bmo | no | 42 | long | 12 | 23L | 57L | 43L | 43L | 0 | +0.53 | +1.40 | +0.29% [-0.51, +0.98] | 0.56 | 0 | 0 |
| 8 | CMC | bmo | no | 27 | long | 3 | 27L | 23L | 32L | 25L | 0 | +0.37 | +0.80 | +0.29% [-0.57, +0.84] | 0.56 | 0 | 0 |
| 9 | USB | bmo | no | 25 | short | 5 | 23S | 23S | 20S | 34S | 0 | -0.31 | -0.55 | +0.29% [-0.57, +0.84] | 0.56 | 0 | 0 |
| 10 | BNY | bmo | no | 24 | long | 23 | 16S | 41L | 32L | 39L | 0 | +0.40 | +0.50 | +0.29% [-0.58, +0.83] | 0.56 | 0 | 0 |
| 11 | MRSH | bmo | no | 24 | short | 14 | 36S | 7S | 14S | 39S | 0 | -0.34 | +0.30 | +0.29% [-0.58, +0.83] | 0.56 | 0 | 0 |
| 12 | WIT | bmo | no | 20 | short | 2 | 23S | 18S | 18S | 20S | 0 | -0.25 | +0.30 | +0.29% [-0.60, +0.82] | 0.56 | 0 | 0 |
| 13 | HOMB | amc 10-14 | no | 16 | long | 5 | 14L | 25L | 11L | 16L | 0 | +0.16 | -0.10 | +0.29% [-0.64, +0.81] | 0.56 | 0 | 0 |
| 14 | FHN | bmo | no | 15 | short | 14 | 14S | 7L | 32S | 20S | 0 | -0.21 | -0.80 | +0.29% [-0.65, +0.81] | 0.56 | 0 | 0 |
| 15 | EQBK | amc 10-14 | no | 14 | short | 1 | 14S | 16S | 14S | 14S | 0 | -0.17 | -0.25 | +0.29% [-0.66, +0.81] | 0.56 | 0 | 0 |
| 16 | BSVN | bmo | no | 12 | short | 2 | 16S | 14S | 11S | 9S | 0 | -0.16 | +0.10 | +0.29% [-0.67, +0.81] | 0.56 | 0 | 0 |

Not ranked: PNC (bmo 10-15), no hunt.

## Selected: CMTL, short (amc tonight)

All four judges name the same two items. First, the Q4 FY26 presentation: the Q3 10-Q
says the held-for-sale criteria were "not met as of April 30, 2026", the sale of
Satellite & Space to Gilat was signed on 14 June, so this print is likely to show it as
held for sale or discontinued, against a consensus still set on consolidated revenue
($109-114m), with an annual goodwill test on $204.6m of goodwill behind an equity stub
of about $38m. Second, Allerium's Q3 book-to-bill of 0.32x (0.91x a year earlier) with no
award release since. Opus 5 and Fable 5.1 sized it at -3.60, Sonnet 5.5 at -2.40, Opus 5.5
at -1.44. Opus 5 states the size comes from the name's own reaction scale (6 of 7 prints
down, median move 18%), not from a strong lean, and that holds for the other three too:
p_up sits at 40-47.

The strongest case against comes from the searcher's own file. Liquidity is better than
the price implies (revolver undrawn on 3 August, $10m voluntary prepayments on 31 July,
five positive operating cash flow quarters), Gilat calls the deal "progressing well", and
results come four weeks earlier than last year, which lowers the risk of a late 10-K or
going-concern language. The searcher itself sized the name at only -0.80 (p54 of its own
scale), `print_vs_bar_pct` -3.0 and `expected_move_pct` -1.08. There is no usable option
chain, so the 18% scale is history, not a priced expectation. The common sits behind
about $109m of debt and a $220.5m preferred liquidation preference, so a short of a $38m
residual is a short of a thin, retail-heavy name (retail tilt 80, 20-day vol 56%): the
expected return is an upper bound on what size could have got.

## Where the panel and the searcher disagree most

- **CMTL**: searcher -0.80, panel 93 short. The judges paid for the reaction scale; the
  searcher kept the liquidity offsets.
- **ERIC**: searcher +0.20, panel 46 short (spread 30). Fable 5.1 (80S, in its own top
  20%) and Opus 5 (66S) weighted the DRAM/NAND contract-price rise into the Q4 Networks
  margin guide; Sonnet 5.5 sat at zero.
- **MRSH**: searcher +0.30, panel 24 short; all four judges leaned the other way.
- **TSM**: searcher +0.20, panel 50 long. Sonnet 5.5 and Opus 5.5 read the Q3 revenue
  already above guide harder than the searcher did; Opus 5 cut it for the capex line.

## Against stage E

Stage E's `edge-scores.json` exists: 17 names, the same 16 ranked here plus PNC; none
over the floor and no order placed. On the 16 names both ranked: **Spearman ρ, stage E
`impact_sum` vs `panel_pct_signed`: +0.355**; stage E vs this searcher +0.541; this
searcher vs the panel +0.712. Largest disagreements with stage E: EDUC (E +0.80, panel 44
short), CMC (E -0.60, panel 27 long), and TSM (E -0.40, panel 50 long). Stage E sized CMTL
at -0.70.

## Control

`-run_up_20d_pct` ranks the day at ρ +0.02 against the panel and -0.06 against the
searcher's key, so neither order is the free control today. CMTL carries a -14.8% 20-day
run-up, which points the control the other way.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct` on CMTL, -4.44 as a signed move) is what
names at that percentile have earned, with a weak out-of-sample record (correlation +0.12
with the realised return over 148 names). It is not a forecast to size on. The weights
are research, nothing trades them. `p_up` is recorded and decides nothing. Below the
floor the searcher's sign is a coin flip on the evidence so far (53% over 38 events);
`impact_sum` ranks and does not size. Nothing checked the findings for factual error,
and the key has not been shown reproducible to better than its own size (twelve
double-hunted pairs, median gap 2.40 points, four opposite signs). 10 of the 16 ranked
names have a live option chain (BSVN, EDUC no market; CMTL, EQBK, WIT unusable; HOMB
empty).

## Searcher table and notes

Sign balance of the searcher's key: 10 positive, 6 negative. Flags per name are in
`edge-scores.json`. V2 grounded was written at 18:17 UTC, before the first print (20:00 UTC), on 186
ledger observations; it is in `edge-scores-grounded.json` (CMTL -1.96, the largest).
Universe: 17 of 40 calendar rows (4 amc 10-14, 13 bmo 10-15); the sweep confirmed 17 of
17.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on these. Retail ≥50: CMTL (80), EDUC (51).
Vol ≥58: none (CMTL 56%). Search quiet (<1.0x): ERIC, FHN. Search failed for TSM, BSVN,
HOMB, EQBK and PNC; sparse for MAN, CMC, BNY, USB, CMTL.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
