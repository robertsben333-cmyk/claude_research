# Stage EU — Europe researcher, event date 2026-11-13

Sealed 2026-11-12 ~14:45 UTC (15:45 Amsterdam), while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The scored window is close(2026-11-12) → close(2026-11-13) for bmo names, measured by `eu_resolve.py` from daily bars. Ranking key: `impact_sum` (from `edge-scores.json`). Conviction floor: 2.8.

**Answer first:** no name reaches the 2.8 floor; the day is small on both sides. The hunters' top is **MRL +1.40** and bottom **TRE −1.30**. The four-model panel **selects no name** (no name has 3 of 4 judges in their own top 20%). The two highest `panel_pct` readings are both short and both 72 with all four judges: **MARR** and **TRE**, which is what the IBKR handoff carries at the >= 70 rule. Over the whole US sample the sign below the floor was a coin flip. One day is not a result.

## Ranked table

| # | ticker | mkt | session | impact_sum | abs_move | p_up | impact_scaled | anchor | history |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MRL | es | bmo (before open, merca2 + last year's 08:22 story) | +1.40 | 4.0 | 54 | +0.32 | no (no register) | est. |
| 2 | IRLAB_A | se | bmo (07:00 per invitation) | +1.00 | 15.0 | 53 | +0.90 | no | est. |
| 3 | IP | it | in-session ~15:00 CET | +0.65 | 5.0 | 55 | +0.50 | no | est. |
| 4 | ELN | it | bmo? → **amc** likely | +0.60 | 5.0 | 55 | +0.50 | no | est. |
| 5 | LAND | uk | bmo | +0.60 | 4.0 | 52 | +0.16 | yes (3.80%) | observed_rns |
| 6 | AFG | no | bmo (07:00 CET) | +0.50 | 5.0 | 55 | +0.50 | no | observed_newsweb |
| 7 | ASMDEE_B | se | bmo (07:00 CET) | +0.40 | 7.0 | 54 | +0.56 | no | est. |
| 8 | G | it | bmo (07:00 CET) | +0.40 | 2.6 | 57 | +0.36 | no | est. |
| 9 | BAVA | dk | bmo (pattern) | +0.30 | 4.0 | 52 | +0.16 | yes (2.31%, DK 0.1% threshold) | est. |
| 10 | FAA | de | bmo (pattern) | +0.30 | 6.5 | 49 | −0.13 | no | est. |
| 11 | TIP | it | bmo? → **amc** likely | +0.30 | 2.5 | 52 | +0.10 | no | est. |
| 12 | COG | pl | bmo? → **amc** likely | +0.20 | 7.0 | 49 | −0.14 | no (no register) | est. |
| 13 | NA9 | de | bmo (pattern) | +0.20 | 1.0 | 52 | +0.04 | no | est. |
| 14 | AEIN | de | Q3 pre-released 12 Nov 13:17 CET | +0.10 | 3.0 | 52 | +0.12 | no | est. |
| 15 | ERG | it | in-session (11:00–13:00 pattern) | −0.10 | 3.2 | 47 | −0.19 | no | est. |
| 16 | ETH | it | bmo? → **amc** likely (20:30 pattern) | −0.40 | 6.0 | 45 | −0.60 | no | est. |
| 17 | MARR | it | in-session ~15:30–16:15 CET | −1.10 | 5.0 | 40 | −1.00 | yes (1.31%) | est. |
| 18 | BC8 | de | bmo | −1.20 | 3.8 | 45 | −0.38 | yes (0.54%) | est. |
| 19 | TRE | es | bmo or evening 12 Nov (both inside) | −1.30 | 7.0 | 46 | −0.56 | no (no register) | est. |

`impact_scaled` = (2·p_up/100 − 1)·abs_move is the hunter's second, separate measurement. It is not the key and nothing is ranked on it. FAA and COG differ in sign between the two numbers (findings sum small positive, p_up just under 50).

