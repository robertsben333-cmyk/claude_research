#!/usr/bin/env python3
"""Which kinds of evidence carry the sign? Every cut, one test.

  python3 analyze.py [--unseal] [--perms 1000]

Discovery set: every role except judge-lab `test` (sealed). `--unseal` adds them and is
logged by the caller in ../judge-lab/TEST-LOG.md; confirm.py does that for the short list.

THE TEST. A cell is a set of (event, sign) pairs: items of one kind voting for a
direction, or names called by one judge inside one group. Its statistic is the mean of
sign x move/priced (the realised move over the move the baseline priced), gross. Its p is
a permutation p: the realised moves are shuffled across events WITHIN each day, a
thousand times, keeping every event's items together, so clustering of items within a
name and of names within a day is respected. Each cell's z is the observed mean over the
permutation sd. A family-wise p reads the observed |z| against the permutation
distribution of the largest |z| over every cell in its family; Benjamini-Hochberg q is
reported beside it.
"""
import argparse, json, math, os, random, statistics as st, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'judge-lab'))
import judge_lab as J  # noqa: E402

SEED = 20261005
DOMCLS = json.load(open(f'{HERE}/data/domain_classes_llm.json'))
NUMS = ('reliability', 'specificity', 'novelty', 'obscurity', 'relevance', 'strength')


def sgn(x):
    return (x > 0) - (x < 0) if x is not None else 0


# ---------------------------------------------------------------- load
def load_labels():
    """labels[pack_id] = {'pack': {...averaged}, 'items': {i: {...averaged}}, 'agree': {...}}"""
    out = {}
    runs = sorted(d for d in os.listdir(f'{HERE}/labels') if d.startswith('run'))
    per = defaultdict(list)
    for r in runs:
        for f in os.listdir(f'{HERE}/labels/{r}'):
            if f.endswith('.json'):
                per[f[:-5]].append(json.load(open(f'{HERE}/labels/{r}/{f}')))
    for pid, L in per.items():
        pk = {}
        for k in ('pack_reliability', 'pack_sufficiency', 'pack_conviction'):
            v = [x.get(k) for x in L if isinstance(x.get(k), (int, float))]
            pk[k] = st.mean(v) if v else None
        pk['pack_direction'] = st.mean([x.get('pack_direction') or 0 for x in L])
        pk['coverage'] = Counter(x.get('coverage') for x in L).most_common(1)[0][0]
        pk['n_runs'] = len(L)
        items = defaultdict(list)
        for x in L:
            for it in x.get('items') or []:
                items[it.get('i')].append(it)
        avg = {}
        for i, V in items.items():
            a = {k: st.mean([v.get(k) for v in V if isinstance(v.get(k), (int, float))]) if any(isinstance(v.get(k), (int, float)) for v in V) else None for k in NUMS}
            a['direction'] = st.mean([v.get('direction') or 0 for v in V])
            ct = [v.get('claim_type') for v in V]
            a['claim_type'] = ct[0]
            a['claim_type_agree'] = len(set(ct)) == 1
            a['focal'] = Counter(bool(v.get('focal')) for v in V).most_common(1)[0][0]
            a['runs'] = V
            avg[i] = a
        out[pid] = {'pack': pk, 'items': avg}
    return out


