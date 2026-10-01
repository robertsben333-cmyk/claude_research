# Stage E — lessons for the hunter, from the resolved days

This file is the part of the post-mortems that is still true tomorrow. It carries no
company fixes. Each entry is a pattern that has repeated across resolved runs, the tell
that you are inside it, and the rule that follows. It is the only research guidance the
hunter gets beyond the sealed baseline — the stage prescribes no method and no sources,
and this file does not change that. It changes what counts as a finding and how one is
sized.

**The hunter reads this file second, and the day is scored twice.** It sizes every
finding with the baseline alone, freezes that draft into `pre_lessons`, reads this file,
and then revises (`.claude/agents/unpriced-hunter.md` sets the order). `edge_score.py`
carries both sums — `impact_sum` and `diagnostics.impact_sum_pre_lessons` — and
`edge_resolve.py` ranks both against the same realised move, reporting the second as
`spearman_pre_lessons` beside the key. The price of that order is that nothing here can
steer a search, only a size and a selection. What it buys is falsifiability: a rule that
keeps costing rank correlation is visible within a few resolved days instead of living
here forever because it sounds right.

How it grows: `researcher_us/scripts/edge_postmortem.py` scores each resolved run finding by
finding — was the fact right, was the reaction right, which line did the move actually
land on — and pools the result. When a pattern recurs in that table, it belongs here.
When one of these stops recurring, say so under it rather than deleting it.

Provenance is given so the rule can be checked; the rule is what matters. Every example
below comes from the runs of 2026-09-08 through 2026-09-14, scored after the fact against
the releases.

---

## 1. A verified fact is not a predicted reaction

**The pattern.** The hunter proves something the market has not priced. The print
confirms it in every particular. The stock moves the other way, on the forward guide,
on the quality of the beat, or on positioning. This is the single most common failure
across the resolved days: on one day three of the four largest longs had their thesis
confirmed by the release and lost double digits; on another the top-ranked long got
revenue, margin and guidance direction right to within a rounding error and fell 8%.

**The tell.** Your finding is about the quarter being reported. The name's own reaction
history — the last eight prints in the baseline — shows beats being sold or a damped
response to good numbers. You have written a sentence like "an 8% revenue beat bought
only +1.8% last time" and your size does not reflect it.

**The rule.** Answer two questions separately and emit both: *what will the number be*
(`print_vs_bar_pct`) and *what will the stock do* (`expected_move_pct`). They are
different objects. The reaction function has veto power over the fundamental read: if
this name has not paid for the line your finding lands on, size the reaction small
however good the fact is. The divergence between the two numbers is recorded and
resolved; a hunter whose two numbers always agree is not answering the second question.

## 2. Name the line the finding lands on, and size one-offs as one-offs

**The pattern.** Four names on two days carried the same thesis — a tariff refund landing
in the quarter. The refund landed in all four. Two rose double digits, two fell double
digits, and the split was entirely the direction of guidance. The refund was correct
and it was noise. Elsewhere the most precisely right findings of a day — a below-the-line
recovery called to within $0.1m — opened up 8% and closed up 2% because sales were down.

**The tell.** The finding is a gain contingency, a refund, a remeasurement, an
impairment, a tax item, or anything below operating income; and nothing in it changes
what the company will guide to.

**The rule.** Every finding carries `lands_on`: `reported_quarter`, `guidance`,
`one_off`, `financing`, `capital_return`, `positioning`, or `other`. A `one_off` with no
stated path to the guide or to the multiple is sized at a fraction of what the same
dollars would be worth as operating profit, and the finding must say what the path is if
you size it larger. A `one_off` that *flows into* guidance (a raised range, a firmed
outlook) is a `guidance` finding and should be filed as one. A reported-quarter
impairment that nobody has quantified is the exception that has paid — it lands on the
line and it is not in the price — and it should still be filed under `reported_quarter`
with the reaction history checked.

## 3. Your own caveat has to reach the number

**The pattern.** The hunter writes the counter-argument in `independence`,
`why_not_priced`, `conviction_note` or `baseline_tension` and then sizes as if it had not.
One name carried "+2.0, record backlog coming" and "−3.0, cannot fund the revenue" at the
same time — they cannot both be true, the sum added them, and the wrong one won. Another
name had two of five findings whose own independence text argued the finding away; both
were sized negative anyway and together they were the difference between in the book
and out of it. A third wrote "an honest zero is a very plausible result" and emitted
+1.40.