**Not ranked:** DIA (uk). The vendor's 2026-11-13 date is a **phantom**: Dialight's H1 FY27 interims came out by RNS on 2026-11-10 07:00 (https://www.investegate.co.uk/announcement/rns/dialight--dia/half-year-financial-report/9866388); 13 Nov is only an Investor Meet Company presentation of those results (https://www.investegate.co.uk/announcement/rns/dialight--dia/investor-presentation-via-investor-meet-company/9862955). The UK archive is reachable, so the resolver can record `event_occurred: false`.

**Session corrections from the hunters (window was sealed bmo):** COG, ELN, ETH and TIP release after the 13 Nov close by their own timestamp history, so their reaction is close(11-13) → close(11-16) and the sealed window probably holds none of it; each `session_check` opens with `amc` and cites the timestamps. ERG, IP and MARR release inside the 13 Nov session, so only part of the reaction is inside the window. AEIN's Q3 was already published by ad-hoc on 12 Nov 13:17 CET (inside the sealed spot); 13 Nov only details it. NA9 is a takeover stub (Persistent EUR 81 cash, 94.04% held).

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing. All four members ran, no fallback. Each judge's own top 20% starts at |1.12| (Opus 5), |0.84| (Opus 5.5), |0.64| (Sonnet 5.5), |0.96| (Fable 5.1), read on 200 live sizes each. Sonnet 5.5 read only the Nordic definition plus the shared core and LESSONS; Opus 5.5 read the core, LESSONS and part of the DE definition; Opus 5 the Nordic and part of the DE definition; Fable 5.1 all six definitions.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ETH | | 69 | short | 16 | 73S | 42S | 82S* | 80S | 2 | −1.12 | −0.40 |
| 2 | MARR | | 72 | short | 12 | 75S | 73S | 52S | 86S* | 1 | −1.00 | −1.10 |
| 3 | IRLAB_A | | 45 | short | 50 | 68S | 40L | 90S* | 60S | 1 | −0.84 | +1.00 |
| 4 | TRE | | 72 | short | 6 | 76S | 78S | 64S | 68S | 0 | −1.03 | −1.30 |
| 5 | ELN | | 65 | long | 4 | 62L | 64L | 62L | 72L | 0 | +0.85 | +0.60 |
| 6 | AFG | | 63 | long | 8 | 68L | 54L | 73L | 55L | 0 | +0.83 | +0.50 |
| 7 | ASMDEE_B | | 47 | long | 13 | 58L | 43L | 28L | 60L | 0 | +0.62 | +0.40 |
| 8 | BC8 | | 44 | short | 17 | 62S | 42S | 18S | 55S | 0 | −0.61 | −1.20 |
| 9 | COG | | 26 | short | 29 | 20L | 25S | 49S | 52S | 0 | −0.44 | +0.20 |
| 10 | MRL | | 38 | long | 10 | 31L | 43L | 28L | 52L | 0 | +0.44 | +1.40 |
| 11 | IP | | 35 | long | 8 | 20L | 41L | 38L | 39L | 0 | +0.44 | +0.65 |
| 12 | G | | 26 | long | 7 | 14L | 30L | 26L | 34L | 0 | +0.32 | +0.40 |
| 13 | ERG | | 21 | short | 5 | 14S | 22S | 19S | 30S | 0 | −0.23 | −0.10 |
| 14 | LAND | | 14 | long | 16 | 6S | 37L | 18L | 9L | 0 | +0.19 | +0.60 |
| 15 | BAVA | | 9 | long | 15 | 14S | 10L | 26L | 14L | 0 | +0.17 | +0.30 |
| 16 | NA9 | | 8 | long | 3 | 6L | 6L | 12L | 6L | 0 | +0.08 | +0.20 |
| 17 | AEIN | | 3 | long | 8 | 11L | 10L | 0- | 9S | 0 | +0.07 | +0.10 |
| 18 | TIP | | 4 | long | 2 | 5L | 5L | 6L | 0- | 0 | +0.05 | +0.30 |
| 19 | FAA | | 0 | long | 22 | 8L | 10S | 30S | 30L | 0 | −0.01 | +0.30 |

**No name is selected.** The nearest are ETH (2 of 4) and MARR (1 of 4). The two names at panel_pct 72:

- **MARR short (72, sd 12).** All four judges short. Evidence the judges name: Italian diesel about +29% y/y through Q3 against +26% in Q2, the quarter whose EBITDA fell 37.7m → 31.7m on fuel and energy by the company's own attribution; the only visible bar (Intesa, 5 Aug) still has H2 EBITDA slightly up; every 2026 print fell. Case against: the stock is already −20% since H1 with no company news, and the release lands around 15:30–16:15 CET so most of a reaction may fall on 16 Nov, outside the window.
- **TRE short (72, sd 6, the tightest agreement of the day).** All four short. Evidence: the >EUR 6.5bn sales guide needs about +16% H2 on H1 after Q2 sales grew 2.9%; Renta 4's model is already 5% under it; the stock ran +20% in 20 sessions into the print. Case against: the chairman ruled out new provisions and confirmed the dividend's return, order intake keeps coming, and Spain has no short register, so the lean is the run-up itself.

**Where the panel and the hunters disagree most:** IRLAB_A (hunter +1.00, panel short 45 with sd 50: three judges short, Opus 5.5 long; abs_move 15–22 the day after a −72% fall, so this is size without direction); MRL (hunter's top at +1.40, panel only 38 long); COG (hunter +0.20, panel short 26); FAA (hunter +0.30, panel 0); ETH (hunter −0.40, panel's highest-ranked at −1.12 but the hunter puts its release after the close).

What the numbers are not: `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; certainty (`p_up`) is recorded and decides nothing; this market's member scales are still largely seeded from stage E-P until it has about 200 panel names of its own; and in the four-model re-judge the judges ranked Europe better than the live hunt, so nothing about this market's panel is established (2026-10-21: ρ +0.22, p 0.19 on 45 names).

## Top and bottom name

- **Top, MRL +1.40:** CoreWeave (about 80% of Merlin's data-centre capacity) beat and raised on 10 Nov and rose 24.7% on 11 Nov while MRL rose 0.6% (+0.5), and the EUR 340m FY26 FFO guide after EUR 180m in H1 implies a flat H2, leaving room for a raise (+0.6). Source: H1 2026 release and CoreWeave's 10 Nov results, cited in `hunts/MRL.json`. The bear risk (Spanish draft Real Decreto on data centres) sits in `outside_window` at −2.0.
- **Bottom, TRE −1.30:** the sales-guide gap above (−1.5, https://www.r4.com/articulos-y-analisis/valores/tecnicas-reunidas-castigo-injustificado), partly offset by the dividend and no-provision statement (+0.3, https://www.bolsamania.com/capitalbolsa/noticias/empresas/tecnicas-reunidas-despeja-sus-grandes-dudas-vuelve-el-dividendo-y-no-habra-mas-provisiones-en-2026--23636332.html).

## Per name: what was already public and what is new

- **Already pre-released:** AEIN (Q3 ad-hoc 12 Nov), BC8 (Q3 ad-hoc and second guide raise 5 Nov; only cash flow is new), LAND (H1 valuation and lettings in the 1 Oct placing), BAVA (third guide raise 8 Oct), TIP (Bending Spoons gain flagged at H1), IRLAB_A (restructuring by inside-information release on 12 Nov, stock −72%).
- **Likely guidance change in the release, per the hunters:** TRE (sales-guide trim risk), MRL and ELN (room to raise or firm), IP (possible narrowing to the upper end), MARR (no numeric guide; current-trading commentary on diesel).
- **New numbers, nothing pre-released:** AFG, ASMDEE_B, COG, ELN, ERG, ETH, FAA, G, IP, MARR, MRL, TRE.

## What the note has to say every time

- **Selection:** `random sample of 23 eligible, seed 'eu-2026-11-13'`; 66 scheduled, 23 eligible above $100k/day, 20 hunted. `by_market`: it 7, de 4, uk 2, se 2, es 2, dk 1, no 1, pl 1, fr 0, fi 0. The draw was random among the eligible names.
- **Concentration:** largest market **Italy at 35%** (7 of 20), 8 markets represented. The Italian seven share one calendar week and one diesel/energy backdrop (MARR, IP, ERG) — a correlated exposure the scorer cannot see.
- **`session_unresolved`:** AEIN, AFG, BAVA, COG, DIA, ELN, ERG, ETH, FAA, G, IP, MARR, MRL, NA9, TIP, TRE carried it at seal. The hunters settled most of them (above); COG, ELN, ETH and TIP point to amc, which roughly halves what the sealed window can see.
- **Option anchor:** `options` is null in all ten markets; Europe runs in the anchor-less regime (`backtest/FINDINGS.md` §33: ρ +0.073, p 0.45 over 104 events).
- **Short registers:** UK, DE, DK, NO, SE, IT read; FR and FI not in today's draw; ES and PL have none. **4 of 20 names carry `anchor_covered: true`** (LAND 3.80%, BAVA 2.31% on Denmark's 0.1% scale, MARR 1.31%, BC8 0.54%). The other 13 read zero at the 0.5% truncation floor, which is not an anchor.
- **Spain and Poland:** 3 of 20 names (MRL, TRE, COG) have no positioning anchor and can never be confirmed or killed after the fact; their lean is the run-up, which is the free control. **Germany:** 4 names (AEIN, BC8, FAA, NA9) cannot reach `event_occurred: false` either. Italy cannot since 2026-09-22.
- **`lean_vs_free_control_rho`:** the last resolved run with the field (2026-10-16) carries it for Sweden only, 0.60.
- **Lean weights** are priors borrowed from the US runs and measured nowhere in Europe.
- **History basis:** only DIA and LAND (`observed_rns`) and AFG (`observed_newsweb`) carry real dated history; the other 17 are cadence estimates, a scale and not a record. Two hunters (ASMDEE_B, FAA) found the estimated dates miss the real prints.
- **Above the floor:** none. Below it the sign was a coin flip over the whole US sample.
- **Language notes worth quoting:** COG, ERG, MARR, ETH and TIP: every load-bearing item (dates, release timestamps, the diesel series, the share issue) came from local-language sources only. BC8: the Cancom peer cut reached only the German press. TRE: the Renta 4 sales-gap numbers were Spanish only. LAND and DIA: domestic sources added nothing, the expected UK result.
- One day is not a result.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
