import json,urllib.parse,subprocess,sys,datetime,collections
kw=sys.argv[1]; geo=sys.argv[2] if len(sys.argv)>2 else ''
req={"comparisonItem":[{"keyword":kw,"geo":geo,"time":"2026-03-01 2026-11-16"}],"category":0,"property":""}
u="https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req="+urllib.parse.quote(json.dumps(req))
r=subprocess.run(['curl','-sS','-m','20','-A','Mozilla/5.0','-b','cj.txt',u],capture_output=True,text=True).stdout
d=json.loads(r[r.find('{'):])
w=[x for x in d['widgets'] if x['id']=='TIMESERIES'][0]
url="https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=0&req="+urllib.parse.quote(json.dumps(w['request'],separators=(',',':')))+"&token="+w['token']
r=subprocess.run(['curl','-sS','-m','20','-A','Mozilla/5.0','-b','cj.txt',url],capture_output=True,text=True).stdout
pts=json.loads(r[r.find('{'):])['default']['timelineData']
m=collections.OrderedDict()
for p in pts:
  k=str(datetime.datetime.utcfromtimestamp(int(p['time'])).date())[:7]; m.setdefault(k,[]).append(p['value'][0])
print(kw,geo,{k:round(sum(v)/len(v),1) for k,v in m.items()})
