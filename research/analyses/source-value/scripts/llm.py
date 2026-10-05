"""One isolated model call with budget accounting.

Wraps ../../skillopt-judge/us_judge/judge_call.py: `claude -p`, `--tools ""`,
`--strict-mcp-config`, `--setting-sources ""`, a temp working directory and the two
CLAUDE_*ADDITIONAL_DIRECTORIES* variables removed, so no call can read CLAUDE.md (which
quotes realised outcomes for some of these names). Every call's `cost_usd` is added to
`ledger/budget.json` under its arm, and a call is refused before it is made when the arm
or the total would pass its cap.
"""
import fcntl, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SV, '..', 'skillopt-judge'))
from us_judge import judge_call  # noqa: E402

BUDGET = os.path.join(SV, 'ledger', 'budget.json')
CALLS = os.path.join(SV, 'ledger', 'calls.jsonl')
ARM_CAPS = {'ablation': 120.0}
RESERVE = {'default': 0.60}  # headroom kept below a cap so a call in flight cannot overrun


class BudgetExceeded(RuntimeError):
    pass


def _update(fn):
    with open(BUDGET + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        b = json.load(open(BUDGET))
        r = fn(b)
        tmp = BUDGET + '.tmp'
        json.dump(b, open(tmp, 'w'), indent=1)
        os.replace(tmp, BUDGET)
        return r


def check(arm, need=RESERVE['default']):
    def f(b):
        if b['spent_total_usd'] + need > b['cap_total_usd']:
            raise BudgetExceeded(f"total {b['spent_total_usd']:.2f} + {need} > {b['cap_total_usd']}")
        cap = ARM_CAPS.get(arm)
        if cap is not None and b['by_arm'].get(arm, 0) + need > cap:
            raise BudgetExceeded(f"arm {arm} {b['by_arm'].get(arm, 0):.2f} + {need} > {cap}")
    _update(f)


def spent():
    return json.load(open(BUDGET))


def call(system, user, model, arm, tag='', timeout=1200):
    check(arm)
    t0 = time.time()
    text, meta = judge_call.call(system, user, model, timeout=timeout)
    cost = float(meta.get('cost_usd') or 0.0)

    def f(b):
        b['spent_total_usd'] = round(b['spent_total_usd'] + cost, 4)
        b['by_arm'][arm] = round(b['by_arm'].get(arm, 0) + cost, 4)
        if arm == 'ablation':
            b['spent_ablation_usd'] = b['by_arm'][arm]
    _update(f)
    with open(CALLS, 'a') as fh:
        fh.write(json.dumps({'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'arm': arm, 'tag': tag, 'model': model,
                             'served': meta.get('model_usage'), 'cost_usd': cost, 'secs': round(time.time() - t0, 1)}) + '\n')
    served = meta.get('model_usage') or []
    if model and served and not any(model in s for s in served):
        meta['served_mismatch'] = True
    return text, meta


parse = judge_call.parse
