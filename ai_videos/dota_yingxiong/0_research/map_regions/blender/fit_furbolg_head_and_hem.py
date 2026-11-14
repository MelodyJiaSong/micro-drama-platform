"""Correct head scale under the hood and bring the hide's rear hem toward the body."""
from pathlib import Path
import bpy,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r09';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r08/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];body=bpy.data.objects['geometry_0']
def smooth(a,lo,hi):
 t=np.clip((a-lo)/(hi-lo),0,1);return t*t*(3-2*t)
def head(points):
 p=points.copy();w=smooth(-p[:,1],.22,.43)*smooth(p[:,2],1.15,1.40)*(1-smooth(p[:,2],1.72,1.85))*(1-smooth(abs(p[:,0]),.18,.34));target=p.copy();target[:,0]*=1.30;target[:,1]=-.43+(p[:,1]+.43)*1.15-.025;target[:,2]=1.45+(p[:,2]-1.45)*1.32+.17;return p+(target-p)*w[:,None],int((w>.01).sum())
co=np.empty(len(body.data.vertices)*3,np.float32);body.data.vertices.foreach_get('co',co);co,count=head(co.reshape(-1,3));body.data.vertices.foreach_set('co',co.ravel());body.data.update()
hair=bpy.data.objects['Groomed_polar_fur_curves'].data;co=np.empty(len(hair.attributes['position'].data)*3,np.float32);hair.attributes['position'].data.foreach_get('vector',co);co,hair_count=head(co.reshape(-1,3));hair.attributes['position'].data.foreach_set('vector',co.ravel())
def hem(points):
 p=points.copy();v=np.clip((p[:,1]+.51)/1.18,0,1);w=smooth(v,.64,1);p[:,0]*=1-.12*w;p[:,1]-=.11*w;target=.64+.10*(1-np.clip(abs(p[:,0])/.55,0,1));p[:,2]=p[:,2]*(1-w)+target*w;return p
cloth=bpy.data.objects['Continuous_stitched_hide'];co=np.empty(len(cloth.data.vertices)*3,np.float32);cloth.data.vertices.foreach_get('co',co);co=hem(co.reshape(-1,3));cloth.data.vertices.foreach_set('co',co.ravel());cloth.data.update()
for ob in coll.objects:
 if ob.name.startswith(('Raised_hide_panel_seam','Cross_laced_hide_stitch','Cross_hide_panel_seam')):
  for sp in ob.data.splines:
   for p in sp.points:p.co=(*hem(np.array([p.co[:3]],np.float32))[0],p.co.w)
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r09','source':'r08','status':'author_preview_not_accepted','changes':['Raise and enlarge undersized head with continuous weighted deformation shared by skin and groom','Bring flared rear cape hem down toward body'],'head_vertices_affected':count,'hair_points_affected':hair_count,'remaining':['Head anatomy and hood clearance','Rear cape shape and clipping','Author and independent checks']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,2.5);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));scene.render.filepath=str(out/'back_preview.png');bpy.ops.render.render(write_still=True)
