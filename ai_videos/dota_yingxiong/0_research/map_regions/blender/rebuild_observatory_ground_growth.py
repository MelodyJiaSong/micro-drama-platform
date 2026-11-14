"""Rebuild visible root paths and reference-scale plinth crystals after r45 review."""
from pathlib import Path
import bpy, json, math, random, sys
from mathutils import Vector, Quaternion
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3]
folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'))
out=folder/'r46';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r45/authoring.blend'))
coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2346)
stats={}
def wall(a):return 2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)
def door(p):return p.y < -2.20 and abs(p.x)<.91
for ob in coll.objects:
 if ob.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root','Fine_feeder_root')):
  ob.hide_render=True;ob.hide_viewport=True
 if not ob.hide_render and ob.name.startswith(('Irregular_fern_root_margin','Dense_base_fern_skirt')):
  ob.scale*=.66
  direction=Vector((ob.location.x,ob.location.y,0)).normalized()
  ob.location+=direction*rng.uniform(.10,.30)
bark=bpy.data.materials['Tileable_root_bark_actual_scale'].copy();bark.name='Weathered_connected_root_bark_r46'
nt=bark.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');tex=next(q for q in n if q.type=='TEX_IMAGE' and q.image and '_diff_' in q.image.name)
hsv=n.new('ShaderNodeHueSaturation');hsv.inputs['Saturation'].default_value=.28;hsv.inputs['Value'].default_value=.82;l.new(tex.outputs['Color'],hsv.inputs['Color']);l.new(hsv.outputs[0],bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value=.93;bs.inputs['Specular IOR Level'].default_value=.10
for node in n:
 if node.type=='BUMP':node.inputs['Distance'].default_value=.0025
root_count=0;root_end_z=[]
def tube(points,radius,name,end_radius=.012):
 global root_count
 if any(door(p) for p in points):return
 rings=16;verts=[];faces=[];length=[0.]
 for j,p in enumerate(points):
  if j:length.append(length[-1]+(p-points[j-1]).length)
  tangent=(points[min(j+1,len(points)-1)]-points[max(0,j-1)]).normalized()
  u=tangent.cross(Vector((0,0,1))).normalized();v=tangent.cross(u);t=j/(len(points)-1)
  r=radius*(1-t)**.8+end_radius
  for k in range(rings):
   a=k*math.tau/rings;rr=r*(1+.06*math.sin(5*a+j*.18))
   verts.append(tuple(p+rr*(u*math.cos(a)+v*math.sin(a))))
 for j in range(len(points)-1):
  for k in range(rings):faces.append((j*rings+k,j*rings+(k+1)%rings,(j+1)*rings+(k+1)%rings,(j+1)*rings+k))
 faces += [tuple(range(rings-1,-1,-1)),tuple((len(points)-1)*rings+k for k in range(rings))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();mesh.materials.append(bark)
 uv=mesh.uv_layers.new(name='Longitudinal_bark_metres')
 for p in mesh.polygons:
  p.use_smooth=True;ks=[mesh.loops[li].vertex_index%rings for li in p.loop_indices];seam=0 in ks and rings-1 in ks
  for li in p.loop_indices:
   j,k=divmod(mesh.loops[li].vertex_index,rings)
   uv.data[li].uv=((rings if seam and k==0 else k)/rings*math.tau*(radius+end_radius),length[j])
 ob=bpy.data.objects.new(name,mesh);coll.objects.link(ob);ob.parent=parent;root_count+=1;root_end_z.append(points[-1].z)
 return ob
# Start inside the stone, emerge as a curved root, branch continuously, then bury tips.
for i in range(38):
 a=i*math.tau/38+rng.uniform(-.04,.04)
 if math.sin(a)<-.94:continue
 start=wall(a)-.18;extent=rng.uniform(1.0,1.35);bend=rng.uniform(-.22,.22);phase=rng.random()*math.tau
 points=[];radius=rng.uniform(.055,.083)
 for j in range(91):
  t=j/90;aa=a+bend*t+.025*math.sin(t*7+phase)*math.sin(math.pi*t);r=start+extent*t
  z=.23*(1-t)**3+.105+.018*math.sin(t*9+phase)*math.sin(math.pi*t)-.19*t**8
  points.append(Vector((r*math.cos(aa),r*math.sin(aa),z)))
 tube(points,radius,'Continuous_forest_primary_root')
 for j,sign in [(32,-1),(54,1)]:
  origin=points[j];angle=math.atan2(origin.y,origin.x);r0=math.hypot(origin.x,origin.y);turn=sign*rng.uniform(.14,.29);ext=rng.uniform(.30,.56);branch=[]
  for k in range(51):
   t=k/50;aa=angle+turn*t;rr=r0+ext*t;z=origin.z*(1-t)+.07*math.sin(math.pi*t)-.08*t**7
   branch.append(Vector((rr*math.cos(aa),rr*math.sin(aa),z)))
  tube(branch,radius*.45,'Continuous_forest_branch',.005)
stats['new_root_paths']=root_count;stats['buried_root_tip_z']= [min(root_end_z),max(root_end_z)]
# Reveal the full framed mineral surface: the old geodes were mostly inside the stone.
crystals=0
for ob in coll.objects:
 if not ob.name.startswith('Inset_faceted_amethyst_geode'):continue
 center=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
 angle=round(math.atan2(center.y,center.x)/(math.pi/4))*math.pi/4;normal=Vector((math.cos(angle),math.sin(angle),0));tangent=Vector((-normal.y,normal.x,0))
 for v in ob.data.vertices:
  d=v.co-center;v.co=center+tangent*d.dot(tangent)*1.12+Vector((0,0,d.z*1.28))+normal*(d.dot(normal)+.068)
 ob.data.update();crystals+=1
for mat in bpy.data.materials:
 if not mat.name.startswith('Inset_quartz_amethyst_'):continue
 nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.25,.065,.38,1);bs.inputs['Transmission Weight'].default_value=.40;bs.inputs['Roughness'].default_value=.19
 for node in nt.nodes:
  if node.type=='VOLUME_ABSORPTION':node.inputs['Density'].default_value=2.0
stats['revealed_plinth_crystals']=crystals
# Add branching, wall-contact ivy patches rather than parallel vertical strips.
leaf=next(o for o in coll.objects if not o.hide_render and o.name.startswith('Wall_attached_ivy_leaf'));wood=bpy.data.materials['Oak_door_and_roots'];ivy_count=0
for side in range(8):
 angle=-math.pi/2+side*math.pi/4;normal=Vector((math.cos(angle),math.sin(angle),0));tangent=Vector((-normal.y,normal.x,0))
 for cluster in range(4):
  u0=rng.uniform(-.86,.86);z0=rng.uniform(.40,1.95)
  if side==0 and abs(u0)<.78:continue
  for branch in range(3):
   sign=(-1,1,1)[branch];extent=rng.uniform(.20,.48);points=[]
   for j in range(25):
    t=j/24;u=max(-.92,min(.92,u0+sign*extent*t));z=z0+t*rng.uniform(.2,.25) if j==0 else z0+t*.34+.025*math.sin(t*6+branch)
    co=normal*2.421+tangent*u+Vector((0,0,z));points.append(co)
    if j%3:continue
    for s in [-1,1]:
     ob=leaf.copy();ob.data=leaf.data;coll.objects.link(ob);ob.name='Clustered_wall_contact_ivy';ob.parent=parent;ob.location=co+tangent*s*rng.uniform(.025,.065)+Vector((0,0,rng.uniform(-.02,.025)));ob.scale=leaf.scale*rng.uniform(.65,1.0);ob.rotation_mode='QUATERNION';ob.rotation_quaternion=normal.to_track_quat('Z','Y')@Quaternion((0,0,1),rng.uniform(-1.9,1.9));ivy_count+=1
   cu=bpy.data.curves.new('Ivy_connected_branch','CURVE');cu.dimensions='3D';cu.bevel_depth=.0025;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
   for p,co in zip(sp.points,points):p.co=(*co,1)
   ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob);ob.parent=parent;cu.materials.append(wood)
