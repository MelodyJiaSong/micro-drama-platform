"""Make a new map file whose external asset references resolve to tested preview LODs."""
from pathlib import Path
import bpy,json,hashlib,argparse,sys
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
p=argparse.ArgumentParser();p.add_argument('--version',default='overview_v001');p.add_argument('--output',default='assembly_working_v022_lod_v001.blend');args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);dest=OUT/args.output
if dest.exists():raise FileExistsError(dest)
report=json.loads((OUT/'assembly_working_v022_report.json').read_text(encoding='utf-8'));replacements={};evidence={}
for aid,relative in report['source_libraries'].items():
 original=(ROOT/relative).resolve();folder=OUT/'lod_libraries'/args.version/aid;record=json.loads((folder/'lod_report.json').read_text());target=folder/(aid+'.blend')
 if hashlib.sha256(original.read_bytes()).hexdigest()!=record['source_sha256']:raise ValueError(('Changed original source',aid))
 if hashlib.sha256(target.read_bytes()).hexdigest()!=record['output_sha256']:raise ValueError(('Changed LOD file',aid))
 check_path=folder/'comparison_author_check.json'
 check=json.loads(check_path.read_text(encoding='utf-8')) if check_path.exists() else {}
 if record['changes'] and check.get('status')!='usable_for_map_preview':
  # A failed preview may keep the intact source for this family. Never trade
  # a visible texture/silhouette failure for a lower face count.
  target=original;record=dict(record);record.update(output=str(original),output_sha256=record['source_sha256'],visible_unique_faces_after=record['visible_unique_faces_before'],lod_fallback='Original retained: visual comparison rejected or not yet reviewed')
 replacements[str(original).casefold()]=target;evidence[aid]=record
bpy.ops.wm.open_mainfile(filepath=str(OUT/'assembly_working_v022.blend'));changed=[]
for library in bpy.data.libraries:
 path=Path(bpy.path.abspath(library.filepath)).resolve();key=str(path).casefold()
 if key not in replacements:continue
 library.filepath=str(replacements[key]);changed.append(key)
missing=set(replacements)-set(changed)
coverage=json.loads((OUT/'assembly_working_v022_asset_coverage.json').read_text(encoding='utf-8'))
unused={row['asset'] for row in coverage['not_currently_instanced']}
allowed_missing={str((ROOT/report['source_libraries'][aid]).resolve()).casefold() for aid in unused}
if missing-allowed_missing:raise ValueError(('Instanced library remap incomplete',missing-allowed_missing))
for ob in bpy.context.scene.objects:
 if ob.instance_collection and ob.instance_collection.name in {'ASSET_'+aid for aid in unused}:
  raise ValueError(('Coverage audit no longer matches scene',ob.name))
report['unloaded_alternative_families']=[aid for aid in unused if str((ROOT/report['source_libraries'][aid]).resolve()).casefold() in missing]
# Do not render in this process: existing in-memory meshes are still the high
# versions. Reopening the saved file loads the low-resolution external IDs.
bpy.context.scene['production_status']='MAP_PREVIEW_LOD_NOT_RELEASED_REOPEN_REQUIRED';bpy.ops.wm.save_as_mainfile(filepath=str(dest),relative_remap=True)
report.update(file=dest.name,status='MAP_PREVIEW_LOD_NOT_RELEASED',high_resolution_source_libraries=report['source_libraries'],source_libraries={aid:str(Path(row['output']).relative_to(ROOT)) for aid,row in evidence.items()},lod_evidence={aid:{k:row[k] for k in ['source_sha256','output_sha256','visible_unique_faces_before','visible_unique_faces_after']} for aid,row in evidence.items()},lod_limitations=['Separate working preview only; high-detail source files are unchanged.','Must reopen before rendering or measuring actual LOD geometry.','Close asset quality acceptance remains attached to original sources.'])
(OUT/(dest.stem+'_report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('LOD_MAP_SAVED_REOPEN_REQUIRED',dest,flush=True)
