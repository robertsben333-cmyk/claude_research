# Portfolio simulator over the re-judge sample (2026-10-01)

Question: if each re-judge model's calls had been traded as a real book, day by day,
what would the account have done? It is a different question from the per-trade tables
in `../rejudge-four-models/`: it compounds, splits the equity over the day's names and
leaves the rest in cash.

Open `portfolio.html` from disk. Every control recomputes in the page: model (live hunt,
Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), ranking key, selection (absolute threshold, top
% per day, or a pooled top % over all scores), per-name cap, equal or score weighting,
and market.

`portfolio.py` rebuilds the page from `../rejudge-four-models/key.json` and its
`out-*-*.json` files, so a new re-judge arm shows up after a rerun.

Gross: no spread, commission or borrow. This is the research level, not the broker's
fills; the account's real trades are on the dashboard.
