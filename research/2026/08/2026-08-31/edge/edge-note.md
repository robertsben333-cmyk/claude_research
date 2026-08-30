# Edge hunt — 2026-08-31, before the open

## The answer

**No calls. 0 of 12 names, 0% coverage.**

Eight of the twelve names on the calendar are not reporting on 31 August at all. Of the
four that are, one had both its hunters abstain, and the other three produced findings
that the adversary showed were already published, already in the price, or arithmetically
wrong.

This is the first live run of stage E, and 0% coverage is the design working rather than
the design failing. A day with four real events and no surviving unpriced information is a
day to stand aside.

## The universe was mostly fiction

Nasdaq's calendar carried twelve rows for the date. Nine had `time-not-supplied`, and
every one of the eight checked resolved to **no earnings event on 31 August**.

| name | what is actually true |
| --- | --- |
| AIV | reports on a liquidation basis since a February shareholder vote; no earnings release since 2 March |
| CHRN | 31 May fiscal year end; FY26 10-K filed 19 August. The 31st is a fiscal-quarter *end* |
| GRFS | reported H1 on 28 July; next print 10 November |
| SSL | reports 1 September, 11h00 SAST |
| GASS | announced on 28 August that Q2 lands 2 September |
| FRGT | re-qualified as a foreign private issuer in September 2025; files no quarterly report at all |
| CURR | semi-annual filer; next report in the autumn |
| CBAT | redomiciled to Cayman on 23 June, now exempt from 10-Q and 8-K |

The mechanism is identical every time: a data vendor projects the last known reporting
cadence twelve months forward. The clearest tell came on FRGT, where Nasdaq and
stockanalysis.com both carry a date **and disagree by a day** — two independent estimators
rather than a schedule.

This vindicates `universe.exclude: unconfirmed_timing` in `config/pipeline.yaml`. Stage 0
already drops these rows, and the exclusion is better founded than its one-line comment
suggests: not merely conflicting BMO/AMC, but rows where no event exists. This run
measured the base rate at 8 of 8 by deliberately including them.

## The four real names

**SAIC** — full tier, and the only name with a proper priced-in statement: a 9.39%
event-implied move, **+6.86 vol points of 25-delta skew** and a 23:1 put/call
open-interest ratio, sitting 2.3% off its 52-week high after a +7.5% twenty-day run. The
market is paying hard for downside protection on a stock near its high.

Both hunters abstained, independently, and both found the same thing: an 8-K of 14 August
raising the MUFG receivables-purchase facility from $300m to $400m, seventeen days before
the print, while the Q1 10-Q shows only $164m drawn on the old cap. Each judged that its
more probable reading agrees with a skew already paying for downside, and neither would
take the other side. Both also independently killed the same false signal — SAIC prime
obligations down 14% year on year looked like deterioration until Leidos (−21%), CACI
(−32%) and Parsons (−49%) showed the same shape, which makes it FPDS reporting lag.

**SY** — the two hunters returned **opposite calls** from the same sealed baseline, both
deriving their case from the same disclosed cohort table. One read a frozen store count as
a maturing cohort compounding without new-store drag; the other read it as a shrinking
network with accelerating closures and a 26% fall in revenue per centre.

Six findings judged, four `already_priced` and one `partially_priced`. The bull case fell
when management turned out to have stated **59 centres, not 54**, on the Q1 call — the
trade-press source was reproducing the March-31 press release, not recounting. The bear
case fell on arithmetic: the cohort buckets key on *operating duration*, so December-opened
stores carry over, and 6 carryovers plus 5 new gives 11 with zero closures. The average-age
datum settles it — 6 at ~3.1 months and 5 at ~0.9 averages 2.10 against a reported 2.1 —
and the same model reproduces management's stated Q4 figure.

Held at 48.8 on `no finding survived the adversary outright`.

**LX** — confirmed event, five findings, the strongest informal-layer discovery of the day:
a Wuhan Fenqile office where staff were given a collections-or-minimum-wage choice in July,
present only in Chinese commentary and corroborated across two outlets, against an offline
inclusive-financing business management said was nearly half of Q1 originations. Plus the
peer read-through that post-dates anything LX has said: FinVolution disclosed on 27 August
that July China volume fell roughly 50%. Held at 32.5 under the thin-tier cap.

**BLRX** — confirmed event and a mechanical finding: a $3.75m registered direct closing the
morning of the print. The adversary broke it on three counts. The "140 sessions of ADV"
used a denominator the announcement had already invalidated fivefold — 47,836 ADSs traded
that day against a 9,660 average. The deal priced at a *premium* to the prior close, not a
discount. And the warrant structure the hunter believed was unpublished had its own
subheading in the wire coverage. Held at 25.0.

## Coverage

**0 called / 12 scored.** Every name in the universe is in `edge-calls.json` with its
confidence and the components that produced it, whether called or not. Selection happens by
thresholding that complete table, which is what makes the risk-coverage curve computable
after the fact and what stops "I only call the ones I am sure about" from being an
unfalsifiable claim.

Worth recording as a property rather than an accident: a `thin`-tier name with one hunter
**cannot reach the 55 threshold at all**. Maximum raw is 90 against a 0.5 multiplier. A
name with no usable option chain and no recoverable reaction history is structurally
uncallable, which is what the coverage gate was for.

## What this run cannot tell you

One day of four real events is not a test of accuracy, and 0% coverage means there is no
accuracy to measure. The risk-coverage curve needs many runs before its slope means
anything. What this run did test is the plumbing, and the plumbing found eight phantom
events and six of its own bugs.

Coverage tracks market cap. Three of the four real names here are sub-$250m ADRs, which is
the thin end of the distribution rather than the flattering one.

## Corrections made during the run

Six faults, every one silent, every one flattering, and every one found by checking a
number against an independent source rather than by reading code.

- Reaction history drawn from a reporting regime the company had abandoned (AIV)
- Reaction history belonging to a predecessor on the same CIK (CHRN, pre-reverse-merger)
- Illiquid option chains returning garbage rather than nothing (AIV 135.69% implied move,
  GASS −124 vol-point skew)
- The guard against that then nulling a good number on a wide weekend spread (SAIC)
- Scoring voting two abstaining hunters into a Lean Down at 65 confidence
- Adversaries launched against the bullish findings only, which would have mechanically
  favoured whichever side went unattacked

A seventh is fixed but **deliberately not applied to this run**: `priced_in.py` now reads
6-K exhibit text and recovers reaction history for foreign private issuers, where it
previously reported `n=0` on five of twelve names. Regenerating a sealed baseline after the
hunts would have lifted SY from `partial` to `full` and LX from `thin` to `partial` with
the evidence already in. It runs from the next session. The counterfactual is recorded and
it is clean: with the fix LX reaches 48.8, still short of 55, so the bug did not cost a
call.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
