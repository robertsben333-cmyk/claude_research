#!/usr/bin/env python3
"""Phase 6: the source-value registry.

  python3 scripts/registry.py                 # registry/registry-v1.json and registry/REGISTRY.md
  python3 scripts/registry.py --forward <dir> # (update_registry.py) adds forward agreement, writes registry-forward.json

One row per code (codebook v1 subtype after merges, and per group) overall and per cap band,
on stratum A, with: counts, prevalence, DV, DV* (raw, shrunk, 80% interval), hit rate, MV,
MgV (observational; ablation where run), leave-one-day-out sign share, stratum B and C raw DV*,
a pooled A+B DV* where Cochran's Q allows, the ledger q of the question that tested the
cell, the verdict by METHODS.md's frozen rules, and one sentence of guidance.

This file is a diagnostic. No scorer, no book and no hunter reads it.
"""
import json, math, os, statistics as st, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402
import questions as QQ  # noqa: E402

BANDS = ['micro', 'small', 'mid', 'large']
Z80 = 1.2816


def stat_set(items, eng, kind='res', h='strategy'):
    y = eng.vec(kind, h)
    up, dn, al = core.item_agg(items, eng)
    v = core.dv_stat(up, dn, y)
    se = core.cluster_se(up, dn, y)
    n = sum(up.values()) + sum(dn.values())
    return v, se, n, len(set(up) | set(dn)), up, dn


def lodo_share(items, eng, full):
    if full is None or full == 0:
        return None, 0
    byday = defaultdict(list)
    for x in items:
        byday[x['ev']['perm_day']].append(x)
    y = eng.vec('res', 'strategy')
    signs = []
    for d, xs in byday.items():
        up, dn, _ = core.item_agg(xs, eng)
        v = core.dv_stat(up, dn, y)
        if v is not None and v != 0:
            signs.append(core.sgn(v) == core.sgn(full))
    return (sum(signs) / len(signs) if signs else None), len(signs)


def with_w(items, code_of, code):
    out = []
    for x in items:
        w = sum(v for k, v in x['subtype_w'].items() if code_of(k) == code)
        if w > 0:
            out.append(dict(x, w=w))
    return out


def ledger_index():
    idx = {}
    for q in QQ.read_ledger():
        if q.get('metric') != 'DVstar' or q.get('stratum', 'A') != 'A' or q.get('outcome_horizon', 'strategy') != 'strategy' or 'result' not in q:
            continue
        c = q.get('cut') or {}
        if set(c) - {'subtype', 'group', 'cap_band'}:
            continue
        key = (c.get('subtype') or ('GROUP:' + c['group'] if isinstance(c.get('group'), str) else None), c.get('cap_band'))
        if key[0] and not isinstance(key[0], list) and not isinstance(key[1], list):
            idx[key] = q
    return idx


def verdict(sh, lo, hi, q, lodo, repl_ok, fwd_ok=None, raw=None, se=None, n=0):
    if lo is None:
        return 'not computable'
    # amendment 1: a directional verdict also needs the cell's OWN raw 80% interval to exclude 0
    # and at least 10 voting items, so a cell cannot inherit a verdict from its parent alone
    own = raw is not None and se and n >= 10
    if not own or (raw - Z80 * se <= 0 <= raw + Z80 * se):
        return 'no evidence'
    if core.sgn(raw) != core.sgn(sh or 0):
        return 'no evidence'
    held = (repl_ok or fwd_ok)
    if lo > 0:
        full = q is not None and q.get('q_ledger') is not None and q['q_ledger'] < 0.10 and (lodo or 0) >= 0.65 and held
        return 'works' if full else 'probably works'
    if hi < 0:
        full = q is not None and q.get('q_ledger') is not None and q['q_ledger'] < 0.10 and (lodo or 0) >= 0.65 and held
        return 'misleads' if full else 'probably misleads'
    return 'no evidence'


def guidance(v, mv, mv_p, n):
    if v in ('works', 'probably works'):
        return 'Weight it: its votes have pointed the right way beyond drift.' + (' Not yet confirmed forward.' if v == 'probably works' else '')
    if v in ('misleads', 'probably misleads'):
        return 'Do not weight its direction: its votes have pointed the wrong way beyond drift. Do not invert it either until forward days confirm.'
    if mv is not None and mv_p is not None and mv_p < 0.10 and mv > 0:
        return 'No directional value; its presence goes with larger-than-priced moves, so treat it as a size signal only.'
    if n < 20:
        return 'Too few voting items to say; no weight either way.'
    return 'No directional value either way; do not weight its direction.'


