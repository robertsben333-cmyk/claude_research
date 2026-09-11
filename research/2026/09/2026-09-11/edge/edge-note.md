# Edge hunt — 2026-09-11 window

**Ranked on `impact_sum`** — the hunters' signed per-finding sizes added up, in points
of spot. That is the ranking key `edge-scores.json` names in its own `ranking_key`
field. There is no call, no threshold and no direction label anywhere below.

The window resolved today's `amc` plus the next trading day's `bmo`. **Zero names
report tonight**; all four are Monday 2026-09-14 before the open. 4 of 4 confirmed by
the sweep, **0 phantom calendar rows**, 0 sessions left unsettled.

## The ranking

| # | ticker | company | `impact_sum` | `conviction` | clears floor (3.0) | control `priced_lean_pct` | findings | $/day turnover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **RFIL** | RF Industries | **+2.50** | 2.50 | no | +1.12% | 3 | $1.70m |
| 2 | **CODA** | Coda Octopus | **−4.10** | 4.10 | yes | +0.06% | 5 | $0.75m |
| 3 | **CSHR** | CoinShares | **−5.50** | 5.50 | yes | −0.25% | 5 | $1.06m |
| 3= | **HAIN** | Hain Celestial | **−5.50** | 5.50 | yes | +0.04% | 4 | $0.42m |

All four are rankable. CSHR and HAIN **tie** at −5.50, so the day is not a strict
order — it is three distinct positions over four names.

### Read this before you read the table

**The order is not the sign.** Below the conviction floor the sign of `impact_sum` is a
coin flip on the evidence so far — 53% over 38 resolved events. Above it, the *rank* of
conviction predicted whether the sign was right at ρ=+0.514 (permutation p=0.0015), and
above the median prediction the sign was right on 74% of events. So RFIL's +2.50 is a
position in an ordering, not a bullish view: it sits **below** the floor and its sign
carries no more information than a coin. CODA, CSHR and HAIN clear it.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. Regression
slope against the realised move is 0.72–0.76, median absolute error 6–7 points against a
realised standard deviation near 11, and it double-counts: the same fact reaching a
hunter through two documents enters twice. Three of today's four hunters flagged their
own source clusters in `independence` — CSHR's findings 1 and 2 share the FY2025 6-K,
RFIL's single largest finding is the diff between two of the company's own 10-Qs plus the
8-K exhibit filed the same day, and HAIN's covenant finding takes both its interest
figure and its EBITDA implication from one 10-Q. The cluster-max that used to collapse
those was measured as subtractive and removed, so the double-counting is in the number by
design.

## The control beat nothing today, because it produced almost the same answer

`-run_up_20d_pct` — one number off the sealed baseline, available before a single
subagent was spawned — ranks the day: RFIL (+1.12%), CODA (+0.06%), HAIN (+0.04%),
CSHR (−0.25%).

The hunt ranks: RFIL, CODA, CSHR=HAIN.

**Spearman between the hunt's order and the free control's is +0.95.** The two agree on
the top name, agree on second, and differ only in that the control separates HAIN from
CSHR at the bottom while the hunt ties them. Four names cannot support a correlation
statistic and this one should not be read as evidence either way — but it is worth
stating plainly that **on this day the hunt bought essentially nothing the run-up did not
already give away for free.** Over the six resolved runs the control ranks at ρ=0.335
against the hunt's raw 0.407, a gap whose confidence interval spans zero. The hunt has
still not been shown to beat it.

## What drives the top and the bottom

### Top: RFIL +2.50 — a deferred-tax release the filings pre-announced

The finding: RF Industries added deferred-tax-asset release language to its **Q2 FY2026
10-Q MD&A that is absent from the Q1 10-Q filed three months earlier** — "it is
reasonably possible that a reduction of a significant portion of the valuation allowance
may be appropriate in a future reporting period", with the cumulative-loss justification
recast into the past tense. The allowance is $4,521,000; on 11,424,572 diluted shares
that is roughly **$0.40 per share of potential one-time GAAP EPS against a $0.18
two-analyst consensus**. Sized +2.5 with a band of [0.0, +11.0].

Source: https://www.sec.gov/Archives/edgar/data/740664/000143774926020659/rfil20260430_10q.htm (2026-06-15)
Prior-quarter comparison: https://www.sec.gov/Archives/edgar/data/740664/000143774926008410/rfil20260131_10q.htm

