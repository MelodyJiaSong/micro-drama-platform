"""Measured side-profile eye anatomy and enclosed dark mouth trial."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d'));out=folder/'r10';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/authoring.blend'));body=bpy.data.objects['Closed_lizard_surface_3mm'];coll=bpy.data.collections['ASSET_m26'];me=body.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
def material(name,color,rough):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Specular IOR Level'].default_value=.25;return mat
outer=material('Reptile_dark_ochre_eye',(.045,.021,.004),.20);iris=material('Golden_radial_reptile_iris',(.32,.17,.018),.23);pupil=material('Reptile_vertical_pupil',(.001,.0006,.0002),.12);oral=material('Recessed_dark_red_oral_mucosa',(.055,.006,.004),.38)
nt=iris.node_tree;bs=nt.nodes.get('Principled BSDF');attr=nt.nodes.new('ShaderNodeVertexColor');attr.layer_name='IrisPigment';nt.links.new(attr.outputs[0],bs.inputs['Base Color']);bs.inputs['Coat Weight'].default_value=.25;bs.inputs['Coat Roughness'].default_value=.08
def move(ob):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob)
eyes=[];deforms=[]
for side in [-1,1]:
 hit,p,n,index=body.ray_cast(Vector((1.95,side*3,.978)),Vector((0,-side,0)));assert hit
 # The small ochre remnant below the brow in the profile diagnostic identifies
 # the eye; the large opening ahead of it is the nostril and remains untouched.
 normal=Vector((.40,side*.915,.045)).normalized();u=(Vector((1,0,0))-normal*normal.x).normalized();v=normal.cross(u)
 if v.z<0:v=-v
 radius=.026;centre=p-normal*.018;deforms.append((p.copy(),normal,u,v))
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=radius,location=centre);eye=bpy.context.object;move(eye);eye.name=f'Reptile_eye_{side}';eye.data.materials.append(outer)
 for f in eye.data.polygons:f.use_smooth=True
 for kind,rx,rz,mat in [('Iris',.019,.019,iris),('Pupil',.0027,.011,pupil)]:
  vv=[tuple(centre+normal*(radius+.00008))];ff=[];colors=[(.32,.17,.018,1)];rng=np.random.default_rng(26100+side);radial=rng.uniform(.45,1.4,96)
  for ring in range(1,9):
   t=ring/8
   for k in range(96):
    angle=math.tau*k/96;dx=rx*t*math.cos(angle);dz=rz*t*math.sin(angle);depth=math.sqrt(max(0,radius*radius-dx*dx-dz*dz))+.0001+(.00008 if kind=='Pupil' else 0);vv.append(tuple(centre+u*dx+v*dz+normal*depth));a=radial[k]*(.25 if ring==8 else 1);colors.append((.36*a,.20*a,.022*a,1))
  for k in range(96):ff.append((0,k+1,(k+1)%96+1))
  for ring in range(7):
   for k in range(96):ff.append((1+ring*96+k,1+ring*96+(k+1)%96,1+(ring+1)*96+(k+1)%96,1+(ring+1)*96+k))
  mesh=bpy.data.meshes.new(f'{kind}_{side}');mesh.from_pydata(vv,[],ff);ob=bpy.data.objects.new(f'Reptile_{kind}_{side}',mesh);coll.objects.link(ob);mesh.materials.append(mat)
  for f in mesh.polygons:f.use_smooth=True
  if kind=='Iris':a=mesh.color_attributes.new(name='IrisPigment',type='FLOAT_COLOR',domain='POINT');a.data.foreach_set('color',np.array(colors,np.float32).ravel())
 # Short tapered skin rims follow existing surrounding face and the actual
 # spherical eye. Vertex colour transfer avoids inventing UV atlas coordinates.
 vv=[];ff=[]
 for ring in range(5):
  t=ring/4
  for k in range(96):
   a=math.tau*k/96;dx=.021*math.cos(a);dz=.010*math.sin(a);inner=centre+u*dx+v*dz+normal*(math.sqrt(max(0,radius*radius-dx*dx-dz*dz))+.0005);edge=p+u*(.034*math.cos(a))+v*(.022*math.sin(a));hit,q,nn,face=body.ray_cast(edge+normal*.10,-normal)
   if hit:edge=q-normal*.0005
   vv.append(tuple(inner.lerp(edge,t)))
 for ring in range(4):
  for k in range(96):ff.append((ring*96+k,ring*96+(k+1)%96,(ring+1)*96+(k+1)%96,(ring+1)*96+k))
 mesh=bpy.data.meshes.new('Reptile_anatomical_lid_rim');mesh.from_pydata(vv,[],ff);lid=bpy.data.objects.new(f'Reptile_lid_rim_{side}',mesh);coll.objects.link(lid);mesh.color_attributes.new(name='Baked_source_albedo',type='FLOAT_COLOR',domain='CORNER');mesh.materials.append(body.data.materials[0])
 for f in mesh.polygons:f.use_smooth=True
 bpy.ops.object.select_all(action='DESELECT');lid.select_set(True);bpy.context.view_layer.objects.active=lid;transfer=lid.modifiers.new('Adjacent_scale_colour','DATA_TRANSFER');transfer.object=body;transfer.use_loop_data=True;transfer.data_types_loops={'COLOR_CORNER'};transfer.loop_mapping='POLYINTERP_NEAREST';transfer.layers_vcol_loop_select_src='ALL';transfer.layers_vcol_loop_select_dst='NAME';bpy.ops.object.modifier_apply(modifier=transfer.name)
 eyes.append({'side':side,'surface':list(p),'centre':list(centre),'normal':list(normal),'radius_m':radius})
for p,n,u,v in deforms:
 delta=co-np.array(p);du=delta@np.array(u);dv=delta@np.array(v);depth=delta@np.array(n);d=np.sqrt((du/.025)**2+(dv/.013)**2);t=np.clip((1.25-d)/.45,0,1);weight=t*t*(3-2*t)*(np.abs(depth)<.08);co-=np.array(n)[None,:]*(.035*weight[:,None])
me.vertices.foreach_set('co',co.ravel());me.update()
bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=1,location=(2.035,0,.71));palate=bpy.context.object;move(palate);palate.name='Enclosed_dark_oral_cavity';palate.scale=(.16,.205,.07);palate.data.materials.append(oral)
for f in palate.data.polygons:f.use_smooth=True
scene=bpy.context.scene;scene['production_status']='LIZARD_EYE_AND_ORAL_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m26','revision':'r10','source':'r09','status':'author_trial_pending_view','landmarks':'r09 head_side_diagnosis.png and head_side_ray_probe.json','eyes':eyes,'oral_cavity':{'centre':[2.035,0,.71],'radii':[.16,.205,.07]},'remaining':['Eye scale and lid integration','Mouth cavity clearance','Pitted source surface and colour fidelity','Independent review']},indent=2),encoding='utf-8');print('EYE_ORAL_TRIAL_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=24;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('head_side',(1.85,-5,1.1),(1.85,0,1.1),1.5),('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
