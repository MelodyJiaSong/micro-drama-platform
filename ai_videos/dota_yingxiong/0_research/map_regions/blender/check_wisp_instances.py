"""Render the same collection instance at origin and map coordinates."""
from pathlib import Path
import bpy,numpy as np,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));revision=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'r11';source=folder/revision/'authoring.blend';out=folder/revision/'instance_check';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;asset=bpy.data.collections['ASSET_m306']
for parent in list(bpy.data.collections)+[scene.collection]:
    if asset.name in parent.children:parent.children.unlink(asset)
instance=bpy.data.objects.new('Translated_collection_instance',None);instance.instance_type='COLLECTION';instance.instance_collection=asset;scene.collection.objects.link(instance)
scene.cycles.samples=16;scene.cycles.seed=613;scene.render.resolution_x=384;scene.render.resolution_y=384;scene.camera.data.ortho_scale=.8;scene.camera.location=(1.1,-1.6,1.25);look_at(scene.camera,(0,.05,1));bpy.data.objects['Inspection_10cm_scale_cube'].hide_render=True
outside=[o for o in scene.objects if o!=instance];positions={o.name:o.location.copy() for o in outside};arrays=[]
for label,shift in [('origin',(0,0,0)),('map_position',(128,-96,4))]:
    instance.location=shift
    for ob in outside:ob.location=positions[ob.name]+Vector(shift)
    scene.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True)
    im=bpy.data.images.load(scene.render.filepath,check_existing=False);arr=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(arr);arrays.append(arr.reshape(-1,4)[:,:3]);bpy.data.images.remove(im);print('RENDERED',label,flush=True)
error=arrays[1]-arrays[0];rmse=float(np.sqrt((error**2).mean()));relative=float(abs(arrays[1].mean()-arrays[0].mean())/max(arrays[0].mean(),1e-8));report={'source':str(source),'translations_m':[[0,0,0],[128,-96,4]],'image_rmse':rmse,'mean_radiance_relative_change':relative,'pass':rmse<.025 and relative<.02,'purpose':'Collection placement must not extinguish the local optical fields; appearance QC remains separate'};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if not report['pass']:raise RuntimeError('Translation changed optical output')
