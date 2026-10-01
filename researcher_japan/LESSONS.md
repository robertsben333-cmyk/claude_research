# What the resolved Japanese runs have taught the hunters

**Four days have resolved, eight names (2026-09-24, 09-25, 09-28, 09-29).** That is far
too few for any rule here to be established. Each rule below states its count, so a
reader can see how little it rests on, and each is written to move one number, once,
as the shared hunter core requires. Write the rule, not the company.

## The record so far, on the corrected window

Scored from the last price before the release to the next close (see the hunter
definition, "find out WHEN it releases"). The first column is the hunt's
`impact_sum`, the second the realised move.

| print | released | call | moved | sign |
| --- | --- | --- | --- | --- |
| 2026-09-24 | 15:30 | −3.5 | +8.15 | wrong |
| 2026-09-25 | 15:30 | −3.9 | −1.15 | right |
| 2026-09-25 | 13:00 | −2.5 | −0.15 | right, by 0.15 |
| 2026-09-28 | 15:30 | −0.5 | +2.76 | wrong |
| 2026-09-29 | 15:00 | +1.0 | +2.47 | right |
| 2026-09-29 | 15:30 | +0.5 | −2.97 | wrong |
| 2026-09-29 | 15:30 | −1.5 | +0.86 | wrong |
| 2026-09-29 | 13:00 | 0.0 | +0.13 | no call |

Three of seven signs right. Before 2026-10-01 the resolver entered every name at the
event-day close, which scored the 13:00 and 15:00 releases on a window that began after
their own reaction and read the same day as one of seven. That was a measurement defect,
not a lesson, and it is fixed in `jp_resolve.py`.

## Rules

**1. A negative that rests on a series the market already has: `p_up` toward 50.**
Four of the seven calls were negatives built on "the 月次 show the quarter missing the
company's own plan". Two of those stocks fell (1.15% and 0.15%) and two rose (2.76% and
0.86%). The monthly series is public before the print, so the miss is held by the price
before you find it. If your negative rests on 月次 or on a 進捗率 that anyone can compute
from the last 短信, move `p_up` toward 50 unless the release is likely to ADD something
to it (a forecast cut, a dividend cut). Count: 4 names, 2 days.

**2. Your negatives outnumber your positives: check the sign, not just the size.**
Five of seven calls were negative. Nothing about these eight companies says five of seven
should fall, and the US stage saw the same tilt on its first day (six of eight negative).
Being asked what the market has missed into a print pulls toward bad news. Before you
emit a negative, write in `baseline_tension` the strongest positive the release could
carry (a held forecast, a buyback, a dividend) and whether you looked for it. This moves
`p_up` only where you did not look. Count: 7 calls.

## Open questions, and what the first days said

1. **Does the 進捗率 beat everything else?** So far, no: the progress-rate findings were
   the visible-miss findings of rule 1. Whether the progress rate against the company's
   OWN history ranks better than against a straight line is not yet measurable.
2. **Do monthly disclosures pre-empt the print?** The first evidence says yes, on four
   names. Rule 1 is the provisional answer.
3. **Does a prior 業績予想の修正 kill the event?** One case: a name whose H1 had been
   pre-released to the million yen four days earlier was hunted to 0 and moved +0.13% on
   the corrected window. Consistent with yes; one name settles nothing.
4. **NEW: is a five-day run-in into a print a short signal?** One hunter sized a +4.4%
   five-session run-in as −1.5 of positioning; the stock rose 8.15% on the release. One
   case. Not a rule; record it again if it recurs.

## The anchor, and the one number that tells you it is still working

There is no option anchor in this market. Since 2026-09-18 the baseline's lean is built
instead from JPX's disclosed short register (level and change) and 信用倍率, so it is no
longer the same number as the free control -- it ranked against the control at 0.446 to
0.59 on the 2026-09-11 universe, where it used to be 1.0 by construction.

**Check `lean_vs_free_control_rho` in the resolved file on every run.** If it drifts back
toward 1.0, the JPX register or the margin scrape has stopped resolving and the lean has
silently fallen back to `-0.05 * run_up_20d_pct`. That failure is invisible in the
ranking itself, which is why the resolver reports the number.

## The weights are open questions, not rules

`jp_priced_in.lean_components()` carries four weights and **none is measured on Japanese
data**. `jp_resolve.py` ranks each component separately. When several days have pooled,
a component that ranks at or below zero gets its weight cut to zero here, in writing,
with the pooled number beside it. Until then they are priors borrowed from the US runs.
