# Stage IPO — 2026-10-14

**This is stage IPO: debuts are scored from the first trade to the close, lock-ups from the open to the close. A blind four-model panel re-sizes the evidence. No orders are placed.**
All four judges ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), with no fallback.
One day is an anecdote. This stage is judged pooled.

## Ranked

| # | ticker | event | impact_sum | impact_scaled | selected | panel_pct | side | consensus_k | panel_score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MAIR | lockup | +0.45 (p34) | +0.20 | no | 10 | long | 0 | +0.50 |
| – | ARXS | lockup | not ranked | – | – | – | – | – | – |

ARXS is not ranked because the hunter returned `event_confirmed: false`. See "Unranked" below.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunter's evidence. The panel ranks beside `impact_sum` and replaces nothing.

```
own top 20% starts at: opus5 |2.63|, opus55 |1.89|, sonnet55 |1.60|, fable51 |2.02|  (live sizes before 2026-10-14, n=20 live+20 fallback each)
rank ticker   session sel pct side    sd  members (own percentile, L/S)                 k  score
   1 MAIR     lockup       10 long    17  opus5: 40L  opus55:  0-  sonnet55:  0-  fable51:  0-   0  +0.50
```

Member sizes on MAIR:

| judge | impact_sum | p_up | abs_move |
|---|---|---|---|
| Opus 5 | +1.4 | 60 | 2.8 |
| Opus 5.5 | +0.4 | 54 | 2.2 |
| Sonnet 5.5 | −0.1 | 49 | 2.3 |
| Fable 5.1 | +0.5 | 55 | 2.5 |

- **Selected:** none. No judge put MAIR in its own top 20%.
- **Panel vs hunter:** they agree on a small positive lean. Only Sonnet 5.5 had the opposite sign, at −0.1, which is a non-result.
- **What the numbers are not:**
  - Each judge's top-20% line is still mostly OUR OWN ESTIMATE, not measured: stage E-P's sizes × 0.674 (`ipo_hunt.panel_seed`). That holds until about 60 IPO names have been judged.
  - Debuts and lock-ups share one threshold, although debuts move about twice as much.
  - `panel_score` ranks and does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.

## Per name

**MAIR (Madison Air Solutions, NYSE): lock-up, open→close 2026-10-14**

The setup:

| item | value |
|---|---|
| offer price | $27.00 |
| deal size | $2.23bn |
| 180-day lock-up, expiration date | 2026-10-13 (Nasdaq) |
| spot | $24.08 (10.8% below offer) |
| `early_release_checked` | no early release, waiver or follow-on found (EDGAR has nothing after 2026-08-27, 0 "early release" hits, no Form 144) |

- **Driving finding (+0.3):** only about 37M Class A shares come free today. That is roughly 7% of 501M shares, or about 16 days of volume. The controller's 324.4M Class B shares and the Bertarelli entities' 44.8M Class A shares sit under two-year company lock-ups, to about April 2028. Source: https://www.sec.gov/Archives/edgar/data/2098430/000119312526161509/ck0002098430-ex10_5.htm
- **Strongest case against (−0.4):** about 24.7M of the freed shares belong to low-basis executives, employees, consultants and IAQ Holdings II investors, who are the likeliest sellers today. Source: https://www.sec.gov/Archives/edgar/data/0002098430/000162828026033863/mair-20260331.htm
- **Caveats:**
  - The supply arithmetic is the hunter's own subtraction. The 424B4 was too large to fetch, so the 180-day term rests on a secondary source (MarketBeat syndication).
  - The baseline's 50.3% float share overstates how much is released today.
- **Outside the window:** about 65M PIPE shares sold at $24.97 are unregistered and under water. Their resale registration is due around late November (−1.5, not counted).

## Unranked

**ARXS (Arxis, Nasdaq): lock-up, `event_confirmed: false`**

- **Why it is not ranked:** the 424B4 cover is dated 2026-04-15 and locks holders up "for a period of 180 days after the date of this prospectus". That ends 2026-10-12, so the first free session was **2026-10-13**, not today. stockanalysis.com lists the lock-up at Oct 12. Source: https://www.sec.gov/Archives/edgar/data/2093536/000119312526159369/d81728d424b4.htm
- **Setup:** offer $28.00, deal $1.13bn, spot $49.91 (+78% vs offer).
- **Early release, waiver, follow-on:** none found. The resale S-1 for Omnetics holders was filed 2026-10-13 and is not yet effective.
- **Share that unlocks:** about 85% of economic shares are locked, mostly the Arcline Class B. The baseline's 63.6% counts Class A only.

**Possible defect, not fixed in this run.** MAIR's prospectus is also dated 2026-04-15 with a 180-day term. On ARXS's arithmetic, its first free session was also 10-13. If Nasdaq's "expiration date" is the first free day rather than the last locked one, then `ipo_universe.py`'s "first session strictly after expiration" rule hunts every lock-up one session late. Check this before the next lock-up day. If it holds, MAIR's event is not today's either.

## Funnel

| step | count |
|---|---|
| debuts scheduled | 1 |
| debuts dropped as SPAC | 1 |
| debuts sealed on a range | none |
| lock-ups scheduled | 2 |
| under the deal-size or turnover floor | 0 |
| already trading | 0 |
| kept | 2 |
| hunted | 2 |
| ranked | 1 |

## What this is not

- The 2.8 conviction floor was measured on earnings prints and means nothing here.
- The panel's member scales are still the borrowed E-P seed estimate.
- Nothing has resolved.
- With one ranked name, nothing about ranking is tested today.

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*
