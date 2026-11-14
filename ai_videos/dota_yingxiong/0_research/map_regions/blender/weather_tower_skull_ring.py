"""Match jawless skulls and aged octagonal metalwork to the tower design."""
from pathlib import Path
import bpy,bmesh,json,math,random,numpy as np,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from build_production_map import surface
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r05';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];skulls=[o for o in coll.objects if o.name.startswith('Scanned_skull_')];me=skulls[0].data
v=np.array([p.co[:] for p in me.vertices]);parent=list(range(len(v)))
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for edge in me.edges:
 a,b=map(find,edge.vertices);parent[a]=b
groups={}
for i in range(len(v)):groups.setdefault(find(i),[]).append(i)
lo,hi=v.min(0),v.max(0);remove=[]
for ids in groups.values():
 if ((v[ids,2].mean()-lo[2])/(hi[2]-lo[2]))<.20:remove.extend(ids)
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.verts[i] for i in remove],context='VERTS');bm.to_mesh(me);bm.free()
rng=random.Random(2605)
for o in skulls:o.scale=(rng.uniform(1.06,1.21),)*3;o.location.z-=.045;o.rotation_euler.y+=rng.uniform(-.07,.07)
ivory=me.materials[0];nt=ivory.node_tree;bs=nt.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket
tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=13;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.8;nt.links.new(tc.outputs['Object'],noise.inputs['Vector'])
ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.4;ramp.color_ramp.elements[0].color=(.025,.018,.008,1);ramp.color_ramp.elements[1].position=.59;ramp.color_ramp.elements[1].color=(.8,.76,.62,1);nt.links.new(noise.outputs[0],ramp.inputs[0]);mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.64;nt.links.new(source,mix.inputs[1]);nt.links.new(ramp.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
def oct_radius(angle,apothem):return apothem/math.cos((angle%(math.pi/4))-math.pi/8)
for o in coll.objects:
 if o.name=='Closed_skull_support_band':
  for vv in o.data.vertices:
   r=math.hypot(vv.co.x,vv.co.y)
   if r>.1:
    a=math.atan2(vv.co.y,vv.co.x);rr=oct_radius(a,3.47);vv.co.x*=rr/r;vv.co.y*=rr/r
 if o.name.startswith('Skull_ring_bronze_rim'):
  for vv in o.data.vertices:
   r=math.hypot(vv.co.x,vv.co.y);a=math.atan2(vv.co.y,vv.co.x);rr=oct_radius(a,3.5)+(r-3.6);vv.co.x*=rr/r;vv.co.y*=rr/r
mat=bpy.data.materials['Skull_ring_blackened_bronze'];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=.55;bs.inputs['Roughness'].default_value=.73
for n in nt.nodes:
 if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.008,.014,.012,1);n.color_ramp.elements[1].color=(.052,.036,.024,1)
for i in range(64):
 a=(i+.5)*math.tau/64;radius=oct_radius(a,3.53)
 for zz in [6.91,7.75]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=6,radius=.042,location=(radius*math.cos(a),radius*math.sin(a),zz));o=bpy.context.object
  for c in list(o.users_collection):c.objects.unlink(o)
  coll.objects.link(o);o.name='Separate_skull_band_rivet';o.data.materials.append(mat)
moss=surface('Skull_ring_hanging_moss',(.018,.027,.006),(.12,.15,.038),42,.96,.001)
cu=bpy.data.curves.new('Skull_ring_weathered_moss_fibres','CURVE');cu.dimensions='3D';cu.bevel_depth=.003;cu.bevel_resolution=0;cu.materials.append(moss)
for i in range(600):
 a=rng.random()*math.tau;r=oct_radius(a,3.63);z=rng.choice([6.92,7.72])+rng.uniform(-.04,.04);length=rng.uniform(.06,.32);s=cu.splines.new('POLY');s.points.add(7)
 for j,p in enumerate(s.points):
  t=j/7;rr=r+.06*math.sin(t*3);aa=a+.008*math.sin(t*6+i);p.co=(rr*math.cos(aa),rr*math.sin(aa),z-length*t,1);p.radius=(1-t)*rng.uniform(.4,1)
o=bpy.data.objects.new(cu.name,cu);coll.objects.link(o)
nt=bpy.data.materials['Tower_faceted_fluorite_shell'].node_tree;bs=nt.nodes.get('Principled BSDF');vor=next(n for n in nt.nodes if n.type=='TEX_VORONOI');crack=nt.nodes.new('ShaderNodeMath');crack.operation='LESS_THAN';crack.inputs[1].default_value=.014;nt.links.new(vor.outputs['Distance'],crack.inputs[0]);gain=nt.nodes.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=.75;nt.links.new(crack.outputs[0],gain.inputs[0]);nt.links.new(gain.outputs[0],bs.inputs['Emission Strength']);bs.inputs['Emission Color'].default_value=(.18,.65,.30,1)
scene=bpy.context.scene;scene.cycles.samples=32;scene.render.filepath=str(out/'tower_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r05','source':'r04','status':'author_preview_pending','changes':['Removed separate mandible and lower-tooth components to match jawless reference skulls','Varied skull sizes and applied ochre weathering','Octagonal patinated support band, 128 real rivets and 600 hanging moss fibres','Thin fluorite fracture emission'],'removed_skull_vertices':len(remove),'skull_mesh_faces':len(me.polygons),'skull_instances':len(skulls),'remaining':['All-view independent review pending']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
