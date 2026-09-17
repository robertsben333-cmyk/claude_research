# Edge hunt — 2026-09-17 amc + 2026-09-18 bmo

**Two names. One clears the floor — TRT at +5.10 — and it was bought at market two minutes
before the close. I do not recommend it, and the reasons are below.**

The ranking key is `impact_sum` — the hunter's own signed per-finding sizes added up, in
points of spot — exactly as `edge-scores.json` names it in its `ranking_key` field. There
is no call, no threshold and no direction label anywhere below.

## The ranked table

| ticker | session | `impact_sum` | floor | tradable | control (`-run_up_20d_pct`) |
| --- | --- | ---: | :---: | --- | ---: |
| TRT | `bmo` 2026-09-18 | **+5.10** | **yes** | `yes` — $1.63m/day, liquidity `ok`, long side needs no borrow | +0.35 |
| UPXI | `amc` 2026-09-17 | **−2.30** | no | `elsewhere` — $4.80m/day, `ok`, **Alpaca will not lend it** | −19.32 |

**1 of 2 clears the `conviction_floor` of 3.0. Both are rankable.** Two names is still not a
day that can be ranked in any statistical sense — a two-point Spearman is either +1 or −1 —
so this contributes two events to the pooled sample and nothing more.

**The book: TRT long, 338 shares at $11.2592, $3,799 = 33.0% of equity**, filled at 19:58
UTC against a 20:00 close. Execution cost 0.23% against the mid at submission, inside a
half-spread the tool measured at 14.6% — which tells you how wide this name quotes. UPXI was
refused for being below the floor, and would have been refused again on borrow.

## How TRT got into this run at all, and why that matters

TRT was **not** in the sealed universe. It arrived on the Nasdaq calendar as a
`time-not-supplied` row for 09-18, was dropped with the other nineteen, and was then
**refuted by the day's second sweep** — which claimed its fiscal-year prints "historically
land ~09-23" and told the run to look again on 09-22.

That was wrong, and the operator's challenge is what surfaced it. TRT's own EDGAR history
shows it files its fiscal-year item-2.02 8-K and its 10-K **the same day, in mid-to-late
September, every year for twenty years** — and last year that day was **2025-09-19**, a
Friday, one day off the calendar row. The sweep cited 2022 and 2024 and missed the single
most relevant precedent. No item-2.02 has been filed since 2026-05-14 and the 10-K deadline
is around 09-28, so the print is genuinely due.

**This is the third bad call of the day from an agent in this stage**, and they should be
read together rather than as three accidents: the first sweep asserted UPXI's baseline
reaction history was contaminated when it was clean (see below); the second sweep refuted
TRT on an incomplete filing history; and the same sweep's reasoning on ZONE was thin even
where its conclusion held. Nothing in the stage checks a sweep's assertions — the adversary
never looked there — and all three were caught only by hand.

## The critical read of the floor-clearer

**TRT — not recommended, and the book took it anyway.**

The book rule is mechanical: `|impact_sum| >= 3.0`, side from the sign, plus a turnover floor
and a borrow check. TRT passes it. That rule is the only cut in `edge/EDGE_ANALYSIS.md` that
survived a family-wise correction and step 6b is explicitly not a decision the session gets
to make, so the order went in. This paragraph changes no file and no order. It is still what
I would tell a reader.

- **The hunter does not believe its own sum.** `flags` records it: *"hunter's
  expected_move_pct (+2.00) is under half the sum of its findings (+5.10): its own caveats
  did not reach the sum."* The hunter's stated reaction number is **+2.0, below the floor**.
  Only the mechanical sum clears it. Its `conviction_note` is explicit that +5.1 becomes +2.0
  through two haircuts — a 0.45 probability that the print even lands in the window, and a
  15% sell-the-news discount — and neither haircut can reach `impact_sum` by construction,
  because the key sums findings and nothing else.
- **The date is not company-confirmed, and that is the dominant risk.** TRT has **never
  pre-announced an earnings date in its entire EDGAR history**. Aggregators split between
  09-18 and 09-21. 09-18 would be the earliest fiscal-year print in nine years — the earliest
  on record is 2025-09-19 and the median is 09-24. The hunter put P(print in window) at
  **~0.45**. If it does not print tomorrow, the position is a coin-flip on a thin microcap
  with no event in it.
- **The bar is unsourced, and `flags` says the sizes should have been capped.** There is no
  analyst estimate for TRT at all — `stockanalysis.com` shows coverage and price target as
  `n/a` — no company guidance, and no options market. The hunter built its own ~$18m naive
  bar and estimated ~$19.5m against it. That is a model, not a bar.
- **Which line does it land on?** The +4.0 driver is `reported_quarter` — a record ~$19–20m
  FQ4 taking FY2026 to ~$67m against $36.5m, roughly +83%, flipping the year to profit. The
  supporting +1.8 is `positioning`. Nothing lands on `guidance`, which is the line that has
  historically paid.
