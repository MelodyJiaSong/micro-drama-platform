"""Seat mineral in real stone sockets and separate ground roots from crystals."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));OUT=WORLD/'background/map_3d';folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r48';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r47/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2348);stats={}
def object_mesh(name,vertices,faces,mat):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();mesh.materials.append(mat);ob=bpy.data.objects.new(name,mesh);coll.objects.link(ob);ob.parent=parent;return ob
stone=bpy.data.materials['Limestone_capstones'];backing=material('Quartz_rough_mineral_bed',(.065,.048,.075),.9);sockets=0
for ob in list(coll.objects):
 if ob.name.startswith('Stone_amethyst_socket'):ob.hide_render=True;ob.hide_viewport=True
 if not ob.name.startswith('Inset_faceted_amethyst_geode'):continue
 edge=[v.co.copy() for v in ob.data.vertices[:12]];center=sum(edge,Vector())/12;angle=round(math.atan2(center.y,center.x)/(math.pi/4))*math.pi/4;normal=Vector((math.cos(angle),math.sin(angle),0));plane=center.dot(normal);verts=[]
 # Actual closed masonry annulus, whose inner edge follows the irregular crystal.
 for scale,depth in [(1.01,2.375),(1.23,2.375),(1.23,2.485),(1.01,2.485)]:
  for p in edge:
   delta=p-center;delta-=normal*delta.dot(normal);verts.append(tuple(center+delta*scale+normal*(depth-plane)))
 faces=[]
 for ring in range(4):
  for k in range(12):faces.append((ring*12+k,ring*12+(k+1)%12,((ring+1)%4)*12+(k+1)%12,((ring+1)%4)*12+k))
 frame=object_mesh('Fitted_stone_crystal_socket',verts,faces,stone);bevel=frame.modifiers.new('Small_worn_socket_edges','BEVEL');bevel.width=.003;bevel.segments=2
 vv=[]
 for depth in [2.375,2.406]:
  for p in edge:
   d=p-center;d-=normal*d.dot(normal);vv.append(tuple(center+d*1.12+normal*(depth-plane)))
 ff=[tuple(range(11,-1,-1)),tuple(range(12,24))]+[(k,(k+1)%12,(k+1)%12+12,k+12) for k in range(12)];object_mesh('Recessed_quartz_stone_bedding',vv,ff,backing);sockets+=1
stats['closed_fitted_crystal_sockets']=sockets
print('FITTED_SOCKETS',sockets,flush=True)
# Ground roots emerge below the masonry, never from the crystal centres.
roots=0
for ob in coll.objects:
 if not ob.name.startswith(('Continuous_forest_primary_root','Continuous_forest_branch')):continue
 count=len(ob.data.vertices)//16
 for j in range(count):
  ring=[ob.data.vertices[j*16+k] for k in range(16)];center=sum((v.co for v in ring),Vector())/16;t=j/(count-1);target=.045+.027*math.sin(math.pi*t)-.13*t**8
  if ob.name.startswith('Continuous_forest_branch'):target=.045*(1-t)+.025*math.sin(math.pi*t)-.08*t**8
  for v in ring:v.co.z+=target-center.z
 ob.data.update();roots+=1
stats['lowered_root_paths']=roots
soil=bpy.data.objects['Continuous_root_soil_bed'];mat=soil.data.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.98
for n in nt.nodes:
 if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY':n.inputs[2].default_value=(.75,.65,.50,1)
diff=next(n for n in nt.nodes if n.type=='TEX_IMAGE');disp=nt.nodes.new('ShaderNodeTexImage');disp.image=bpy.data.images.load(str(OUT/'textures/brown_mud_02_disp_2k.png'),check_existing=True);disp.image.colorspace_settings.name='Non-Color';disp.projection='BOX';disp.projection_blend=.3
if diff.inputs[0].is_linked:nt.links.new(diff.inputs[0].links[0].from_socket,disp.inputs[0])
bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.006;bump.inputs['Strength'].default_value=.8;nt.links.new(disp.outputs[0],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
# A broken forest-litter margin covers the regular soil boundary with real leaves.
leaf=next(o for o in coll.objects if not o.hide_render and o.name.startswith('Wall_attached_ivy_leaf'));leafmesh=leaf.data.copy()
for slot,original in enumerate(leafmesh.materials):
 mat=original.copy();mat.name='Dry_forest_leaf_'+str(slot);nt=mat.node_tree;diffuse=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_diff_' in (n.image.name+n.image.filepath));source=diffuse.outputs['Color'];targets=[link.to_socket for link in list(source.links)]
 # Modify the texture connection outside the shared Poly Haven shader group;
 # preserve its alpha, normals, roughness and the living ivy's material.
 gray=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(source,gray.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.025,.009,.003,1);ramp.color_ramp.elements[-1].color=(.26,.11,.025,1);nt.links.new(gray.outputs[0],ramp.inputs[0])
 for socket in targets:nt.links.new(ramp.outputs[0],socket)
 leafmesh.materials[slot]=mat
moss=[o for o in coll.objects if not o.hide_render and o.name.startswith('Cornice_moss_tuft')];leaves=0;cushions=0
ground_tree=BVHTree.FromPolygons([v.co.copy() for v in soil.data.vertices],[tuple(p.vertices) for p in soil.data.polygons])
for i in range(1400):
 a=rng.random()*math.tau;wall=2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8);r=wall+rng.uniform(.10,1.43);x,y=r*math.cos(a),r*math.sin(a)
 if y < -2.2 and abs(x)<.95:continue
 p,normal,face,distance=ground_tree.ray_cast(Vector((x,y,1)),Vector((0,0,-1)))
 if p is None or p.z<.008:continue
 if i%3:
  ob=bpy.data.objects.new('Scattered_dry_ground_leaf',leafmesh);coll.objects.link(ob);ob.parent=parent;ob.location=p+Vector((0,0,.002));ob.rotation_euler=(rng.uniform(-.18,.18),rng.uniform(-.18,.18),rng.random()*math.tau);ob.scale=leaf.scale*rng.uniform(.6,1.2);leaves+=1
 else:
  src=rng.choice(moss);ob=src.copy();ob.data=src.data;coll.objects.link(ob);ob.name='Forest_floor_moss_cushion';ob.parent=parent;ob.location=p;ob.rotation_euler=(0,0,rng.random()*math.tau);ob.scale=(rng.uniform(.75,1.4),)*3;cushions+=1
ferns=0
for ob in coll.objects:
 if not ob.hide_render and ob.name.startswith(('Irregular_fern_root_margin','Dense_base_fern_skirt')):ob.scale*=1.28;ferns+=1
stats.update(dry_leaf_instances=leaves,ground_moss_cushions=cushions,ferns_enlarged=ferns)
scene=bpy.context.scene;scene['production_status']='R48_SOCKET_ROOT_SEPARATION_AND_FOREST_FLOOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r47/authoring.json').read_text());report.update(revision='r48',source='r47',status='author_trial_pending_view',r48_changes=stats,remaining=['Crystal frame stone contact and depth','Root network visibility without mushroom forms','Ground material and forest-litter transitions','Multi-angle independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('R48_SAVED',json.dumps(stats),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=40;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
