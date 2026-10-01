# Edge hunt — 2026-10-01 amc + 2026-10-02 bmo

**Answer first: one name in the window. It is NKE at `impact_sum` −0.38, which is under the 3.0 conviction floor. So there is nothing to rank and no book.** The ranking key is `impact_sum`, as `edge-scores.json` names it.

| ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control (−run_up_20d) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NKE | amc 2026-10-01 | −0.76 | **−0.38** | −0.22 | no | yes: $1,224m/day turnover, ok, Alpaca borrow available | +6.00 |

Pre-lessons and V2 are measured beside the key. They are not traded.

## What drives it

The sum nets five findings, two positive and three negative, and does not resolve between them. All five land on the **guidance** line or on **positioning**:

- **−0.45: North America wholesale sell-through was weak over June–August.** JD North America LFL was −6.8% and Foot Locker comps −3.6%, which points to a softer sell-in guide. Source: https://www.just-style.com/news/dicks-q2-fy26-result/
- **−0.40: the Street's Q1+Q2 EPS of $0.97 sits at the ceiling of Nike's own "flattish" framework.** Nike had already flagged that Q2 slows down. Source: https://s1.q4cdn.com/806093406/files/doc_financials/2026/q4/NIKE-Inc-Q4FY26-OFFICIAL-Transcript_-FINAL.pdf
- **+0.40: the tariff rate is lower than the guide assumed.** Section 122 was replaced on 2026-07-24 by a 10%/12.5% Section 301 tariff, against the 15% in the guide. Source: https://www.tariffstool.com/guides/section-301-replacing-section-122
- **+0.22: the bar was cut hard into the print.** Nine downgrades or target cuts landed in September, against a record short interest. Source: https://www.ad-hoc-news.de/boerse/news/corporate-news/nike-stock-falls-as-index-removal-and-analyst-downgrades-sharpen/70124363
- **−0.15: China retail is still falling.** Pou Sheng's August sales were −9%.

**What the price already says.** The straddle is 9.22%. Skew is +2.03, so mild downside protection is being paid for. The priced lean is −0.94%. The stock is −6.0% over 20 days and 1.5% above its 52-week low. Short interest is a record ~87M shares, ~7.3% of float (snippet only).

**The hunter's two numbers agree in sign and are both small.** `print_vs_bar_pct` is −0.3 and `expected_move_pct` is −0.38, with `p_up` 48. The bar is sourced (revenue ~$11.3bn, EPS $0.43–0.44).

Flags:
- 2 findings worth −0.30 fall after the exit window and are kept out of the key.
- The findings split 2 positive / 3 negative, so the sum nets opposing theses.

**Critical read:** NKE does not clear the floor, so there is no floor-clearer to recommend. At this size the sign is a coin flip on the evidence so far (53% over 38 events). Read −0.38 as "no edge found", not as a bearish view.

## Names not ranked

None in the window. The universe was 1 of 19 calendar rows. The 14 `time-not-supplied` rows were checked with `session_resolve.py`:
- 4 were killed, either as already reported or with filings in the last ten days.
- VFS was resolved to bmo 2026-10-01, which is outside the window.
- None was confirmed by a press release.
- 10 were carried but not added, mostly microcaps. HUBG reported 16 days ago.

The sweep confirmed NKE from the company's own release (results ~1:15 pm PT, after the close). It found 0 phantom rows.

## Standing caveats

- **The order and the sign are separate questions.** Below the floor the sign is a coin flip (53% over 38 events). Above it, the rank of conviction predicted sign-correctness at ρ=+0.514. `impact_sum` ranks; it is not a forecast of the move.
- **The control:** −run_up_20d_pct is +6.00. With one name, neither ranks anything. The hunt has not yet beaten that free control on the pooled sample.
- **Sign balance:** of 1 hunt, 1 leaned negative and 0 positive.
- **Nothing checked the findings.** There is no adversary pass and no second hunter.
- **The key's own reproducibility is poor.** Paired hunts had a median gap of 2.40 points, and 4 of 12 pairs had opposite signs.
- **How much was measured:** 1 of 1 names had a live option chain, so the baseline is option-anchored.
- **Cost to trade:** NKE is fully tradable, but there is nothing above the floor to trade.
- **This is the first US day under the loosened hunter core (2026-10-01).** The 3.0 floor was set on Opus 5's scale and has not been re-derived.
- **One day is an anecdote.** One name is not a ranking.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
