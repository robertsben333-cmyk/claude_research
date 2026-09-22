# Stage R — the reversal researcher

**The question.** Yesterday's biggest US losers: do they keep falling, or do they
bounce? And can research tell which is which, name by name, on the day?

**The hunter answers two questions, both bounded to the very short term** — the drop-day
close to the next session's close. *Did the fall misprice what is already known?* and
*does anything land inside the window that the price does not hold?* The second is the
one with documents behind it: an open ATM, a covenant, a deficiency clock, estimate cuts
that have only started, against an index trade that cleared or insiders who bought. The
first is the one the stage was built for and it is only answerable because of the
bound — **an overshoot earns nothing unless something closes the gap inside the window**,
so every repricing finding has to name that mechanism. See §7.

**The short answer, measured before a single agent was built: they keep falling.** Over
11,235 falls of 5% or more on 749 sessions, the median stock is down another 1.00% by
the next close, down 3.89% by the fifth and down 11.11% by the twenty-first. The median
is negative in **every** cut we took — by size of fall, by turnover, by price, by
sector, by how much of the fall happened overnight. "Buy the dip on yesterday's worst
names" is not a marginal idea. It is refuted at every horizon and every liquidity band.

**This stage places no orders.** There is no execution path and there must not be one.

---

## 1. How the stage is built, and why in this order

Phase 0 ran first, deliberately. It cost bars and no tokens, and it could have killed
the stage before anything expensive existed. `CLAUDE.md` is largely a record of what
the other order costs: stage E spent thirteen days of hunts before anyone measured that
its scorer was subtractive and that a one-line free control ranked better than it did.

```
rev_market.py      the listed universe, adjusted daily bars, a spread estimator, stats
rev_harvest.py     phase 0's data: every fall in the market, with what happened next
rev_backtest.py    phase 0's answer: base rates, cuts, free rankers, cost, the book
--------------------------------------------------------------- phase 0 ends here
rev_universe.py    the live day's worst K fallers
rev_forward.py     what is still SCHEDULED for each name, from measured sources
rev_priced_in.py   one sealed baseline per name, before any agent runs
edge_score.py      researcher_us/scripts/edge_score.py, UNCHANGED
rev_resolve.py     did the hunt rank the day, and did it beat the free controls
```

The scorer is not copied, forked or wrapped. The reversal baseline supplies the four
keys `edge_score.py` reads (`history.n`, `anchor_quality`, `priced_lean_pct`,
`event_plausibility.verdict`) and the hunter emits the same finding contract, so one
scorer serves five markets and two different events. A US earnings run rescores
byte-identically because nothing in it was touched.

---

## 2. Phase 0: the sample

| | |
| --- | --- |
| Universe | 6,014 US common stocks and ADRs on NASDAQ, NYSE and AMEX. Warrants, units, rights, preferreds and notes excluded |
| Bars | 3 years of split- and dividend-adjusted daily OHLCV, 0 empty charts out of 6,014 |
| Sessions | 749, 2023-09-25 to 2026-09-18 |
| Candidate rows | 283,812 falls of 4% or more above $100k a day |
| After the floors | 168,049 rows at ≤ −5%, ≥ $200k median 20-day turnover, ≥ $1 |
| **Selected** | **11,235 events** — the worst 15 of each session |
| Median fall | −20.83% |
| Median turnover | $1.43m a day |
| Median estimated half-spread | 0.53% |

The screen is the event definition, not a ranking inside it: "the biggest losers" is the
population being studied. Everything is rebuildable with
`rev_harvest.py --range 3y` and `rev_backtest.py --drops <dir>`; the 11,235 selected
rows travel with the report as `analysis/phase0-selected.jsonl.gz`, so every number
below is auditable without re-fetching the market.

---

## 3. What happens after a big fall

Entry at the close of the drop day, equal weight, gross of costs.

| horizon | mean | median | share that rose | t |
| --- | --- | --- | --- | --- |
| next open | **+0.93%** | 0.00% | 49.7% | +4.61 |
| next close | −0.30% | −1.00% | 44.5% | −1.15 |
| 2 sessions | −0.76% | −1.76% | 42.7% | −2.08 |
| 3 sessions | −0.83% | −2.58% | 41.5% | −1.52 |
| 5 sessions | −1.79% | −3.89% | 39.5% | −3.44 |
| 10 sessions | −3.84% | −6.72% | 37.2% | −5.81 |
| 21 sessions | −5.15% | −11.11% | 34.4% | −3.83 |

