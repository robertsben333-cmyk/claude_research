# Stage E-P — 2026-10-07 amc + 2026-10-08 bmo

**This is stage E-P: Opus 5.5 searchers (`unpriced-searcher`) and a blind four-model judging panel. It places no orders.**
All four judges ran as their named agents on their pinned models: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. None was missing and none needed a retry.
One day is an anecdote. The panel rule was chosen on development names in `research/analyses/judge-lab/`. Only pooled forward days can judge it.

Ten names were in the window. The sweep confirmed 10 of 10 from company sources, with 0 phantoms and 0 unsettled sessions. All 10 were searched, all 10 are rankable, and all 10 went to the panel.

## The panel table

`k` is the number of members that put the name in their own top 20% on the panel's side. `*` marks a member z inside that member's own top.

| rank | ticker | session | selected | k | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge_pct | w_equal | w_prec_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **RELL** | amc 10-07 | **yes** | 4 | 4/4 | +2.58 | +1.80* | +2.93* | +2.69* | +2.47* | +5.00 | +3.35 | 1.0 | 1.0 |
| 2 | BYRN | bmo 10-08 | – | 2 | 4/4 | +0.98 | +0.70 | +0.51 | +1.26* | +1.63* | +2.10 | – | 0 | 0 |
| 3 | APLD | amc 10-07 | – | 1 | 4/4 | +0.93 | +0.96 | +0.82 | +1.17* | +0.90 | +2.30 | – | 0 | 0 |
| 4 | LEVI | amc 10-07 | – | 0 | 4/4 | +0.98 | +1.05 | +1.14 | +0.58 | +0.90 | +1.00 | – | 0 | 0 |
| 5 | RGP | amc 10-07 | – | 0 | 4/4 | −0.62 | −0.63 | −0.60 | −0.63 | −0.61 | −0.60 | – | 0 | 0 |
| 6 | HELE | bmo 10-08 | – | 0 | 4/4 | +0.55 | +0.80 | +0.45 | +0.54 | +0.57 | +0.80 | – | 0 | 0 |
| 7 | ANGO | bmo 10-08 | – | 0 | 3/4 | +0.28 | −0.39 | +0.21 | +0.45 | +0.35 | +0.50 | – | 0 | 0 |
| 8 | PEP | bmo 10-08 | – | 0 | 4/4 | +0.23 | +0.20 | +0.18 | +0.27 | +0.33 | +0.50 | – | 0 | 0 |
| 9 | NG | bmo 10-08 | – | 0 | 3/4 | −0.14 | +0.00 | −0.10 | −0.45 | −0.18 | −0.50 | – | 0 | 0 |
| 10 | TLRY | bmo 10-08 | – | 0 | 2/4 | −0.01 | −0.33 | −0.16 | +0.36 | +0.15 | +0.80 | – | 0 | 0 |

Rank is `panel_score.py`'s own order. It sorts by consensus before score, so BYRN and APLD sit above LEVI.

## The one selected name: RELL (long side, 4 of 4)

**What the members' notes name.** All four rest on two items from company documents:

- **Backlog.** Backlog was $164.4m (+22.5% YoY, "faster turns"), against a FQ1 revenue bar of about $58.5m. That bar is about 12% below the $66.2m just reported, and EPS is $0.09, set by 2–3 analysts. The figures are in the 2026-08-26 Midwest IDEAS deck, https://www.rell.com/webfoo/wp-content/uploads/2026/08/RELL-Q4-FY26-Investor-Presentation-Midwest-IDEAS-Conf-Final.pdf.
- **Wafer-fab line.** The same deck, presented three days before the quarter closed, says semiconductor wafer-fab sales "remain strong".

On top of those two items, the members add:

