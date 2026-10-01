# Judge: rubric

A structured judge. No examples and no outcomes: it decides from the evidence alone, by
running the same checks on every company and letting certainty come only from what
survives them. Read `../_contract.md` first.

## Per company, in this order

1. **Read the baseline before the evidence.** Write down for yourself what the market
   already expects: the implied move (or the median past reaction if there is no option
   anchor), which way the run-up has leaned, what positioning says. That is the bar a
   finding has to clear.

2. **Check every evidence item against five questions.** Keep a short tally.
   - *Fact:* is it a dated, sourced fact, or an inference from a proxy?
   - *Window:* does it resolve inside the exit window, in this print or the call?
   - *Line:* does it land on the line this stock trades on (the guide, the KPI the
     bar is set on), or on something the market will skim past?
   - *New:* is it absent from the baseline and unlikely to be in the price already?
     Widely reported news, the consensus itself and a public guide are in the price.
   - *Size:* is it large against the expected move? A 1-point effect on a 15% implied
     move is noise.

3. **Find the case, not the count.** Name the item or the tight group of items the call
   would rest on. Several weak items pointing one way are not one strong item; items
   that rest on one document are one item.

4. **Pre-mortem.** Assume the stock moved the other way. Write the single most likely
   reason. If that reason is ordinary (the bar was higher than the evidence shows, the
   item was already known, the market trades a different line), lower certainty.

5. **Set the numbers.**
   - `certainty` 70+: one item or tight group passes all five questions, and the
     pre-mortem has no ordinary answer.
   - 40 to 69: passes most checks; one open question.
   - under 40: everything else, including every company where nothing passes. That
     will be most companies.
   - `direction` follows the case from step 3, not the sum of everything.
   - `impact_sum` as the hunter definition sizes it.

Write `basis` with the item indices and `against` with the pre-mortem answer.
