#!/usr/bin/env python3
"""Did the release happen, what did the stock do, and did the ranking predict it.

Three jobs, in that order, because the first one gates the other two.

1. CONFIRM. A JPX-notified date can move. TDnet is the record of what was actually
   disclosed, so each name is checked against TDnet's list for the event date: a
   `決算短信` filed under that code confirms the event, and nothing found sets
   `event_occurred: false`. That field is the retrospective kill the US stage added
   on 2026-09-18 after TRT was ranked, traded and never reported, and it takes
   precedence over every other reason a row might not rank.

2. MEASURE. Exit is the close of the session after the event date. Entry depends on
   WHEN the company released, which TDnet records to the minute and this script reads:

   - at or after the 15:30 JST close (the TSE has closed at 15:30, not 15:00, since
     2024-11-05): entry is the close on the event date. This is the same window
     `researcher_us/scripts/edge_resolve.py` uses for an amc print.
   - BEFORE the close (13:00, 13:30, 15:00 are all common): the release moved the stock
     inside the session, so the event-date close already holds part of the reaction.
     Entry is the sealed spot instead -- the live price the baseline was struck at,
     10:05 JST, before any release and the price a reader of the note could have
     traded. `entry_basis` says which, and `move_close_to_close_pct` keeps the old
     window beside it so the change is inspectable.

   Until 2026-10-01 every row entered at the event-date close. On the first four
   resolved days that put 3 of 8 names (13:00, 13:00 and 15:00 releases) on a window
   that started after their own reaction: TAKARA & CO (7921), released at 15:00, rose
   3.3% into the close on a +1.0 call and was scored on the next day's -1.9%.

3. RANK. Spearman of the day's `impact_sum` against the realised move, with a
   permutation p-value, and the same three controls the US run carries: the free
   control `-run_up_20d_pct`, the baseline's `priced_lean_pct`, and `conviction`
   against whether the sign was right.

ONE CAVEAT THAT IS SPECIFIC TO JAPAN. Daily price limits (値幅制限) truncate the tail:
a name that would have moved 40% stops at its limit and prints a smaller number. That
biases every correlation here toward zero on exactly the events the hunt most wants
credit for, and it has no US analogue. Limit hits are flagged, not corrected.
"""
import argparse
import json
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
YQ = "https://query1.finance.yahoo.com"
TDNET = "https://www.release.tdnet.info/inbs/I_list_{p:03d}_{d}.html"


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout


def tdnet_codes(d):
    """Every securities code that disclosed a 決算短信 on date `d` (YYYYMMDD), with the
    earliest such release time, as {code: "HH:MM"} (JST). A code whose time could not
    be read maps to None.

    TDnet keeps roughly 31 days online, so this can only confirm a recent run. An
    older run resolves with `event_occurred: null` rather than false -- absence of
    the page is not absence of the release.
    """
    codes, seen_any = {}, False
    for p in range(1, 15):
        html = sh(f"curl -sS --max-time 30 -H 'User-Agent: {UA}' '{TDNET.format(p=p, d=d)}'")
        if len(html) < 3000 or "該当する適時開示情報はありません" in html:
            break
        seen_any = True
        got = 0
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
            text = re.sub(r"<[^>]+>", " ", row)
            if "決算短信" in text:
                mc = re.search(r">\s*(\d{4}0|\d{3}[A-Z]0)\s*<", row)
                if mc:
                    code = mc.group(1)[:-1]
                    mt = re.search(r"\b([0-2]\d:[0-5]\d)\b", text)
                    t = mt.group(1) if mt else None
                    prev = codes.get(code)
                    codes[code] = (t if prev is None or (t and t < prev) else prev)
                    got += 1
        if got == 0 and p > 1:
            break
    return (codes if seen_any else None)


# The TSE close since 2024-11-05. A release before it lands in a live session.
TSE_CLOSE = "15:30"