Net of the market it is worse at every horizon (−6.99% at 21 sessions), so this is not
the sample sitting in a bad tape.

**The mean and the median disagree, and the median is the honest one.** Means are
dragged up by a thin right tail of names that double; the median stock is down in every
row and in every cut below. Anyone quoting a positive mean from this stage is quoting a
tail.

**The one real bounce is overnight and it does not survive the spread.** +0.93% to the
next open, then the session gives it back. A round trip at the estimated half-spread
turns that +0.93% into −0.52%.

---

## 4. The cuts, at the next close

| by size of fall | n | mean | median | rose |
| --- | --- | --- | --- | --- |
| ≤ −40% | 916 | **−4.00%** | −5.41% | 35.4% |
| −40 to −25% | 2,720 | −0.76% | −1.55% | 43.6% |
| −25 to −15% | 5,827 | +0.27% | −0.64% | 45.6% |
| −15 to −10% | 1,608 | +0.39% | −0.24% | 46.8% |

Monotonic, and against the rebound thesis: **the harder it fell, the harder it keeps
falling.**

| by volume on the drop day | n | mean | median | rose |
| --- | --- | --- | --- | --- |
| > 15× normal | 1,601 | **−2.44%** | −2.59% | 38.8% |
| 5–15× | 3,277 | −0.54% | −1.03% | 43.8% |
| 2–5× | 3,222 | −0.72% | −0.70% | 45.5% |
| < 2× | 3,135 | +1.46% | −0.37% | 47.3% |

This is the most useful free variable on the page. Heavy volume means the fall carried
information and it keeps going; light volume means it did not. It is also the closest
thing phase 0 has to a test of the stage's own hypothesis, and it points the predicted
way.

Turnover, price and sector all move less. The $1–3 band is the only one with a positive
mean (+1.18%) and its median is still negative (−0.44%) — fat tail, not edge.

---

## 5. The free rankers, and the bar the hunt has to clear

Within-day rank correlation against the next close, 749 sessions, permutation p from
shuffling the outcomes inside each day.

| ranker | ρ | perm p |
| --- | --- | --- |
| **14-day ATR** (its own volatility) | **−0.126** | 0.0003 |
| position in the 52-week range | +0.079 | 0.0003 |
| **minus the size of the fall** (the reversal control) | **−0.076** | 0.0003 |
| price level | −0.075 | 0.0003 |
| minus the 20-day run-up | −0.053 | 0.0003 |
| volume spike | −0.046 | 0.0003 |
| share of the fall that was the gap | −0.014 | 0.138 |

Max-statistic correction over all thirteen candidates, one shuffle per day shared by
every candidate: **best |ρ| = 0.126, family-wise p = 0.0017.** It survives.

Two things follow and both are uncomfortable for the stage:

- **The reversal control has the wrong sign.** Ranking by how far a name fell is
  *negatively* related to what it does next. A rebound thesis is fighting this.
- **The bar is `atr14`, not nothing.** A hunt that ranks the day below ρ=−0.126 has
  added nothing a single number off the sealed baseline does not already give.

---

## 5b. Is it the fall, or just the kind of stock that falls?

The one-session table cannot tell those apart, and the drift that survives cost lives
at ten to twenty-one sessions. So the same two cuts, at 21 sessions:

| by size of fall | n | mean | median | rose |
| --- | --- | --- | --- | --- |
| ≤ −40% | 895 | **−13.76%** | −21.68% | 28.6% |
| −40 to −25% | 2,658 | −9.01% | −12.34% | 34.1% |
| −25 to −15% | 5,657 | −2.60% | −9.97% | 35.3% |
| −15 to −10% | 1,561 | −2.38% | −9.26% | 35.2% |

**Monotonic in the depth of the fall, and steeper than at one session.** So the drift is
about the event, not only about the kind of company that has these events. Good.

| by turnover | n | mean at 21 sessions | rose |
| --- | --- | --- | --- |
| < $1m a day | 4,601 | −5.18% | 31.3% |
| $1–5m | 3,201 | −6.34% | 31.9% |
| $5–25m | 1,845 | −5.67% | 37.9% |
| $25–100m | 796 | −3.08% | 45.2% |
| **> $100m** | 492 | **+1.65%** | 48.8% |

