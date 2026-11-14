"""Normalize measured material regions, discard detached hair debris and add sparse strands."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m309_*/model_3d'));out=folder/'r03';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r02/authoring.blend'));body=bpy.data.objects['Goblin_merchant_body'];me=body.data;coll=bpy.data.collections['ASSET_m309'];co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);indices=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',indices);x,y,z=co[indices].T
def smooth(v,lo,hi):t=np.clip((v-lo)/(hi-lo),0,1);return t*t*(3-2*t)
def readmask(name):a=np.empty(len(me.loops),np.float32);me.attributes[name].data.foreach_get('value',a);return a
skin=readmask('Goblin_skin');scalp=smooth(z,.86,.89)*(1-smooth(np.abs(x),.075,.09))*(1-smooth(y,.025,.06));skin=np.maximum(skin,scalp);me.attributes['Goblin_skin'].data.foreach_set('value',skin)
coat=readmask('Goblin_coat');back=smooth(y,.005,.025)*smooth(z,.47,.50)*(1-smooth(z,.71,.745));coat=np.maximum(coat,back);me.attributes['Goblin_coat'].data.foreach_set('value',coat)
eye=np.zeros(len(me.loops),np.float32)
for cx,cz,rx,rz in [(-.019,.849,.011,.006),(.056,.862,.010,.007)]:
 d=np.sqrt(((x-cx)/rx)**2+((z-cz)/rz)**2);eye=np.maximum(eye,(1-smooth(d,.75,1.05))*(y<0))
me.attributes.new('Goblin_eye_region','FLOAT','CORNER').data.foreach_set('value',eye)
for mat in me.materials:
 nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');tex=next(q for q in n if q.type=='TEX_IMAGE' and q.image and q.image.colorspace_settings.name=='sRGB');source=tex.outputs['Color'];gray=n.new('ShaderNodeRGBToBW');l.new(source,gray.inputs[0]);color=source
 for attrname,dark,light,lo,hi in [('Goblin_skin',(.040,.046,.014,1),(.17,.19,.065,1),.01,.30),('Goblin_coat',(.006,.003,.010,1),(.050,.023,.070,1),.004,.15),('Goblin_trim',(.05,.028,.006,1),(.30,.19,.045,1),.015,.35),('Goblin_hair',(.004,.005,.004,1),(.025,.028,.024,1),.01,.5)]:
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=lo;ramp.color_ramp.elements[0].color=dark;ramp.color_ramp.elements[1].position=hi;ramp.color_ramp.elements[1].color=light;l.new(gray.outputs[0],ramp.inputs[0]);a=n.new('ShaderNodeAttribute');a.attribute_name=attrname;mix=n.new('ShaderNodeMixRGB');l.new(a.outputs['Fac'],mix.inputs[0]);l.new(color,mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2]);color=mix.outputs[0]
 a=n.new('ShaderNodeAttribute');a.attribute_name='Goblin_eye_region';bright=n.new('ShaderNodeMapRange');bright.clamp=True;bright.inputs['From Min'].default_value=.015;bright.inputs['From Max'].default_value=.07;l.new(gray.outputs[0],bright.inputs[0]);mask=n.new('ShaderNodeMath');mask.operation='MULTIPLY';l.new(a.outputs['Fac'],mask.inputs[0]);l.new(bright.outputs[0],mask.inputs[1]);mix=n.new('ShaderNodeMixRGB');mix.blend_type='COLOR';mix.inputs[2].default_value=(.30,.25,.045,1);l.new(mask.outputs[0],mix.inputs[0]);l.new(color,mix.inputs[1]);l.new(mix.outputs[0],bs.inputs['Base Color'])
 hair=n.new('ShaderNodeAttribute');hair.attribute_name='Goblin_hair';inverse=n.new('ShaderNodeMath');inverse.operation='SUBTRACT';inverse.inputs[0].default_value=1;l.new(hair.outputs['Fac'],inverse.inputs[1]);metal=bs.inputs['Metallic'].links[0].from_socket;mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(metal,mul.inputs[0]);l.new(inverse.outputs[0],mul.inputs[1]);l.new(mul.outputs[0],bs.inputs['Metallic']);spec=n.new('ShaderNodeMapRange');spec.inputs['To Min'].default_value=.18;spec.inputs['To Max'].default_value=.03;l.new(hair.outputs['Fac'],spec.inputs[0]);l.new(spec.outputs[0],bs.inputs['Specular IOR Level'])
bm=bmesh.new();bm.from_mesh(me);before=len(bm.verts);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);hair_layer=bm.loops.layers.float.get('Goblin_hair');remaining=set(bm.verts);deleted=[];components=0
while remaining:
 start=remaining.pop();stack=[start];part=[start]
 while stack:
  for edge in stack.pop().link_edges:
   for v in edge.verts:
    if v in remaining:remaining.remove(v);stack.append(v);part.append(v)
 components+=1
 if len(part)>2400:continue
 points=np.array([tuple(v.co) for v in part]);centre=points.mean(0)
 if centre[2]<.72 or centre[1]<-.025 or np.ptp(points,axis=0).max()>.08:continue
 faces={f for v in part for f in v.link_faces};values=[loop[hair_layer] for f in faces for loop in f.loops]
 if values and float(np.mean(values))>.35:deleted.extend(part)
removed=len(deleted)
if deleted:bmesh.ops.delete(bm,geom=deleted,context='VERTS')
after=len(bm.verts);bm.normal_update();bm.to_mesh(me);bm.free();me.update();print('HAIR_FRAGMENT_CLEANUP',before,after,removed,flush=True)
rng=np.random.default_rng(30903);strands=[]
for _ in range(2400):
 x=float(rng.choice([-1,1])*rng.uniform(.025,.075));z=float(rng.uniform(.78,.89));hit,p,normal,index=body.ray_cast(Vector((x,1,z)),Vector((0,-1,0)))
 if not hit or p.y<.015 or normal.y<.15:continue
 length=float(rng.uniform(.025,.065));side=float(rng.uniform(-.008,.008));points=[]
 for t in np.linspace(0,1,6):points.append(p+normal*(.0002+.008*math.sin(t*math.pi*.85))+Vector((side*t,.006*t,-length*t*t)))
 strands.append(points)
curves=bpy.data.hair_curves.new('Sparse_gray_black_goblin_hair');curves.add_curves([6]*len(strands));curves.set_types(type='CATMULL_ROM');curves.attributes['position'].data.foreach_set('vector',np.array(strands,np.float32).ravel());radius=curves.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',(rng.uniform(.000018,.000034,len(strands))[:,None]*np.array([1,.9,.8,.6,.35,.02])).astype(np.float32).ravel());ob=bpy.data.objects.new('Sparse_gray_black_goblin_hair',curves);coll.objects.link(ob);mat=bpy.data.materials.new('Goblin_hair_dielectric');mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.010,.012,.009,1);bs.inputs['Roughness'].default_value=.68;bs.inputs['Specular IOR Level'].default_value=.12;curves.materials.append(mat)
scene=bpy.context.scene;scene['production_status']='GOBLIN_PALETTE_AND_HAIR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r02/authoring.json').read_text());report.update(revision='r03',source='r02',status='author_trial_pending_view',geometry_changed=True,hair_cleanup={'weld_distance_m':1e-6,'vertices_before_weld':before,'vertices_after_cleanup':after,'removed_detached_hair_vertices':removed,'components_after_weld':components,'new_strands':len(strands)},palette='World-aware scalp and back masks plus controlled linear albedo ranges; dark violet cloth, grey-black hair, local gold-yellow eye hue',remaining=['Mask transitions and uncovered skin patches','Remaining attached scan hair','Groom roots and eye colour','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('author_preview',(2.5,-4,1.8),(0,0,.475),1.23),('face_detail',(0,-2,.82),(0,0,.82),.42),('back_detail',(0,2,.79),(0,0,.79),.48)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
