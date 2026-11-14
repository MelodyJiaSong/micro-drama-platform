"""Move root centre lines without flattening their circular cross sections."""
from pathlib import Path
import bpy,json,math,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r30';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r29/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];names=[o.name for o in coll.objects if not o.hide_render and o.type=='MESH' and o.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root'))];targets=[bpy.data.objects[name] for name in names];mat=bpy.data.materials['Tileable_root_bark_actual_scale']
with bpy.data.libraries.load(str(folder/'r28/authoring.blend'),link=False) as (src,dst):dst.objects=names
def warp(p):
 p=p.copy();t=max(0,min(1,(p.z+.03)/.30));p.z-=.22*t*t*(3-2*t)
 if p.y<-2.25 and abs(p.x)<.86:p.x=math.copysign(.86+(abs(p.x)/.86)*.08,p.x)
 return p
for target,original in zip(targets,dst.objects):
 me=original.data.copy();target.data=me;me.materials.clear();me.materials.append(mat);count=len(me.vertices)//14;centres=[sum((me.vertices[j*14+k].co for k in range(14)),Vector())/14 for j in range(count)];new=[warp(c) for c in centres];factor=.66 if target.name.startswith('Woven_pale_primary_root') else 1
 for j in range(count):
  a,b=max(0,j-1),min(count-1,j+1);old_t=(centres[b]-centres[a]).normalized();new_t=(new[b]-new[a]).normalized();rotation=old_t.rotation_difference(new_t)
  for k in range(14):v=me.vertices[j*14+k];v.co=new[j]+rotation@((v.co-centres[j])*factor)
 me.update();bpy.data.objects.remove(original,do_unlink=True)
for node in mat.node_tree.nodes:
 if node.type=='VALTORGB' and abs(node.color_ramp.elements[1].position-.45)<.001:
  node.color_ramp.elements[0].color=(.10,.09,.065,1);node.color_ramp.elements[1].color=(.42,.38,.29,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r30','source':'r29 with root mesh sections restored from r28','status':'author_preview_not_accepted','diagnosis':'r29 applied height compression to every vertex and visibly flattened root tubes; rejected for integration','changes':['Reposition centre lines and parallel-transport circular root rings','Retain thinner primary roots, source bark UV and branched network','Lighter gray-brown bark; r29 bracket and clear crystal openings retained'],'root_meshes_rebuilt':len(targets),'remaining':['Root shape and grounding author view','Side-view bracket contact','Full independent review']},indent=2),encoding='utf-8')
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
