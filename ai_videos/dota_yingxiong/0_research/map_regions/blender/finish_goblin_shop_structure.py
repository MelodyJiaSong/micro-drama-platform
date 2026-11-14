"""Rebuild freestanding shop sign and individual paving stones."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at
from build_environment_details import DetailGeometry
from build_production_map import mesh_object as make_mesh,surface
def mesh_object(name,g,coll,mats):
 return make_mesh(name,g.vertices,g.faces,mats,g.indices,coll)
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));a=next(a for a in json.loads((WORLD/'background/map_3d/asset_manifest.json').read_text(encoding='utf-8'))['assets'] if a['id']=='bg12');folder=ROOT/a['model_directory'];out=folder/'r08';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'));coll=bpy.data.collections['ASSET_bg12'];ob=next(o for o in coll.objects if o.type=='MESH');me=ob.data
bm=bmesh.new();bm.from_mesh(me);remove=[f for f in bm.faces if (lambda c:c.x>2.85 and c.z>4.75)(f.calc_center_median())];bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(me);bm.free();me.update()
wood=bpy.data.materials['bg12_Aged_golden_bamboo'];bronze=bpy.data.materials['bg12_Oxidised_bronze'];rope=surface('Shop_dark_hemp',(.07,.042,.015),(.20,.13,.05),130,.92,.001);bone=surface('Shop_old_porous_bone',(.22,.17,.10),(.60,.53,.36),35,.79,.001)
g=DetailGeometry()
# The post is outside the roof; crossbar extends away from it.
base=Vector((3.98,1.55,.08));top=Vector((3.98,1.55,6.82));g.branch([base,top],[.065,.045],0,12)
for z in np.arange(.3,6.8,.43):g.ring((3.98,1.55,float(z)),.060,.010,0,16)
g.branch([(3.62,1.55,6.2),(5.13,1.55,6.38)],[.038,.026],0,10)
for z in (1.4,3.1,4.9,6.24):
 for j in range(6):g.ring((3.98,1.55,z+j*.012),.069,.006,1,24)
def cord(start,end):g.branch([start,end],[.007,.005],1,6)
cord((4.35,1.55,6.29),(4.35,1.55,5.98));cord((4.85,1.55,6.35),(4.85,1.55,5.83))
sign=mesh_object('Freestanding_bamboo_shop_sign',g,coll,[wood,rope]);
# A weathered antler/bone charm with tapered branching tips.
b=DetailGeometry();b.branch([(4.31,1.55,5.97),(4.40,1.55,5.67),(4.31,1.55,5.35),(4.36,1.55,5.08)],[.045,.07,.045,.008],0,10)
b.branch([(4.39,1.55,5.68),(4.13,1.55,5.82),(4.03,1.55,5.95)],[.052,.035,.009],0,10)
b.branch([(4.39,1.55,5.68),(4.60,1.55,5.78),(4.65,1.55,5.91)],[.052,.03,.008],0,10)
b.branch([(4.32,1.55,5.36),(4.18,1.55,5.17)],[.035,.007],0,10);mesh_object('Hanging_weathered_bone_charm',b,coll,[bone])
# Open bell, including the inner wall and clapper instead of a solid cone.
vs=[];fs=[];profile=[(.04,5.87),(.09,5.82),(.12,5.69),(.19,5.56),(.20,5.53),(.17,5.53),(.145,5.58),(.085,5.72),(.055,5.80)]
for radius,z in profile:
 for i in range(48):
  ang=i*math.tau/48;vs.append((4.85+radius*math.cos(ang),1.55+radius*math.sin(ang),z))
for j in range(len(profile)-1):
 for i in range(48):fs.append((j*48+i,j*48+(i+1)%48,(j+1)*48+(i+1)%48,(j+1)*48+i))
mesh=bpy.data.meshes.new('Hollow_bronze_bell');mesh.from_pydata(vs,[],fs);bell=bpy.data.objects.new(mesh.name,mesh);coll.objects.link(bell);mesh.materials.append(bronze)
for p in mesh.polygons:p.use_smooth=True
g=DetailGeometry();g.branch([(4.85,1.55,5.81),(4.85,1.55,5.51)],[.012,.016],0,8);g.ellipsoid((4.85,1.55,5.50),(.03,.03,.04),0,8,12);mesh_object('Bell_clapper',g,coll,[bronze])
# Lay actual irregular stone slabs only where the retained foundation exists.
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);tri=vi.reshape(-1,3);centres=v[tri].mean(1);ground=tri[centres[:,2]<.24];tree=BVHTree.FromPolygons(v.tolist(),ground.tolist(),all_triangles=True)
stone=surface('Shop_paving_stone',(.07,.08,.075),(.25,.26,.22),12,.88,.003);rng=random.Random(287128);g=DetailGeometry();n=0
for iy in range(-8,9):
 for ix in range(-8,9):
  x=ix*.48+(iy%2)*.24;y=iy*.48
  hit=tree.ray_cast(Vector((x,y,.5)),Vector((0,0,-1)),.6)
  if hit[0] is None:continue
  # Keep slabs clear of existing columns and stairs using the original mesh.
  full_hit=ob.ray_cast(Vector((x,y,3.2)),Vector((0,0,-1)))
  if full_hit[0] and full_hit[1].z>.4:continue
  z=hit[0].z+.015;w=rng.uniform(.40,.45);d=rng.uniform(.40,.45);start=len(g.vertices)
  for dz in (-.08,.02):
   for xx,yy in [(-1,-1),(1,-1),(1,1),(-1,1)]:g.vertices.append((x+xx*w/2+rng.uniform(-.02,.02),y+yy*d/2+rng.uniform(-.02,.02),z+dz+rng.uniform(-.01,.01)))
  for face in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:g.faces.append(tuple(start+k for k in face));g.indices.append(0)
  n+=1
paving=mesh_object('Individually_laid_stone_paving',g,coll,[stone]);bev=paving.modifiers.new('Worn_slab_edges','BEVEL');bev.width=.015;bev.segments=2
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.data.ortho_scale=11.8;scene.camera.location=(14,-25,11);look_at(scene.camera,(.2,0,3.5))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r08','status':'author_preview_pending','source':'r07','changes':['Removed intersecting upper sign; rebuilt post outside roof, tied crossbar, hanging bone, hollow bronze bell and clapper','Individual paving stones with bevelled edges'],'paving_slabs':n,'removed_sign_faces':len(remove),'remaining':['Material segmentation and all-view geometry inspection pending']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'shop_preview.png');bpy.ops.render.render(write_still=True)
