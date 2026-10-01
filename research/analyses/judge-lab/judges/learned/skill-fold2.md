# Judging skill (learned from 125 resolved cases, fold 2)

The base rate is a coin flip, so start every name low. Across the 108 cases where the first
hunter filed anything, its sign was right 55 times (51%). A judge earns money only on the
small subsets below. Every count is taken from the casebook. "Right" means the realised
move had the sign of the call.

You do not see the hunter's sizes. Size each item yourself as the hunter definition would,
and sum them into your own `impact_sum`. The rules use that number.

## Rules that set how much the sign can be trusted

**R1. A listed options market means the price already knows. Cap these names.** On US
names whose baseline carries an implied move, the hunt was right **16 of 42 (38%)**, and the
misses were large (moves of −13 to +33%). On US names with no implied move it was right
**25 of 41 (61%)**, and on European names, which have no option anchor, 13 of 23. This held
on every day in the sample, not on one. Hold an optioned name at certainty 45 or lower,
and at no more than 55 even when R2 is met (2 of 4 in that cell).

**R2. Conviction counts only when the items agree.** When your own |impact_sum| is 7 or more
and items of the opposite sign make up less than 15% of the gross (the sum of absolute
sizes), the hunt was right **8 of 11**. At 7 or more with 15% or more on the opposite side,
it was right 2 of 6. At |impact_sum| ≥ 3 overall it was right 25 of 44, and below 3 it was
right 30 of 64. In Europe, size did not help at all (7 of 14 at ≥ 1.0, 6 of 9 below), so do
not lift a European name on size alone. If one item carries most of the sum, count it as one
finding and not as agreement.

**R3. Short calls on names with no options are the best cell.** On US names with no implied
move, negative calls were right **17 of 26**, and **11 of 16** at |impact_sum| ≥ 3. Positive
calls on the same names were right 8 of 15. Across all US names, negative calls were right
25 of 47 and positive calls 16 of 36. A long needs more than a short does to reach the same
certainty.

**R4. A short into a fresh pop needs very high conviction.** A negative call on a name with a
5-day run-up of +5% or more was right **4 of 12**. Below |impact_sum| 7 it was right 0 of 6,
and at 7 or more 4 of 6. Below 7, keep certainty at 30 or lower.

## Evidence types with a measured direction (use them to set the sign and to break ties)

**R5. A finance or revenue leadership change points down.** When a pack held an item about a
new or departing CFO, CAO, CRO or division head, or a quarter run without one, the stock fell
**8 of 10**. That includes two names where the hunter netted the pack positive. Treat such
an item as real negative weight, never as noise.

**R6. A dated funding, covenant or runway item points down.** Examples are a covenant test
about to bite, a waiver, a cash runway shorter than the plan, a deficit, or financing that
has not closed. The stock fell **8 of 10**, two of them names the hunter called up. An item
saying that stress has been removed (a refinancing, a maturity pushed out) does not belong
here.

**R7. Guidance that needs a back-half ramp points down; a stale, beatable bar does not point
up.** An item showing that the full-year guide needs a much stronger second half than the
first preceded a fall **7 of 9**. The mirror case, "consensus or guide is set too low, so a
beat is likely", was right **6 of 12**, which is no signal. Give beat arithmetic little size.

**R8. One-off windfalls do not lift the stock.** In packs that cited a one-off item as upside
(tariff refunds, gains on a sale or on debt extinguishment, a recognised contingency), the
stock fell **8 of 13**. Positive calls led by such an item were right 2 of 6. The market strips
these out, so size them near zero.

**R9. A direct read on the company's own sales line beats a macro proxy.** When the pack's
largest item is a direct measure of the line being reported, the call was right **8 of 11**.
Examples are category background checks or retail-category statistics that map onto the
product, the same-format competitor's same-quarter comps or margins, and category
registrations. When the largest item is an indirect proxy, the call was right **1 of 6**.
Examples are a producer price index, the weather, sector hiring, exchange turnover, a
commodity price or a partner's production. A direct series that agrees across two sources
(for example, the industry series plus two channel peers) is the strongest evidence in this
casebook.

## Evidence that should not move certainty

**R10. Crowded short interest is not a direction signal.** In packs that cited a large or
building short book, days to cover or squeeze risk, the stock rose **6 of 11**. Do not add
size for it in either direction.

**R11. An empty pack is no view.** When nothing was filed (17 cases), the stock rose 7 times
and fell 10 times, with moves as large as ±25%. Set direction 0 and certainty 0 to 10.

## Calibration

- About **one name in seven** should reach certainty 60 or more, and about half the names
  should sit at 25 or lower.
- To reach **60 or more**, a name needs all of these:
  - no implied move in its baseline (R1);
  - your |impact_sum| at 7 or more with less than 15% opposite-sign weight (R2), or a
    negative call at 3 or more backed by an R5, R6, R7 or R9-direct item;
  - not a short into a 5-day pop of +5% or more unless it is at 7 or more (R4).
- Reserve **70 or more** for an unlisted name with a negative call that meets R2 and also
  carries an R5, R6 or R7 item. In this casebook, every unlisted name that met R2 with a
  negative sign was right (5 of 5), but that is a small cell.
- **35 to 55**: a name that meets one strong rule but not the full set, an optioned name
  with strong agreeing direct evidence, or a long that meets R2.
- **25 or lower**: everything else. That covers most optioned names, most European names,
  sums under 3, mixed packs, and packs resting on beat arithmetic, windfalls, short interest
  or macro proxies.
- `expected_move_pct`: start from the median past reaction (or the implied move when there
  is one). Do not go above it unless the evidence is direct and agrees.

## Per-company checklist

1. Are there any findings? If not, set direction 0 and certainty ≤ 10 (R11).
2. Size every item yourself and sum them. Compute the share of gross that sits on the
   opposite side (R2).
3. Is there an implied move? If so, cap certainty at 45, or 55 when R2 is met (R1).
4. Long or short? Shorts on unlisted names start higher than longs (R3).
5. Does the 5-day run-up exceed +5% on a short? If so, cap at 30 unless the sum is ≥ 7 (R4).
6. Look for R5 (leadership), R6 (funding or covenant) and R7 (back-half ramp) items, and let
   them pull the sign down.
7. Discount windfalls (R8), short-interest items (R10), beat arithmetic (R7) and macro
   proxies (R9) to near zero.
8. Is the largest item a direct read on the company's own sales line? Only then may it carry
   the call (R9).
9. Count how many names are at 60 or more. If it is more than one in six, lower the weakest.
10. Write `basis` from the items that decide the call, and `against` from the strongest
    opposite-sign item or the rule that caps the name.
