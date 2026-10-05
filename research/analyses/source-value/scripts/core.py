"""The one place outcomes meet labels. Everything in METHODS.md is implemented here.

load()      events (de-duplicated prints) and items with their v1 labels merged in
Engine      within-day permutation engine over prints, per stratum and horizon
cell stats  DV, DV*, hit rate, MV, contrasts, cluster-robust SE
shrink()    normal-normal empirical Bayes, top-down
lodo()      leave-one-day-out sign share
power_n()   prints needed for a 10-point hit-rate gap at 80% power
"""
import json, math, os, random, statistics as st
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
SEED = 20261005
WINS = 4.0
VERSION = 'v1'


def sgn(x):
    return (x > 0) - (x < 0) if x is not None else 0


def wins(x, c=WINS):
    return max(-c, min(c, x))


# ------------------------------------------------------------------ load
def codebook():
    return json.load(open(f'{SV}/codebook/codebook-{VERSION}.json'))


def merge_map():
    p = f'{SV}/codebook/merges-{VERSION}.json'
    return json.load(open(p))['map'] if os.path.exists(p) else {}


def load_labels(version=VERSION, root=None):
    root = root or f'{SV}/labels/{version}'
    per = defaultdict(list)
    for r in sorted(d for d in os.listdir(root) if d.startswith('run')):
        for f in os.listdir(f'{root}/{r}'):
            if f.endswith('.json'):
                j = json.load(open(f'{root}/{r}/{f}'))
                per[j['pack']].append({x['i']: x for x in j['items']})
    return per


BOOL_FLAGS = ('quantified', 'dated_in_window', 'about_focal_company', 'primary_document', 'already_widely_reported', 'contradicted_in_pack')


def merged_label(runs, mm, groups):
    """Two runs of one item -> one record. Subtype as weights (half each on disagreement)."""
    sub = Counter()
    for r in runs:
        s = r.get('subtype')
        s = mm.get(s, s)
        sub[s] += 1.0 / len(runs)
    d = st.mean([sgn(r.get('direction') or 0) for r in runs])
    out = {'subtype_w': dict(sub), 'subtype': sub.most_common(1)[0][0], 'subtype_agree': len(sub) == 1,
           'vote': sgn(d), 'dir_agree': len({sgn(r.get('direction') or 0) for r in runs}) == 1,
           'group': groups.get(sub.most_common(1)[0][0])}
    for f in BOOL_FLAGS:
        v = [bool(r.get(f)) for r in runs if r.get(f) is not None]
        out[f] = (st.mean(v) if v else None)
    nis = [r.get('n_independent_sources') for r in runs if isinstance(r.get('n_independent_sources'), (int, float))]
    out['n_indep'] = st.mean(nis) if nis else None
    mags = [r.get('magnitude_claim') for r in runs]
    out['magnitude_claim'] = Counter(mags).most_common(1)[0][0]
    out['magnitude_agree'] = len(set(mags)) == 1
    langs = [str(r.get('language') or 'en').lower()[:2] for r in runs]
    out['language'] = Counter(langs).most_common(1)[0][0]
    return out


def naive_fit(events):
    """naive_n per print: leave-day-out mean move_n of its stratum x band + run-up slope."""
    for h in ('strategy', 'open', 'close'):
        for e in events:
            e.setdefault('y', {})
            e.setdefault('res', {})
        for e in events:
            y = e['y'].get(h)
            if y is None:
                continue
            band = e['cap_band'] if e['stratum'] != 'C' else e['turnover_band']
            pool = [o for o in events if o['stratum'] == e['stratum'] and o['perm_day'] != e['perm_day'] and o['y'].get(h) is not None]
            same = [o['y'][h] for o in pool if (o['cap_band'] if o['stratum'] != 'C' else o['turnover_band']) == band]
            mu = st.mean(same) if len(same) >= 5 else (st.mean([o['y'][h] for o in pool]) if pool else 0.0)
            ru = [(o['runup_20d'], o['y'][h]) for o in pool if o.get('runup_20d') is not None]
            slope, xm = 0.0, 0.0
            if len(ru) >= 10:
                xm = st.mean(x for x, _ in ru)
                ym = st.mean(v for _, v in ru)
                sxx = sum((x - xm) ** 2 for x, _ in ru)
                slope = sum((x - xm) * (v - ym) for x, v in ru) / sxx if sxx else 0.0
            naive = mu + (slope * (e['runup_20d'] - xm) if e.get('runup_20d') is not None else 0.0)
            e['res'][h] = wins(y - naive)
            e.setdefault('naive', {})[h] = naive


