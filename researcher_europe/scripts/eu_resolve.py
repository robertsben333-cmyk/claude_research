#!/usr/bin/env python3
"""Did the release happen, what did the stock do, and did the ranking predict it.

Three jobs in that order, because the first gates the other two, and a fourth that is
specific to this stage: measuring whether searching in the local language earned
anything.

1. CONFIRM. The calendar is a VENDOR calendar. Its measured phantom rate on the UK was
   2 of 90 rows over 20 sampled days -- far better than the US feed's `time-not-supplied`
   rate of 20 of 20 on 2026-09-17, and not zero, which on a ten-name day is one phantom
   every five days. TRT was ranked, traded and never reported, so `event_occurred: false`
   has to be reachable here too. The confirmation sources differ in strength and that
   difference is recorded per name rather than smoothed over:

     UK  Investegate's day archive, which is queryable BY DATE back to 1999. This is a
         STRONGER instrument than Japan's TDnet, which keeps about 31 days -- a UK run
         can be confirmed months later.
     DE  EQS-News, which serves a non-paginating snapshot of the LIVE feed. It confirms
         today and yesterday and nothing older. Resolve promptly or the confirmation is
         lost, exactly as for TDnet.
     FR  Euronext's company news is a single-page application and is the weakest of the
         three. A French name that cannot be confirmed gets `event_occurred: null`, NOT
         false: absence of a readable page is not absence of a release, and turning an
         unreadable source into a retrospective kill would be inventing a fact.

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

4. SCORE THE LANGUAGE PASS. Each hunter runs an ENGLISH pass first, freezes it as
   `pre_local`, then runs the local-language pass and revises. `spearman_pre_local`
   ranks the frozen draft against the same realised move as the published key, so
   "searching in German and French earns rank correlation" becomes a measured claim.

   **The UK number is not the same experiment.** The UK's local language IS English, so
   its second pass is a DOMESTIC-SOURCE pass (RNS, Investegate, Citywire, Proactive,
   Sharecast, the Investors' Chronicle) and the variable is source locality, not
   language. This script therefore reports the pre/post delta per market and REFUSES to
   pool the UK delta with the German and French ones. Averaging them would report the
   mean of two different questions.

   Nothing pools on one day. A single day's delta on four to twelve names is noise and
   must not be reported as a finding, the same caveat `researcher_japan` records for its
   own `impact_sum_pre_lessons`.

ONE CAVEAT SPECIFIC TO EUROPE, AND IT IS A GOOD ONE. None of the three markets has a
daily price limit, only volatility interruptions and auction pauses, so the tail is
intact: Phase 1 measured maxima of 42.2% (UK), 27.5% (DE) and 51.8% (FR) against Tokyo's
値幅制限, which truncates exactly the events the hunt most wants credit for. Europe is
the one market of the three in this repo where a large correct call can be paid in full.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_market import MARKETS                     # noqa: E402

UTC = ZoneInfo("UTC")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
YQ = "https://query1.finance.yahoo.com"
IG_DAY = "https://www.investegate.co.uk/today-announcements/{d}"
EQS = "https://www.eqs-news.com/"

RESULTS_RE = re.compile(r"""(?ix)\b(
   interim\s+(results|report|accounts) |half[-\s]?year(ly)? |final\s+(audited\s+)?results
  |preliminary\s+(results|announcement) |annual\s+(results|financial\s+report)
  |full[-\s]?year\s*(20\d\d\s*)?results |audited\s+results
  |(q[1-4]|first|second|third|fourth)[-\s]*quarter |quarterly\s+(results|report|statement)
  |trading\s+(statement|update) |results\s+for\s+the
  |quartalsmitteilung |halbjahres |jahresabschluss |zwischenbericht
  |r[ée]sultats |chiffre\s+d.affaires
 )\b""")


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


# --- confirmation -----------------------------------------------------------------
def confirm_uk(day):
    """Every EPIC that published a results-type RNS on `day`, plus every EPIC that
    published anything at all.

    Both are returned because a UK issuer's results headline is not reliably a results
    headline: Trustpilot's 2026 interims went out as "AI, Enterprise and US momentum
    fuel strong growth". A name that announced SOMETHING on its scheduled results day
    and nothing recognisable is reported as `announced_unclassified` -- a human call,
    not an automatic kill.
    """
    res, any_ = set(), set()
    for pg in range(1, 15):
        url = IG_DAY.format(d=day) + (f"?page={pg}" if pg > 1 else "")
        html = sh(f"curl -sSL --max-time 40 -H 'User-Agent: {UA}' '{url}'")
        rows = re.findall(r"/company/([A-Z0-9\.]+)\".*?announcement-link\"[^>]*>([^<]*)<",
                          html, re.S)
        if not rows:
            break
        before = len(any_)
        for code, head in rows:
            any_.add(code.upper())
            if RESULTS_RE.search(head):
                res.add(code.upper())
        if len(any_) == before:
            break
    return (res, any_) if any_ else (None, None)


def confirm_de(day):
    """EQS-News' live snapshot. Same-day only -- it does not paginate and has no date
    archive, so a run older than a day or two resolves `null`, never false."""
    today = datetime.now(UTC).date().isoformat()
    if day < (datetime.now(UTC).date() - timedelta(days=2)).isoformat():
        return None, None
    html = sh(f"curl -sSL --max-time 40 -H 'User-Agent: {UA}' '{EQS}'")
    if len(html) < 20000:
        return None, None
    text = re.sub(r"<[^>]+>", " ", html)
    return ("TEXT", text) if today else (None, None)


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

    uk_res = uk_any = de_text = None
    if not a.no_confirm:
        if any(b["submarket"] == "uk" for b in baselines.values()):
            uk_res, uk_any = confirm_uk(ev)
        if any(b["submarket"] == "de" for b in baselines.values()):
            _, de_text = confirm_de(ev)

    rows = []
    for r in ranking:
        tk = r.get("ticker")
        bl = baselines.get(tk) or {}
        m = bl.get("submarket")
        sym = bl.get("yahoo_symbol")
        sess = bl.get("session") or "bmo"
        cs = closes(sym, d0) if sym else []
        ds = [x[0] for x in cs]
        mv_bmo = mv_amc = None
        if d0 in ds:
            i = ds.index(d0)
            if i >= 1 and cs[i - 1][1]:
                mv_bmo = round((cs[i][1] / cs[i - 1][1] - 1) * 100, 2)
            if i + 1 < len(cs) and cs[i][1]:
                mv_amc = round((cs[i + 1][1] / cs[i][1] - 1) * 100, 2)
        move = mv_bmo if sess == "bmo" else mv_amc

        occurred, cnote = None, "not checked"
        if m == "uk" and uk_any is not None:
            t = tk.upper()
            if t in (uk_res or set()):
                occurred, cnote = True, "results RNS on Investegate for this EPIC"
            elif t in (uk_any or set()):
                occurred = None
                cnote = ("announced_unclassified: this EPIC published on the day but "
                         "nothing matched the results classifier. UK issuers headline "
                         "results in marketing language often enough that this is a "
                         "HUMAN call, not an automatic kill -- read the announcement.")
            else:
                occurred, cnote = False, ("nothing at all from this EPIC on Investegate "
                                         "for the event date")
        elif m == "de" and de_text:
            nm = (bl.get("company") or "").split()[0]
            occurred = bool(nm and nm.lower() in de_text.lower()) or None
            cnote = ("EQS-News live snapshot names this issuer" if occurred else
                     "not in the EQS-News snapshot; the snapshot is ~60 items and does "
                     "not paginate, so this is NOT a kill")
        elif m == "fr":
            cnote = ("no readable French confirmation source; Euronext company news is "
                     "an SPA. event_occurred stays null -- an unreadable source is not "
                     "evidence of absence.")

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
            "event_occurred": occurred, "confirmation_note": cnote,
            "rankable": r.get("rankable"),
        })

    usable = [x for x in rows if x["realised_move_pct"] is not None and x["rankable"]
              and x["event_occurred"] is not False and x["impact_sum"] is not None]

    out = {"market": "EU", "event_date": ev, "run": str(run),
           "resolved_utc": datetime.now(UTC).isoformat(timespec="seconds"),
           "confirmation": {
               "uk": ("skipped" if a.no_confirm else
                      f"{len(uk_res)} EPICs with a results RNS, {len(uk_any)} with any "
                      f"announcement" if uk_any is not None else "unavailable"),
               "de": ("skipped" if a.no_confirm else
                      "EQS-News live snapshot read" if de_text else
                      "unavailable (snapshot is same-day only and does not paginate)"),
               "fr": "no readable source; event_occurred stays null for French names"},
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
            "positioning_covered": sum(1 for x in sub if x["positioning_covered"]),
            "median_abs_realised_pct": round(median(abs(y) for y in sy), 2),
        }

    # The language experiment. Reported per market and NOT pooled across the UK / DE-FR
    # boundary, because the UK's second pass tests source locality and the German and
    # French ones test language. See the module docstring.
    pre = [x for x in usable if x.get("impact_sum_pre_local") is not None]
    s["language_pass"] = {
        "n_with_pre_local": len(pre),
        "spearman_pre_local": (spearman([x["impact_sum_pre_local"] for x in pre],
                                        [x["realised_move_pct"] for x in pre])
                               if len(pre) >= 3 else None),
        "by_market": {},
        "note": "spearman_pre_local is the ENGLISH-only draft, frozen by the hunter "
                "before it ran the local pass, ranked against the same realised move as "
                "the published key. The delta is the local pass's contribution. NOTHING "
                "POOLS ON ONE DAY: four to twelve names is noise. And the UK delta is "
                "NOT the same experiment as the German and French ones -- the UK's "
                "local language is English, so its second pass is a domestic-SOURCE "
                "pass and the variable is source locality. They are reported apart and "
                "must not be averaged.",
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
                 "the check that the lean has not collapsed into the control: France has "
                 "no readable short register and should read near 1.0 there, near "
                 "0.4-0.6 in the UK and Germany. `unresolved_sessions` counts rows whose "
                 "window was assumed rather than known -- compare "
                 "move_bmo_window_pct against move_amc_window_pct on those rows before "
                 "believing their sign.")
    return s


if __name__ == "__main__":
    main()
