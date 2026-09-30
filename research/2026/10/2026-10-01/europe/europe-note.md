# Stage EU — Europe ranking for Thursday 2026-10-01

The baselines were sealed on Wed 2026-09-30 at about 13:42 UTC, while the European
markets were **still trading**. Every sealed spot and run-up is therefore an **intraday
price, not a close**. `eu_resolve.py` measures the realised move from daily bars, never
from the sealed spot.

## Answer first

**There is no ranking today.** Two names were eligible and only one of them has an event
in the window. That one sits at −1.00, below the conviction floor of 3.0. Across the whole
US sample, the sign below the floor was a coin flip. The ranking key is `impact_sum`, as
`edge-scores.json` reports it.

| # | name | market | session | `impact_sum` | pre-lessons | `abs_move_pct` | `p_up` | lean | anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SNI Stolt-Nielsen | no | bmo (06:00 UTC pattern, issuer notice 09-24) | **−1.00** | −0.9 | 6.5 | 42 | −0.69 | truncated zero (Finanstilsynet read, no position) |
| — | JHD James Halstead | uk | **results delayed to 14 Oct** | not ranked | 0.0 | 1.6 | 50 | +0.26 | FCA 0.2% |

**SNI, Stolt-Nielsen (−1.00).** The company has already set the bar for Q3 (Jun–Aug). The
Q2 release said "improved performance in the third quarter", and on the Q2 call management
put tanker TCE at about $24.5k/day. Sources:
<https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=677877>,
<https://norwaystocks.substack.com/p/stolt-nielsen-q2-2026-key-takeaways>.

What is new, and what can move the stock, is the Q4 tanker outlook and whether the 2026
guidance (withdrawn in April) comes back.

- **The one finding, −1.0 on `guidance`:** the hunter expects a flat-to-softer Q4 rate
  comment, for three reasons:
  - Chemical spot ex-US Gulf has been soft since mid-June and flat through late September,
    per ICIS via Hellenic Shipping News.
  - Peer Odfjell guided its Jul–Sep underlying result lower. Original: *"sterk konkurranse
    og reduserte globale volumer per nå fører til et mer krevende marked … forventer vi at
    det underliggende nettoresultatet i 3Q26 blir lavere"* ("strong competition and
    reduced global volumes are currently making for a more demanding market … we expect
    the underlying net result in 3Q26 to be lower").
    Source: <https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=680427>.
  - SNI goes into the print +13.7% over 20 days on a sector re-rating.
- **Reaction history:** SNI fell on both prior Q3 prints when management flagged softer Q4
  rates (−6.83% in 2024, −4.93% in 2025). It fell on 7 of its last 10 results days.
- **How far to trust it:** the interval is −4.0 to +2.5. No consensus could be sourced, so
  the bar is the company's own directional statement and the size is held small.
- **The lean does not confirm it.** The finding agrees in sign with the lean, but the lean
  here is only the run-up: the register holds no position, so it is not independent
  confirmation.
- **`already_public`:** the Q3 direction and TCE level, the April guidance withdrawal and
  Odfjell's lower guide.
- **`new_in_release`:** the Q3 numbers and the Q4 guidance line, which is the swing. The
  Avenir LNG sale (completed 1 Sep) lands in Q4, not in this print.

**JHD, James Halstead (not ranked).** At 07:00 on 28 Sep, the company announced by RNS that
FY26 results move from 1 Oct to **Wed 14 Oct 2026**. The reason given is that BDO needs
more audit time, and the company says it "has not been informed of any material audit
issues". Source:
<https://www.investegate.co.uk/announcement/rns/james-halstead--jhd/delay-in-publication-of-fy26-audited-results/9792824>.

The vendor calendar had not picked up the delay, although the sealed baseline's own RNS
history already listed it. 1 Oct is an ordinary session for JHD. The UK archive can reach
`event_occurred: false` at resolve, so this kill should happen automatically; check that it
does.

## Selection and instrumentation

- **Funnel:** 6 scheduled (uk 3, fr 2, no 1), then 2 eligible above $200k/day, then 2
  hunted.
  - `selection.method` is "all 2 eligible names (at or under the cap)". No random draw
    was needed, and the seed `eu-2026-10-01` was unused.
  - `by_market`: uk 1, no 1, the other eight 0.
- **`market_concentration`:** uk 0.50 across 2 markets. With one rankable name, no pooled
  statement is possible.
- **Off-primary rows filtered:** se 231 (NGM), pl 326 (NewConnect).
- **`options`:** null for both names. Europe runs in the anchor-less regime that
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Short registers:** uk (FCA, as of 09-29) and no (Finanstilsynet, 09-29) both read.
  **`anchor_covered: true` on 1 of 2**, JHD at 0.2%. SNI's zero is a truncated zero, not a
  measurement.
- **Spain and Poland:** 0 names. **Germany:** 0 names.
- **`session_unresolved`:** 0 of 2, both vendor-flagged bmo. SNI's session is confirmed by
  the issuer's own conference notice and its 06:00 UTC release pattern.
- **`history.basis`:** observed on both names, `observed_rns` for JHD and
  `observed_newsweb` for SNI. Neither rests on a cadence estimate.
- **`lean_vs_free_control_rho`** (UK, previous resolved runs): 0.69 on 09-22, 0.943 on
  09-23 and 0.70 on 09-24. No later run has resolved, and no Norwegian figure exists yet.
  The lean's weights are priors borrowed from the US runs and have been measured nowhere
  in Europe.

## `language_note` (prose, not ranked)

- **SNI:** E24's Norwegian headlines on the last two Q3 prints tie those sell-offs to the
  Q4 rate comment ("venter lavere skipsrater i fjerde kvartal", "expects lower shipping
  rates in the fourth quarter"). The English wires carried the numbers but not that
  framing. A paywalled Finansavisen buy-side piece of 09-26 ("Forventer reprising av
  kjemikalierederier", "expects chemical-tanker shipowners to re-rate") is the local read
  of the September run-up. It is a snippet only and is not load-bearing.
- **JHD:** nothing the English sources did not already carry.

## What this is and is not

One day is not a result, and this day has one rankable name below the floor. The vendor
calendar produced 1 of 2 rows without an event in the window. Last run it was 4 of 10, so a
stale vendor date has now shown up on two consecutive days.

**Resolve plan:**
- **SNI:** from the 2026-10-01 close. Norway's day archive has a true date query, so there
  is no one-week limit.
- **JHD:** confirm the automatic kill.

No orders were placed or considered. This stage reads no broker.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