def load(version=VERSION, label_root=None):
    E = json.load(open(f'{SV}/data/events.json'))
    I = json.load(open(f'{SV}/data/items.json'))
    M = json.load(open(f'{SV}/data/mechanical.json'))
    cb = codebook()
    groups = {s['id']: s['group'] for s in cb['subtypes']}
    mm = merge_map()
    for s, t in mm.items():
        groups.setdefault(t, groups.get(s))
    L = load_labels(version, label_root)
    keep = [e for e in E if not e['duplicate_hunt']]
    ev = {e['id']: e for e in keep}
    for e in keep:
        pm = e['priced_move']
        y = {}
        for h, k in (('strategy', 'move_strategy'), ('open', 'move_open'), ('close', 'move_close')):
            if e.get(k) is not None:
                y[h] = wins(e[k] / pm)
        if e['stratum'] in ('B', 'C'):
            y['strategy'] = wins(e['move'] / pm)
        e['y'] = y
        e['y_raw'] = e['move'] / pm
        e['big'] = abs(e['move']) / pm > 1
    naive_fit(keep)
    items = []
    for it in I:
        e = ev.get(it['event'])
        if e is None:
            continue
        runs = [r[it['i']] for r in L.get(it['pack_id'], []) if it['i'] in r]
        if not runs:
            continue
        x = dict(it)
        x.update(M.get(f"{it['pack_id']}#{it['i']}", {}))
        x.update(merged_label(runs, mm, groups))
        x['ev'] = e
        items.append(x)
    return keep, items


# ------------------------------------------------------------------ permutation engine
class Engine:
    """Within-day shuffles of the per-print outcome vector, shared by every question."""

    def __init__(self, events, n=2000, seed=SEED):
        self.events = events
        self.keys = [e['id'] for e in events]
        self.idx = {k: j for j, k in enumerate(self.keys)}
        days = defaultdict(list)
        for e in events:
            days[e['perm_day']].append(self.idx[e['id']])
        rnd = random.Random(seed)
        self.perms = []
        for _ in range(n):
            p = list(range(len(self.keys)))
            for d in days.values():
                sh = d[:]
                rnd.shuffle(sh)
                for a, b in zip(d, sh):
                    p[a] = b
            self.perms.append(p)
        self.n = n

    def vec(self, kind, h):
        out = []
        for e in self.events:
            if kind == 'res':
                out.append(e['res'].get(h))
            elif kind == 'y':
                out.append(e['y'].get(h))
            elif kind == 'big':
                out.append(1.0 if e['big'] else 0.0)
        return out


def item_agg(items, eng):
    """Per print: w_up, w_dn (weighted voting items), w_all."""
    up, dn, al = defaultdict(float), defaultdict(float), defaultdict(float)
    for x in items:
        w = x.get('w', 1.0)
        j = eng.idx.get(x['ev']['id'])
        if j is None:
            continue
        al[j] += w
        if x['vote'] > 0:
            up[j] += w
        elif x['vote'] < 0:
            dn[j] += w
    return up, dn, al


def dv_stat(up, dn, y, perm=None):
    num = den = 0.0
    for j in set(up) | set(dn):
        v = y[perm[j]] if perm else y[j]
        if v is None:
            continue
        a = up.get(j, 0.0) - dn.get(j, 0.0)
        num += a * v
        den += up.get(j, 0.0) + dn.get(j, 0.0)
    return num / den if den else None


