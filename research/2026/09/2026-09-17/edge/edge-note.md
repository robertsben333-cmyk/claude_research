# Edge hunt — 2026-09-17 amc + 2026-09-18 bmo

**One name in the window, and it does not clear the floor. Nothing is traded today.**

The ranking key is `impact_sum` — the hunter's own signed per-finding sizes added up, in
points of spot — exactly as `edge-scores.json` names it in its `ranking_key` field. There
is no call, no threshold and no direction label anywhere below.

## The ranked table

| ticker | session | `impact_sum` | floor | tradable | control (`-run_up_20d_pct`) |
| --- | --- | ---: | :---: | --- | ---: |
| UPXI | `amc` 2026-09-17 | **−2.30** | no | `elsewhere` — $4.80m/day, liquidity `ok`, **Alpaca will not lend it** | −19.32 |

`conviction` 2.30 against a `conviction_floor` of 3.0. **Zero of one names clear the
floor**, so nothing below is an emphasis call — it is the whole table.

**A one-name day cannot be ranked.** There is nothing to rank UPXI against. This run
contributes exactly one event to the pooled sample and produces no within-day rank
correlation at all; `edge_resolve.py` will have nothing to report for 2026-09-17 on its
own. That is a property of the day, not a failure.

## Why the day is one name

22 rows sat on the Nasdaq calendar across the two dates (15 on 09-17, 7 on 09-18).
**Twenty of them carry no session at all** — Nasdaq's `time-not-supplied` — and were
dropped, per the standing rule that eight of eight such rows had no earnings event
whatever on 2026-08-31. `--include-unknown` was deliberately withheld. Of the two rows
carrying an explicit session, IPHA is 09-17 `bmo`, which is this morning and outside the
window. That leaves UPXI.

The sweep **confirmed 1 of 1 and found 0 phantom rows**, from a company source: a
2026-09-15 GlobeNewswire release naming a 5:30 p.m. ET call on 2026-09-17 for fiscal-year
2026 results (FY ended 2026-06-30). The date is verified on the URL path, not the snippet.
`amc` is settled, so the reaction session is the 2026-09-18 regular session.

## The finding driving the number

The name is both top and bottom of the table, so this is the whole of it. UPXI is a
~$74m-equity Solana treasury company holding ~2.17m SOL, trading at roughly 0.35× gross
treasury NAV, reporting its **first audited annual report** since the treasury was built.

**The single most interesting finding — −1.2 points — is that Upexi is carrying two live
Nasdaq deficiencies that no financial media has covered.** A 2026-06-24 Staff determination
that it violated Listing Rule 5635(a) by issuing $151,169,169 of convertible notes at $4.25
(2025-07-09) and ~$36m at $2.39 (2026-01-09), convertible into 20%+ of pre-transaction
shares, **without shareholder approval**; a remediation plan was due 2026-08-10 and no 8-K
has since reported its acceptance, nor has a proxy for a ratification vote been filed. On
top of that a 2026-07-31 notice of non-compliance with the $1.00 minimum bid price, with a
2027-01-26 deadline and an explicit reverse-split path.

- Source: https://www.sec.gov/Archives/edgar/data/1775194/000147793226004047/upxi_8k.htm
  (2026-06-26), and https://www.sec.gov/Archives/edgar/data/1775194/000147793226004640/upxi_8k.htm
  (2026-07-31) for the bid-price notice.
- **What the price already says:** essentially nothing. A targeted search on the listing
  rule returns the SEC document and generic law-firm explainers — zero wire pickup, zero
  analyst note. Put/call open interest is 0.06 on 11,453 contracts, so nobody is paying
  for downside. Against that, the stock is up 19.32% in 20 days.
- **Why it is only −1.2:** the hunter's own stated risk is that the 10-K may not be filed
  by the 2026-09-18 close — last year's went in on 2025-09-24 against a 2026-09-28 deadline
  — in which case the risk factors are never visible inside the exit window and only the
  call can surface it.

The other five: a walk-forward to a **stockholders' deficit of roughly −$50m to −$60m** on a
balance sheet struck at SOL $75.01 against ~$101 today (−2.0); the company's own marketed
"adjusted SOL per share" KPI **going backwards** on its own methodology (−1.2); a revenue
miss to ~$3.5–4.2m against a $7.00m estimate (−0.4); the BitGo Prime facility amendment
three days before the audit read as a secured lender getting *more* comfortable, and so as
evidence against a going-concern paragraph (**+1.5**); and the crowded short itself
(**+1.0**).