def closes(code, start, end):
    p1 = int(datetime.combine(start - timedelta(days=10), datetime.min.time(),
                              tzinfo=JST).timestamp())
    p2 = int(datetime.combine(end + timedelta(days=10), datetime.min.time(),
                              tzinfo=JST).timestamp())
    url = (f"{YQ}/v8/finance/chart/{code}.T?period1={p1}&period2={p2}&interval=1d")
    try:
        d = json.loads(sh(f"curl -sS --max-time 35 -H 'User-Agent: {UA}' '{url}'"))
        r = d["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        out = []
        for i, t in enumerate(r["timestamp"]):
            c = q["close"][i]
            if c is None:
                continue
            out.append((datetime.fromtimestamp(t, JST).date(), c,
                        q["high"][i], q["low"][i]))
        return out
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="a day's run directory")
    ap.add_argument("--no-confirm", action="store_true",
                    help="skip the TDnet confirmation pass")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    run = Path(a.run)
    scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
    ranking = scores.get("ranking") or []
    ev = None
    for f in sorted((run / "baselines").glob("*.json")):
        ev = json.loads(f.read_text(encoding="utf-8")).get("event_date")
        break
    if not ev:
        raise SystemExit("no baselines: cannot tell what date this run is for")
    d0 = date.fromisoformat(ev)

    confirmed = None if a.no_confirm else tdnet_codes(d0.strftime("%Y%m%d"))

    rows = []
    for r in ranking:
        code = r.get("ticker")
        bl_path = run / "baselines" / f"{code}.json"
        bl = json.loads(bl_path.read_text(encoding="utf-8")) if bl_path.exists() else {}
        cs = closes(code, d0, d0 + timedelta(days=8))
        # A bar for a Tokyo session still trading is a live price, not a close; on
        # 2026-09-25 a 10:05 JST resolve read one as the exit and froze it.
        now_jst = datetime.now(ZoneInfo("Asia/Tokyo"))
        if now_jst.hour * 60 + now_jst.minute < 15 * 60 + 30:
            cs = [b for b in cs if b[0] < now_jst.date()]
        entry = exitp = exit_d = prev_close = None
        limit_hit = False
        for i, (dd, c, hi, lo) in enumerate(cs):
            if dd == d0:
                entry = c
                prev_close = cs[i - 1][1] if i > 0 else None
                if i + 1 < len(cs):
                    nd, nc, nh, nl = cs[i + 1]
                    exitp, exit_d = nc, nd
                    if nh is not None and nl is not None and nh == nl:
                        limit_hit = True      # locked limit: one price all session
                break
        close_entry = entry
        released_at = (confirmed or {}).get(code)
        in_session = bool(released_at and released_at < TSE_CLOSE)
        spot = (bl.get("tape") or {}).get("spot")
        sealed = bl.get("sealed_utc")
        # The sealed spot is a pre-release price only if it was struck on the event
        # date in Tokyo. The 2026-09-18 verification run sealed 2026-09-25's names a
        # week early, and that spot is a stale price, not an entry.
        sealed_same_day = False
        if sealed:
            try:
                sealed_same_day = (datetime.fromisoformat(sealed).astimezone(JST).date()
                                   == d0)
            except ValueError:
                pass
        entry_basis = "close_event_date"
        if in_session:
            # The release moved the stock before the close. Enter at the sealed spot
            # (10:05 JST, before any release), else at the previous close.
            if spot and sealed_same_day:
                entry, entry_basis = spot, "sealed_spot_before_release"
            elif prev_close:
                entry, entry_basis = prev_close, "previous_close"
        pct = lambda a_, b_: round((b_ / a_ - 1) * 100, 2) if a_ and b_ else None
        move = pct(entry, exitp)
        occurred = None
        if confirmed is not None:
            occurred = code in confirmed
        rows.append({
            "ticker": code,
            "company": bl.get("company"),
            "impact_sum": r.get("impact_sum"),
            "conviction": r.get("conviction"),
            "priced_lean_pct": r.get("priced_lean_pct"),
            "run_up_20d_pct": (bl.get("tape") or {}).get("run_up_20d_pct"),
            "run_up_5d_pct": (bl.get("tape") or {}).get("run_up_5d_pct"),
            "lean_components": bl.get("lean_components") or {},
            "short_ratio_pct": (bl.get("positioning") or {}).get("short_ratio_pct"),
            "margin_ratio": (bl.get("positioning") or {}).get("margin_ratio"),
            "release_time_jst": released_at,
            "released_in_session": in_session if released_at else None,
            "entry_basis": entry_basis,
            "entry_price": entry,
            "entry_close": close_entry, "exit_close": exitp,
            "exit_date": exit_d.isoformat() if exit_d else None,
            "realised_move_pct": move,
            # The pre-2026-10-01 window, kept beside the primary one.
            "move_close_to_close_pct": pct(close_entry, exitp),
            "limit_locked_next_session": limit_hit,
            "event_occurred": occurred,
            "rankable": r.get("rankable"),
        })

    usable = [x for x in rows
              if x["realised_move_pct"] is not None and x["rankable"]
              and x["event_occurred"] is not False and x["impact_sum"] is not None]
    out = {"market": "JP", "event_date": ev, "run": str(run),
           "resolved_utc": datetime.now(ZoneInfo("UTC")).isoformat(timespec="seconds"),
           "tdnet_confirmation": ("skipped" if confirmed is None and a.no_confirm
                                  else "unavailable (page expired)" if confirmed is None
                                  else f"{len(confirmed)} codes disclosed 決算短信 that day"),
           "window_rule": ("exit = close of the next session; entry = event-date close "
                           "for a release at or after 15:30 JST, the sealed 10:05 JST "
                           "spot for a release before it (since 2026-10-01)"),
           "n_in_session": sum(1 for x in rows if x.get("released_in_session")),
           "n_rows": len(rows), "n_usable": len(usable), "rows": rows}

    if len(usable) >= 3:
        ys = [x["realised_move_pct"] for x in usable]
        key = [x["impact_sum"] for x in usable]
        ctl = [-(x["run_up_20d_pct"] or 0.0) for x in usable]
        lean = [x["priced_lean_pct"] or 0.0 for x in usable]
        conv = [x["conviction"] or 0.0 for x in usable]
        sign_ok = [1.0 if (x["impact_sum"] or 0) * (x["realised_move_pct"] or 0) > 0
                   else 0.0 for x in usable]
        r_key = spearman(key, ys)
        r_ctl = spearman(ctl, ys)
        r_lean = spearman(lean, ys)
        r_conv = spearman(conv, sign_ok)
        out["stats"] = {
            "n": len(usable),
            "spearman_impact_sum_vs_move": r_key,
            "permutation_p": perm_p(key, ys, r_key),
            "spearman_free_control_neg_runup": r_ctl,
            # The 5-day window as its own free control. Added after the first live run
            # found the 20-day one netting out a +4.4% five-session run-in. If this
            # out-ranks the 20-day version across pooled days, it is the control the
            # stage has to beat and lean_components should carry it instead.
            "spearman_free_control_neg_runup_5d": spearman(
                [-(x.get("run_up_5d_pct") or 0.0) for x in usable], ys),
            "spearman_priced_lean": r_lean,
            "spearman_conviction_vs_sign_right": r_conv,
            "sign_right_frac": round(sum(sign_ok) / len(sign_ok), 3),
            "median_abs_realised_pct": round(median(abs(y) for y in ys), 2),
            # Every lean component ranked on its own. The weights in
            # jp_priced_in.lean_components() are PRIORS with no Japanese measurement
            # behind them; these are what replaces them. A component that ranks at or
            # below zero across several pooled days should have its weight cut to zero
            # rather than argued for.
            "spearman_lean_components": {
                k: spearman([(x["lean_components"].get(k) or 0.0) for x in usable], ys)
                for k in ("short_squeeze", "short_building", "margin_overhang", "runup")
            },
            "lean_vs_free_control_rho": spearman(lean, ctl),
            "note": "One day is not a result. These pool across days; a single "
                    "day's rho on 4 to 25 names is noise and must not be reported "
                    "as a finding. The free control is the thing to beat. "
                    "`lean_vs_free_control_rho` is the check that the baseline's lean "
                    "has not collapsed back into the control: it was 1.0 by "
                    "construction before 2026-09-18 and is expected around 0.4-0.5. "
                    "If it returns to 1.0 the positioning sources stopped resolving "
                    "and the lean is the run-up again.",
        }
    else:
        out["stats"] = {"n": len(usable),
                        "note": "fewer than 3 usable rows: no statistics computed"}

    text = json.dumps(out, ensure_ascii=False, indent=2)
    dest = Path(a.out) if a.out else run / "jp-resolved.json"
    dest.write_text(text + "\n", encoding="utf-8")
    s = out["stats"]
    print(f"{ev}: {out['n_usable']}/{out['n_rows']} usable. "
          f"rho={s.get('spearman_impact_sum_vs_move')} "
          f"p={s.get('permutation_p')} control={s.get('spearman_free_control_neg_runup')} "
          f"-> {dest}")


if __name__ == "__main__":
    main()
