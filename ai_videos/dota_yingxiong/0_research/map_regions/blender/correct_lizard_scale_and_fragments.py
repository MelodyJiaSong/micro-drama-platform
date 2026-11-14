"""Correct the demonstrated length-axis error and remove detached back-arc fragments."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,sys,hashlib
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m26_Thunder_Lizard/model_3d'));out=folder/'r02';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m26_r01.blend'));coll=bpy.data.collections['ASSET_m26'];ob=next(o for o in coll.objects if o.type=='MESH');factor=5/ob.dimensions.x
for o in coll.objects:
 if o.parent is None:o.matrix_world=Matrix.Scale(factor,4)@o.matrix_world
for light in [o for o in bpy.context.scene.objects if o.type=='LIGHT' and o.name not in coll.all_objects]:
 light.location*=factor;light.data.energy*=factor*factor;light.data.size*=factor
bm=bmesh.new();bm.from_mesh(ob.data);original_vertices=len(bm.verts);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.verts.ensure_lookup_table();bm.verts.index_update();seen=set();remove=[];records=[];m=np.array(ob.matrix_world)
for v in bm.verts:
 if v.index in seen:continue
 stack=[v];seen.add(v.index);part=[]
 while stack:
  q=stack.pop();part.append(q)
  for e in q.link_edges:
   n=e.other_vert(q)
   if n.index not in seen:seen.add(n.index);stack.append(n)
 if len(part)>1100:continue
 p=np.array([tuple(q.co) for q in part]);p=p@m[:3,:3].T+m[:3,3];center=p.mean(axis=0)
 if p[:,2].min()>.9 and center[0]<1.3 and abs(center[1])<.46:
  remove.extend(part);records.append({'vertices':len(part),'center_m':center.tolist(),'bounds_m':[p.min(axis=0).tolist(),p.max(axis=0).tolist()]})
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.normal_update();bm.to_mesh(ob.data);bm.free();ob.data.update()
for poly in ob.data.polygons:poly.use_smooth=True
mat=ob.data.materials[0];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');original=bs.inputs['Base Color'].links[0].from_socket
sep=n.new('ShaderNodeSeparateColor');sep.mode='HSV';l.new(original,sep.inputs['Color']);mask=n.new('ShaderNodeMapRange');mask.clamp=True;mask.interpolation_type='SMOOTHSTEP';mask.inputs['From Min'].default_value=.07;mask.inputs['From Max'].default_value=.25;l.new(sep.outputs[1],mask.inputs['Value'])
hue=n.new('ShaderNodeHueSaturation');hue.inputs['Hue'].default_value=.535;hue.inputs['Saturation'].default_value=1.25;hue.inputs['Value'].default_value=.88;l.new(original,hue.inputs['Color']);tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=.55;tint.inputs[2].default_value=(.78,1.08,.66,1);l.new(hue.outputs[0],tint.inputs[1]);mix=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],mix.inputs[0]);l.new(original,mix.inputs[1]);l.new(tint.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],bs.inputs['Base Color'])
scene=bpy.context.scene;scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;bpy.context.view_layer.update();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
calibration=WORLD/'background/map_3d/model_calibration.json'
report={'asset_id':'m26','revision':'r02','source':'r01','status':'author_trial_pending_view','scale_correction':factor,'calibration_basis':{'axis':'X','metres':5,'status':'length_including_tail_verified_from_card_and_views'},'calibration_sha256':hashlib.sha256(calibration.read_bytes()).hexdigest(),'body_dimensions_m':list(ob.dimensions),'removed_high_back_fragments':records,'seam_weld_distance_local':.000001,'original_vertices':original_vertices,'current_vertices':len(ob.data.vertices),'changes':['Uniform correction of mistaken body-width calibration','Remove only small disconnected high back/tail pieces; principal body and head excluded','Selective olive-green skin adjustment while retaining low-saturation ivory'],'electrical_state':'Neutral resting pose: no permanent solid lightning; intermittent animated arcs deferred with animation','remaining':['Inspect green skin versus ivory separation','All views and head detail','No topology acceptance from seam welding alone']}
(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('LIZARD_CORRECTED',json.dumps({'dimensions':list(ob.dimensions),'removed_fragments':len(records)}),flush=True)
for name,loc,target,scale in [('author_preview',(6,-8,4.3),(0,0,1.2),5.8),('side_detail',(0,-9,2.4),(0,0,1.2),5.7),('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
