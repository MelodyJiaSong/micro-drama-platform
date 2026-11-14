import json,hashlib,sys,os
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
for name in ['ep16_largest_stadiums_master','ep16_largest_stadiums_master_with-risk-images']:
    m=json.load(open(f'render/{name}.manifest.json',encoding='utf-8'))
    out=sha(f'render/{name}.mp4')
    print(name,'output ok' if out==m['output_sha256'] else 'OUTPUT MISMATCH', m['duration_s'], m['render_seconds'], len(m['inputs']))
    print(' timeline',m['timeline'])
    bad=[]
    for p,h in m['inputs'].items():
        if not os.path.exists(p): bad.append((p,'missing')); continue
        if sha(p)!=h: bad.append((p,'changed'))
    print(' input mismatches:',bad)