def build(forward=None):
    E, I = core.load()
    cb = core.codebook()
    grp = {s['id']: s['group'] for s in cb['subtypes']}
    names = {s['id']: s['name'] for s in cb['subtypes']}
    mm = core.merge_map()

    def code_of(s):
        return mm.get(s, s)

    def group_of(c):
        return c[2:] if c.startswith('G:') else grp.get(c)
    engs = {s: core.Engine([e for e in E if e['stratum'] == s], 2000) for s in ('A', 'B', 'C')}
    IA = [x for x in I if x['stratum'] == 'A']
    codes = sorted({code_of(k) for x in IA for k in x['subtype_w']})
    LI = ledger_index()
    abl = json.load(open(f'{SV}/results/ablation.json')) if os.path.exists(f'{SV}/results/ablation.json') else {'codes': {}}
    prints_A = [e for e in E if e['stratum'] == 'A']
    # ---------- raw estimates
    raw = {}
    ov = stat_set(IA, engs['A'])
    raw[('ALL', None)] = ov

    def items_of(code, band=None, stratum='A'):
        xs = [x for x in I if x['stratum'] == stratum and (band is None or x['ev']['cap_band'] == band)]
        return with_w(xs, code_of, code)
    groups = sorted(set(grp.values()))
    for g in groups:
        raw[('GROUP:' + g, None)] = stat_set([dict(x, w=1.0) for x in IA if group_of(code_of(x['subtype'])) == g], engs['A'])
        for b in BANDS:
            raw[('GROUP:' + g, b)] = stat_set([dict(x, w=1.0) for x in IA if group_of(code_of(x['subtype'])) == g and x['ev']['cap_band'] == b], engs['A'])
    for c in codes:
        raw[(c, None)] = stat_set(items_of(c), engs['A'])
        for b in BANDS:
            raw[(c, b)] = stat_set(items_of(c, b), engs['A'])
    # ---------- shrinkage, top-down, one tau2 per level (METHODS amendment 1)
    ov_est, ov_se = ov[0], ov[1]
    ok = lambda k: raw[k][2] >= 3  # noqa: E731
    t_grp = core.level_tau2([(raw[('GROUP:' + g, None)][0], raw[('GROUP:' + g, None)][1], ov_est) for g in groups if ok(('GROUP:' + g, None))])
    t_sub = core.level_tau2([(raw[(c, None)][0], raw[(c, None)][1], raw[('GROUP:' + group_of(c), None)][0]) for c in codes if ok((c, None))])
    t_band = core.level_tau2([(raw[(c, b)][0], raw[(c, b)][1], raw[(c, None)][0]) for c in codes for b in BANDS if ok((c, b))] +
                             [(raw[('GROUP:' + g, b)][0], raw[('GROUP:' + g, b)][1], raw[('GROUP:' + g, None)][0]) for g in groups for b in BANDS if ok(('GROUP:' + g, b))])
    tau = {'group': t_grp, 'subtype': t_sub, 'band': t_band}
    gsh, _ = core.shrink_level({g: (raw[('GROUP:' + g, None)][0], raw[('GROUP:' + g, None)][1], raw[('GROUP:' + g, None)][2]) for g in groups}, ov_est, ov_se, t_grp)
    sh = {}
    for g in groups:
        sh[('GROUP:' + g, None)] = gsh[g]
        bs, _ = core.shrink_level({b: raw[('GROUP:' + g, b)][0:2] + (raw[('GROUP:' + g, b)][2],) for b in BANDS}, gsh[g][0], gsh[g][1], t_band)
        for b in BANDS:
            sh[('GROUP:' + g, b)] = bs[b]
        kids = [c for c in codes if group_of(c) == g]
        ks, _ = core.shrink_level({c: raw[(c, None)][0:2] + (raw[(c, None)][2],) for c in kids}, gsh[g][0], gsh[g][1], t_sub)
        for c in kids:
            sh[(c, None)] = ks[c]
            cs_, _ = core.shrink_level({b: raw[(c, b)][0:2] + (raw[(c, b)][2],) for b in BANDS}, ks[c][0], ks[c][1], t_band)
            for b in BANDS:
                sh[(c, b)] = cs_[b]
    # ---------- per row extras
    rows = []
    mgv_y = engs['A'].vec('y', 'strategy')
    for key in sorted(sh, key=lambda k: (k[0], BANDS.index(k[1]) if k[1] else -1)):
        code, band = key
        isgrp = code.startswith('GROUP:')
        g = code[6:] if isgrp else group_of(code)
        if isgrp:
            its = [dict(x, w=1.0) for x in IA if group_of(code_of(x['subtype'])) == g and (band is None or x['ev']['cap_band'] == band)]
        else:
            its = items_of(code, band)
        v, se, n, npr, up, dn = raw[key]
        dv_raw = core.dv_stat(up, dn, engs['A'].vec('y', 'strategy'))
        hit = core.hit_stat(up, dn, engs['A'].vec('y', 'strategy'))
        est, psd, B = sh[key]
        lo, hi = (est - Z80 * psd, est + Z80 * psd) if est is not None and psd is not None else (None, None)
        lodo, nd = lodo_share(its, engs['A'], v)
        pool = [e for e in prints_A if band is None or e['cap_band'] == band]
        present = {x['ev']['id'] for x in its}
        prev = len(present & {e['id'] for e in pool}) / len(pool) if pool else None
        bigp = [e['big'] for e in pool if e['id'] in present]
        biga = [e['big'] for e in pool if e['id'] not in present]
        mv = (st.mean(bigp) - st.mean(biga)) if bigp and biga else None
        # replication strata
        rep = {}
        for s in ('B', 'C'):
            xs = [x for x in I if x['stratum'] == s and (band is None or s == 'C' or x['ev']['cap_band'] == band)]
            if isgrp:
                xs = [dict(x, w=1.0) for x in xs if group_of(code_of(x['subtype'])) == g]
            else:
                xs = with_w(xs, code_of, code)
            if s == 'C' and band is not None:
                xs = []  # no cap band outside the US: C replicates the overall row only
            rv, rse, rn, rp, _, _ = stat_set(xs, engs[s]) if xs else (None, None, 0, 0, {}, {})
            rep[s] = {'DVstar_raw': rv, 'se': rse, 'n_vote': rn, 'prints': rp}
        repl_ok = any(r['DVstar_raw'] is not None and r['n_vote'] >= 5 and v is not None and core.sgn(r['DVstar_raw']) == core.sgn(est or 0) for r in rep.values())
        # pooled A+B where Cochran's Q allows
        pooled = None
        rb = rep['B']
        if v is not None and se and rb['DVstar_raw'] is not None and rb['se']:
            Qs = (v - rb['DVstar_raw']) ** 2 / (se ** 2 + rb['se'] ** 2)
            pQ = math.erfc(math.sqrt(Qs / 2))
            if pQ > 0.10:
                w1, w2 = 1 / se ** 2, 1 / rb['se'] ** 2
                pooled = {'DVstar': (w1 * v + w2 * rb['DVstar_raw']) / (w1 + w2), 'se': (w1 + w2) ** -0.5, 'Q_p': pQ}
            else:
                pooled = {'DVstar': None, 'Q_p': pQ, 'note': 'A and B disagree (Q p <= 0.10): not pooled'}
        # marginal value, observational (name level, overall rows only to keep it cheap)
        mgv = None
        if band is None:
            netv = defaultdict(float)
            for x in its:
                netv[x['ev']['id']] += x['w'] * x['vote']
            agree, other = [], []
            for e in prints_A:
                rj = e.get('rejudge') or {}
                four = [rj[k]['impact_sum'] for k in ('opus5', 'opus', 'sonnet', 'fable') if k in rj and rj[k].get('impact_sum') is not None]
                if len(four) < 4 or st.median(four) == 0:
                    continue
                js = core.sgn(st.median(four))
                right = js * e['move'] > 0
                (agree if core.sgn(netv.get(e['id'], 0)) == js else other).append(right)
            if agree and other:
                mgv = {'hit_agree': st.mean(agree), 'n_agree': len(agree), 'hit_other': st.mean(other), 'n_other': len(other),
                       'lift': st.mean(agree) - st.mean(other)}
        ab = None
        akey = code
        if akey.replace(':', '_') in abl['codes'] and band is None:
            ab = abl['codes'][akey.replace(':', '_')]
        q = LI.get((code, band))
        fwd = (forward or {}).get(f'{code}|{band}')
        fwd_ok = None if not fwd else (fwd.get('n_vote', 0) >= 5 and core.sgn(fwd.get('DVstar_raw') or 0) == core.sgn(est or 0))
        vd = verdict(est, lo, hi, q, lodo, repl_ok, fwd_ok, v, se, n)
        rows.append({'code': code, 'group': g, 'name': ('group: ' + g) if isgrp else names.get(code, code), 'band': band or 'all',
                     'n_items': round(sum(x['w'] for x in its), 1), 'n_vote': round(n, 1), 'prints_vote': npr, 'prevalence': prev,
                     'DV': dv_raw, 'hit_rate': hit, 'DVstar_raw': v, 'DVstar_se': se, 'DVstar_shrunk': est, 'shrink_B': B,
                     'ci80': [lo, hi], 'MV_lift': mv, 'MgV_obs': mgv, 'MgV_ablation': ab, 'lodo_sign_share': lodo, 'lodo_days': nd,
                     'replication': rep, 'pooled_AB': pooled, 'ledger_question': q['id'] if q else None,
                     'q_ledger': q.get('q_ledger') if q else None, 'p': q.get('p') if q else None,
                     'forward': fwd, 'forward_agrees': fwd_ok, 'verdict': vd,
                     'confirmed': bool(fwd_ok) and vd in ('works', 'probably works', 'misleads', 'probably misleads'),
                     'guidance': guidance(vd, mv, None, n)})
    meta = {'tau2': tau, 'version': 'v1', 'built_from': 'stratum A (US edge hunts) with B and C as replication', 'overall_DVstar': ov_est, 'overall_se': ov_se,
            'note': 'Diagnostic only. No scorer, no book and no hunter reads this file.'}
    return {'meta': meta, 'rows': rows}