- **This name pays for revenue and ignores the P&L — which cuts both ways.** The +30.54% on
  2026-05-14 came on FQ3 revenue of $16.5m, +124% YoY on AI-GPU and EV burn-in demand,
  reported alongside an **$81k operating loss**. That is the whole reason the gross-margin
  negative was sized at only −0.4. But note the other half of the history: this name paid
  **+0.55% for the fiscal-year print specifically** on 2025-09-19. The big move was a
  quarter, not a year-end.
- **It is thin, and the quote is wide.** $1.63m/day of turnover — above the $1m thin
  threshold, so not flagged `thin`, but the measured half-spread at submission was 14.6%.
  Any headline return on this name is an upper bound on what size could actually have got.
- **The 09-15 Form 25 lead resolved the opposite way to how it reads.** The Form 25 /
  8-A12B / CERT trio is not a delisting — it is the mechanical follow-through of a
  **voluntary upgrade from NYSE American to the Nasdaq Global Market**, disclosed in the
  8-K of 2026-08-19, last day on NYSE MKT 09-15, first day on Nasdaq 09-16. It was on the
  wire a month ago and is priced. No finding was taken on it.
- **Remaining flags:** two findings worth +3.00 resolve after the exit window and are
  correctly out of the key; the findings split 2 positive / 2 negative, so the sum nets
  opposing theses rather than resolving them.

**UPXI — not recommended, and correctly not traded.** Below the floor at −2.30, where the
sign is a coin flip. Separately unlendable at Alpaca, so the short could not have been taken
even had it cleared; that is `elsewhere`, not untradeable — check borrow at IBKR.