def load(unseal=False):
    E = json.load(open(f'{HERE}/data/events.json'))
    I = json.load(open(f'{HERE}/data/items.json'))
    L = load_labels()
    keep = [e for e in E if unseal or e['role'] != 'test']
    ids = {e['id'] for e in keep}
    # the day a print is grouped on: the non-duplicate hunt's day
    twin_day = {e['event_key']: e['day'] for e in E if not e['duplicate_hunt']}
    for e in keep:
        e['perm_day'] = twin_day.get(e['event_key'], e['day'])
        e['move_n'] = e['move'] / e['priced_move']
        lab = L.get(e['pack_id'], {})
        e['lab'] = lab.get('pack', {})
        e['lab_items'] = lab.get('items', {})
        rj = e.get('rejudge') or {}
        e['call'] = {'live': e['live_impact'] or 0.0}
        for m in ('opus5', 'opus', 'sonnet', 'fable'):
            if m in rj and rj[m].get('impact_sum') is not None:
                e['call'][m] = float(rj[m]['impact_sum'])
        four = [e['call'][m] for m in ('opus5', 'opus', 'sonnet', 'fable') if m in e['call']]
        if len(four) == 4:
            e['call']['median4'] = st.median(four)
        if e.get('rated'):
            e['call']['rated'] = st.mean([r['impact_sum'] or 0 for r in e['rated']])
            e['rated_suf'] = st.mean([r['sufficiency'] for r in e['rated'] if r['sufficiency'] is not None] or [None]) if any(r['sufficiency'] is not None for r in e['rated']) else None
            e['rated_rel'] = st.mean([r['reliability'] for r in e['rated'] if r['reliability'] is not None]) if any(r['reliability'] is not None for r in e['rated']) else None
        if e['lab']:
            e['call']['labeler'] = (e['lab'].get('pack_direction') or 0) * (e['lab'].get('pack_conviction') or 0)
    items = []
    for it in I:
        if it['event'] not in ids:
            continue
        ev = next(e for e in keep if e['id'] == it['event'])
        lab = ev['lab_items'].get(it['i'])
        if lab is None:
            continue
        it.update({k: lab[k] for k in NUMS + ('direction', 'claim_type', 'claim_type_agree', 'focal')})
        it['label_runs'] = lab['runs']
        it['domain_class'] = DOMCLS.get(it['domain']) if it['domain'] else 'no_source'
        it['ev'] = ev
        items.append(it)
    return keep, items


# ---------------------------------------------------------------- permutation engine
class Perm:
    """Shuffle move_n across events within each perm_day. Cells are lists of (event_key, weight)."""

    def __init__(self, events, n, seed=SEED):
        by_key = {}
        for e in events:
            by_key.setdefault(e['event_key'], e)
        self.keys = sorted(by_key)
        self.idx = {k: j for j, k in enumerate(self.keys)}
        self.mv = [by_key[k]['move_n'] for k in self.keys]
        days = defaultdict(list)
        for k in self.keys:
            days[by_key[k]['perm_day']].append(self.idx[k])
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

    def stat(self, cell, p=None):
        if not cell:
            return None
        if p is None:
            return sum(w * self.mv[self.idx[k]] for k, w in cell) / len(cell)
        return sum(w * self.mv[p[self.idx[k]]] for k, w in cell) / len(cell)

    def test(self, cell):
        obs = self.stat(cell)
        null = [self.stat(cell, p) for p in self.perms]
        sd = st.pstdev(null) or 1e-9
        mu = st.mean(null)
        z = (obs - mu) / sd
        p = (1 + sum(abs(x - mu) >= abs(obs - mu) for x in null)) / (1 + len(null))
        return obs, z, p, [(x - mu) / sd for x in null]


def family(perm, cells, min_n=8):
    """cells: {name: {'cell': [(event_key, w)], 'extra': {...}}}. Adds z, p, fwer, q."""
    out, nulls = {}, []
    for name, c in cells.items():
        cell = c['cell']
        hits = sum(1 for k, w in cell if w * perm.mv[perm.idx[k]] > 0)
        row = {'n': len(cell), 'events': len({k for k, _ in cell}), 'hits': hits,
               'hit_rate': hits / len(cell) if cell else None, **c.get('extra', {})}
        if len({k for k, _ in cell}) >= min_n:
            obs, z, p, null = perm.test(cell)
            row.update({'mean_signed_move_n': obs, 'z': z, 'p': p})
            nulls.append(null)
        out[name] = row
    # family-wise: the max |z| per permutation over the family
    if nulls:
        mx = [max(abs(n[j]) for n in nulls) for j in range(len(nulls[0]))]
        for row in out.values():
            if 'z' in row:
                row['p_fwer'] = (1 + sum(m >= abs(row['z']) for m in mx)) / (1 + len(mx))
        tested = sorted([r for r in out.values() if 'p' in r], key=lambda r: r['p'])
        m = len(tested)
        prev = 1.0
        for rank in range(m, 0, -1):
            r = tested[rank - 1]
            prev = min(prev, r['p'] * m / rank)
            r['q_bh'] = prev
    return out


