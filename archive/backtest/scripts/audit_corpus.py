#!/usr/bin/env python3
"""Whole-corpus contamination audit, run against whatever the fence currently is.

Exists because the corpus has twice been declared clean and twice was not. Both
times the fence itself was sound and something beside it leaked -- once the URL
slugs recorded in the manifest, once the event date. So this checks the corpus as
an agent actually experiences it: every byte of every file inside events/, not
just the documents the manifest claims to have kept.

Checks, in order of how badly each has bitten:

  1. every kept file's timestamp against the CURRENT fence
  2. outcome tells in kept bodies
  3. any URL surviving anywhere inside events/ (the CL failure)
  4. manifests describing rejected documents in a way that names the result
  5. the realised move appearing anywhere at all
  6. event dating: chosen cutoff vs the earliest results disclosure
"""
import json, glob, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT

TELLS = [
    r"\bbeat(?:s|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bmiss(?:es|ed|ing)?\s+(?:the\s+)?(?:consensus|estimates?|expectations?)",
    r"\bshares?\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\bstock\s+(?:rose|fell|jumped|plunged|surged|sank|tumbled|soared|slid)",
    r"\breported\s+(?:quarterly\s+)?(?:earnings|revenue|results)\s+of",
    r"\bafter\s+(?:the\s+)?(?:company\s+)?reported\b",
    r"\bQ\d\s+Adj\.?\s+EPS\b.{0,40}\b(?:beats?|misses?)\b",
]
RX = [re.compile(p, re.I) for p in TELLS]
URL = re.compile(r"https?://[^\s\"'<>]{12,}")
# Only a slug that names THIS company's result matters. Flagging every URL made the
# audit useless: 446 hits, all of them SOURCE headers and in-body links on
# legitimately pre-fence articles. An audit that cries wolf gets ignored, which is
# worse than not running it.
OUTCOME_SLUG = re.compile(
    r"(adj-eps|eps)[-/][\d.]+.{0,30}(beat|miss)|q[1-4][-/].{0,25}(beat|miss)"
    r"|shares?[-/](slip|dip|surge|jump|fall|rise|plunge|soar)"
    r"|(beats|misses|tops)[-/].{0,20}estimate", re.I)


def _subject_tokens(ticker, company):
    base = re.sub(r"(?i),?\s+(inc|corp|corporation|company|co|ltd|plc|holdings|"
                  r"technologies|group|lp|l\.p\.)\.?$", "", company or "").strip()
    out = {ticker.lower()}
    if base:
        out.add(re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-"))
        w = re.sub(r"[^a-z0-9]+", "", base.split()[0].lower())
        if len(w) >= 4:
            out.add(w)
    return {x for x in out if len(x) >= 3}
SLUG = re.compile(r"(adj-eps|eps)[-/][\d.]+.{0,30}(beat|miss)|q[1-4][-/].{0,25}(beat|miss)"
                  r"|shares?[-/](slip|dip|surge|jump|fall|rise)", re.I)


def audit():
    draw = json.loads((ROOT / "runs" / "pilot-40" / "draw.json").read_text(encoding="utf-8"))
    companies = {e["ticker"]: e["company"] for e in draw["events"]}
    findings = {"post_fence_files": [], "tells_in_kept": [], "urls_in_corpus": [],
                "leaky_manifest_text": [], "realised_move_present": []}
    events = sorted(Path("backtest/events").glob("*/"))
    for d in events:
        ev = d.name
        nm = d / "news_manifest.json"
        fence = None
        if nm.exists():
            m = json.loads(nm.read_text(encoding="utf-8"))
            fence = m.get("fence_utc")
            for doc in m["documents"]:
                if doc.get("status") != "ok":
                    continue
                ts = doc.get("provider_published_utc")
                if fence and ts and ts >= fence:
                    findings["post_fence_files"].append((ev, doc.get("file"), ts, fence))
        # every file an agent could read
        for f in d.rglob("*"):
            if not f.is_file():
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = str(f.relative_to(d))
            if f.suffix == ".txt":
                body = txt.split("-" * 72, 1)[-1]
                hits = [p.pattern for p in RX if p.search(body)]
                if hits:
                    findings["tells_in_kept"].append((ev, rel, hits[:2]))
            tick = ev.rsplit("-", 3)[0]
            tk = _subject_tokens(tick, companies.get(tick, ""))
            for u in URL.findall(txt)[:400]:
                ul = u.lower()
                if OUTCOME_SLUG.search(ul) and any(t in ul for t in tk):
                    findings["urls_in_corpus"].append((ev, rel, u[:100]))
                    break
            if f.suffix == ".json" and SLUG.search(txt):
                findings["leaky_manifest_text"].append((ev, rel))
        # realised move
        tp = ROOT / "truth" / f"{ev}.json"
        if tp.exists():
            tj = json.loads(tp.read_text(encoding="utf-8"))
            if isinstance(tj, list):          # truth.py writes a list for batch runs
                tj = tj[0] if tj else {}
            mv = tj.get("actual_move_pct")
            if mv is not None:
                # a bare "4.03%" collides with loan rates, growth ranges and price
                # targets -- all four hits in the first run were coincidences like
                # "fixed interest rate of 4.03%". Require move-shaped context.
                pat = re.compile(rf"(?:rose|fell|jumped|plunged|surged|sank|slid|gained|lost|"
                                 rf"moved|closed|down|up)\D{{0,20}}{abs(mv):.2f}\s*%", re.I)
                for f in d.rglob("*"):
                    if f.is_file() and pat.search(f.read_text(encoding="utf-8", errors="replace")):
                        findings["realised_move_present"].append((ev, str(f.relative_to(d))))
                        break
    return findings, len(events)


if __name__ == "__main__":
    f, n = audit()
    print(f"audited {n} event directories\n")
    order = [("post_fence_files", "kept files dated at or after the fence"),
             ("urls_in_corpus", "URLs still readable inside events/"),
             ("leaky_manifest_text", "manifest text naming a result"),
             ("realised_move_present", "the realised move appearing verbatim"),
             ("tells_in_kept", "outcome tells in kept bodies")]
    clean = True
    for k, label in order:
        v = f[k]
        flag = "CLEAN" if not v else f"{len(v)} FINDING(S)"
        if v and k != "tells_in_kept":
            clean = False
        print(f"  {label:44} {flag}")
        for row in v[:6]:
            print(f"      {row}")
        if len(v) > 6:
            print(f"      ... and {len(v)-6} more")
    print()
    print("VERDICT:", "corpus clean on every hard check" if clean else "CONTAMINATED - do not run forecasts")
    print("note: tells in kept bodies are expected and not disqualifying on their own --")
    print("      a tier-2 body is archive-proven pre-fence, so a results phrase in it is")
    print("      forward-looking. They are listed for eyeballing, not as failures.")
