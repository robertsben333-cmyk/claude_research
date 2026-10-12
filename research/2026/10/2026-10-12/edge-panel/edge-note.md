# Stage E-P — 2026-10-12 amc + 2026-10-13 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.**
All four judges ran on their pinned models: Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1. None was missing and no fallback was used.
**No name was selected**: none reached 3 of 4 judges with the name in that judge's own top 20%. One day is an anecdote.

Window: nine names, all reporting 2026-10-13 bmo, all with a listed option chain. The sweep confirmed all nine from company sources.
Two are mega-cap banks reporting the same morning, and the day leans heavily on financials: JPM, GS, WFC and C, plus FBK, a regional bank.
Six `time-not-supplied` rows (UNTY, FNGR, RMCF, NCPL, BMRA, MSS) were checked with `session_resolve.py`: 0 killed, 0 confirmed, 6 carried. None of them was hunted.

## The panel

| rank | ticker | session | selected | k | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge | w_equal | w_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DPZ | bmo | no | 2 | 4/4 | −1.06 | −1.51* | −1.04 | −0.73 | −1.08* | −0.60 | — | 0 | 0 |
| 2 | GS | bmo | no | 0 | 4/4 | +0.60 | +0.49 | +0.72 | +0.25 | +0.72 | +0.90 | — | 0 | 0 |
| 3 | ACI | bmo | no | 0 | 3/4 | +0.56 | +0.65 | −0.38 | +0.47 | +0.93 | +0.90 | — | 0 | 0 |
| 4 | UNH | bmo | no | 0 | 3/4 | +0.38 | −0.86 | +0.33 | +0.42 | +0.79 | −0.10 | — | 0 | 0 |
| 5 | JPM | bmo | no | 0 | 4/4 | +0.33 | +0.65 | +0.30 | +0.30 | +0.36 | +0.55 | — | 0 | 0 |
| 6 | JNJ | bmo | no | 0 | 3/4 | −0.22 | −0.49 | −0.14 | +0.14 | −0.29 | −0.00 | — | 0 | 0 |
| 7 | FBK | bmo | no | 0 | 2/4 | +0.03 | +0.05 | +0.19 | −0.07 | +0.00 | +0.45 | — | 0 | 0 |
| 8 | C | bmo | no | 0 | 2/4 | +0.01 | −0.05 | +0.25 | −0.07 | +0.07 | +0.10 | — | 0 | 0 |
| 9 | WFC | bmo | no | 0 | 2/4 | +0.01 | −0.49 | −0.07 | +0.08 | +0.22 | −0.10 | — | 0 | 0 |

`*` means the name is in that member's own top 20%, judged against the member's recent history. `k` is how many members put it there.

## Selected names

None. The nearest was **DPZ** (k = 2, sign agreed 4 of 4, the most negative name for every judge):
- **The case for the short.** The Q3 comp laps the year's hardest quarter (+5.2%), so the +1.1% US comp bar needs about a 2.8-point acceleration on a two-year stack. Year to date, US comps are +0.5% and operating income +2.6% ex-FX, both against mid-to-high-single-digit FY guides, so neither guide line has room. It is the new CEO's first call. The April comp miss plus guide cut was the −8.8% day.
- **The case against.** Seven price targets were cut into the print and short interest fell 20.5% (to 7.9% of float at the 09-30 settlement), so the bar is already lowered. The stock ran +5.5% in the five days before. The July print rose on a comp miss. A World Cup lift inside fiscal Q3 is plausible and ignored by the stack arithmetic.
- **The read.** This is the July low-bar setup again. The +7.1 put skew already pays for the downside.

## Where the panel and the searcher disagree most

- **UNH.** The searcher was −0.10 and the panel +0.38. But Opus 5 is strongly negative (z −0.86), because consensus sits 20–35% above the company's own H2 cadence and KFF counts 228 county exits. The other three judges lean on the CFO's remark that the cost trend "has not dissipated". The panel's standard deviation of 0.62 is the widest of the day.
- **ACI.** The searcher was +0.90 and the panel +0.56. Opus 5.5 alone is negative (−0.38): it treats the Kroger comp slowdown and the leadership reset (new executive chair, interim CFO on his first call) as outweighing a 12.3% short base and the insider buys.
- **FBK.** The searcher was +0.45; the panel is flat (+0.03). The judges sized it as a non-result, and the 11.9% option-implied move was discarded by everyone (33 contracts of open interest, ATM spread 66% of mid).

## Against stage E

Stage E's `edge-scores.json` exists for the same nine names, from separate hunts and baselines. Spearman ρ between stage E's `impact_sum` and `panel_score` is **+0.53** on n = 9. Both put DPZ at the bottom and GS near the top. They disagree on ACI (stage E −0.50, panel +0.56). Neither stage has a name above the 2.8 conviction floor (stage E's DPZ at −2.10 is the closest).

## What the numbers are not

- **`expected_edge_pct`** is a shrunk in-sample prior, not a forecast. Nothing was selected, so it is null for every name.
- **The weights** are research; nothing trades them. This stage places no orders.
- **Certainty (`p_up`)** is recorded and decides nothing, because it did not predict on the development names.
- **The conviction floor.** No name clears 2.8 on the searcher's own key; the largest |impact_sum| is 0.90 (ACI and GS). Below the floor the sign is a coin flip on the evidence so far (53% over 38 events).
- **`impact_sum` is not a move forecast.** It ranks; it does not size.
- **Unchecked findings.** No adversary pass and no second searcher checked the findings. A factually wrong finding enters at full size.
- **Reproducibility.** The key is not reproducible to better than its own size: double-hunted pairs had a median gap of 2.40 and 4 of 12 had opposite signs.
- **Sign balance.** Five searcher hunts lean positive (ACI, GS, JPM, FBK, C), three lean negative (UNH, WFC, DPZ) and JNJ sits at zero.
- **Baselines.** All 9 have a live option chain, so the expected move is option-implied. FBK is the exception: its chain is unusable.
- **The free control.** `-run_up_20d_pct` has not been beaten by the hunt on the pooled sample. All nine baseline 20-day run-ups are negative, from JNJ −1.16% to GS −9.75%. The control therefore ranks GS first and JNJ last.
- **Capacity.** Every name is liquid; this is a large-cap day. Capacity is not the constraint, but it also means the most-covered names in the market, which is where the hunt has the least room.

## Context: retail, search and volatility (not used for selection)

These labels are context only.
- **Retail tilt** is below 50 on all nine (the highest are ACI 49 and FBK 35).
- **Search spike.** It is quiet (<1.0x) on GS, C, JNJ, UNH and WFC. It reads 1.32x on DPZ. The query failed for ACI and JPM and was too sparse for FBK.
- **Volatility.** 20-day realised volatility is below 58% on all nine (16–30%).

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
