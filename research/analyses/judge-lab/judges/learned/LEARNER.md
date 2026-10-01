# Learner: write a judging skill from resolved cases

You do not judge anything. You write the skill another judge will use. Read
`../_contract.md` first: the isolation rules apply to you too, and the contract is what
the judge using your skill must produce.

## Input

One casebook file (named in your task): resolved cases from earlier days, each with
what the hunter filed, the sizes it gave, its `impact_sum`, and the move that followed.

## What to produce

A file `SKILL.md` at the path your task gives, at most about 1,200 words, that tells a
judge how to pick the few names it should be sure about. It will be applied to
companies on OTHER days that you never see.

Rules for writing it:

- **Only patterns that recur.** Each rule states how many cases support it and how many
  go against it, counted from the casebook, e.g. "(right 9 of 12 when the hunter was
  confident)". A rule with fewer than five supporting cases does not go in.
- **No company names, no tickers, no dates.** Rules must transfer to new companies.
- **Watch for day effects.** If a pattern holds only because one day's names all moved
  the same way, it is not a rule.
- **Say what lowers certainty as well as what raises it.** The judge's main job is to
  leave most names low.
- **Calibrate.** Say roughly what share of names should reach certainty 60 or more, and
  what a name needs to get there.
- End with a short checklist the judge runs per company.

Then reply with one line: the path you wrote and how many rules it has.
