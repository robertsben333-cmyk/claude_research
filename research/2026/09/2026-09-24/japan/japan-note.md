# Stage J — Japan researcher — 2026-09-24

**1 eligible of 2 scheduled; 1 hunted.** all 1 eligible names (at or under the cap). Calendar as of 2026-09-03.

## The ranking

| # | code | company | impact_sum | conviction | above floor | priced_lean | baseline_quality |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 4716 | ORACLE CORPORATION JAPAN | -3.5 | 3.5 | yes | -0.454 | 0.725 |

## The driver

**4716 日本オラクル (Oracle Corporation Japan), impact_sum −3.50, above the floor.** The
hunter's larger finding is on the reported quarter: the consensus bar for 経常利益 sits at
¥23,100M, +7.4% YoY, with the full-year guide behind it. Its second finding is positioning
rather than fundamentals — the stock rallied +4.4% in the five sessions into the print
(¥8,954 on 2026-09-10 to ¥9,346), so the run-in is itself an expectation. `pre_lessons`
and the final sum are identical at −3.50: the (deliberately empty) lessons file changed
nothing, which is the correct behaviour on a file with no measured rules in it yet.

Only one name cleared the microcap floor. The other scheduled name, 3160 OOMITSU, trades
¥3.1m a day against a ¥30m floor.

## What a reader must not take from this table

**Every name here is negative.** Three names is not a sample and a one-directional day
carries no information about the method; it is recorded because a reader who saw only
this table would infer a bearish view the stage does not hold.

**There is no option anchor in this market, and since 2026-09-18 it is substituted rather
than merely disclosed.** `options` is all `null`. The lean above is built from JPX's
disclosed short register (level and change) and 信用倍率, so `baseline_quality` reads
0.725 where it was capped at 0.40, and the lean's rank correlation with the free control
is around 0.45–0.59 where it used to be 1.0 by construction. **The weights behind it are
priors with no Japanese measurement behind them.** `jp_resolve.py` ranks each component
separately so measurement can replace them, and reports `lean_vs_free_control_rho` — if
that climbs back to 1.0 the sources stopped resolving and the lean is the run-up alone
again, which is invisible in this table.

**All three names carry a real zero on the short register**, i.e. no disclosed position at
or above the 0.5% threshold. So on this particular day the short components contributed
nothing and the lean is carried by 信用倍率 and the run-up. That is a property of these
three names, not of the method.

**`history` is an estimated cadence**, not a record of announcement dates. It is a scale
for how far the name travels. No date in it is a fact.

**Daily price limits truncate the tail**, so a large finding can be right and still not be
paid in full.

**The selection was not a judgement.** Names were cut on turnover and then, where more
than the cap survived, drawn at random against a date seed. Nothing in the ranking above
reflects a view about which names were worth hunting.

**One day establishes nothing.** These numbers pool across days. A single day's ranking
over one to three names is noise, and `jp_resolve.py` will say so.

This is research, not investment advice. It is a forecasting exercise over public information and must not be presented as advice.
