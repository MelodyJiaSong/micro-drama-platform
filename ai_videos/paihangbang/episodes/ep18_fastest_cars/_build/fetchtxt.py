import re,sys,html,urllib.request
url=sys.argv[1]; pats=sys.argv[2:]
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36","Accept-Language":"en"})
try:
    s=urllib.request.urlopen(req,timeout=40).read().decode('utf-8','replace')
except Exception as e:
    print('ERR',e); sys.exit()
t=html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)))
t=re.sub(r'\s+',' ',t)
print('LEN',len(t))
seen=[]
for p in pats:
    for m in re.finditer(p,t,re.I):
        if any(abs(m.start()-x)<250 for x in seen): continue
        seen.append(m.start())
        print('..',t[max(0,m.start()-250):m.end()+250])
        if len(seen)>12: sys.exit()
