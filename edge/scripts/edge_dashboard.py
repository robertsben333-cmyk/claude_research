#!/usr/bin/env python3
"""Build the stage E research dashboard from the analysis JSON on disk.

The dashboard is GENERATED, never hand-edited. Every number on every page is read
out of `edge/analysis/*.json`, which is written by the scripts that did the
measuring, so a page cannot drift from the run that produced it. Re-run the
analysis scripts, then re-run this.

    python3 edge/scripts/edge_runup.py
    python3 edge/scripts/edge_entry_clock.py
    python3 edge/scripts/edge_search_volume.py
    python3 edge/scripts/edge_calendar.py
    python3 edge/scripts/edge_dashboard.py

Writes edge/analysis/dashboard/{index,runup,entry-clock,search-volume,calendar}.html.

SCOPE, because it has been asked: stage E only. Every input traces to
`research/<date>/edge/`, which is the edge hunt and nothing else -- no stage 0-4
output, no `claude_naive/`, no `backtest/`. The sample opens on 2026-08-31, the
first hunt, and ends at the last run whose event window has closed.

The reading surface is Dutch; the repository is English. That split is the existing
convention here -- see the two artifacts this dashboard links out to.
"""
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANA = REPO / "edge" / "analysis"
OUT = ANA / "dashboard"

