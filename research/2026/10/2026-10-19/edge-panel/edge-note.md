# Stage E-P — 2026-10-19 amc + 2026-10-20 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.** All four
judges ran on their pinned models (Opus 5 `claude-opus-5`, Opus 5.5 `claude-opus-5-5`,
Sonnet 5.5 `claude-sonnet-5-5`, Fable 5.1 `claude-fable-5-1`), each covering 19 of 19 packs.
One day is an anecdote; judge this stage only pooled.

**Selected (mean percentile ≥ 80, all four present): EFX short (90) and VICR long (90).**
AERO is the near miss: panel_pct 79.9, so it falls under the mean rule. It IS selected
under the old 3-of-4 consensus rule (`selected_consensus: true`), which is still recorded.

## The panel table

Percentiles are each judge's own: the share of that judge's live sizes from runs before
today with a smaller |impact_sum| (n=76 each). `*` = in that judge's own top 20% (≥ 80).
`k` and `panel_score` are the legacy z-based consensus and score, still written.
E[return] is what names at that `panel_pct` have earned on the panel's side, gross, on the
scorebord window: one number per percentile, flat at about +0.3% below 50. It is the
translation of the percentile, not a separate forecast.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | EFX | bmo | **yes** | 90 | short | 4 | 93S* | 92S* | 84S* | 92S* | 4 | -2.05 | -2.80 | +4.16% [+2.08, +6.09] | 0.69 | 1.00 | 1.13 |
| 2 | VICR | bmo | **yes** | 90 | long | 5 | 95L* | 93L* | 91L* | 83L* | 4 | +2.01 | +2.10 | +4.16% [+2.08, +6.09] | 0.69 | 1.00 | 0.87 |
| 3 | AERO | amc |  | 80 | short | 9 | 68S | 87S* | 90S* | 75S | 3 | -1.22 | -1.30 | +2.60% [+0.62, +4.53] | 0.60 | 0.00 | 0.00 |
| 4 | HAS | bmo |  | 75 | short | 13 | 82S* | 82S* | 53S | 84S* | 2 | -1.30 | -0.80 | +2.01% [+0.37, +3.83] | 0.57 | 0.00 | 0.00 |
| 5 | NOC | bmo |  | 63 | short | 15 | 68S | 71S | 37S | 75S | 1 | -0.99 | -0.90 | +1.02% [-0.03, +2.56] | 0.56 | 0.00 | 0.00 |
| 6 | SFBS | amc |  | 52 | long | 6 | 60L | 54L | 50L | 43L | 0 | +0.58 | +0.80 | +0.33% [-0.37, +1.62] | 0.56 | 0.00 | 0.00 |
| 7 | GE | bmo |  | 43 | long | 22 | 13L | 43L | 40L | 75L | 1 | +0.44 | +0.40 | +0.29% [-0.50, +1.02] | 0.56 | 0.00 | 0.00 |
| 8 | MMM | bmo |  | 42 | long | 22 | 12L | 64L | 30L | 62L | 0 | +0.55 | +0.00 | +0.29% [-0.50, +1.00] | 0.56 | 0.00 | 0.00 |
| 9 | HAL | bmo |  | 42 | long | 9 | 46L | 53L | 40L | 29L | 0 | +0.52 | +0.40 | +0.29% [-0.50, +0.99] | 0.56 | 0.00 | 0.00 |
| 10 | KARO | amc |  | 28 | long | 34 | 22S | 21L | 70L | 45L | 0 | +0.38 | +1.30 | +0.29% [-0.56, +0.85] | 0.56 | 0.00 | 0.00 |
| 11 | ZION | amc |  | 27 | long | 18 | 41L | 49L | 9L | 10L | 0 | +0.35 | +0.55 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 12 | WASH | amc |  | 22 | short | 21 | 14L | 34S | 40S | 28S | 0 | -0.33 | -0.70 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 13 | AGNC | amc |  | 21 | short | 23 | 16L | 34S | 24S | 43S | 0 | -0.28 | -0.90 | +0.29% [-0.59, +0.83] | 0.56 | 0.00 | 0.00 |
| 14 | MSCI | bmo |  | 19 | long | 23 | 13S | 43L | 40L | 8L | 0 | +0.30 | +0.00 | +0.29% [-0.60, +0.82] | 0.56 | 0.00 | 0.00 |
| 15 | GM | bmo |  | 17 | long | 43 | 14S | 40L | 76L | 32S | 1 | +0.05 | -0.10 | +0.29% [-0.63, +0.82] | 0.56 | 0.00 | 0.00 |
| 16 | WAL | amc |  | 11 | short | 30 | 38L | 42S | 17S | 22S | 0 | -0.29 | -0.00 | +0.29% [-0.68, +0.80] | 0.56 | 0.00 | 0.00 |
| 17 | GPC | bmo |  | 7 | long | 39 | 57S | 46L | 30L | 7L | 0 | +0.27 | +0.10 | +0.29% [-0.71, +0.79] | 0.56 | 0.00 | 0.00 |
| 18 | ALLY | bmo |  | 5 | short | 18 | 16L | 13S | 30S | 7L | 0 | +0.03 | -0.25 | +0.29% [-0.72, +0.78] | 0.56 | 0.00 | 0.00 |
| 19 | VMI | bmo |  | 5 | short | 28 | 41S | 14L | 30L | 22S | 0 | -0.09 | -0.20 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |

