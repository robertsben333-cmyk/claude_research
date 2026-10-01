# What the resolved Australian runs have taught the hunters

**This file is deliberately empty, and it must stay empty until a run resolves.**

`researcher_us/LESSONS.md` holds rules that were earned: each one came out of
`edge_postmortem.py` scoring a finished US run finding by finding, after the outcome
existed. Nothing in Australia has resolved. There is no Australian post-mortem, so there
is nothing here that measurement put here.

Copying the US or Japanese lessons across would be worse than leaving it empty. It would
make `diagnostics.impact_sum_pre_lessons` measure the transfer of another market's rules
rather than the value of this market's own, and the delta would be uninterpretable from
the first day. The hunter reads this file, finds nothing, and says "nothing changed" in
`lessons_applied`. That is the correct behaviour and not a fault.

Add the first rule when `au_resolve.py` has scored a real run and a post-mortem says what
went wrong. Not before.
