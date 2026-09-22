# researcher_canada — stage CA, the Canadian researcher

The same question as stages E, J and EU, asked of Toronto: **is there anything in this
company's print the market has missed, and how does it rank against the other names
reporting today.** One signed number per company, no call, no threshold, no direction
label, scored by the shared scorer (`researcher_us/scripts/edge_score.py`, unchanged).

**It places no orders.** There is no execution block, no broker call, and there must not
be one. Alpaca carries no Canadian venue and execution would be a separate build.

## Why Canada, and it is not the calendar

Canada is the only market in this repo where the **option-anchored and anchor-less
regimes run inside one day's names**. The Montréal Exchange lists options on 360
underlyings, covering 96% of names above $25m a day and 10% below $1m, while the CIRO
short register covers 87–88% of *every* turnover band. So a Canadian day splits into an
arm anchored exactly as a US name is and an arm anchored as a Japanese or European one,
in the same market, on the same dates, through the same scorer.

`archive/backtest/FINDINGS.md` §33 priced the anchor-less regime at ρ=+0.073, p=0.45 over
104 events and could not separate the anchor from the market it was measured in.
`ca_resolve.py`'s `by_anchor_covered` holds the market fixed and separates them. The
ranking is the by-product; that comparison is the reason the stage exists.

## What the market gives, and what it does not

Both official surfaces are shut from this container and stay shut on the eight-try France
protocol: `sedarplus.ca` is a Radware 403 (0/8), `ciro.ca` a Cloudflare interstitial
(0/8), `sedi.ca` the same 403. Everything reaches the stage through TMX Group's own
unauthenticated GraphQL endpoint and through `m-x.ca`. `SOURCES.md` has the measurement;
this is what it means for the stage.

| | measured | what the stage does about it |
| --- | --- | --- |
| Short register | 87–88% of every band, **no history, no date argument** | level is sealed; the change accumulates from `analysis/short-register/<date>.json` |
| Option chain | 360 underlyings, **zeroed bid/ask outside 09:30–16:00 ET** | the implied move is **refused** unless the chain quotes two-sided |
| Calendar | two vendors, **disagree on 172 of 277 forward dates** | reconciled and graded; disputed dates are not hunted |
| Event shape | **a third of the universe reports by filing, not release** | `filing_only` issuers are screened out of the draw |
| Consensus EPS | **absent from every source here** | the hunter sources the bar and caps its sizes when it cannot |
| Reaction history | real dated releases, years deep | `basis: "observed"`, not Japan's cadence estimate |
| Vendor concentration | register, filings, archive, calendar and tape are **one stack** | one outage is one failure, not four; the note must say so |
| Phantom rate | **1 in 140**, against the US `time-not-supplied` 20 of 20 | confirmation runs in code, no sweep agent |

## The pipeline

```bash
python3 researcher_canada/scripts/ca_universe.py  -o   <RUN>/universe.json
python3 researcher_canada/scripts/ca_priced_in.py --universe <RUN>/universe.json --out-dir <RUN>/baselines
#   spawn one `unpriced-hunter-ca` per name, in waves        -> <RUN>/hunts/
python3 researcher_us/scripts/edge_score.py       --run <RUN>
python3 researcher_canada/scripts/ca_resolve.py   --run <RUN> -o <RUN>/canada-resolved.json
```

`<RUN>` is `research/<YYYY>/<MM>/<DATE>/canada/`. The skill
(`.claude/skills/researcher-canada-hunt/`) is the workflow; the Routine prompt is in
`routine-prompts/canada-hunt.md` and the budget block is `canada_hunt` in
`config/pipeline.yaml`.

## Validated end to end, on synthetic findings

2026-08-13, 40 scheduled names above the $200k floor, cap 20, 19 sealed and hunted with
**random findings** (`ca_synth_hunts.py`). The whole chain ran: universe → baselines →
shared scorer → resolver. What it establishes and what it does not:

- **Establishes**: the contract is right. The shared scorer reads a Canadian run
  unchanged and ranked 19 of 19; the resolver confirmed **19 of 19 releases by their real
  wire headline** and measured the window off TMX's own tape; both sessions windowed
  correctly. Random findings ranked at **ρ = −0.146, p = 0.55**, which is what random
  findings should do, and that is the null any real Canadian number has to beat.
- **Establishes**: the lean is a real rival to the free control.
  `lean_vs_free_control_rho` came out at **0.125**, not 1.0. That is the defect that
  makes Spain and Poland structurally unable to beat their own benchmark, and Canada does
  not have it.
- **Does not establish anything about the hunt.** No real hunter has run. Nothing has
  resolved. The per-component correlations in that file (`short_squeeze` 0.456,
  `days_to_cover` 0.434 on 17 names) are computed off real baseline data against a real
  realised move, but they are one day, chosen for validation, and every weight behind
  them is a prior carried over from Tokyo.
- **Does not test the option arm.** The run sealed with Toronto shut, so all 19 names
  landed on the register arm and `by_anchor_covered.options` is empty. The two-sided
  path is covered by `ca_smoke.py` against a fabricated chain instead, which proves the
  arithmetic and not the feed.

## Three things still unsettled

1. **Does `register_business_date` move daily?** Every reading on 2026-09-22 was stamped
   2026-09-21, which fits neither of CIRO's twice-monthly as-of dates. Running the stage
   answers this on its own: the snapshots accumulate.
2. **Which calendar is right?** `by_date_confidence` in the resolved files answers it
   from runs rather than argument. If `vendor_only` rows do not resolve, a quarter of the
   universe is noise.
3. **Does a Toronto-session seal actually produce two-sided quotes?** One weekday run at
   18:30 UTC settles it. Until then every run is a register-arm run and the stage's
   headline reason for existing is untested.

## Files

```
SOURCES.md                    what is reachable in Canada, measured, with the caveats
scripts/ca_sources.py         the client: TMX GraphQL + Montreal Exchange, plus CAPABILITY
scripts/ca_market.py          sessions, TSX holidays, event-shape and announcement rules
scripts/ca_universe.py        calendar reconciliation, floors, share-class fold, the draw
scripts/ca_priced_in.py       the sealed baseline; two anchor arms
scripts/ca_resolve.py         confirm, measure, rank — and rank the arms apart
scripts/ca_measure.py         reproduces every number in SOURCES.md
scripts/ca_synth_hunts.py     synthetic findings, for validating the chain only
scripts/ca_smoke.py           plumbing checks, no network, no model calls
LESSONS.md                    deliberately empty until a Canadian run resolves
analysis/validation-2026-08-13/   the end-to-end validation run above
analysis/short-register/      one snapshot per run; what makes the change computable
routine-prompts/canada-hunt.md    the text for the Routine, kept in step by hand
```
