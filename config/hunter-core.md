## The core: when to stop, what to file, how to size (every hunter, every region)

This block is shared by every hunter in this repository and is kept identical in each
definition by `scripts/sync_hunter_core.py`. It decides three things: how far you
search, what counts as a finding, and how big the numbers are. **Where anything else in
this definition, in a LESSONS file or in your brief says otherwise on those three
things, this block wins.** Everything else (where to look in your market, the event
check, the hard source rule, the output fields) stands as written below.

Two older instructions are superseded by name, because they appear further down in most
definitions: an instruction to make `expected_move_pct` "visibly smaller than the sum of
your findings", and any instruction to leave a sourced fact out because it is a proxy,
an inference, partly priced or in agreement with the skew. Both are replaced by the
steps below.

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

### 3. Size in three steps, in this order

**a. `abs_move_pct`: how far the stock moves over the window, whatever the direction.**
Start from the best scale you have: a usable option-implied move; else the base rates
this definition gives for your market; else the name's own median reaction in the
baseline. Move it for what is new in this release (a guidance change or first guide moves
more than a pre-released period), for thin turnover and for a crowded short. **Your
uncertainty about the sign never shrinks this number.** On every resolved sample in this
repo the hunters' numbers were too small: US regression slope 0.72-0.76, Europe a median
factor of three under the realised move.

**b. `p_up`: the probability, 0 to 100, that the stock closes the window higher.** This
is where all your uncertainty goes, and nowhere else.
- 50: nothing found, or the evidence is balanced. This is the non-result.
- 55-60, or 40-45: a lean from proxies, inference or partly priced facts.
- 60-70, or 30-40: a lean resting on a company-level number in a primary document.
- 70-85, or 15-30: a sourced number the market has not seen that decides this print.

**c. The findings carry the signed total.** `expected_move_pct` = (2 × p_up / 100 − 1) ×
abs_move_pct, and the findings' `expected_impact_pct` values must add up to it, because
the day is ranked on their sum. Give each finding a share in proportion to its weight:
the finding that sets your `p_up` carries most of the total. A minor finding gets a small
share; do not cancel a decisive finding with a stack of weak opposite ones. With `p_up`
at 50 the findings sum to 0, whether there are none or several that offset.

### 4. Each lesson moves one number, once

Choose `abs_move_pct` and `p_up` with every caveat in mind, then stop. Do not apply a
lesson a second time by shrinking the findings afterwards.

| lesson | the number it moves |
| --- | --- |
| a verified fact is not a predicted reaction; this name sells its beats | `p_up` toward 50 |
| the finding lands inside what the company already guided | `p_up` toward 50 |
| the bar is unsourced or disputed | `p_up` toward 50, for the findings that depend on it |
| your own caveat argues against the finding | `p_up` toward 50, or merge or drop it if a document contradicts it |
| a proxy, an inference or macro-to-company transmission | the finding's weight inside the total, never its filing |
| a sign against a strong skew, or a crowded short against a negative | `p_up` toward 50 unless you can say why the market is wrong |
| thin coverage with a confirmed, unpriced, company-level number | `abs_move_pct` up |
| a guidance change, first guide or new period likely | `abs_move_pct` up |
| the period is already pre-released and the guide is not expected to move | `abs_move_pct` down |
| a one-off below operating income with no path to the guide | the finding's weight inside the total |
| financing | the sign, after you have asked what the money buys |
| a segment finding | its weight, net of the rest of the company |
| dated after the exit window | `outside_window`, not `findings` |

### 5. What you emit for this block

Add `abs_move_pct` and `p_up` to your top-level output if your schema below does not
already carry them, add `rejected_candidates` (each with `candidate`, `source`, `reason`
from the four in step 2, and `detail`), and keep `pre_lessons` as your definition
describes, with the same three steps applied to the draft. The hard rule is unchanged:
every finding carries a real URL and date, and nothing you remember about how this print
went may enter your answer.
