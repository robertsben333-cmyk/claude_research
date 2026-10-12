import sys, json
sys.path.insert(0, "/home/user/claude_research/researcher_us/scripts")
import edge_search_volume as SV
out = sys.argv[1]
res = {}
for kw in ["Domino's"]:
    try:
        pts = SV.fetch_series(kw, "2025-01-01", "2026-10-11", geo="US", partial=True)
        res[kw] = pts
    except Exception as e:
        res[kw] = {"error": repr(e)}
json.dump(res, open(out, "w"), default=str)
print({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()})
