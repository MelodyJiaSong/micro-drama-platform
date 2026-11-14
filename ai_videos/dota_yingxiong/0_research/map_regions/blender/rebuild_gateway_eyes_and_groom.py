"""Measured eye reconstruction and short black hair for the Gateway Relics merchant."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
from mathutils import Vector,kdtree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_Gateway_Relics/model_3d'));out=folder/'r02';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m303_r01.blend'));coll=bpy.data.collections['ASSET_m303'];body=bpy.data.objects['geometry_0'];me=body.data;me.transform(body.matrix_world);body.parent=None;body.matrix_world.identity();me.update()
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);original=co.copy()
loops=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',loops);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);vuv=np.zeros((len(co),2),np.float32);vuv[loops]=uv
headids=np.flatnonzero((co[:,2]>1.59)&(co[:,1]<.03));kd=kdtree.KDTree(len(headids))
for j,i in enumerate(headids):kd.insert(Vector(co[i]),int(i))
kd.balance()
def smooth(a,lo,hi):
 t=np.clip((a-lo)/(hi-lo),0,1);return t*t*(3-2*t)
eye_centres=[(-.0494,-.056,1.730),(.02394,-.056,1.730)];R=.015
for cx,cy,cz in eye_centres:
 d=np.sqrt(((co[:,0]-cx)/.0165)**2+((co[:,2]-cz)/.0075)**2);w=(1-smooth(d,.72,1.22))*(co[:,1]<-.025);co[:,1]+=np.maximum(cy+.002-co[:,1],0)*w
# A few millimetres at the lip corners, with a broad smooth falloff, restores the
# slight smile in the reference without changing the central mouth or jaw width.
for cx in [-.0494,.03458]:
 w=np.exp(-((co[:,0]-cx)/.016)**2-((co[:,2]-1.6582)/.013)**2)*smooth(-co[:,1],.025,.065);co[:,2]+=.0045*w
me.vertices.foreach_set('co',co.ravel());me.update()
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
for p in me.polygons:p.use_smooth=True
front=np.clip((.04-co[:,1])/.09,0,1);hairline=1.705+(.112-.055*np.clip(np.abs(co[:,0]+.007)/.09,0,1))*front;scalp=smooth(co[:,2]-hairline,-.002,.004)*(co[:,2]>1.69)
beard=smooth(-co[:,1],.01,.055)*smooth(co[:,2],1.59,1.615)*(1-smooth(co[:,2],1.675,1.70))*(1-smooth(np.abs(co[:,0]+.007),.073,.092));lip=np.sqrt(((co[:,0]+.007)/.049)**2+((co[:,2]-1.658)/.018)**2);beard*=smooth(lip,.85,1.2)
brow=np.zeros(len(co),np.float32)
for cx,cy,cz in eye_centres:
 u=(co[:,0]-cx)/.021;curve=1.747+.0035*(1-np.minimum(u*u,1));brow=np.maximum(brow,(1-smooth(np.abs(u),.80,1.1))*(1-smooth(np.abs(co[:,2]-curve),.001,.004))*smooth(-co[:,1],.025,.055))
for name,values in [('ScalpHair',scalp),('BeardStubble',beard),('Eyebrows',brow)]:
 attr=me.attributes.new(name,'FLOAT','POINT');attr.data.foreach_set('value',values.astype(np.float32))
mat=me.materials[0];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');colour=bs.inputs['Base Color'].links[0].from_socket
for name,strength,tint in [('ScalpHair',.95,(.018,.014,.010,1)),('BeardStubble',.30,(.08,.065,.05,1)),('Eyebrows',.80,(.012,.009,.006,1))]:
 a=n.new('ShaderNodeAttribute');a.attribute_name=name;weight=n.new('ShaderNodeMath');weight.operation='MULTIPLY';weight.inputs[1].default_value=strength;l.new(a.outputs['Fac'],weight.inputs[0]);mix=n.new('ShaderNodeMixRGB');l.new(weight.outputs[0],mix.inputs[0]);l.new(colour,mix.inputs[1]);mix.inputs[2].default_value=tint;colour=mix.outputs[0]
l.new(colour,bs.inputs['Base Color'])
def material(name,colour,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;shader=m.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=colour;shader.inputs['Roughness'].default_value=rough;return m,shader
sclera,s=material('Warm_ivory_sclera',(.62,.57,.49,1),.22);s.inputs['IOR'].default_value=1.38;s.inputs['Subsurface Weight'].default_value=.06
iris,ir=material('Hazel_radial_iris',(.07,.035,.012,1),.18);ir.inputs['IOR'].default_value=1.38;ir.inputs['Coat Weight'].default_value=.35;ir.inputs['Coat Roughness'].default_value=.06;a=iris.node_tree.nodes.new('ShaderNodeVertexColor');a.layer_name='IrisPigment';iris.node_tree.links.new(a.outputs['Color'],ir.inputs['Base Color'])
pupil,ps=material('Dark_brown_pupil',(.0015,.0010,.0007,1),.08);ps.inputs['IOR'].default_value=1.38
def link_asset(ob):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob)
eye_reports=[]
for index,(cx,cy,cz) in enumerate(eye_centres):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=R,location=(cx,cy,cz));eye=bpy.context.object;eye.name=f'Anatomical_eyeball_{index}';link_asset(eye);eye.data.materials.append(sclera)
 for p in eye.data.polygons:p.use_smooth=True
 # Bridge the opening with actual lid thickness. The outer edge follows the
 # existing facial surface, and UVs come from that intact rim, not the bad eye.
 verts=[];faces=[];tex=[];rings=6;segments=96
 for j in range(rings):
  t=j/(rings-1)
  for k in range(segments):
   angle=math.tau*k/segments;ca,sa=math.cos(angle),math.sin(angle);inner=Vector((cx+.0138*ca,cy,cz+(.0048 if sa>=0 else .0035)*sa));inner.y=cy-math.sqrt(max(1e-8,R*R-(inner.x-cx)**2-(inner.z-cz)**2))-.00035
   outer=Vector((cx+.021*ca,cy-.010,cz+(.014 if sa>=0 else .011)*sa));hit,p,norm,face=body.ray_cast(Vector((outer.x,-.4,outer.z)),Vector((0,1,0)))
   if hit and p.y<.015:outer.y=p.y-.00025
   else:outer.y=-.065+abs(ca)*.006
   point=inner.lerp(outer,t);point.y-=.0007*math.sin(t*math.pi);verts.append(tuple(point));nearest=kd.find(outer)[1];tex.append(tuple(vuv[nearest]))
 for j in range(rings-1):
  for k in range(segments):faces.append(((j+1)*segments+k,(j+1)*segments+(k+1)%segments,j*segments+(k+1)%segments,j*segments+k))
 mesh=bpy.data.meshes.new('Anatomical_eyelid_rim');mesh.from_pydata(verts,[],faces);lid=bpy.data.objects.new(f'Reconstructed_upper_lower_lids_{index}',mesh);coll.objects.link(lid);mesh.materials.append(mat);layer=mesh.uv_layers.new(name='UVMap')
 for loop in mesh.loops:layer.data[loop.index].uv=tex[loop.vertex_index]
 for p in mesh.polygons:p.use_smooth=True
 solid=lid.modifiers.new('Lid_thickness','SOLIDIFY');solid.thickness=.0007;solid.offset=0
 # Curved iris and pupil disks, both following the actual eyeball surface.
 for kind,radius,mt in [('Iris',.0047,iris),('Pupil',.0020,pupil)]:
  vv=[(cx,cy-R-.00005,cz)];ff=[];colours=[(.05,.025,.010,1)];rng=np.random.default_rng(303+index)
  angular=rng.uniform(.55,1.5,96)
  for ring in range(1,9):
   rr=radius*ring/8
   for k in range(96):
    ang=k*math.tau/96;vv.append((cx+rr*math.cos(ang),cy-math.sqrt(R*R-rr*rr)-.0001-(.00004 if kind=='Pupil' else 0),cz+rr*math.sin(ang)));fade=.35 if ring==8 else 1;f=angular[k]*fade;colours.append((.085*f,.048*f,.016*f,1))
  for k in range(96):ff.append((0,1+k,1+(k+1)%96))
  for ring in range(7):
   for k in range(96):ff.append((1+ring*96+k,1+ring*96+(k+1)%96,1+(ring+1)*96+(k+1)%96,1+(ring+1)*96+k))
  mm=bpy.data.meshes.new(kind);mm.from_pydata(vv,[],ff);oo=bpy.data.objects.new(f'{kind}_{index}',mm);coll.objects.link(oo);mm.materials.append(mt)
  for p in mm.polygons:p.use_smooth=True
  if kind=='Iris':ca=mm.color_attributes.new(name='IrisPigment',type='FLOAT_COLOR',domain='POINT');ca.data.foreach_set('color',np.array(colours,np.float32).ravel())
 eye_reports.append({'centre_m':[cx,cy,cz],'radius_m':R,'iris_radius_m':.0047,'lid_width_m':.042})
me.calc_loop_triangles();tri=np.empty(len(me.loop_triangles)*3,np.int32);me.loop_triangles.foreach_get('vertices',tri);tri=tri.reshape(-1,3);cross=np.cross(co[tri[:,1]]-co[tri[:,0]],co[tri[:,2]]-co[tri[:,0]]);areas=np.linalg.norm(cross,axis=1)*.5;normals=cross/np.maximum(areas[:,None]*2,1e-12)
hairmat=bpy.data.materials.new('Short_black_keratin');hairmat.use_nodes=True;hn,hl=hairmat.node_tree.nodes,hairmat.node_tree.links;hn.clear();output=hn.new('ShaderNodeOutputMaterial');hairbs=hn.new('ShaderNodeBsdfHairPrincipled');hairbs.parametrization='COLOR';hairbs.inputs['Color'].default_value=(.009,.006,.004,1);hairbs.inputs['Roughness'].default_value=.36;hl.new(hairbs.outputs[0],output.inputs['Surface']);rng=np.random.default_rng(30302);grooms=[]
for name,coverage,count,lengthrange in [('Buzzcut',scalp,65000,(.0015,.0035)),('Stubble',beard,16000,(.00045,.0013)),('Brows',brow,6000,(.002,.004))]:
 weight=areas*coverage[tri].mean(axis=1);weight[areas<1e-12]=0;selected=rng.choice(len(tri),count,p=weight/weight.sum());u,v=rng.random(count),rng.random(count);bary=np.column_stack((1-np.sqrt(u),np.sqrt(u)*(1-v),np.sqrt(u)*v));roots=(co[tri[selected]]*bary[:,:,None]).sum(axis=1);normal=normals[selected];length=rng.uniform(*lengthrange,count);points=np.empty((count,4,3),np.float32);side=rng.normal(size=(count,3));side-=normal*(side*normal).sum(axis=1)[:,None];side/=np.maximum(np.linalg.norm(side,axis=1)[:,None],1e-10)
 for j,t in enumerate(np.linspace(0,1,4)):points[:,j]=roots+normal*(.0001+length*t*.7)[:,None]+side*(length*t*.45)[:,None]
 curves=bpy.data.hair_curves.new(name);curves.add_curves([4]*count);curves.set_types(type='CATMULL_ROM');curves.attributes['position'].data.foreach_set('vector',points.ravel());radius=curves.attributes.new('radius','FLOAT','POINT');radius.data.foreach_set('value',(rng.uniform(.000025,.000045,count)[:,None]*np.array([1,.85,.55,.015])).astype(np.float32).ravel());ob=bpy.data.objects.new(name+'_individual_hairs',curves);coll.objects.link(ob);curves.materials.append(hairmat);grooms.append({'name':name,'strands':count,'length_m':lengthrange})
scene=bpy.context.scene;scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=1000;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report={'asset_id':'m303','revision':'r02','source':'r01 inspection','status':'author_trial_pending_view','landmarks':'face_diagnosis_r01/landmarks.json','changes':['Recess malformed eye surfaces and add separate eyeballs, radial irises, pupils and UV-following eyelid rims','Black cropped hair, eyebrows and stubble with actual short hair curves','Lift lip corners smoothly by at most 4.5mm'],'eyes':eye_reports,'grooms':grooms,'remaining':['Lid-to-face integration and skin colour continuity','Natural gaze and smile','Groom boundaries','Source mesh holes beyond repaired eye region','Independent review']};(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('FACE_REBUILT',flush=True)
for name,loc,target,scale in [('face_detail',(0,-2,1.70),(0,0,1.70),.38),('face_side',(1.3,-2,1.70),(0,0,1.70),.38),('author_preview',(4,-6,2.0),(0,0,.925),2.37)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
