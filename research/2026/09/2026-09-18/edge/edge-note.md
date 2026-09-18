# Edge hunt — 2026-09-18 amc + 2026-09-21 bmo

**There is no ranking today, because there is nothing to rank.** The gated window
resolved to **zero names**. Every one of the fifteen calendar rows across the two window
dates was either outside the window or stamped `time-not-supplied`, and a sweep over the
fourteen carried rows **confirmed none of them** — nine refuted on a positive,
company-sourced fact and five left genuinely unsettled. No hunter was launched, no
finding exists, `impact_sum` is undefined for every name, and no order was placed.

That is the answer, not a failure. A holiday, a Friday-into-Monday window and a
calendar full of vendor projections is a real day.

| | |
| --- | --- |
| calendar rows on the two window dates | 15 |
| in the window with a session Nasdaq supplied | **0** |
| `time-not-supplied` rows carried and checked | 14 |
| confirmed by a company source | **0** |
| refuted by a company source (phantom) | 9 |
| unsettled either way | 5 |
| session sourced for any row | 0 of 14 |
| hunters launched | 0 |
| names ranked | 0 |
| names clearing the conviction floor (3.0) | 0 |
| orders placed | 0 |

`edge-scores.json` names its ranking key as **`impact_sum`** — the hunters' signed
per-finding sizes in points of spot, added up. It carries all fourteen names with
`rankable: false` and the reason `no hunt`, which is the complete table the ranking test
needs; it has not been filtered and no cutoff has been applied to it.

## The complete table — fourteen names, none rankable

Sessions below are the **window-implied** session, not a sourced one. The sweep could not
source the reporting hour for a single row, so every session in this table is an
inference from the window and must be read as unsettled. That is not a detail: a
2026-09-18 `bmo` print already happened this morning, before the entry, and a 2026-09-21
`amc` print lands a full session after the exit — so for several of these rows an
unknown hour is a coin flip on whether the name is in the window at all.

| ticker | session (unsettled) | event | `impact_sum` | floor | tradable | control `-run_up_20d_pct` | why not ranked |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AIV | bmo | 2026-09-21 | — | — | yes · $3.16m · ok | +15.71 | phantom — in liquidation |
| CBAT | bmo | 2026-09-21 | — | — | yes · $0.76m · **thin** | −30.49 | phantom — redomiciled, now an FPI |
| CELU | amc | 2026-09-18 | — | — | yes · $15.82m · ok | −68.19 | phantom — delinquent, NT 10-Q filed twice |
| CHRN | bmo | 2026-09-21 | — | — | yes · $2.87m · ok | +17.18 | phantom — 31 May fiscal year, FY 10-K already filed |
| CURR | bmo | 2026-09-21 | — | — | yes · $2.23m · ok | +17.40 | unsettled (weak) — semi-annual FPI, H1 due Nov/Dec |
| ENLV | amc | 2026-09-18 | — | — | yes · $0.23m · **thin** | +48.93 | phantom — semi-annual, H1 filed 50 days ago |
| FRGT | bmo | 2026-09-21 | — | — | yes · $0.36m · **thin** | +52.44 | unsettled — half-year FPI, no H1 6-K filed |
| GRFS | bmo | 2026-09-21 | — | — | yes · $2.76m · ok | +8.14 | phantom — H1 out 2026-07-28/29, 9M carried for 11-10 |
| HTLM | amc | 2026-09-18 | — | — | **no** · $0.01m below floor | −1.92 | phantom — semi-annual, H1 is a late-Nov event |
| LNAI | amc | 2026-09-18 | — | — | **no** · $0.08m below floor | −5.46 | unsettled — FY 10-K due, but never files an item 2.02 |
| NB | amc | 2026-09-18 | — | — | yes · $9.10m · ok | +17.37 | unsettled — FY 10-K due, no pre-announcement |
| TRT | amc | 2026-09-18 | — | — | yes · $1.52m · ok | +2.91 | unsettled — last item 2.02 still 2026-05-14 |
| YYAI | bmo | 2026-09-21 | — | — | yes · $0.30m · **thin** | +42.03 | phantom — Nasdaq deficiency notice, 10-K delayed |
| ZONE | amc | 2026-09-18 | — | — | yes · $0.62m · **thin** | +13.11 | phantom — 309 days since last results filing |

The control column is printed because the note owes it every time, but **it should not be
read as a ranking today**. `-run_up_20d_pct` is defined for all fourteen names and would
happily order them — FRGT, ENLV and YYAI at the top — but there is no established
earnings event under any of those rows, so the control is ranking names on nothing.

