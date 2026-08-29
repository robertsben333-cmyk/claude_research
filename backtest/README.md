# backtest — does the preliminary read see anything?

A research project beside the daily pipeline. It does not write to `research/`,
`LEDGER.md` or `PREDICTIONS.*`, and no Routine fires it.

- `PLAN.md` — the design and the build order
- `FINDINGS.md` — what was actually probed, and what came back
- `scripts/` — the harness

Start here:

```bash
python3 backtest/scripts/events.py --start 2026-08-24 --end 2026-08-27 --min-cap 2e9
python3 backtest/scripts/anchors.py --ticker OKTA --date 2026-08-26 --session amc
python3 backtest/scripts/corpus_edgar.py --ticker OKTA --cutoff 2026-08-26 \
    --out backtest/events/OKTA-2026-08-26
python3 backtest/scripts/truth.py --ticker OKTA --date 2026-08-26 --session amc
```

`truth.py` and the outcome it computes are **harness-side only**. Nothing under
`events/<TICKER>-<date>/` except `filings/` and `anchors.json` may ever be visible to a
research agent.
