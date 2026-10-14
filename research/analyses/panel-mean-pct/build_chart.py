#!/usr/bin/env python3
"""Renders panel-mean-pct.json into panel-mean-pct.html (inline SVG, no network)."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent
data = json.load(open(D / 'panel-mean-pct.json'))
slim = {k: data[k] for k in ('curve', 'short_every_name_mv_close', 'current_rule_selected', 'factor', 'model_median_abs_size', 'resolved', 'names')}
slim['rows'] = [{k: r[k] for k in ('date', 'ticker', 'session', 'avg_pct', 'mv_close', 'mv_strategy', 'selected', 'scaled')}
                for r in data['rows'] if r['mv_close'] is not None]
html = (D / 'chart_template.html').read_text().replace('__DATA__', json.dumps(slim))
(D / 'panel-mean-pct.html').write_text(html)
print('wrote', D / 'panel-mean-pct.html')
