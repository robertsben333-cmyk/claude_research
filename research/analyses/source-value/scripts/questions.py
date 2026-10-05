#!/usr/bin/env python3
"""Phase 3: the question ledger.

  python3 scripts/questions.py register <batch.json>   # appends the batch to ledger/questions.jsonl (no outcome read)
  python3 scripts/questions.py run <batch id>           # answers that batch, rewrites results in place, recomputes q

A question is a JSON object:
  id, batch, question, hypothesis ('+', '-' or 'any'), unit ('item' or 'name'),
  stratum ('A', 'B', 'C'), cut (a filter, below), metric, outcome_horizon
  ('strategy', 'open', 'close'), why;
  for contrasts also cut_b (the comparison set; default: the complement within `base`).

Filters: {"field": [allowed values] | value | {"min": x, "max": y}}; an item field is
looked up on the item first, then on its print (`ev`). Boolean flags hold the two-run
mean, so `true` matches only items both runs flagged and `false` only items neither did.

Metrics:
  DV, DVstar, hit           item votes in the cut (DVstar uses the residual outcome)
  contrast_DVstar           DVstar(cut) - DVstar(cut_b)
  contrast_hit              hit(cut) - hit(cut_b)
  presence_res              name level: mean residual move (res_n) of prints holding a cut item minus the rest of `base_events`
  MV                        name level: P(big | a cut item present) - P(big | absent), within `base` prints
  oversize                  item level: mean(|live_size| / priced) - mean(|move| / priced) over FILED items in
                            the cut (positive = the hunter sized bigger than what came); a print's items share one move
  MgV_obs                   name level: median4 hit rate where the cut's net vote agrees with median4,
                            minus where it is absent or disagrees
A question is never deleted or rewritten after running; a better version is a new id.
"""
import json, math, os, statistics as st, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402

LEDGER = f'{SV}/ledger/questions.jsonl'


def read_ledger():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in open(LEDGER) if l.strip()]


