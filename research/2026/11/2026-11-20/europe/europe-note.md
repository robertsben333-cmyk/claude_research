# Stage EU — Europe ranking for 2026-11-20 (Fri)

Sealed 2026-11-19, about 14:40 UTC, while the European markets were still open. The sealed spots are intraday prices, not closes. The event date is Friday 2026-11-20.

**Answer first: a near-empty day.** Of the 7 names drawn, three were calendar phantoms: TRI, JACK and BMC have no print on 20 November. The four that do report all sum to almost nothing, and none clears the 2.8 conviction floor. The panel selects nothing. Its strongest name is **PRS, long, panel_pct 73**, which is at the executor's 70 threshold, so the IBKR handoff carries PRS alone.

## Ranked on `impact_sum` (the key, per `edge-scores.json`)

| # | ticker | market | session | impact_sum | floor | impact_scaled | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CMP | pl | bmo? (hunter: **amc**) | +0.20 | no | +0.20 | 5.0 | 52 |
| 2 | PAX | se | bmo (07:00 CET, MFN) | +0.20 | no | +0.15 | 7.5 | 51 |
| 3 | PNOR | no | bmo (06:30 CET) | +0.10 | no | −0.40 | 3.3 | 44 |
| 4 | PRS | no | bmo (07:00 CET) | +0.10 | no | +0.26 | 6.5 | 52 |