# ---------------------------------------------------------------- helpers
def tercile_cut(vals):
    v = sorted(x for x in vals if x is not None)
    return v[len(v) // 3], v[2 * len(v) // 3]


def bucket3(x, cuts, names=('low', 'mid', 'high')):
    if x is None:
        return None
    return names[0] if x < cuts[0] else (names[1] if x < cuts[1] else names[2])


def item_cells(items, groupfn, signfn=lambda it: sgn(it['direction']), weightfn=None):
    cells = defaultdict(list)
    for it in items:
        s = signfn(it)
        if not s:
            continue
        g = groupfn(it)
        if g is None:
            continue
        for gg in (g if isinstance(g, (list, tuple)) else [g]):
            cells[gg].append((it['event_key'], s * (weightfn(it) if weightfn else 1)))
    return {k: {'cell': v} for k, v in cells.items()}


def name_cells(events, groupfn, callname):
    cells = defaultdict(list)
    for e in events:
        if e['duplicate_hunt'] or callname not in e['call']:
            continue
        s = sgn(e['call'][callname])
        g = groupfn(e)
        if not s or g is None:
            continue
        for gg in (g if isinstance(g, (list, tuple)) else [g]):
            cells[gg].append((e['event_key'], s))
    return {k: {'cell': v} for k, v in cells.items()}


def top_ids(events, callname, share=0.2):
    rows = [{'id': e['id'], 'region': 'us', 'day': e['day'], 'move': e['move'], 'dv': e['dollar_vol'] or 0}
            for e in events if not e['duplicate_hunt'] and callname in e['call']]
    pred = {e['id']: e['call'][callname] for e in events if not e['duplicate_hunt'] and callname in e['call']}
    return set(J.top_metrics(rows, pred, share)['ids'])


def spearman(a, b):
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(p) < 5:
        return None
    ra, rb = J.rank([x for x, _ in p]), J.rank([y for _, y in p])
    ma, mb = st.mean(ra), st.mean(rb)
    d = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / d if d else None


def r2(x):
    return None if x is None else round(x, 3)


def fmt(tab, keys=('n', 'events', 'hits', 'hit_rate', 'mean_signed_move_n', 'z', 'p', 'p_fwer', 'q_bh')):
    return {k: {kk: (r2(v[kk]) if isinstance(v.get(kk), float) else v.get(kk)) for kk in keys if kk in v} for k, v in
            sorted(tab.items(), key=lambda kv: -(kv[1].get('z') or -99))}


# ---------------------------------------------------------------- analyses
def stability(items, events):
    two = [it for it in items if len(it['label_runs']) == 2]
    out = {'items_with_two_runs': len(two)}
    if not two:
        return out
    for k in NUMS:
        out[f'spearman_{k}'] = r2(spearman([it['label_runs'][0].get(k) for it in two], [it['label_runs'][1].get(k) for it in two]))
    out['claim_type_agree'] = r2(st.mean(it['claim_type_agree'] for it in two))
    out['direction_agree'] = r2(st.mean(int(sgn(it['label_runs'][0].get('direction')) == sgn(it['label_runs'][1].get('direction'))) for it in two))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unseal', action='store_true')
    ap.add_argument('--perms', type=int, default=1000)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    events, items = load(a.unseal)
    names = [e for e in events if not e['duplicate_hunt']]
    perm = Perm(events, a.perms)
    R = {'sample': {'events': len(names), 'hunts': len(events), 'items_labeled': len(items),
                    'unsealed': a.unseal, 'roles': Counter(e['role'] for e in names)}}
    R['label_stability'] = stability(items, events)

    # ---- A. the observation that started this: pack-level reliability and sufficiency
    for src in ('lab', 'rated'):
        suf = (lambda e: e['lab'].get('pack_sufficiency')) if src == 'lab' else (lambda e: e.get('rated_suf'))
        rel = (lambda e: e['lab'].get('pack_reliability')) if src == 'lab' else (lambda e: e.get('rated_rel'))
        vs = [suf(e) for e in names if suf(e) is not None]
        vr = [rel(e) for e in names if rel(e) is not None]
        if not vs:
            continue
        ms, mr = st.median(vs), st.median(vr)
        q = lambda e: None if suf(e) is None or rel(e) is None else f"suf_{'hi' if suf(e) >= ms else 'lo'}/rel_{'hi' if rel(e) >= mr else 'lo'}"
        R[f'A_{src}_quadrants'] = {'medians': {'suf': ms, 'rel': mr}}
        for call in ('live', 'rated', 'median4', 'opus5', 'opus', 'sonnet', 'fable', 'labeler'):
            R[f'A_{src}_quadrants'][call] = fmt(family(perm, name_cells(events, q, call)))
            tops = top_ids(events, call)
            R[f'A_{src}_quadrants'][call + '_top20'] = fmt(family(perm, name_cells([e for e in events if e['id'] in tops], q, call), min_n=4))

    # ---- B. is it the name, not the evidence? coverage, size, volatility
    vcut = st.median([e['vol20'] for e in names if e['vol20']])
    dcut = st.median([e['dollar_vol'] for e in names if e['dollar_vol']])
    R['B_name_type'] = {}
    for call in ('live', 'median4', 'rated', 'labeler'):
        R['B_name_type'][call] = {
            'coverage': fmt(family(perm, name_cells(events, lambda e: e['lab'].get('coverage'), call))),
            'vol': fmt(family(perm, name_cells(events, lambda e: None if not e['vol20'] else ('vol_hi' if e['vol20'] >= vcut else 'vol_lo'), call))),
            'turnover': fmt(family(perm, name_cells(events, lambda e: None if not e['dollar_vol'] else ('dv_hi' if e['dollar_vol'] >= dcut else 'dv_lo'), call))),
            'session': fmt(family(perm, name_cells(events, lambda e: e['session'], call))),
            'hunter_model': fmt(family(perm, name_cells(events, lambda e: e['hunter_model'], call))),
        }
    R['B_name_type']['_medians'] = {'vol20': vcut, 'dollar_vol': dcut}

    # ---- C. item level: which kind of evidence points the right way
    directional = [it for it in items if sgn(it['direction'])]
    R['C_items'] = {'directional_items': len(directional), 'events_with_directional': len({it['event_key'] for it in directional})}
    cuts = {k: tercile_cut([it[k] for it in directional]) for k in NUMS}
    R['C_items']['tercile_cuts'] = cuts
    fam = {}
    fam['claim_type'] = item_cells(items, lambda it: it['claim_type'])
    fam['domain_class'] = item_cells(items, lambda it: it['domain_class'])
    fam['kind'] = item_cells(items, lambda it: it['kind'])
    fam['focal'] = item_cells(items, lambda it: 'focal' if it['focal'] else 'not_focal')
    for k in NUMS:
        fam[k] = item_cells(items, (lambda kk: lambda it: bucket3(it[kk], cuts[kk]))(k))
    fam['reliability_x_novelty'] = item_cells(items, lambda it: None if it['reliability'] is None or it['novelty'] is None else
                                              f"rel_{bucket3(it['reliability'], cuts['reliability'])}/nov_{bucket3(it['novelty'], cuts['novelty'])}")
    fam['reliability_x_obscurity'] = item_cells(items, lambda it: None if it['reliability'] is None or it['obscurity'] is None else
                                                f"rel_{bucket3(it['reliability'], cuts['reliability'])}/obs_{bucket3(it['obscurity'], cuts['obscurity'])}")
    fam['reliability_x_claim'] = item_cells(items, lambda it: None if it['reliability'] is None else
                                            f"{it['claim_type']}/rel_{'lo' if it['reliability'] < cuts['reliability'][0] else 'mid_hi'}")
    age_cut = lambda a_: None if a_ is None else ('age<=7d' if a_ <= 7 else ('age8-30d' if a_ <= 30 else ('age31-90d' if a_ <= 90 else 'age>90d')))
    fam['age'] = item_cells(items, lambda it: age_cut(it['age_days']))
    # the same families scored on the LIVE hunter's own sign (findings only)
    live_sign = lambda it: sgn(it['live_size']) if it['kind'] == 'filed_by_first_hunter' else 0
    fam_live = {f'live:{k}': item_cells(items, g, signfn=live_sign) for k, g in
                [('claim_type', lambda it: it['claim_type']), ('domain_class', lambda it: it['domain_class']),
                 ('reliability', lambda it: bucket3(it['reliability'], cuts['reliability'])),
                 ('novelty', lambda it: bucket3(it['novelty'], cuts['novelty'])),
                 ('live_category', lambda it: it['live_category'])]}
    all_cells = {}
    for fname, cells in list(fam.items()) + list(fam_live.items()):
        for k, v in cells.items():
            all_cells[f'{fname}={k}'] = v
    scored = family(perm, all_cells)
    R['C_items']['cells'] = fmt(scored)

    # ---- F. further cuts, scored as one family together with C (global_fwer)
    HEDGE = __import__('re').compile(r'\b(may|might|could|likely|possibly|appears?|suggests?|estimated?|implies|roughly|about|approximately|if)\b', __import__('re').I)
    NUMBER = __import__('re').compile(r'[-+]?\$?\d[\d,.]*\s?(%|bn|m|million|billion|bps|x)?', __import__('re').I)
    for it in items:
        t = it.get('text') or ''
        w = max(len(t.split()), 1)
        it['hedge_rate'] = len(HEDGE.findall(t)) / w
        it['number_rate'] = len(NUMBER.findall(t)) / w
        net = it['ev']['live_impact'] or 0
        it['vs_name_net'] = None if not net or not sgn(it['direction']) else ('with_name_net' if sgn(it['direction']) == sgn(net) else 'against_name_net')
        pl = it['ev'].get('priced_lean_pct')
        it['vs_lean'] = None if not pl or not sgn(it['direction']) else ('with_lean' if sgn(it['direction']) == sgn(pl) else 'against_lean')
    hcut, ncut = tercile_cut([it['hedge_rate'] for it in directional]), tercile_cut([it['number_rate'] for it in directional])
    famF = {}
    famF['hedging'] = item_cells(items, lambda it: bucket3(it['hedge_rate'], hcut))
    famF['numbers'] = item_cells(items, lambda it: bucket3(it['number_rate'], ncut))
    famF['n_urls'] = item_cells(items, lambda it: 'urls_0' if not it['n_urls'] else ('urls_1' if it['n_urls'] == 1 else 'urls_2plus'))
    famF['vs_name_net'] = item_cells(items, lambda it: it['vs_name_net'])
    famF['vs_lean'] = item_cells(items, lambda it: it['vs_lean'])
    lowrel = lambda it: it['reliability'] is not None and it['reliability'] < cuts['reliability'][0]
    famF['hypothesis'] = item_cells(items, lambda it: [g for g, ok in [
        ('lowrel_and_novel', lowrel(it) and it['novelty'] is not None and it['novelty'] >= cuts['novelty'][1]),
        ('lowrel_and_obscure', lowrel(it) and it['obscurity'] is not None and it['obscurity'] >= cuts['obscurity'][1]),
        ('lowrel_not_novel', lowrel(it) and it['novelty'] is not None and it['novelty'] < cuts['novelty'][1]),
        ('highrel_and_novel', (not lowrel(it)) and it['novelty'] is not None and it['novelty'] >= cuts['novelty'][1]),
        ('lowrel_focal', lowrel(it) and it['focal']), ('lowrel_not_focal', lowrel(it) and not it['focal'])] if ok] or None)
    # findings where the labeler and the live hunter read the direction differently: who is right?
    fnd = [it for it in items if it['kind'] == 'filed_by_first_hunter' and sgn(it['live_size']) and sgn(it['direction'])]
    famF['sign_reading'] = {
        'agree (shared sign)': {'cell': [(it['event_key'], sgn(it['live_size'])) for it in fnd if sgn(it['live_size']) == sgn(it['direction'])]},
        'disagree: live hunter sign': {'cell': [(it['event_key'], sgn(it['live_size'])) for it in fnd if sgn(it['live_size']) != sgn(it['direction'])]},
        'disagree: labeler sign': {'cell': [(it['event_key'], sgn(it['direction'])) for it in fnd if sgn(it['live_size']) != sgn(it['direction'])]},
        'labeler-only direction (hunter size 0 or not a finding)': {'cell': [(it['event_key'], sgn(it['direction'])) for it in items if sgn(it['direction']) and not (it['kind'] == 'filed_by_first_hunter' and sgn(it['live_size']))]},
    }
    for fname, cells in famF.items():
        for k, v in cells.items():
            all_cells[f'{fname}={k}'] = v
    glob_scored = family(perm, all_cells)
    R['F_more_cuts'] = fmt({k: v for k, v in glob_scored.items() if k.split('=')[0] in famF})
    R['F_more_cuts']['_cuts'] = {'hedge': hcut, 'numbers': ncut}
    R['global_family'] = {'n_cells_tested': sum(1 for v in glob_scored.values() if 'z' in v),
                          'top': fmt(dict(sorted(((k, v) for k, v in glob_scored.items() if 'z' in v), key=lambda kv: -abs(kv[1]['z']))[:15]))}

    # ---- G. a book on one kind of evidence: top 20% by the class vote, net of cost
    def book(pred):
        rows = [{'id': e['id'], 'region': 'us', 'day': e['day'], 'move': e['move'], 'dv': e['dollar_vol'] or 0} for e in names]
        m = J.top_metrics(rows, pred, 0.2)
        return {k: r2(m[k]) if isinstance(m[k], float) else m[k] for k in ('n', 'hits', 'net', 't', 'short_all_net')}

    # ---- D. per name: the vote of one kind of evidence, does it rank the day?
    def vote(e, pred):
        its = [it for it in items if it['event'] == e['id'] and pred(it)]
        return sum((it['direction'] or 0) * (it['strength'] or 0) for it in its) if its else None
    groups = {f'claim={c}': (lambda c: lambda it: it['claim_type'] == c)(c) for c in sorted({it['claim_type'] for it in items if it['claim_type']})}
    groups.update({f'domain={c}': (lambda c: lambda it: it['domain_class'] == c)(c) for c in sorted({it['domain_class'] for it in items if it['domain_class']})})
    groups.update({'rel_low': lambda it: it['reliability'] is not None and it['reliability'] < cuts['reliability'][0],
                   'rel_mid_hi': lambda it: it['reliability'] is not None and it['reliability'] >= cuts['reliability'][0],
                   'novel_high': lambda it: it['novelty'] is not None and it['novelty'] >= cuts['novelty'][1],
                   'obscure_high': lambda it: it['obscurity'] is not None and it['obscurity'] >= cuts['obscurity'][1],
                   'all_items': lambda it: True})
    D = {}
    for g, pred in groups.items():
        vals = {e['id']: vote(e, pred) for e in names}
        nz = [e for e in names if vals[e['id']]]
        cell = [(e['event_key'], sgn(vals[e['id']])) for e in nz]
        D[g] = {'cell': cell, 'extra': {'rho_vote_vs_move': r2(spearman([vals[e['id']] for e in nz], [e['move'] for e in nz]))}}
    R['D_votes'] = fmt(family(perm, D), keys=('n', 'hits', 'hit_rate', 'mean_signed_move_n', 'z', 'p', 'p_fwer', 'q_bh', 'rho_vote_vs_move'))
    R['G_books'] = {f'judge:{c}': book({e['id']: e['call'][c] for e in names if c in e['call']})
                    for c in ('live', 'median4', 'opus5', 'opus', 'sonnet', 'fable', 'rated', 'labeler')}
    for g, pred in groups.items():
        R['G_books'][f'vote:{g}'] = book({e['id']: (vote(e, pred) or 0.0) for e in names})

    # ---- E. robustness for the item cells that lead: horizons and eras
    R['E_robust'] = {}
    lead = [k for k, v in sorted(scored.items(), key=lambda kv: -abs(kv[1].get('z') or 0)) if 'z' in v][:8]
    for horizon in ('move_open', 'move_close'):
        alt = Perm([{**e, 'move_n': (e[horizon] if e[horizon] is not None else e['move']) / e['priced_move']} for e in events], a.perms)
        R['E_robust'][horizon] = fmt({k: v for k, v in family(alt, {k: all_cells[k] for k in lead}).items()})
    for era in ('Opus 5', 'Opus 5.5'):
        keys = {e['event_key'] for e in events if e['hunter_model'] == era}
        sub = {k: {'cell': [(kk, w) for kk, w in all_cells[k]['cell'] if kk in keys]} for k in lead}
        R['E_robust'][era] = fmt(family(perm, sub, min_n=5))
    # leave one day out: does the lead cell keep its sign on every day?
    R['E_robust']['by_day'] = {}
    ev_day = {e['event_key']: e['perm_day'] for e in events}
    for k in lead[:4]:
        per = defaultdict(list)
        for kk, w in all_cells[k]['cell']:
            per[ev_day[kk]].append(w * perm.mv[perm.idx[kk]])
        R['E_robust']['by_day'][k] = {d: {'n': len(v), 'mean': r2(st.mean(v))} for d, v in sorted(per.items())}

    out = a.out or f"{HERE}/results/analysis{'-unsealed' if a.unseal else ''}.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(R, open(out, 'w'), indent=1, default=str)
    print('wrote', out)


if __name__ == '__main__':
    main()