**What the price already says.** RFIL is −22.49% over 20 days and −52% from its 52-week
high, and it is the only name of the four with a quoted option chain: 24.46% event-implied
move. The hunter declined that anchor and used the 9.27% historical median instead, on the
grounds that 297 total open interest and a **67%-of-mid ATM bid-ask spread** is a quote
rather than a market, and that 48.8% annualised 20-day realised vol independently implies
an earnings day near 9–10%. The baseline's own `warnings` field agrees the implied move is
indicative only. So the single most specific thing the market says about this name is
itself unreliable.

The honest weakness, which the hunter states: the conventional moment to release a
valuation allowance is the fiscal year-end assessment (31 October), not fiscal Q3, so the
low end of the band is a quarter that merely repeats the language.

### Bottom (tied): HAIN −5.50 — a compliance deadline five business days after the print

The finding: Hain's Nasdaq minimum-bid 180-day compliance date is **2026-09-21, five
business days after this print**, and the cure the company itself named in its 8-K —
"propose a reverse stock split to shareholders at its 2026 annual meeting" — cannot
complete in time, because the annual meeting is held in early November (the 2025 meeting's
item 5.07 8-K was filed 2025-11-05) and **no PRE 14A or DEF 14A has been filed**. The only
outcomes available in the week of the print are a transfer down to the Nasdaq Capital
Market for a second 180 days, or a delisting determination. Sized −2.0, band [−6.0, +1.0].

Source: https://www.sec.gov/Archives/edgar/data/910406/000119312526128948/hain-20260324.htm (2026-03-24)

