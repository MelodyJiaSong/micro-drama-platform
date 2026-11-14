"""Inspect the accepted wisp in the actual map, without altering the map file."""
from pathlib import Path
import bpy,sys,json,argparse,hashlib
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';source=OUT/args.blend
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
slots=[o for o in scene.objects if o.get('asset_id')=='m306' and o.instance_collection]
if not slots:raise RuntimeError('Map does not contain a wisp merchant')
slot=min(slots,key=lambda o:o.location.x);bpy.context.view_layer.update();mat=slot.matrix_world.copy()
data=bpy.data.cameras.new('Wisp_map_integration_camera');camera=bpy.data.objects.new(data.name,data);scene.collection.objects.link(camera);scene.camera=camera;data.lens=48;data.clip_start=.02;data.clip_end=3000
camera.location=mat@Vector((1.1,-2,1.55));look_at(camera,mat@Vector((0,.05,.62)))
scene.cycles.device='CPU';scene.cycles.samples=96;scene.cycles.use_denoising=False;scene.cycles.transparent_max_bounces=64;scene.render.resolution_x=1000;scene.render.resolution_y=1000
prefix=Path(args.blend).stem+'_Wisp_Integration';scene.render.filepath=str(OUT/(prefix+'_Day.png'));bpy.ops.render.render(write_still=True)
report={'map':args.blend,'map_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'asset_instance':slot.name,'asset_source':slot.instance_collection.library.filepath if slot.instance_collection.library else None,'position':list(slot.location),'samples':96,'denoising':False,'status':'rendered_pending_visual_inspection','saved_map_modified':False}
(OUT/(prefix+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