**And here is the one place a rebound thesis survives.** Above $100m a day the drift is
gone and turns slightly positive, and at five sessions that band is **+2.05% with
t=2.06** — the only positive cell in the whole cut table. Large, liquid stocks that fall
hard do bounce a little; small ones keep falling. The stage's own screen sits at a
median turnover of $1.43m, which is the wrong side of that line, and 492 events is a
thin basis for the claim. It is recorded because it is the kind of thing that gets
remembered wrongly, and because it is the natural next screen to test.

## 6. Could it be traded? Only at the long end, only short, and only with caveats

Equal-weight the worst 15 each session, one book per day, charged one round trip at the
Corwin-Schultz estimated spread (`x1`).

| horizon | short, all names | short, ≥ $5m a day | long, ≥ $5m a day |
| --- | --- | --- | --- |
| next close | −1.14% (t −4.2) | −0.56% (t −1.2) | −1.65% (t −3.5) |
| 5 sessions | +0.59% (t 1.1) | +0.63% (t 0.8) | −2.84% (t −3.7) |
| 10 sessions | +3.07% (t 4.3) | **+2.36% (t 2.5)** | −4.58% (t −4.8) |
| 21 sessions | +5.42% (t 4.0) | **+4.56% (t 4.4)** | −6.80% (t −6.6) |

**One session is not tradeable.** The gross edge is ±0.35% against a round-trip cost of
about 1.06 points. The drift only clears cost once it has had ten to twenty-one sessions
to accumulate, because the spread is paid once whatever the holding period.

### The t above is inflated, and here is the corrected version

Starting a new 21-session book every day means 21 books are open at once and consecutive
day-returns share 20/21 of their window. Thinned to non-overlapping books, all offsets
run:

| book | independent books | median mean | worst offset | median t | offsets with t>2 |
| --- | --- | --- | --- | --- | --- |
| 5 sessions, short | 148 | −0.53% | −0.88% | −0.44 | 2 of 5 |
| 10 sessions, short | 73 | +2.58% | −1.84% | +1.64 | 4 of 10 |
| **21 sessions, short** | 34 | **+6.57%** | −12.21% | **+2.44** | **15 of 21** |
| 21 sessions, long | 34 | −9.54% | −15.13% | −3.57 | 0 of 21 |

The five-session result evaporates. Ten is marginal. **Twenty-one holds**, with 15 of 21
offsets clearing t=2 — and with one offset losing 12% a book, which is the dispersion a
reader should take away rather than the median.

### Four reasons not to act on that table

1. **Borrow.** The short side assumes every name can be borrowed and charges no fee.
   These are exactly the names that cannot be. A hard-to-borrow rate of 20–100%
   annualised is 1.2–6.0 points over 21 sessions, the same order as the drift.
2. **Capital.** Fifteen names a day held 21 days is 315 concurrent positions.
3. **Spread.** Corwin-Schultz is a **floor** on the real cost, estimated from the days
   *before* the fall, so it cannot see the widening the fall itself causes.
4. **It is not this stage's question.** Stage R predicts the next session. The drift
   lives at ten to twenty-one. Those are different stages and they should not be
   conflated.

**One bias runs the other way, and it is worth stating.** The universe is today's
listings, so a fall followed by a delisting is absent from every row. That removes the
worst continuations only, which means the drift measured here is *understated*, not
flattered.

---

## 7. What phase 1 asks, and the hypothesis it pre-registers

Phase 0 says the *average* faller keeps falling. It says nothing about whether the
fallers can be told apart on the day. That is the research question, and it is the one a
language model might answer where a factor model cannot, because it turns on reading
documents.

### The question the hunter is given, in two legs

**Leg 1 — repricing.** Did the fall misprice what is already known?
**Leg 2 — new information.** Does anything land inside the window that the price does not
hold, bad or good?

Both are bounded to the drop-day close → next session close. This is the third version
and the first two were each half of it, which is worth recording because the reasoning
generalises.

**v1 asked only "did the fall overshoot".** Three problems, and the third is the one that
matters: it is backward-looking; "proportionate" has no unit; and **hindsight is
structural**, because the fall is the hunter's own input, so a model handed a 25% drop
will produce a fluent rationalisation in either direction.

**v2 asked only "is there more bad news coming".** Checkable, dated, document-backed —
and it throws away the case this stage exists for. A fall that was simply too big had no
leg to sit in, so it could only appear as colour.

**v3 asks both, and the short-horizon bound is what rescues leg 1.** An overshoot pays
nothing unless it *corrects* inside the window, so a `repricing` finding must carry
`mechanism_in_window`: the named thing that closes the gap before the next close.

