import json,hashlib,os
for m in ['render/ep16_largest_stadiums_master.manifest.json','render/ep16_largest_stadiums_master_with-risk-images.manifest.json']:
    d=json.load(open(m,encoding='utf-8'))
    print(m, {k:v for k,v in d.items() if k not in ('inputs','timeline')})
    print(d['timeline'])
    bad=[]
    for k,v in d['inputs'].items():
        try:
            h=hashlib.sha256(open(k,'rb').read()).hexdigest()
        except Exception as e:
            h=str(e)
        if h!=v: bad.append(k)
    print('inputs changed since render:',bad, 'n inputs',len(d['inputs']))
    out=os.path.basename(d['output'].replace(chr(92),'/'))
    h=hashlib.sha256(open('render/'+out,'rb').read()).hexdigest()
    print('output sha match', h==d.get('output_sha256'))
