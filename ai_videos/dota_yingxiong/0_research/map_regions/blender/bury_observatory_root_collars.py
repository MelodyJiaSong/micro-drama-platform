"""Bury the new thick root's start caps inside masonry, preserving the network."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r36';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r35/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];primary=[];count=0
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Woven_pale_primary_root'):continue
 rings=len(ob.data.vertices)//14
 for j in range(rings):
  vertices=[ob.data.vertices[j*14+k] for k in range(14)];center=sum((v.co for v in vertices),Vector())/14;t=j/(rings-1);radial=Vector((center.x,center.y,0)).normalized();target=center-radial*(.26*(1-t)**5);target.z=.45*(1-t)**3+.075*(1-t**5)-.08*t**8
  for v in vertices:v.co+=target-center
  primary.append(target)
 ob.data.update();count+=1
tree=kdtree.KDTree(len(primary))
for i,p in enumerate(primary):tree.insert(p,i)
tree.balance();branches=0
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Connected_crossing_rootlet'):continue
 rings=len(ob.data.vertices)//14;origin=sum((ob.data.vertices[k].co for k in range(14)),Vector())/14;nearest=primary[tree.find(origin)[1]];delta=nearest-origin
 for j in range(rings):
  t=j/(rings-1)
  for k in range(14):ob.data.vertices[j*14+k].co+=delta*(1-t)**2
 ob.data.update();branches+=1
scene=bpy.context.scene;scene['production_status']='ROOT_COLLAR_CONTACT_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r35/authoring.json').read_text());report.update(revision='r36',source='r35',root_collar_fix={'primary_roots':count,'connected_branches':branches,'start_recess_parent_m':.26,'initial_centre_height_parent_m':.525,'reason':'r35 exposed thick start caps above the plinth, creating stumps; recess these into the host masonry and reconnect branch origins'},remaining=['Root emergence and ground contact','All r34 material/structure blockers need independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
