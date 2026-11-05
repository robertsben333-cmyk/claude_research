"""Run stage EU's own resolver (with the 2026-11-05 Nordic fix) over every panel day,
writing to resolved/<day>.json here. The Nasdaq Nordic feed has no date query and is
paged; pages are memoised across days so one walk back to 2026-10-12 serves all runs."""
import sys, glob, functools
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'researcher_europe/scripts'))
import eu_archive as A, eu_resolve as R
_get = A.get
@functools.lru_cache(maxsize=None)
def _cached(url, timeout):
    return _get(url, timeout=timeout)
def get(url, timeout=45):
    return _cached(url, timeout) if 'news.eu.nasdaq.com' in url else _get(url, timeout=timeout)
A.get = get
A.NASDAQ_MAX_PAGES = 45
import eu_market; eu_market.NASDAQ_MAX_PAGES = 45
here = Path(__file__).resolve().parent
days = sys.argv[1:] or [p.split('/')[-2] for p in sorted(glob.glob(str(REPO / 'research/2026/1*/*/europe')))]
for d in days:
    run = next(iter(glob.glob(str(REPO / f'research/2026/*/{d}/europe'))))
    if not Path(run, 'edge-scores-panel.json').exists():
        continue
    sys.argv = ['eu_resolve.py', '--run', run, '-o', str(here / 'resolved' / f'{d}.json')]
    try:
        R.main()
    except SystemExit as e:
        print(d, 'exit', e)
