#!/usr/bin/env python3
"""Judge lab: test ways of turning a hunt's findings into a score, on a fixed split.

The question is narrow on purpose: which way of scoring the findings puts the right
names in the TOP ~20% of each day. Nothing is measured on the other 80% except as
context, because the book only ever trades the top.

Data. Every resolved, hunted name in key.json of the full re-judge (US, Europe, Japan,
Australia): the live hunter's findings with their own sizes, the sealed baseline and the
realised move (US: the strategy exit; elsewhere the market's resolver window).

Split. Whole days, never names, so one print never sits on both sides. Days whose runs
LESSONS.md was written from are forced into train: the hunter already learned from
them, so they cannot validate anything. The rest is assigned once, by a seeded shuffle
balanced on name count, WITHOUT looking at any outcome, and frozen in split.json. A
split that is re-drawn after seeing results is not a split.

Test. `score` never prints test numbers unless `--unseal` is given, and every unseal is
appended to TEST-LOG.md with the variants it opened. Open it once, for variants that
were chosen on train and validation alone. Opening it twice turns it into a second
validation set and the log says so.

Selection. Per day, the k = max(1, round(share x n)) names with the largest |score| are
traded on the sign of the score. Per day, because the hunter's scale moved on
2026-09-23 (Opus 5.5) and again on 2026-10-01 (the shared core): a pooled absolute
threshold would select one era. Days with fewer than 3 names are skipped.

  python3 judge_lab.py split               # build split.json once (refuses to redraw)
  python3 judge_lab.py score               # train / validation / cross-validation
  python3 judge_lab.py score --unseal v1,v2   # also the test set, logged
  python3 judge_lab.py packs --split val --out x.json   # re-judge packs for a model judge
"""
import argparse, glob, json, math, os, random, re, statistics as st, sys
from datetime import datetime, timezone

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
D = os.path.dirname(os.path.abspath(__file__))
KEY = f'{R}/researcher_us/analysis/rejudge-full-2026-10-01/key.json'
REJ = f'{R}/researcher_us/analysis/rejudge-full-2026-10-01'
SPLIT = f'{D}/split.json'
TESTLOG = f'{D}/TEST-LOG.md'
SEED = 20261001
SHARES = {'train': 0.6, 'val': 0.2, 'test': 0.2}
# runs the LESSONS files were written from (their own provenance lines)
LESSON_DAYS = {'us': {'2026-09-08', '2026-09-09', '2026-09-10', '2026-09-11', '2026-09-14'},
               'europe': {'2026-09-16', '2026-09-19', '2026-09-22', '2026-09-28'},
               'japan': {'2026-09-11', '2026-09-18'}, 'australia': set()}
TOP = 0.15
SHARES_REPORTED = (0.10, 0.15, 0.20)
ERA_BREAK = '2026-09-23'   # hunters moved to Opus 5.5; the scale of impact_sum fell
# assumed round trip in % by 20-day turnover, as in score_full.py: an assumption, not a fit
COST = [(1e6, 2.0), (5e6, 1.0), (25e6, 0.5), (float('inf'), 0.2)]

# ---------------------------------------------------------------- data
CATS = [('positioning', r'short interest|short position|days to cover|short base|squeeze|borrow|put/call|open interest|skew|crowded|positioning'),
        ('guidance', r'guid|outlook|forecast|target'),
        ('bar', r'consensus|estimate|whisper|bar |the bar|expectation'),
        ('insider', r'insider|form 4|director|buyback|repurchas'),
        ('peer_macro', r'peer|read-through|readthrough|sector|tariff|macro|commodity|price of '),
        ('channel', r'traffic|app download|card data|channel|survey|web|search volume|pricing|backlog|order')]