Not hunted (budget, 19 hunted names; shed by lowest `hunt_priority`): SYF, RLI, RTX, HBCP,
RBB, CCK, PEBO, WRB, SMBK, KEY, AUB, WTFC, STLD, MBWM, BOKF, UCB, FNB, CCBG. CBSH was not
confirmed by the sweep. All sit in `edge-scores.json` as `rankable: false`.

## The selected names

**EFX short (panel_pct 90, all four judges at 84–93 short; searcher −2.80, the only name
over the 2.8 floor).** The judges all cite the same thing. The July full-year guide embeds
roughly 6.6% mortgage rates against about 7.4% now. MBA refi applications were −56% year
on year in late September, yet full-year consensus ($8.53, a single and possibly stale
MarketBeat source) still sits at the guide midpoint. The stock also comes in on an +8.4%
five-session bounce caused by an FHFA non-announcement on bi-merge, not by the company, and
this name has sold its guide cuts. **The case against:** the mortgage-rate evidence is public
macro data that the Street has had for weeks; six target cuts in October and a +2.58 put
skew show downside is already paid for; government verification guidance and four straight
EPS beats can carry the call. The bar the whole case rests on has one source.

**VICR long (panel_pct 90, judges 83–95 long; searcher +2.10).** Licensing has run far
ahead of the company's own "not until 2027" line: four licensees, two September guide
raises, and USITC 337-TA-1526 instituted on 2026-10-09 against nine respondents. The stock
fell 36% from about $308 to $197.70 in a chip-sector rout with no company-specific negative
found, which puts it below its pre-first-license level, and the skew is call-bid. Royalty
revenue at close to 100% margin makes an EPS beat on pre-announced revenue likely. **The
case against**, which every judge files as the largest single item: the Q3 royalty jump (~$28m+
against a guided $5m) may be catch-up, the company's full-year floor implies a Q4 revenue
step down, and Q4 EPS consensus is flat with Q3. A normalising Q4 guide is exactly what sold
the last print (−7% on a large beat). The baseline's event-implied move computes to 0
because 20-day realised volatility (109%) exceeds the straddle IV, so the scale comes from a
16.6% median reaction.

## Where the panel and the searcher disagree most

- **MMM**: searcher +0.00 (findings net to zero), panel 42 long. Opus 5.5 and Fable put it
  in their 60s, Opus 5 at 12.
- **KARO**: searcher +1.30 (p72 of Opus 5.5's own scale), panel 28 long, with Opus 5
  on the other side (22S). Biggest searcher-to-panel drop of the day.
- **GPC**: searcher +0.10, panel 7. Opus 5 leans short (57S) on the fuel-cost finding while
  Fable is at 7L; sd 39.
- **GM**: the widest spread (sd 43), Sonnet 76L against Opus 5 14S and Fable 32S.
- **HAS**: searcher −0.80, panel 75 short. Three judges ≥ 82; Sonnet at 53 kept it out.

## Against stage E

**Stage E's `edge-scores.json` does not exist for this date.** There is no
`research/2026/10/2026-10-19/edge/` on `origin/main` as of this note (about 18:20 UTC), so
there is no overlap or Spearman ρ to report. This session cannot see stage E's Routine (it
lives on another account, per CLAUDE.md), so whether it fired late, failed or published
elsewhere is not established from here.

## What the numbers are not

- `expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have
  earned, with a weak out-of-sample record (correlation +0.12 with the realised return over
  148 names). It is not a forecast to size on. The weights are research; nothing trades them.
- `p_up` is recorded and decides nothing; it did not predict on the development names.
- Below the floor the searcher's sign is a coin flip on the pooled evidence (53% over 38
  events). Only EFX clears 2.8 today.
- `impact_sum` is not a forecast of the move; it ranks and double-counts findings that share
  a source.
- Nothing checked the findings: there is no adversary pass and one searcher per name. A
  wrong finding enters at full size.
- The key is not reproducible to better than its own size: when the stage double-hunted,
  twelve pairs had a median gap of 2.40 points and four had opposite signs.
- Sign balance of the searchers: 7 positive, 9 negative, 3 at zero (MMM, MSCI, WAL).
- Option anchor: 15 of the 19 hunted names carry a usable chain (AERO, AGNC, ALLY, EFX, GE,
  GM, GPC, HAL, HAS, MMM, MSCI, NOC, VMI, WAL, ZION). VICR's chain gave an event move of 0, and
  KARO, SFBS and WASH have none, so their lean falls back to the 20-day run-up.
- WAL and ZION report the same evening and share a 2025 fraud borrower; Opus 5 flagged them
  as closer to one bet than two.
- Capacity: VICR and EFX both clear the turnover floor comfortably; no `assets` call was run,
  because this stage runs no `alpaca_trade.py` command of any kind.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on these. EFX: retail 41, search 0.65x
(quiet), vol 38. VICR: retail 57 (≥50), search 1.05x, vol 109 (≥58). Every other name is in
the score_report table in the run log reply; only VICR and AGNC have retail ≥ 50, and only
VICR has vol ≥ 58.

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