def write_ledger(rows):
    tmp = LEDGER + '.tmp'
    with open(tmp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    os.replace(tmp, LEDGER)


def get(x, f):
    if f in x:
        return x[f]
    return x.get('ev', {}).get(f)


def match(x, flt):
    for f, want in (flt or {}).items():
        if f == 'subtype':
            ws = x.get('subtype_w') or {}
            if not any(s in ws for s in (want if isinstance(want, list) else [want])):
                return False
            continue
        if f == 'not_subtype':
            ws = x.get('subtype_w') or {}
            if any(s in ws for s in (want if isinstance(want, list) else [want])):
                return False
            continue
        v = get(x, f)
        if isinstance(want, dict):
            if v is None or ('min' in want and v < want['min']) or ('max' in want and v >= want['max']):
                return False
        elif isinstance(want, list):
            if v not in want:
                return False
        elif isinstance(want, bool):
            if v is None:
                return False
            if isinstance(v, bool):
                if v != want:
                    return False
            elif (v == 1.0) != want or v not in (0.0, 1.0):
                return False
        elif v != want:
            return False
    return True


def subset(items, flt, subtype_filter=None):
    """Items in the filter, weighted by the share of runs that gave the filtered subtype."""
    out = []
    for x in items:
        if not match(x, flt):
            continue
        w = 1.0
        if subtype_filter:
            sel = subtype_filter if isinstance(subtype_filter, list) else [subtype_filter]
            w = sum(x['subtype_w'].get(s, 0.0) for s in sel)
        if w > 0:
            y = dict(x)
            y['w'] = w
            out.append(y)
    return out


class Ctx:
    def __init__(self, n_perm=2000):
        self.events, self.items = core.load()
        self.eng = {}
        self.n_perm = n_perm

    def engine(self, stratum):
        if stratum not in self.eng:
            self.eng[stratum] = core.Engine([e for e in self.events if e['stratum'] == stratum], self.n_perm)
        return self.eng[stratum]


def run_one(q, C):
    s = q.get('stratum', 'A')
    eng = C.engine(s)
    h = q.get('outcome_horizon', 'strategy')
    base_items = [x for x in C.items if x['stratum'] == s and match(x, q.get('base') or {})]
    cut = q.get('cut') or {}
    vf = q.get('vote_field')
    if vf:
        base_items = [dict(x, vote=x.get(vf) or 0) for x in base_items]
    sub_a = subset(base_items, cut, cut.get('subtype'))
    m = q['metric']
    res = {}
    if m in ('DV', 'DVstar', 'hit', 'contrast_DVstar', 'contrast_hit'):
        y = eng.vec('res' if 'DVstar' in m else 'y', h)
        upa, dna, _ = core.item_agg(sub_a, eng)
        if m.startswith('contrast'):
            cb = q.get('cut_b')
            sub_b = subset(base_items, cb, cb.get('subtype')) if cb else [dict(x, w=1 - sum(x['subtype_w'].get(s2, 0) for s2 in (cut.get('subtype') if isinstance(cut.get('subtype'), list) else [cut.get('subtype')])) if cut.get('subtype') else (0.0 if match(x, cut) else 1.0)) for x in base_items]
            sub_b = [x for x in sub_b if x.get('w', 1) > 0]
            upb, dnb, _ = core.item_agg(sub_b, eng)
            f = core.dv_stat if 'DVstar' in m else core.hit_stat

            def fn(p):
                a, b = f(upa, dna, y, p), f(upb, dnb, y, p)
                return None if a is None or b is None else a - b
            res['n_b'] = round(sum(upb.values()) + sum(dnb.values()), 2)
            res['prints_b'] = len(set(upb) | set(dnb))
        else:
            f = core.hit_stat if m == 'hit' else core.dv_stat

            def fn(p):
                v = f(upa, dna, y, p)
                return None if v is None else (v - 0.5 if m == 'hit' else v)
            res['se_cluster'] = core.cluster_se(upa, dna, y) if m != 'hit' else None
            res['hit_rate'] = core.hit_stat(upa, dna, y)
            res['DV_raw'] = core.dv_stat(upa, dna, y)
        res['n'] = round(sum(upa.values()) + sum(dna.values()), 2)
        res['prints'] = len(set(upa) | set(dna))
        mper = (res['n'] / res['prints']) if res['prints'] else 1
        res['power_n_prints'] = core.power_n(mper, two_arm=m.startswith('contrast'))
        r = core.perm_test(fn, eng)
    elif m in ('MV', 'presence_res'):
        y = eng.vec('big' if m == 'MV' else 'res', h)
        idxs = [eng.idx[e['id']] for e in eng.events if match({'ev': e}, q.get('base_events') or {})]
        present = {eng.idx[x['ev']['id']] for x in sub_a} & set(idxs)
        res['n'] = len(present)
        res['prints'] = len(present)
        res['n_b'] = len(idxs) - len(present)
        res['p_big_present'] = st.mean([y[j] for j in present]) if present else None
        res['p_big_absent'] = st.mean([y[j] for j in idxs if j not in present]) if res['n_b'] else None
        res['power_n_prints'] = core.power_n(1, two_arm=True)
        r = core.perm_test(lambda p: core.name_stat(present, y, p, idxs), eng)
    elif m == 'oversize':
        rows = [x for x in sub_a if x['kind'] == 'filed_by_first_hunter' and x.get('live_size') is not None]
        byp = defaultdict(list)
        for x in rows:
            byp[eng.idx[x['ev']['id']]].append(abs(x['live_size']) / x['ev']['priced_move'])
        absmv = [abs(e['y_raw']) for e in eng.events]
        keys = list(byp)

        def fn(p):
            if not keys:
                return None
            sz = [v for k in keys for v in byp[k]]
            mv = [absmv[p[k] if p else k] for k in keys for _ in byp[k]]
            return st.mean(sz) - st.mean(mv)
        res['n'] = len(rows)
        res['prints'] = len(keys)
        res['mean_size_n'] = st.mean([v for k in keys for v in byp[k]]) if keys else None
        res['power_n_prints'] = core.power_n(1)
        r = core.perm_test(fn, eng)
        # the permutation leaves sizes in place and shuffles |move|: it asks whether these prints' sizes
        # relate to their own moves differently from other prints' moves on the same day
    elif m == 'MgV_obs':
        pr = {}
        for x in sub_a:
            pr.setdefault(eng.idx[x['ev']['id']], 0.0)
            pr[eng.idx[x['ev']['id']]] += x['w'] * x['vote']
        jud = {}
        for e in eng.events:
            v = (e.get('rejudge') or {})
            four = [v[k]['impact_sum'] for k in ('opus5', 'opus', 'sonnet', 'fable') if k in v and v[k].get('impact_sum') is not None]
            if len(four) == 4 and st.median(four) != 0:
                jud[eng.idx[e['id']]] = core.sgn(st.median(four))
        y = eng.vec('y', h)
        agree = {j for j in jud if core.sgn(pr.get(j, 0)) == jud[j] and pr.get(j, 0) != 0}

        def fn(p):
            a = [(jud[j] * y[p[j] if p else j]) > 0 for j in jud if j in agree and y[p[j] if p else j] is not None]
            b = [(jud[j] * y[p[j] if p else j]) > 0 for j in jud if j not in agree and y[p[j] if p else j] is not None]
            return (st.mean(a) - st.mean(b)) if a and b else None
        res['n'] = len(agree)
        res['prints'] = len(agree)
        res['n_b'] = len(jud) - len(agree)
        res['power_n_prints'] = core.power_n(1, two_arm=True)
        r = core.perm_test(fn, eng)
    else:
        raise ValueError(m)
    res.update({k: r.get(k) for k in ('stat', 'z', 'p', 'null_mean', 'null_sd')})
    res['underpowered'] = (res.get('prints') or 0) < res.get('power_n_prints', 1)
    return res, r.get('null')


def run_batch(bid, n_perm=2000):
    rows = read_ledger()
    todo = [q for q in rows if q['batch'] == bid]
    C = Ctx(n_perm)
    nulls = {}
    for q in todo:
        res, null = run_one(q, C)
        q['result'] = {k: (round(v, 5) if isinstance(v, float) else v) for k, v in res.items()}
        q['n'] = res.get('n')
        q['p'] = res.get('p')
        nulls[q['id']] = (null, res.get('null_mean'), res.get('null_sd'))
    # family-wise within the batch: max |z| over the batch, shuffle by shuffle (same seed => aligned)
    zs = {}
    for qid, (null, mu, sd) in nulls.items():
        if null and sd:
            zs[qid] = [abs((v - mu) / sd) for v in null]
    L = min((len(v) for v in zs.values()), default=0)
    mx = [max(v[k] for v in zs.values()) for k in range(L)] if zs else []
    for q in todo:
        z = q['result'].get('z')
        if z is None or not mx:
            q['p_batch_fwer'] = None
        else:
            q['p_batch_fwer'] = round((1 + sum(m >= abs(z) for m in mx)) / (1 + len(mx)), 5)
    write_ledger(rows)
    requery()
    return todo


def verdict(q):
    p, z, hyp = q.get('p'), (q.get('result') or {}).get('z'), q.get('hypothesis', 'any')
    if p is None:
        return 'not computable'
    up = (q.get('result') or {}).get('underpowered')
    sign_ok = hyp == 'any' or (hyp == '+' and z > 0) or (hyp == '-' and z < 0)
    if q.get('q_ledger') is not None and q['q_ledger'] < 0.10 and sign_ok:
        return 'supported (ledger q < 0.10)'
    if p < 0.05 and sign_ok:
        return 'lead (p < 0.05, not ledger-corrected)'
    if p < 0.05 and not sign_ok:
        return 'opposite sign (p < 0.05)'
    return 'no evidence' + (' (underpowered)' if up else '')


def requery():
    rows = read_ledger()
    ps = [q.get('p') if 'result' in q else None for q in rows]
    qs = core.bh(ps)
    for q, v in zip(rows, qs):
        if 'result' in q:
            q['q_ledger'] = round(v, 5) if v is not None else None
            q['verdict'] = verdict(q)
    write_ledger(rows)


def register(path):
    rows = read_ledger()
    ids = {q['id'] for q in rows}
    new = json.load(open(path))
    for q in new['questions']:
        assert q['id'] not in ids, q['id']
        q['batch'] = new['batch']
        q.setdefault('stratum', 'A')
        q.setdefault('outcome_horizon', 'strategy')
        rows.append(q)
    write_ledger(rows)
    print('registered', len(new['questions']), 'total', len(rows))


if __name__ == '__main__':
    if sys.argv[1] == 'register':
        register(sys.argv[2])
    elif sys.argv[1] == 'run':
        out = run_batch(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2000)
        for q in out:
            r = q['result']
            print(f"{q['id']:<10} n={r.get('n')!s:>6} pr={r.get('prints')!s:>4} stat={r.get('stat') if r.get('stat') is None else round(r['stat'],3)!s:>7} "
                  f"z={r.get('z') if r.get('z') is None else round(r['z'],2)!s:>6} p={q.get('p')!s:>8} fw={q.get('p_batch_fwer')!s:>8} {q.get('verdict')}")
