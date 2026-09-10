#!/usr/bin/env python3
"""Compatibility shim. The real script is `edge/scripts/edge_universe.py`.

Stage E's Routine (`trig_01CvGQJWoKeNLXWCxiffM3ED`) holds a prompt that was
pasted in by hand, names this path, and **verifies it exists before doing
anything else**. An agent session cannot edit that prompt -- `update_trigger`
refuses any Routine an agent did not create -- so moving the script without
leaving something here would have stopped the next unattended run at step 0,
before step 0b sold the previous day's book.

Delete this file only after `edge/routine-prompts/edge-hunt.md` has been
re-pasted into the Routine with the new path, and the Routine's `updated_at`
confirms it.

`runpy` is used rather than an import so that `__file__` inside the real script
is its own path: every one of them resolves the repo root as
`Path(__file__).resolve().parents[2]`, which is only correct from
`edge/scripts/`.
"""
import runpy
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "edge" / "scripts" / "edge_universe.py"

if __name__ == "__main__":
    # Guarded, so that importing this name by accident does not run a CLI. Anything
    # that wants the module itself should put `edge/scripts` on sys.path and import
    # from there; this file forwards a command line and nothing else.
    if not TARGET.exists():
        raise SystemExit(f"shim: {TARGET} is missing; the tree is not intact")
    sys.argv[0] = str(TARGET)
    runpy.run_path(str(TARGET), run_name="__main__")
