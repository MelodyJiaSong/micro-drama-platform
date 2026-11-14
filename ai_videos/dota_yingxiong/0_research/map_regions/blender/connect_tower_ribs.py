"""Continuous load-bearing ribs, large basal bone claws and directional corrosion."""
from pathlib import Path
import bpy,json,math,numpy as np,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from build_production_map import surface
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r09';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r08/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];body=max((o for o in coll.objects if o.type=='MESH' and not o.name.startswith('Scanned_skull')),key=lambda o:len(o.data.polygons));me=body.data
bronze=surface('Continuous_dark_bronze_sheath',(.025,.019,.012),(.09,.065,.032),8,.57,.008);bronze.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.78
bone=surface('Basal_weathered_bone',(.12,.085,.043),(.48,.39,.24),7,.83,.009)
def curve(name,points,radius,mat,radii):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=radius;cu.bevel_resolution=4;cu.use_fill_caps=True;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co,r in zip(sp.bezier_points,points,radii):p.co=co;p.radius=r;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob
# Locate existing upper tusks before extending their supporting ribs downward.
co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);sel=co[(co[:,2]>8.55)&(co[:,2]<8.8)&(np.linalg.norm(co[:,:2],axis=1)>2.0)]
angles=np.arctan2(sel[:,1],sel[:,0]);centers=np.arange(8)*math.tau/8+math.pi/8
for _ in range(20):
 dist=np.abs(np.angle(np.exp(1j*(angles[:,None]-centers[None,:]))));labels=dist.argmin(1)
 for i in range(8):
  if np.any(labels==i):centers[i]=np.angle(np.exp(1j*angles[labels==i]).mean())
for i,a in enumerate(centers):
 d=Vector((math.cos(a),math.sin(a),0));points=[d*4.68+Vector((0,0,1.0)),d*4.23+Vector((0,0,2.9)),d*3.65+Vector((0,0,5.7)),d*3.55+Vector((0,0,7.35)),d*3.38+Vector((0,0,8.57))]
 curve('Continuous_structural_bronze_rib',points,.19,bronze,[1.25,1,.85,.9,1.15])
 curve('Large_outward_basal_bone_claw',[d*4.68+Vector((0,0,1.42)),d*4.86+Vector((0,0,.87)),d*5.23+Vector((0,0,.25)),d*5.61+Vector((0,0,.08))],.26,bone,[1.35,1,.55,.03])
 for zz,rr in [(1.5,4.56),(4.1,3.98),(7.95,3.48)]:
  bpy.ops.mesh.primitive_torus_add(major_radius=.225,minor_radius=.045,major_segments=32,minor_segments=8,location=d*rr+Vector((0,0,zz)));ob=bpy.context.object
  for c in list(ob.users_collection):c.objects.unlink(ob)
  coll.objects.link(ob);ob.name='Bronze_rib_retaining_cuff';ob.data.materials.append(bronze)
# Rework the existing broad orange camouflage into narrow vertical rust runs.
mat=bpy.data.materials['Tower_hammered_purple_grey_metal'];nt=mat.node_tree
for n in nt.nodes:
 if n.type=='TEX_NOISE' and abs(n.inputs['Scale'].default_value-2.8)<.001:
  source=n.inputs['Vector'].links[0].from_socket;stretch=nt.nodes.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(3,3,.10);nt.links.new(source,stretch.inputs[0]);nt.links.new(stretch.outputs[0],n.inputs['Vector'])
 for s in n.inputs:
  if s.name=='Color2' and s.type=='RGBA' and abs(s.default_value[0]-.12)<.0001 and abs(s.default_value[1]-.036)<.0001:s.default_value=(.035,.015,.008,1)
# A mineral should illuminate through its volume without visible lamp reflections.
removed=[]
for ob in list(coll.objects):
 if ob.type=='LIGHT' and ob.name.startswith('Fluorite_bounce_light'):removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
nt=bpy.data.materials['Tower_faceted_fluorite_shell'].node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.16,.45,.36,1)
for n in nt.nodes:
 if n.type=='VOLUME_ABSORPTION':n.inputs['Color'].default_value=(.025,.26,.19,1);n.inputs['Density'].default_value=.8
 if n.type=='EMISSION':n.inputs['Color'].default_value=(.015,.25,.17,1)
# Reduce the visible cellular pattern on the external optical surface.
for key in ['Normal','Emission Color','Emission Strength']:
 for link in list(bs.inputs[key].links):nt.links.remove(link)
bs.inputs['Emission Strength'].default_value=0
for ob in coll.objects:
 if ob.name.startswith('Internal_mineral_fissure'):
  # The authored triangular planes are too regular in the previous revision.
  ob.hide_render=True
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg26','revision':'r09','source':'r08','status':'author_preview_not_accepted','changes':['Eight continuous bronze structural ribs through skull band','Eight large outward-curving basal bone claws','Directional dark rust instead of uniform orange blotches','Teal fluorite without reflected point lamps or external cellular emission'],'removed_lights':removed,'remaining':['Panel seams and stair detail','Bone attachment integration','Mineral fissure realism','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'tower_preview.png');bpy.ops.render.render(write_still=True)
