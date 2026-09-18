# What the resolved Japanese runs have taught the hunters

**Nothing yet. No Japanese run has resolved.**

That is the honest state of this file on 2026-09-18 and it should stay empty until a
run has actually been scored by `jp_resolve.py`. The US equivalent,
`researcher_us/LESSONS.md`, holds rules that were each paid for by a resolved run, and
its value comes entirely from that. Copying its rules across would give this market a
file that looks authoritative and has never been tested here, which is worse than an
empty one: the hunters read this file *after* sizing the day once, precisely so the
cost of the guidance can be measured (`diagnostics.impact_sum_pre_lessons` against the
key). Guidance that has never been measured would corrupt that comparison from day one.

## What goes in here, and what does not

A rule earns its place after `jp_resolve.py` has scored the run it came from. Write
the rule, not the company: "a narrow proxy loses to a broad series" belongs here, "XYZ
Corp's monthly sales mislead" does not.

## Three things already known to be different, kept here as questions, not rules

These come from market structure rather than from a resolved run, so they are written
as open questions for the first post-mortems to answer.

1. **Does the 進捗率 beat everything else?** The bar in Japan is the company's own
   full-year forecast, not sell-side consensus. If the progress rate against plan turns
   out to be where the findings that rank actually come from, this file should say so
   plainly and the hunters should start there.
2. **Do monthly disclosures pre-empt the print?** Retailers and chains publish 月次.
   If most of the quarter is visible in them, findings built on them may be priced by
   the time the results land, and the honest size is smaller than it looks.
3. **Does a prior 業績予想の修正 kill the event?** A guidance revision filed before the
   results pre-releases the number. The first few runs should record whether names with
   a prior revision moved less, and if so the universe step may need to flag them.

## The caveat that applies to every Japanese finding until measured otherwise

There is no option anchor in this market, so nothing here tells you what the market
expected. `priced_lean_pct` is `-0.05 * run_up_20d_pct` and nothing else, which means
the free control and the baseline's only directional content are the same number. A
finding has to beat the run-up, not merely agree with it.