The larger of HAIN's findings, at −3.0 each, are a **quiet 8-K of 2026-04-17** disclosing
a $5,000,000 retention plan — about 9% of the equity market cap — vesting 31 December 2026,
nine days after the 22 December debt maturity, which dates the board's own expected
resolution to year-end rather than to Monday
(https://www.sec.gov/Archives/edgar/data/910406/000119312526161777/hain-20260417.htm); and
an argument that the **binding covenant is the 2.00:1.00 interest-coverage test, not the
5.50:1.00 leverage test the CFO quotes**, with interest expense rising to $45.1m for the
nine months to 31 March from $38.4m a year earlier despite a $101m term-loan paydown.

**What the price already says.** Everything about the distress: $0.5951 a share, −72.3%
from the 52-week high, and the sub-$1 listing risk is general knowledge. That is why the
hunter sized the set at about a third of the 15.83% historical median rather than at it.
Its counterweight is the one positive finding on the name (+2.5): the −20.65% five-day
run-in has **no informational cause** — no 8-K of any item since 2026-05-11, no press
release since 2026-08-17, and HAIN is not among the S&P SmallCap 600 deletions announced
2026-09-04.

### Bottom (tied): CSHR −5.50 — a first SEC-format half against a trailing multiple

The largest finding (−3.0): CoinShares' own US ETF filing puts bitcoin at $58,391 on
30 June 2026 against $87,650 on 31 December 2025, and BRRR net assets down 32.3% despite
net creations, implying group AUM falling from $7.4bn at FY2025 toward roughly $5bn at the
balance-sheet date. At the disclosed ~170bp blended yield that is ~$50m of H1
asset-management revenue against $126.4m for FY2025 — which the hunter argues turns the
**3.0x trailing P/E retail data pages still display into roughly 12x**.

Source: https://www.stocktitan.net/sec-filings/BRRR/10-q-coin-shares-bitcoin-etf-quarterly-earnings-report-779e4f810fb8.html (2026-08-12)
Fee-rate and AUM base: https://www.sec.gov/Archives/edgar/data/2087587/000121390026050703/ea028870801ex99-1.htm (6-K, 2026-05-01)

**What the price already says.** Nothing usable. There is no option chain (368 total open
interest, no two-sided ATM), and — see the next section — **no earnings reaction history
at all**, so there is no anchor of any kind on this name. The 20-day run-up is +4.99%
against a −10.7% five-day. The hunter's offsetting positive (+1.5) is that bitcoin is
~$78,800 in early September against the $58,391 the release reports AUM at, a 35% recovery
after the balance-sheet date, and that the EGM the following morning seeks authority to
buy back up to 25% of shares.

## What could not be measured, and what nothing checked

**Nothing checked these findings for being factually wrong.** There is no adversary pass
and no second hunter — both removed 2026-09-09 after being measured as subtractive over
215 findings on six days. A factually wrong finding therefore enters the key at full size
and nothing in this run would have caught it. When the adversary last ran, on 2026-09-09,
it caught a covenant amendment misread by a year and a short-interest claim contradicted
by its own source. That is the accepted cost of one hunter per name, and it applies to
every number in the table above.

**The key is not reproducible to better than its own size.** While the stage still
double-hunted, twelve paired names came back with a **median gap of 2.40 points and four
of the twelve had opposite signs**, on a key whose typical magnitude is about 5. Nothing
re-measures that now. Today's spread from top to bottom is 8.0 points, so the ordering is
inside a few multiples of its own noise — and the CSHR/HAIN tie is not a real tie so much
as two numbers that happened to land on the same value.

**Almost none of the baseline was measured; nearly all of it was inferred.**

- **1 of 4 names has a live option chain** (RFIL), and its ATM bid-ask spread is 67% of
  mid, so the baseline itself marks the implied move indicative only. On a strict reading,
  **zero of four** names have a usable priced-move anchor.
- For CSHR, CODA and HAIN the "expected move" is a historical median, not a market
  expectation, and `priced_lean_pct` falls back to −0.05 × the 20-day run-up.
- **CSHR has no usable reaction history either.** The sweep verified that its three
  recorded "moves" are 6-K text matches on corporate-action filings — one of them confirmed
  as a notice of extraordinary general meeting, not an earnings release
  (https://www.sec.gov/Archives/edgar/data/0002087587/000121390026092804/ea0303148-6k_coinshares.htm).
  Its `baseline_history_trustworthy` is **false**, and the 4.46% expected move and 2.23%
  deadband derived from those three are meaningless. Its hunter was told so explicitly.
- **CODA has zero recorded reactions, and that is genuine absence.** The company does not
  file 8-K item 2.02 for earnings at all — it issues a press release and files the 10-Q the
  same day. The matcher correctly imported nothing wrong, but n=0 must not be read as a
  quiet stock; it means unmeasured. Its hunter built its own anchor from the 15 June price
  action (−5.6% on the Q2 print) and said so.

`edge_resolve.py` normalises by the expected move, so any normalised correlation reported
for this day is normalising three of four names on a historical median — or, for CSHR, on
a number with nothing behind it. Do not call it an implied-move measure.

**Sign balance: 3 of 4 hunts leaned negative, 1 positive.** That is the same tilt seen on
2026-08-31 (six of eight negative) and it is more plausibly an artefact of asking hunters
to find what the market has missed *into a print* than a fact about these four companies.
It is recorded here so that if it recurs across many days the hunter prompt can be
identified as generating pessimism rather than detecting it.

**Capacity is the binding constraint on this day, and it is in neither the scorer nor the
budget.** Turnover, spot × 20-day average volume: RFIL $1.70m, CSHR $1.06m, CODA $0.75m,
HAIN **$0.42m**. Every name is above the $200k execution floor and **not one is above
$5m**, where the resolved sample says the rule worked best (11/12 and +8.09% a trade at
$5m against 15/18 and +5.86% at $200k). The bottom-ranked name by turnover is also the
joint-bottom name by score, so whatever this ranking is worth, its extremes are the
hardest part of it to trade. On 2026-09-02 the single best-ranked name of the sample,
DLTH, moved +23.20% on $170k a day — a research result, not a signal.

## One further thing about this particular window

**Every name is Monday before the open, so the book is a weekend hold.** The entry is
today's close and the exit is Monday's close, which is the window `edge_resolve.py`
scores — the method is intact. But it is three calendar days of exposure over a weekend
rather than an overnight, and the whole day is a single-session `bmo` book, which under
`exit_mode: auction_split` means every leg exits into Monday's **closing** auction and
the "Close AMC" Routine has nothing to do.

## The standing caveat

**One day is an anecdote.** Four names cannot produce a meaningful rank correlation —
they cannot produce a meaningful anything. The pooled figure across many days is the
result, and today's contribution to it is four events. Over the six runs resolved so far
the stage's ranking has not been shown to beat minus the 20-day run-up, and on this day
it reproduced that control at ρ=+0.95. Read the table as one more day of sample, not as
a finding.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.