def cat_of(f):
    lo = (f.get('lands_on') or '').lower()
    if lo:
        for c, _ in CATS:
            if c.split('_')[0] in lo: return c
    t = (f.get('finding') or '').lower()
    for c, rx in CATS:
        if re.search(rx, t): return c
    return 'other'

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def load():
    rows = []
    for r in json.load(open(KEY)):
        if r.get('move') is None: continue
        hs = sorted(glob.glob(f"{R}/{r['run']}/hunts/{r['ticker']}.json") + glob.glob(f"{R}/{r['run']}/hunts/{r['ticker']}-*.json"))
        if not hs: continue
        F, outside, nothing, emv = [], 0, 0, []
        for h in hs:
            j = json.load(open(h))
            F += [f for f in j.get('findings') or [] if num(f.get('expected_impact_pct')) is not None]
            outside += len(j.get('outside_window') or []); nothing += len(j.get('searched_and_found_nothing') or [])
            if num(j.get('expected_move_pct')) is not None: emv.append(num(j['expected_move_pct']))
        b = json.load(open(f"{R}/{r['baseline']}"))
        tape, opt, hist = b.get('tape') or {}, b.get('options') or {}, b.get('history') or {}
        imp = [num(f['expected_impact_pct']) / len(hs) for f in F]  # one hunt's worth if double-hunted
        width = [num(f.get('impact_high_pct')) - num(f.get('impact_low_pct')) for f in F
                 if num(f.get('impact_high_pct')) is not None and num(f.get('impact_low_pct')) is not None]
        srcs = {re.sub(r'^https?://(www\.)?', '', (f.get('source') or '')).split('/')[0] for f in F if f.get('source')}
        cats = {}
        for f, v in zip(F, imp): cats[cat_of(f)] = cats.get(cat_of(f), 0) + v
        em = b.get('expected_move') if isinstance(b.get('expected_move'), dict) else {}
        implied = num(opt.get('event_implied_move_pct')) or num(em.get('pct')) or num(b.get('expected_move_pct'))
        rows.append(dict(
            id=r['id'], region=r['region'], day=r['day'], ticker=r['ticker'], leak=r.get('leak'),
            move=r['move'], dv=r.get('dollar_vol') or 0, live=float(r['live'] or 0),
            session=b.get('session'), n_hunts=len(hs),
            f=imp, cats=cats, n_f=len(F), n_src=len(srcs), outside=outside, nothing=nothing,
            width=st.mean(width) if width else None, emv=st.mean(emv) if emv else None,
            run20=num(tape.get('run_up_20d_pct')), run5=num(tape.get('run_up_5d_pct')),
            implied=implied, hist=num(hist.get('median_abs_move_pct')),
            lean=num(b.get('priced_lean_pct')), vol=num(tape.get('realised_vol_20d_annualised_pct'))))
    return rows

def tradable(r): return r['region'] != 'us' or r['dv'] >= 2e5
def cost(r): return next(c for lim, c in COST if r['dv'] < lim)

# ---------------------------------------------------------------- split
def make_split(rows):
    if os.path.exists(SPLIT): sys.exit(f'{SPLIT} exists. It is frozen; delete it by hand only if no result was read on it.')
    groups = {}
    for r in rows: groups.setdefault((r['region'], r['day']), 0); groups[(r['region'], r['day'])] += 1
    assign, count = {}, {s: 0 for s in SHARES}
    for g, n in groups.items():
        if g[1] in LESSON_DAYS.get(g[0], ()): assign[g] = 'train'; count['train'] += n
    rest = sorted(g for g in groups if g not in assign); random.Random(SEED).shuffle(rest)
    tot = sum(groups.values())
    for g in rest:
        s = min(SHARES, key=lambda s: count[s] / tot - SHARES[s]); assign[g] = s; count[s] += groups[g]
    out = {'made_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'seed': SEED,
           'rule': 'whole days; LESSONS days forced to train; seeded shuffle balanced on name count; no outcome read',
           'counts': count, 'days': {f'{g[0]}/{g[1]}': s for g, s in sorted(assign.items())}}
    json.dump(out, open(SPLIT, 'w'), indent=1); print(json.dumps(count))

def split_of(r, S): return S['days'].get(f"{r['region']}/{r['day']}")

# ---------------------------------------------------------------- tiny linear models
def standardise(X, mu=None, sd=None):
    cols = list(zip(*X))
    if mu is None:
        mu = [st.mean(c) for c in cols]; sd = [st.pstdev(c) or 1 for c in cols]
    return [[(x - m) / s for x, m, s in zip(row, mu, sd)] for row in X], mu, sd

