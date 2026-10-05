# Stage E-P — 2026-10-05 amc + 2026-10-06 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.**
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1); none missing, no fallback.
Three names, one day: an anecdote, not a result.

## The panel

| # | ticker | session | selected | consensus_k | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge_pct | w_equal | w_precision_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | APOG | 2026-10-06 bmo | **yes** | 4 | 4/4 | +1.65 | +1.28* | +1.61* | +2.45* | +1.70* | +3.40 | 3.35 | 1.0 | 1.0 |
| 2 | RPM | 2026-10-06 bmo | no | 0 | 4/4 | +0.67 | +0.68 | +0.67 | +0.56 | +0.68 | +0.30 | — | 0 | 0 |
| 3 | LW | 2026-10-06 bmo | no | 0 | 3/4 | +0.18 | +0.21 | +0.15 | −0.19 | +0.27 | −0.10 | — | 0 | 0 |

`*` = in that member's own top 20%. Members' raw signed sizes: APOG +2.64 / +2.20 / +2.64 / +2.50;
RPM +1.40 / +0.91 / +0.60 / +1.00; LW +0.44 / +0.20 / −0.20 / +0.40 (opus5 / opus55 / sonnet55 / fable51).

### APOG (selected, 4 of 4)

Every member rests on the same item: the CFO's Q2 guide ("net sales slightly lower and adjusted EPS
lower year over year") repeats the Q1 wording word for word, and Q1 then came in at $0.57 against
roughly $0.41 expected and the stock rose 15.2% on 2026-06-26
(https://www.nasdaq.com/press-release/apogee-enterprises-reports-fiscal-2027-first-quarter-results-2026-06-26).
The Q2 consensus of $0.63 (MarketBeat, TradingView) is 36% below last year's $0.98 and only about 10% above Q1,
on a 2–4 analyst name, and the stock has given back the whole June move (−9.5% over 20 days, −26% from its high).
Kalwall (closed 2026-07-01, about two months, ~$14m) and the GroGlass fold-in (closed 2026-09-18, guide likely restated on the call) add to it.
**The strongest case against:** a peer, Tecnoglass, reported aluminum up 77% y/y and cut its guide on it
(2026-08-06), and the tariff/aluminum line is exactly what produced APOG's −13.9% in January 2026; this stock sells
a beat when the guide cracks (−4.4% in October 2025 on a beat with a cut guide). The revenue bar is disputed ($359.5m against ~$351m)
and one EPS figure ($0.84) could not be found on its cited page. Thin: ~252k shares a day, about $9m of turnover.
Recommended with a named reservation: the guide line on aluminum.

### Where the panel and the searcher disagree

- **RPM:** the searcher sums +0.30 (p12); all four judges lean higher (+0.60 to +1.40), on H.B. Fuller's same-months print (price ahead of raws, raised guide). None put it in its own top 20%.
- **LW:** the searcher sums −0.10 (its prose reported −0.4; the findings sum to −0.1 and the scorer uses the findings); three judges are mildly positive on washed-out positioning, Sonnet 5.5 mildly negative. A non-result either way.
- **APOG:** searcher and panel agree; the searcher's +3.40 is the only name above the 2.8 floor.

### Against stage E

Stage E's `research/2026/10/2026-10-05/edge/edge-scores.json` did not exist on `origin/main` when this note was
written (~17:35 UTC), so there is no overlap or Spearman ρ to report. Not waited for.

### What the numbers are not

`expected_edge_pct` is a shrunk in-sample prior from the judge-lab development names, not a forecast. The weights are
research; nothing trades them. Certainty (`p_up`) is recorded and decides nothing, because it did not predict on the
development names. Three names cannot produce a meaningful rank correlation.

## The searcher's own ranking (comparison arm)

| # | ticker | session | pre-lessons | impact_sum (key) | scaled | V2 | floor | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | APOG | 2026-10-06 bmo | +3.70 | +3.40 | +2.20 | +1.19 | yes | +9.46 |
| 2 | RPM | 2026-10-06 bmo | +0.60 | +0.30 | +0.48 | −0.04 | no | +6.23 |
| 3 | LW | 2026-10-06 bmo | −0.30 | −0.10 | −0.19 | −0.27 | no | +11.92 |

Pre-lessons, scaled and V2 are measured beside the key, not traded. Flags: APOG 4 positive / 2 negative findings netted;
RPM 4/4 netted, one finding outside the window; LW 4/4 netted, and the hunter expects the number (+4.0% vs bar) and the
stock (−0.2%) to go opposite ways. The free control orders the day LW > APOG > RPM; the hunt orders it APOG > RPM > LW.

- Below the 2.8 floor the sign is a coin flip on the evidence so far (53% over 38 events); `impact_sum` ranks, it does not size a move.
- Sign balance: 2 positive, 1 negative. Nothing checked the findings (no adversary, no second hunter); the key's reproducibility gap is a median 2.40 points with 4 of 12 pairs flipping sign when last measured.
- All 3 names had a live option chain (RPM's is thin: OI 385, ATM spread 57% of mid).
- Turnover (spot × 20-day volume, from the sealed baselines): APOG ≈ $9m, RPM ≈ $91m, LW ≈ $76m. No tradability check was run; this stage places no orders and does not call `alpaca_trade.py`.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on these.
APOG retail 42, search sparse, vol 24% · RPM retail 18, search sparse, vol 19% · LW retail 40, search 0.62x (quiet), vol 33%.

## Universe

3 confirmed-session names, all confirmed by the sweep from company releases. Five `time-not-supplied` rows checked
(`session_resolve.py`): none confirmed, none killed; AEHR checked by hand, no company date announcement found, not hunted.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market
positioning, guidance, macro conditions, and management commentary rather than reported results alone.
