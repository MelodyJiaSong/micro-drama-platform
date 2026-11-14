from pathlib import Path
import json,requests,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/textures';records=[]
for asset in ['white_sandstone_blocks_02','worn_mossy_plasterwall','wood_planks']:
    response=requests.get('https://api.polyhaven.com/files/'+asset,timeout=40);response.raise_for_status();data=response.json();(OUT/(asset+'_files.json')).write_text(json.dumps(data,indent=2))
    for kind in ['Diffuse','Rough','nor_gl']:
        formats=data[kind]['2k'];fmt='jpg' if 'jpg' in formats else 'png' if 'png' in formats else 'exr';entry=formats[fmt];path=OUT/entry['url'].rsplit('/',1)[-1]
        if not path.exists() or hashlib.md5(path.read_bytes()).hexdigest()!=entry['md5']:
            r=requests.get(entry['url'],timeout=90);r.raise_for_status();assert hashlib.md5(r.content).hexdigest()==entry['md5'];path.write_bytes(r.content)
        records.append(dict(asset=asset,map=kind,path=path.name,**entry,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),license='CC0',license_url='https://polyhaven.com/license'));print('VERIFIED',path.name,flush=True)
old=json.loads((OUT/'sources.json').read_text());keys={(x['asset'],x['map']) for x in records};old=[x for x in old if (x['asset'],x['map']) not in keys];(OUT/'sources.json').write_text(json.dumps(old+records,indent=2))
