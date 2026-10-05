#!/usr/bin/env python3
"""Train the US judge skill with SkillOpt.

  python3 run.py --skillopt-dir <checkout> --out <dir> --margin 0.006

Two changes to SkillOpt's behaviour, both made from outside its code:
  * the env `us_judge` is registered into scripts/train.py's registry;
  * the gate needs the candidate to beat the current skill by `--margin` (in mean soft),
    not merely to be higher. SkillOpt's default ("strictly higher") accepts noise on a
    gate set this small; the margin is set from two runs of the SAME skill (noise.py).
The CLAUDE.md-loading environment variables are removed for the optimizer too, because
this repository's CLAUDE.md quotes realised outcomes for some of these names.
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skillopt-dir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--margin', type=float, required=True)
    a, rest = ap.parse_known_args()
    for k in ('CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD', 'CLAUDE_ADDITIONAL_DIRECTORIES'):
        os.environ.pop(k, None)
    sys.path.insert(0, a.skillopt_dir)
    sys.path.insert(0, HERE)
    os.makedirs(a.out, exist_ok=True)
    cfg = open(f'{HERE}/config.yaml').read().replace('@SKILLOPT_BASE@', f'{a.skillopt_dir}/configs/_base_/default.yaml').replace('@HERE@', HERE)
    cfg_path = f'{a.out}/config.resolved.yaml'
    open(cfg_path, 'w').write(cfg)

    import scripts.train as T
    import skillopt.engine.trainer as TR
    from skillopt.evaluation.gate import GateResult
    from us_judge.adapter import USJudgeAdapter
    T._ENV_REGISTRY['us_judge'] = USJudgeAdapter

    orig = TR.evaluate_gate

    def gate_with_margin(**kw):
        g = orig(**kw)
        if g.action in ('accept', 'accept_new_best'):
            cand = g.current_score
            if cand < kw['current_score'] + a.margin:
                print(f'  [margin gate] candidate {cand:.4f} does not clear current {kw["current_score"]:.4f} + {a.margin:.4f}: reject')
                return GateResult(action='reject', current_skill=kw['current_skill'], current_score=kw['current_score'],
                                  best_skill=kw['best_skill'], best_score=kw['best_score'], best_step=kw['best_step'])
        return g

    TR.evaluate_gate = gate_with_margin
    sys.argv = ['train.py', '--config', cfg_path, '--out_root', a.out] + rest
    T.main()


if __name__ == '__main__':
    main()
