"""Add masonry relief, actual frieze cuts and door hardware after r26 review."""
from pathlib import Path
import bpy,json,math,random,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/'r27';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r26/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2327);brass=bpy.data.materials['Polished_worn_brass']
def curve(name,points,radius,mat=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);ob.parent=parent
 if mat:cu.materials.append(mat)
 return ob
def sphere(name,position,radius,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=radius,location=position);o=bpy.context.object
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o);o.parent=parent;o.name=name;o.data.materials.append(mat);return o
# Raise the dome profile while retaining its measured footprint and bearing edge.
dome_prefix=('Cast_bronze_dome','Concentric_cast_relief','Cast_spiral_relief','Fine_cast_volute');instrument_prefix=('Cast_instrument_foot','Substantial_segmented_axis','Cast_axis_brass_collar','Companion_instrument_column','Companion_column_collar','Reference_mirror_sphere','Sphere_cast_cradle','Wide_flat_cast_support','Open_C_meridian','High_open_question_mark_hook','Question_hook_terminal_ball')
for ob in coll.objects:
 if ob.hide_render:continue
 if ob.name.startswith(dome_prefix):
  m=parent.matrix_world.inverted()@ob.matrix_world;inv=m.inverted()
  points=ob.data.vertices if ob.type=='MESH' else [p for sp in ob.data.splines for p in sp.points]
  for p in points:
   co=m@(p.co if ob.type=='MESH' else p.co.xyz);co.z=2.61+(co.z-2.61)*1.35;local=inv@co
   if ob.type=='MESH':p.co=local
   else:p.co=(*local,p.co.w)
 elif ob.name.startswith(instrument_prefix):ob.location.z+=.17
mat=bpy.data.materials['Tileable_root_bark_actual_scale']
for n in mat.node_tree.nodes:
 if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY':n.inputs[2].default_value=(.40,.39,.30,1)
# Change root girth by branch family; secondary feeders remain fine.
for ob in coll.objects:
 if ob.name.startswith('Woven_pale_primary_root'):
  me=ob.data;factor=rng.uniform(.9,1.55)
  for j in range(len(me.vertices)//14):
   center=sum((me.vertices[j*14+k].co for k in range(14)),Vector())/14
   for k in range(14):me.vertices[j*14+k].co=center+(me.vertices[j*14+k].co-center)*factor
  me.update()
# Variation is geometric and constrained to existing stones, not a uniform texture overlay.
changed_stones=0
for ob in coll.objects:
 if ob.hide_render:continue
 if ob.name.startswith(('Staggered_limestone_block','Unbroken_tapered_obelisk','Arch_voussoir')):
  for mod in ob.modifiers:
   if mod.type=='DISPLACE':mod.strength=rng.uniform(.008,.026)
   elif mod.type=='BEVEL':mod.width*=rng.uniform(.7,1.65)
  changed_stones+=1
 elif ob.name.startswith('Continuous_lime_backing'):
  for v in ob.data.vertices:
   r=math.hypot(v.co.x,v.co.y)
   if r>2.34:v.co.x*=1.003;v.co.y*=1.003
# Add an interlinked geometric border as real shallow incisions in all eight bands.
for side,band in enumerate(sorted([o for o in coll.objects if o.name.startswith('Mitered_continuous_frieze')],key=lambda o:o.name)):
 phi=-math.pi/2+side*math.pi/4;n=Vector((math.cos(phi),math.sin(phi),0));t=Vector((-n.y,n.x,0));paths=[]
 for zz in [2.377,2.563]:paths.append([n*2.419+t*u+Vector((0,0,zz)) for u in [-.97,.97]])
 for j in range(3):
  u=(j-1)*.45;paths.append([n*2.419+t*(u+x)+Vector((0,0,2.47+z)) for x,z in [(-.12,0),(0,.065),(.12,0),(0,-.065),(-.12,0)]])
 cu=bpy.data.curves.new('Frieze_interlace_cutter','CURVE');cu.dimensions='3D';cu.bevel_depth=.005;cu.bevel_resolution=2;cu.use_fill_caps=True
 for path in paths:
  sp=cu.splines.new('POLY');sp.points.add(len(path)-1)
  for p,co in zip(sp.points,path):p.co=(*co,1)
 cutter=bpy.data.objects.new(cu.name,cu);coll.objects.link(cutter);cutter.parent=parent;bpy.ops.object.select_all(action='DESELECT');cutter.select_set(True);bpy.context.view_layer.objects.active=cutter;bpy.ops.object.convert(target='MESH');cutter=bpy.context.object
 bpy.context.view_layer.objects.active=band;mod=band.modifiers.new('Interlinked_geometric_stone_carving','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Paired ring pulls and separate rivets give the oak door functional construction.
for x in [-.13,.13]:
 sphere('Door_handle_mount',(x,-2.30,.84),.027,brass).scale.y=.5
 curve('Hinged_bronze_ring_pull',[(x+.048*math.cos(a),-2.324,.79+.061*math.sin(a)) for a in [j*math.tau/64 for j in range(65)]],.006,brass)
for z in [.22,.58,1.42]:
 for x in [-.51,-.33,.33,.51]:sphere('Door_strap_hand_forged_rivet',(x,-2.264,z),rng.uniform(.008,.011),brass).scale.y=.45
for ob in coll.objects:
 if ob.name.startswith('Arched_oak_door_plank'):
  for mod in ob.modifiers:
   if mod.type=='BEVEL':mod.width=rng.uniform(.002,.005)
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.9;look_at(scene.camera,(0,0,2.5));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r27','source':'r26','status':'author_preview_not_accepted','changes':['Raise dome profile while retaining bearing footprint','Move connected instrument together','Moderately lighter tileable root bark and varied primary root girth','Vary stone edge erosion and bring mortar forward','Real cut frieze borders and interlinked diamonds','Paired bronze ring pulls and door strap rivets'],'stones_varied':changed_stones,'remaining':['Dome contact and instrument placement','Root naturalness','Stone carving and door details','Author and independent inspection']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=3.8;look_at(scene.camera,(1.25,-.9,.35));scene.render.filepath=str(out/'root_detail.png');bpy.ops.render.render(write_still=True)
