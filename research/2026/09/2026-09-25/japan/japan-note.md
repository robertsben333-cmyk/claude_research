# Stage J — Japan researcher — 2026-09-25

**2 eligible of 4 scheduled; 2 hunted.** all 2 eligible names (at or under the cap). Calendar as of 2026-09-03.

## The ranking

| # | code | company | impact_sum | conviction | above floor | priced_lean | baseline_quality |
| --- | --- | --- | ---: | ---: | :---: | ---: | ---: |
| 1 | 3333 | ASAHI CO.,LTD. | -2.5 | 2.5 | — | -0.11 | 0.725 |
| 2 | 2742 | HALOWS CO.,LTD. | -3.9 | 3.9 | yes | -0.46 | 0.725 |

## The drivers

**2742 ハローズ (Halows), impact_sum −3.90, above the floor.** The strongest-sourced hunt
of the three (20 sources). Its case is that the monthly 既存店 series — the only H1 series
most holders track — improved into August and reads like a recovery, while Q1's 94bp
operating-margin collapse from staffing and depreciation on four February stores is
structural and repeats in Q2. That puts H1 operating profit near ¥5.2bn, a 進捗率 of ~42%
against a ~48% norm, on a name with **no published sell-side consensus at all** — IFIS
returns a dash — so nothing on the tape forces the two series to be reconciled.
Source: https://www.halows.com/ir/finance_monthly/

**3333 あさひ (Asahi), impact_sum −2.50, below the floor.** Its finding is that IFIS
consensus 経常 is byte-identical to the company's own ¥4,440M guide, so no analyst has
independently marked the plan down. The hunter cut its own reported-quarter finding from
−1.0 to −0.5 after reading `LESSONS.md`, on the open question about monthly disclosures
pre-empting the print — all six months of H1 were already published. `pre_lessons` −3.0
against a final −2.50, so the lessons control is live and measurable.
Source: https://kabuyoho.ifis.co.jp/index.php?action=tp1&sa=consNewsDetail&nid=3333_20260403_act_20260403_130015_1

**Capacity note the scorer cannot see:** Halows turns over ¥137.9m a day, about $0.9m.
It clears the floor but sits in the thin range `researcher_us/EDGE_ANALYSIS.md` flags as
unnoticed by the budget. Stage J places no orders, so this is a ranking caveat only.

**Exit timing:** the 09-25 release is a Friday after the close, so the exit session is
Monday 2026-09-28.

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
