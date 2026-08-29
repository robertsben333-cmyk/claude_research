#!/usr/bin/env python3
"""Build the fenced corpus for every event in a draw. Resumable, stage by stage.

Runs five stages per event -- anchors, truth, filings, news, social -- and records
what each one produced. A stage that already has output on disk is skipped, and a
stage that fails is recorded and does not stop the event or the run.

Resumability is not a nicety here. The pipeline's own CLAUDE.md records that a
long multi-name session reliably dies partway through, and every long run in this
project so far has been killed by a wall clock. State is written after each stage
so a kill costs one stage, not one run.

Truth is computed and stored per event. That is post-outcome data, and it lives
in `truth.json` beside the corpus rather than inside it -- the sealed reader is
never pointed at the event directory root, only at the specific corpus
subdirectories. Keeping the answer close by is a deliberate risk taken for the
convenience of scoring; the blinding is enforced by what the reader is given, and
that is worth restating wherever this file is edited.

Stages can be run separately with --stages, because they have very different rate
limits: StockTwits throttles hard on an unauthenticated key and is the slowest
part of the run by a wide margin.
"""
import argparse, json, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, ticker_cik_map
import anchors as anchors_mod
import corpus_edgar, corpus_news, corpus_social, truth

STAGES = ["anchors", "truth", "filings", "news", "social"]


def cutoff_of(ev):
    """The print instant, in UTC, from the EDGAR 8-K acceptance time."""
    dt = datetime.fromisoformat(ev["accepted_et"]).astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def event_dir(root, ev):
    return Path(root) / "events" / f"{ev['ticker']}-{ev['event_date']}"


def run_event(ev, root, stages, window_days, max_docs, workers, force=False):
    d = event_dir(root, ev)
    d.mkdir(parents=True, exist_ok=True)
    cutoff = cutoff_of(ev)
    cik = ev.get("cik") or ticker_cik_map().get(ev["ticker"])
    status_path = d / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    status.update({"ticker": ev["ticker"], "company": ev.get("company"),
                   "event_date": ev["event_date"], "session": ev["session"],
                   "cutoff_utc": cutoff, "cik": cik})
    status.setdefault("stages", {})

    def done(stage, marker):
        return not force and (d / marker).exists() and \
            status["stages"].get(stage, {}).get("ok")

    def record(stage, ok, **kw):
        status["stages"][stage] = {"ok": ok, "at": datetime.now(timezone.utc)
                                   .isoformat().replace("+00:00", "Z"), **kw}
        status_path.write_text(json.dumps(status, indent=1), encoding="utf-8")

    if "anchors" in stages and not done("anchors", "anchors.json"):
        try:
            a = anchors_mod.build(ev["ticker"], cik, ev["event_date"], ev["session"])
            (d / "anchors.json").write_text(json.dumps(a, indent=1), encoding="utf-8")
            record("anchors", True, prior_reactions=len(a.get("prior_reactions") or []),
                   proxy_move=a.get("expected_move_proxy_pct"))
        except Exception as e:
            record("anchors", False, error=f"{type(e).__name__}: {e}"[:200])

    if "truth" in stages and not done("truth", "truth.json"):
        try:
            t = truth.move(ev["ticker"], ev["event_date"], ev["session"])
            (d / "truth.json").write_text(json.dumps(t, indent=1), encoding="utf-8")
            record("truth", "error" not in t, move=t.get("actual_move_pct"),
                   error=t.get("error"))
        except Exception as e:
            record("truth", False, error=f"{type(e).__name__}: {e}"[:200])

    if "filings" in stages and not done("filings", "filings_manifest.json"):
        try:
            ok, tot, nf, errs = corpus_edgar.build(ev["ticker"], cik,
                                                   cutoff[:10], str(d))
            record("filings", ok > 0, documents=ok, examined=tot, filings=nf,
                   exhibit_errors=len(errs))
        except Exception as e:
            record("filings", False, error=f"{type(e).__name__}: {e}"[:200])

    if "news" in stages and not done("news", "news_manifest.json"):
        try:
            t2, t3, n, log, wbf = corpus_news.harvest(
                ev["ticker"], ev.get("company", ""), cutoff, str(d),
                window_days, max_docs, ["finnhub"], 1.0, workers)
            record("news", (t2 + t3) > 0, tier2=t2, tier3=t3, candidates=n,
                   archive_lookups_failed=wbf,
                   tier3_share=round(t3 / max(t2 + t3, 1), 3))
        except Exception as e:
            record("news", False, error=f"{type(e).__name__}: {e}"[:200])

    if "social" in stages and not done("social", "social_manifest.json"):
        try:
            n_st, n_hn, meta = corpus_social.harvest(
                ev["ticker"], ev.get("company", ""), cutoff, str(d), window_days)
            record("social", True, stocktwits=n_st, hackernews=n_hn,
                   pages=meta["pages"], covered=meta["window_fully_covered"],
                   error=meta.get("error"))
        except Exception as e:
            record("social", False, error=f"{type(e).__name__}: {e}"[:200])

    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draw", required=True, help="runs/<id>/draw.json")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--stages", default=",".join(STAGES))
    ap.add_argument("--window-days", type=int, default=14)
    ap.add_argument("--max-docs", type=int, default=25)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    draw = json.load(open(a.draw, encoding="utf-8"))
    stages = [s.strip() for s in a.stages.split(",") if s.strip()]
    events = draw["events"][:a.limit] if a.limit else draw["events"]
    progress = Path(a.draw).parent / "progress.json"
    rows = []
    t0 = time.time()
    for i, ev in enumerate(events, 1):
        try:
            st = run_event(ev, a.root, stages, a.window_days, a.max_docs,
                           a.workers, a.force)
        except Exception:
            st = {"ticker": ev["ticker"], "event_date": ev.get("event_date"),
                  "fatal": traceback.format_exc()[-400:]}
        rows.append(st)
        s = st.get("stages", {})
        bits = []
        for k in stages:
            v = s.get(k, {})
            bits.append(f"{k}={'ok' if v.get('ok') else 'FAIL'}")
        news = s.get("news", {}); soc = s.get("social", {})
        print(f"[{i}/{len(events)}] {st.get('ticker'):6} {st.get('event_date')} "
              f"{' '.join(bits)} | news t2={news.get('tier2')} t3={news.get('tier3')} "
              f"| st={soc.get('stocktwits')} | {time.time()-t0:.0f}s", flush=True)
        progress.write_text(json.dumps(
            {"draw": str(a.draw), "stages": stages, "completed": i,
             "of": len(events), "elapsed_s": round(time.time() - t0),
             "events": rows}, indent=1), encoding="utf-8")

    ok_news = sum(1 for r in rows if r.get("stages", {}).get("news", {}).get("ok"))
    t2 = sum(r.get("stages", {}).get("news", {}).get("tier2") or 0 for r in rows)
    t3 = sum(r.get("stages", {}).get("news", {}).get("tier3") or 0 for r in rows)
    st_msgs = sum(r.get("stages", {}).get("social", {}).get("stocktwits") or 0 for r in rows)
    print(f"\n{len(rows)} events | news ok on {ok_news} | tier2={t2} tier3={t3} "
          f"(tier-3 share {t3/max(t2+t3,1):.0%}) | stocktwits messages={st_msgs} "
          f"| {time.time()-t0:.0f}s")
    print(f"-> {progress}")


if __name__ == "__main__":
    main()
