"""Separate bristles and enamel, calibrate shoulders and ground the four limbs."""
from pathlib import Path
import bpy,json,numpy as np,random,hashlib,sys,math
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='m4');folder=ROOT/a['model_directory'];out=folder/'r06/inspection';out.mkdir(parents=True,exist_ok=True);dest=out/'m4_r06.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/inspection/m4_r04.blend'));coll=bpy.data.collections['ASSET_m4'];obj=next(o for o in coll.objects if o.type=='MESH');me=obj.data;me.transform(obj.matrix_world);obj.matrix_world=Matrix.Identity(4)
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)
mat=me.materials[0];bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');img=bs.inputs['Base Color'].links[0].from_node.image;w,h=img.size;pixels=np.empty(w*h*4,np.float32);img.pixels.foreach_get(pixels);pixels=pixels.reshape(h,w,4);rgb=pixels[np.clip((uv[:,1]*h).astype(int),0,h-1),np.clip((uv[:,0]*w).astype(int),0,w-1),:3];co=v[loops]
hair_mask=(rgb[:,0]<.20)&(np.abs(co[:,0])<.18)&(co[:,2]>.78)&(co[:,2]<1.21)&(co[:,1]<-.10)&((np.abs(co[:,0])>.075)|(co[:,2]>.90))
teeth_mask=(np.abs(co[:,0])<.08)&(co[:,1]<-.40)&(co[:,2]>.735)&(co[:,2]<.795)&(rgb[:,2]<rgb[:,0]*.48)&(rgb[:,0]>.20)
hair=material('Black_coarse_bristles',(.006,.004,.0028),.48);me.materials.append(hair)
enamel=mat.copy();enamel.name='Aged_yellow_white_enamel';nt=enamel.node_tree;eb=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');src=eb.inputs['Base Color'].links[0].from_socket;hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.22;hue.inputs['Value'].default_value=1.08;nt.links.new(src,hue.inputs['Color']);nt.links.new(hue.outputs[0],eb.inputs['Base Color']);eb.inputs['Roughness'].default_value=.32;me.materials.append(enamel)
labels=np.zeros(len(me.polygons),np.int32);hair_faces=hair_mask.reshape(-1,3).sum(1)>=2;tooth_faces=teeth_mask.reshape(-1,3).sum(1)>=2;labels[hair_faces]=1;labels[tooth_faces]=2;me.polygons.foreach_set('material_index',labels)
nt=mat.node_tree;src=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[0].default_value=.12;mix.inputs[2].default_value=(.27,.20,.13,1);nt.links.new(src,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
contact=[]
for side in [-1,1]:
    for end in ['front','rear']:
        region=(v[:,0]*side>0)&(v[:,2]<.2)&((v[:,1]<-.07) if end=='front' else (v[:,1]>.08));delta=float(v[region,2].min());contact.append({'side':side,'limb':end,'lowered_m':delta});zweight=np.clip((.45-v[:,2])/.22,0,1);zweight=zweight*zweight*(3-2*zweight);yweight=np.clip((-.02-v[:,1])/.1,0,1) if end=='front' else np.clip((v[:,1]-.02)/.1,0,1);v[:,2]-=delta*zweight*yweight*(v[:,0]*side>0)
shoulder=(np.abs(v[:,0])>.15)&(np.abs(v[:,0])<.29)&(v[:,1]>-.08)&(v[:,1]<.08)&(v[:,2]>.9)
landmark=float(np.quantile(v[shoulder,2],.90));scale=1.3/landmark;v*=scale;me.vertices.foreach_set('co',v.ravel());me.update()
hair_vertices=np.unique(loops[hair_mask]);rng=random.Random(405);normals=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('normal',normals);normals=normals.reshape(-1,3);cu=bpy.data.curves.new('Individual_black_bristles','CURVE');cu.dimensions='3D';cu.bevel_depth=.00032;cu.bevel_resolution=1;cu.materials.append(hair)
for i in range(14000):
    idx=int(hair_vertices[rng.randrange(len(hair_vertices))]);root=Vector(v[idx]);normal=Vector(normals[idx]);flow=(normal*.6+Vector((rng.uniform(-.2,.2),.35,rng.uniform(.45,.85)))).normalized();length=rng.uniform(.025,.065);s=cu.splines.new('POLY');s.points.add(6)
    for j,p in enumerate(s.points):
        t=j/6;point=root+normal*.0005+flow*length*t+Vector((math.sin(t*4+i)*.003*t,0,-.01*t*t));p.co=(*point,1);p.radius=max(.05,1-t)
ob=bpy.data.objects.new('Black_bristle_hair',cu);coll.objects.link(ob)
scene=bpy.context.scene;scene.cycles.samples=32;bpy.data.objects['Studio_floor'].location.z=0;camera=scene.camera;camera.data.ortho_scale=1.3*scale*1.28
for name,x,y,z in [('south',0,-1,.22),('east',1,0,.22),('north',0,1,.22),('west',-1,0,.22),('perspective',1,-1,.7)]:
    camera.location=(x*4.5,y*4.5,.72+z*1.5);look_at(camera,(0,0,.72));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'asset_id':'m4','revision':'r05','source':'m4_r04 with separate hair and enamel, grounded limbs','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'status':'candidate_not_reviewed','shoulder_height_m':1.3,'shoulder_landmark_method':'90th percentile of bilateral shoulder patch, excluding central spine and head','shoulder_original_m':landmark,'uniform_scale':scale,'limb_contacts':contact,'black_bristles':14000,'hair_faces':int(hair_faces.sum()),'tooth_faces':int(tooth_faces.sum()),'design_resolution':'Claw count follows the existing front/side/back image designs supplied for this task; prose card count of three conflicts with the images. Preserve the established visible design, no hero or animation scope added.','views':['south.png','east.png','north.png','west.png','perspective.png']};(out/'inspection.json').write_text(json.dumps(report,indent=2));print('SAVED',dest,flush=True)
