# claude_naive — 2026-09-07 — no forecast written

**Decision: no `forecasts.json` for this date.** The universe was built, qualified, and
found to contain no forecastable event that was not already forecast on 2026-09-04.
Deliberately skipped, not failed.

## Why

**1. Today is not a trading session.** NYSE and Nasdaq were closed for Labor Day
(first Monday of September 2026). `00-universe.json` carries
`reference_is_trading_day: false` from the repo's own NYSE calendar
(`scripts/get_earnings.py:83-103`), and it is independently confirmed —
[NYSE 2026/2027/2028 holiday calendar](https://s2.q4cdn.com/154085107/files/doc_news/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar-2025.pdf),
[coverage of the 7 Sep closure](https://www.aol.com/articles/know-stock-market-closure-sept-090829000.html).
The stage exists to fire 30 minutes before a 20:00 CET / 14:00 ET entry. Today that
entry bar does not exist, so there is nothing this forecast could precede.

**2. The window duplicates Friday's.** Every name in tonight's window prints BMO
2026-09-08, and both names above the $500M floor — ABM and UNFI — were already
forecast in `claude_naive/2026-09-04/forecasts.json` (ABM Lean Down 6.5%; UNFI
Neutral / No Edge 12.0%), with entry prices frozen at 2026-09-04T17:44Z.

**3. Friday's run holds the correct entry, and a duplicate would corrupt the ledger.**
Under the backtest scheme a `bmo` print enters on the prior *session*. With Monday
closed, that is Friday 2026-09-04. `trade_prices.py:72-80` resolves the entry day from
the bar series (`ds[i-1]`), so it lands on Friday's 14:00 ET bar either way. A
2026-09-07 row for ABM would therefore be scored against the **identical** entry and
exit bars as the 2026-09-04 row — one event counted twice in a ledger whose entire
purpose is calibration at N≈40. Both rows would move the direction rate and the
magnitude error in the same direction, inflating or deflating whichever way the print
lands.

## What was checked, not assumed

Both reporting dates were re-confirmed from company sources, so Friday's forecast is
still live and correctly timed rather than stale:

- ABM — Q3 FY2026, Tuesday 8 September 2026, before market open, call 08:30 ET.
  [ABM press release, 2026-08-25](https://www.globenewswire.com/news-release/2026/08/25/3350870/799/en/abm-to-announce-third-quarter-2026-financial-results.html)
- UNFI — Q4 and full-year FY2026 (52 weeks ended 1 August 2026), morning of Tuesday
  8 September 2026, call 08:30 ET.
  [UNFI press release, 2026-08-10](https://secure.businesswire.com/news/home/20260810413437/en/United-Natural-Foods-to-Release-Fourth-Quarter-and-Full-Year-Fiscal-2026-Results-on-September-8-2026)

## Universe as built

6 calendar rows, 0 after-close + 6 before-open, all event date 2026-09-08:

| Ticker | Company | Mkt cap | Status |
| --- | --- | ---: | --- |
| ABM | ABM Industries | $2.77B | above floor — **already forecast 2026-09-04** |
| UNFI | United Natural Foods | $2.64B | above floor — **already forecast 2026-09-04** |
| WDH | Waterdrop | $0.36B | dropped, below $500M floor |
| CAN | Canaan | $0.30B | dropped, below $500M floor |
| DLNG | Dynagas LNG Partners | $0.13B | dropped, below $500M floor (new vs 09-04) |
| GMHS | Gamehaus Holdings | $0.04B | dropped, below $500M floor |

DLNG is the only row not present in Friday's universe, and it is 4x below the floor.
No name above the floor is new.

## Noted for whoever touches stage 0 next

`get_earnings.py` printed the window as *"After the US close on Monday 07 September
2026 through before the US open on Tuesday 08 September 2026"* on a day it had itself
flagged `reference_is_trading_day: false`. There was no Monday close. The company set
is right — Friday's run, generated when Monday was in the future, already skipped
Monday and drew the same window — so this is the human-readable string only, not the
selection logic. Left unchanged rather than edited from this stage, since that string
is stage 0 output that every stage reads. Flagged, not fixed.

## Scoring

`score_naive.py --date 2026-09-07` will exit `no forecasts at ...`, which is the
intended outcome. The 2026-09-08 prints get scored once, off 2026-09-04.

---

A forecasting exercise over public information. Not investment advice.