def hit_stat(up, dn, y, perm=None):
    num = den = 0.0
    for j in set(up) | set(dn):
        v = y[perm[j]] if perm else y[j]
        if v is None or v == 0:
            continue
        num += up.get(j, 0.0) * (v > 0) + dn.get(j, 0.0) * (v < 0)
        den += up.get(j, 0.0) + dn.get(j, 0.0)
    return num / den if den else None


def cluster_se(up, dn, y):
    rows = []
    for j in set(up) | set(dn):
        if y[j] is None:
            continue
        rows.append((up.get(j, 0.0) - dn.get(j, 0.0), up.get(j, 0.0) + dn.get(j, 0.0), y[j]))
    W = sum(w for _, w, _ in rows)
    if W == 0 or len(rows) < 2:
        return None
    m = sum(a * v for a, _, v in rows) / W
    n = len(rows)
    var = sum((a * v - m * w) ** 2 for a, w, v in rows) / W ** 2 * n / (n - 1)
    return math.sqrt(var)


def name_stat(present, y, perm=None, idxs=None):
    """mean y over present prints minus mean over the rest (idxs = universe)."""
    a, b = [], []
    for j in idxs:
        v = y[perm[j]] if perm else y[j]
        if v is None:
            continue
        (a if j in present else b).append(v)
    if not a or not b:
        return None
    return st.mean(a) - st.mean(b)


def perm_test(fn, eng):
    obs = fn(None)
    if obs is None:
        return {'stat': None}
    null = [v for v in (fn(p) for p in eng.perms) if v is not None]
    mu = st.mean(null)
    sd = st.pstdev(null) or 1e-12
    p = (1 + sum(abs(v - mu) >= abs(obs - mu) - 1e-12 for v in null)) / (1 + len(null))
    return {'stat': obs, 'null_mean': mu, 'null_sd': sd, 'z': (obs - mu) / sd, 'p': p, 'null': null}


# ------------------------------------------------------------------ shrinkage
def dl_tau2(ys, ss):
    pairs = [(y, s) for y, s in zip(ys, ss) if y is not None and s and s > 0]
    if len(pairs) < 2:
        return 0.0
    w = [1 / s ** 2 for _, s in pairs]
    ybar = sum(wi * y for wi, (y, _) in zip(w, pairs)) / sum(w)
    Q = sum(wi * (y - ybar) ** 2 for wi, (y, _) in zip(w, pairs))
    c = sum(w) - sum(wi ** 2 for wi in w) / sum(w)
    return max(0.0, (Q - (len(pairs) - 1)) / c) if c > 0 else 0.0


def shrink_level(children, parent_est, parent_sd):
    """children: {key: (y, s, n_vote)} -> {key: (shrunk, post_sd, B)}"""
    tau2 = dl_tau2([c[0] for c in children.values()], [c[1] for c in children.values()])
    out = {}
    for k, (y, s, n) in children.items():
        if y is None or s is None or n < 3 or s == 0:
            out[k] = (parent_est, parent_sd, 0.0)
            continue
        B = tau2 / (tau2 + s ** 2) if (tau2 + s ** 2) > 0 else 0.0
        est = parent_est + B * (y - parent_est)
        sd = math.sqrt(B * s ** 2 + (1 - B) ** 2 * parent_sd ** 2)
        out[k] = (est, sd, B)
    return out, tau2


# ------------------------------------------------------------------ power
def power_n(m_items_per_print=1.0, two_arm=False, gap=0.10):
    z = 1.959964 + 0.841621
    n = z ** 2 * 0.25 / gap ** 2
    if two_arm:
        n *= 2
    deff = 1 + max(0.0, m_items_per_print - 1) * 0.3
    return math.ceil(n * deff)


def bh(ps):
    """Benjamini-Hochberg q for a list (None passes through)."""
    idx = [i for i, p in enumerate(ps) if p is not None]
    m = len(idx)
    order = sorted(idx, key=lambda i: ps[i])
    q = [None] * len(ps)
    prev = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        prev = min(prev, ps[i] * m / rank)
        q[i] = prev
    return q