## What refuted the nine

Each of these is a positive fact from a company source, not an absence of evidence.

- **GRFS** — Grifols published H1 2026 on 2026-07-28/29 and reports Q1 / H1 / 9M / FY; the
  9M release is carried for 2026-11-10.
  https://www.grifols.com/en/h1-2026-financial-results
- **CHRN** — ChronoScale (ex-Ekso Bionics, CIK 1549084) has a **31 May** fiscal year end and
  filed its FY 10-K on 2026-08-19. The 09-21 row is projected off the abandoned December
  cadence. https://data.sec.gov/submissions/CIK0001549084.json
- **AIV** — Aimco is in voluntary liquidation (plan adopted 2026-02-06) and has stopped
  issuing earnings releases; Q2 10-Q filed 2026-08-07 with no item-2.02 8-K.
  https://data.sec.gov/submissions/CIK0000922864.json
- **CBAT** — CBAK redomiciled to the Cayman Islands under a **new CIK** (8-K12B,
  2026-06-23) and is now a 20-F / 6-K foreign private issuer. The quarterly obligation the
  vendor is projecting no longer exists.
  https://data.sec.gov/submissions/CIK0002086841.json
- **ENLV** — Israeli semi-annual filer; H1 2026 6-K filed 2026-07-30, fifty days before the
  row. No semi-annual reporter repeats at fifty days.
  https://data.sec.gov/submissions/CIK0001596812.json
- **HTLM** — Singapore semi-annual filer that pre-announces every call; on its own pattern
  H1 lands in late November, and it has issued no announcement.
  https://www.nasdaq.com/market-activity/stocks/htlm/press-releases
- **CELU** — Celularity filed Form **NT 10-Q** for both Q1 and Q2 2026 and has not filed its
  FY2025 10-K. A company that has told the SEC in writing it cannot file on time is not
  releasing results three days from now.
  https://www.sec.gov/Archives/edgar/data/0001752828/000149315226038318/formnt10-q.htm
- **YYAI** — AiRWA disclosed a Nasdaq deficiency notice on 2026-08-28 for the delayed filing
  of its annual report.
  https://www.nasdaq.com/press-release/airwa-receives-expected-notification-deficiency-nasdaq-related-delayed-filing-annual
- **ZONE** — 309 days since the last results filing; the only recent corporate action is a
  name change completed 2026-09-01.
  https://www.nasdaq.com/press-release/zone-frontier-inc-announces-completion-corporate-name-change-2026-09-01

## The five that could not be settled

None of these reached `event_confirmed`, so none was hunted. Two are worth naming because
they are the only rows where a real filing could plausibly land inside the fortnight.

- **NB (NioCorp), `hunt_priority` 20.** 30 June fiscal year end; the last three FY 10-Ks went
  in on 2025-09-11, 2024-09-23 and 2023-10-06, so FY2026 is due in roughly this fortnight.
  But EDGAR shows no 10-K and no 8-K since 2026-07-02, no FY2026 preliminary-results
  release exists, and NioCorp has never reported without pre-announcing. Its precedent
  release hour is ~07:00 ET, which would put it **bmo on 09-18 — this morning, before the
  entry, and therefore outside the window entirely** even if it were real.
- **TRT (Trio-Tech), `hunt_priority` 12.** Re-checked from EDGAR rather than inherited from
  yesterday. Last item-2.02 is still 2026-05-14; the 2026-09-15 CERT / Form 25 / 8-A12B
  trio is an exchange transfer, not results. The FY2026 annual release is a late-September
  event and nothing names 09-18. **The filing-cadence prior reads "fits a cadence" on TRT
  for the second day running and is wrong for the second day running** — on 2026-09-17 that
  same prior was read as confirmation, 33% of equity went behind it, and TRT never
  reported. It is a reason to look. It is not evidence a print exists.
- **CURR**, **LNAI**, **FRGT** — carried at priority 3, 6 and 5. CURR's 86-day "fits" is
  wrong on its own demonstrated cadence (FY2025 announced 2026-05-01; the prior half-year
  not until 2025-12-01). LNAI has an FY 10-K due but has never filed an item-2.02, so its
  periodic report lands with no scheduled release and no session. FRGT's 150-day "fits" is
  a coincidence of the annual-to-interim gap.

## What this note owes the reader, every time

