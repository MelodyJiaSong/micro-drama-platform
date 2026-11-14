import json,hashlib
d=json.load(open('data.json',encoding='utf-8'))
L={e['file']:e for e in json.load(open('assets.json',encoding='utf-8'))}
rm=json.load(open('render/ep16_largest_stadiums_master_with-risk-images.manifest.json',encoding='utf-8'))['inputs']
mm=json.load(open('render/ep16_largest_stadiums_master.manifest.json',encoding='utf-8'))['inputs']
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
cnt={}
for it in d['items']:
    main=it.get('image'); risk=it.get('image_risk'); alt=it.get('image_alt')
    if main and risk:
        dm = alt or None
    else:
        dm = main
    rk = main
    lic=L.get(dm,{}).get('licence','-') if dm else '-'
    kind='NOIMG' if not dm else ('AI' if lic.lower().startswith('ai-generated') else 'photo')
    cnt[kind]=cnt.get(kind,0)+1
    rok = (rk in rm and rm[rk]==sha(rk)) if rk else None
    print(f"{it['rank']:>2} {it['name'][:34]:34} | DEF {kind:5} {(dm or '')[11:60]:50} | lic {lic[:22]:22} | RISK {(rk or '')[11:55]:45} risk={risk or ''} inRiskManifest={rok} note={it.get('image_note','')} badge={it.get('badge','')}")
print(cnt)