**The tell.** Read your finding text as if someone else wrote it. If the sentence after
the finding starts with "but", "although", "the honest counterweight" or "cuts against",
the number above it was written before that sentence was.

**The rule.** Before you emit, read the set. A finding whose own text argues against it is
resolved or dropped, not sized. Two findings on one name that cannot both be true are
resolved by you, now, into one finding with one sign — the sum cannot do it and will add
them. If `baseline_tension` says the evidence cuts against the skew and the run-up, your
`expected_move_pct` has to be visibly smaller than the sum of your findings, and the
`conviction_note` says by how much and why.

## 4. Financing is a question, not a verdict

**The pattern.** A new revolver, a term loan, an ATM, a secured facility ahead of the
print was read as distress and sized as a large negative. The company was funding a
record ramp; revenue printed +70% and backlog at a record. On another name the same
read was made and the company posted record revenue with 600 basis points of gross
margin expansion.

**The tell.** Your negative finding is a financing event and you have not looked at what
the money is for.

**The rule.** Ask what the money buys and whether backlog, bookings, inventory build or
hiring corroborate a ramp. Financing that funds visible demand is a positive or a zero.
Financing with no corroborated use, covenant pressure, or a going-concern flag is the
negative you were looking for. Sign it only after the question is answered, and say
which answer you got.

## 5. A narrow proxy loses to a broad public series, and "no filing" is not a cause

**The pattern.** A distributor's quarter was called down on one promotional week of
industry unit data, while the industry body's half-year revenue figure was already public
and pointed up 18%. A company's end market was called hot from three government series;
the company itself said its job volume in that market was soft. Two names got positive
findings from "the drawdown has no cause in EDGAR, so the reaction is symmetric"; one fell
another 12% on a record quarter.

**The tell.** The finding is an inference from something that is not this company's own
number, and you have not checked whether a broader or more direct series already exists.
Or the finding is the *absence* of an explanation.

**The rule.** A company-level number in a primary document beats an industry proxy. A
proxy that contradicts a broader series already in the public record loses to that
series. Macro-to-company transmission is a hypothesis, not a finding, until the company
or a direct counterparty has said it. An unexplained drawdown in a microcap is worth 0:
positioning, borrow and a two-analyst bar do not file, and they are the information set.

## 6. Verify the bar; keep the finding inside the exit window

**The pattern.** A name turned on $0.19 against a $0.20 consensus; the baseline carried
$0.18, the hunter noticed it could not resolve the bar, wrote that down, and let the
disowned number anchor the whole name. On the same day two well-sourced negatives were
dated after the exit — a lock-up expiry and an exchange deadline — and they were 3.5
points of an 8-point spread that the trade would never see.

**The tell.** You are sizing a beat or miss and the consensus you are sizing against has
one source, or two sources that disagree. Or your finding's catalyst has a date and the
date is after the close of the first full session following the print.

**The rule.** State the bar you are sizing against and its source. If the bar cannot be
sourced to a company guide or to two agreeing estimate sources, cap every finding on the
name at a small size and say so. Every finding carries `resolves_by`: the date by which
the market can see it. A finding that resolves after the exit window goes in
`outside_window`, sourced and sized, and not in `findings` — the key must only sum what
the trade can experience. Say also whether the finding lands inside or outside what the
company has already guided to; a finding inside the guided range is a reported-quarter
item on a name that already told the market to expect it.

## 7. Positioning is the thing you have to beat, not colour

**The pattern.** The most extreme put-skew in the universe said "buy downside"; the hunter
noted it, discounted for it, and went long. The skew won by 11%. Two shorts were placed
into names with 18% and 23% of float short; both squeezed for 24% and 26%. On a third,
the 20-day run-up was the withdrawal of an insider's bid, not priced disappointment, and
the hunter read that correctly — that is what beating the baseline looks like.

**The tell.** Your sign disagrees with a large `skew_25d_vol_points`, or you are negative
on a name whose short interest you have not looked up.

**The rule.** The baseline is not a formality. A sign against a strong skew needs an
explicit statement of why the option market is wrong about this print, or a smaller
size. Before any negative finding, look up short interest and days to cover — the
baseline does not carry them — and a crowded short is a reason to shrink the negative,
because the squeeze is a mechanism in its own right. Record what you found in
`positioning_check`.

## 8. Thin coverage means a confirmed fact moves more, not less

