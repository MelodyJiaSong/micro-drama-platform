"""Give newly constructed socket stones physical-scale UVs for existing scanned materials."""
from pathlib import Path
import bpy,json,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r49';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r48/authoring.blend'));rng=random.Random(2349);count=0
for ob in bpy.data.collections['ASSET_bg23'].objects:
 if not ob.name.startswith(('Fitted_stone_crystal_socket','Recessed_quartz_stone_bedding')):continue
 mesh=ob.data;uv=mesh.uv_layers.new(name='Socket_stone_metres');offset=(rng.uniform(-20,20),rng.uniform(-20,20))
 for face in mesh.polygons:
  axis=max(range(3),key=lambda i:abs(face.normal[i]));a,b=[(1,2),(0,2),(0,1)][axis]
  for li in face.loop_indices:
   point=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(point[a]+offset[0],point[b]+offset[1])
 count+=1
scene=bpy.context.scene;scene['production_status']='SOCKET_STONE_UV_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r48/authoring.json').read_text());report.update(revision='r49',source='r48',status='author_trial_pending_view',socket_uv_repair={'meshes':count,'mapping':'Dominant face-plane projection in parent-space metres, independent random offsets as used by existing masonry.','reason':'New r48 socket meshes had no UVs, sampling a single point of the scanned stone texture.'});(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SOCKET_UV_SAVED',count,flush=True)
scene.cycles.device='CPU';scene.cycles.samples=40;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
