## The core: when to stop, what to file, how to size (every hunter, every region)

This block is shared by every hunter in this repository and is kept identical in each
definition by `scripts/sync_hunter_core.py`. It decides three things: how far you
search, what counts as a finding, and how big the numbers are. **Where anything else in
this definition, in a LESSONS file or in your brief says otherwise on those three
things, this block wins.** Everything else (where to look in your market, the event
check, the hard source rule, the output fields) stands as written below.

Three older instructions are superseded by name, because they appear further down in
some definitions: an instruction to make `expected_move_pct` "visibly smaller than the
sum of your findings"; any instruction to leave a sourced fact out because it is a proxy,
an inference, partly priced or in agreement with the skew; and any instruction that your
findings' sizes "must add up to" `(2 × p_up / 100 − 1) × abs_move_pct`. All three are
replaced by the steps below.

### 1. Search in proportion, and a non-result is a real result

Cover the places a print turns on: the company's own latest documents (filings, the
last release and call), counterparties that have spoken since the company last did
(customers, suppliers, peers that reported after it), at least one independent series
where one exists for this business, and positioning. Follow anything strange you meet on
the way. **When those come back empty, stop.** You do not have to try every angle, and a
hunt that finds nothing is a correct and common outcome. Write the angles you tried in
`searched_and_found_nothing` and return the non-result as described in step 3.

### 2. File what you found

Every sourced fact that bears on this print inside the exit window is a finding. You may
drop a candidate for exactly four reasons: it has no source URL and date; it resolves
after the exit window (it goes in `outside_window`); it duplicates another finding (merge
them); or a primary document contradicts it. A stage-specific admission rule written in
this definition also applies (stage R: a `repricing` finding needs a
`mechanism_in_window`). Nothing else removes a finding. Every candidate you drop goes in
`rejected_candidates` with its reason.

### 3. Size twice: each finding on its own, then the print as a whole

You emit two measurements of the same print. They are scored apart, stored apart and
ranked apart, and **neither is fitted to the other**.

**a. Each finding on its own: `expected_impact_pct`. Their sum is `impact_sum`, the
ranking key.** Size every finding at what THAT finding alone would move the stock over
the window, signed, in points of spot, with `impact_low_pct` and `impact_high_pct` as an
honest range. Size it against what actually moves this stock: a usable option-implied
move, the base rates this definition gives, the name's own reaction when that line
surprised before. A finding worth more than the implied move needs to be extraordinary.
Do not divide a total among your findings, and do not shrink them afterwards so their sum
matches anything: a decisive finding carries its full size even when weaker ones sit
beside it. Where two findings rest on one fact, merge them rather than counting the fact
twice. A caveat that applies to a finding makes THAT finding smaller, once (step 4).
With no findings, or findings that genuinely offset, the sum is 0, and that is a correct
answer.

**b. `abs_move_pct`: how far the stock moves over the window, whatever the direction.**
Start from the best scale you have: a usable option-implied move; else the base rates
this definition gives for your market; else the name's own median reaction in the
baseline. Move it for what is new in this release (a guidance change or first guide moves
more than a pre-released period), for thin turnover and for a crowded short. **Your
uncertainty about the sign never shrinks this number.** On every resolved sample in this
repo the hunters' numbers were too small: US regression slope 0.72-0.76, Europe a median
factor of three under the realised move.

**c. `p_up`: the probability, 0 to 100, that the stock closes the window higher.** This
is where the uncertainty of this second measurement goes, and nowhere else.
- 50: nothing found, or the evidence is balanced. This is the non-result.
- 55-60, or 40-45: a lean from proxies, inference or partly priced facts.
- 60-70, or 30-40: a lean resting on a company-level number in a primary document.
- 70-85, or 15-30: a sourced number the market has not seen that decides this print.

**d. `expected_move_pct` = (2 × p_up / 100 − 1) × abs_move_pct.** The scorer recomputes
it from your two numbers and stores it in a separate file as `impact_scaled`. It is not
the ranking key, and your findings do not have to add up to it. If the two measurements
disagree in sign, or one is several times the other, say why in `conviction_note`: the
gap is information, not an inconsistency to tidy away.

### 4. Each lesson moves one number per measurement, once

Size the findings with every caveat in mind, then stop; size `abs_move_pct` and `p_up`
with every caveat in mind, then stop. Do not apply a lesson a second time by shrinking
the findings, or the sum, afterwards.

| lesson | in your findings (3a) | in the scaled number (3b-3d) |
| --- | --- | --- |
| a verified fact is not a predicted reaction; this name sells its beats | that finding smaller | `p_up` toward 50 |
| the finding lands inside what the company already guided | that finding toward 0 | `p_up` toward 50 |
| the bar is unsourced or disputed | the findings that depend on it capped small | `p_up` toward 50 |
| your own caveat argues against the finding | that finding smaller, or merged or dropped if a document contradicts it | `p_up` toward 50 |
| a proxy, an inference or macro-to-company transmission | that finding smaller, never left unfiled | its weight in `p_up` |
| a sign against a strong skew, or a crowded short against a negative | that finding smaller unless you can say why the market is wrong | `p_up` toward 50, same exception |
| thin coverage with a confirmed, unpriced, company-level number | that finding larger | `abs_move_pct` up |
| a guidance change, first guide or new period likely | the guidance finding sized on the guidance scale | `abs_move_pct` up |
| the period is already pre-released and the guide is not expected to move | findings on the pre-released lines toward 0 | `abs_move_pct` down |
| a one-off below operating income with no path to the guide | that finding at a fraction of the same money as operating profit | its weight in `p_up` |
| financing | the sign, after you have asked what the money buys | the same |
| a segment finding | its size, net of the rest of the company | its weight in `p_up` |
| dated after the exit window | `outside_window`, not `findings` | neither |

### 5. What you emit for this block

Add `abs_move_pct` and `p_up` to your top-level output if your schema below does not
already carry them, set `expected_move_pct` by the formula in 3d, add
`rejected_candidates` (each with `candidate`, `source`, `reason` from the four in step 2,
and `detail`), and keep `pre_lessons` as your definition describes, with both
measurements applied to the draft: `impact_sum_pct` is the sum of the draft findings'
own sizes and `expected_move_pct` the draft's scaled number. The hard rule is unchanged:
every finding carries a real URL and date, and nothing you remember about how this print
went may enter your answer.
