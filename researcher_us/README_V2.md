# Stage E V2 — the shadow grounding layer

Designed by RobinBaumeister in PR #9; rebuilt on 2026-09-23 against that PR's review.
**V2 runs beside V1 and never instead of it.** V1's `impact_sum` ranks the note and is
the only key `alpaca_trade.py` places money on. V2 writes a second file,
`edge-scores-grounded.json`, and has to earn a role in `edge_resolve.py` first.

## The problem it answers

Hunters size findings in points of spot, and nothing maps those sizes onto what prices
do. V1's key has a regression slope of 0.72–0.76 against the realised move, and
`LESSONS.md` corrects past failures one rule at a time without ever fitting a scale.
PR #9's point: the one kind of news whose reaction *is* observable is news that was
public. Score it on the same scale, measure what the stock did, and fit the map.

## How it works

```
8-K on EDGAR, t0 = SEC acceptance time
        │  collect: text only, no price anywhere in the input
        ▼
shadow-scorer agent (Read/Write only, no web)  →  S_i, lands_on
        │  ingest: refused unless the input file still hashes to what was collected
        ▼
measure (only after a score exists)
        α_i,τ = ΔP_i,τ − β_i · ΔP_SPY,τ         β over 60 sessions BEFORE t0
        α̃_i,τ = α_i,τ / σ_i                     σ = 20-session realised daily sigma at t0
        ▼
fit     κ_τ,L = Σ α̃·S / Σ S²   with standard error, 95% interval and n
        ▼
runtime grounded_τ(j) = S_j · κ_τ,L_j · σ_live   σ_live off the sealed baseline tape
```

`researcher_us/scripts/edge_shadow_engine.py` does the first four steps and
`researcher_us/scripts/edge_grounded_score.py` the last. The ledger is
`researcher_us/analysis/shadow-ledger.json`; the scorer's inputs and scores are under
`researcher_us/analysis/shadow/`. The three rows PR #9 committed were not produced by
its own code and are gone; the ledger was filled on 2026-09-23 with 303 8-Ks for the 197
tickers of every run on disk (up to three per ticker since 2026-07-01), 302 scored blind.

## What the fit excludes

- **Any ticker CLAUDE.md names.** That file is loaded into every agent's context and it
  quotes outcomes (NAVN fell 18.4%, WLTH rose 8.0%, DLTH +23.20%). Two scorers reported
  it themselves. A score that says in its `basis` that it saw the name is excluded too.
  39 filings on the first fill.
- **One accession under two tickers** (BF.A/BF.B, LEN/LEN.B) counts once.
- **Two filings of one issuer whose horizon ends at the same moment** share one move, so
  they are one observation with their scores summed (CPRT results + acquisition, RENT
  results + rights offering).

## First reading, 2026-09-23

At `session_close` the scorer's sizes predict the real 8-K reaction: κ **0.365**, 95%
interval 0.224–0.506, pearson **0.40**, n 161. The model sizes public news with real
information. That is the calibration; it says nothing yet about the ranking.

## Forward only