def ridge(X, y, lam):
    """Closed form by Gauss-Jordan on (X'X + lam I) w = X'y, intercept unpenalised."""
    X = [[1.0] + row for row in X]; p = len(X[0])
    A = [[sum(X[k][i] * X[k][j] for k in range(len(X))) + (lam if i == j and i else 0) for j in range(p)] for i in range(p)]
    b = [sum(X[k][i] * y[k] for k in range(len(X))) for i in range(p)]
    M = [A[i] + [b[i]] for i in range(p)]
    for c in range(p):
        piv = max(range(c, p), key=lambda r: abs(M[r][c])); M[c], M[piv] = M[piv], M[c]
        if abs(M[c][c]) < 1e-12: continue
        for r in range(p):
            if r != c:
                f = M[r][c] / M[c][c]; M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][p] / M[i][i] if abs(M[i][i]) > 1e-12 else 0 for i in range(p)]

def logistic(X, y, lam, it=600, lr=0.1):
    p = len(X[0]) + 1; w = [0.0] * p; n = len(X)
    for _ in range(it):
        g = [0.0] * p
        for row, t in zip(X, y):
            z = w[0] + sum(a * b for a, b in zip(w[1:], row)); q = 1 / (1 + math.exp(-max(-30, min(30, z))))
            g[0] += q - t
            for j, a in enumerate(row): g[j + 1] += (q - t) * a
        w = [wi - lr * (gi / n + (lam * wi / n if j else 0)) for j, (wi, gi) in enumerate(zip(w, g))]
    return w

def dot(w, row): return w[0] + sum(a * b for a, b in zip(w[1:], row))

# ---------------------------------------------------------------- variants
def z(x): return 0.0 if x is None else x
def sgn(x): return (x > 0) - (x < 0)

def signed_feats(r):
    s = sum(r['f']); pos = sum(v for v in r['f'] if v > 0); neg = sum(v for v in r['f'] if v < 0)
    mx = max(r['f'], key=abs) if r['f'] else 0
    return [s, pos, neg, mx, -z(r['run20']), -z(r['run5']), z(r['lean'])]

def conf_feats(r):
    """Unsigned: what might make the hunt's sign more trustworthy for this name."""
    s = sum(r['f']); a = sum(abs(v) for v in r['f'])
    agree = sgn(s) * sgn(-z(r['run20'])) if s else 0
    return [abs(s), math.log1p(r['n_f']), a and abs(s) / a, math.log1p(r['n_src']),
            z(r['width']), math.log10(max(r['dv'], 1e4)), z(r['implied']) or z(r['hist']),
            abs(z(r['run20'])), agree, 1.0 if r['session'] == 'bmo' else 0.0,
            r['cats'].get('positioning', 0) and abs(r['cats']['positioning']) / (a or 1),
            1.0 if r['region'] == 'us' else 0.0]

class Fixed:
    def __init__(self, name, fn, note): self.name, self.fn, self.note = name, fn, note
    def fit(self, train): return self
    def score(self, r): return self.fn(r)

class Ridge:
    """Signed move regressed on signed features; lambda chosen inside the fit by
    leave-one-day-out over the training days only."""
    note = 'ridge on signed features, lambda by inner leave-one-day-out'
    def __init__(self, name='ridge_signed'): self.name = name
    def fit(self, train, lams=(1, 10, 100, 1000)):
        best = None
        for lam in lams:
            days = sorted({(r['region'], r['day']) for r in train}); pred = {}
            for d in days:
                tr = [r for r in train if (r['region'], r['day']) != d]
                X, mu, sd = standardise([signed_feats(r) for r in tr]); w = ridge(X, [r['move'] for r in tr], lam)
                for r in train:
                    if (r['region'], r['day']) == d: pred[r['id']] = dot(w, standardise([signed_feats(r)], mu, sd)[0][0])
            m = top_metrics(train, pred)['mean']
            if m is not None and (best is None or m > best[0]): best = (m, lam)
        self.lam = best[1] if best else 100
        X, self.mu, self.sd = standardise([signed_feats(r) for r in train]); self.w = ridge(X, [r['move'] for r in train], self.lam)
        return self
    def score(self, r): return dot(self.w, standardise([signed_feats(r)], self.mu, self.sd)[0][0])

