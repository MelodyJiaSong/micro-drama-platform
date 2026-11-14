import re,sys,pathlib
for f in sys.argv[1:]:
    t=pathlib.Path(f).read_text(encoding='utf-8',errors='replace')
    t=re.sub(r'<ref[^>/]*/>','',t); t=re.sub(r'(?s)<ref[^>]*>.*?</ref>','',t)
    t=re.sub(r'\{\{(?:[Cc]onvert|cvt)\|([\d.,]+)\|([A-Za-z/]+)[^}]*\}\}',r'\1 \2',t)
    print('=====',f)
    seen=set()
    m=re.search(r'\|\s*production\s*=([^\n]*)',t)
    if m: print('  PROD:',m.group(1)[:150])
    for m in re.finditer(r'(?i)top.speed|maximum speed|units|examples (?:were|will)|produced',t):
        a=max(0,m.start()-140)
        if any(abs(a-s)<200 for s in seen): continue
        seen.add(a)
        print('  ..',t[a:m.end()+140].replace('\n',' '))
        if len(seen)>=7: break
