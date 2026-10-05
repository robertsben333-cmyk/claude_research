#!/usr/bin/env python3
"""Copy the parts of a SkillOpt output dir worth keeping into results/<name>/.

Kept: every skill version, history, per-step record, candidate and merged patch, the
meta-skill and slow-update text, and every rollout reduced to the judge's numbers and
the reward (no packs, no transcripts: those are rebuilt from data/ and are large).
  python3 archive_run.py <skillopt out dir> <name>
"""
import json, os, shutil, sys

src, name = sys.argv[1], sys.argv[2]
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', name)
os.makedirs(dst, exist_ok=True)
KEEP = {'history.json', 'best_skill.md', 'config.resolved.yaml', 'step_record.json', 'candidate_skill.md',
        'merged_patch.json', 'ranked_edits.json', 'edit_apply_report.json'}
FIELDS = ('name_id', 'impact_sum', 'p_up', 'abs_move_pct', 'r', 'soft', 'hard', 'reward_mode', 'scale',
          'judge_model_served', 'cost_usd')
for root, dirs, files in os.walk(src):
    dirs[:] = [d for d in dirs if d != 'predictions']
    rel = os.path.relpath(root, src)
    for f in files:
        keep_md = f.endswith('.md') and (rel.startswith(('skills', 'meta_skill', 'slow_update')) or f in KEEP)
        if f in KEEP or keep_md:
            os.makedirs(os.path.join(dst, rel), exist_ok=True)
            shutil.copy(os.path.join(root, f), os.path.join(dst, rel, f))
        elif f == 'rollouts.json':
            os.makedirs(os.path.join(dst, rel), exist_ok=True)
            R = json.load(open(os.path.join(root, f)))
            json.dump([{k: r.get(k) for k in FIELDS} for r in R], open(os.path.join(dst, rel, 'judged.json'), 'w'), indent=0)
print(dst)
