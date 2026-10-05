#!/usr/bin/env python3
"""Run one skill over one split, n times, and score it the way judge-lab does.

  python3 evaluate.py --skillopt-dir <checkout> --skill seed_skill.md --split val --runs 2 --tag seed

Writes runs/<tag>-<split>-<k>/ (rollouts and per-name trajectories) and
results/<tag>-<split>.json. With --runs 2 it also reports the run-to-run noise of the
gate score, which is what sets run.py's --margin: two runs of the SAME skill differ by
this much with nothing changed.
"""
import argparse, json, os, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'judge-lab'))


def metrics(items, res):
    import judge_lab as J
    rows = []
    for it in items:
        o = it['outcome']
        rows.append({'id': it['name_id'], 'region': 'us', 'day': o['day'], 'move': o['move_pct'],
                     'dv': o['dollar_vol'], 'priced': o['priced_move_pct']})
    pred = {r['name_id']: (r['impact_sum'] if r['impact_sum'] is not None else 0.0) for r in res}
    soft = [r['soft'] for r in res]
    views = [r for r in res if r['impact_sum']]
    hit = [int((r['impact_sum'] > 0) == (next(x['move'] for x in rows if x['id'] == r['name_id']) > 0)) for r in views]
    out = {'n': len(res), 'soft_mean': st.mean(soft), 'r_mean': st.mean(r['r'] for r in res),
           'views': len(views), 'sign_hits': f'{sum(hit)}/{len(hit)}',
           'rho_within_day': J.rho(rows, pred)}
    for share in (0.15, 0.20):
        m = J.top_metrics(rows, pred, share)
        out[f'top{int(share*100)}'] = {k: m[k] for k in ('n', 'hits', 'mean', 'net', 't', 'short_all_net')}
    # magnitude: do the largest |impact| names move more than priced?
    k = max(1, round(0.2 * len(rows)))
    top = sorted(rows, key=lambda x: -abs(pred[x['id']]))[:k]
    out['top20_abs_move_over_priced'] = st.mean(abs(x['move']) / x['priced'] for x in top)
    out['all_abs_move_over_priced'] = st.mean(abs(x['move']) / x['priced'] for x in rows)
    out['parse_failures'] = sum(1 for r in res if r['impact_sum'] is None)
    out['models_served'] = sorted({m for r in res for m in (r.get('judge_model_served') or [])})
    out['cost_usd'] = round(sum(r.get('cost_usd') or 0 for r in res), 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skillopt-dir', required=True)
    ap.add_argument('--skill', required=True)
    ap.add_argument('--split', required=True, choices=['train', 'val', 'test'])
    ap.add_argument('--runs', type=int, default=1)
    ap.add_argument('--tag', required=True)
    ap.add_argument('--model', default='claude-sonnet-5-5')
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    for k in ('CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD', 'CLAUDE_ADDITIONAL_DIRECTORIES'):
        os.environ.pop(k, None)
    sys.path.insert(0, a.skillopt_dir)
    sys.path.insert(0, HERE)
    from us_judge.adapter import USJudgeAdapter
    from us_judge import judge_call

    items = json.load(open(f'{HERE}/data/{a.split}/items.json'))
    ad = USJudgeAdapter(split_dir=f'{HERE}/data', workers=a.workers)
    ad.target_model = a.model
    skill = open(a.skill).read()
    runs = []
    for k in range(a.runs):
        d = f'{HERE}/runs/{a.tag}-{a.split}-{k}'
        res = ad.rollout(items, skill, d)
        runs.append(res)
        # re-judge format, so judge_lab can read it like any other arm
        json.dump([{'id': r['name_id'], 'impact_sum': r['impact_sum'], 'p_up': r['p_up'],
                    'abs_move_pct': r['abs_move_pct']} for r in res], open(f'{d}/out.json', 'w'), indent=1)
    out = {'skill': a.skill, 'split': a.split, 'model': a.model, 'reference_digest': judge_call.reference_digest(),
           'runs': [metrics(items, r) for r in runs]}
    if len(runs) >= 2:
        s0 = {r['id']: r['soft'] for r in runs[0]}
        d = [r['soft'] - s0[r['id']] for r in runs[1]]
        se = st.stdev(d) / len(d) ** .5
        out['noise'] = {'mean_soft_diff_run1_minus_run0': st.mean(d), 'sd_item_diff': st.stdev(d),
                        'se_of_mean_diff': se, 'margin_one_sided_95': 1.645 * se,
                        'same_sign_share': st.mean(int((a_['impact_sum'] or 0) * (b['impact_sum'] or 0) > 0)
                                                   for a_, b in zip(runs[0], runs[1]) if a_['impact_sum'] or b['impact_sum'])}
    os.makedirs(f'{HERE}/results', exist_ok=True)
    json.dump(out, open(f'{HERE}/results/{a.tag}-{a.split}.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
