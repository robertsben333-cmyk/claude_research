#!/usr/bin/env python3
"""Renders panel-mean-pct.json into panel-mean-pct.html (inline SVG, no network)."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent
data = json.load(open(D / 'panel-mean-pct.json'))
html = (D / 'chart_template.html').read_text().replace('__DATA__', json.dumps(data['regions']))
(D / 'panel-mean-pct.html').write_text(html)
print('wrote', D / 'panel-mean-pct.html')
