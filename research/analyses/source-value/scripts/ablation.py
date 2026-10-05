#!/usr/bin/env python3
"""MgV (b): the ablation arm. A Sonnet 5.5 panel judge re-judges stratum A's packs with all
items of one subtype removed; the change in its within-day rho, hit rate and top-20% book
is the subtype's marginal value.

  python3 scripts/ablation.py intact            # intact arm, two runs (also the noise yardstick)
  python3 scripts/ablation.py ablate <code>...  # one ablated run per code, only packs that contain it
  python3 scripts/ablation.py score             # results/ablation.json

The judge: ../skillopt-judge/seed_skill.md plus the fixed reference block (hunter definition
and US lessons), exactly as ../skillopt-judge/us_judge/adapter.py builds it; isolated call.
An item is removed when at least half of the labelling runs gave it the code (after the v1
merges). Packs are stratum A's (anonymised where needed, opaque ids). Budget arm 'ablation',
capped at $120 in scripts/llm.py.
"""
import json, os, statistics as st, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SV, '..', 'skillopt-judge'))
sys.path.insert(0, os.path.join(SV, '..', 'judge-lab'))
import llm  # noqa: E402
from us_judge import judge_call  # noqa: E402

OUT = f'{SV}/results/ablation'
MODEL = 'claude-sonnet-5-5'


def system():
    return open(os.path.join(SV, '..', 'skillopt-judge', 'seed_skill.md')).read() + '\n\n---\n\n' + judge_call.reference_block()


def packs():
    E = {e['pack_id']: e for e in json.load(open(f'{SV}/data/events.json')) if e['stratum'] == 'A' and not e['duplicate_hunt']}
    return [p for p in json.load(open(f'{SV}/data/packs-A.json')) if p['id'] in E]


def codes_by_item():
    import core
    mm = core.merge_map()
    L = core.load_labels()
    out = {}
    for pid, runs in L.items():
        if not pid.startswith('A-'):
            continue
        for r in runs:
            for i, x in r.items():
                c = mm.get(x.get('subtype'), x.get('subtype'))
                out.setdefault((pid, i), []).append(c)
    return out


def judge(p, path):
    if os.path.exists(path):
        return 'skip'
    text, meta = llm.call(system(), judge_call.user_prompt(p), MODEL, 'ablation', os.path.basename(path), timeout=1200)
    j = llm.parse(text) or {}
    try:
        imp = float(j.get('impact_sum') or 0)
    except (TypeError, ValueError):
        imp = None
    json.dump({'pack': p['id'], 'impact_sum': imp, 'p_up': j.get('p_up'), 'abs_move_pct': j.get('abs_move_pct'), 'meta': meta,
               'n_items': len(p['evidence'])}, open(path, 'w'))
    return 'ok'


def run_jobs(jobs, workers=6):
    def f(j):
        try:
            return judge(*j)
        except llm.BudgetExceeded as e:
            return f'budget: {e}'
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(f, jobs))


def cmd_intact():
    jobs = []
    for k in (0, 1):
        d = f'{OUT}/intact{k}'
        os.makedirs(d, exist_ok=True)
        jobs += [(p, f'{d}/{p["id"]}.json') for p in packs()]
    from collections import Counter
    print(Counter(run_jobs(jobs)), llm.spent()['by_arm'].get('ablation'))


def cmd_ablate(codes):
    import core
    grp = {x['id']: x['group'] for x in core.codebook()['subtypes']}
    cbi0 = codes_by_item()
    cbi = cbi0
    P = packs()
    from collections import Counter
    for c in codes:
        d = f'{OUT}/minus-{c.replace(":", "_")}'
        os.makedirs(d, exist_ok=True)
        if c.startswith('GROUP:'):  # a whole group: map every item's codes to their group
            g = c[6:]
            cbi = {k: [c if ((x[2:] if x.startswith('G:') else grp.get(x)) == g) else x for x in v] for k, v in cbi0.items()}
        else:
            cbi = cbi0
        jobs = []
        for p in P:
            keep = [e for e in p['evidence'] if sum(x == c for x in cbi.get((p['id'], e['i']), [])) * 2 < max(1, len(cbi.get((p['id'], e['i']), [])))]
            if len(keep) == len(p['evidence']):
                continue
            q = dict(p)
            q['evidence'] = keep
            jobs.append((q, f'{d}/{p["id"]}.json'))
        json.dump({'code': c, 'n_packs_changed': len(jobs)}, open(f'{d}/_meta.json', 'w'))
        res = run_jobs(jobs)
        print(c, len(jobs), Counter(res), 'ablation spend', llm.spent()['by_arm'].get('ablation'))
        if any(str(r).startswith('budget') for r in res):
            print('budget reached; stopping the arm')
            break


def read(d):
    out = {}
    if not os.path.isdir(d):
        return out
    for f in os.listdir(d):
        if f.endswith('.json') and not f.startswith('_'):
            j = json.load(open(f'{d}/{f}'))
            out[j['pack']] = j['impact_sum']
    return out