**Not ranked: the hunter found no event on this date.**
- **TRI (uk):** the half-year report was on 2026-11-17 at 07:00. That was the date the company's 20 October trading update named, and the stock fell 19.8% on an FY27 guidance cut. The 2026-11-20 row came from the RNS calendar and is stale. ([RNS](https://www.investegate.co.uk/announcement/rns/trifast--tri/half-year-financial-report/9878195))
- **JACK (no):** the issuer's own calendar puts Q3 on 2026-11-25. The vendor's 11-20 date is an estimate. ([NewsWeb](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=672200))
- **BMC (pl):** ESPI 68/2026 of 2026-11-17 moved the Q3 report to 2026-11-30: "przesunięciu terminu publikacji … na dzień 30 listopada 2026 roku" (moving the publication date … to 30 November 2026). ([biznesradar](https://www.biznesradar.pl/a/170208,bumech-sa-68-2026-zmiana-terminu-publikacji-raportu-okresowego-za-trzy-kwartaly-2026-roku))

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran; there were no fallbacks.

```
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 PRS      bmo          73 long    19  opus5: 77L  opus55: 40L  sonnet55: 86L* fable51: 88L*  2  +1.21
   2 CMP      bmo?         11 long    38  opus5: 54S  opus55: 28L  sonnet55: 45L  fable51: 26L   0  +0.31
   3 PNOR     bmo           4 long     8  opus5: 13L  opus55:  0-  sonnet55:  9L  fable51:  6S   0  +0.06
   4 PAX      bmo           2 short   67  opus5: 64L  opus55: 67L  sonnet55: 62S  fable51: 76S   0  +0.03
```

`sel` = 3 of 4 judges in their own top 20% (the market panels' rule). `pct` = `panel_pct`, the size of the mean of the four signed percentiles, each read against that judge's own live range (n=200 each). The hunter's `impact_sum` is in the table above.

**Selected names: none.** PRS has 2 of 4 judges in their own top 20% (Sonnet 5.5 and Fable 5.1). Its panel_pct of 73 is still at or above the executor's `panel_pct >= 70` rule.

**PRS, the panel's strongest name.** The judges named three things:
- The pre-released Q3 utilisation of 80% plus the Safe Notos re-rate from USD 75k to 140k a day. On the hunter's bottom-up, H2 EBITDA comes to about USD 30-35m against the 25.5-30.5m implied by the FY26 guide of 50-55m ([Q2 report](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=681099), [Q3 operations update](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=684399)).
- The single-analyst coverage.
- A 22% fall over 60 sessions.

**The strongest case against PRS:** Safe Eurus (contract ends H1 2027) and Safe Zephyrus (ends September 2027) have no announced follow-on. A backlog-only Q3 in 2024 fell 22%. Caius Capital sold through 15% in October and still holds 14.66% ([flagging](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=684129)). The −9.9% on 7x volume on 17 November has no filing behind it. The guide upgrade is the hunter's inference, not a company number.

**Where the panel and the hunter disagree:**
- **PAX:** the judges split 2 long and 2 short, with sd 67, the widest of the day. The hunter has it at +0.2.
- **CMP:** Opus 5 reads it short (54S), against the hunter's long.
- **PRS:** the panel's top name and the hunter's bottom ranked name. Same sign, larger panel scale.

**What these numbers are not:**
- `panel_score` ranks and does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are each judge's own live European range.
- The EU panel has no measured edge yet: on 2026-10-21 it read ρ +0.22, p 0.19 on 45 names.

## What drives the top and the bottom

- **Top, CMP +0.20:**
  - A possible raise of at least 10% to the 2027/28 EBITDA targets, sized at +0.8 and about 20% likely in this release. The CEO repeated it in a Parkiet TV interview on 2026-10-16, in Polish only.
  - Offset by weaker Q3 cash flow from pre-buying SAFE components (−0.5) and a DM BOŚ 98 PLN target with the spot at 98.6 (−0.2).
  - The quarter itself (+0.1) had already been telegraphed by the CEO.
- **Bottom, PRS/PNOR +0.10:**
  - PNOR: production was pre-released on 9 October and no oil sales were guided for Q3. The only live item is a possible OML 113 sale (+0.2) ([production update](https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=683842)).
  - PRS: the guide upgrade (+0.6) and cash flow (+0.2) are offset by recontracting (−0.4) and Caius supply (−0.3).

## The day's composition and its caveats

- **The draw:** `selection.method` is "all 7 eligible names (at or under the cap)", with no random cut needed (seed `eu-2026-11-20`). 28 were scheduled and 7 were eligible above the $100k floor.
  - `by_market`: no 3, pl 2, se 1, uk 1.
  - `selection.market_concentration`: the largest market is **Norway at 43%**, across 4 markets. Of the 4 ranked names, 2 are Norwegian.
- **Phantoms: 3 of 7.** TRI came from the RNS calendar, JACK from the vendor, and BMC from the vendor after the company postponed.
- **Calendar sources:**
  - Yahoo's calendar was **unavailable in all ten markets**: the quote endpoint failed on every batch.
  - The UK RNS calendar read: 3 dated, adding TRI and PAM.
  - Issuer calendars read for de (EQS), se/dk/fi (inderes, Nasdaq), and no (Euronext Oslo).
  - **bankier (pl) returned HTTP 403.**
- **Session:**
  - **`session_unresolved` at seal:** JACK, BMC, CMP, TRI. Three of them have no event.
  - **CMP: the hunter found the session is amc**, because H1 was filed at 20:15 and FY at 17:12, both after the Warsaw close. So the real window is likely 11-20 close to 11-23 close, not the sealed bmo. Getting this wrong roughly halves the move.
  - PAX, PNOR and PRS are confirmed bmo by the issuers' own notices.
- **Option anchor:** `options` is null in all ten markets. Europe runs in the anchor-less regime (ρ=+0.073, p=0.45 over 104 events on the sealed corpus).
- **Short registers:**
  - no, se and uk read. **pl has no register.**
  - **`anchor_covered: true`: 0 of 7.** Every name read on a register is a truncated zero.
- **Weak legs:**
  - **2 of 7 names are Polish** (BMC, CMP). They have no positioning anchor: their lean is the run-up, which is the free control. They cannot be confirmed or killed after the fact.
  - No Spanish or German names today.
- **`lean_vs_free_control_rho`:** the last resolved European run is 2026-10-16, which reports se 0.6 only.
- **The lean's weights** are priors borrowed from the US runs, measured nowhere in Europe.
- **`history.basis`:**
  - Estimated (a scale, not a record of dates): BMC, CMP (pl) and PAX (se).
  - Observed: JACK, PNOR, PRS (`observed_newsweb`) and TRI (`observed_rns`).
  - PNOR's history row for 2026-05-29 (−27.5%) is mostly a NOK 3.25 ex-distribution, not a results reaction.
- **`already_public` / `new_in_release`:**
  - PNOR pre-released Q3 production and guided no Q3 lifting.
  - PRS pre-released Q3 utilisation.
  - CMP's quarter was signalled by its CEO.
  - PAX has nothing pre-released and gives no guidance, so its whole quarter is new; that is why it has the largest `abs_move` at 7.5.
  - A guidance change is possible at PRS (FY26 narrowing) and CMP (the 2027/28 targets).
- **Conviction floor:** no name is above 2.8. Over the whole US sample the sign was a coin flip below the floor.
- **Language notes:**
  - The Polish sources carried everything that mattered for CMP (the CEO interview, ESPI) and BMC (the postponement).
  - The Nordic issuers publish in English: "nothing the English sources did not already carry".
- **Orchestration:** all 7 hunters ran at once rather than in waves of 5, to reach the IBKR handoff before the Oslo close. Two scraped PAX scratch pages were deleted because GitHub push protection flagged an embedded third-party Mapbox token; the hunt itself is intact.
- **One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.
