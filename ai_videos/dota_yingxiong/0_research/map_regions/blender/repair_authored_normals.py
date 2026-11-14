"""Preserve authored parts and correct only detected imported custom normals."""
from pathlib import Path
import bpy,numpy as np,json,argparse,sys,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('asset');p.add_argument('--source',required=True);p.add_argument('--revision',required=True);p.add_argument('--authoring-source',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));manifest=json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'));asset=next(a for a in manifest['assets'] if a['id']==args.asset);folder=ROOT/asset['model_directory'];source=folder/args.source/'inspection'/f'{args.asset}_{args.source}.blend';out=folder/args.revision;out.mkdir(exist_ok=True)
if args.authoring_source:source=folder/args.source/'authoring.blend'
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_'+args.asset];records=[]
for ob in coll.all_objects:
    if ob.hide_render or ob.type!='MESH' or not ob.data.has_custom_normals:continue
    me=ob.data
    # Ignore tiny decoration meshes; the diagnosis concerns dense imported meshes.
    if len(me.polygons)<1000:continue
    normals=np.empty(len(me.loops)*3,np.float32);me.corner_normals.foreach_get('vector',normals);normals=normals.reshape(-1,3)
    starts=np.empty(len(me.polygons),np.int32);me.polygons.foreach_get('loop_start',starts);face=np.empty(len(me.polygons)*3,np.float32);me.polygons.foreach_get('normal',face);face=face.reshape(-1,3)
    vn=normals[starts];rotation=vn[:,[0,2,1]]*np.array([1,-1,1]);original=float(np.median(np.sum(face*vn,1)));corrected=float(np.median(np.sum(face*rotation,1)));row={'object':ob.name,'faces':len(me.polygons),'original_median_dot':original,'rotated_median_dot':corrected,'applied':False}
    if original<.85 and corrected>.94:
        fixed=normals[:,[0,2,1]]*np.array([1,-1,1],np.float32);me.normals_split_custom_set(fixed);me.update();row['applied']=True
    records.append(row)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900
if args.asset=='m300':scene.camera.data.ortho_scale=1.73;scene.camera.location=(4.05,-4.05,1.62);look_at(scene.camera,(0,0,.675))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report={'revision':args.revision,'status':'author_preview_pending','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'repairs':records,'normal_repair_applied':any(r['applied'] for r in records),'positions_and_materials_preserved':True,'reason':'Detected exporter extra normal rotation, retained original custom smoothing' if any(r['applied'] for r in records) else 'No matching imported custom-normal defect; authored geometry preserved and re-inspected'}
(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene.render.filepath=str(out/'normal_corrected_preview.png');bpy.ops.render.render(write_still=True)
