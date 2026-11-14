import json,collections
inb=json.load(open('inbound.json',encoding='utf-8'));acc=json.load(open('acc.json',encoding='utf-8'))
d=collections.defaultdict(dict)
for r in inb+acc:
    if r.get('partner_area_label') not in (None,'World') : continue
    code=r['indicator_code'].replace('INBD_TRIP_TOTL_TOTL_','').replace('INBD_ACCM_','')
    if code not in ('TOUR','VSTR','COMM_GUES','HOTL_GUES'): continue
    try: v=float(r['value'])
    except: continue
    d[r['reporter_area_label']][(code,int(r['year']))]=v/1000
groups={
'europe':['France','Türkiye','Spain','Italy','United Kingdom of Great Britain and Northern Ireland','Germany','Greece','Austria','Portugal','Netherlands (Kingdom of the)','Poland','Croatia','Czechia','Denmark','Hungary','Romania','Switzerland','Albania','Belgium','Ireland','Bulgaria','Sweden','Norway','Russian Federation','Slovenia','Finland','Cyprus','Andorra','Belarus','Montenegro','Estonia','Malta','Iceland','Serbia','Lithuania','Latvia','Ukraine','Bosnia and Herzegovina','Slovakia','Luxembourg'],
'asia':['China','China, Hong Kong Special Administrative Region','China, Macao Special Administrative Region','Japan','Thailand','Saudi Arabia','Malaysia','United Arab Emirates','Viet Nam','Republic of Korea','Indonesia','Singapore','Kazakhstan','India','Uzbekistan','Taiwan Province of China','Bahrain','Philippines','Cambodia','Jordan','Georgia','Qatar','Iran (Islamic Republic of)','Kyrgyzstan','Azerbaijan','Armenia','Australia','New Zealand','Maldives','Sri Lanka','Oman','Israel','Lebanon','Lao People\'s Democratic Republic','Kuwait','Iraq','Mongolia','Nepal'],
'africa_americas':['United States of America','Mexico','Canada','Egypt','Morocco','Tunisia','South Africa','Dominican Republic','Brazil','Argentina','Colombia','Puerto Rico','Chile','Peru','Cuba','Costa Rica','El Salvador','Jamaica','Panama','Uruguay','Guatemala','Ecuador','Kenya','Nigeria','Tanzania (United Republic of)','United Republic of Tanzania','Zimbabwe','Algeria','Bahamas']}
cols=[('TOUR',2019),('TOUR',2022),('TOUR',2023),('TOUR',2024),('VSTR',2019),('VSTR',2023),('VSTR',2024),('COMM_GUES',2019),('COMM_GUES',2024),('HOTL_GUES',2019),('HOTL_GUES',2024)]
for g,cs in groups.items():
    out=['# UN Tourism Statistics Database (bulk 12/2025) reference values, million','','| country | '+' | '.join(f'{a} {y}' for a,y in cols)+' |','|'+'---|'*(len(cols)+1)]
    for c in cs:
        if c not in d: out.append(f'| {c} | (not in database) |'); continue
        out.append(f'| {c} | '+' | '.join(f"{d[c][k]:.3f}" if k in d[c] else '' for k in cols)+' |')
    open(f'ref_{g}.md','w',encoding='utf-8').write('\n'.join(out)+'\n')
    print(g,len(cs))
