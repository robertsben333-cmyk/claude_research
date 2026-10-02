# Better attention proxies: do they predict where the hunt is right?

**Question (2026-10-02).** The hunt looks for public information the price has not yet
taken in, which should only work where attention is scarce. Retail tilt and the Google
search spike were read as attention proxies. Are there better ones, and do they predict
the hunt's results better?

**Method.** `collect.py` builds sixteen proxies for the 141 resolved, de-duplicated US
names in `dashboard/data/ledger.json`, every one dated before the entry except the
StockTwits watcher count (today's snapshot, so mildly look-ahead). `evaluate.py` fixed
its design before any result was read: higher = more attention, the theory predicts a
negative rho, three outcomes (sign right, signed return, |move|), the book and all names,
Spearman with a within-day permutation p, a family-wise p over all proxies, and two
composites declared up front. `vol_check.py` asks how much of retail tilt is volatility.

| family | proxies |
|---|---|
| structural attention | analyst estimates, market cap, dollar volume, option chain exists, option OI / share volume, ATM option spread, English Wikipedia article, Wikipedia median views (via Wikidata ticker), StockTwits watchers |
| momentary attention | abnormal volume 5d vs 60d, Wikipedia 3-day spike, Google search spike, abs 5-day run-up, closeness to 52-week high |
| other | sources the hunter cited, retail tilt (existing) |

**Result: no better proxy.** On the book (62 names, 15 days), nothing clears the
family-wise correction at either exit. The leaders change with the exit:

| book, rho of attention with sign right | strategy exit | close |
|---|---|---|
| retail tilt (existing, oriented) | -0.372 (p 0.005) | -0.232 (p 0.062) |
| closeness to 52-week high | -0.254 (p 0.047) | -0.371 (p 0.001) |
| market cap | -0.240 (p 0.025) | -0.166 (p 0.111) |
| option chain exists | -0.234 (p 0.028) | -0.121 (p 0.350) |
| structural composite | -0.177 (p 0.131) | -0.098 (p 0.432) |
| momentary composite | -0.067 (p 0.852) | -0.102 (p 0.747) |

Wikipedia, StockTwits, analyst count and the hunter's own source count carry nothing.
Abnormal volume points the WRONG way at the strategy exit (high volume +6.10% against
-0.76%, t -2.06). The structural sizes (cap, options, analysts) all lean the predicted
way and none is stronger than retail tilt, which already contains small cap.

**Retail tilt is largely volatility.** Rank correlation with 20-day realised volatility
0.74. Volatility alone splits the book 80.6% / 38.7% right at the strategy exit (77.4% /
51.6% at the close). Netted of volatility, retail tilt keeps rho +0.28 on the hit rate
(+0.17 at the close). The likeliest reading is signal against noise: in a name that
barely moves, the sign of the move is mostly noise, so any forecaster's hit rate falls
toward 50% there. That is not an attention effect, and it would show up for a coin with
a good prior too.

**What this does not show.** 62 book names over 15 days, almost all Opus 5. Twenty-plus
cells tested, so several nominal p < 0.05 are expected by chance. Wikipedia coverage is
70 of 141 tickers (Wikidata ticker mapping, NYSE/Nasdaq/NYSE American only) and median
views only reach 19 book names. The Google spike exists for 22 book names.