stats['clustered_ivy_leaves']=ivy_count
# Broader irregular moss patches on the ledge, using true-scale scanned shoots.
sources=[o for o in coll.objects if o.name.startswith('Cornice_moss_tuft')]
for i in range(700):
 a=rng.random()*math.tau
 if math.sin(a*7+.8)+.5*math.cos(a*13)<-.25:continue
 src=sources[i%len(sources)];ob=src.copy();ob.data=src.data;coll.objects.link(ob);ob.name='Broad_cornice_moss_patch';ob.parent=parent
 r=wall(a)+rng.uniform(-.06,.08);ob.location=(r*math.cos(a),r*math.sin(a),2.59+rng.uniform(-.006,.003));ob.rotation_euler.z=rng.random()*math.tau;ob.scale=(rng.uniform(.7,1.2),)*3
stats['additional_moss_patches']=sum(o.name.startswith('Broad_cornice_moss_patch') for o in coll.objects)
scene=bpy.context.scene;scene['production_status']='R46_ROOT_CRYSTAL_GROWTH_TRIAL_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r46','source':'r45','status':'author_trial_pending_view','changes':stats,'remaining':['Root path and fern balance','Crystal/stone frame fit','Ivy attachment and moss coverage','Independent review']},indent=2),encoding='utf-8');print('R46_SAVED',json.dumps(stats),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=40;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