## The critical read — there is no floor-clearer to be hard on

Nothing clears the floor, so the note owes no recommendation. What it owes instead is why
the number is small, because the hunt is not saying "nothing is here":

- **The gross negative case is about −4.8 points and it nets to −2.3.** `flags` records
  this: *"findings split 2 positive / 4 negative: the sum nets opposing theses rather than
  resolving them."* That is a real weakness of the row, not a nuance. Two sourced positives
  cut against four sourced negatives and the key adds them rather than deciding between
  them.
- **The bar is one source.** ($0.09) EPS and $7.00m revenue from a single syndicated
  estimate in the MarketBeat family, which the hunter could not corroborate — TipRanks
  shows the same −0.09 attached to a *different* fiscal quarter. No company guide exists.
  The hunter capped every size on the name for this reason and said so.
- **Positioning is a reason to shrink a negative, and it did.** 14.78m shares short =
  **27.33% of a 54.06m float**, 5.41 days to cover. Into a nano-cap print with no real
  option market, that is a squeeze mechanism, and the squeeze is the thing that has cost
  this stage its worst losses.
- **Most of the negative case resolves outside the window.** Four sourced findings worth
  **−16.0 points** are dated after the 2026-09-18 close — the July 2027 convertible
  maturity, the 2027-01-26 bid-price deadline — and are correctly kept out of the key. A
  reader who reads the −2.30 as the hunter's view of the company is reading it wrong: it is
  the hunter's view of what resolves by tomorrow's close.
- **It is not shortable at Alpaca.** `assets` asked live and got `no`. A negative row the
  book could not have taken even had it cleared the floor. It is `elsewhere`, not
  untradeable — a short Alpaca will not lend is routinely borrowable at IBKR, and COE read
  borrowable the morning after this book refused it — so check borrow at IBKR before
  calling it untradeable.

## Everything a reader needs in order not to over-read this table

**Separate the order from the sign.** Below the conviction floor the sign of `impact_sum`
is a **coin flip** on the evidence so far — 53% over 38 de-duplicated events. UPXI sits at
−2.30, *below* the floor. Reading that as a bearish view is exactly the mistake this
paragraph exists to prevent. Above the floor the rank of `conviction` predicted whether the
sign was right at ρ=+0.514 (permutation p=0.0015), but the forward regime is one hunter per
name and the single-hunter control puts that at **+0.361, not +0.514** — that is the number
to expect.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. Regression
slope 0.72–0.76, median absolute error 6–7 points against a realised standard deviation
near 11. It also double-counts: the same fact reached through two documents enters twice,
which is what the cluster-max was built to stop and what the measurement then demoted.

**The control.** `-run_up_20d_pct` is **−19.32** for UPXI. With one name there is no order
to compare, so the hunt neither beats nor loses to the control today — it simply cannot be
tested. Over the six resolved runs that free number, available off the sealed baseline
before any subagent is spawned, ranked at ρ=0.335 against the hunt's raw 0.407, a gap whose
confidence interval spans zero. **The stage has not been shown to beat doing no research at
all.**

**Sign balance: 1 of 1 hunts leaned negative** (findings 2 positive / 4 negative). One name
says nothing about hunter pessimism, but the count is recorded so it can pool: if hunts keep
leaning negative across many days, the hunter prompt is generating pessimism into a print
rather than detecting it.

**Nothing checked the findings.** There is no adversary pass and no second hunter —
`diagnostics.adversary_judged` reads `0/6`. A factually wrong finding entered the key at
full size and nothing in this run would have caught it. That is the accepted cost of
running nineteen names on twenty subagents, and **it did not stay hypothetical today**: the
sweep's claim that the baseline history was contaminated was itself factually wrong (see
below), and it reached the hunter's sizing unchallenged. It was caught only because the
session re-checked EDGAR by hand after the key was written.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four of
the twelve had opposite signs**, on a key whose typical magnitude is about 5. UPXI's key is
−2.30. Nothing re-measures that dispersion now. A second hunter on this name could
plausibly have returned a positive number.

**How much of the baseline was measured rather than inferred.** One of one names has a live
option chain — but only just. Front expiry 2026-09-18 at **1 day to expiry**, ATM bid-ask
**67% of mid**, total open interest 11,453, put/call 0.06. The baseline's own warning reads
*"implied move is indicative only"*. So the 11.43% straddle implied move is not a market
view and was not handed to the hunter as one. `edge_resolve.py` still normalises by the
expected move, so the normalised correlation for this name should not be called an
implied-move measure.

