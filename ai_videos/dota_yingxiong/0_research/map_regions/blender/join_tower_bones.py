"""Join structural ribs inside measured upper tusks and define metal plate joints."""
from pathlib import Path
import bpy,json,math,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r11';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r10/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];body=max((o for o in coll.objects if o.type=='MESH' and not o.name.startswith('Scanned_skull')),key=lambda o:len(o.data.polygons));me=body.data
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);bone_index=next(i for i,m in enumerate(me.materials) if m.name=='Tower_weathered_ivory_bone');indices=set()
for p in me.polygons:
 if p.material_index==bone_index:
  for i in p.vertices:
   if 8.45<v[i,2]<8.85:indices.add(i)
selected=v[list(indices)];angles=np.arctan2(selected[:,1],selected[:,0]);centers=np.arange(8)*math.tau/8+math.pi/8
for _ in range(20):
 labels=np.abs(np.angle(np.exp(1j*(angles[:,None]-centers[None,:])))).argmin(1)
 for i in range(8):
  if np.any(labels==i):centers[i]=np.angle(np.exp(1j*angles[labels==i]).mean())
bone_roots=[Vector(selected[labels==i].mean(0)) for i in range(8) if np.any(labels==i)]
def radius(d,z):
 hit,pos,normal,face=body.ray_cast(d*15+Vector((0,0,z)),-d)
 if not hit:raise RuntimeError('Missing wall at '+str(z))
 return math.hypot(pos.x,pos.y)
for ob in list(coll.objects):
 if ob.name.startswith('Continuous_structural_bronze_rib'):
  points=ob.data.splines[0].bezier_points;root=min(bone_roots,key=lambda p:(p-points[-1].co).length);points[-1].co=root+Vector((0,0,.12));points[-1].radius=.95
 elif ob.name.startswith('Large_outward_basal_bone_claw'):
  points=ob.data.splines[0].bezier_points;d=Vector((points[0].co.x,points[0].co.y,0)).normalized()
  for p,z,offset in zip(points,[1.48,.98,.36,.10],[.19,.30,.36,.75]):p.co=d*(radius(d,max(z,.32))+offset)+Vector((0,0,z))
 elif ob.name.startswith('Bronze_rib_retaining_cuff'):bpy.data.objects.remove(ob,do_unlink=True)
mat=bpy.data.materials['Continuous_dark_bronze_sheath'];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.68
old=bs.inputs['Base Color'].links[0].from_socket;mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.27,.32,.30,1);nt.links.new(old,mul.inputs[1]);nt.links.new(mul.outputs[0],bs.inputs['Base Color'])
joint=bpy.data.materials.new('Recessed_metal_plate_seam');joint.use_nodes=True;p=joint.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.009,.008,.01,1);p.inputs['Roughness'].default_value=.86
count=0
for z in [1.65,3.30,4.95,6.40]:
 for segment in range(32):
  lo=segment*math.tau/32;hi=(segment+1)*math.tau/32;mid=(lo+hi)/2
  if min(abs(math.atan2(math.sin(mid-(math.pi/8+k*math.pi/2)),math.cos(mid-(math.pi/8+k*math.pi/2)))) for k in range(4))<.17:continue
  coords=[]
  for a in np.linspace(lo,hi,9):
   d=Vector((math.cos(a),math.sin(a),0));coords.append(d*(radius(d,z)+.008)+Vector((0,0,z)))
  cu=bpy.data.curves.new('Horizontal_panel_joint','CURVE');cu.dimensions='3D';cu.bevel_depth=.012;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(len(coords)-1)
  for point,co in zip(sp.points,coords):point.co=(*co,1)
  ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob);cu.materials.append(joint);count+=1
scene=bpy.context.scene;scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'bg26','revision':'r11','source':'r10','status':'author_preview_not_accepted','changes':['Ribs terminate inside measured tusk roots','Removed misplaced extra cuffs','Basal claws placed outside measured wall','Dark weathered structural bronze','Horizontal plate joints with stair gaps'],'upper_tusk_root_centers':[list(v) for v in bone_roots],'panel_joint_segments':count,'remaining':['Visual continuity and stair detail','Full independent review']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'tower_preview.png');bpy.ops.render.render(write_still=True)
