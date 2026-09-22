#!/usr/bin/env python3
"""Did the release happen, what did the stock do, and did the ranking predict it.

Three jobs in that order, because the first gates the other two, and a fourth that is
specific to this stage: measuring whether searching in the local language earned
anything.

1. CONFIRM. The calendar is a VENDOR calendar. Its measured phantom rate on the UK was
   2 of 90 rows over 20 sampled days -- far better than the US feed's `time-not-supplied`
   rate of 20 of 20 on 2026-09-17, and not zero, which on a ten-name day is one phantom
   every five days. TRT was ranked, traded and never reported, so `event_occurred: false`
   has to be reachable here too.

   **Eight of the ten markets have a day archive** (`eu_archive.py`), so this is one code
   path over several sources rather than a special case each:

     UK  Investegate's RNS mirror, queryable BY DATE back to 1999. Stronger than Japan's
         TDnet, which keeps about 31 days. Classification is by headline.
     FR  info-financiere.gouv.fr, the AMF's own regulated-information archive, 536,868
         records back to 2012 and current to yesterday. It is the only one of the three
         that publishes the ISSUER'S OWN filing category, so a French results release is
         identified by what the issuer filed it as rather than by what its headline
         says -- the one real fix for the Trustpilot failure mode.
     DE  EQS-News SEARCH, paginated, back years -- not the front-page snapshot Phase 1
         measured and wrote off as same-day-only. It is queried per issuer, because no
         EQS query returns a whole day, so a German name whose EQS spelling differs from
         the vendor's resolves `null` rather than false.

     SE/DK/FI  The Nasdaq Nordic disclosure feed, which carries the ISSUER'S OWN
         category (`Half Year financial report`, `Interim report (Q1 and Q3)`,
         `Financial Statement Release`) -- the France property, in three more markets.
         **Its date filter is accepted and IGNORED**, so it is paged instead, and a day
         it could not be paged back to returns None rather than an empty list.
     NO  Oslo Bors NewsWeb: a true day query, categorised, and keyed by the exchange
         TICKER, so Norwegian confirmation joins on a code rather than on a normalised
         company name -- the weakest link everywhere else here.
     IT  eMarket STORAGE, Borsa Italiana's storage mechanism, behind an intermittent WAF
         (7 of 8 good) and with an EXCLUSIVE `data_to`, which read naively returns zero
         rows for every day and would have killed every Italian name ever hunted.
     ES/PL  **Nothing reachable.** Every CNMV `Consulta-OIR` path returns 403, and
         `www.gpw.pl` and `espi.pap.pl` each scored 0 of 8 on the sweep where
         emarketstorage scored 7 of 8. Every Spanish and Polish row resolves null.

   So `event_occurred: false` is reachable for the UK, France, Norway and Italy; for
   Sweden, Denmark and Finland only while the print is still inside the Nasdaq feed's
   rolling window; and never for Germany, Spain or Poland. `false_reachable` and
   `archive_kind` in the output say which case each market is in, per run, and that
   asymmetry is recorded in each row's `confirmation_note`.

2. MEASURE. Europe reports before the open -- 339 of 379 measured UK results
   announcements landed before 08:00 London -- so a `bmo` name is scored close(D-1) ->
   close(D) and an `amc` name close(D) -> close(D+1). Getting that backwards roughly
   halves the number. Where the vendor could not say which session it was
   (`session_unresolved`), BOTH windows are reported and the assumed one is flagged, so
   a reader can see which rows rest on a guess instead of finding out later that the
   German maximum realised move was 15.4% when the correct window gives 27.5%.

3. RANK. Spearman of the day's `impact_sum` against the realised move, with a
   permutation p and the same controls the other two stages carry: the free control
   `-run_up_20d_pct`, a 5-day version of it, the baseline's `priced_lean_pct`, and
   `conviction` against whether the sign was right. Plus, per market, every lean
   component on its own and `lean_vs_free_control_rho`.

   AND SPLIT BY `anchor_covered`, which is new on 2026-09-19 with the turnover floor.
   The floor dropped from $1m to $200k for cross-market comparability and stream depth,
   and the measured cost is that below $1m the national short register returns a
   disclosed position for 12% of UK issuers against 89% in the $1-5m band. So most of
   what the floor buys is names with no positioning anchor at all, and pooling them with
   the anchored ones would hide an unanchored half ranking at zero. `by_anchor_covered`
   carries the count in each arm, and over a fortnight of pooled days it is what makes
   that decision reviewable.

4. SCORE THE LANGUAGE PASS — RETIRED 2026-09-22, AND READ AS HISTORY. Until that day
   each hunter ran an ENGLISH pass first, froze it as `pre_local`, then ran the
   local-language pass and revised, and `spearman_pre_local` ranked the frozen draft
   against the same realised move as the published key. On the operator's instruction
   the hunters now run ONE bilingual pass and emit no freeze, so a run sealed after
   that date carries no `pre_local` and this section reports `n_with_pre_local: 0`.

   **No European day had resolved while the freeze ran**, so this control never
   produced a number on a real outcome; what was given up is a future measurement and
   not a result. The code stays because the runs that carry the field must keep
   reproducing, and because an empty section here is the honest report of a control
   that no longer runs.

   **The UK number was never the same experiment.** The UK's local language IS English,
   so its second pass was a DOMESTIC-SOURCE pass (RNS, Investegate, Citywire,
   Proactive, Sharecast, the Investors' Chronicle) and the variable was source
   locality, not language. This script therefore reports the pre/post delta per market
   and REFUSES to pool the UK delta with the German and French ones. Averaging them
   would report the mean of two different questions.

   Nothing pools on one day. A single day's delta on four to twelve names is noise and
   must not be reported as a finding, the same caveat `researcher_japan` records for its
   own `impact_sum_pre_lessons`.

ONE CAVEAT SPECIFIC TO EUROPE, AND IT IS A GOOD ONE. None of these markets has a daily
price limit, only volatility interruptions and auction pauses, so the tail is intact:
Phase 1 measured maxima of 42.2% (UK), 27.5% (DE) and 51.8% (FR) against Tokyo's
値幅制限, which truncates exactly the events the hunt most wants credit for. Europe is
the one region of the three in this repo where a large correct call can be paid in full.

AND ONE THAT ARRIVED WITH THE SEVEN NEW MARKETS. The universe draw is random and the
forward calendar is seasonal, so a day can be almost entirely one market -- 15 of 20
names were Swedish on 2026-10-22. That is a correlated exposure the scorer cannot see,
the same shape as the four US names the IEEPA tariff refunds ranked together.
`selection.market_concentration` in the universe file carries it; read it before pooling
a day's rho as if it were ten markets.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import Counter
from statistics import median
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eu_archive as ARCH                         # noqa: E402
from eu_market import MARKETS, capability, false_reachable  # noqa: E402

UTC = ZoneInfo("UTC")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
YQ = "https://query1.finance.yahoo.com"
# The day archives, the classifier and the three-state confirm all live in
# eu_archive.py now, so this file no longer carries a second copy of a results regex
# that could drift from the one the archive uses.


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


# --- confirmation -----------------------------------------------------------------
# All three markets go through `eu_archive`, which returns one row shape per market and
# says per row whether the results classification came from the issuer's own filing
# category (France) or from a headline keyword (everywhere else).


def build_archives(ev, baselines, verbose=True):
    """Read each market's day archive once, for the whole run."""
    arch, notes = {}, {}
    markets = {b["submarket"] for b in baselines.values()}
    for m in sorted(markets):
        try:
            if m == "de":
                issuers = [(b.get("company") or b["ticker"], b.get("company"))
                           for b in baselines.values() if b["submarket"] == "de"]
                rows = ARCH.de_day(ev, issuers)
            else:
                rows = ARCH.day(m, ev)
        except Exception as exc:
            arch[m], notes[m] = None, f"unavailable: {exc}"
            continue
        arch[m] = rows
        if rows is None:
            # `day()` returns None rather than [] where the source could not be read at
            # all -- Spain and Poland always, the Nasdaq feed when it could not be paged
            # back to the date, Italy when the WAF won all eight retries. Every row from
            # such a market resolves `event_occurred: null`, never false.
            notes[m] = ("no archive read: " + (MARKETS[m]["confirm_name"] or "none"))
            continue
        extra = {"de": " (searched per issuer; EQS has no whole-day query)",
                 "se": " (Nasdaq feed paged back to the date; its date filter is "
                       "accepted and ignored, so it is never passed)",
                 "dk": " (Nasdaq feed, paged)", "fi": " (Nasdaq feed, paged)",
                 "it": " (eMarket STORAGE; data_to is EXCLUSIVE and the WAF is "
                       "retried)"}.get(m, "")
        notes[m] = (f"{len({r['issuer_norm'] for r in rows if r['is_results']})} issuers "
                    f"with a results-classified announcement, {len(rows)} rows" + extra)
        if verbose:
            print(f"  archive {m}: {notes[m]}")
    return arch, notes


