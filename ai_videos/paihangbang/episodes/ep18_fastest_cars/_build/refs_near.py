import re,sys,pathlib
pat=sys.argv[1]; files=sys.argv[2:]
for f in files:
    t=pathlib.Path(f).read_text(encoding='utf-8',errors='replace')
    names={}
    for m in re.finditer(r'<ref name\s*=\s*"?([^">/]+)"?\s*>(.*?)</ref>',t,re.S): names[m.group(1).strip()]=m.group(2)
    print('=====',f)
    k=0
    for m in re.finditer(pat,t,re.I):
        seg=t[m.start()-50:m.end()+700]
        refs=re.findall(r'<ref(?: name\s*=\s*"?([^">/]+)"?)?\s*(/?)>(.*?)(?:</ref>|$)',seg,re.S)
        urls=[]
        for nm,sl,body in refs:
            b=body if body.strip() else names.get(nm.strip(),'')
            urls+=re.findall(r'url\s*=\s*([^\s|}]+)',b)[:1]
            ti=re.findall(r'title\s*=\s*([^|}]+)',b)[:1]
            if ti: urls.append('   ['+ti[0].strip()[:90]+']')
        print('  >>',re.sub(r'<ref.*?(</ref>|/>)','',seg[:300],flags=re.S).replace('\n',' ')[:260])
        for u in urls[:6]: print('       ',u)
        k+=1
        if k>=3: break