| mechanism | why it closes a gap in one session |
| --- | --- |
| a wider overnight audience | the intraday tape was traders; the 8-K exhibit and the transcript get read after the close |
| the seller is finished and dated | an index trade that cleared, an offering that priced, a lock-up that passed |
| a note lands before the open | a reiteration, upgrade or defence puts a named buyer under a stock the tape had none for |
| a disclosed buyer stepped in | a Form 4 cluster, a 13D/G, an ETF trade file that publishes after the close |
| the wire copy is checkably wrong | and the correction is already public |
| supply is countable and spent | the close printed at the low on exhausted volume; say how many shares against what |

"It is cheap now", "the data was good", "the market over-reacts to these" are not
mechanisms. The brief tells the hunter to drop them or file them in `outside_window`,
and `pipeline.overshoot_has_mechanism` is the honest way to emit an overshoot that is
believed but cannot be dated.

**The legs are summed into the one ranked number and reported apart.** Every finding
carries `leg`; `rev_resolve.py` ranks `leg1_repricing`, `leg2_new_information`,
`overshoot_pct` and `more_to_come_pct` separately at every horizon, and splits
`by_overshoot_mechanism` into two arms. Which leg carries the result is the most useful
thing this stage can learn in its first month, and pooling them makes it unanswerable.

The cause of the fall is still established, in one block, because you cannot work out
what follows from something nobody has named. It is an input to both legs.

### The sources, and why the hunt is possible at all

Every source below was probed on 2026-09-22 and answered. `rev_forward.py` pulls them
into the sealed baseline, so the hunt starts at a document rather than a search box and
two hunts on one name start from the same documents.

| source | what it gives |
| --- | --- |
| `data.sec.gov/submissions` | every filing this issuer has made, dated, by form |
| **`efts.sec.gov` full-text search** | the TEXT of filings, scoped by CIK, form and date |
| `sec.gov` browse-edgar atom | Form 4 and 8-K feeds |
| `api.nasdaq.com/.../short-interest` | 24 dated settlements, level and days to cover |
| `api.nasdaq.com/.../insider-trades` | Form 4 summary, 3 and 12 month |
| `clinicaltrials.gov/api/v2` | trial status and primary completion dates |
| `api.fda.gov` | recalls, adverse events, approvals |
| `courtlistener.com/api/rest/v4` | federal dockets, **125 requests/day** |

The full-text search is the one that makes the stage work: seven phrases are run against
each issuer's own filings, twice — once ever, once over the last 550 days, because the
index returns hits by relevance and not by date. On the 2026-09-21 screen that found
recent ATM language in 11 of 15 names, going-concern language in 6, a minimum-bid-price
clock in 8 and a non-reliance item in 1.

**Three sources do NOT answer from this container and nothing may rest on them**: Nasdaq's
Listing Center (403), FTSE Russell's index *notices* page (404), Nasdaq's press-release
API (301). So an index deletion or a delisting notice is only assertable through the
issuer's own 8-K.

**Two corrections came out of the 2026-09-22 hunts, and both were wrong in the report
that raised them** — which is the argument for re-probing an agent's claim rather than
filing it. A hunt reported CourtListener unreachable; it had spent the **125-request daily
quota** and a re-probe returned 200, so a 429 there means spent, not down. The same hunt
reported FTSE Russell's quarterly IPO-additions PDF as having no ToUnicode map; it
downloads at 200, 419 KB, **and it has one**. What fails is this container's reader —
`eu_pdftext.py` decompresses streams but does not apply CMaps, so a subset-font document
comes back as font-table bytes. **The fix is a CMap-aware decoder, not another source**,
and it is not built. Until it is, issuer-level index membership rests on a secondary
aggregator plus the volume signature, and a finding that uses it has to say so.

**Two labels stop a reader over-trusting a number.** `next_earnings_estimated` is Zacks's
algorithm over historical reporting dates, served by Nasdaq, not a company announcement —
this repo has already paid for reading a cadence prior as evidence when TRT cleared the
conviction floor, was the day's only trade and never reported. And FINRA publishes short
interest about eight business days after settlement, so the position carried *into* the
fall is not observable.

### The outcome is reachable, which no earnings stage has to deal with

An earnings hunter runs before the print, so the outcome does not exist anywhere on the
internet. **Here the session being predicted may already be trading.** Its price arrives
unbidden in search snippets, quote widgets and page headers, and a hunt that has seen it
looks exactly like research while scoring like hindsight.