def fmt(x, d=2):
    return '' if x is None else (f'{x:+.{d}f}' if isinstance(x, float) else str(x))


def write_md(reg, path):
    rows = reg['rows']
    order = ['works', 'probably works', 'no evidence', 'probably misleads', 'misleads']
    L = ['# Source-value registry v1', '', '**A diagnostic. No scorer, no book and no hunter reads it.** Built by `scripts/registry.py` from',
         'stratum A (163 US edge hunts, 158 prints); strata B (US dossiers) and C (Europe, Japan, Australia) are replication',
         'columns. DV\\* is the item vote times the move over the priced move, net of what a vote with no source earns in that',
         'name (drift and run-up), shrunk toward the parent level; 80% interval in brackets. Verdict rules: `METHODS.md`.', '']
    small = ['micro', 'small']
    large = ['mid', 'large']
    for v in order:
        sel = [r for r in rows if r['verdict'] == v]
        L += [f'## {v.capitalize()} ({len(sel)} cells)', '']
        if not sel:
            L += ['None.', '']
            continue
        L += ['| source | band | voting items (prints) | hit | DV\\* shrunk [80%] | MV lift | B / C DV\\* | days same sign | guidance |', '|---|---|---|---|---|---|---|---|---|']
        for r in sorted(sel, key=lambda r: (r['band'] not in small, r['code'], r['band'])):
            rp = r['replication']
            L.append(f"| {r['name']} (`{r['code']}`) | {r['band']} | {r['n_vote']} ({r['prints_vote']}) | {fmt(r['hit_rate'] and r['hit_rate'] * 100, 0)}% | "
                     f"{fmt(r['DVstar_shrunk'])} [{fmt(r['ci80'][0])}, {fmt(r['ci80'][1])}] | {fmt(r['MV_lift'])} | "
                     f"{fmt(rp['B']['DVstar_raw'])} ({rp['B']['n_vote']:.0f}) / {fmt(rp['C']['DVstar_raw'])} ({rp['C']['n_vote']:.0f}) | "
                     f"{fmt(r['lodo_sign_share'] and r['lodo_sign_share'] * 100, 0)}% | {r['guidance']} |")
        L.append('')
    ab = [r for r in rows if r.get('MgV_ablation') and r['band'] == 'all']
    if ab:
        L += ['## Marginal value by ablation (overall rows)', '',
              'Sonnet 5.5 judge re-judges every pack holding the code with its items removed. Paired change per changed pack in',
              'sgn(impact) x move/priced, ablated minus the mean of two intact runs: **positive means the judge does better WITHOUT',
              'the source** (it was misleading the judge), negative means the source was helping. No correction for the number of codes.', '',
              '| source | packs changed | paired change | t | within-day rho change | top-20% net change (pp) |', '|---|---|---|---|---|---|']
        for r in sorted(ab, key=lambda r: (r['MgV_ablation']['paired'] or {}).get('t') or 0):
            a = r['MgV_ablation']
            p = a.get('paired') or {}
            dl = a['delta_vs_intact_mean']
            L.append(f"| {r['name']} (`{r['code']}`) | {a['n_packs_changed']} | {fmt(p.get('mean_change_signed_score'))} | {fmt(p.get('t'))} | "
                     f"{fmt(dl.get('rho'), 3)} | {fmt(dl.get('top20_net'), 1)} |")
        L.append('')
    open(path, 'w').write('\n'.join(L))


if __name__ == '__main__':
    fwd = None
    if '--forward' in sys.argv:
        fwd = json.load(open(sys.argv[sys.argv.index('--forward') + 1]))
    reg = build(fwd)
    os.makedirs(f'{SV}/registry', exist_ok=True)
    out = 'registry-forward.json' if fwd else 'registry-v1.json'
    json.dump(reg, open(f'{SV}/registry/{out}', 'w'), indent=1, default=float)
    if not fwd:
        write_md(reg, f'{SV}/registry/REGISTRY.md')
    from collections import Counter
    print(Counter(r['verdict'] for r in reg['rows']))
