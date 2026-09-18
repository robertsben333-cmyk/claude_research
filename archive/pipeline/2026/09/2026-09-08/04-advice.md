# Daily earnings advice — 2026-09-08

**Window:** After the US close on Tuesday 2026-09-08 through before the US open on
Wednesday 2026-09-09. **Researched:** 6 names (TTAN, CHWY, SAIL, BRZE, SIG, ASO), all
panel-eligible. **Panelled:** 2 (TTAN, CHWY) — `panel.names=2` per `config/pipeline.yaml`,
already reduced from 3 to 2 on 2026-08-13 per the config's own history; no further
degradation was applied at this stage.

## The calls

### TTAN — ServiceTitan, Inc. — reports tonight, AMC (2026-09-08)

**Call: Neutral / No Edge** · Unsigned band **5.8% – 18.4%** (event-implied ≈ ±13.14%,
refreshed today) · P(up) 55.5% · Certainty **High** (that there is no strong edge, not
that direction is known) · Reversal risk 56/100 (Med)

All seven personas leaned mildly bullish (consensus +15, every individual score positive,
range +8 to +20) on a beat-and-raise setup — but too weakly and too uniformly to clear the
+25 Lean-Up threshold. **Reason:** the beat itself looks near-mechanical (6 for 6 on
non-GAAP EPS since IPO), but this market has repeatedly sold TTAN's good quarters on
software-multiple-compression regime risk. **Caveat:** the red team's unrefuted arithmetic
— the current FY27 guide midpoint implies H2 revenue growth decelerating to ~15% y/y versus
the 25% just printed — is the main reason certainty on magnitude stays capped even though
certainty that there's no strong directional edge is high.
→ [Full dossier](03-panel/TTAN-dossier.md)

### CHWY — Chewy, Inc. — reports tomorrow, BMO (2026-09-09)

**Call: Neutral / No Edge** · Unsigned band **4.7% – 17.4%** (event-implied ≈ ±10.65%,
reconfirmed today) · P(down) 52.2% · Certainty **High** · Reversal risk 59/100 (Med)

The panel is genuinely split (consensus -8, range -25 to +12, five of seven lean down but
none reach Lean-Down strength). **Reason:** this is a live guidance binary — June's sales-
guide cut already reset the bar once, and whether it needs a second trim is the question
every persona converged on independently, with two personas (macro/peer read-through,
forensics) reading the same reset-bar evidence as bullish rather than bearish. **Caveat:**
two-sided reversal risk — a rebuilt-but-loose short base could squeeze on a clean print,
while a large Class B sponsor overhang could sell into any relief rally.
→ [Full dossier](03-panel/CHWY-dossier.md)

## Ranked field

All 6 names cleared the deep-dive exclusion floors (event confirmed, evidence ≥50, a usable
implied-move anchor) and were panel-eligible; only the top 2 by `panel_priority` received a
persona panel.

| Rank | Ticker | Company | Session | Implied move | Prelim. direction (stage 2) | Evidence completeness | Panelled | Panel call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TTAN | ServiceTitan, Inc. | AMC 09-08 | 13.0% (13.14% refreshed) | +25 | 84 | Yes | Neutral / No Edge |
| 2 | CHWY | Chewy, Inc. | BMO 09-09 | 10.65% | +16 | 84 | Yes | Neutral / No Edge |
| 3 | SAIL | SailPoint, Inc. | — | 16.05% | -18 | 84 | No | — |
| 4 | BRZE | Braze, Inc. | — | 14.0% | -15 | 80 | No | — |
| 5 | SIG | Signet Jewelers Limited | — | 10.0% | +18 | 80 | No | — |
| 6 | ASO | Academy Sports and Outdoors, Inc. | — | 7.5% | -12 | 82 | No | — |

Stage 2's `preliminary_direction_score` is the deep-dive researcher's own single-analyst
read, unseen by the panel — it is shown here only to make clear how the independent panel's
verdict compares to the researcher who built the dossier. For TTAN, the panel's consensus
(+15) landed close to stage 2's own preliminary read (+25) but fell short of the same
Lean-Up threshold. For CHWY, the panel (-8) diverged more from stage 2's read (+16),
reflecting the panel surfacing a genuine split that the single-analyst dossier had not.
SAIL, BRZE, SIG and ASO were not panelled this run; their stage 2 dossiers and preliminary
reads stand as the day's only forecast for those names — see `02-dossiers/<TICKER>.md`.

## What would change these calls

- **TTAN:** the size of tonight's FY27 revenue-guidance raise. A raise clearing roughly
  $1.15bn with subscription growth held at or above 24% points the stock at the call-heavy
  open interest 14–25% above spot. A token raise, or any further step-down in the operating-
  margin guide, reproduces the setup behind both of TTAN's negative prints this year.
- **CHWY:** whether the FY26 sales guide ($13.40–13.55bn) is reaffirmed or cut a second
  time. A reaffirm-or-raise with active adds ≥21.7m turns the "bar already reset" bull case
  into a clean re-rating against a discretionary, cheap-to-borrow short base. A second cut,
  or a Q2 print at the low end of the guided range, repeats Chewy's own "beat-then-cut"
  pattern that has produced two of its last six double-digit moves.
- **Both:** neither call rests on a specific catalyst outside the print itself, but TTAN's
  straddle also spans next week's CPI (2026-09-11) and FOMC (2026-09-15/16), so some of its
  13.1% implied move is macro rather than earnings-specific.

## Coverage and caveats

- Both panels ran the full seven seats with no missing personas and no chair overrides.
- TTAN's panel was unusually tight (disparity 8.7/100, "aligned") — all seven personas
  agreed on sign but none individually cleared Lean-Up strength, which is why the call reads
  Neutral / No Edge despite a real, if weak, bullish tilt. This is the plain call-band
  outcome for a genuinely weak-but-coherent lean, not a forced conviction-gate override
  (`conviction_gate_applied: false` on both names).
- CHWY's panel was the more genuinely split of the two (disparity 28.2/100, two personas
  positive against five negative) — a coin-flip-close P(direction) of 52.2%.
- Both tickers' price-sensitive anchors (spot, implied move) were refreshed same-day, within
  ~4 hours of TTAN's print and the day before CHWY's; stage 2's dossiers, built hours to a
  day earlier, carried the stale figures noted in each panel file's `refresh_note`.
- SAIL, BRZE, SIG and ASO were shed from the panel purely by rank under `panel.names=2` —
  not for any evidence or eligibility problem; each is fully researched at evidence
  completeness 80–84 in its own stage 2 dossier.
- No budget degradation was needed at this stage beyond the config's existing `panel.names=2`
  setting; stage 2 completed both its batches in full per `_run-log.md`, so there was no
  upstream scope-shedding to inherit.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
