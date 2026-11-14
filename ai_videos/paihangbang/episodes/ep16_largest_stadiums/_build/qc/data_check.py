import json,collections
d=json.load(open('data.json',encoding='utf-8')); it=d['items']
vals=[x['value'] for x in it]
print('n',len(it),'sorted desc',vals==sorted(vals,reverse=True))
bad=[]
for x in it:
    exp=1+sum(1 for y in it if y['value']>x['value'])
    if exp!=x['rank']: bad.append((x['name'],x['rank'],exp))
    if x['value_display'].replace(',','')!=str(x['value']): bad.append(('disp',x['name'],x['value_display']))
print('rank/display issues',bad)
c=collections.Counter(x['country_name'] for x in it); print(c.most_common())
print('iso',sorted(set((x['country_iso2'],x['country_name']) for x in it)))
for x in it:
    if len(x.get('badge') or '')>22: print('badge long',x['badge'])
    for t in x.get('tags',[]):
        if len(t['text'])>24: print('tag long',x['name'],t)
for s in d['insights']: print(len(s['text']),s['text'])
print(len(d['scope_note']))