**The pattern.** A hunter proved the consensus for a one-analyst microcap was a
mechanical output of guidance plus a known refund, concluded the outcome was
"pre-determined" and therefore expected a *smaller* move than the median. The stock
moved +17.5%. On the best day in the record, eight of nine realised moves were larger
than the hunter's number, by up to 16 points.

**The tell.** You have a confirmed, unpriced, company-level number on a name with one or
two estimates and you are sizing it below the name's own median reaction because "it is
already determined".

**The rule.** Pre-determined and unpriced on a thin name is the setup for a large move,
because nobody is positioned for it. Size on the name's own reaction distribution,
which the baseline carries, not on how certain you are of the number. Understatement is
the systematic error in the hunters' sizes; it does not need help.

## 9. Size a segment finding net of the rest of the company

**The pattern.** A hunter was correctly bearish on the 44% of revenue it modelled and
silent on the 56% that grew 68%. Total revenue cleared the bar it had called
unreachable. The sweep had handed it the offsetting segment by name.

**The rule.** Where a finding rests on one segment, one customer or one product, write
the line "what would have to go right in the rest, and how big is it" and size the
finding net of that answer, not gross.

---

## What has worked, and shares one property

The findings that paid, across the resolved days, were a number in a primary document
that no aggregator carries and that lands on the line the stock trades on: a refund
recognition policy in a 10-Q matched to a disbursement window; a backlog figure in a
prospectus that implied bookings far above the record quarter every preview anchored
on; a peer's print landing after the company last spoke, leaving consensus stale; a
quantified impairment in the body of a 6-K that was not in the exhibit sent to the
wire; a deferred-revenue and cash walk read straight off the filing. None was reasoning
from weather, covenant arithmetic or a remeasurement model. Documents beat inference,
and on this sample it is not close.

## Lessons recorded before this file existed

These were found on earlier runs and live in the hunter and sweep prompts or in
`EDGE_ANALYSIS.md`. They are restated here in the same form so this file is the complete
set; the prompts keep their own wording.

**Least priced is not most likely right.** The old scorer multiplied size by
(1 − priced_in), which structurally rewarded obscurity; the least-priced finding of one
whole day was the most wrong about the future. A fact nobody has priced may be unpriced
because it is wrong or irrelevant. "Nobody is looking at this" is the start of a finding,
not the finding. `why_not_priced` has to say what would be visibly different if the
market had priced it.

**Pass the market's directional statement as a number, never as prose.** A brief once
described skew in words and got the sign backwards; the hunter caught it only because the
sealed file contradicted the brief. Read `skew_25d_vol_points` and `priced_lean_pct` from
the baseline yourself.

**Two readings of one document are one finding.** "Missed the June guide" and "missed the
Q2 guide" were the same range and the same miss. Two findings resting on one number is one
finding; say in `independence` when findings share a document.

**Do not use one entity as evidence in both directions.** A file once argued a partnership
was hollow because the partner's documentation named a subsidiary, while another finding in
the same file treated that subsidiary as the company's own impaired asset. Read the set.

**The date is on the URL path, not in the snippet.** Search results relabel last year's
stories with this year's date. Three separate leads on one name were a year old.

**Asking "what did the market miss" into a print generates pessimism.** Six of eight leaned
negative on the first run; six of eight on another day, into a day that was five of eight
positive. Good news and nothing are both real answers, and the note counts the sign balance
every day so the artefact stays visible.

**A calendar row is a claim.** Eight of twelve names on the first run had no earnings event.
The sweep now confirms events from company sources; a hunter that finds no event returns 0.

**Self-rated confidence carries no information.** Across the sealed backtest the model's own
evidence-quality split accuracy 50/50. Nothing you feel about your certainty enters the
key; only your sizes do, which is why the sizing rules above matter.

**A reaction history built from the wrong events is worse than none.** For foreign private
issuers the baseline can mistake monthly operational updates for prints. Where the sweep
set `baseline_history_trustworthy: false`, rebuild the base rate from confirmed releases
before sizing against it.

## What this file does not do

It does not change the ranking key, the conviction floor or the execution rule; those
are measured in `EDGE_ANALYSIS.md` and set in `config/pipeline.yaml`. It does not
reintroduce a checker — nothing verifies a finding for being factually wrong, and two of
the costliest errors above were contradicted by public documents available before the
print. That cost is accepted and the note says so every day. And it is not a checklist
of where to look: where the hunter looks stays free.
