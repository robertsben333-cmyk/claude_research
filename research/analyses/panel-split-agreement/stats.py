import random, math


def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float("nan")


def spearman(a, b):
    return pearson(rank(a), rank(b))


def within_day_rho(groups, n_perm=5000, seed=1):
    """groups: list of (xs, ys) per day. Mean of per-day rho weighted by n, permutation within day."""
    groups = [g for g in groups if len(g[0]) >= 3]
    def stat(gs):
        num = den = 0
        for xs, ys in gs:
            r = spearman(xs, ys)
            if r == r: num += r * len(xs); den += len(xs)
        return num / den if den else float("nan")
    obs = stat(groups); rnd = random.Random(seed); ge = 0
    for _ in range(n_perm):
        gs = []
        for xs, ys in groups:
            y = ys[:]; rnd.shuffle(y); gs.append((xs, y))
        if abs(stat(gs)) >= abs(obs) - 1e-12: ge += 1
    return obs, (ge + 1) / (n_perm + 1), sum(len(g[0]) for g in groups)


def tstat(xs):
    n = len(xs)
    if n < 2: return (sum(xs) / n if n else float("nan")), float("nan"), n
    m = sum(xs) / n; sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return m, (m / (sd / math.sqrt(n)) if sd else float("nan")), n


def pval_t(t, df):
    # two-sided, normal approx for df>=30 else Student via incomplete beta
    if t != t: return float("nan")
    x = df / (df + t * t)
    return betainc(df / 2, 0.5, x)


def betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b + lbeta)
    if x < (a + 1) / (a + b + 2):
        return front * cf(a, b, x) / a
    return 1 - math.exp(math.log(1 - x) * b + math.log(x) * a + lbeta) * cf(b, a, 1 - x) / b


def cf(a, b, x):
    f, c, d = 1.0, 1.0, 0.0
    for i in range(200):
        m = i // 2
        if i == 0: num = 1.0
        elif i % 2 == 0: num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else: num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1 + num * d; d = 1 / d if abs(d) > 1e-30 else 1e30
        c = 1 + num / c if abs(c) > 1e-30 else 1e30
        f *= c * d
        if abs(1 - c * d) < 1e-10: break
    return f - 1


def summ(xs):
    m, t, n = tstat(xs)
    p = pval_t(t, n - 1) if n > 1 else float("nan")
    hit = sum(1 for x in xs if x > 0)
    return dict(n=n, mean=round(m, 2) if m == m else None, t=round(t, 2) if t == t else None,
                p=round(p, 3) if p == p else None, hit=hit)


def welch(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((v - ma) ** 2 for v in a) / (len(a) - 1); vb = sum((v - mb) ** 2 for v in b) / (len(b) - 1)
    se = (va / len(a) + vb / len(b)) ** .5; t = (ma - mb) / se
    df = (va / len(a) + vb / len(b)) ** 2 / ((va / len(a)) ** 2 / (len(a) - 1) + (vb / len(b)) ** 2 / (len(b) - 1))
    return round(ma - mb, 2), round(t, 2), round(pval_t(t, df), 3)