class Selector:
    """Keeps the hunt's sign; learns only WHICH names to trust. Logistic on whether the
    hunt's sign was right, sample-weighted toward the large moves the top is made of."""
    note = "live sign x P(sign right) from a logistic on unsigned features"
    def __init__(self, name='selector', lam=5.0): self.name, self.lam = name, lam
    def fit(self, train):
        tr = [r for r in train if sum(r['f']) != 0]
        X, self.mu, self.sd = standardise([conf_feats(r) for r in tr])
        y = [1.0 if sgn(sum(r['f'])) * r['move'] > 0 else 0.0 for r in tr]
        self.w = logistic(X, y, self.lam); return self
    def score(self, r):
        s = sum(r['f'])
        if not s: return 0.0
        q = 1 / (1 + math.exp(-dot(self.w, standardise([conf_feats(r)], self.mu, self.sd)[0][0])))
        return sgn(s) * q

class CatWeights:
    """One multiplier per finding category, set on train to that category's own sign
    hit rate, mapped to 0..2 (0.5 hit -> 1). Shrunk toward 1 by its count."""
    note = 'per-category weight from train hit rate, shrunk by n'
    def __init__(self, name='cat_weights', k=10): self.name, self.k = name, k
    def fit(self, train):
        acc = {}
        for r in train:
            for c, v in r['cats'].items():
                if v: a = acc.setdefault(c, [0, 0]); a[0] += sgn(v) * r['move'] > 0; a[1] += 1
        self.w = {c: 1 + (2 * h / n - 1) * n / (n + self.k) for c, (h, n) in acc.items()}
        return self
    def score(self, r): return sum(v * self.w.get(c, 1) for c, v in r['cats'].items())

def rejudge_arms():
    key = {x['id']: x for x in json.load(open(KEY))}; pid = {x.get('pid', x['id']): x['id'] for x in key.values()}
    arms = {}
    for f in glob.glob(f'{REJ}/out-*-*.json'):
        m = os.path.basename(f)[:-5].split('-')[-1]
        for o in json.load(open(f)):
            if o['id'] in pid: arms.setdefault(m, {})[pid[o['id']]] = float(o.get('impact_sum') or 0)
    return arms

def variants():
    V = [Fixed('live', lambda r: r['live'], 'the impact_sum the live hunt emitted (the book today)'),
         Fixed('signed_max', lambda r: max(r['f'], key=abs) if r['f'] else 0, 'the single largest finding, signed'),
         Fixed('net_count', lambda r: sum(sgn(v) for v in r['f']) + 0.01 * sum(r['f']), 'findings up minus findings down'),
         Fixed('sum_ge1', lambda r: sum(v for v in r['f'] if abs(v) >= 1), 'impact_sum of findings of at least 1 point'),
         Fixed('no_positioning', lambda r: sum(v for c, v in r['cats'].items() if c != 'positioning'), 'impact_sum without positioning findings'),
         Fixed('per_implied', lambda r: r['live'] / max(z(r['implied']) or z(r['hist']) or 5, 1), 'impact_sum over the move the market expects'),
         Fixed('agree_runup', lambda r: r['live'] * (1.5 if sgn(r['live']) == sgn(-z(r['run20'])) else 0.5), 'impact_sum x1.5 where it agrees with -run_up_20d, x0.5 where not'),
         Fixed('ctrl_runup', lambda r: -z(r['run20']), 'free control: minus the 20-day run-up'),
         Fixed('ctrl_short', lambda r: -1e-6 * (1 + random.Random(r['id']).random()), 'short every name, random pick of the top share'),
         CatWeights(), Ridge(), Selector()]
    for m, sc in rejudge_arms().items():
        V.append(Fixed(f'rejudge_{m}', (lambda sc: lambda r: sc.get(r['id']))(sc), f'blinded re-judge, {m}, same evidence (names it did not judge are skipped)'))
    for j in sorted(os.listdir(JUDGES)) if os.path.isdir(JUDGES) else []:
        if j.startswith('_') or not glob.glob(f'{JUDGES}/{j}/out/*.json'): continue
        V.append(Fixed(f'judge_{j}', (lambda sc: lambda r: sc.get(r['id']))(load_judge(j)), f'agent judge {j} (direction x certainty)'))
    return V

# ---------------------------------------------------------------- metrics
def bucket(r):
    return ('us' if r['region'] == 'us' else 'ex', r['day'] >= ERA_BREAK)

