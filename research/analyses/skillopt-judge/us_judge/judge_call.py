"""One blind judge call: the trainable skill plus fixed reference documents, one pack in.

The judge runs as `claude -p` with no tools, no MCP servers, no setting sources and its
working directory in a fresh temp dir, and with the two environment variables that make
Claude Code load extra CLAUDE.md directories removed. Checked on 2026-10-05: a call made
this way reports no tools and no CLAUDE.md. That matters here because this repository's
CLAUDE.md quotes realised outcomes for some of these very names.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import time

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
REFERENCE_FILES = ['.claude/agents/unpriced-hunter.md', 'researcher_us/LESSONS.md']
STRIP_ENV = ('CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD', 'CLAUDE_ADDITIONAL_DIRECTORIES')


def _strip_frontmatter(text: str) -> str:
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            return text[end + 4:].lstrip('\n')
    return text


def reference_block() -> str:
    parts = ['# Fixed reference documents (not part of the trainable skill)\n']
    for rel in REFERENCE_FILES:
        with open(os.path.join(R, rel), encoding='utf-8') as fh:
            parts.append(f'\n## `{rel}`\n\n{_strip_frontmatter(fh.read())}')
    return '\n'.join(parts)


def reference_digest() -> str:
    h = hashlib.sha256()
    for rel in REFERENCE_FILES:
        with open(os.path.join(R, rel), 'rb') as fh:
            h.update(fh.read())
    return h.hexdigest()[:12]


def user_prompt(pack: dict) -> str:
    return ('Judge this one company. Reply with the JSON object only.\n\n'
            'PACK:\n' + json.dumps(pack, ensure_ascii=False, indent=1))


def _clean_env() -> dict:
    env = dict(os.environ)
    for k in STRIP_ENV:
        env.pop(k, None)
    return env


def call(system: str, user: str, model: str, timeout: int = 900, retries: int = 3) -> tuple[str, dict]:
    last = ''
    for attempt in range(retries):
        with tempfile.TemporaryDirectory(prefix='usjudge_') as tmp:
            sp = os.path.join(tmp, 'system.txt')
            with open(sp, 'w', encoding='utf-8') as fh:
                fh.write(system)
            cmd = ['claude', '-p', '--system-prompt-file', sp, '--tools', '', '--strict-mcp-config',
                   '--setting-sources', '', '--output-format', 'json', '--no-session-persistence']
            if model:
                cmd += ['--model', model]
            try:
                p = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=timeout,
                                   cwd=tmp, env=_clean_env())
                d = json.loads(p.stdout)
                if d.get('is_error') or not d.get('result'):
                    raise RuntimeError(str(d.get('result') or p.stderr)[:300])
                meta = {'model_usage': list((d.get('modelUsage') or {}).keys()),
                        'cost_usd': d.get('total_cost_usd'), 'duration_ms': d.get('duration_ms')}
                return d['result'], meta
            except Exception as e:  # noqa: BLE001
                last = f'{type(e).__name__}: {e}'
                time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'judge call failed after {retries} tries: {last}')


def parse(text: str) -> dict | None:
    m = re.search(r'\{.*\}', text, re.S)
    if not m:
        return None
    raw = m.group(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            from json_repair import repair_json
            return json.loads(repair_json(raw))
        except Exception:  # noqa: BLE001
            return None