def _anchor_state(bl):
    """Three states, derived for a baseline sealed before 2026-09-19 that has none.

    `anchor_covered` and `anchor_coverage` are sealed into every baseline from
    2026-09-19, when the turnover floor dropped to $200k. Runs sealed before that date
    carry neither, and reading a missing key as False would file four disclosed UK
    shorts under "no anchor" -- so the state is reconstructed from the positioning
    block, which those baselines do carry, by exactly the rule eu_priced_in.py now
    seals.
    """
    st = (bl.get("anchor_coverage") or {}).get("state")
    if st:
        return st
    pos = bl.get("positioning") or {}
    if not pos.get("covered"):
        return "register_unreadable"
    return "disclosed" if pos.get("short_ratio_pct") else "register_read_no_position"


def _anchor_covered(bl):
    v = bl.get("anchor_covered")
    return bool(v) if v is not None else _anchor_state(bl) == "disclosed"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="a day's run directory")
    ap.add_argument("--no-confirm", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    run = Path(a.run)
    scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
    ranking = scores.get("ranking") or []
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        baselines[b["ticker"]] = b
    if not baselines:
        raise SystemExit("no baselines: cannot tell what date or market this run is for")
    ev = next(iter(baselines.values()))["event_date"]
    d0 = date.fromisoformat(ev)

    # A RUN CANNOT BE CONFIRMED BEFORE ITS EVENT. Without this, resolving a forward run
    # reads the day archives for a date that has not happened, finds no announcement
    # from the issuer, and writes `event_occurred: false` -- a retrospective KILL, which
    # is the one verdict in this stage that is settled by the outcome rather than
    # predicted. TRT is in this repo because a name was ranked and traded on a print
    # that never came; the mirror-image mistake is killing a name whose print is still
    # three days away.
    today = datetime.now(UTC).date().isoformat()
    if ev > today and not a.no_confirm:
        print(f"  confirmation SKIPPED: the event date {ev} is in the future "
              f"(today is {today}). Nothing is confirmed and nothing is killed.")
        a.no_confirm = True
    arch, arch_notes = ({}, {}) if a.no_confirm else build_archives(ev, baselines)

    rows = []
    for r in ranking:
        tk = r.get("ticker")
        bl = baselines.get(tk) or {}
        m = bl.get("submarket")
        sym = bl.get("yahoo_symbol")
        sess = bl.get("session") or "bmo"
        cs = closes(sym, d0) if sym else []
        ds = [x[0] for x in cs]
        last_bar = ds[-1].isoformat() if ds else None
        mv_bmo = mv_amc = None
        if d0 in ds:
            i = ds.index(d0)
            if i >= 1 and cs[i - 1][1]:
                mv_bmo = round((cs[i][1] / cs[i - 1][1] - 1) * 100, 2)
            if i + 1 < len(cs) and cs[i][1]:
                mv_amc = round((cs[i + 1][1] / cs[i][1] - 1) * 100, 2)
        move = mv_bmo if sess == "bmo" else mv_amc

        occurred, cnote = None, "not checked"
        if not a.no_confirm and m in arch:
            if arch[m] is None:
                cnote = f"{MARKETS[m]['confirm_name']}: {arch_notes.get(m)}"
            else:
                occurred, cnote = ARCH.confirm(
                    m, ev, bl.get("company") or tk,
                    # The UK's EPIC and Norway's issuerSign are both real exchange
                    # tickers carried by their archives, so those two join on a code.
                    # Everywhere else the join is on a normalised company name and a
                    # spelling difference reads as silence.
                    ticker=tk if m in ARCH.TICKER_KEYED else None, archive=arch[m])

        rows.append({
            "ticker": tk, "submarket": m, "company": bl.get("company"),
            "impact_sum": r.get("impact_sum"), "conviction": r.get("conviction"),
            "impact_sum_pre_local": ((r.get("diagnostics") or {})
                                     .get("impact_sum_pre_local")),
            "pre_local_variable": ((r.get("diagnostics") or {})
                                   .get("pre_local_variable")),
            "priced_lean_pct": r.get("priced_lean_pct"),
            "run_up_20d_pct": (bl.get("tape") or {}).get("run_up_20d_pct"),
            "run_up_5d_pct": (bl.get("tape") or {}).get("run_up_5d_pct"),
            "run_up_60d_pct": (bl.get("tape") or {}).get("run_up_60d_pct"),
            "history_basis": (bl.get("history") or {}).get("basis"),
            "history_median_abs_move_pct": (bl.get("history") or {})
                                           .get("median_abs_move_pct"),
            "median_turnover_usd_20d": (bl.get("tape") or {}).get("median_turnover_usd_20d"),
            "analyst_count": (bl.get("consensus") or {}).get("analyst_count"),
            "analyst_band": (bl.get("consensus") or {}).get("analyst_band"),
            "lean_components": bl.get("lean_components") or {},
            "positioning_covered": (bl.get("positioning") or {}).get("covered"),
            "anchor_covered": _anchor_covered(bl),
            "anchor_state": _anchor_state(bl),
            "short_ratio_pct": (bl.get("positioning") or {}).get("short_ratio_pct"),
            "session": sess, "session_unresolved": bl.get("session_unresolved"),
            "move_bmo_window_pct": mv_bmo, "move_amc_window_pct": mv_amc,
            "realised_move_pct": move,
            # The last daily close Yahoo actually serves for this symbol. MEASURED
            # 2026-09-19: Paris and Frankfurt run about TWO sessions behind and London
            # about one -- `.PA` and `.DE` symbols carried timestamps for 09-17 and
            # 09-18 with null closes, on liquid names as well as thin ones. So a
            # European run cannot be resolved the morning after the print, and a row
            # whose `last_bar_date` is before its event date is PENDING, not a name
            # that did not move.
            "last_bar_date": last_bar,
            "move_pending": bool(move is None and last_bar and last_bar < ev),
            "event_occurred": occurred, "confirmation_note": cnote,
            "rankable": r.get("rankable"),
        })

    # Yahoo occasionally serves a European symbol's daily bars truncated by a session or
    # two -- the same request that returned bars to 09-16 returned bars to 09-18 twenty
    # minutes later, with no error either time. A resolve where EVERY row has no move is
    # far more likely to be that than a day on which nothing traded, so it says so
    # rather than reporting an empty statistics block as a result.
    if rows and all(x["realised_move_pct"] is None for x in rows):
        pend = sum(1 for x in rows if x["move_pending"])
        print(f"  WARNING: no row resolved to a realised move ({pend} of {len(rows)} "
              f"PENDING -- Yahoo's last daily close is before the event date). Measured "
              f"2026-09-19: Paris and Frankfurt daily closes run about two sessions "
              f"behind and London about one, so a European run cannot be resolved the "
              f"morning after. Re-run in a day or two; this is not a result.")

    usable = [x for x in rows if x["realised_move_pct"] is not None and x["rankable"]
              and x["event_occurred"] is not False and x["impact_sum"] is not None]

    out = {"market": "EU", "event_date": ev, "run": str(run),
           "resolved_utc": datetime.now(UTC).isoformat(timespec="seconds"),
           "confirmation": ({m: "skipped" for m in
                             {b['submarket'] for b in baselines.values()}}
                            if a.no_confirm else
                            {m: {"source": MARKETS[m]["confirm_name"],
                                 "read": arch_notes.get(m),
                                 # Per market, from the measured capability table, not
                                 # from a rule of thumb. It is false for Germany (EQS
                                 # has no whole-day query) and for Spain and Poland (no
                                 # archive reachable at all), and it is CONDITIONALLY
                                 # true for the three Nasdaq markets -- only while the
                                 # print is still inside the feed's rolling window,
                                 # which `archive_read` above records.
                                 "false_reachable": false_reachable(m),
                                 "archive_kind": capability(m, "archive"),
                                 "archive_read": arch.get(m) is not None,
                                 "classified_by": dict(Counter(
                                     r["classified_by"] for r in (arch.get(m) or [])
                                     if r["is_results"]))}
                             for m in sorted(arch)}),
           "n_rows": len(rows), "n_usable": len(usable), "rows": rows}
    out["stats"] = stats_block(usable)
    text = json.dumps(out, ensure_ascii=False, indent=2)
    dest = Path(a.out) if a.out else run / "eu-resolved.json"
    dest.write_text(text + "\n", encoding="utf-8")
    s = out["stats"]
    print(f"{ev}: {out['n_usable']}/{out['n_rows']} usable. "
          f"rho={s.get('spearman_impact_sum_vs_move')} p={s.get('permutation_p')} "
          f"control={s.get('spearman_free_control_neg_runup')} -> {dest}")


def closes(symbol, d0):
    p1 = int(datetime.combine(d0 - timedelta(days=12), datetime.min.time(),
                              tzinfo=UTC).timestamp())
    p2 = int(datetime.combine(d0 + timedelta(days=12), datetime.min.time(),
                              tzinfo=UTC).timestamp())
    url = f"{YQ}/v8/finance/chart/{symbol}?period1={p1}&period2={p2}&interval=1d"
    try:
        d = json.loads(sh(f"curl -sS --max-time 35 -H 'User-Agent: {UA}' '{url}'"))
        r = d["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        return [(datetime.fromtimestamp(t, UTC).date(), q["close"][i])
                for i, t in enumerate(r["timestamp"]) if q["close"][i] is not None]
    except Exception:
        return []


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None

    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return round(num / (dx * dy), 3) if dx and dy else None


def perm_p(xs, ys, rho, iters=20000, seed=7):
    import random
    if rho is None:
        return None
    rng = random.Random(seed)
    ys = list(ys)
    hits = 0
    for _ in range(iters):
        rng.shuffle(ys)
        r = spearman(xs, ys)
        if r is not None and abs(r) >= abs(rho):
            hits += 1
    return round((hits + 1) / (iters + 1), 4)


def stats_block(usable):
    if len(usable) < 3:
        return {"n": len(usable),
                "note": "fewer than 3 usable rows: no statistics computed"}
    ys = [x["realised_move_pct"] for x in usable]
    key = [x["impact_sum"] for x in usable]
    ctl = [-(x["run_up_20d_pct"] or 0.0) for x in usable]
    lean = [x["priced_lean_pct"] or 0.0 for x in usable]
    sign_ok = [1.0 if (x["impact_sum"] or 0) * (x["realised_move_pct"] or 0) > 0 else 0.0
               for x in usable]
    r_key = spearman(key, ys)
    s = {
        "n": len(usable),
        "spearman_impact_sum_vs_move": r_key,
        "permutation_p": perm_p(key, ys, r_key),
        "spearman_free_control_neg_runup": spearman(ctl, ys),
        "spearman_free_control_neg_runup_5d": spearman(
            [-(x.get("run_up_5d_pct") or 0.0) for x in usable], ys),
        # The 60-day control, sealed 2026-09-22. The 20- and 5-day windows share a blind
        # spot: a move OLDER than twenty sessions reads as flat in both, which is what
        # W7L did on 2026-09-23 (+0.24% and -0.67% on a stock +21.5% off its July low).
        # Ranked as its own control and never folded into the lean.
        "spearman_free_control_neg_runup_60d": spearman(
            [-(x.get("run_up_60d_pct") or 0.0) for x in usable], ys),
        "spearman_priced_lean": spearman(lean, ys),
        "spearman_conviction_vs_sign_right": spearman(
            [x["conviction"] or 0.0 for x in usable], sign_ok),
        "sign_right_frac": round(sum(sign_ok) / len(sign_ok), 3),
        "median_abs_realised_pct": round(median(abs(y) for y in ys), 2),
        "spearman_lean_components": {
            k: spearman([(x["lean_components"].get(k) or 0.0) for x in usable], ys)
            for k in ("short_squeeze", "short_building", "runup")},
    }

    # Per market. Pooling the three hides the one thing most worth seeing: France runs
    # with an empty short register, so its lean IS the free control and
    # lean_vs_free_control_rho should read near 1.0 there and near 0.4-0.6 in the UK and
    # Germany. An average of the three would make that invisible.
    s["per_market"] = {}
    for m in sorted({x["submarket"] for x in usable if x["submarket"]}):
        sub = [x for x in usable if x["submarket"] == m]
        if len(sub) < 3:
            s["per_market"][m] = {"n": len(sub), "note": "too few rows"}
            continue
        sy = [x["realised_move_pct"] for x in sub]
        sl = [x["priced_lean_pct"] or 0.0 for x in sub]
        sc = [-(x["run_up_20d_pct"] or 0.0) for x in sub]
        s["per_market"][m] = {
            "n": len(sub),
            "spearman_impact_sum_vs_move": spearman([x["impact_sum"] for x in sub], sy),
            "spearman_free_control_neg_runup": spearman(sc, sy),
            "lean_vs_free_control_rho": spearman(sl, sc),
            # Two different things, and confusing them would misread the line above.
            # `register_read` counts names whose national register DOWNLOADED;
            # `anchor_covered` counts names the register actually NAMES. A day whose
            # names are all absent from a register that read perfectly well has every
            # lean equal to -0.05 * run_up, so lean_vs_free_control_rho is 1.0 -- and
            # that is a thin-name day, not a broken register. Read the two together.
            "register_read": sum(1 for x in sub if x["positioning_covered"]),
            "anchor_covered": sum(1 for x in sub if x.get("anchor_covered")),
            "median_abs_realised_pct": round(median(abs(y) for y in sy), 2),
        }

    # The language experiment, RETIRED 2026-09-22. Empty on every run sealed after that
    # date, because the hunters now run one bilingual pass and freeze nothing. On the
    # runs that carry it, reported per market and NOT pooled across the UK / DE-FR
    # boundary, because the UK's second pass tested source locality and the German and
    # French ones tested language. See the module docstring.
    pre = [x for x in usable if x.get("impact_sum_pre_local") is not None]
    s["language_pass"] = {
        "n_with_pre_local": len(pre),
        "spearman_pre_local": (spearman([x["impact_sum_pre_local"] for x in pre],
                                        [x["realised_move_pct"] for x in pre])
                               if len(pre) >= 3 else None),
        "by_market": {},
        "note": "RETIRED 2026-09-22: the hunters now run ONE bilingual pass and freeze "
                "nothing, so n_with_pre_local is 0 on every run sealed after that date "
                "and that is by design, not a hunter that failed to freeze. On earlier "
                "runs spearman_pre_local is the ENGLISH-only draft, frozen by the "
                "hunter before it ran the local pass, ranked against the same realised "
                "move as the published key; the delta is the local pass's "
                "contribution. NOTHING POOLS ON ONE DAY: four to twelve names is "
                "noise. And the UK delta is NOT the same experiment as the German and "
                "French ones -- the UK's local language is English, so its second pass "
                "was a domestic-SOURCE pass and the variable is source locality. They "
                "are reported apart and must not be averaged.",
    }
    for m in sorted({x["submarket"] for x in pre if x["submarket"]}):
        sub = [x for x in pre if x["submarket"] == m]
        s["language_pass"]["by_market"][m] = {
            "n": len(sub),
            "variable": ("source_locality" if m == "uk" else "language"),
            "spearman_pre_local": (spearman([x["impact_sum_pre_local"] for x in sub],
                                            [x["realised_move_pct"] for x in sub])
                                   if len(sub) >= 3 else None),
            "spearman_published": (spearman([x["impact_sum"] for x in sub],
                                            [x["realised_move_pct"] for x in sub])
                                   if len(sub) >= 3 else None),
            "median_abs_revision_pts": round(median(
                abs((x["impact_sum"] or 0) - (x["impact_sum_pre_local"] or 0))
                for x in sub), 3),
        }

    # The thesis, by coverage band. Phase 1 measured 1-2 analysts below $1m/day of
    # turnover, 5-7 at $1-5m, 11-13 at $5-25m and 16-19 above. If the hunt earns
    # something in the thin bands and nothing in the covered ones, that is the thesis
    # with a within-sample control the stage got for free -- which is exactly why the
    # universe is NOT cut to the thin band.
    s["by_analyst_band"] = {}
    for b in ("<=2", "3-7", "8-13", ">13", "unknown"):
        sub = [x for x in usable if x.get("analyst_band") == b]
        if len(sub) >= 3:
            s["by_analyst_band"][b] = {
                "n": len(sub),
                "spearman": spearman([x["impact_sum"] for x in sub],
                                     [x["realised_move_pct"] for x in sub]),
                "sign_right_frac": round(sum(
                    1 for x in sub
                    if (x["impact_sum"] or 0) * (x["realised_move_pct"] or 0) > 0
                ) / len(sub), 3)}
        elif sub:
            s["by_analyst_band"][b] = {"n": len(sub), "note": "too few rows"}

    # --- the cost of the $200k floor, split so it is readable rather than pooled -----
    # The floor moved from $1m to $200k on 2026-09-19 for cross-market comparability and
    # stream depth. What it buys is names; what it costs is the anchor, because below
    # $1m the national short register returns a disclosed position for 12% of UK issuers
    # against 89% in the $1-5m band. Pooling the two halves would hide exactly that: if
    # the unanchored half ranks at zero the pooled number still looks like a result.
    #
    # `anchor_covered` is true only where the register NAMED this issuer. A name the
    # register was read for and does not carry reads a truncated 0.0 and counts as
    # uncovered here, which is the whole point -- that is the state the cheap half of
    # the universe is in.
    s["by_anchor_covered"] = {}
    for lab, want in (("covered", True), ("uncovered", False)):
        sub = [x for x in usable if bool(x.get("anchor_covered")) is want]
        blk = {"n": len(sub),
               "median_turnover_usd_20d": (round(median(
                   x["median_turnover_usd_20d"] for x in sub
                   if x.get("median_turnover_usd_20d") is not None))
                   if any(x.get("median_turnover_usd_20d") is not None for x in sub)
                   else None),
               "n_below_1m_turnover": sum(
                   1 for x in sub
                   if (x.get("median_turnover_usd_20d") or 0) < 1_000_000)}
        if len(sub) >= 3:
            sy = [x["realised_move_pct"] for x in sub]
            blk.update({
                "spearman_impact_sum_vs_move": spearman([x["impact_sum"] for x in sub], sy),
                "spearman_free_control_neg_runup": spearman(
                    [-(x["run_up_20d_pct"] or 0.0) for x in sub], sy),
                "sign_right_frac": round(sum(
                    1 for x in sub
                    if (x["impact_sum"] or 0) * (x["realised_move_pct"] or 0) > 0
                ) / len(sub), 3),
                "median_abs_realised_pct": round(median(abs(y) for y in sy), 2)})
        else:
            blk["note"] = "too few rows for a rank correlation"
        s["by_anchor_covered"][lab] = blk

    # --- by_history_basis -----------------------------------------------------------
    # Added 2026-09-22. `history` carries OBSERVED announcement dates for the UK
    # (Investegate) and Norway (Oslo NewsWeb) and a CADENCE ESTIMATE for the other
    # eight markets, and the two are not the same quality of evidence: measured on the
    # nine names of the 2026-09-23 run, the six observed names had a median absolute
    # historical move of 2.61-10.50% against 1.82-2.09% for the three estimated ones,
    # because an estimated date mostly lands on an ordinary session and samples
    # ordinary-session volatility. On KWS exactly one of eight estimated dates was a
    # real print day.
    #
    # Two different things could follow and this split is what tells them apart: the
    # hunters may be sized too small in the estimated markets (a scale problem, which
    # shows up as a smaller median realised move being predicted well), or the ranking
    # may simply be worse there (an evidence problem). Nothing is corrected on the
    # strength of one day -- `anchor_quality.magnitude` is cut to 0.35 for an estimated
    # history and that reaches `diagnostics` only, never `impact_sum`.
    s["by_history_basis"] = {}
    for lab in ("observed", "estimated"):
        want_obs = lab == "observed"
        sub = [x for x in usable
               if (str(x.get("history_basis") or "").startswith("observed")) is want_obs]
        blk = {"n": len(sub),
               "median_history_abs_move_pct": (
                   round(median(x["history_median_abs_move_pct"] for x in sub
                                if x.get("history_median_abs_move_pct") is not None), 2)
                   if any(x.get("history_median_abs_move_pct") is not None for x in sub)
                   else None),
               "markets": sorted({x["submarket"] for x in sub if x.get("submarket")})}
        if len(sub) >= 3:
            sy = [x["realised_move_pct"] for x in sub]
            blk.update({
                "spearman_impact_sum_vs_move": spearman(
                    [x["impact_sum"] for x in sub], sy),
                "spearman_free_control_neg_runup": spearman(
                    [-(x["run_up_20d_pct"] or 0.0) for x in sub], sy),
                "sign_right_frac": round(sum(
                    1 for x in sub
                    if (x["impact_sum"] or 0) * (x["realised_move_pct"] or 0) > 0
                ) / len(sub), 3),
                "median_abs_realised_pct": round(median(abs(y) for y in sy), 2)})
        else:
            blk["note"] = "too few rows for a rank correlation"
        s["by_history_basis"][lab] = blk
    s["by_history_basis"]["note"] = (
        "`observed` is a real dated announcement record (uk via Investegate, no via "
        "Oslo NewsWeb); `estimated` is this quarter's notified lag stepped backwards, "
        "which is a SCALE and never evidence that a print happened on a date. Compare "
        "`median_history_abs_move_pct` with `median_abs_realised_pct` in each arm: if "
        "the estimated arm's history is systematically below what those names actually "
        "do, the cadence estimator is sampling ordinary sessions and every hunter in "
        "those eight markets is being handed a scale that is too small.")

    s["by_anchor_covered"]["note"] = (
        "`covered` means the national short register returned a DISCLOSED net short "
        "position for this issuer; `uncovered` pools the truncated zeros (register read, "
        "issuer not named) with the unreadable registers, and `anchor_state` on each row "
        "separates those two. This split exists because the turnover floor dropped from "
        "$1m to $200k on 2026-09-19 and the names that buys are overwhelmingly in the "
        "uncovered arm. One day says nothing; over a fortnight of pooled days, an "
        "uncovered arm ranking at zero while the covered arm does not is the measured "
        "cost of that decision.")

    s["unresolved_sessions"] = sum(1 for x in usable if x.get("session_unresolved"))
    s["note"] = ("One day is not a result. These pool across days; a single day's rho on "
                 "4 to 12 names is noise and must not be reported as a finding. The free "
                 "control is the thing to beat. `per_market.lean_vs_free_control_rho` is "
                 "the check on whether the lean is anything but the control -- but read "
                 "it beside `anchor_covered` in the same block, because a day whose "
                 "names are all ABSENT from registers that read perfectly well has every "
                 "lean equal to -0.05 * run_up and reads 1.0 for a reason that is about "
                 "the names, not the source. All three registers resolve since "
                 "2026-09-19. `unresolved_sessions` counts rows whose "
                 "window was assumed rather than known -- compare "
                 "move_bmo_window_pct against move_amc_window_pct on those rows before "
                 "believing their sign.")
    return s


if __name__ == "__main__":
    main()