def top_metrics(rows, pred, share=TOP):
    """Pooled, not per day: within each bucket (US or not, before or after the 09-23
    scale change) the names with the largest |score| up to `share` of the bucket's
    tradable names are traded on the sign. Zeros are never picked."""
    B = {}
    for r in rows:
        if pred.get(r['id']) is None or not tradable(r): continue
        B.setdefault(bucket(r), []).append(r)
    picks = []
    for v in B.values():
        k = max(1, round(share * len(v)))
        v = sorted(v, key=lambda r: (-abs(pred[r['id']]), r['id']))
        picks += [r for r in v[:k] if pred[r['id']] != 0]
    ret = [sgn(pred[r['id']]) * r['move'] for r in picks]
    net = [x - cost(r) for x, r in zip(ret, picks)]
    allv = [r for v in B.values() for r in v]
    short = [-r['move'] - cost(r) for r in allv]
    return {'n': len(ret), 'hits': sum(x > 0 for x in ret), 'mean': st.mean(ret) if ret else None,
            'net': st.mean(net) if net else None, 'short_all_net': st.mean(short) if short else None,
            't': (st.mean(net) / (st.stdev(net) / len(net) ** .5)) if len(net) > 2 and st.stdev(net) else None,
            'ids': [r['id'] for r in picks]}

def day_metrics(rows, pred, share=TOP):
    days = {}
    for r in rows:
        if pred.get(r['id']) is None or not tradable(r): continue
        days.setdefault((r['region'], r['day']), []).append(r)
    picks = []
    for v in days.values():
        if len(v) < 3: continue
        k = max(1, round(share * len(v)))
        v = sorted(v, key=lambda r: (-abs(pred[r['id']]), r['id']))
        picks += [r for r in v[:k] if pred[r['id']] != 0]
    ret = [sgn(pred[r['id']]) * r['move'] for r in picks]
    net = [x - cost(r) for x, r in zip(ret, picks)]
    short = [-r['move'] - cost(r) for v in days.values() if len(v) >= 3 for r in v]
    out = {'n': len(ret), 'hits': sum(x > 0 for x in ret), 'mean': st.mean(ret) if ret else None,
           'net': st.mean(net) if net else None, 'short_all_net': st.mean(short) if short else None,
           't': (st.mean(net) / (st.stdev(net) / len(net) ** .5)) if len(net) > 2 and st.stdev(net) else None}
    return out

def rank(a):
    s = sorted(range(len(a)), key=lambda i: a[i]); r = [0] * len(a); i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[s[j + 1]] == a[s[i]]: j += 1
        for k in range(i, j + 1): r[s[k]] = (i + j) / 2
        i = j + 1
    return r

def rho(rows, pred):
    days = {}
    for r in rows:
        if pred.get(r['id']) is not None: days.setdefault((r['region'], r['day']), []).append(r)
    num_, den = 0, 0
    for v in days.values():
        if len(v) < 3: continue
        a, b = rank([pred[r['id']] for r in v]), rank([r['move'] for r in v])
        ma, mb = st.mean(a), st.mean(b); d = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** .5
        if d: num_ += len(v) * sum((x - ma) * (y - mb) for x, y in zip(a, b)) / d; den += len(v)
    return num_ / den if den else None

def perm_p(rows, pred, n=500):
    """Share of within-day shuffles of the scores whose top-share net mean is at least
    the observed one: what a random top 20% on the same days does."""
    o = top_metrics(rows, pred)['net']
    if o is None: return None
    days = {}
    for r in rows:
        if pred.get(r['id']) is not None: days.setdefault((r['region'], r['day']), []).append(r['id'])
    rnd = random.Random(SEED); hit = 0
    for _ in range(n):
        p2 = {}
        for ids in days.values():
            v = [pred[i] for i in ids]; rnd.shuffle(v); p2.update(zip(ids, v))
        m = top_metrics(rows, p2)['net']; hit += m is not None and m >= o
    return hit / n

def lodo(V, dev):
    """Leave one day out over train+val: refit, predict the held-out day."""
    pred = {}
    for d in sorted({(r['region'], r['day']) for r in dev}):
        tr = [r for r in dev if (r['region'], r['day']) != d]
        m = V.fit(tr)
        for r in dev:
            if (r['region'], r['day']) == d: pred[r['id']] = m.score(r)
    return pred


