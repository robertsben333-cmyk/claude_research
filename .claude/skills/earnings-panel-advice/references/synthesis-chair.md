# Synthesis chair — aggregation rules

Read this when reviewing the output of `scripts/synthesize.py`.

You are the chair. You consume **only** the seven compact verdicts and the Phase-0
anchors. You do not go back to the personas' research, and you do not introduce facts
that are not in the verdicts or the anchors. New evidence at this stage is how a panel
result quietly becomes one analyst's opinion.

Be prediction-forward but not promotional. Identify the best-supported directional
forecast as soon as the aggregated evidence allows one. A weak but coherent lean should
stay a **Low-certainty prediction**, not collapse to Neutral. A system that answers
"no edge" every day is never wrong and never useful.

## What the script computes

| Quantity | Rule |
| --- | --- |
| `consensus_score` | Plain mean of the seven `direction_score` values |
| `confidence_weighted_score` | Diagnostic only: mean weighted High 1.0 / Med 0.7 / Low 0.4 |
| `call` | Band mapping: Strong Up +60…+100 · Lean Up +25…+59 · Neutral −24…+24 · Lean Down −25…−59 · Strong Down −60…−100 |
| `disparity` | `min(100, 2 × stdev(scores))` |
| `panel_alignment` | aligned < 30 · mixed < 60 · split ≥ 60 |
| `prob_up` | Mean `prob_up`, shrunk toward 50 by `1 − disparity/200`, further for missing anchors |
| `consensus_reversal_risk` | Mean reversal risk, red team weighted 1.5× when its case is specific |
| `unsigned_expected_move` | `0.60 × implied + 0.40 × historical`, or whichever anchor exists |
| `move_band_low_high` | Unsigned magnitude band, `0.5×` to `1.6×` expected move, widened for a high historical max or a binary catalyst |
| `signed_estimated_move` | `expected_move × conviction_multiplier × sign(consensus)` |
| `certainty_tier` | 100 − 0.7×disparity − anchor and confidence penalties; High ≥ 70, Med ≥ 45 |

### The conviction multiplier

Direction and magnitude are separate questions. The multiplier is:

- Lean (|score| 25–59): 0.30 → 0.50
- Strong (|score| ≥ 60): 0.50 → 0.80
- Then scaled by certainty: High ×1.0, Med ×0.85, Low ×0.70, capped at 0.80

**The full implied move is never the point estimate.** The implied move is roughly a
one-standard-deviation expectation — a reference distribution, not a target and not a
bound. Claiming it as a directional forecast overstates what the panel knows.

### The conviction gate

The script forces `Neutral / No Edge` only when a directional call would actively
mislead:

- earnings timing not confirmed
- no usable move anchor from either implied or historical data
- disparity > 70 with |consensus| < 35 — a genuinely split panel with no centre
- red-team reversal risk ≥ 75 with |consensus| < 40 — the reversal case breaks a thesis
  the panel only weakly holds

Everything short of that lowers certainty instead of erasing the forecast. When the
gate fires, `signed_estimated_move` is `null` and only the unsigned band is reported.

## What you review

Read the packet and check:

- **Does the call match the panel's actual shape?** A consensus of +26 with three
  personas at −40 is technically Lean Up and substantively a split panel. The disparity
  number should already be catching this; confirm that it did.
- **Is the red-team case specific and sourced, or just pessimistic?** The 1.5× weight is
  earned by evidence. If the reversal case is a story with no citation, note it in
  `red_team_survival_note` and consider overriding certainty down rather than up.
- **Do any two personas cite the same single source for the same claim?** Then the panel
  is less independent than its spread suggests. Say so, and lower certainty.
- **Are missing anchors reflected?** A name with no implied move should not come out
  High certainty.

Then write, into the synthesis object:

- `early_prediction` — one sentence: likely direction, main driver, strongest caveat.
  This sharpens the dossier's `Prediction first` line.
- `red_team_survival_note` — did the thesis survive the strongest opposite case, and how
  comfortably?

## Overriding

You may override `call`, `certainty_tier`, or `signed_estimated_move`. Every override
requires `chair_override_note` naming what the formula missed.

Legitimate reasons to override:

- Two or more personas are leaning on the same single source, so the apparent agreement
  is one data point counted several times.
- A verdict's `direction_score` plainly contradicts its own `key_drivers`.
- An anchor in the packet is stale enough to be misleading (a spot price from last week).

Not legitimate:

- The number feels too strong or too weak.
- The call disagrees with the stage 2 dossier's preliminary read. It is supposed to be
  able to — that is why the panel exists.
- You want a cleaner headline.

If you override on most days, the formula is miscalibrated. Fix
`scripts/synthesize.py`, where the change is versioned and visible to every future run,
rather than re-deciding it in prose each morning.

## Quality bar

- No new facts beyond the seven verdicts and the Phase-0 anchors.
- Never hide a split panel behind an assertive headline — report the disparity.
- Reversal risk stays separate from direction throughout.
- Prefer a clearly labelled Low-certainty prediction over a vague Neutral when the
  evidence supports a lean but not confidence.
