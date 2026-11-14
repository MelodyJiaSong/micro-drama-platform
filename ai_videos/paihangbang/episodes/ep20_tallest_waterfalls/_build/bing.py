# python -I bing.py "query" → Bing 图片搜索结果（murl 原图、purl 来源页、标题、尺寸）；只读公开搜索页
import sys,re,html,json,urllib.parse,urllib.request
sys.stdout.reconfigure(encoding='utf-8')
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 15
u='https://www.bing.com/images/search?'+urllib.parse.urlencode({'q':q,'form':'HDRSC2','first':'1','setlang':'en-us','cc':'us','mkt':'en-US'})
t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}),timeout=60).read().decode('utf-8','replace')
k=0
for m in re.finditer(r'class="iusc"[^>]*?m="([^"]+)"',t):
    d=json.loads(html.unescape(m.group(1)))
    sz=re.search(r'(\d+) x (\d+)', t[m.end():m.end()+3000])
    print(k, d.get('murl'),'|',d.get('purl'),'|',d.get('t','')[:70]); k+=1
    if k>=n: break