**The order and the sign are separate questions, and today there is neither.** There is no
`impact_sum` for any name, so nothing here is a bullish or bearish view on any of these
fourteen companies. For the record that governs days when there *is* a table: below the
conviction floor the sign of `impact_sum` is a coin flip on the evidence so far — 53% over
38 de-duplicated events — while the rank of conviction predicted whether the sign was
right at ρ=+0.514 (permutation p=0.0015). A reader who treats a small `impact_sum` as a
directional view is reading the table wrong.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. The same fact
often appears in two findings from two sources and adding both double-counts it — which is
exactly what the cluster-max was built to stop, and what the measurement then demoted.

**The control has its own line.** `-run_up_20d_pct` is printed above. On the six resolved
runs that free number — available off the sealed baseline before a single subagent is
spawned — ranked at ρ=0.335 against the hunt's raw 0.407, a gap whose confidence interval
spans zero. **The stage has not been shown to beat it.** Today the hunt produced no order
at all, so the control is unbeaten by default and that is not a result either way.

**Sign balance: zero hunts, so no count.** There is nothing to report, and the absence
should not be read as a balanced day. The reason this line exists is that six of eight
hunts leaned negative on 2026-08-31, which is more plausibly an artefact of asking hunters
to find what the market has missed into a print than a fact about eight companies; it is
only visible if every note records the count.

**Nothing checked any finding — and there were no findings to check.** There is no
adversary pass and no second hunter, so on a normal day a factually wrong finding enters
the key at full size and nothing in the run would catch it. That is the accepted cost of
nineteen names. It did not bind today.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four of
the twelve had opposite signs**, on a key whose typical magnitude is about 5. Nothing
re-measures that now. It is a standing caveat on every ranking this stage produces,
including the ones that look tidy.

**How much of the baseline was measured rather than inferred: none of it.** **Zero of the
fourteen names has a live option chain.** Every `priced_lean_pct` here is the fallback,
−0.05 × the 20-day run-up, and every "expected move" is a historical median rather than a
priced expectation. Worse, the sweep marked `baseline_history_trustworthy: false` on
**11 of 14** rows — six of them because `priced_in.py`'s 6-K text matching is picking up
operational announcements (FRGT's proof-of-delivery launch, CBAT's sodium-ion test,
CURR's Mint collaboration, GRFS's SPARTA readout) and presenting them as prior earnings
prints. Seven of the fourteen baselines carry `hist_n = 0` or 1. A ranking built on these
baselines would have been measuring very little.

**What the day would have cost to trade.** Nothing, because nothing was traded. For the
record the column carries: two of the fourteen (HTLM at $0.01m/day, LNAI at $0.08m/day)
are below the $200k turnover floor outright, and five more (ENLV $0.23m, YYAI $0.30m,
FRGT $0.36m, ZONE $0.62m, CBAT $0.76m) are **thin** — under $1m a day, where a broker's
limited-liquidity warning applies. So seven of fourteen names on this calendar would have
been untradeable or thin. That is the shape of a `time-not-supplied` day: the rows Nasdaq
cannot time are also, largely, the rows nobody trades.

**One day is an anecdote, and a zero-name day is not even that.** Five to twelve names
cannot produce a meaningful rank correlation, and this run contributes no events at all to
the pooled sample. The pooled figure across many days is the result; nothing here moves
it.

## Execution

`execution.enabled` is `true` and `orders.exit_mode` is `amc_open`. This was a live run,
not a dry one, and it placed nothing because no name cleared — indeed no name was ranked.

- **Exit (step 0b).** The account was already flat when the run started.
  `verify --scan --fix --submit` over 6 runs and 12 exit legs reported every leg `ok` with
  0.0 still held; `close --scan --submit` found nothing due. Yesterday's only position,
  TRT, had been sold that morning by the "Close AMC" Routine: 338 bought at 11.2592 on
  09-17, 338 sold at 11.4194 on 09-18, **+1.43% gross on the leg**. Note that this is a
  `bmo` leg going at the open, which is the defect CLAUDE.md records as fixed on 09-18 by
  `defer_to_session_run()`; the sale predates the fix taking effect.
- **Entry (step 7).** Zero names rankable, so zero met the benchmark. No order was placed,
  no name was refused on turnover or borrow, and the US session was still open throughout
  (the run finished well inside the 16:00 ET deadline) — so this is a genuinely empty book
  and not a missed entry.
- Account after the run: equity $11,582.19, cash $11,582.19, **no positions**.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.
