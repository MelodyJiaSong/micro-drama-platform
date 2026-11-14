"""Keep the enlarged iris behind a convex lid, with a clear physical corneal surface."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
from transfer_uv_in_chunks import transfer_uv
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d'));out=folder/'r15';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r14/authoring.blend'));report=json.loads((folder/'r14/authoring.json').read_text());body=bpy.data.objects['Closed_lizard_surface_3mm'];source=bpy.data.objects['Archive_r07_lizard_before_closed_surface'];coll=bpy.data.collections['ASSET_m26'];material=bpy.data.materials.new('Clear_reptile_cornea');material.use_nodes=True;bs=material.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(1,1,1,1);bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.38;bs.inputs['Roughness'].default_value=.035
for row in report['eye_aperture_repair']:
 side=row['side'];old=next(q for q in report['eyes'] if q['side']==side);center=Vector(row['centre']);normal=Vector(old['normal']);p=Vector(old['surface']);u=(Vector((1,0,0))-normal*normal.x).normalized();v=normal.cross(u)
 if v.z<0:v=-v
 lid=bpy.data.objects[f'Reptile_lid_rim_{side}'];radius=.0389
 for ring in range(5):
  t=ring/4
  for k in range(96):
   a=math.tau*k/96;dx=.030*math.cos(a);dz=.018*math.sin(a);inner=center+u*dx+v*dz+normal*(math.sqrt(radius*radius-dx*dx-dz*dz)+.0012);edge=p+u*(.048*math.cos(a))+v*(.046*math.sin(a));hit,q,nn,face=body.ray_cast(edge+normal*.12,-normal)
   if hit:edge=q-normal*.0004
   point=inner.lerp(edge,t);delta=point-center;x=delta.dot(u);z=delta.dot(v)
   if x*x+z*z<radius*radius:
    minimum=math.sqrt(radius*radius-x*x-z*z)+.0012;point+=normal*max(0,minimum-delta.dot(normal))
   lid.data.vertices[ring*96+k].co=point
 lid.data.update();uvout=out/f'lid_uv_{side}';uvout.mkdir(exist_ok=True);transfer_uv(source,lid,uvout)
 iris=bpy.data.objects[f'Reptile_Iris_{side}'];pigment=iris.data.color_attributes.get('IrisPigment')
 if pigment:
  for item in pigment.data:item.color=(item.color[0]*.70,item.color[1]*.74,item.color[2]*.80,1)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=radius,location=center);cornea=bpy.context.object
 for c in list(cornea.users_collection):c.objects.unlink(cornea)
 coll.objects.link(cornea);cornea.name=f'Reptile_clear_cornea_{side}';cornea.data.materials.append(material)
 for face in cornea.data.polygons:face.use_smooth=True
scene=bpy.context.scene;scene['production_status']='CONVEX_LIDS_CORNEA_TRIAL_OTHER_BLOCKERS_REMAIN';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report.update(revision='r15',source='r14',status='author_trial_pending_view',corneal_lid_repair={'corneal_radius_m':.0389,'ior':1.38,'roughness':.035,'minimum_lid_clearance_m':.0012,'outer_lid_half_width_height_m':[.048,.046],'reason':'Straight interpolation in r14 crossed through the spherical iris, revealing a round button instead of an oval aperture.'});(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('CONVEX_LIDS_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=40;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('head_side',(1.85,-5,1.1),(1.85,0,1.1),1.5),('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
