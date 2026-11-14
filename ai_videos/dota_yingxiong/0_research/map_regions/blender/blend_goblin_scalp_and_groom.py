"""Fit the scalp overlap to surviving skin and grow sparse rear hair on its surface."""
from pathlib import Path
import bpy,json,numpy as np,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'));out=folder/'r06';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r05/authoring.blend'));coll=bpy.data.collections['ASSET_m309'];body=bpy.data.objects['Goblin_merchant_body'];patch=bpy.data.objects['Measured_reconstructed_rear_scalp']
with bpy.data.libraries.load(str(folder/'r03/authoring.blend'),link=False) as (src,dst):dst.objects=['Goblin_merchant_body']
original=dst.objects[0];bpy.context.scene.collection.objects.link(original);original.hide_render=True;bpy.context.view_layer.update()
changed=0
for v in patch.data.vertices:
 x,y,z=v.co;ell=((x+.003)/.085)**2+((z-.875)/.065)**2
 if ell<.55:continue
 hit,p,n,index=original.ray_cast(Vector((x,1,z)),Vector((0,-1,0)))
 if hit and p.y>.025 and n.y>.1:
  t=min(1,max(0,(ell-.55)/.40));t=t*t*(3-2*t);v.co.y=y*(1-t)+(p.y-.00003)*t;changed+=1
patch.data.update();bpy.data.objects.remove(original,do_unlink=True)
old=bpy.data.objects.get('Sparse_gray_black_goblin_hair')
if old:old.hide_render=True;old.hide_viewport=True
rng=np.random.default_rng(30906);strands=[]
for _ in range(28000):
 x=float(rng.uniform(-.09,.09));z=float(rng.uniform(.79,.932));ellipse=((x+.003)/.088)**2+((z-.865)/.072)**2
 if ellipse>1:continue
 density=.95 if z<.90 or abs(x)>.04 else .35
 if rng.random()>density:continue
 hits=[]
 for surface in [body,patch]:
  hit,p,n,index=surface.ray_cast(Vector((x,1,z)),Vector((0,-1,0)))
  if hit and p.y>.025 and n.y>.12:hits.append((p.copy(),n.copy()))
 if not hits:continue
 p,n=max(hits,key=lambda q:q[0].y);length=float(rng.uniform(.025,.068));side=float(rng.uniform(-.009,.009));points=[]
 for t in map(float,np.linspace(0,1,7)):
  points.append(p+n*(.00012+.004*math.sin(math.pi*t*.9))+Vector((side*t,.002*t,-length*t*t)))
 strands.append(points)
curves=bpy.data.hair_curves.new('Rear_hair_on_reconstructed_scalp');curves.add_curves([7]*len(strands));curves.set_types(type='CATMULL_ROM');curves.attributes['position'].data.foreach_set('vector',np.array(strands,np.float32).ravel());radius=curves.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',(rng.uniform(.000025,.000045,len(strands))[:,None]*np.array([1,.95,.87,.73,.53,.28,.02])).astype(np.float32).ravel());ob=bpy.data.objects.new(curves.name,curves);coll.objects.link(ob)
mat=bpy.data.materials.new('Natural_gray_black_rear_hair');mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.013,.016,.013,1);bs.inputs['Roughness'].default_value=.6;bs.inputs['Specular IOR Level'].default_value=.22;curves.materials.append(mat)
scene=bpy.context.scene;scene['production_status']='REAR_SCALP_BLEND_AND_GROOM_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r05/authoring.json').read_text());report.update(revision='r06',source='r05',status='author_trial_pending_view',scalp_edge_vertices_fitted=changed,new_rear_hair_strands=len(strands),remaining=['Scalp overlap seam','Natural sparse hair silhouette','Front face and cloth holes remain','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SCALP_BLEND_SAVED',changed,len(strands),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('back_detail',(0,2,.85),(0,0,.85),.36),('back_side',(1.4,2,.86),(0,0,.85),.40),('author_preview',(2.5,-4,1.8),(0,0,.475),1.23)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
