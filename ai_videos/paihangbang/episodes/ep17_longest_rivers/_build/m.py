import json,sys,glob
for a in sys.argv[1:]:
    i,ids=a.split(':'); d=glob.glob(f'reselect/cand/{int(i):02d}_*')[0]
    for m in json.load(open(d+'/meta.json',encoding='utf-8')):
        if m['id'] in ids.split(','):
            print(d[-22:],m['id'],m.get('w'),'x',m.get('h'),'|',m['author'][:25],'|',m['licence'][:22],'|',m['page_url'][:85],'|',m['why'][:140])
