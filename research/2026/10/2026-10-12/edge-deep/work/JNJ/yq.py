import urllib.request, http.cookiejar, json, sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
try:
    op.open(urllib.request.Request("https://fc.yahoo.com", headers={"User-Agent":UA}), timeout=20)
except Exception as e:
    pass
crumb=op.open(urllib.request.Request("https://query2.finance.yahoo.com/v1/test/getcrumb", headers={"User-Agent":UA}), timeout=20).read().decode()
mods=sys.argv[2]
u=f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sys.argv[1]}?modules={mods}&crumb={crumb}"
d=json.loads(op.open(urllib.request.Request(u, headers={"User-Agent":UA}), timeout=20).read())
print(json.dumps(d)[:200000])