**V2 is compared on runs it was grounded for BEFORE their first print, and on nothing
else** (operator's instruction, 2026-09-23). `edge_grounded_score.py` refuses to write
once a run's first print has passed, every file carries `forward: true` and
`first_print_utc`, and `build_v2.py` and `edge_resolve.py` read only files that say so.
The 17 historical runs were grounded once as of their own seal and then deleted: an as-of
matrix keeps the prints out of κ, but a run scored after its outcome is still a backtest,
and pooling it with forward runs would make the comparison unreadable. The ranking
comparison therefore starts with the first stage E run after 2026-09-23 and has no
number yet.

## What changed from PR #9, and why

| PR #9 | now | why |
| --- | --- | --- |
| Ledger of three hand-entered rows, `correlation: 1.0` at n=1 | Empty ledger, filled only by `collect → score → measure` | The repo's first rule: never fabricate a number |
| No ingestion, no scorer | `collect`, the `shadow-scorer` agent, `ingest` with a hash check | The pipeline in the README did not exist in the code |
| Scored when and how is unstated | Scorer has no web tools; `measure` refuses unscored items; filings before `min_event_date` skipped | A score written after seeing the price measures the model's memory |
| Normaliser = event implied move | Normaliser = realised daily σ, same definition as `priced_in.py` | An implied move for a financing 8-K does not exist; symmetry needs one quantity at both ends |
| Line with no κ falls back to the raw score | Pooled κ for the horizon; below `min_n` the whole day is `uncalibrated` | A raw 5 beside a grounded 1.8 is two units added together |
| Defaults of 1.0 / 3.0 when a baseline is thin | Name not grounded, reason stated | No invented denominators |
| β over the last 60 days of *today* | β over 60 sessions before t0 | Look-ahead |
| `1d` = next session's close | `1d` = last price at or before t0+24h, intraday | It was `next_close` under another name |
| `session_close` for an amc filing ran backwards in time | First regular close after t0, from the last close before t0 | Same window `edge_resolve.py` uses for a print |
| Missing SPY subtracted 0 and read `ok` | `no_benchmark`, excess null | A missing number never reads as zero |
| κ fitted on today's ledger for any run | κ refitted as of the run's baseline seal | An item-2.02 8-K of a hunted name IS its print |
| Output unsorted, unread by the resolver | Sorted `rank_v2`; `edge_resolve.py` ranks V2, V1 and a vol-only control | V2 cannot beat V1 if nothing scores it |

## The nine horizons

All measured from one reference: the price at t0 when t0 falls inside the regular
session and 5-minute bars reach it, otherwise the last regular close before t0.
`5m`, `15m`, `60m` and `1d` start from the price at t0, extended hours included.

| τ | end point |
| --- | --- |
| `5m` · `15m` · `60m` | last 5-minute bar ending at or before t0 + Δ |
| `session_close` | first regular close after t0 — **the primary horizon**, the edge window |
| `next_open` | first regular open after t0 |
| `next_close` | second regular close after t0 |
| `1d` | last 5-minute bar at or before t0 + 24 h |
| `5d` · `1m` | 5th and 21st regular close after t0 |

Yahoo serves 5-minute bars for 60 days, so a filing measured later than that has no
intraday horizons (`intraday_window_passed`). A number once measured is kept on
re-measure for that reason.

## Three scores per name

Every stage E note carries three scores side by side: **pre-lessons** (the hunters'
sum before `LESSONS.md`), **post-lessons** (V1's `impact_sum`, the key, and the only
one the book trades on) and **V2** (`impact_sum_grounded`, or `uncalibrated`).
`edge_grounded_score.py` prints that table and `edge_resolve.py` ranks all three
against the same realised move, per day and pooled within days.

## The test V2 has to pass

`edge_resolve.py` reports three rankers against the same realised move:
`spearman_vs_raw_move` (V1), `spearman_v2_grounded` (V2) and `control_vol_only`
(V1 × σ, no κ). When κ is close to one number across lines, V2 is rank-identical to
the vol-only control, so **V2 has added something only where it beats that control**.
Beating V1 alone can be pure volatility, which this repo has already measured as
the thing that moves ranking-by-size without skill. It also reports the calibration
slope of each key: V2's claim is that its unit is percent of spot, so its slope
should sit near 1.

## What it does not fix

- **t0 is the filing, not the wire.** Companies usually wire the release minutes
  before they file, so t0 is an upper bound and the 5m horizon is the most
  contaminated. Nasdaq's press-release API answers 301 from here; tighten the
  definition when a timestamped wire source is reachable.
- **Two populations.** Shadow items are public filings; runtime findings are claimed
  to be unpriced. κ calibrates the scale of the model's sizes, and it is an
  assumption, not a measurement, that the scale carries over. `lands_on` per line is
  where the populations are most alike (item 2.02 against `reported_quarter`).
- **Blindness is instructed, not enforced.** The scorer's Read tool can open other
  files in the tree. Its definition forbids it; nothing stops it.
- **One scorer per run.** It is outside the hunt budget, runs after the book is
  placed, and is the first thing shed.

## Running it

```bash
# every stage E run, right after edge_score.py (skill step 5b)
python3 researcher_us/scripts/edge_grounded_score.py --run <RUN>/edge

# after the book is placed (skill step 6c)
python3 researcher_us/scripts/edge_shadow_engine.py collect --from-run <RUN>/edge
python3 researcher_us/scripts/edge_shadow_engine.py brief -o <RUN>/edge/shadow-brief.json
#   -> one shadow-scorer agent on that brief
python3 researcher_us/scripts/edge_shadow_engine.py ingest
python3 researcher_us/scripts/edge_shadow_engine.py measure
python3 researcher_us/scripts/edge_shadow_engine.py fit
python3 researcher_us/scripts/edge_shadow_engine.py status
```

Settings are in `config/pipeline.yaml` under `edge_v2`. `scripts/smoke_test.py`
covers the arithmetic, the horizons, the seal and the refusals offline.
