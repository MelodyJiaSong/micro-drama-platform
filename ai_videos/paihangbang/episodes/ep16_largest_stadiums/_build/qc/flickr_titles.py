import json,subprocess,re,html
a=json.load(open('assets.json',encoding='utf-8'))
out=open('_build/qc/source_titles.txt','w',encoding='utf-8')
for e in a:
    u=e.get('source_page') or ''
    if not any(s in u for s in ('flickr.com','pexels.com','unsplash.com')): continue
    try:
        t=subprocess.run(['curl','-sL','-A','Mozilla/5.0','--max-time','30',u],capture_output=True,timeout=40).stdout.decode('utf-8','ignore')
    except Exception as ex: t=''
    ti=re.search(r'<title>([^<]*)</title>',t); de=re.search(r'og:description" content="([^"]{0,250})',t)
    lic=re.search(r'(Attribution[^"<]{0,60}|Some rights reserved|All rights reserved|Public Domain[^"<]{0,30})',t)
    line=f"{e['file'].split('/')[-1]} | {html.unescape(ti.group(1)) if ti else '-'} | {html.unescape(de.group(1)) if de else ''} | {lic.group(1) if lic else ''}"
    print(line); out.write(line+'\n')
