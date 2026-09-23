# Stage EU — Europe ranking for 2026-09-24

Sealed 2026-09-23 13:44–13:49 UTC while the European markets were still trading, so every
sealed spot and every `run_up_*` is an **intraday price, not a close**. The resolver takes the
realised move from daily bars, close(2026-09-23) → close(2026-09-24), never from the sealed spot.
Ranking key: `impact_sum` (from `edge-scores.json`'s own `ranking_key`). Research only; no orders.

## The answer

**Nine of fourteen names are rankable, and none clears the conviction floor of 3.0.** It is a
thin, low-conviction UK-heavy day, and half of what the hunters established is about the
calendar rather than the companies.

| # | name | market | impact_sum | the finding driving it |
| --- | --- | --- | --- | --- |
| 1 | SLR Solaria | es | **+2.50** | last five in-session prints closed up on the day (+9.4, +5.3, +15.7, +8.7, +4.3) against Sabadell's Q2 EBITDA bar of ~€92m (+2.0); disclosed short book 5.61% rotating from discretionary to quant holders (+0.5) |
| 2 | HM_B H&M | se | +0.90 | family holding company Ramsbury buying on each of the last three report days, facing a 4.53% short that is building (+0.6); possible US tariff refund of up to SEK 1.5bn left out of consensus (+0.3) |
| 3 | RPI Raspberry Pi | uk | +0.70 | shares down ~41% since June while the company-compiled FY26 EBITDA consensus ($57.8m, 1 Sep) is uncut and no warning has gone out (+0.8); H1 above "at least $38m" (+0.2); short rebuild to 0.92% (−0.3) |
| 4 | ADOC Adocia | fr | 0.00 | no findings; **the print is after the close (18h00 CEST)**, so the bmo window holds nothing |
| 5 | CNE Capricorn | uk | 0.00 | **under a recommended all-cash DNO offer** at US$5.214; the interim cannot move a fixed price |
| 6 | VTY Vistry | uk | 0.00 | H1 loss pre-released on 8 Jul; the one real unknown (CEO-review charges) is unsized by any source |
| 7 | DFS | uk | −0.10 | Man Wah building a 10.18% stake (+0.4) against a freight headwind the company itself sized at £7–8m per $1,000/FEU (−0.5) |
| 8 | VBK Verbio | de | −0.50 | the only new number is the FY26/27 outlook; Verbio guides on spreads below the latest year's, against a single-aggregator EBITDA consensus of €266m (−0.8); possible dividend reinstatement (+0.3) |
| 9 | LIVE Living REIT | uk | −1.40 | **mechanical, not an edge**: the 1.4475p dividend goes ex on results day and the resolver scores unadjusted closes |

**Top — SLR +2.50.** The reaction pattern and the bar come from
https://www.bolsamania.com/capitalbolsa/noticias/empresas/solaria-resultados-1t-2026-baten-estimaciones--22513625.html
and Sabadell's preview
https://www.bolsamania.com/noticias/empresas/sabadell-pone-bajo-revision-precio-solaria-ve-dificil-cumpla-meta-2026--23601040.html
(*"El EBITDA alcanzaría aproximadamente los 92 millones… el beneficio neto (BDI) se situaría en torno a 55 millones de euros"*
— EBITDA about €92m, net profit about €55m). The date is the issuer's own CNMV notice ("publicará los resultados
correspondientes al primer semestre del año 2026 el próximo jueves 24 de septiembre"). No release hour
has been announced: the last four results filings came in-session, but two 2024 releases came after
17:20, so the hunter gives the window roughly a 20–25% chance of being empty. Its evidence is a reaction
pattern plus positioning, not a document that says the number beats.

**Bottom — LIVE −1.40.** https://www.investegate.co.uk/announcement/rns/living-reit-plc--live/dividend-declaration/9775261:
ex-date 24 September, the same session as the interims; on its last ten clean ex-dates the raw close fell a
median 1.58%. It is ranked only because `eu_resolve.py` reads unadjusted closes. Read the real bottom of the day
as **VBK −0.50**:
https://www.eqs-news.com/news/corporate/verbio-se-verbio-confirms-preliminary-ebitda-result-for-2024-25-and-expects-significant-recovery-in-fy-2025-26/0854b0da-73a1-42c5-b801-8d852a22a249_de
(*"Er legt dabei historische Markt-Spreads zugrunde, die unterhalb der im Geschäftsjahr 2024/25 erzielten Spreads liegen"*
— it bases this on historical market spreads below those achieved in FY2024/25).

## Not ranked, and why

The scorer prints all five as "hunter found no event on this date". That is accurate for one of them.
For the other four it overstates: they are **unconfirmed**, not disproven.

| name | market | what the hunter established |
| --- | --- | --- |
| ATE Alten | fr | **Wrong date.** Alten's AMF-filed H1 revenue release says *"Publication des résultats semestriels 2026 : 25 septembre 2026"*, after the close (~17:40 Paris), so the first session that can react is 2026-09-28. Neither window holds it. |
| KEFI | uk | No Notice of Results; last three interims came 29–30 Sep; vendor row has a placeholder time and a stale last-release date of 2022. Probably a phantom for the 24th. |
| ALTN AltynGold | uk | No Notice of Results; the vendor date is exactly 52 weeks after last year's release. The hunter puts ~30% on the 24th. |
| CHAR Chariot | uk | No Notice of Results; Fidelity gives only "Sep 2026". AIM deadline 30 Sep. A 1-for-25 consolidation approved on 22 Sep has no effective date yet, so the resolver must check an unadjusted Yahoo bar for a ~25x step. |
| RKH Rockhopper | uk | No Notice of Results (the company never issues one); vendor says the 24th, Quartr says 2 Oct. Plausible but unverified. |

`eu_resolve.py` settles all five against the 2026-09-24 Investegate and AMF day archives. The UK and France
are both markets where `event_occurred: false` is reachable.

## What the day is, before any pooled statement

- **Selection:** all 14 eligible names hunted (`selection.method`: at or under the cap of 20, so **no
  draw**). 46 scheduled, 32 dropped on the $200k floor or other filters. `by_market`: uk 9, fr 2, de 1, se 1,
  es 1; dk, no, fi, it and pl zero. **`market_concentration`: the UK is 64.3% of the day** (5 markets
  represented). This is one market's day.
- **Window assumed rather than known (`session_unresolved`):** SLR, ADOC, ATE, ALTN, CHAR, DFS, KEFI, RKH.
  The hunters settled several: ADOC is **amc** (the resolver's second window, close 24th → close 25th, is
  the one that matters), DFS is confirmed bmo by its own calendar, and ATE is not on the 24th at all.
- **Options:** null in all ten markets; Europe runs in the anchor-less regime that
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers:** uk (FCA, as of 09-19), de (Bundesanzeiger, 09-22), fr (AMF, 09-21), se (FI, 09-22)
  read; es unreadable. **5 of 14 names carry `anchor_covered: true`** (ATE, KEFI, RKH, RPI, VTY). Eight read
  a truncated zero and one (SLR) no register.
- **Three baseline positioning numbers are known to be wrong, and the baselines were left sealed:**
  - **HM_B** read 0.0, but the FI register carries "H M HENNES MAURITZ AB" at **4.53%**. The issuer-name join
    missed the vendor's "H&M Hennes & Mauritz AB Class B". That is a defect in `eu_positioning` and may hit
    other Nordic share classes.
  - **RPI** and **RKH** were read from a UK cache four days old. Live: RPI 0.92% and rebuilding, not 0.70%
    and covering; RKH 1.21% and covering, not building.
  - **SLR:** the hunter read the CNMV per-issuer short register from this container (`cnmv.es/portal/consultas/ee/posicionescortas`,
    5.61% across seven holders). That contradicts `CAPABILITY['es']`. The Spanish register should be
    re-probed before the "Spain has no register" line is repeated.
- **Spain and Poland:** 1 name (SLR, es), whose lean is the run-up and whose print cannot be confirmed or
  killed after the fact. **Germany:** 1 name (VBK), which cannot reach `event_occurred: false` either.
- **`history.basis` is an estimated cadence** for ADOC, ATE, HM_B, SLR and VBK: a scale, not a record of
  dates. The nine UK names are `observed_rns`.
- **`lean_vs_free_control_rho`:** no real European run has resolved. The only resolved files (09-16, 09-17)
  are validation runs on synthetic findings, and their per-market values (fr 1.0 on a handful of names)
  are not evidence. The lean's weights are priors borrowed from the US and Tokyo, measured nowhere in Europe.
- **Two data defects the resolver should know about:** Yahoo's LIVE.L closes around 8–10 Jul 2026 read
  0.768 (a pence/pounds error, which is why LIVE's baseline `realised_vol_60d_pct` reads 20132.93). And
  CNE's run-up is takeover premium, so the free control means nothing on that row.
- **Conviction floor:** 0 of 9 above 3.0. Over the whole US sample the sign was a coin flip below the
  floor, so nothing on this page should be read as a direction.
- **Controls:** `pre_lessons` present on 14 of 14, moved by the lessons file on 6. The `pre_local` language
  control is retired (0/0 by design since 2026-09-22); each hunter wrote a `language_note` instead. The
  Spanish (CNMV, Bolsamanía), Swedish (FI insider register, local previews) and Hong Kong Chinese (the Man
  Wah stake in DFS) sources each carried something the English ones did not.

One day is not a result. Nine rankable names, none above the floor, a third of the universe on
dates nobody has confirmed: this is noise until many days pool.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