The most interesting single finding in the run is still UPXI's, and it did not reach the
book: **two live Nasdaq deficiencies that no financial media has covered** — a 2026-06-24
Staff determination that Upexi violated Listing Rule 5635(a) by issuing $151,169,169 of
converts at $4.25 and ~$36m at $2.39 without shareholder approval, with a remediation plan
due 2026-08-10 that no 8-K reports as accepted and no proxy filed; plus a 2026-07-31 $1.00
bid-price notice.
(https://www.sec.gov/Archives/edgar/data/1775194/000147793226004047/upxi_8k.htm). A targeted
search returns the SEC document and law-firm explainers, nothing else. It is only −1.2
because the 10-K may not be filed before the 09-18 close — last year's went in 2025-09-24 —
in which case the risk factors never appear inside the window.

## Everything a reader needs in order not to over-read this table

**Separate the order from the sign.** Below the conviction floor the sign of `impact_sum` is
a **coin flip** on the evidence so far — 53% over 38 de-duplicated events. UPXI at −2.30 is
below the floor; reading it as a bearish view is the mistake this paragraph exists to
prevent. Above the floor the rank of `conviction` predicted sign-correctness at ρ=+0.514
(permutation p=0.0015), but the forward regime is one hunter per name and the single-hunter
control puts that at **+0.361, not +0.514**.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. Regression slope
0.72–0.76, median absolute error 6–7 points against a realised standard deviation near 11.
TRT is the live demonstration: the key says +5.10 and the hunter that produced it says +2.0.

**The control.** `-run_up_20d_pct` is **+0.35** for TRT and **−19.32** for UPXI, which orders
the day the same way the hunt does — TRT above UPXI. On two names that agreement is
meaningless, but it is worth stating that the hunt has **not** distinguished itself from the
free control today. Over the six resolved runs that number ranked at ρ=0.335 against the
hunt's raw 0.407, a gap whose CI spans zero. `alpaca_trade.py plan` printed it beside the
side: the control agrees with the traded side on 1 of 1 names.

**Sign balance: 1 hunt leaned positive, 1 negative.** Findings across both: 4 positive, 6
negative. Recorded so it can pool — if hunts keep leaning negative across many days, the
hunter prompt is generating pessimism into a print rather than detecting it.

**Nothing checked the findings.** No adversary pass and no second hunter —
`adversary_judged` reads `0/4` for TRT and `0/6` for UPXI. A factually wrong finding enters
the key at full size. **This did not stay hypothetical today**: three separate agent
assertions were wrong (see above), and each was caught only by a hand check after the fact.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four of
the twelve had opposite signs**, on a key whose typical magnitude is about 5. TRT's key is
+5.10 and UPXI's is −2.30. Nothing re-measures that dispersion now.

**How much of the baseline was measured rather than inferred.** **One of two** names has a
live option chain, and it is the one that did not clear the floor. UPXI's chain is 1 DTE with
a 67%-of-mid ATM spread and the baseline's own warning is "indicative only". **TRT has no
options market at all** — no implied move, no skew, and its `expected_move_pct` is a
historical median. So the name that was bought is the name with no priced expectation to
measure anything against. `edge_resolve.py` still normalises by expected move, so the
normalised correlation for TRT is not an implied-move measure.

**`edge/LESSONS.md` moved both numbers.** UPXI: pre-file sum −3.5 → −2.3, delta 1.2. TRT:
pre-file sum **+3.0 → +5.1, delta 2.1** — the file made TRT *larger*, which is the direction
worth watching, since it pushed a name from just above the floor to well above it.
`edge_resolve.py` ranks both against the same realised move. **One day's delta is noise.**

**What the day would have cost to trade.** TRT at $1.63m/day is the thinner of the two and
is the one held; the position is 0.23% of ADV, so size was not the binding constraint, but
the 14.6% half-spread is. UPXI turns over $4.80m/day and was blocked on borrow, not
capacity. The general lesson from the pooled sample stands: six of the first 22 positions
traded under $1m a day, and a ranking whose extremes are untradeable is a research result
rather than a signal.

**The sweep alleged UPXI's baseline reaction history was contaminated. It is not — the sweep
was wrong, and the hunt ran on that false premise.**

Checked directly against https://data.sec.gov/submissions/CIK0001775194.json, **all six
baseline dates are exactly the six most recent 8-K item-2.02 acceptances**: 2026-05-13,
2026-02-10, 2025-11-12, 2025-09-26, 2025-05-16, 2024-12-23. `priced_in.py` filters on the
item code and filtered correctly. Both of the sweep's specific claims are refuted: the
2025-11-12 8-K **does** carry items 2.02/9.01 (the 8.01/9.01 filing it meant is 2025-11-14,
two days later), and the 2026-05-12 20:40:59 UTC filing it cited as a Q3 8-K is the **10-Q**.

So `median_abs_move_pct` 6.58, the 2-up-of-6 skew and `deadband_pct` 3.29 were all usable,
and the hunter was told not to use them. It rebuilt a base rate it called "n=1 clean" when
n=6 was clean. UPXI's −2.30 was formed under a false premise about its own baseline. It has
**not** been rescored and the hunt has not been re-run: re-hunting a name after seeing its
first number is the selection this stage exists to avoid, nothing was traded on it, and the
honest record is worth more to `edge_postmortem.py` than a tidier one.

One residual question the feed does not settle: the company's own release put the Q1 FY2026
call on 2025-11-11 while the item-2.02 8-K was accepted 2025-11-12 at 17:06 ET. If the news
was out on 11-11, that one move is measured a session late.

**One day is an anecdote.** Two names cannot produce a meaningful rank correlation. The
pooled figure across many days is the result.

## The twenty dropped rows, checked

The `time-not-supplied` rows were dropped before a baseline was sealed, then **checked
anyway** on the operator's instruction by a second sweep over all twenty
(`sweep-unknown.json`), and the seven 09-18 rows were then re-verified by hand against
EDGAR.

**Corrected score: 1 of 20 was worth hunting, not 0 of 20.** That one is TRT, above. The
other nineteen are refuted, and for the 09-18 set the refutations are now direct filing
evidence rather than the sweep's assertions:

| row | verified |
| --- | --- |
| NB | item-2.02s at 2025-07-16, 2025-10-14, 2026-01-12 and **none since January**; FY2026 is overdue or October |
| ZONE | fiscal year ends **June** and last year's FY print was **2025-08-22**, not September; **no item-2.02 at all in 2026** |
| CELU | last item-2.02 2025-05-09; filed an **NT 10-Q on 2026-08-14** — a late-filing notice, not a print |
| ENLV | Israeli FPI, 6-Ks through 2026-08-11; December year end, so H1 was an August event |
| HTLM | no 1H/Q2 2026 results; what it is actually doing is an **F-1 and FWP in late August** — a follow-on offering |
| LNAI | no item-2.02 or 6-K in its recent filing history at all |
| CMMB, ALAR | already reported, 2026-08-19 and 2026-09-02 |
| HUBG | **no earnings event.** Mid-restatement; Nasdaq exception expired 2026-09-14, delisting determination expected, lender deadline 2026-11-30 |
| DAVA, YRD, IH | release pre-US-open, so a 09-17 row is `bmo` and already past |
| VFS | Q2 2026 genuinely outstanding and undated since the 2026-07-29 6-K; releases `bmo` and has always pre-announced |
| EONR, SMXT, SNYR, ITP, IPST, BTTC | sub-$40m, no discoverable IR schedule; the row is a filing-deadline projection |

**The phantom rate on `time-not-supplied` rows is 19 of 20 for this window** — not the 20 of
20 an earlier version of this note claimed, because TRT is real. Prior data points: 8 of 8 on
the 2026-08-31 first run, 0 of 10 when the flag was withheld. The rule to withhold
`--include-unknown` still holds on cost — nineteen hunters to find one name is a bad trade —
but **it is not costless, and today it cost the only name in the book.**

IPHA was 09-17 `bmo` — a real event, this morning, outside the window.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
