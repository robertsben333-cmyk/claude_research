# Stage E-P — 2026-10-08 amc + 2026-10-09 bmo

**This is stage E-P. Opus 5.5 searchers collected the evidence, a blind four-model panel judged it, and no orders were placed.**
All four members ran: Opus 5 (`claude-opus-5`, accepted), Opus 5.5, Sonnet 5.5 and Fable 5.1, each through its own `panel-judge-*` agent.
**No name was selected today.** One day is an anecdote, and four names are not a ranking test.

## Panel table

Every rankable name is listed. `*` marks a member that put the name in its own top 20%. A name is selected when 3 of the 4 members do.

| rank | ticker | session | selected | consensus_k | sign agreement | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge_pct | w_equal | w_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HOVR | bmo 10-09 | no | 2 | 4/4 neg | −1.23 | −1.04 | −1.02 | −1.43* | −1.50* | −0.50 | — | 0 | 0 |
| 2 | PKE | amc 10-08 | no | 0 | 4/4 pos | +0.98 | +1.09 | +0.85 | +1.08 | +0.89 | +1.30 | — | 0 | 0 |
| 3 | DAL | bmo 10-09 | no | 0 | 4/4 neg | −0.65 | −0.67 | −0.64 | −0.45 | −0.67 | −0.20 | — | 0 | 0 |
| 4 | ODC | amc 10-08 | no | 0 | 4/4 pos | +0.55 | +0.67 | +0.12 | +0.54 | +0.56 | +0.10 | — | 0 | 0 |

The raw member sizes (`impact_sum`, points of spot) were:
- **HOVR:** Opus 5 −2.0, Opus 5.5 −1.33, Sonnet 5.5 −1.6, Fable 5.1 −2.16.
- **PKE:** +2.1, +1.12, +1.2, +1.28.
- **DAL:** −1.3, −0.84, −0.5, −0.96.
- **ODC:** +1.3, +0.16, +0.6, +0.80.

The members agree on the sign of every name, and that agreement is uninformative: sign agreement alone carried nothing on the development names (127 of 151, 50%).

The searcher's own key placed no name above the 2.8 conviction floor. The largest was PKE at +1.30, which is p60 of Opus 5.5's reference.

## Selected names

None. HOVR came closest: Sonnet 5.5 and Fable 5.1 had it in their own top 20%, while Opus 5 and Opus 5.5 did not, so it reached k=2 of the 3 needed.

The case on HOVR, as the members' notes give it:
- The case rests on the $50m at-the-market program filed 2026-09-04 (424B5, https://www.sec.gov/Archives/edgar/data/1930021/000121390026097676/ea0304433-424b5_newhorizon.htm). That program is against a market cap of about $103m, for a pre-revenue company whose 10-K carries going-concern language.
- The 10-Q will show how many shares were sold after August 31.

The strongest case against:
- A non-cash warrant fair-value gain should make GAAP EPS look far better than the single-source −$0.08 bar. The reason is that the stock fell 43% from May 29 to Aug 31 (warrant line: https://data.sec.gov/api/xbrl/companyconcept/CIK0001930021/us-gaap/FairValueAdjustmentOfWarrants.json).
- Short interest is 4.6% of float at the 09-15 settlement, which is not crowded.

## Where the panel and the searcher disagree most

- **HOVR:** the panel (−1.33 to −2.16) is 3–4× the searcher's −0.50. Opus 5 also refiled the audit-chair resignation, which the searcher had dropped as `contradicted_by_document` on "no disagreement" boilerplate, at −0.3.
- **DAL:** every member is more negative than the searcher's −0.20. They weight the Q3 jet-fuel overrun (Gulf Coast jet about $3.84/gal against $2.71 on the guide-curve date; FRED DJFUELUSGULF) and a likely Q4/FY guide cut above the refinery, fare and peer-demand offsets. Opus 5 also read the EPS bar as disputed ($1.70–$2.25).
- **ODC:** Opus 5 sized it +1.3 against the searcher's +0.1. The driver is the 8-K accepted the evening of 2026-10-07: revolver up to $100m, Prudential shelf doubled to $150m, $100m acquisition cap removed. Opus 5 called it the most genuinely unpriced primary document in the pack.

## Against stage E

Stage E's `edge-scores.json` was on main by the end of this run, and both stages ranked the same four names.

| ticker | Stage E impact_sum | E-P searcher impact_sum | panel_score |
| --- | --- | --- | --- |
| ODC | +0.80 | +0.10 | +0.55 |
| PKE | +0.60 | +1.30 | +0.98 |
| DAL | −0.90 | −0.20 | −0.65 |
| HOVR | −0.90 | −0.50 | −1.23 |

- The Spearman ρ between stage E's `impact_sum` and `panel_score` is **+0.74**, on 4 names with a tie (DAL and HOVR, average ranks). On n=4 that means nothing.
- Neither stage cleared its own floor.
- Stage E's book bought nothing: it selects on |impact_scaled| ≥ 1.76, and its largest was HOVR at −1.26.

## What the numbers are not

- `expected_edge_pct` is a shrunk in-sample prior for selected names only, so it is empty today.
- The weights are research, and nothing trades them.
- `p_up` is recorded and decides nothing, because it did not predict on the development names.
- `impact_sum` ranks; it does not size, and it is not a forecast of the move.

The stage E standing caveats also apply:
- **Below the floor the sign is a coin flip on the evidence so far.** That is 53% over 38 events, and every name today is below the floor.
- **Nothing checked the findings for factual error.** There was no adversary pass.
- **The key is not reproducible to better than its own size.** In the paired hunts, the median gap was 2.40 points and 4 of 12 pairs had opposite signs.
- **Only two names had an option chain**, DAL (implied 6.42%) and PKE (8.56%, on a 47% spread and so indicative only).
  - ODC and HOVR have no options. Their baseline scale is a historical median.
- **Free control (`-run_up_20d_pct`):** it is printed in each baseline and was not beaten on any pooled sample since 09-08.
- **Sign balance:** the searchers came out 2 positive and 2 negative, and so did the panel.
- **Capacity:** DAL is a large cap. PKE, ODC and HOVR are thin names, and HOVR is a $1.5 stock.

## Context: retail, search and volatility (not used for selection)

These labels are context only. They do not rank, select, size or trade anything.

- **PKE:** retail 45 (no) · search sparse · vol 28 (no)
- **ODC:** retail 32 (no) · search failed · vol 26 (no)
- **DAL:** retail 26 (no) · search 3.57x on 10-07 (not quiet) · vol 26 (no)
- **HOVR:** retail 61 (yes) · search sparse · vol 37 (no)

## Not ranked

- **NRIX and GLDG.** Both are time-not-supplied rows carried by `session_resolve.py`. The second sweep found no company date notice for this window, so they were left unhunted. They were not shown to be phantoms.
- **CMMB** was killed (6-K filed 09-30).
- **HIFS** was dropped (no CIK).

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
