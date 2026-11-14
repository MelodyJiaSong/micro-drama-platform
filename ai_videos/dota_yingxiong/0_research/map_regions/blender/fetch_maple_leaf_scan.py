from pathlib import Path
import requests,json,hashlib,zipfile,datetime
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/environment_sources';dest=OUT/'LeafSet027';dest.mkdir(exist_ok=True)
asset=next(a for a in json.loads((OUT/'leaf_catalog_ambientcg.json').read_text())['foundAssets'] if a['assetId']=='LeafSet027');entry=next(d for d in asset['downloadFolders']['default']['downloadFiletypeCategories']['zip']['downloads'] if d['attribute']=='4K-PNG')
assert 'CC0' in (OUT/'ambientcg_license.html').read_text(encoding='utf-8')
archive=dest/entry['fileName']
if not archive.exists():
 response=requests.get(entry['downloadLink'],timeout=(20,120));response.raise_for_status();assert len(response.content)==entry['size'];archive.write_bytes(response.content)
assert archive.stat().st_size==entry['size']
with zipfile.ZipFile(archive) as z:
 for name in z.namelist():
  target=(dest/name).resolve();assert target.is_relative_to(dest.resolve()),name
 z.extractall(dest)
record={'at':datetime.datetime.now().astimezone().isoformat(),'source':asset['shortLink'],'asset':'LeafSet027','license':'CC0','license_url':'https://docs.ambientcg.com/license/','download':entry,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in dest.iterdir() if p.is_file() and p!=archive]}
(dest/'provenance.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({'asset':'LeafSet027','files':[p['name'] for p in record['files']]}),flush=True)
