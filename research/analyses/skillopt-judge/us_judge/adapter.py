"""SkillOpt environment: the US panel judge, one blinded pack per episode."""
from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from skillopt.datasets.base import BatchSpec, SplitDataLoader
from skillopt.envs.base import EnvAdapter
from skillopt.prompts import load_prompt

from . import judge_call, reward

HERE = Path(__file__).parent
OMITTED = '\n\n[Fixed reference documents omitted here: the unpriced-hunter definition with the shared core, and researcher_us/LESSONS.md. The judge saw them in full; they are not part of the trainable skill and must not be edited.]'


class USJudgeLoader(SplitDataLoader):
    def load_split_items(self, split_path: str) -> list[dict]:
        with open(Path(split_path) / 'items.json', encoding='utf-8') as fh:
            return json.load(fh)


class USJudgeAdapter(EnvAdapter):
    def __init__(self, split_dir: str = '', split_mode: str = 'split_dir', workers: int = 6,
                 analyst_workers: int = 4, failure_only: bool = False, minibatch_size: int = 8,
                 edit_budget: int = 4, seed: int = 42, limit: int = 0, **_: object) -> None:
        self.workers = int(workers)
        self.analyst_workers = analyst_workers
        self.failure_only = failure_only
        self.minibatch_size = minibatch_size
        self.edit_budget = edit_budget
        self.dataloader = USJudgeLoader(split_dir=split_dir, split_mode=split_mode, seed=seed, limit=limit)
        self._reference = judge_call.reference_block()

    def setup(self, cfg: dict) -> None:
        super().setup(cfg)
        self.dataloader.setup(cfg)
        self.target_model = cfg.get('target_model') or 'claude-sonnet-5-5'

    def get_dataloader(self):
        return self.dataloader

    def build_env_from_batch(self, batch: BatchSpec, **kwargs):
        return list(batch.payload or [])

    def build_train_env(self, batch_size: int, seed: int, **kwargs):
        return self.build_env_from_batch(self.dataloader.build_train_batch(batch_size=batch_size, seed=seed, **kwargs))

    def build_eval_env(self, env_num: int, split: str, seed: int, **kwargs):
        return self.build_env_from_batch(self.dataloader.build_eval_batch(env_num=env_num, split=split, seed=seed, **kwargs))

    def get_task_types(self) -> list[str]:
        return ['us_opus5', 'us_opus55']

    # analyst prompts: SkillOpt's own, plus the rules this domain needs
    def _with_rules(self, name: str) -> str:
        return load_prompt(name) + '\n\n' + (HERE / 'prompts' / 'domain_rules.md').read_text(encoding='utf-8')

    def get_error_minibatch_prompt(self) -> str | None:
        return self._with_rules('analyst_error')

    def get_success_minibatch_prompt(self) -> str | None:
        return self._with_rules('analyst_success')

    def _call(self, item: dict, skill: str) -> tuple:
        system = skill + '\n\n---\n\n' + self._reference
        user = judge_call.user_prompt(item['pack'])
        meta, judged, text = {}, None, ''
        try:
            text, meta = judge_call.call(system, user, self.target_model)
            judged = judge_call.parse(text)
        except RuntimeError as e:
            text = f'[judge call failed: {e}]'
        impact = None
        if judged is not None:
            try:
                impact = float(judged.get('impact_sum') or 0)
            except (TypeError, ValueError):
                impact = None
        return user, text, meta, judged, impact

    def _finish(self, item: dict, skill: str, pred_dir: Path, called: tuple, scale: float) -> dict:
        user, text, meta, judged, impact = called
        sc = reward.score(impact, item['outcome'], scale)
        if judged is None:
            sc['fail_reason'] = 'Output was not one parseable JSON object. ' + sc['fail_reason']
        tdir = pred_dir / item['id']
        tdir.mkdir(parents=True, exist_ok=True)
        conv = [{'role': 'system', 'content': skill + OMITTED},
                {'role': 'user', 'content': user},
                {'role': 'assistant', 'content': text}]
        (tdir / 'conversation.json').write_text(json.dumps(conv, ensure_ascii=False, indent=1), encoding='utf-8')
        (tdir / 'judged.json').write_text(json.dumps({'judged': judged, 'meta': meta, 'score': sc, 'scale': scale},
                                                     ensure_ascii=False, indent=1), encoding='utf-8')
        return {
            'id': item['id'], 'name_id': item['name_id'], 'hard': sc['hard'], 'soft': sc['soft'],
            'r': sc['r'], 'impact_sum': impact, 'p_up': (judged or {}).get('p_up'),
            'abs_move_pct': (judged or {}).get('abs_move_pct'), 'reward_mode': reward.MODE, 'scale': scale,
            'predicted_answer': json.dumps(judged, ensure_ascii=False) if judged else text[:500],
            'task_description': f"Judge the blinded evidence pack for {item['name_id']} and size it.",
            'task_type': item['task_type'], 'fail_reason': sc['fail_reason'],
            'reference_text': reward.hidden_reference(impact, judged, item['outcome'], sc),
            'target_system_prompt': skill + OMITTED, 'target_user_prompt': user, 'n_turns': 1,
            'judge_model_served': meta.get('model_usage'), 'cost_usd': meta.get('cost_usd'),
        }

    def rollout(self, env_manager, skill_content: str, out_dir: str, **kwargs) -> list[dict]:
        items: list[dict] = env_manager
        pred_dir = Path(out_dir) / 'predictions'
        pred_dir.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            called = list(ex.map(lambda it: self._call(it, skill_content), items))
        scale = reward.batch_scale([(c[4] or 0.0) / it['outcome']['priced_move_pct'] for it, c in zip(items, called)])
        results = [self._finish(it, skill_content, pred_dir, c, scale) for it, c in zip(items, called)]
        Path(out_dir, 'rollouts.json').write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
        return results
