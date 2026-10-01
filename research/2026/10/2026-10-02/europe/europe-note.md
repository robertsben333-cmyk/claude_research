# Stage EU — Europe ranking for Friday 2026-10-02

The baseline was sealed on Thu 2026-10-01 at about 13:40 UTC, while the European markets
were **still trading**. The sealed spot and run-up are therefore an **intraday price, not
a close**. `eu_resolve.py` measures the realised move from daily bars, never from the
sealed spot.

## Answer first

**There is no ranking today.** One name was eligible. It is rankable but sits at −0.91,
below the conviction floor of 3.0. Across the whole US sample, the sign below the floor
was a coin flip. The ranking key is `impact_sum`, as `edge-scores.json` reports it.

| # | name | market | session | `impact_sum` | pre-lessons | `abs_move_pct` | `p_up` | lean | anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | JDW J D Wetherspoon | uk | bmo (issuer-dated; 07:01 last year) | **−0.91** | −0.88 | 6.5 | 43 | +2.76 | FCA 4.57% disclosed (−0.01pp) |

**JDW, Wetherspoon (−0.91): FY26 preliminary results.** The date comes from the issuer's
own 22 Jul pre-close RNS: "The preliminary results are due to be released on 2 October
2026". Source:
<https://www.investegate.co.uk/announcement/rns/wetherspoon-j-d---jdw/pre-close-trading-update-correction/9681606>.

- **`already_public`:** the year is already out. The July update was the fourth profit
  warning of FY26, giving Q4 like-for-like sales +4.0%, year-to-date +4.2% and net debt of
  about £720m. The interims had already warned.
- **The bar is disputed.** LSEG consensus has full-year pre-tax profit at £64.6m (IG
  preview, 25 Sep), while Panmure Liberum has £60.0m for FY26 and £74.2m for FY27 (SQC
  Research, 30 Sep). The hunter had no sourced lean on which side the profit lands, so
  `print_vs_bar_pct` is 0.
- **`new_in_release`:** the swing is the FY27 outlook (Tim Martin's statement) and the
  current-trading figure for roughly the first nine weeks of the new year.
- **The finding driving the number, −0.77 on `guidance`.**
  - Since the warning-day close the stock has risen 13.5%, from 722.5p to 822.5p, against a
    625p Panmure target. That price assumes a recovery of about 24% in FY27 profit.
  - His last two results-day statements fell 5.64% (FY25 prelims) and 10.55% (FY26
    interims).
  - Sources: <https://www.investegate.co.uk/announcement/rns/wetherspoon-j-d---jdw/preliminary-results/9147818>,
    <https://www.investegate.co.uk/announcement/rns/wetherspoon-j-d---jdw/interim-results/9483469>,
    <https://www.sqcresearch.com/post/jd-wetherspoon-just-how-will-its-shares-react-to-this-friday-s-finals>.
- **The other three findings:**
  - **Current trading, −0.26.** The CGA RSM tracker had managed pubs at +0.5% in August
    2026, and Mitchells & Butlers' last quarter was +1.4%. Wetherspoon has beaten the
    tracker for 42+ months, so this carries little weight. Source:
    <https://nielseniq.com/global/en/news-center/2026/restaurant-sales-revive-but-pubs-soften-in-steady-august-for-hospitality/>.
  - **Short position, +0.17.** The FCA register shows 4.57% net short, flat through the
    rally.
  - **Insider sale, −0.05.** A person closely associated with the Operations Director sold
    3,000 shares on 13 Aug. It is tiny.
- **Against the baseline.** The sealed lean is +2.76, almost all of it from the short
  position. The hunter's evidence leans mildly the other way. The 20-day run-up is flat
  (+0.06%), but the 60-day run-up is +14.9%: the move happened more than 20 sessions
  ago, which is the blind spot `run_up_60d_pct` exists to catch.
- **The `pre_lessons` freeze is live.** The draft was −0.88, with a 5.5 move size and
  `p_up` 42. `LESSONS.md` raised the move size to 6.5, because the first outlook for a new
  year is a scheduled guidance event.

## Selection and instrumentation

- **Funnel:** 3 scheduled (uk 1, fr 1, pl 1), then 1 eligible above $200k/day, then 1
  hunted.
  - `selection.method` is "all 1 eligible names (at or under the cap)". No random draw
    was needed, and the seed `eu-2026-10-02` was unused.
  - `by_market`: uk 1, the other nine 0.
  - Dropped below the floor: ALBPK Broadpeak (fr, $8.8k/day) and KER Kernel (pl,
    $41k/day).
- **`market_concentration`:** uk 1.00, one market. No pooled statement is possible.
- **Off-primary rows filtered:** se 231 (NGM), pl 325 (NewConnect).
- **No `market_closed`** on any of the ten markets.
- **`options`:** null. Europe runs in the anchor-less regime that
  `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073, p=0.45 over 104 events.
- **Short register:** uk (FCA, as of 2026-09-29) read. **`anchor_covered: true` on 1 of
  1.**
- **Spain and Poland:** 0 names. **Germany:** 0 names.
- **`session_unresolved`:** 0. The bmo session is vendor-flagged and consistent with last
  year's 07:01 RNS.
- **`history.basis`:** `observed_rns` (n 8, median absolute move 4.91%). Nothing rests on
  a cadence estimate.
- **`lean_vs_free_control_rho`** (UK, previous resolved runs): 0.69 on 09-22, 0.943 on
  09-23 and 0.70 on 09-24. The 09-25 run resolved one usable row and computed no
  statistics. The lean's weights are priors borrowed from the US runs and have been
  measured nowhere in Europe.

## `language_note` (prose, not ranked)

UK, so the "local" half is source locality rather than language:

- The RNS record gave the issuer's date confirmation, last year's timestamp and the
  13 Aug insider sale. None of these surfaced on the wires.
- SQC Research carried Panmure's full forecast set, where Reuters carried only a
  "low-to-mid £60m" range.
- The CGA RSM tracker carried the August managed-pub like-for-like figure.

## What this is and is not

One day is not a result, and this day has one name, below the floor. Early October is
the thin gap between the UK's September season and the Nordic October one.

**Resolve plan:** from the 2026-10-01 close to the 2026-10-02 close. The UK archive can
confirm the release. Yahoo's `.L` closes lag a session, so resolve on Monday or later.

No orders were placed or considered. This stage reads no broker.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.*
