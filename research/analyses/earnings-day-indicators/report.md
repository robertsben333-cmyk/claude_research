# Earnings-day technical indicators: do they add to the E-P panel?

2026-11-15. Pre-registered in `PREREG.md` (move test, then an addendum for entry and exit legs, both written
before any indicator was joined to an outcome). us-panel.v3 primary (218 names, 11 run days, 29 Oct to 12 Nov),
us-panel.v2 as direction check (186 names, 11 days), never pooled; 13 Nov run left out. Market-wide check on
every E-P baseline name in the same days (about 2,040 priced names in the v3 period, 870 in v2).
Window: entry 13:30 ET on the run day; amc out at the next open, bmo out at 13:00 ET. Gross.
Statistic: Spearman ρ on within-day ranks, p from 5,000 within-day shuffles; Holm over the 12 tests per leg.

## Answer first

**No technical indicator adds to the panel on the pre-registered rule, for the move, the entry or either exit.**
None of 60 indicator-by-leg tests on v3 survives Holm (the best adjusted p is 0.18). The equal-weight
composite of all eleven does nothing either (ρ −0.06 v3, −0.08 v2).

One lead, and it points the opposite way from the practitioner claim: **when the stock has already moved our
way on the run day and sits above (for a long) its intraday VWAP at 13:30, the trade does worse.**

| Price vs run-day VWAP, on our side, within-day terciles | v3 | v2 |
| --- | --- | --- |
| Low (moved against us before entry) | +2.99 (n 77) | +0.30 (n 66) |
| Middle | +1.99 (n 75) | −0.63 (n 62) |
| High (moved our way before entry) | −1.07 (n 66) | −2.25 (n 58) |
| High minus low | −4.06, t −2.03 | −2.56, t −1.78 |
| ρ, permutation p | −0.14, p 0.047 (Holm 0.52) | −0.08, p 0.28 |
| Controlling for panel_pct (day-clustered) | t −2.86 | t −1.13 |

Run-day return to entry (the same idea measured from the prior close) leans the same way: ρ −0.10 v3, −0.13 v2.
Market-wide the VWAP effect is −0.04 (p 0.10) in the v3 period and +0.03 in v2, so it is not a general market
pattern; it is a property of the names the panel picks, or noise. Among pct ≥ 60 names the tercile gap is
−5.1 (v3, n 79) and −8.3 (v2, n 72). That is a lead to log forward, not a rule.

## The move (panel side)

ρ is for the indicator signed by its literature hypothesis and the panel's side, so positive means "worked as claimed".

| # | Indicator | Claim | v3 ρ (p) | v2 ρ (p) | Market v3 / v2 | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | 5-day run-up | reversal | −0.09 (0.19) | −0.17 (0.03) | −0.01 / −0.04 | nothing (if anything continuation) |
| D2 | 20-day run-up | reversal | −0.05 (0.50) | −0.07 (0.35) | −0.02 / −0.01 | nothing |
| D3 | RSI(14) | overbought falls | −0.10 (0.13) | −0.13 (0.09) | −0.02 / +0.01 | nothing |
| D4 | Close vs 50-day SMA | trend | +0.07 (0.31) | +0.04 (0.63) | +0.02 / −0.01 | nothing |
| D5 | Previous earnings reaction | PEAD / persistence | +0.12 (0.10) | +0.07 (0.39) | +0.02 / +0.03 | nothing, misses the lead bar by 0.003 |
| D6 | 25-delta skew | steep skew falls | −0.01 (0.89) | −0.05 (0.62) | +0.03 / −0.01 | nothing (n 119 / 110) |
| D7 | Put/call open interest | puts fall | −0.02 (0.77) | −0.05 (0.56) | −0.01 / +0.03 | nothing |
| D8 | Run-day return to 13:30 | continuation | −0.10 (0.17) | −0.13 (0.09) | −0.04 / +0.01 | nothing (fade side) |
| D9 | Price vs run-day VWAP | continuation | **−0.14 (0.047)** | −0.08 (0.28) | −0.04 / +0.03 | **lead, reversed sign** |
| D10 | Abnormal volume, 5d vs 60d | EA premium | −0.03 (0.64) | −0.08 (0.31) | **+0.08 (0.001)** / +0.03 | nothing on the panel |
| D11 | Short interest, days to cover | shorts right | −0.05 (0.56) | −0.17 (0.16) | −0.01 / −0.07 | nothing (n 144 / 85, Nasdaq coverage) |
| S1 | Implied / historical move | rich options hurt us | −0.21 (0.015) | +0.14 (0.15) | n/a | nothing: flips between versions |
| C | Composite of D1..D11 | | −0.06 (0.36) | −0.08 (0.29) | −0.00 / +0.01 | nothing |

