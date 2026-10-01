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

# Model variants: a definition generated WHOLE from another one, with only frontmatter
# fields replaced. unpriced-hunter-sonnet is stage E-S (2026-10-01): the US hunt with the
# hunters on Sonnet and everything else unchanged, so the hunter model is the only
# variable. Never hand-edit a variant; edit its source and run this script.
VARIANTS = {
    # stage E-P (2026-10-01): the US hunter on Opus 5.5 as the SEARCHER for a four-model
    # judging panel. Same definition with config/searcher-addendum.md inserted after the
    # core, so the search, the event check, the hard source rule and the output contract
    # stay identical to stage E's hunter.
    "unpriced-searcher.md": ("unpriced-hunter.md", {
        "name": "unpriced-searcher",
        "model": "claude-opus-5-5",
        "description": ("Stage E-P. The unpriced-hunter run as the evidence SEARCHER for a "
                        "four-model judging panel: same search and output contract, with "
                        "breadth over polish because its own sizes are not used to rank. "
                        "Generated from unpriced-hunter.md plus config/searcher-addendum.md "
                        "by scripts/sync_hunter_core.py; never edit this copy. Give it the "
                        "ticker, the event window and the path to the sealed baseline."),
    }, "searcher-addendum.md"),
    "unpriced-hunter-sonnet.md": ("unpriced-hunter.md", {
        "name": "unpriced-hunter-sonnet",
        "model": "sonnet",
        "description": ("Stage E-S. The unpriced-hunter, byte for byte, run on Sonnet instead "
                        "of Opus so the hunter model is the only thing that differs from "
                        "stage E. Generated from unpriced-hunter.md by "
                        "scripts/sync_hunter_core.py; never edit this copy. Same contract - "
                        "give it the ticker, the event window and the path to the sealed "
                        "priced-in baseline."),
    }),
}
# Stage E-P judges (2026-10-01): one source, config/panel-judge.md, one definition per
# model, each pinned to a full model ID. Four DIFFERENT models because the measured gain
# came from model diversity: five runs of one model added nothing over one
# (research/analyses/judge-lab/). Never hand-edit a judge; edit the source.
PANEL_SOURCE = os.path.join(REPO, "config", "panel-judge.md")
PANEL_JUDGES = {
    "panel-judge-opus5.md": "claude-opus-5",
    "panel-judge-opus55.md": "claude-opus-5-5",
    "panel-judge-sonnet55.md": "claude-sonnet-5-5",
    "panel-judge-fable51.md": "claude-fable-5-1",
}
PANEL_NOTE = ("<!-- GENERATED from config/panel-judge.md by scripts/sync_hunter_core.py; "
              "edit the source, not this copy -->\n\n")


def render_judge(name, model, body):
    desc = ("Stage E-P panel judge on %s. Judges the day's searcher evidence blind, from a "
            "packs file with the searcher's sizes removed, and returns abs_move_pct, p_up and "
            "a signed impact_sum per company. Read and Write only; one instance per model per "
            "day; give it the packs file and the output path." % model)
    return ("---\nname: %s\ndescription: %s\ntools: Read, Write\nmodel: %s\neffort: high\n"
            "maxTurns: 60\ncolor: cyan\n---\n\n" % (name[:-3], desc, model)) + PANEL_NOTE + body.strip() + "\n"


VARIANT_NOTE = ("<!-- GENERATED from %s by scripts/sync_hunter_core.py with the frontmatter "
                "above replaced; edit the source, not this copy -->\n\n")


def render_variant(src_text, fields, src_name, addendum=None):
    m = re.match(r"---\n(.*?)\n---\n", src_text, re.S)
    if not m:
        raise SystemExit("no frontmatter in " + src_name)
    lines = []
    for line in m.group(1).split("\n"):
        key = line.split(":", 1)[0]
        lines.append("%s: %s" % (key, fields[key]) if key in fields else line)
    body = src_text[m.end():].lstrip("\n")
    if addendum:
        if END not in body:
            raise SystemExit("an addendum needs the hunter core in " + src_name)
        pre, post = body.split(END, 1)
        body = pre + END + "\n\n" + addendum.strip() + "\n" + post
    return "---\n" + "\n".join(lines) + "\n---\n\n" + VARIANT_NOTE % src_name + body


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
    for name, spec in VARIANTS.items():
        src, fields = spec[0], spec[1]
        add = open(os.path.join(REPO, "config", spec[2]), encoding="utf-8").read() if len(spec) > 2 else None
        path = os.path.join(AGENTS, name)
        src_text = open(os.path.join(AGENTS, src), encoding="utf-8").read()
        if src in HUNTERS:
            src_text = render(src_text, core)
        new = render_variant(src_text, fields, src, add)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if new != old:
            drift.append(name)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    body = open(PANEL_SOURCE, encoding="utf-8").read()
    for name, model in PANEL_JUDGES.items():
        path = os.path.join(AGENTS, name)
        new = render_judge(name, model, body)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if new != old:
            drift.append(name)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    if check:
        if drift:
            print("hunter core out of date in: " + ", ".join(drift))
            sys.exit(1)
        print("hunter core current in all %d hunters, %d variants and %d panel judges"
              % (len(HUNTERS), len(VARIANTS), len(PANEL_JUDGES)))
    else:
        print("updated %d of %d hunters, variants and panel judges"
              % (len(drift), len(HUNTERS) + len(VARIANTS) + len(PANEL_JUDGES)))


if __name__ == "__main__":
    main()
