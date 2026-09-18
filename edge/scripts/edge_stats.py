#!/usr/bin/env python3
"""The statistics the edge scripts share, with the same conventions throughout.

Three choices are made here once rather than argued three times:

PERMUTATION, NOT A TABLE. Every p-value over a rank correlation is a permutation
p-value. The sample is 106 events over 13 days with a long-tailed return
distribution and repeated tickers; a t-distribution p on Spearman's rho assumes
none of that.

WITHIN-DAY WHERE THE QUESTION IS A RANKING. A ranking question asks whether the
day's names sort correctly, so days are ranked internally, centred, and the centred
ranks pooled. Concatenating raw pairs across days lets market-wide drift into the
rank structure -- `edge/EDGE_ANALYSIS.md` measures that at 0.189 against 0.243 for
the same ranker.

THE DAY IS THE UNIT FOR A RETURN. A book is placed once a day and its names share a
market, so bootstrap intervals over returns resample DAYS, not events. Resampling
events would treat 22 names bought on one morning as 22 independent draws.
"""
import math
import random
import statistics as st
from math import comb


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for m in range(i, j + 1):
            out[order[m]] = avg
        i = j + 1
    return out


def pearson(a, b):
    if len(a) < 2:
        return float("nan")
    ma, mb = st.mean(a), st.mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(len(a)))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b))
    return num / den if den else 0.0


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def spearman_perm(a, b, n=20000, seed=20260918):
    """rho and a two-sided permutation p from shuffling b against a."""
    rho = spearman(a, b)
    if len(a) < 3 or math.isnan(rho):
        return rho, float("nan")
    rng = random.Random(seed)
    ra, rb = ranks(a), list(ranks(b))
    hits = 0
    for _ in range(n):
        rng.shuffle(rb)
        if abs(pearson(ra, rb)) >= abs(rho) - 1e-12:
            hits += 1
    return rho, (hits + 1) / (n + 1)


def within_day(days, xkey, ykey):
    """Centre each day's ranks, then pool. `days` is a list of lists of dicts."""
    xs, ys = [], []
    for d in days:
        rows = [r for r in d if r.get(xkey) is not None and r.get(ykey) is not None]
        if len(rows) < 2:
            continue
        rx = ranks([r[xkey] for r in rows])
        ry = ranks([r[ykey] for r in rows])
        mx, my = st.mean(rx), st.mean(ry)
        xs += [v - mx for v in rx]
        ys += [v - my for v in ry]
    return xs, ys


def within_day_perm(days, xkey, ykey, n=20000, seed=20260918):
    xs, ys = within_day(days, xkey, ykey)
    if len(xs) < 3:
        return float("nan"), float("nan"), len(xs)
    rho = pearson(xs, ys)
    rng = random.Random(seed)
    # permute the realised side WITHIN each day, which is the null that matters:
    # "this day's names could have been ordered any way"
    blocks, i = [], 0
    for d in days:
        rows = [r for r in d if r.get(xkey) is not None and r.get(ykey) is not None]
        if len(rows) < 2:
            continue
        blocks.append((i, i + len(rows)))
        i += len(rows)
    hits = 0
    for _ in range(n):
        sh = list(ys)
        for a, b in blocks:
            seg = sh[a:b]
            rng.shuffle(seg)
            sh[a:b] = seg
        if abs(pearson(xs, sh)) >= abs(rho) - 1e-12:
            hits += 1
    return rho, (hits + 1) / (n + 1), len(xs)


def tstat(xs):
    if len(xs) < 2:
        return float("nan")
    sd = st.stdev(xs)
    return st.mean(xs) / (sd / math.sqrt(len(xs))) if sd else float("nan")


def boot_days(day_values, n=20000, seed=20260918):
    """95% CI on the mean, resampling DAYS with replacement.

    `day_values` is a list of per-day lists of returns. The statistic is the mean
    over all events in the resampled days, so a day with more names carries more
    weight -- the same weighting a real equal-weight book would have.
    """
    days = [d for d in day_values if d]
    if len(days) < 2:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        pick = [days[rng.randrange(len(days))] for _ in range(len(days))]
        flat = [v for d in pick for v in d]
        if flat:
            out.append(st.mean(flat))
    out.sort()
    return (out[int(0.025 * len(out))], out[int(0.975 * len(out))])


def binom_ge(k, n):
    """P(X >= k) under a fair coin. The floor a hit rate has to clear."""
    return sum(comb(n, i) * 0.5 ** n for i in range(k, n + 1))


def summarise(rets):
    """mean, sd, t, hit rate -- the block every table in these scripts prints."""
    if not rets:
        return {"n": 0}
    hits = sum(1 for x in rets if x > 0)
    return {
        "n": len(rets), "hits": hits, "hit_rate": hits / len(rets),
        "mean": st.mean(rets),
        "median": st.median(rets),
        "sd": st.stdev(rets) if len(rets) > 1 else 0.0,
        "t": tstat(rets),
        "binom_p": binom_ge(hits, len(rets)),
    }