**The sweep alleged the baseline's reaction history was contaminated. It is not — the sweep
was wrong, and the hunt ran on that false premise. This is the run's most important
caveat.**

The sweep set `baseline_history_trustworthy: false` and claimed EDGAR supported only one of
the baseline's six prints. Checked directly against the submissions feed
(https://data.sec.gov/submissions/CIK0001775194.json), **all six baseline dates are exactly
the six most recent 8-K item-2.02 acceptances**: 2026-05-13, 2026-02-10, 2025-11-12,
2025-09-26, 2025-05-16, 2024-12-23. `priced_in.py` filters on the item code and it filtered
correctly. The sweep's two specific claims are both refuted by that feed:

- It said the 2025-11-12 row lines up with 8-Ks carrying items 8.01/9.01 and **no** 2.02.
  The 2025-11-12 8-K carries items **2.02, 9.01**, accepted 21:06:12 UTC. The 8.01/9.01
  filing it is thinking of is dated **2025-11-14** — a different filing, two days later.
- It said the 2026-05-13 row is measured a session late against a Q3 8-K accepted
  2026-05-12 at 20:40:59 UTC. That 2026-05-12 20:40:59 filing is the **10-Q**, not an 8-K.
  The item-2.02 8-K is 2026-05-13, accepted 20:35:40 UTC.

So `median_abs_move_pct` 6.58, the 2-up-of-6 skew and `deadband_pct` 3.29 were all usable,
and the hunter was told — on the sweep's authority and in this session's own briefing — not
to use them. It rebuilt a base rate it described as "n=1 clean" when n=6 was clean, and its
`lessons_applied` records discarding the median and the deadband. **The key below was
therefore formed under a false premise about its own baseline.**

It has not been rescored and the hunt has not been re-run. Re-hunting a name after seeing
its first number is the selection this stage is built to avoid, nothing was traded, and the
honest record is more useful to `edge_postmortem.py` than a tidier one. But a reader — and
the resolver — should treat this row's size as carrying that defect. The direction of the
effect is not obvious: the true history (median absolute move 6.58%, 2 up of 6) and the
hunter's substitute (two prints in a 9–16% band) point the same way in kind, and the
hunter's stated reason for a small number was the run-up and the short base, not the base
rate.

One residual question the feed does not settle: the company's own release put the Q1 FY2026
call on 2025-11-11, while the item-2.02 8-K was accepted 2025-11-12 at 17:06 ET. If the news
was genuinely out on 11-11, that one move is measured a session late. That is a real and
much narrower question than the contamination the sweep alleged.

**This is exactly the failure mode the removed adversary used to catch** — a factually wrong
claim entering the run at full weight with nothing checking it. Here it entered through the
sweep rather than a finding, where not even the adversary would have looked.
`baseline_quality` 0.4 is in `diagnostics` and decides nothing either way.

**What the day would have cost to trade.** UPXI turns over **$4.80m a day** at $1.05 —
comfortably above the $200k floor and above the $1m thin threshold, so this is not a
capacity problem. The binding constraint is borrow, not size. With one name, the question
"are the extremes of the ranking reachable" has no content today; on the pooled sample it
does, and six of the first 22 positions traded under $1m a day.

**`edge/LESSONS.md` moved this number, and by how much is recorded.** The hunter's frozen
pre-file draft summed to **−3.5**; after reading the file it revised to **−2.3**, a
`lessons_delta` of 1.2 — driven by capping sizes on an uncorroborated bar, shrinking
negatives into a crowded short rather than only offsetting them, and resolving a finding
that contained its own rebuttal. `edge_resolve.py` will rank both against the same realised
move. **One day's delta is noise**; it takes several resolved days carrying both numbers
before that comparison says anything about whether the guidance file earns its place.

**One day is an anecdote.** Five to twelve names cannot produce a meaningful rank
correlation, and one name cannot produce one at all. The pooled figure across many days is
the result.

## Names that could not be ranked

None. One name in the window, `rankable: true`, scored.

The twenty `time-not-supplied` calendar rows were never in the universe and so are not
"unrankable" — they were dropped before a baseline was sealed, deliberately, and are listed
here only so the reader knows the day had 22 rows and not 1: VFS, HUBG, DAVA, YRD, IH,
EONR, CMMB, ALAR, SMXT, BTTC, SNYR, ITP, IPST (09-17) and NB, HTLM, TRT, ZONE, CELU, ENLV,
LNAI (09-18). IPHA was 09-17 `bmo`, outside the window.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