# ---------------------------------------------------------------- agent judges
JUDGES = f'{D}/judges'
FOLDS = f'{D}/folds.json'
NFOLD, CHUNK = 3, 24

def make_folds(rows, S):
    """Three folds over the train+validation days, by whole day, balanced on name count,
    seeded, no outcome read. A judge that learns from outcomes learns from two folds and
    judges the third, so every development name gets an out-of-sample judgement."""
    if os.path.exists(FOLDS): return json.load(open(FOLDS))
    g = {}
    for r in rows:
        if split_of(r, S) in ('train', 'val'): g[f"{r['region']}/{r['day']}"] = g.get(f"{r['region']}/{r['day']}", 0) + 1
    keys = sorted(g); random.Random(SEED + 1).shuffle(keys); cnt = [0] * NFOLD; out = {}
    for k in sorted(keys, key=lambda k: -g[k]):
        f = min(range(NFOLD), key=lambda i: cnt[i]); out[k] = f; cnt[f] += g[k]
    json.dump({'rule': 'dev days only; balanced on name count; seeded; no outcome read', 'counts': cnt, 'days': out}, open(FOLDS, 'w'), indent=1)
    return json.load(open(FOLDS))

def fold_of(r, F): return F['days'].get(f"{r['region']}/{r['day']}")

def all_packs():
    key = {x['id']: x for x in json.load(open(KEY))}; back = {v.get('pid', k): k for k, v in key.items()}
    P = {}
    for f in sorted(glob.glob(f'{REJ}/packs-*.json')):
        for p in json.load(open(f)): P[back.get(p['id'], p['id'])] = p
    return P

def build_cases(rows, P):
    key = {x['id']: x for x in json.load(open(KEY))}
    out = {}
    for r in rows:
        p = P.get(r['id'])
        if not p: continue
        k = key[r['id']]
        hs = sorted(glob.glob(f"{R}/{k['run']}/hunts/{k['ticker']}.json") + glob.glob(f"{R}/{k['run']}/hunts/{k['ticker']}-*.json"))
        sized = []
        for h in hs:
            for f in json.load(open(h)).get('findings') or []:
                if num(f.get('expected_impact_pct')) is None: continue
                sized.append((num(f['expected_impact_pct']), (f.get('finding') or '')[:420]))
        b = p.get('baseline') or {}; tape = b.get('tape') or {}; opt = b.get('options') or {}
        name = p['id'] if p['id'].startswith('anon/') else r['id']
        lines = [f"### {name}  ({b.get('session') or r['session']}, {r['region']})",
                 f"baseline: implied move {opt.get('event_implied_move_pct')}, median past reaction {(b.get('history') or {}).get('median_abs_move_pct')}, run-up 20d {tape.get('run_up_20d_pct')} / 5d {tape.get('run_up_5d_pct')}, turnover ${r['dv']/1e6:.1f}m/day"]
        if not sized: lines.append("hunter filed no findings (impact_sum 0)")
        for v, t in sized:
            if p['id'].startswith('anon/'): t = '[text withheld: anonymised case]'
            lines.append(f"- [{v:+.1f}] {t}")
        lines.append(f"hunter impact_sum {r['live']:+.2f}  ->  REALISED MOVE {r['move']:+.2f}%  ({'sign right' if r['live'] and sgn(r['live'])*r['move']>0 else 'sign wrong' if r['live'] else 'no call'})")
        out[r['id']] = '\n'.join(lines)
    return out

