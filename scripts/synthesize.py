#!/usr/bin/env python3
"""
Turn seven persona verdicts plus Phase-0 anchors into a synthesis packet.

The arithmetic in the synthesis chair role — means, standard deviations, shrinkage,
band construction, the conviction gate — is mechanical and must be reproducible from
one day to the next. Doing it in code rather than in prose means a run can be re-derived
and audited later, and that a bad day cannot be explained away by different mental math.

The chair still has judgement: it may override `call`, `certainty_tier` or
`signed_estimated_move` afterwards, but every override must be written into
`chair_override_note` in the stored packet.

Input JSON:
{
  "ticker": "TTWO",
  "anchors": {
    "event_confirmed": true,
    "event_implied_move_pct": 9.2,
    "historical_move_mean_abs": 7.7,
    "historical_move_max_abs": 12.4,
    "historical_sample_size": 8,
    "binary_catalyst": false
  },
  "panel_verdicts": [ ... seven verdict objects ... ]
}

    python3 scripts/synthesize.py input.json            # prints the packet
    python3 scripts/synthesize.py input.json -o out.json
"""

import argparse
import json
import statistics
import sys

CONFIDENCE_WEIGHT = {"High": 1.0, "Med": 0.7, "Low": 0.4}
RED_TEAM = "Red-Team Skeptic"
RED_TEAM_REVERSAL_WEIGHT = 1.5

CALL_BANDS = [
    (60, 100, "Strong Up"),
    (25, 59.999, "Lean Up"),
    (-24.999, 24.999, "Neutral / No Edge"),
    (-59.999, -25, "Lean Down"),
    (-100, -60, "Strong Down"),
]


def call_for(score):
    for lo, hi, name in CALL_BANDS:
        if lo <= score <= hi:
            return name
    return "Neutral / No Edge"


def _mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def expected_move(anchors):
    """Blend implied and historical anchors into an unsigned expected move."""
    implied = anchors.get("event_implied_move_pct")
    hist = anchors.get("historical_move_mean_abs")
    if implied and hist:
        return 0.60 * implied + 0.40 * hist, "blended 0.6x implied + 0.4x historical"
    if implied:
        return float(implied), "implied only (no historical anchor)"
    if hist:
        return float(hist), "historical only (no implied anchor)"
    return None, "no usable move anchor"


def move_band(em, anchors):
    """
    Right-skewed magnitude band around the expected move, unsigned.

    Earnings reactions have a fat right tail: the downside of the *magnitude* is
    bounded by zero but the upside is not, so the band is deliberately asymmetric.
    """
    if em is None:
        return None
    lo = round(0.50 * em, 1)
    hi = 1.60 * em
    hist_max = anchors.get("historical_move_max_abs")
    if hist_max:
        hi = max(hi, 1.05 * hist_max)          # history has already exceeded the band
    if anchors.get("binary_catalyst"):
        hi *= 1.25                              # binary events break the distribution
    return [lo, round(hi, 1)]


def certainty(disparity, anchors, verdicts, red_team_reversal):
    """Certainty is earned from evidence quality, anchors and panel agreement."""
    score, why = 100.0, []

    score -= 0.7 * disparity
    if disparity > 40:
        why.append(f"panel disparity {disparity:.0f}/100")

    if not anchors.get("event_confirmed", True):
        score -= 30
        why.append("earnings timing unconfirmed")
    if not anchors.get("event_implied_move_pct"):
        score -= 15
        why.append("no event-implied move anchor")
    if not anchors.get("historical_move_mean_abs"):
        score -= 10
        why.append("no historical realised-move anchor")
    if (anchors.get("historical_sample_size") or 0) < 6:
        score -= 5
        why.append("thin historical sample")

    lows = sum(1 for v in verdicts if v.get("confidence") == "Low")
    if lows >= 3:
        score -= 5 * lows
        why.append(f"{lows} of 7 personas at Low confidence")

    if red_team_reversal >= 70:
        score -= 12
        why.append(f"red-team reversal risk {red_team_reversal:.0f}")

    tier = "High" if score >= 70 else "Med" if score >= 45 else "Low"
    return tier, round(score, 1), why


def conviction_multiplier(consensus, tier):
    """
    Fraction of the expected move to claim as the signed point estimate.

    Direction and magnitude are separate questions. A lean is worth roughly a third to
    a half of the expected move; only a high-certainty strong call approaches 0.8x. The
    full implied move is never the point estimate — it is a one-standard-deviation
    reference, not a target.
    """
    mag = abs(consensus)
    if mag < 25:
        return 0.0
    if mag < 60:
        base = 0.30 + 0.20 * (mag - 25) / 35.0        # 0.30 .. 0.50
    else:
        base = 0.50 + 0.30 * (mag - 60) / 40.0        # 0.50 .. 0.80
    base *= {"High": 1.0, "Med": 0.85, "Low": 0.70}[tier]
    return min(base, 0.80)