This was not theorised, it was observed: on the 2026-09-22 validation run one hunter
reported, unprompted, that live 09-22 quotes had appeared in several fetched pages and
that it had excluded them from every number. That disclosure is the reason the rule is
now in the brief — **no price, quote, chart or market summary dated after the drop-day
close may enter the reasoning**, and anything that reaches the hunter anyway has to be
declared in `searched_and_found_nothing`.

**The structural fix is the clock, not the rule.** The Routine fires after the US close
and the window opens the next morning, so a scheduled run cannot see the outcome. Both
validation hunts were hand-run in the middle of the session they were predicting, so
they are contaminated by construction and must never be pooled. That is recorded in the
run log as well as here.

### The hypotheses, pre-registered

Written into `config/pipeline.yaml:reversal_hunt.pre_registered_hypotheses` so neither
can be rewritten once the answer arrives:

> **Leg 2.** A fall with an identified, dated, **unfinished** pipeline of further bad
> news continues. A fall whose cause is **complete and dated** does not.
>
> **Leg 1.** An overshoot pays only where a **named mechanism** closes the gap inside the
> window. An overshoot without one does not.

The hunter supplies `pipeline.news_flow_balance` (−100…+100 on the forward flow alone)
and `cause.seller_is_finished_pct` (0…100 on whether the selling pressure is spent).
`rev_resolve.py` ranks both as their own columns at every horizon, **whether or not they
look good**, and the hunter is told to score them on the evidence rather than to make
them agree with `expected_move_pct`, so a disagreement is data.

Phase 0 already offers one piece of weak support, and it is the right way round: the
drift exists because bad news arrives in clusters, so the second shoe is the norm. Volume
is the cheapest proxy for it and it is the strongest conditional on the page.

### What would make phase 1 a failure

- The hunt's ρ against the next close does not beat `atr14`'s −0.126 over a pooled
  fortnight.
- `lean_vs_free_control_rho` sits near 1.0, meaning the baseline's own lean is the free
  control wearing another name. That is the stage J failure mode and it is a defect.
- `news_flow_balance` and `seller_is_finished_pct` show no separation.
- Neither leg ranks, and the two do not separate from each other.

Any of those, and the honest outcome is to write it down and stop.

## 8. Known biases, carried in the data file as well as here

| bias | direction |
| --- | --- |
| Survivorship: the universe is today's listings | **understates** the continuation |
| Spread is estimated, from before the fall | overstates every net return |
| No borrow check or fee on the short side | overstates the short book |
| Overlapping books at long horizons | inflates t, corrected in §6 |
| Hindsight: the hunter is handed the fall | overstates the hunt, mitigated not solved |

---

## 9. What the first live screen showed, which phase 0 could not

The 2026-09-21 session: 6,014 listed names, 200 pre-ranked on the screener, **77 above
the $200k and $1 floors**, worst 15 taken. SPY was +1.55% that day, so these were
idiosyncratic falls and not a tape.

**Not one of the fifteen had a usable option chain.** All came back
`no_options_market` or `unusable_chain`. That is not bad luck, it is a property of the
screen — a losers screen selects small names — and it means **stage R runs anchor-less
like stages J, EU and AU rather than like stage E**. The regime
`archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events is the
one this stage is in, and no amount of hunting changes that.

**The estimated half-spreads ran from 0.00% to 4.10%.** YDES at 4.10% is an 8.2-point
round trip on a name that fell 17.6%. The zeros are the estimator flooring a negative
alpha, not a narrow spread, and the baseline says so in `costs.half_spread_status`
rather than reporting a bare 0.00 that a reader would take at face value. **The spread
is this stage's binding constraint, not its ranking.**

**Two of fifteen tripped the corporate-action check** (`event_plausibility: suspect`) on
the shape that matters: the whole fall overnight, on below-normal volume, with no
intraday follow-through. Four others fell more than 15% on under 1.5× volume and were
deliberately left `unknown` — thin volume alone is ordinary in a $2m-a-day stock, and
naming the cause is the hunter's job rather than the baseline's guess.

## 10. State

Phase 0 is complete and is the only thing in this stage that has been measured.

**Nothing has resolved in phase 1. No hunter has run. No number here is evidence about
the hunt** — it is evidence about the market the hunt is being pointed at, and about
how high the bar is. `researcher_reversal/LESSONS.md` is deliberately empty until a
run resolves.