def cmd_prepare(a):
    """Write, per fold: the chunked blinded packs to judge, and the casebook of the OTHER
    folds' resolved cases (with outcomes) for judges that learn."""
    rows = load(); S = json.load(open(SPLIT)); F = make_folds(rows, S); P = all_packs()
    dev = [r for r in rows if fold_of(r, F) is not None]
    cases = build_cases(dev, P)
    os.makedirs(f'{JUDGES}/_in', exist_ok=True)
    for k in range(NFOLD):
        mine = sorted([r for r in dev if fold_of(r, F) == k], key=lambda r: r['id'])
        n = max(1, round(len(mine) / CHUNK))
        for c in range(n):
            part = mine[c::n]
            json.dump([P[r['id']] for r in part], open(f'{JUDGES}/_in/fold{k}-c{c}.json', 'w'), ensure_ascii=False, indent=1)
        other = sorted([r for r in dev if fold_of(r, F) != k], key=lambda r: (r['region'], r['day'], r['id']))
        txt = [f"# Casebook for fold {k}: {len(other)} resolved cases from OTHER days\n",
               "Each case: what the hunter filed, with its own signed size in points, its impact_sum, and the move that followed (US: the strategy exit; elsewhere the market's resolver window). Positive move = the stock rose.\n"]
        txt += [cases[r['id']] + '\n' for r in other if r['id'] in cases]
        open(f'{JUDGES}/_in/casebook-fold{k}.md', 'w').write('\n'.join(txt))
        print(f"fold {k}: {len(mine)} names in {n} chunks; casebook {len(other)} cases")

def load_judge(name):
    """A judge's outputs: score = direction x certainty, ties broken by |impact_sum|."""
    key = {x['id']: x for x in json.load(open(KEY))}; back = {v.get('pid', k): k for k, v in key.items()}
    sc = {}
    for f in glob.glob(f'{JUDGES}/{name}/out/*.json'):
        for o in json.load(open(f)):
            i = back.get(o['id'], o['id']); d = sgn(num(o.get('direction')) or 0)
            c = num(o.get('certainty')) or 0; im = abs(num(o.get('impact_sum')) or 0)
            sc[i] = d * (c + min(im, 50) / 100)
    return sc


def cmd_compare(a):
    """Every judge and re-judge against live on the names they all covered, out of sample:
    agent judges that learn only ever saw the other two folds."""
    rows = load(); F = make_folds(rows, json.load(open(SPLIT)))
    dev = [r for r in rows if fold_of(r, F) is not None]
    arms = {'live': {r['id']: r['live'] for r in dev}}
    for m, sc in sorted(rejudge_arms().items()): arms['rejudge_' + m] = sc
    for j in sorted(os.listdir(JUDGES)):
        if not j.startswith('_') and glob.glob(f'{JUDGES}/{j}/out/*.json'): arms['judge_' + j] = load_judge(j)
    common = [r for r in dev if all(r['id'] in v for v in arms.values())]
    out = {'n': len(common), 'arms': {}}
    print(f"{len(common)} development names judged by every arm; pooled top share within bucket, net of assumed cost; p = within-day shuffle")
    for g, f in [('all', lambda r: True), ('us', lambda r: r['region'] == 'us'), ('ex_us', lambda r: r['region'] != 'us')]:
        sub = [r for r in common if f(r)]
        print(f"== {g} ({len(sub)} names)   {'top 10%':>24s} {'top 15%':>30s} {'top 20%':>24s}")
        for name, sc in arms.items():
            p = {r['id']: sc[r['id']] for r in sub}; cells = []
            for q in SHARES_REPORTED:
                m = top_metrics(sub, p, q)
                out['arms'].setdefault(name, {}).setdefault(g, {})[f'{q:.2f}'] = {k: v for k, v in m.items() if k != 'ids'}
                cells.append(f"{m['hits']:2d}/{m['n']:<2d} {m['net']:+6.2f}%" if m['n'] else '   -   ')
            global TOP
            old, TOP = TOP, 0.15; pp = perm_p(sub, p); TOP = old
            out['arms'][name][g]['perm_p_15'] = pp
            print(f"  {name:18s} {cells[0]:>16s}   {cells[1]:>16s} p {pp:.2f}   {cells[2]:>16s}")
    json.dump(out, open(f'{D}/compare.json', 'w'), indent=1)

# ---------------------------------------------------------------- commands
def fmt(m):
    if not m['n']: return f"{'0':>3s} {'':>6s} {'':>7s} {'':>7s} {'':>5s}"
    t = f"{m['t']:+5.2f}" if m['t'] is not None else '    -'
    return f"{m['n']:3d} {m['hits']:2d}/{m['n']:<3d} {m['mean']:+6.2f}% {m['net']:+6.2f}% {t}"