def metrics(pred, rows):
    import judge_lab as J
    pr = {r['id']: pred.get(r['pack']) for r in rows}
    ok = [r for r in rows if pr.get(r['id']) not in (None, 0)]
    tm = J.top_metrics(rows, pr)
    return {'rho': J.rho(rows, pr), 'views': len(ok), 'hit': (sum(J.sgn(pr[r['id']]) * r['move'] > 0 for r in ok) / len(ok)) if ok else None,
            'top20_n': tm['n'], 'top20_hits': tm['hits'], 'top20_net': tm['net']}


def cmd_score():
    E = [e for e in json.load(open(f'{SV}/data/events.json')) if e['stratum'] == 'A' and not e['duplicate_hunt']]
    rows = [{'id': e['id'], 'pack': e['pack_id'], 'region': 'us', 'day': e['day'], 'move': e['move'], 'dv': e['dollar_vol'] or 0} for e in E]
    i0, i1 = read(f'{OUT}/intact0'), read(f'{OUT}/intact1')
    mean_intact = {k: (i0[k] + i1[k]) / 2 for k in i0 if k in i1 and i0[k] is not None and i1[k] is not None}
    base = {'intact0': metrics(i0, rows), 'intact1': metrics(i1, rows), 'intact_mean': metrics(mean_intact, rows)}
    out = {'baseline': base, 'codes': {}}
    for d in sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []:
        if not d.startswith('minus-'):
            continue
        ab = read(f'{OUT}/{d}')
        changed = set(ab)
        # ablated arm: changed packs re-judged; unchanged packs keep the intact mean
        pred = dict(mean_intact)
        pred.update({k: v for k, v in ab.items() if v is not None})
        # noise yardstick on the same changed packs: intact0 there, intact mean elsewhere (vs intact1 there)
        n0 = dict(mean_intact); n0.update({k: i0[k] for k in changed if k in i0})
        n1 = dict(mean_intact); n1.update({k: i1[k] for k in changed if k in i1})
        mA, m0, m1 = metrics(pred, rows), metrics(n0, rows), metrics(n1, rows)
        noise = {k: (abs(m0[k] - m1[k]) if m0[k] is not None and m1[k] is not None else None) for k in ('rho', 'hit', 'top20_net')}
        # paired per-pack: sign agreement of ablated vs each intact run on changed packs
        flips = sum(1 for k in changed if k in i0 and ab[k] is not None and (ab[k] > 0) != (i0[k] > 0) and ab[k] != 0 and i0[k] != 0)
        flips_noise = sum(1 for k in changed if k in i0 and k in i1 and i0[k] and i1[k] and (i0[k] > 0) != (i1[k] > 0))
        # paired per pack (changed packs only): signed score sgn(impact) x move/priced (Winsorised at 4)
        mn = {e['pack_id']: max(-4, min(4, e['move'] / e['priced_move'])) for e in E}
        sg = lambda v: (v > 0) - (v < 0) if v is not None else 0  # noqa: E731
        dd, nn = [], []
        for k in changed:
            if k in i0 and k in i1 and ab.get(k) is not None:
                dd.append(sg(ab[k]) * mn[k] - (sg(i0[k]) + sg(i1[k])) / 2 * mn[k])
                nn.append((sg(i0[k]) - sg(i1[k])) / 2 * mn[k])
        paired = None
        if len(dd) > 2:
            m, sdv = st.mean(dd), st.stdev(dd)
            paired = {'n': len(dd), 'mean_change_signed_score': m, 'se': sdv / len(dd) ** .5, 't': m / (sdv / len(dd) ** .5) if sdv else None,
                      'noise_sd_per_pack': st.pstdev(nn), 'packs_sign_changed': sum(1 for k in changed if k in i0 and ab.get(k) and i0.get(k) and sg(ab[k]) != sg((i0[k] + i1.get(k, i0[k])) / 2))}
        out['codes'][d[6:]] = {'n_packs_changed': len(changed), 'ablated': mA, 'paired': paired,
                               'delta_vs_intact_mean': {k: (mA[k] - base['intact_mean'][k]) if mA[k] is not None and base['intact_mean'][k] is not None else None for k in ('rho', 'hit', 'top20_net')},
                               'noise_intact0_vs_intact1_same_packs': noise, 'sign_flips_vs_intact0': flips, 'sign_flips_intact0_vs_intact1': flips_noise}
    json.dump(out, open(f'{SV}/results/ablation.json', 'w'), indent=1)
    print(json.dumps(out['baseline'], indent=1))
    for c, v in out['codes'].items():
        print(c, v['n_packs_changed'], {k: round(x, 3) if x is not None else None for k, x in v['delta_vs_intact_mean'].items()},
              'noise', {k: round(x, 3) if x is not None else None for k, x in v['noise_intact0_vs_intact1_same_packs'].items()}, 'flips', v['sign_flips_vs_intact0'], v['sign_flips_intact0_vs_intact1'])


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'intact':
        cmd_intact()
    elif c == 'ablate':
        cmd_ablate(sys.argv[2:])
    elif c == 'score':
        cmd_score()
