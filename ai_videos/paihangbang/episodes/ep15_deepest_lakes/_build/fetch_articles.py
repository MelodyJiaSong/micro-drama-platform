import json, re, time, urllib.request, urllib.error, urllib.parse, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
titles = ["Lake Baikal","Lake Tanganyika","Caspian Sea","Lake Vostok","O'Higgins/San Martín Lake","Viedma Lake","Lake Argentino","Lake Malawi","Issyk-Kul","Great Slave Lake","Crater Lake","Lake Matano","Lake General Carrera/Buenos Aires","Hornindalsvatnet","Quesnel Lake","Sarez Lake","Lake Toba","Lake Tahoe","Salvatnet","Lake Kivu","Nahuel Huapi Lake","Lake Hauroko","Cochrane/Pueyrredón Lake","Lake Tinn","Adams Lake","Lake Chelan","Mjøsa","Lake Van","Lake Poso","Lake Fagnano","Great Bear Lake","Lake Manapouri","Lake Como","Lake Te Anau","Lake Tazawa","Lake Khantayskoye","Lake Wakatipu","Grey Lake","Lake Superior","Lake Hāwea","Suldalsvatnet","Fyresvatnet","Lake Maggiore","Chilko Lake","Lake Shikotsu","Dead Sea","Lake Ohrid","Lake Titicaca","Lake Garda","Lake Geneva","Loch Morar","Kurile Lake","Lake Teletskoye","Lago de Atitlán","Lake Pend Oreille","Todos los Santos Lake","Llanquihue Lake","Traful Lake","Lake Sarmiento","Lake Iliamna"]
out = Path('raw/articles')
UA={'User-Agent':'paihangbang-research/1.0 (python-urllib; 1 req/s)'}
res={}
for t in titles:
    f = out/(re.sub(r'[^\w]+','_',t)+'.wikitext')
    if not f.exists():
        u='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode({'action':'parse','page':t,'prop':'wikitext|revid','format':'json','formatversion':2,'redirects':1})
        for a in range(6):
            try:
                d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()); break
            except urllib.error.HTTPError as e:
                if e.code!=429: raise
                time.sleep(10*(a+1))
        if 'parse' not in d: print('MISSING',t); continue
        f.write_text(f"<!--revid {d['parse']['revid']} title {d['parse']['title']}-->\n"+d['parse']['wikitext'],encoding='utf-8')
        time.sleep(2.5)
    w=f.read_text(encoding='utf-8')
    keys={}
    for k in ['max-depth','max_depth','depth','area','elevation','countries','basin_countries','volume','surface_area','mean_depth','avg-depth','coords']:
        m=re.search(r'\|\s*'+k+r'\s*=\s*(.{0,300})',w)
        if m: keys[k]=m.group(1)[:300]
    res[t]=keys
    print('==',t); [print('  ',k,':',v[:220]) for k,v in keys.items() if k in('max-depth','max_depth','depth','area','surface_area','elevation','countries','basin_countries')]
json.dump(res,open('raw/infobox_summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