def cmd_score(a):
    rows = load(); S = json.load(open(SPLIT))
    for r in rows: r['split'] = split_of(r, S)
    if a.region: rows = [r for r in rows if (r['region'] == 'us') == (a.region == 'us')]
    by = {s: [r for r in rows if r['split'] == s] for s in SHARES}
    dev = by['train'] + by['val']
    unseal = [x for x in (a.unseal or '').split(',') if x]
    print(f"names: train {len(by['train'])}, val {len(by['val'])}, test {len(by['test'])} (sealed){'' if not unseal else ' -- UNSEALED for ' + ','.join(unseal)}")
    print(f"top {TOP:.0%} by |score| pooled within bucket (US or not x before/after {ERA_BREAK}), traded on its sign; net after an assumed cost")
    sa = top_metrics(by['val'], {r['id']: -1 for r in by['val']}, 1.0)
    print(f"short every tradable val name, net: {sa['net']:+.2f}% on {sa['n']}")
    hdr = f"{'variant':16s} | {'TRAIN (fit here)':^34s} | {'VALIDATION':^34s} | {'LEAVE-ONE-DAY-OUT on train+val':^40s}"
    print(hdr); print('-' * len(hdr))
    res = {}
    for V in variants():
        m = V.fit(by['train'])
        ptr = {r['id']: m.score(r) for r in by['train']}
        pva = {r['id']: m.score(r) for r in by['val']}
        pcv = lodo(V, dev)
        tr, va, cv = top_metrics(by['train'], ptr), top_metrics(by['val'], pva), top_metrics(dev, pcv)
        rcv, pcv_p = rho(dev, pcv), perm_p(dev, pcv)
        res[V.name] = dict(note=V.note, train=tr, val=va, lodo=cv, lodo_rho=rcv, lodo_perm_p=pcv_p,
                           lodo_by_share={f'{q:.2f}': top_metrics(dev, pcv, q) for q in SHARES_REPORTED},
                           lodo_per_day=day_metrics(dev, pcv))
        print(f"{V.name:16s} | {fmt(tr)} | {fmt(va)} | {fmt(cv)} p {'-' if pcv_p is None else f'{pcv_p:.2f}'} rho {'-' if rcv is None else f'{rcv:+.2f}'}")
        if V.name in unseal:
            m = V.fit(dev); pte = {r['id']: m.score(r) for r in by['test']}
            res[V.name]['test'] = top_metrics(by['test'], pte)
    out = {'run_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'region': a.region or 'all',
           'top_share': TOP, 'cost_assumption': COST, 'variants': res}
    json.dump(out, open(f"{D}/results-{a.region or 'all'}.json", 'w'), indent=1)
    if unseal:
        print('\nTEST (fit on train+val, opened now):')
        for n in unseal:
            if 'test' in res.get(n, {}): print(f"{n:16s} | {fmt(res[n]['test'])}")
        with open(TESTLOG, 'a') as fh:
            fh.write(f"- {out['run_utc']} region={out['region']} unsealed: {', '.join(unseal)}\n")

def cmd_packs(a):
    """Write the re-judge packs of one split, so a model judge can be run on them."""
    S = json.load(open(SPLIT)); want = {r['id'] for r in load() if split_of(r, S) == a.split}
    key = {x['id']: x for x in json.load(open(KEY))}
    out = []
    for f in sorted(glob.glob(f'{REJ}/packs-*.json')):
        for p in json.load(open(f)):
            rid = next((k for k, v in key.items() if v.get('pid', k) == p['id']), p['id'])
            if rid in want: out.append(p)
    json.dump(out, open(a.out, 'w'), ensure_ascii=False); print(f'{len(out)} packs of {len(want)} {a.split} names -> {a.out}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('split')
    sp.add_parser('prepare')
    sp.add_parser('compare')
    s = sp.add_parser('score'); s.add_argument('--unseal'); s.add_argument('--region', choices=['us', 'ex_us'])
    p = sp.add_parser('packs'); p.add_argument('--split', required=True, choices=list(SHARES)); p.add_argument('--out', required=True)
    a = ap.parse_args()
    if a.cmd == 'split': make_split(load())
    elif a.cmd == 'score': cmd_score(a)
    elif a.cmd == 'prepare': cmd_prepare(a)
    elif a.cmd == 'compare': cmd_compare(a)
    else: cmd_packs(a)
