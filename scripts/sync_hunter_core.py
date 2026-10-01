#!/usr/bin/env python3
"""Copy config/hunter-core.md into every live hunter definition, verbatim.

One source, many copies: the harness loads each agent definition as a single file and an
agent cannot include another, so the shared core is written into each definition between
two markers, right after the frontmatter. Edit config/hunter-core.md, never a copy, and
run this script. `--check` exits 1 if any copy has drifted; smoke_test.py runs it.

It also adds `abs_move_pct`, `p_up` and `rejected_candidates` to a definition's output
schema when that schema does not carry them yet, because the core asks for all three.

    python3 scripts/sync_hunter_core.py           # write
    python3 scripts/sync_hunter_core.py --check   # verify, change nothing
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(REPO, "config", "hunter-core.md")
AGENTS = os.path.join(REPO, ".claude", "agents")

# Every hunter that runs live, in every region. The corpus hunter is the sealed
# backtest's arm and is left as it was, so archived results stay reproducible.
HUNTERS = [
    "unpriced-hunter.md",
    "unpriced-hunter-uk.md", "unpriced-hunter-de.md", "unpriced-hunter-fr.md",
    "unpriced-hunter-it.md", "unpriced-hunter-es.md", "unpriced-hunter-pl.md",
    "unpriced-hunter-nordic.md",
    "unpriced-hunter-jp.md", "unpriced-hunter-au.md", "unpriced-hunter-ca.md",
    "reversal-hunter.md",
]

BEGIN = "<!-- HUNTER-CORE BEGIN: generated from config/hunter-core.md by scripts/sync_hunter_core.py; edit the source, not this copy -->"
END = "<!-- HUNTER-CORE END -->"

SCHEMA_ADD = {
    "abs_move_pct": '  "abs_move_pct": 0.0,',
    "p_up": '  "p_up": 50,',
    "rejected_candidates": (
        '  "rejected_candidates": [\n'
        '    {\n'
        '      "candidate": "a sourced fact you found and did not file",\n'
        '      "source": "https://...",\n'
        '      "reason": "no_source | outside_window | duplicate | contradicted_by_document",\n'
        '      "detail": "one line: which document, which finding it duplicates, or which date"\n'
        '    }\n'
        '  ],'),
}


def render(text, core):
    block = BEGIN + "\n\n" + core.strip() + "\n\n" + END + "\n"
    if BEGIN in text:
        pre, rest = text.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        text = pre + block + "\n" + post.lstrip("\n")
    else:
        m = re.match(r"(---\n.*?\n---\n)", text, re.S)
        if not m:
            raise SystemExit("no frontmatter in a hunter definition")
        text = m.group(1) + "\n" + block + "\n" + text[m.end():].lstrip("\n")
    # The output schema: add what the core asks for, after the
    # searched_and_found_nothing line of the first JSON block.
    anchor = re.search(r'^  "searched_and_found_nothing":.*$', text, re.M)
    if anchor:
        adds = [v for k, v in SCHEMA_ADD.items() if '"%s"' % k not in text.split(END, 1)[1]]
        if adds:
            text = text[:anchor.end()] + "\n" + "\n".join(adds) + text[anchor.end():]
    return text


def main():
    check = "--check" in sys.argv
    core = open(CORE, encoding="utf-8").read()
    drift = []
    for name in HUNTERS:
        path = os.path.join(AGENTS, name)
        old = open(path, encoding="utf-8").read()
        new = render(old, core)
        if new != old:
            drift.append(name)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    if check:
        if drift:
            print("hunter core out of date in: " + ", ".join(drift))
            sys.exit(1)
        print("hunter core current in all %d hunters" % len(HUNTERS))
    else:
        print("updated %d of %d hunters" % (len(drift), len(HUNTERS)))


if __name__ == "__main__":
    main()