# ---------------------------------------------------------------- design tokens
# Palette: cool paper rather than the warm cream default, one deep-teal accent for
# "measured", and the dataviz reference palette's first three categorical slots
# (blue/orange/aqua) which validate all-pairs in BOTH modes. Aqua sits under 3:1 on
# the light surface, so every series is direct-labelled and every chart has a table.
CSS = """
:root{
  --ground:#EDF0F2; --surface:#FFFFFF; --raised:#E3E8EB; --sunk:#F5F7F8;
  --ink:#0F1418; --ink-2:#4B575E; --ink-3:#7E8B93;
  --rule:#D2D9DD; --rule-2:#E5EAED;
  --accent:#0B6E6E; --accent-soft:#DCEDEC; --accent-ink:#095A5A;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a;
  --good:#2E6B4A; --good-soft:#E2EFE7;
  --bad:#A33A3A;  --bad-soft:#F6E5E5;
  --warn:#8A5A1B; --warn-soft:#F6ECDC;
  --grid:#E5EAED;
  --f-d:"Newsreader",Georgia,"Times New Roman",serif;
  --f-b:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  --f-m:"IBM Plex Mono","SFMono-Regular",Consolas,monospace;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --ground:#0E1215; --surface:#161B1F; --raised:#1E252A; --sunk:#12171A;
  --ink:#E9EEF0; --ink-2:#A3AFB6; --ink-3:#77848B;
  --rule:#272F34; --rule-2:#1D2429;
  --accent:#4FB5B0; --accent-soft:#11302F; --accent-ink:#79CFCA;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70;
  --good:#5FA57C; --good-soft:#15291F;
  --bad:#DA6F6F;  --bad-soft:#2B1A1A;
  --warn:#C79350; --warn-soft:#2A2013;
  --grid:#242C31;
}}
:root[data-theme="dark"]{
  --ground:#0E1215; --surface:#161B1F; --raised:#1E252A; --sunk:#12171A;
  --ink:#E9EEF0; --ink-2:#A3AFB6; --ink-3:#77848B;
  --rule:#272F34; --rule-2:#1D2429;
  --accent:#4FB5B0; --accent-soft:#11302F; --accent-ink:#79CFCA;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70;
  --good:#5FA57C; --good-soft:#15291F;
  --bad:#DA6F6F;  --bad-soft:#2B1A1A;
  --warn:#C79350; --warn-soft:#2A2013;
  --grid:#242C31;
}

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
     font-family:var(--f-b);font-size:15.5px;line-height:1.6;
     -webkit-font-smoothing:antialiased}
.wrap{max-width:980px;margin:0 auto;padding-block:40px 80px;padding-left:20px;padding-right:20px;
      display:flex;flex-direction:column;gap:38px}
a{color:var(--accent-ink);text-decoration-thickness:1px;text-underline-offset:2px}

h1,h2,h3{font-family:var(--f-d);font-weight:500;margin:0;text-wrap:balance;letter-spacing:-.01em}
h1{font-size:clamp(29px,4.6vw,42px);line-height:1.12}
h2{font-size:23px;line-height:1.25}
h3{font-size:17px;line-height:1.35}
p{margin:0;max-width:68ch}
.lede{font-size:17.5px;color:var(--ink-2);max-width:66ch}
.lede b,.lede strong{color:var(--ink);font-weight:600}

.eyebrow{font-family:var(--f-m);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
         color:var(--ink-3)}
.mono{font-family:var(--f-m);font-variant-numeric:tabular-nums}
code{font-family:var(--f-m);font-size:.87em;background:var(--raised);padding:1px 5px;
     border-radius:3px;color:var(--ink-2)}

header.top{display:flex;flex-direction:column;gap:14px;padding-bottom:24px;
           border-bottom:2px solid var(--ink)}
nav.crumbs{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13.5px;align-items:baseline}
nav.crumbs .sep{color:var(--ink-3)}

section{display:flex;flex-direction:column;gap:14px}
section > .sub{color:var(--ink-3);font-size:13.5px;max-width:72ch;margin-top:-6px}

/* the sample band: every number on every page rests on it */
.facts{display:flex;flex-wrap:wrap;gap:1px;background:var(--rule);
       border:1px solid var(--rule);border-radius:4px;overflow:hidden}
.fact{flex:1 1 130px;background:var(--surface);padding:13px 16px}
.fact b{display:block;font-family:var(--f-m);font-size:22px;font-weight:500;
        font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.2}
.fact span{display:block;font-size:12.5px;color:var(--ink-3);margin-top:3px}

/* verdict chips — the register's own vocabulary, not decoration */
.chip{display:inline-block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.07em;
      text-transform:uppercase;padding:2.5px 8px;border-radius:3px;white-space:nowrap;
      border:1px solid currentColor;vertical-align:2px}
.c-null{background:var(--warn-soft);color:var(--warn)}
.c-open{background:var(--accent-soft);color:var(--accent-ink)}
.c-lead{background:var(--good-soft);color:var(--good)}
.c-done{background:var(--raised);color:var(--ink-3)}
.c-plan{background:var(--sunk);color:var(--ink-3)}

/* the question ledger: rows, not cards. Each row is a register entry. */
.ledger{display:flex;flex-direction:column}
.q{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 22px;
   padding:22px 0;border-top:1px solid var(--rule)}
.q:last-child{border-bottom:1px solid var(--rule)}
.q .qh{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.q .qh h2{font-size:20px}
.q .ans{color:var(--ink-2);font-size:15px;max-width:64ch}
.q .stat{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:0;margin-top:4px;
         border-left:2px solid var(--accent);padding-left:14px}
.q .stat .n{font-family:var(--f-m);font-variant-numeric:tabular-nums;font-size:14px;
            color:var(--ink);padding-right:20px}
.q .stat .n em{font-style:normal;color:var(--ink-3);font-size:12.5px;display:block;
               letter-spacing:.04em;text-transform:uppercase;font-family:var(--f-m)}
.q .go{grid-row:1;grid-column:2;align-self:start;font-size:13.5px;white-space:nowrap}

.tbl{overflow-x:auto;border:1px solid var(--rule);border-radius:4px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:13.5px;font-variant-numeric:tabular-nums}
th,td{padding:7px 12px;text-align:right;border-bottom:1px solid var(--rule-2);white-space:nowrap}
th:first-child,td:first-child{text-align:left}
thead th{font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;
         color:var(--ink-3);font-weight:400;border-bottom:1px solid var(--rule);
         position:sticky;top:0;background:var(--surface)}
tbody tr:last-child td{border-bottom:0}
td.num,th.num{font-family:var(--f-m)}
tr.hl td{background:var(--accent-soft)}
.pos{color:var(--good)} .neg{color:var(--bad)} .dim{color:var(--ink-3)}
table.prose td:nth-child(2){white-space:normal;min-width:30ch}
table.prose td:first-child{white-space:normal}

.note{border-left:3px solid var(--warn);background:var(--surface);padding:14px 18px;
      border-radius:0 4px 4px 0;display:flex;flex-direction:column;gap:7px}
.note .lbl{font-family:var(--f-m);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
           color:var(--warn)}
.note p{max-width:none;font-size:14.5px}
.note.acc{border-left-color:var(--accent)} .note.acc .lbl{color:var(--accent-ink)}

figure{margin:0;display:flex;flex-direction:column;gap:9px}
figcaption{font-size:13px;color:var(--ink-3);max-width:72ch}
.chart{background:var(--surface);border:1px solid var(--rule);border-radius:4px;
       padding:14px 12px 8px;position:relative}
.chart svg{display:block;width:100%;height:auto;overflow:visible}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:13px;color:var(--ink-2);
        padding:2px 4px 6px}
.legend i{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;
          vertical-align:-1px}
.tip{position:absolute;pointer-events:none;opacity:0;transition:opacity .08s;
     background:var(--ink);color:var(--ground);font-family:var(--f-m);font-size:11.5px;
     line-height:1.45;padding:7px 9px;border-radius:4px;white-space:pre;z-index:5;
     transform:translate(-50%,-115%)}
details{background:var(--surface);border:1px solid var(--rule);border-radius:4px;
        padding:10px 14px}
details[open]{padding-bottom:14px}
summary{cursor:pointer;font-size:13.5px;color:var(--ink-2);font-family:var(--f-m)}
summary:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

footer{border-top:1px solid var(--rule);padding-top:18px;color:var(--ink-3);font-size:13px;
       display:flex;flex-direction:column;gap:10px}
footer p{max-width:74ch}

@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
@media (max-width:620px){
  .q{grid-template-columns:minmax(0,1fr)}
  .q .go{grid-row:auto;grid-column:1}
}
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Newsreader:opsz,wght@6..72,400;6..72,500&'
         'family=IBM+Plex+Sans:wght@400;500;600&'
         'family=IBM+Plex+Mono:wght@400;500&display=swap">')

TIP_JS = """
<script>
(function(){
  document.querySelectorAll('.chart').forEach(function(box){
    var tip = box.querySelector('.tip'); if(!tip) return;
    box.querySelectorAll('[data-tip]').forEach(function(el){
      function show(e){
        var r = box.getBoundingClientRect();
        var b = el.getBoundingClientRect();
        tip.textContent = el.getAttribute('data-tip');
        tip.style.left = (b.left + b.width/2 - r.left) + 'px';
        tip.style.top  = (b.top - r.top) + 'px';
        tip.style.opacity = 1;
      }
      el.addEventListener('mouseenter', show);
      el.addEventListener('focus', show);
      el.addEventListener('mouseleave', function(){ tip.style.opacity = 0; });
      el.addEventListener('blur', function(){ tip.style.opacity = 0; });
    });
  });
})();
</script>
"""


def esc(s):
    return html.escape(str(s if s is not None else ""))


def page(title, body, desc=""):
    return (f"<title>{esc(title)}</title>\n{FONTS}\n<style>{CSS}</style>\n"
            f"<div class=\"wrap\">\n{body}\n</div>\n{TIP_JS}")


def crumbs(here):
    items = [("index.html", "Overzicht"), ("runup.html", "Aanloop"),
             ("entry-clock.html", "Instapmoment"), ("search-volume.html", "Zoekvolume"),
             ("calendar.html", "Agenda")]
    out = []
    for href, label in items:
        out.append(f"<b>{esc(label)}</b>" if href == here
                   else f'<a href="{href}">{esc(label)}</a>')
    return ('<nav class="crumbs">' + '<span class="sep">/</span>'.join(out) + '</nav>')


def foot(generated, extra=""):
    return (f"""<footer>
{extra}
<p>Gegenereerd uit <code>edge/analysis/*.json</code> door
<code>edge/scripts/edge_dashboard.py</code> op {esc(generated)}. Elk getal op deze
pagina's komt uit het script dat de meting deed; deze pagina's worden nooit met de
hand bijgewerkt.</p>
<p>Bron is uitsluitend de edge hunt (stage E), <code>research/&lt;datum&gt;/edge/</code>,
vanaf de eerste run op 31 augustus 2026. Geen resultaten van stage 0 tot 4, niet van
<code>claude_naive/</code>, niet van <code>backtest/</code>.</p>
<p>Dit is een voorspelexercitie op openbare informatie. Het is geen beleggingsadvies.
Rendementen zijn brutobedragen zonder transactiekosten, spread, slippage of leenkosten,
op een boek waarvan een groot deel uit shorts bestaat in namen die per dag weinig
omzetten.</p>
</footer>""")


# ------------------------------------------------------------------ chart helpers
def fmt(x, d=2, sign=True):
    if x is None:
        return "–"
    try:
        f = float(x)
    except (TypeError, ValueError):
        return esc(x)
    if f != f:                                   # NaN
        return "–"
    return f"{f:+.{d}f}" if sign else f"{f:.{d}f}"


def cls(x):
    if x is None:
        return "dim"
    try:
        return "pos" if float(x) > 0 else ("neg" if float(x) < 0 else "dim")
    except (TypeError, ValueError):
        return "dim"


def line_chart(series, xlabels, ylab, mark_index=None, w=880, h=300,
               pad=(16, 104, 34, 52)):   # right pad holds the direct labels
    """series: [{name, color, pts:[y|None], tips:[str]}]. One y-scale, always."""
    pt, pr, pb, pl = pad
    iw, ih = w - pl - pr, h - pt - pb
    vals = [v for s in series for v in s["pts"] if v is not None]
    if not vals:
        return "<p class='dim'>geen data</p>"
    lo, hi = min(vals), max(vals)
    if hi == lo:
        hi, lo = hi + 1, lo - 1
    span = hi - lo
    lo, hi = lo - span * 0.14, hi + span * 0.14
    n = len(xlabels)

    def X(i):
        return pl + (iw * i / max(1, n - 1))

    def Y(v):
        return pt + ih * (hi - v) / (hi - lo)

    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(ylab)}">']
    # y grid + ticks, every label naming a value the chart reaches
    steps = 5
    for k in range(steps + 1):
        v = lo + (hi - lo) * k / steps
        y = Y(v)
        o.append(f'<line x1="{pl}" y1="{y:.1f}" x2="{pl+iw}" y2="{y:.1f}" '
                 f'stroke="var(--grid)" stroke-width="1"/>')
        o.append(f'<text x="{pl-9}" y="{y+4:.1f}" text-anchor="end" font-size="11" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">{v:+.1f}</text>')
    # zero line, if it is inside the range
    if lo < 0 < hi:
        o.append(f'<line x1="{pl}" y1="{Y(0):.1f}" x2="{pl+iw}" y2="{Y(0):.1f}" '
                 f'stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="3 3"/>')
    # the anchor rule
    if mark_index is not None:
        x = X(mark_index)
        o.append(f'<line x1="{x:.1f}" y1="{pt}" x2="{x:.1f}" y2="{pt+ih}" '
                 f'stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"/>')
        o.append(f'<text x="{x:.1f}" y="{pt-3}" text-anchor="middle" font-size="10.5" '
                 f'fill="var(--accent)" font-family="var(--f-m)" '
                 f'letter-spacing="0.06em">20:00 CET</text>')
    # x ticks, thinned so they never collide
    every = max(1, -(-n // 7))            # at most 7 ticks, so they never collide
    for i, lb in enumerate(xlabels):
        if i % every and i != n - 1:
            continue
        o.append(f'<text x="{X(i):.1f}" y="{pt+ih+18}" text-anchor="middle" font-size="11" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">{esc(lb)}</text>')
    o.append(f'<text x="{pl-9}" y="{pt-6}" text-anchor="end" font-size="10.5" '
             f'fill="var(--ink-3)" font-family="var(--f-m)">%</text>')
    # series
    for s in series:
        d = []
        for i, v in enumerate(s["pts"]):
            if v is None:
                continue
            d.append(("M" if not d else "L") + f"{X(i):.1f},{Y(v):.1f}")
        if d:
            o.append(f'<path d="{" ".join(d)}" fill="none" stroke="{s["color"]}" '
                     f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(s["pts"]):
            if v is None:
                continue
            tip = s["tips"][i] if i < len(s["tips"]) else ""
            o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4.5" fill="{s["color"]}" '
                     f'stroke="var(--surface)" stroke-width="2" tabindex="0" '
                     f'data-tip="{esc(tip)}"><title>{esc(tip)}</title></circle>')
        # direct label at the last point: identity is never colour alone
        last = max((i for i, v in enumerate(s["pts"]) if v is not None), default=None)
        if last is not None:
            o.append(f'<text x="{X(last)+9:.1f}" y="{Y(s["pts"][last])+4:.1f}" font-size="11.5" '
                     f'fill="{s["color"]}" font-family="var(--f-m)">{esc(s["name"])}</text>')
    o.append("</svg>")
    return "".join(o)


def bar_pairs(groups, w=880, h=300, pad=(16, 16, 46, 52)):
    """groups: [{label, bars:[{name,color,v,lo,hi,tip}]}] — grouped bars with CI whiskers."""
    pt, pr, pb, pl = pad
    iw, ih = w - pl - pr, h - pt - pb
    vals = [b["v"] for g in groups for b in g["bars"]]
    vals += [b["lo"] for g in groups for b in g["bars"] if b.get("lo") is not None]
    vals += [b["hi"] for g in groups for b in g["bars"] if b.get("hi") is not None]
    vals = [v for v in vals if v is not None and v == v]
    if not vals:
        return "<p class='dim'>geen data</p>"
    lo, hi = min(min(vals), 0), max(max(vals), 0)
    span = (hi - lo) or 1
    lo, hi = lo - span * 0.1, hi + span * 0.1

    def Y(v):
        return pt + ih * (hi - v) / (hi - lo)

    gw = iw / len(groups)
    o = [f'<svg viewBox="0 0 {w} {h}" role="img">']
    for k in range(5 + 1):
        v = lo + (hi - lo) * k / 5
        o.append(f'<line x1="{pl}" y1="{Y(v):.1f}" x2="{pl+iw}" y2="{Y(v):.1f}" '
                 f'stroke="var(--grid)"/>')
        o.append(f'<text x="{pl-9}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="11" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">{v:+.1f}</text>')
    o.append(f'<line x1="{pl}" y1="{Y(0):.1f}" x2="{pl+iw}" y2="{Y(0):.1f}" '
             f'stroke="var(--ink-3)" stroke-width="1"/>')
    for gi, g in enumerate(groups):
        nb = len(g["bars"])
        bw = min(34, (gw - 22) / nb - 4)
        x0 = pl + gw * gi + (gw - (bw + 4) * nb) / 2
        for bi, b in enumerate(g["bars"]):
            x = x0 + bi * (bw + 4)
            y0, y1 = Y(0), Y(b["v"])
            top, hgt = min(y0, y1), abs(y1 - y0)
            o.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{bw:.1f}" '
                     f'height="{max(hgt,1.5):.1f}" fill="{b["color"]}" rx="3" '
                     f'tabindex="0" data-tip="{esc(b.get("tip",""))}">'
                     f'<title>{esc(b.get("tip",""))}</title></rect>')
            if b.get("lo") is not None and b.get("hi") is not None and b["lo"] == b["lo"]:
                cx = x + bw / 2
                o.append(f'<line x1="{cx:.1f}" y1="{Y(b["lo"]):.1f}" x2="{cx:.1f}" '
                         f'y2="{Y(b["hi"]):.1f}" stroke="var(--ink-2)" stroke-width="1.5"/>')
                for yy in (b["lo"], b["hi"]):
                    o.append(f'<line x1="{cx-4:.1f}" y1="{Y(yy):.1f}" x2="{cx+4:.1f}" '
                             f'y2="{Y(yy):.1f}" stroke="var(--ink-2)" stroke-width="1.5"/>')
        o.append(f'<text x="{pl+gw*gi+gw/2:.1f}" y="{pt+ih+20}" text-anchor="middle" '
                 f'font-size="11.5" fill="var(--ink-2)" font-family="var(--f-m)">'
                 f'{esc(g["label"])}</text>')
    o.append("</svg>")
    return "".join(o)


def legend(items):
    return ('<div class="legend">' + "".join(
        f'<span><i style="background:{c}"></i>{esc(n)}</span>' for n, c in items)
        + '</div>')


def load(name):
    p = ANA / name
    if not p.exists():
        return None
    return json.loads(p.read_text())


# =============================================================================
# PAGES
# =============================================================================
WINDOWS = ["2d", "5d", "10d", "20d"]
FLOORKEY = "conviction >= 3.0"


def pct(x, d=2):
    return "–" if x is None or x != x else f"{x:+.{d}f}%"


def ci(s):
    lo, hi = s.get("ci_lo"), s.get("ci_hi")
    if lo is None or lo != lo:
        return "–"
    return f"[{lo:+.2f}, {hi:+.2f}]"


# ------------------------------------------------------------------- run-up page
def build_runup(d, gen):
    n, nd, nf = d["n_events"], d["n_days"], d["n_above_floor"]
    w = d["windows"]
    best_p = min((v["p_signed"] for v in w.values()), default=1)
    ag_all = d["agreement"]["all names"]
    ag_fl = d["agreement"][FLOORKEY]

    rows_q1 = "".join(
        f"<tr><td>{k}</td><td class='num'>{v['n']}</td>"
        f"<td class='num'>{v['rho_signed']:+.3f}</td><td class='num dim'>{v['p_signed']:.3f}</td>"
        f"<td class='num'>{v['rho_abs']:+.3f}</td><td class='num dim'>{v['p_abs']:.3f}</td>"
        + "".join(f"<td class='num'>{x*100:.0f}%</td>" for x in v["tercile_hit_rates"])
        + "</tr>" for k, v in w.items())

    groups = []
    for k in WINDOWS:
        a, b = ag_fl[k]["agree"], ag_fl[k]["disagree"]
        groups.append({"label": k, "bars": [
            {"name": "eens", "color": "var(--s1)", "v": a["mean"],
             "lo": a.get("ci_lo"), "hi": a.get("ci_hi"),
             "tip": f"{k} · aanloop EENS met voorspelling\nn={a['n']}  raak {a['hits']}/{a['n']}\n"
                    f"gemiddeld {a['mean']:+.2f}%  t={a['t']:.2f}\n95%-BI {ci(a)}"},
            {"name": "oneens", "color": "var(--s2)", "v": b["mean"],
             "lo": b.get("ci_lo"), "hi": b.get("ci_hi"),
             "tip": f"{k} · aanloop ONEENS met voorspelling\nn={b['n']}  raak {b['hits']}/{b['n']}\n"
                    f"gemiddeld {b['mean']:+.2f}%  t={b['t']:.2f}\n95%-BI {ci(b)}"}]})

    rows_q2 = ""
    for pool, tag in ((ag_all, "alle namen"), (ag_fl, f"conviction &ge; {d['floor']}")):
        rows_q2 += f"<tr class='hl'><td colspan='8'><b>{tag}</b></td></tr>"
        for k in WINDOWS:
            a, b = pool[k]["agree"], pool[k]["disagree"]
            rows_q2 += (
                f"<tr><td>{k} aanloop</td>"
                f"<td class='num'>{a['hits']}/{a['n']}</td>"
                f"<td class='num {cls(a['mean'])}'>{a['mean']:+.2f}%</td>"
                f"<td class='num dim'>{ci(a)}</td>"
                f"<td class='num'>{b['hits']}/{b['n']}</td>"
                f"<td class='num {cls(b['mean'])}'>{b['mean']:+.2f}%</td>"
                f"<td class='num dim'>{ci(b)}</td>"
                f"<td class='num {cls(pool[k]['gap'])}'>{pool[k]['gap']:+.2f}pp</td></tr>")

    bk = d["books"]
    rows_ctl = "".join(
        f"<tr><td>{lbl}</td><td class='num'>{bk[k]['hits']}/{bk[k]['n']}</td>"
        f"<td class='num'>{bk[k]['hit_rate']*100:.0f}%</td>"
        f"<td class='num {cls(bk[k]['mean'])}'>{bk[k]['mean']:+.2f}%</td>"
        f"<td class='num dim'>{bk[k]['t']:.2f}</td></tr>"
        for k, lbl in (("hunt_above_floor", "de hunt, boven de floor"),
                       ("hunt_all", "de hunt, alle namen"),
                       ("short_all", "alles shorten, geen onderzoek"),
                       ("minus_runup_20d", "min de 20-daagse aanloop"),
                       ("minus_runup_10d", "min de 10-daagse aanloop"))
        if k in bk)

    body = f"""
<header class="top">
  <span class="eyebrow">stage E &middot; onderzoeksvraag 1 en 2</span>
  {crumbs("runup.html")}
  <h1>Zegt de aanloop iets over de voorspelling?</h1>
  <p class="lede">Twee vragen over hetzelfde getal. Voorspelt het rendement van de
  2, 5, 10 en 20 sessies vóór de instap of de <b>richting</b> van de hunt klopte? En
  levert het meer op als die aanloop <b>dezelfde kant op wijst</b> als de voorspelling?
  Op {n} events over {nd} dagen is het antwoord op de eerste vraag nee, en op de tweede
  nee op precies het boek dat wordt verhandeld.</p>
  <div class="facts">
    <div class="fact"><b>{n}</b><span>afgerekende events</span></div>
    <div class="fact"><b>{nd}</b><span>hunt-dagen</span></div>
    <div class="fact"><b>{nf}</b><span>boven de floor van {d['floor']}</span></div>
    <div class="fact"><b class="mono">{best_p:.2f}</b><span>laagste p, vraag 1</span></div>
  </div>
</header>

<section>
  <h2>Meten tot 20:00 CET, niet tot de slotkoers</h2>
  <p>Elke aanloop eindigt op de 14:00 ET-balk van de instapdag &mdash; 20:00 CET, het
  moment waarop het boek wordt geplaatst. Doorrekenen tot de close zou twee uur koers
  in een voorspeller stoppen die op het beslismoment bekend hoort te zijn. Bij een
  <code>bmo</code>-print is de instapdag de sessie <em>vóór</em> de eventdatum, want
  dat is de laatste waarop je kunt handelen; bij <code>amc</code> is het de eventdag zelf.</p>
</section>

<section>
  <h2>Vraag 1 &mdash; voorspelt de aanloop of het teken klopte?</h2>
  <p class="sub">Raak is <code>sign(impact_sum) == sign(gerealiseerde beweging)</code>.
  De eerste rho zet de aanloop af tegen die 0/1-uitkomst, de tweede de absolute aanloop.
  p-waarden zijn permutatie-p's.</p>
  <div class="tbl"><table>
    <thead><tr><th>venster</th><th class="num">n</th><th class="num">rho aanloop</th>
    <th class="num">p</th><th class="num">rho |aanloop|</th><th class="num">p</th>
    <th class="num">raak laag</th><th class="num">midden</th><th class="num">hoog</th></tr></thead>
    <tbody>{rows_q1}</tbody>
  </table></div>
  <div class="note"><span class="lbl">wat hier staat</span>
  <p>Geen enkele rho komt boven 0,16 uit en geen enkele p onder 0,11. De trefkans per
  aanlooptercile blijft in een band van 49% tot 57% &mdash; vlak, en niet monotoon. Dit
  is geen zwak signaal dat meer dagen nodig heeft; het is de vorm van niets.</p></div>
</section>

<section>
  <h2>Vraag 2 &mdash; helpt het als de aanloop dezelfde kant op wijst?</h2>
  <p class="sub">Eens is <code>sign(aanloop) == sign(impact_sum)</code>. Het boek is
  gelijkgewogen, getekend door de voorspelling, ingestapt om 20:00 CET en verkocht op de
  volgende slotkoers. Staven zijn het gemiddelde rendement per trade; de sprieten zijn
  een 95%-betrouwbaarheidsinterval uit een bootstrap over <em>dagen</em>, niet over events.</p>
  <figure>
    <div class="chart">
      {legend([("aanloop eens met de voorspelling", "var(--s1)"),
               ("aanloop oneens", "var(--s2)")])}
      {bar_pairs(groups)}
      <div class="tip"></div>
    </div>
    <figcaption>Het verhandelde boek: de {nf} namen boven de conviction floor van
    {d['floor']}. Bij elk venster ligt de <em>oneens</em>-staaf hoger. Elk interval
    overlapt nul en elkaar.</figcaption>
  </figure>
  <div class="tbl"><table>
    <thead><tr><th>venster</th><th class="num">eens raak</th><th class="num">eens</th>
    <th class="num">95%-BI</th><th class="num">oneens raak</th><th class="num">oneens</th>
    <th class="num">95%-BI</th><th class="num">verschil</th></tr></thead>
    <tbody>{rows_q2}</tbody>
  </table></div>
  <div class="note"><span class="lbl">de twee pools wijzen tegengesteld, en dat is het antwoord</span>
  <p>Over <b>alle</b> namen lijkt eens-zijn te helpen: de 2-daagse aanloop geeft
  {pct(ag_all['2d']['agree']['mean'])} tegen {pct(ag_all['2d']['disagree']['mean'])}.
  Over het <b>verhandelde</b> boek draait het om, bij alle vier de vensters: 10 dagen
  geeft {pct(ag_fl['10d']['agree']['mean'])} als de aanloop meebeweegt tegen
  {pct(ag_fl['10d']['disagree']['mean'])} als hij tegenbeweegt.</p>
  <p>Twee deelverzamelingen van dezelfde data die tegengesteld wijzen, met intervallen
  die elkaar volledig overlappen, zijn geen twee bevindingen. Het is ruis die twee keer
  is gemeten. Er zijn hier vier vensters, twee pools en twee uitgangen bekeken; bij
  zestien cellen hoort een p van 0,05 er ongeveer één keer bij te zitten.</p></div>
</section>

<section>
  <h2>Waar dit tegen afgezet hoort te worden</h2>
  <p class="sub">Dezelfde events, dezelfde instap. Alles shorten kost geen onderzoek.</p>
  <div class="tbl"><table>
    <thead><tr><th>regel</th><th class="num">raak</th><th class="num">trefkans</th>
    <th class="num">per trade</th><th class="num">t</th></tr></thead>
    <tbody>{rows_ctl}</tbody>
  </table></div>
  <p>Op deze {n} events verdient de hunt boven de floor
  {pct(bk['hunt_above_floor']['mean'])} per trade tegen {pct(bk['short_all']['mean'])}
  voor alles shorten zonder enig onderzoek. Dat is een echt verschil en het is de reden
  dat de floor blijft staan. Maar <code>min de 20-daagse aanloop</code> &mdash; de
  gratis controle die in <code>edge/EDGE_ANALYSIS.md</code> de hunt op elke eerdere
  steekproef versloeg &mdash; doet het hier met {pct(bk['minus_runup_20d']['mean'])}
  juist slecht. Ook die controle is dus niet stabiel over deze grotere steekproef.</p>
</section>

{foot(gen)}
"""
    return page("Aanloop en trefkans", body)


# -------------------------------------------------------------- entry clock page
def build_entry(d, gen):
    grid = [k for k in d["all_close"].keys()]
    labels = [d["all_close"][k]["label"].split(" / ")[1] for k in grid]
    anchor = grid.index("1400")

    def ser(tag, name, color):
        pts, tips = [], []
        for k in grid:
            v = d.get(tag, {}).get(k)
            pts.append(v["mean"] if v else None)
            tips.append("" if not v else
                        f"{name}\n{v['label']}\nn={v['n']}  raak {v['hits']}/{v['n']}\n"
                        f"gemiddeld {v['mean']:+.2f}%  t={v['t']:.2f}\n"
                        f"95%-BI [{v['ci'][0]:+.2f}, {v['ci'][1]:+.2f}]")
        return {"name": name, "color": color, "pts": pts, "tips": tips}

    fl = d["floor_close"]
    sp = d["floor_close_spread"]
    a14 = fl["1400"]

    rows = "".join(
        f"<tr{' class=hl' if k == '1400' else ''}><td>{d['all_close'][k]['label']}</td>"
        f"<td class='num'>{d['all_close'][k]['n']}</td>"
        f"<td class='num {cls(d['all_close'][k]['mean'])}'>{d['all_close'][k]['mean']:+.2f}%</td>"
        f"<td class='num'>{fl[k]['hits']}/{fl[k]['n']}</td>"
        f"<td class='num {cls(fl[k]['mean'])}'>{fl[k]['mean']:+.2f}%</td>"
        f"<td class='num dim'>{fl[k]['t']:.2f}</td>"
        f"<td class='num dim'>[{fl[k]['ci'][0]:+.2f}, {fl[k]['ci'][1]:+.2f}]</td>"
        f"<td class='num {cls(d['amc_close'][k]['mean']) if k in d.get('amc_close',{}) else 'dim'}'>"
        f"{fmt(d.get('amc_close',{}).get(k,{}).get('mean'))}%</td>"
        f"<td class='num {cls(d['bmo_close'][k]['mean']) if k in d.get('bmo_close',{}) else 'dim'}'>"
        f"{fmt(d.get('bmo_close',{}).get(k,{}).get('mean'))}%</td></tr>"
        for k in grid)

    dr = d.get("drift_to_close", {})
    rows_dr = "".join(
        f"<tr><td>{d['all_close'][k]['label']}</td><td class='num'>{v['n']}</td>"
        f"<td class='num {cls(v['mean'])}'>{v['mean']:+.3f}%</td>"
        f"<td class='num dim'>{v['t']:.2f}</td></tr>" for k, v in dr.items())

    amc_sp, bmo_sp = d["amc_close_spread"], d["bmo_close_spread"]

    body = f"""
<header class="top">
  <span class="eyebrow">stage E &middot; onderzoeksvraag 3</span>
  {crumbs("entry-clock.html")}
  <h1>Is 20:00 CET het juiste instapmoment?</h1>
  <p class="lede">De uitgang is vastgezet en alleen de <b>ingang</b> schuift, van 16:00
  tot 22:00 CET in stappen van een half uur. Elk verschil tussen twee rijen is dus
  instapmoment en niets anders. Over het verhandelde boek is de spreiding over de hele
  sessie <b>{sp['spread']:.2f} procentpunt</b> &mdash; op een rendement van
  {a14['mean']:+.2f}% en een standaardafwijking van {a14['sd']:.0f}. Het maakt niet uit.</p>
  <div class="facts">
    <div class="fact"><b>{d['n_events']}</b><span>afgerekende events</span></div>
    <div class="fact"><b class="mono">{a14['mean']:+.2f}%</b><span>om 20:00 CET, boven de floor</span></div>
    <div class="fact"><b class="mono">{sp['spread']:.2f}pp</b><span>spreiding over 6 uur</span></div>
    <div class="fact"><b class="mono">{a14['sd']:.0f}</b><span>sd per trade</span></div>
  </div>
</header>

<section>
  <h2>Waarom het raster bij de slotkoers stopt</h2>
  <p>Bij een <code>amc</code>-naam valt de print ná 16:00 ET, dus de slotkoers is de
  laatste verhandelbare minuut en &ldquo;later&rdquo; bestaat niet meer. Bij een
  <code>bmo</code>-naam valt de print vóór de volgende open, dus de slotkoers van de
  instapdag is opnieuw het laatste liquide moment: de nabeurs daartussen draagt in deze
  bron geen volume. &ldquo;Later&rdquo; betekent hier dus later in dezelfde sessie. Het
  raster begint om 16:00 CET omdat de vraag pas iets betekent naast haar spiegelbeeld:
  als vroeger meer oplevert, is het antwoord dat de run eerder klaar moet zijn.</p>
</section>

<section>
  <h2>Rendement per instapmoment</h2>
  <p class="sub">Gemiddeld rendement per trade, uitgang op de volgende slotkoers.
  De stippellijn is 20:00 CET, het moment waarop stage E nu koopt.</p>
  <figure>
    <div class="chart">
      {legend([("boven de conviction floor", "var(--s1)"),
               ("alle namen", "var(--s2)")])}
      {line_chart([ser("floor_close", "boven de floor", "var(--s1)"),
                   ser("all_close", "alle namen", "var(--s2)")],
                  labels, "rendement per trade", mark_index=anchor)}
      <div class="tip"></div>
    </div>
    <figcaption>Beide lijnen lopen vlak. De beste en slechtste instap van de dag
    schelen {sp['spread']:.2f}pp op het verhandelde boek, tegen een standaardafwijking
    van {a14['sd']:.0f} punten per trade.</figcaption>
  </figure>
  <div class="tbl"><table>
    <thead><tr><th>instap</th><th class="num">n</th><th class="num">alle namen</th>
    <th class="num">raak</th><th class="num">boven floor</th><th class="num">t</th>
    <th class="num">95%-BI</th><th class="num">amc</th><th class="num">bmo</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</section>

<section>
  <h2>De twee sessies willen tegengestelde dingen &mdash; zwak</h2>
  <p><code>amc</code>-namen betalen het meest als je <em>vroeg</em> instapt
  ({amc_sp['best_mean']:+.2f}% om {amc_sp['best'][:2]}:{amc_sp['best'][2:]} ET tegen
  {amc_sp['worst_mean']:+.2f}% om {amc_sp['worst'][:2]}:{amc_sp['worst'][2:]} ET),
  <code>bmo</code>-namen juist als je <em>laat</em> instapt
  ({bmo_sp['best_mean']:+.2f}% om {bmo_sp['best'][:2]}:{bmo_sp['best'][2:]} ET tegen
  {bmo_sp['worst_mean']:+.2f}% om {bmo_sp['worst'][:2]}:{bmo_sp['worst'][2:]} ET).
  Dat is dezelfde vorm als de uitgangsbevinding in <code>edge/EDGE_ANALYSIS.md</code>,
  wat het plausibel maakt.</p>
  <div class="note"><span class="lbl">niet naar handelen</span>
  <p>Het gaat om 28 en 27 events. De spreidingen van 1,65 en 1,42 procentpunt zijn
  kleiner dan de standaardfout van elke afzonderlijke cel, en het beste uur is gekozen
  ná het lezen van deze grafiek. Een splitsing die op beide sessies de andere kant op
  wijst is precies wat ruis doet als je hem in tweeën snijdt.</p></div>
</section>

<section>
  <h2>Wat het wachten kost vóór er een voorspelling op zit</h2>
  <p class="sub">Gemiddeld ongetekend rendement van elk instapmoment naar de slotkoers
  van diezelfde dag. Als dit niet vlak is, heeft de sessie een drift die het boek hoe dan
  ook oppikt.</p>
  <div class="tbl"><table>
    <thead><tr><th>instap</th><th class="num">n</th><th class="num">drift naar de close</th>
    <th class="num">t</th></tr></thead>
    <tbody>{rows_dr}</tbody>
  </table></div>
  <p>Geen enkele t komt boven 1,6. Er is geen intradagdrift in deze namen om op te
  timen, wat verklaart waarom de bovenste grafiek vlak is: er valt niets te winnen
  omdat er niets systematisch beweegt tussen 16:00 en 22:00 CET.</p>
</section>

<section>
  <h2>Wat hier niet in zit</h2>
  <p>De spread. Elke koers hierboven is een slotkoers van een 15-minutenbalk, niet een
  prijs waartegen dit boek daadwerkelijk zou zijn gevuld. Op 2026-09-17 mat het
  handelsscript bij TRT een halve spread van 14,6%. In namen als die overheerst de
  spread elk verschil van 0,4 procentpunt dat hier staat, en die spread is niet constant
  over de sessie &mdash; hij is het breedst rond de open en het smalst tegen de close.
  Dat is het enige argument in deze analyse dat vóór later instappen pleit, en het is
  niet gemeten.</p>
</section>

{foot(gen)}
"""
    return page("Het instapmoment", body)


# ------------------------------------------------------------ search volume page
def scatter(rows, xk, yk, xlab, ylab, w=880, h=340, pad=(18, 22, 44, 56)):
    pt, pr, pb, pl = pad
    iw, ih = w - pl - pr, h - pt - pb
    xs = [r[xk] for r in rows]
    ys = [r[yk] for r in rows]
    if not xs:
        return "<p class='dim'>geen data</p>"
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    xsp, ysp = (x1 - x0) or 1, (y1 - y0) or 1
    x0, x1 = x0 - xsp * .08, x1 + xsp * .08
    y0, y1 = y0 - ysp * .08, y1 + ysp * .08

    def X(v):
        return pl + iw * (v - x0) / (x1 - x0)

    def Y(v):
        return pt + ih * (y1 - v) / (y1 - y0)

    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(ylab)} tegen {esc(xlab)}">']
    for k in range(6):
        v = y0 + (y1 - y0) * k / 5
        o.append(f'<line x1="{pl}" y1="{Y(v):.1f}" x2="{pl+iw}" y2="{Y(v):.1f}" stroke="var(--grid)"/>')
        o.append(f'<text x="{pl-9}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="11" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">{v:+.0f}</text>')
    for k in range(6):
        v = x0 + (x1 - x0) * k / 5
        o.append(f'<text x="{X(v):.1f}" y="{pt+ih+18}" text-anchor="middle" font-size="11" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">{v:.1f}&#215;</text>')
    if y0 < 0 < y1:
        o.append(f'<line x1="{pl}" y1="{Y(0):.1f}" x2="{pl+iw}" y2="{Y(0):.1f}" '
                 f'stroke="var(--ink-3)" stroke-dasharray="3 3"/>')
    if x0 < 1 < x1:
        o.append(f'<line x1="{X(1):.1f}" y1="{pt}" x2="{X(1):.1f}" y2="{pt+ih}" '
                 f'stroke="var(--ink-3)" stroke-dasharray="3 3"/>')
        o.append(f'<text x="{X(1):.1f}" y="{pt-5}" text-anchor="middle" font-size="10.5" '
                 f'fill="var(--ink-3)" font-family="var(--f-m)">normaal</text>')
    for r in rows:
        above = abs(r["impact_sum"] or 0) >= 3
        c = "var(--s1)" if above else "var(--s2)"
        o.append(f'<circle cx="{X(r[xk]):.1f}" cy="{Y(r[yk]):.1f}" r="5.5" fill="{c}" '
                 f'fill-opacity="{0.95 if above else 0.55}" stroke="var(--surface)" '
                 f'stroke-width="1.5" tabindex="0" data-tip="'
                 f'{esc(r["ticker"])} · {esc(r.get("company") or "")}\n'
                 f'zoekpiek {r[xk]:.2f}× · impact_sum {r["impact_sum"]:+.2f}\n'
                 f'trade {r[yk]:+.2f}% · omzet ${r["dollar_vol"]/1e6:.1f}m">'
                 f'<title>{esc(r["ticker"])}: piek {r[xk]:.2f}x, trade {r[yk]:+.2f}%</title></circle>')
    o.append(f'<text x="{pl-9}" y="{pt-6}" text-anchor="end" font-size="10.5" '
             f'fill="var(--ink-3)" font-family="var(--f-m)">%</text>')
    o.append(f'<text x="{pl+iw/2:.0f}" y="{h-6}" text-anchor="middle" font-size="11.5" '
             f'fill="var(--ink-3)" font-family="var(--f-m)">{esc(xlab)}</text>')
    o.append("</svg>")
    return "".join(o)


def build_search(d, gen):
    co_all = d["correlations"]["all measured"]
    co_fl = d["correlations"][FLOORKEY]
    rows = [r for r in d["rows"] if r.get("spike_day") is not None
            and r.get("trade_close") is not None]
    n_sparse = sum(1 for s in d["silent"] if s.get("unusable") == "sparse")
    n_sil = len(d["silent"]) - n_sparse
    sel = d.get("threshold_selection", {})

    rows_co = ""
    for tag, co in (("alle meetbare namen", co_all), (f"conviction &ge; {d['floor']}", co_fl)):
        rows_co += f"<tr class='hl'><td colspan='6'><b>{tag}</b> (n={list(co.values())[0]['n']})</td></tr>"
        for k, v in co.items():
            rows_co += (f"<tr><td><code>{k}</code></td><td class='num'>{v['n']}</td>"
                        f"<td class='num'>{v['rho_trade']:+.3f}</td>"
                        f"<td class='num {'pos' if v['p_trade']<.05 else 'dim'}'>{v['p_trade']:.3f}</td>"
                        f"<td class='num'>{v['rho_abs_move']:+.3f}</td>"
                        f"<td class='num dim'>{v['p_abs_move']:.3f}</td></tr>")

    NL = {"all measured": "alle meetbare namen", FLOORKEY: "boven de conviction floor",
          "low spike": "lage zoekpiek", "mid": "midden", "high spike": "hoge zoekpiek"}
    rows_b = ""
    for tag, b in d["buckets"].items():
        rows_b += f"<tr class='hl'><td colspan='6'><b>{esc(NL.get(tag, tag))}</b></td></tr>"
        for name, v in b.items():
            rows_b += (f"<tr><td>{esc(NL.get(name, name))} "
                       f"<span class='dim'>({v['spike_range'][0]:.2f}&#215;&ndash;"
                       f"{v['spike_range'][1]:.2f}&#215;)</span></td>"
                       f"<td class='num'>{v['n']}</td><td class='num'>{v['hits']}/{v['n']}</td>"
                       f"<td class='num'>{v['hit_rate']*100:.0f}%</td>"
                       f"<td class='num {cls(v['mean'])}'>{v['mean']:+.2f}%</td>"
                       f"<td class='num dim'>{v['median_abs_move']:.2f}%</td></tr>")

    sd = co_fl["spike_day"]
    fb = d["buckets"].get(FLOORKEY, {})
    lo_b, hi_b = fb.get("low spike", {}), fb.get("high spike", {})

    body = f"""
<header class="top">
  <span class="eyebrow">stage E &middot; onderzoeksvraag 4</span>
  {crumbs("search-volume.html")}
  <h1>Hoeveel wordt er naar het bedrijf gezocht?</h1>
  <p class="lede">Google Trends, dagelijks, VS, de 90 dagen tot aan de instap. De vraag is
  of <b>aandacht</b> iets zegt over het rendement van de voorspelde trade. Op het
  verhandelde boek is dit de enige van de drie nieuwe vragen die niet leeg terugkomt:
  een hogere zoekpiek gaat samen met een <b>slechter</b> resultaat, rho
  {sd['rho_trade']:+.3f} bij p&nbsp;=&nbsp;{sd['p_trade']:.3f} op {sd['n']} events.
  Dat is één cel uit tien en de steekproef is klein.</p>
  <div class="facts">
    <div class="fact"><b>{d['n_measured']}</b><span>meetbare namen</span></div>
    <div class="fact"><b>{n_sparse}</b><span>te dun voor een basislijn</span></div>
    <div class="fact"><b>{n_sil}</b><span>nul op elke dag</span></div>
    <div class="fact"><b class="mono">{sd['rho_trade']:+.2f}</b><span>rho, boven de floor</span></div>
  </div>
</header>

<section>
  <h2>De helft van het boek is niet meetbaar, en dat is zelf een bevinding</h2>
  <p>Google rapporteert nul onder zijn eigen drempel, en dit is een boek van microcaps.
  Van de {d['n_events']} events zijn er {d['n_measured']} meetbaar: {n_sil} series staan
  op nul op elke dag, en {n_sparse} zijn <b>te dun</b> &mdash; wel iets, maar op minder
  dan de helft van de dagen.</p>
  <div class="note"><span class="lbl">de eerste versie van deze pagina had het fout</span>
  <p>Elke reeks wordt geschaald op haar <em>eigen</em> maximum. Een naam die op drie van
  de negentig dagen wordt gezocht leest dus 0, 0, &hellip; 0, 100 &mdash; en een piek
  gedeeld door een mediaan van nul komt uit op 100&#215;. In de eerste run vulden elf
  van die namen de bovenste tercile en zag het er uit alsof de grootste pieken de
  kleinste rendementen hadden. Dat was de kwantisering van een lege reeks, niet
  aandacht. De eis is nu een mediaan boven nul: minstens de helft van de dagen moet
  meetbare interesse dragen.</p></div>
  <p>Wat overblijft is systematisch de <b>liquide</b> helft: de meetbare namen zetten
  mediaan ${sel.get('median_dv_measured',0)/1e6:.1f}m per dag om, de onmeetbare
  ${sel.get('median_dv_silent',0)/1e6:.1f}m. Elke correlatie hieronder geldt dus voor de
  grotere namen in het boek en zegt niets over de helft die deze stage het vaakst
  verhandelt.</p>
</section>

<section>
  <h2>Zoekpiek tegen het rendement van de trade</h2>
  <p class="sub">Horizontaal: de zoekintensiteit op de instapdag gedeeld door de eigen
  mediaan over 90 dagen. Verticaal: wat de trade opleverde, getekend door
  <code>impact_sum</code>, ingestapt om 20:00 CET en verkocht op de volgende slotkoers.</p>
  <figure>
    <div class="chart">
      {legend([("boven de conviction floor", "var(--s1)"),
               ("onder de floor", "var(--s2)")])}
      {scatter(rows, "spike_day", "trade_close",
               "zoekintensiteit op de instapdag, ten opzichte van de eigen mediaan",
               "rendement per trade")}
      <div class="tip"></div>
    </div>
    <figcaption>{len(rows)} meetbare events. De punten links van de stippellijn zijn
    namen die op hun eigen printdag <em>minder</em> werden gezocht dan normaal.</figcaption>
  </figure>
</section>

<section>
  <h2>De correlaties</h2>
  <p class="sub">Spearman met permutatie-p. <code>trade</code> is het rendement van het
  boek; <code>|move|</code> is hoe ver het aandeel in welke richting dan ook bewoog
  &mdash; een andere claim, en degene die aandacht het meest voor de hand liggend zou
  aandrijven.</p>
  <div class="tbl"><table>
    <thead><tr><th>maat</th><th class="num">n</th><th class="num">rho vs trade</th>
    <th class="num">p</th><th class="num">rho vs |move|</th><th class="num">p</th></tr></thead>
    <tbody>{rows_co}</tbody>
  </table></div>
</section>

<section>
  <h2>Per tercile</h2>
  <p class="sub">Hetzelfde zonder aan te nemen dat het verband monotoon is.</p>
  <div class="tbl"><table>
    <thead><tr><th>bak</th><th class="num">n</th><th class="num">raak</th>
    <th class="num">trefkans</th><th class="num">per trade</th>
    <th class="num">mediane |beweging|</th></tr></thead>
    <tbody>{rows_b}</tbody>
  </table></div>
  <p>Op het verhandelde boek: de laagste zoekpieken geven
  {pct(lo_b.get('mean'))} per trade op {lo_b.get('hits','–')} van {lo_b.get('n','–')},
  de hoogste {pct(hi_b.get('mean'))} op {hi_b.get('hits','–')} van {hi_b.get('n','–')}.
  De kolom rechts verklaart waarom dat plausibel is: in de bak met de hoogste
  zoekintensiteit bewoog het aandeel mediaan {hi_b.get('median_abs_move',0):.2f}%, tegen
  {lo_b.get('median_abs_move',0):.2f}% in de laagste. Veel aandacht hoort bij een print
  die al is uitgekauwd, en die beweegt minder.</p>
  <div class="note"><span class="lbl">wat dit nog niet is</span>
  <p>{sd['n']} events, en tien correlatiecellen bekeken. Een p van {sd['p_trade']:.3f}
  overleeft een correctie voor tien toetsen niet: {sd['p_trade']*10:.2f} na Bonferroni.
  Daar komt bij dat deze steekproef precies de liquide helft van het boek is, en dat de
  zoekopdracht per bedrijf één keer is gekozen zonder alternatieven te proberen &mdash;
  dat laatste is een keuze vóóraf en geen vrijheidsgraad, maar het betekent ook dat een
  bedrijf met een moeilijke naam gewoon slecht is gemeten.</p>
  <p>Dit is een spoor om vooruit te draaien, geen bevinding. De bruikbare versie ervan
  is goedkoop: zet de zoekpiek in de baseline, naast <code>run_up_20d_pct</code>, zodat
  hij elke dag wordt vastgelegd en over een paar maanden een echte steekproef heeft.</p></div>
</section>

{foot(gen)}
"""
    return page("Zoekvolume en rendement", body)


# --------------------------------------------------------------- calendar page
def build_calendar(d, gen):
    t = d["totals"]
    rows = ""
    for date in sorted(d["by_date"]):
        names = d["by_date"][date]
        conf = [n for n in names if n["session"] in ("amc", "bmo")]
        tr = sorted([n for n in conf if n.get("clears_liquidity")],
                    key=lambda n: -(n.get("dollar_vol") or 0))
        if not conf:
            rows += (f"<tr><td>{esc(date)}</td><td class='num dim'>0</td>"
                     f"<td class='num dim'>{len(names)}</td><td class='dim' colspan='2'>"
                     f"geen bevestigde sessie</td></tr>")
            continue
        for i, n in enumerate(tr or conf):
            first = i == 0
            dv = n.get("dollar_vol")
            rows += (
                f"<tr>"
                f"<td>{esc(date) if first else ''}</td>"
                f"<td class='num'>{len(conf) if first else ''}</td>"
                f"<td class='num dim'>{len(names)-len(conf) if first else ''}</td>"
                f"<td><b>{esc(n['ticker'])}</b> <span class='dim'>{esc((n.get('company') or '')[:38])}</span></td>"
                f"<td class='num'>{esc(n['session'])}</td>"
                f"<td class='num'>{'$%.1fm' % (dv/1e6) if dv else '–'}</td>"
                f"<td class='num dim'>{esc(n.get('eps_estimate') or '–')}</td></tr>")
    body = f"""
<header class="top">
  <span class="eyebrow">stage E &middot; vooruitblik</span>
  {crumbs("calendar.html")}
  <h1>Wat er komende week rapporteert</h1>
  <p class="lede">Geen onderzoeksresultaat maar een planningsbeeld: hoeveel namen komen
  eraan, op welke sessie, en hoeveel daarvan de twee poorten halen die bepalen of de
  edge hunt ze überhaupt ziet. Van de {t['rows']} kalenderregels dragen er
  <b>{t['confirmed_session']}</b> een bevestigde sessie, en <b>{t['clears_liquidity']}</b>
  daarvan halen ook de omzetvloer van ${d['liquidity_floor_usd']:,.0f} per dag.</p>
  <div class="facts">
    <div class="fact"><b>{t['rows']}</b><span>kalenderregels</span></div>
    <div class="fact"><b>{t['confirmed_session']}</b><span>bevestigde sessie</span></div>
    <div class="fact"><b>{t['clears_liquidity']}</b><span>halen ook de omzetvloer</span></div>
    <div class="fact"><b>{len(d['by_date'])}</b><span>handelsdagen</span></div>
  </div>
</header>

<section>
  <h2>De twee poorten, allebei toegepast</h2>
  <p><b>Sessie.</b> Het veld <code>time</code> van Nasdaq is een rooster bij
  <code>time-pre-market</code> en <code>time-after-hours</code>, en een bekentenis van
  onwetendheid bij <code>time-not-supplied</code>. Stage 0 laat die derde groep vallen.
  Dat is meestal de <em>grootste</em> helft van de kalender, en de gemeten phantom rate
  erop is 20 van 20 voor het venster van 17 september en 8 van 8 voor 31 augustus
  &mdash; TRT hoorde bij die twintig en rapporteerde nooit. Weglaten is dus goed, maar
  het is niet gratis en beide tellingen staan hieronder.</p>
  <p><b>Liquiditeit.</b> <code>execution.benchmark.min_dollar_volume_usd</code>, nu
  ${d['liquidity_floor_usd']:,.0f} per dag. Namen eronder worden weggelaten in plaats van
  kleiner gemaakt, dus een agenda die ze meetelt overdrijft wat verhandelbaar is.</p>
</section>

<section>
  <h2>De namen</h2>
  <p class="sub">Alleen bevestigde sessies, gesorteerd op omzet per dag. Omzet is de
  slotkoers maal het 20-daagse gemiddelde volume.</p>
  <div class="tbl"><table>
    <thead><tr><th>datum</th><th class="num">bevestigd</th><th class="num">onbekend</th>
    <th>naam</th><th class="num">sessie</th><th class="num">omzet/dag</th>
    <th class="num">eps-verwachting</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <div class="note"><span class="lbl">wat hier niet in staat</span>
  <p>Geen voorspelling, geen ranking, geen score &mdash; die komen uit een hunt die nog
  niet heeft gedraaid. Een naam op deze lijst is een kandidaat, en het archief zegt dat
  de meeste kandidaten de conviction floor nooit halen: 55 van 106 afgerekende events
  wel, en op de vier dunste dagen geen enkele.</p></div>
</section>

{foot(gen)}
"""
    return page("Agenda komende week", body)


PRIOR_PAGES = (
    '<p><b>Eerdere pagina&rsquo;s over deze stage:</b> '
    '<a href="https://claude.ai/artifact/6WTHvvvb4cqHsUG1AuNBqw">Voorspeld tegen '
    'gerealiseerd</a> &middot; '
    '<a href="https://claude.ai/artifact/YUT3cwijrfJ6Gq7DWhqYpu">Stage E Exit Clock</a>.</p>')


# ------------------------------------------------------------------- index page
def qrow(chip, chip_cls, title, answer, stats, href, link_label="Lees de pagina"):
    st = "".join(f'<span class="n">{esc(v)}<em>{esc(k)}</em></span>' for k, v in stats)
    go = f'<a class="go" href="{href}">{esc(link_label)} &rarr;</a>' if href else ""
    return f"""<article class="q">
  <div class="qh"><h2>{title}</h2><span class="chip {chip_cls}">{esc(chip)}</span></div>
  {go}
  <p class="ans">{answer}</p>
  <div class="stat">{st}</div>
</article>"""


def build_index(ru, ec, sv, cal, gen):
    n, nd, nf = ru["n_events"], ru["n_days"], ru["n_above_floor"]
    best_p1 = min(v["p_signed"] for v in ru["windows"].values())
    ag = ru["agreement"][FLOORKEY]
    sp = ec["floor_close_spread"]
    a14 = ec["floor_close"]["1400"]
    sd = sv["correlations"][FLOORKEY]["spike_day"]
    bk = ru["books"]
    t = cal["totals"]

    ledger = "".join([
        qrow("leeg", "c-null",
             "Voorspelt de aanloop of de richting klopte?",
             "Nee. Het rendement over 2, 5, 10 en 20 sessies vóór de instap zegt niets "
             "over de vraag of het teken van de hunt goed was. Geen enkele rho komt "
             "boven 0,16, geen enkele p onder 0,11, en de trefkans per aanloopterciel "
             "blijft binnen 49&ndash;57%.",
             [("events", n), ("laagste p", f"{best_p1:.2f}"),
              ("grootste |rho|", f"{max(abs(v['rho_signed']) for v in ru['windows'].values()):.3f}")],
             "runup.html"),
        qrow("leeg", "c-null",
             "Levert het meer op als de aanloop meebeweegt?",
             "Niet op het boek dat wordt verhandeld. Over alle namen lijkt meebewegen te "
             "helpen, maar boven de conviction floor draait het bij <em>alle vier</em> de "
             "vensters om: tegenbewegen betaalt meer. Twee deelverzamelingen die "
             "tegengesteld wijzen met volledig overlappende intervallen zijn ruis die "
             "twee keer is gemeten.",
             [("eens, 10d", pct(ag["10d"]["agree"]["mean"])),
              ("oneens, 10d", pct(ag["10d"]["disagree"]["mean"])),
              ("boven de floor", nf)],
             "runup.html"),
        qrow("leeg", "c-null",
             "Is 20:00 CET het juiste instapmoment, of is later beter?",
             "Het maakt niet uit. Tussen 16:00 en 22:00 CET scheelt de beste en de "
             "slechtste instap {:.2f} procentpunt op een rendement met een "
             "standaardafwijking van {:.0f}. Er is ook geen intradagdrift om op te "
             "timen: geen enkele t boven 1,6.".format(sp["spread"], a14["sd"]),
             [("om 20:00 CET", pct(a14["mean"])), ("spreiding over 6 uur",
                                                   f"{sp['spread']:.2f}pp"),
              ("sd per trade", f"{a14['sd']:.0f}")],
             "entry-clock.html"),
        qrow("spoor", "c-lead",
             "Zegt het Google-zoekvolume iets over het rendement?",
             "Mogelijk, en de enige van de vier die niet leeg terugkomt. Boven de "
             "conviction floor gaat een hogere zoekpiek samen met een <em>slechter</em> "
             "resultaat, en namen met veel aandacht bewegen ook minder. Eén cel uit "
             "tien, op {} events, op de liquide helft van het boek.".format(sd["n"]),
             [("rho", f"{sd['rho_trade']:+.3f}"), ("p", f"{sd['p_trade']:.3f}"),
              ("p na Bonferroni", f"{min(1, sd['p_trade']*10):.2f}"),
              ("meetbaar", f"{sv['n_measured']} van {sv['n_events']}")],
             "search-volume.html"),
        qrow("vooruitblik", "c-plan",
             "Wat komt er de komende week aan?",
             "{} kalenderregels over {} handelsdagen. {} dragen een bevestigde sessie "
             "en {} daarvan halen ook de omzetvloer &mdash; dat is het aantal namen dat "
             "de hunt volgende week überhaupt kan zien.".format(
                 t["rows"], len(cal["by_date"]), t["confirmed_session"],
                 t["clears_liquidity"]),
             [("bevestigd", t["confirmed_session"]), ("verhandelbaar", t["clears_liquidity"]),
              ("weggelaten", t["rows"] - t["confirmed_session"])],
             "calendar.html", "Bekijk de agenda"),
    ])

    body = f"""
<header class="top">
  <span class="eyebrow">stage E &middot; edge hunt &middot; 31 aug &ndash; heden</span>
  {crumbs("index.html")}
  <h1>Onderzoeksregister van de edge hunt</h1>
  <p class="lede">Eén vraag per regel, met het antwoord dat de data geeft en de
  steekproef waarop dat rust. Alles komt uit de edge hunt zelf &mdash;
  <code>research/&lt;datum&gt;/edge/</code> &mdash; vanaf de eerste run op 31 augustus
  2026. Drie van de vier nieuwe vragen komen leeg terug, en dat is een antwoord.</p>
  <div class="facts">
    <div class="fact"><b>{n}</b><span>afgerekende events</span></div>
    <div class="fact"><b>{nd}</b><span>hunt-dagen</span></div>
    <div class="fact"><b>{nf}</b><span>boven de conviction floor</span></div>
    <div class="fact"><b class="mono">{pct(bk['hunt_above_floor']['mean'])}</b><span>de hunt per trade</span></div>
    <div class="fact"><b class="mono">{pct(bk['short_all']['mean'])}</b><span>alles shorten</span></div>
  </div>
</header>

<section>
  <h2>De steekproef is bijna drie keer zo groot geworden</h2>
  <p>Tot nu toe rustte alles in <code>edge/EDGE_ANALYSIS.md</code> op 38 events over vijf
  onafhankelijke dagen. Dat was geen keuze: <code>edge_decompose.py</code> leest
  <code>edge_score</code> en <code>confidence</code> van elke gerangschikte regel, en die
  velden verlieten het bestand op 9 september toen <code>impact_sum</code> de sleutel
  werd. Sindsdien liep het script vast op elke nieuwe run, en zeven dagen aan hunts
  stonden op schijf zonder in enige steekproef te zitten.</p>
  <p><code>edge_sample.py</code> leest de velden die <em>beide</em> schema's dragen en
  laadt alle {nd} dagen: <b>106 events</b>, ontdubbeld op (ticker, eventdatum, sessie).
  Daarvan hebben er {n} bruikbare koersbalken &mdash; LEN.B valt af als tweede
  aandelenklasse &mdash; en {nf} staan boven de conviction floor. De 38 regels van de
  oude steekproef komen er exact uit terug.</p>
  <div class="note acc"><span class="lbl">wat dat met de bestaande conclusies doet</span>
  <p>Dit register vervangt <code>edge/EDGE_ANALYSIS.md</code> niet. Het zegt wel dat de
  gratis controle die daar de hunt op elke steekproef versloeg &mdash; het omgekeerde van
  de 20-daagse aanloop &mdash; op deze grotere steekproef {pct(bk['minus_runup_20d']['mean'])}
  per trade doet. Ook die controle is niet stabiel. De vergelijking die wél overeind
  blijft is de hunt boven de floor, {pct(bk['hunt_above_floor']['mean'])}, tegen alles
  shorten zonder onderzoek, {pct(bk['short_all']['mean'])}.</p></div>
</section>

<section>
  <h2>De vragen</h2>
  <p class="sub">Leeg = gemeten en niets gevonden. Spoor = iets gevonden dat een
  correctie voor meervoudig toetsen niet overleeft. Vooruitblik = geen meting.</p>
  <div class="ledger">{ledger}</div>
</section>

<section>
  <h2>Wat hiervoor al was vastgesteld</h2>
  <p class="sub">Eerder werk op dezelfde stage, op de oude steekproef van 38 events.
  Niet opnieuw gemeten in dit register.</p>
  <div class="tbl"><table class="prose">
    <thead><tr><th>vraag</th><th>stand</th><th class="num">n</th></tr></thead>
    <tbody>
      <tr><td>Rangschikt <code>edge_score</code> de dag?</td>
          <td>Nee &mdash; rho 0,243 (p 0,156), en de ruwe invoer doet het beter op 0,407.
          De aggregatie is aftrekkend.</td><td class="num">38</td></tr>
      <tr class="hl"><td>Zit de richting in de grote voorspellingen?</td>
          <td>Ja, dit is de enige regel die een familiegewijze correctie overleefde:
          boven <code>|impact_sum| &ge; 3</code> klopte het teken 16 van 21 keer.</td>
          <td class="num">38</td></tr>
      <tr><td>Verslaat de hunt een gratis controle?</td>
          <td>Toen niet &mdash; min de 20-daagse aanloop stond op rho 0,335 en 6 van 6
          dagen positief. Op de steekproef hierboven keert dat om.</td><td class="num">38</td></tr>
      <tr><td>Wanneer moet de positie eruit?</td>
          <td>Geen uniforme vroege uitstap is te onderscheiden van vasthouden tot de
          close; <code>amc</code> en <code>bmo</code> willen tegengestelde dingen.</td>
          <td class="num">38</td></tr>
      <tr><td>Houdt het stand op de verzegelde backtest?</td>
          <td>Nee &mdash; rho +0,073 (p 0,45) over 104 events. Het meest ontmoedigende
          getal in de repo.</td><td class="num">104</td></tr>
    </tbody>
  </table></div>
  <p>De onderbouwing van deze rij staat in <code>edge/EDGE_ANALYSIS.md</code> en
  <code>backtest/FINDINGS.md</code> &sect;33.</p>
</section>

{foot(gen, PRIOR_PAGES)}
"""
    return page("Onderzoeksregister edge hunt", body)


def main():
    gen = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ru, ec, sv, cal = (load("edge-runup.json"), load("edge-entry-clock.json"),
                       load("edge-search-volume.json"), load("edge-calendar.json"))
    missing = [n for n, v in (("edge-runup", ru), ("edge-entry-clock", ec),
                              ("edge-search-volume", sv), ("edge-calendar", cal)) if not v]
    if missing:
        sys.exit("missing analysis output: " + ", ".join(missing)
                 + "\nrun the matching edge_*.py first")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, html_text in (("index.html", build_index(ru, ec, sv, cal, gen)),
                            ("runup.html", build_runup(ru, gen)),
                            ("entry-clock.html", build_entry(ec, gen)),
                            ("search-volume.html", build_search(sv, gen)),
                            ("calendar.html", build_calendar(cal, gen))):
        (OUT / name).write_text(html_text)
        print(f"wrote {(OUT / name).relative_to(REPO)}  "
              f"{len(html_text)/1024:.0f} KB")


if __name__ == "__main__":
    main()