def conviction_gate(consensus, disparity, tier, anchors, em, red_team_reversal):
    """
    Force Neutral / No Edge only when a directional call would actively mislead.

    A weak but coherent lean should survive as a Low-certainty prediction. Collapsing
    every uncertain read to Neutral produces a system that is never wrong and never
    useful.
    """
    if not anchors.get("event_confirmed", True):
        return True, "earnings timing not confirmed — no tradeable window"
    if em is None:
        return True, "no usable move anchor from either implied or historical data"
    if disparity > 70 and abs(consensus) < 35:
        return True, f"panel genuinely split (disparity {disparity:.0f}) with no clear centre"
    if red_team_reversal >= 75 and abs(consensus) < 40:
        return True, "red-team case materially breaks a thesis the panel only weakly holds"
    return False, None


def synthesize(doc):
    verdicts = doc.get("panel_verdicts") or []
    anchors = doc.get("anchors") or {}
    if len(verdicts) < 3:
        sys.exit("need at least 3 panel verdicts to synthesize")

    scores = [float(v["direction_score"]) for v in verdicts]
    probs = [float(v["prob_up"]) for v in verdicts]
    reversals = [float(v["reversal_risk"]) for v in verdicts]

    consensus = _mean(scores)

    # Diagnostic only: what the panel would say if louder analysts counted more.
    weights = [CONFIDENCE_WEIGHT.get(v.get("confidence"), 0.7) for v in verdicts]
    weighted = sum(s * w for s, w in zip(scores, weights)) / sum(weights)

    disparity = min(100.0, 2.0 * statistics.stdev(scores)) if len(scores) > 1 else 0.0

    up = sum(1 for s in scores if s >= 25)
    down = sum(1 for s in scores if s <= -25)
    neutral = len(scores) - up - down
    alignment = "aligned" if disparity < 30 else "mixed" if disparity < 60 else "split"

    # Reversal risk, with the red team weighted up when its case is specific.
    rev_w, rev_total = 0.0, 0.0
    red_team_reversal = 0.0
    for v in verdicts:
        w = 1.0
        if v.get("persona") == RED_TEAM:
            red_team_reversal = float(v["reversal_risk"])
            if v.get("strongest_reversal_case"):
                w = RED_TEAM_REVERSAL_WEIGHT
        rev_w += w
        rev_total += float(v["reversal_risk"]) * w
    consensus_reversal = rev_total / rev_w
    reversal_tier = ("Low" if consensus_reversal < 35
                     else "Med" if consensus_reversal < 60 else "High")

    em, em_basis = expected_move(anchors)
    tier, certainty_score, certainty_why = certainty(
        disparity, anchors, verdicts, red_team_reversal)

    # Shrink probability toward 50 for disagreement and for missing anchors.
    shrink = 1.0 - (disparity / 200.0)
    if not anchors.get("event_implied_move_pct"):
        shrink *= 0.90
    if not anchors.get("historical_move_mean_abs"):
        shrink *= 0.95
    prob_up = 50.0 + (_mean(probs) - 50.0) * shrink

    gated, gate_reason = conviction_gate(
        consensus, disparity, tier, anchors, em, red_team_reversal)

    call = "Neutral / No Edge" if gated else call_for(consensus)

    if call == "Neutral / No Edge" or em is None:
        signed = None
        mult = 0.0
    else:
        mult = conviction_multiplier(consensus, tier)
        signed = round(em * mult * (1 if consensus > 0 else -1), 1)

    prob_direction = prob_up if consensus >= 0 else 100.0 - prob_up

    implied = anchors.get("event_implied_move_pct")
    hist = anchors.get("historical_move_mean_abs")
    if implied and hist:
        ratio = implied / hist
        pricing = ("rich" if ratio > 1.25 else "cheap" if ratio < 0.80
                   else "fairly priced")
    else:
        pricing = "unavailable"

    return {
        "ticker": doc.get("ticker"),
        "consensus_score": round(consensus, 1),
        "confidence_weighted_score": round(weighted, 1),
        "call": call,
        "personas_up_down_neutral": [up, down, neutral],
        "prob_up": round(prob_up, 1),
        "prob_direction": round(prob_direction, 1),
        "certainty_tier": tier,
        "certainty_score": certainty_score,
        "certainty_drivers": certainty_why,
        "panel_alignment": alignment,
        "disparity": round(disparity, 1),
        "consensus_reversal_risk": round(consensus_reversal, 1),
        "max_reversal_risk": round(max(reversals), 1),
        "red_team_reversal_risk": round(red_team_reversal, 1),
        "reversal_risk_tier": reversal_tier,
        "unsigned_expected_move": round(em, 1) if em is not None else None,
        "expected_move_basis": em_basis,
        "signed_estimated_move": signed,
        "conviction_multiplier": round(mult, 2),
        "move_band_low_high": move_band(em, anchors),
        "move_band_note": "unsigned magnitude band, right-skewed; the implied move is "
                          "roughly one standard deviation, not a cap",
        "event_implied_reference": implied,
        "historical_move_reference": hist,
        "pricing_view": pricing,
        "conviction_gate_applied": gated,
        "conviction_gate_note": gate_reason,
        "chair_override_note": None,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="JSON with 'panel_verdicts' and 'anchors'")
    p.add_argument("-o", "--out", help="Write the packet here instead of stdout")
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        doc = json.load(fh)

    packet = synthesize(doc)
    text = json.dumps(packet, indent=2)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