Notes. "IV crush" (S1) flips sign exactly as the sealed expected move did in the selection-score thread: in v3
the panel did well on names whose options were rich versus their history (+5.3 in the top tercile), in v2 badly
(−2.1). D5 (last quarter's reaction, on our side) points the same way in all four samples and is the only
literature indicator with that consistency; top minus bottom tercile +3.4 (t 1.7) v3, +1.4 (t 1.0) v2.

## Entry and exit legs (Xavier's follow-up)

| Leg | What positive means | Any v3 test with p < 0.10? | Verdict |
| --- | --- | --- | --- |
| Entry, 13:30 to run-day close | 13:30 beat a closing entry | none (best D11 p 0.15) | nothing; entry timing is not predictable from these |
| amc, next open to close | holding past the open paid | D4 SMA50 +0.16 (p 0.07), but v2 −0.15 | nothing |
| bmo, open to 13:00 | holding from the open paid | none (n 76) | nothing |
| bmo, 13:00 to close | holding past 13:00 paid | none (n 76) | nothing |

The exit legs on panel names are small (76 bmo, 138 amc in v3) and every v3 sign that looks interesting flips in v2.

## Market-wide patterns that replicate in both periods (not about the panel)

These are raw stock moves on all baseline names, unsigned by any call. Effect sizes are top minus bottom tercile.

| Pattern | v3 period | v2 period |
| --- | --- | --- |
| bmo names that ran up 5 days keep rising from the report-day open to 13:00 | +1.42, t 1.95 (n 821) | +1.35, t 2.43 (n 449) |
| amc names with heavy pre-print volume rise from the next open to the close | +0.58, t 0.92 (n 1,244) | +1.88, t 2.68 (n 419) |
| Heavy pre-print volume, whole window (earnings-announcement premium) | +1.42, t 2.41 (n 2,034) | +0.52, t 0.95 (n 864) |

They are about the market, not about the panel: none of them shows up when signed to the panel's side.
They could matter as a direction-free exit tilt (a long in a run-up bmo name holds to 13:00 anyway; a short
might cover at the open), but that is a separate question and these are 22 days.

## What this means

- Keep the selection, entry and exits as they are. Nothing here earns a live change.
- Worth logging forward, at no cost: price vs run-day VWAP at 13:30 on the panel's side, and the previous
  earnings reaction on the panel's side. Both come free from data E-P already has or can compute at step 6b.
  Settle them on about 20 more v3 run days before using them; the VWAP effect would then need to hold
  on pct ≥ 80 names, where n is about 20 today.
- The options indicators (skew, put/call, IV richness) add nothing in either direction, and IV richness repeats
  the em flip. Short interest is thinly covered (Nasdaq's feed only had 144 of 218 v3 names).

## Caveats

- 22 run days in total; a day effect can carry a whole tercile. The permutation test shuffles within day, so day
  level moves are out of every ρ, but there are still only 11 independent days per version.
- Gross of costs; the VWAP lead is not tradable as such, it would be a filter.
- My recomputed raw moves match the scorebord's on 404 of 404 panel names (median gap 0.19 pts; 22 over 1 pt).
- Short interest uses the latest settlement published by the run day (settlement + 11 calendar days).

## Files

`PREREG.md`, `results.txt` (every test), `results.json`, `explore.txt` (terciles, exploratory),
`features.json`, `scripts/` (events, fetch, si, build, analyse, explore). Alpaca SIP bars; Nasdaq short interest;
skew, put/call and implied move from the sealed E-P baselines.
