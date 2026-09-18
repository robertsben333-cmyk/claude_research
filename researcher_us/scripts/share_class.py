#!/usr/bin/env python3
"""One issuer is one event, however many share classes it lists.

Lennar reported once on 2026-09-16 and the day's universe carried it twice, as LEN
and LEN.B. Both were hunted, both were ranked, and the run log had to say in prose
that `edge_resolve.py` would score one print as two events. Two rows off one release
are not two observations: they share every fundamental, so the day's rank correlation
is computed on a sample that is smaller than it looks and a book can end up with two
correlated legs on one thesis.

Detection is deliberately narrow. A class suffix is a single letter after a dot or a
dash (`LEN.B`, `BRK.A`, `GEF-B`), and it only collapses when the unsuffixed ticker is
in the same day's universe with the same event date. A company that only lists a
suffixed class is left exactly where it is -- it is the issuer, not a duplicate.

    from share_class import base_of, collapse
"""
import re

SUFFIX = re.compile(r"^(?P<base>[A-Z]{1,5})[.\-](?P<cls>[A-Z])$")


def base_of(ticker):
    """`LEN.B` -> `LEN`. Anything without a single-letter class suffix returns None."""
    m = SUFFIX.match((ticker or "").strip().upper())
    return m.group("base") if m else None


def collapse(names, key=lambda x: x):
    """Split a universe into the names to hunt and the share classes folded into them.

    `names` is a list of dicts carrying `ticker` and `event_date`. Returns
    (kept, folded); each folded row gains `share_class_of` and `folded_because`.
    The unsuffixed listing is the one kept, because it is the one with the borrow,
    the options and the volume -- and a hunt on the thin class is the one that would
    have been refused at the turnover floor anyway.
    """
    by_ticker = {}
    for x in names:
        by_ticker.setdefault(str(key(x).get("ticker") or "").upper(), []).append(x)

    kept, folded = [], []
    for x in names:
        row = key(x)
        t = str(row.get("ticker") or "").upper()
        base = base_of(t)
        primary = None
        if base:
            for cand in by_ticker.get(base, []):
                if key(cand).get("event_date") == row.get("event_date"):
                    primary = cand
                    break
        if primary is None:
            kept.append(x)
            continue
        row["share_class_of"] = base
        row["folded_because"] = (
            f"second share class of {base}, same issuer and the same release on "
            f"{row.get('event_date')}: one issuer is one event")
        folded.append(x)
    return kept, folded