- the last two beats moved +21% and +23%;
- short interest is 9.22% of float, about 9 days to cover (https://equibles.com/stocks/rell/shortinterest, 2026-09-15).

**The strongest case against.**

- **Bar.** The revenue bar has one source only.
- **Insider selling.** Six insiders sold about $2.57m during the quarter, including the CFO at $21.61 on 2026-08-04 (https://www.marketbeat.com/instant-alerts/richardson-electronics-nasdaqrell-cfo-robert-ben-sells-9000-shares-of-stock-2026-08-06/). Opus 5 sized this materially more negative than the searcher did.
- **Backlog is public.** The backlog was released with the FQ4 print.
- **Concentration.** One PMT customer is 14% of sales.
- **Implied move.** The implied move is about 13%, so a beat may be partly expected.

RELL is the only name above the 2.8 conviction floor in this searcher's own scores, and stage E's own hunt put it top as well (+4.8).

**Tradability.** Turnover is about $2.3m a day (spot $18.90 × 20-day average volume 122,823), so liquidity is `ok`. The chain is usable. The session is amc today.

## Where the panel and the searcher disagree most

- **TLRY.** The searcher has +0.80; the panel has −0.01 with signs split 2/4. Opus 5 made the 8.5% dilution the dominant item.
- **ANGO.** The searcher has +0.50. Opus 5 is negative (−0.78 impact) on the hard thrombectomy comp and the segment build; the other three are mildly positive.
- **LEVI.** The searcher has +1.00, its fourth-highest. Opus 5 and Opus 5.5 put it near their tops, on Section 301 rates below the guide's 30%/20% tariff assumption. No member put it inside its top 20% on the day, so k = 0.
- **BYRN.** The searcher has +2.10, second. Two members (Sonnet 5.5 and Fable 5.1) put it in their top; the two Opus judges did not. Opus 5 weighed the −16.5% September web traffic heavily.

## Stage E comparison

Stage E's `edge-scores.json` ranks the same 10 names, so the overlap is 10 of 10.

| comparison | Spearman ρ |
| --- | --- |
| stage E `impact_sum` vs `panel_score` | **+0.49** |
| stage E `impact_sum` vs this run's searcher `impact_sum` | +0.59 |
| this run's searcher vs panel | +0.91 |

Both stages put RELL first and alone above the floor. The largest cross-stage gaps are BYRN (E −0.4, E-P searcher +2.1) and HELE (E −0.6, E-P +0.8). Two Opus 5.5 hunts of the same names disagreeing in sign on two of ten is the reproducibility caveat again.

## What the numbers are not

- `expected_edge_pct` (+3.35 on RELL) is a shrunk in-sample prior from the judge lab, not a forecast.
- The weights are research. Nothing trades them, and this stage places no orders.
- `p_up` is recorded and decides nothing, because it did not predict on the development names.
- `impact_sum` ranks the names; it does not size the move. Below the floor its sign is a coin flip on the evidence so far (53% over 38 events).

## Standing notes (stage E's)

- **Sign balance.** In the searcher's key, 8 of 10 names lean positive and 2 negative (NG, RGP). Every hunt leaned only mildly.
- **Free control.** The control is `-run_up_20d_pct`. Ordered by it: NG +20.86, APLD +11.68, TLRY +11.16, PEP +9.16, HELE +8.53, ANGO +6.53, RGP +3.75, LEVI +2.95, BYRN −5.57, RELL −8.50. Its order is close to the inverse of the panel's: it puts the selected name, RELL, last. The stage has not yet beaten this control on pooled days.
- **Nothing checked the findings.** There is no adversary pass and no second searcher. The judges re-sized the evidence but verified no fact.
- **Reproducibility.** The key is not reproducible to better than its own size. Twelve historical double-hunt pairs had a median gap of 2.40 points, and four of the twelve had opposite signs.
- **Measured baseline.** 8 of 10 baselines rest on a live option chain. BYRN and RGP have unusable chains and fall back to a median historical reaction. BYRN's reaction history was flagged untrustworthy by the sweep, because it mixes preliminary-revenue releases with full prints.
- **Capacity.** Every name clears the $200k turnover floor. The smallest are BYRN (about $1.1m a day) and RGP (about $1.3m a day). No order was placed and borrow was not checked: this stage does not call `alpaca_trade.py`.
- **V2 grounded.** `edge_grounded_score.py` grounded 10 of 10 names on 186 ledger observations, before the first print. It was run on this directory only, and the shadow ledger was not fed.

## Context: retail, search and volatility (not used for selection)

These labels are context only. The panel and the scorer decide nothing on them.

| ticker | retail tilt | search | 20d vol |
| --- | --- | --- | --- |
| RELL | 52.5 (≥50) | sparse | 42.9 |
| APLD | 62.9 (≥50) | 1.32x (not quiet) | 70.8 (≥58) |
| BYRN | 71.7 (≥50) | sparse | 45.8 |
| LEVI | 28.0 | sparse | 21.0 |
| HELE | 56.9 (≥50) | 0.38x (quiet) | 41.1 |
| TLRY | 69.6 (≥50) | sparse | 41.1 |
| ANGO | 53.1 (≥50) | sparse | 31.3 |
| PEP | 12.7 | 1.23x | 13.7 |
| NG | 60.8 (≥50) | failed | 53.5 |
| RGP | 62.7 (≥50) | sparse | 36.8 |

*This is a forecasting exercise over public information, not investment advice.*

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
