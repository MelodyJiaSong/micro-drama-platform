"""Replace fused crown with connected branches and individually modelled maple leaves."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys,numpy as np,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r05');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m1_Treant/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m1_r01.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
bpy.context.view_layer.objects.active=body;bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new();bm.from_mesh(body.data);remove=[v for v in bm.verts if v.co.z>1.37 or (v.co.z>1.29 and math.hypot(v.co.x,v.co.y)>.15)];bmesh.ops.delete(bm,geom=remove,context='VERTS');edges=[e for e in bm.edges if e.is_boundary and all(v.co.z>1.28 for v in e.verts)]
if edges:bmesh.ops.holes_fill(bm,edges=edges,sides=0)
bm.to_mesh(body.data);bm.free();body.data.update()
if body.data.has_custom_normals:body.data.normals_split_custom_set([(0,0,0)]*len(body.data.loops))
mat=body.data.materials[0];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
for socket in ['Metallic','Roughness']:
 for link in list(bs.inputs[socket].links):nt.links.remove(link)
bs.inputs['Metallic'].default_value=0;bs.inputs['Roughness'].default_value=.82
old=bs.inputs['Base Color'].links[0].from_socket;tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=.7;tint.inputs[2].default_value=(.48,.32,.19,1);nt.links.new(old,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])
tc=nt.nodes.new('ShaderNodeTexCoord');mapping=nt.nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(150,150,9);nt.links.new(tc.outputs['Object'],mapping.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=3;nt.links.new(mapping.outputs[0],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.004;bump.inputs['Strength'].default_value=.5;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
def material(name,color,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
bark=material('Treant_connected_branch_bark',(.027,.019,.011),.88)
leafmats=[material('Treant_maple_leaf_'+str(i),col,.72) for i,col in enumerate([(.012,.024,.006),(.022,.034,.008),(.018,.009,.019),(.028,.041,.009),(.025,.017,.013)])]
for m in leafmats:
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.035;p.inputs['Subsurface Radius'].default_value=(.02,.05,.01);p.inputs['Subsurface Scale'].default_value=.004;p.inputs['IOR'].default_value=1.33;p.inputs['Specular IOR Level'].default_value=.18
veinmat=material('Treant_maple_leaf_midveins',(.032,.044,.011),.65)
def curve(name,pts,radius,material,radii=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=3;cu.bevel_depth=radius;cu.bevel_resolution=2;s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for i,(p,co) in enumerate(zip(s.bezier_points,pts)):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=radii[i] if radii else 1
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(material);return ob
rng=random.Random(102);verts=[];faces=[];mats=[];leaf_count=0
# Lobed maple outline: five distinct tips and deep intervening sinuses.
outline=[(0,0),(-.20,.10),(-.44,.05),(-.36,.24),(-.65,.38),(-.39,.42),(-.50,.70),(-.23,.60),(-.21,.88),(0,1.14),(.21,.88),(.23,.60),(.50,.70),(.39,.42),(.65,.38),(.36,.24),(.44,.05),(.20,.10)]
def leaf(origin,direction,width,roll):
 global leaf_count
 long=Vector(direction).normalized();side=long.cross(Vector((0,0,1)))
 if side.length<.01:side=Vector((1,0,0))
 side.normalize();normal=side.cross(long).normalized();side,normal=side*math.cos(roll)+normal*math.sin(roll),-side*math.sin(roll)+normal*math.cos(roll)
 start=len(verts);origin=Vector(origin);center=origin+long*width*.43+normal*width*.035;verts.append(tuple(center))
 for x,y in outline:verts.append(tuple(origin+side*x*width+long*y*width+normal*width*(.03*math.sin(y*math.pi)-.10*x*x)))
 material_index=rng.choices(range(5),[4,3,2,2,1])[0]
 for k in range(len(outline)):faces.append((start,start+1+k,start+1+(k+1)%len(outline)));mats.append(material_index)
 # Central vein and petiole are actual geometry and connect leaf to twig.
 curve('Maple_petioles_and_midvein',[origin-long*width*.12,origin,center,origin+long*width*1.1],.00032,veinmat,[1.2,1,.7,.1]);leaf_count+=1
primary_ends=[]
for i in range(3):
 a=i*math.tau/3;start=Vector((math.cos(a)*.035,math.sin(a)*.035,1.32));end=Vector((math.cos(a)*.12,math.sin(a)*.10,1.51+i*.035));primary_ends.append(end);curve('Treant_primary_crown_branch',[start,start.lerp(end,.5)+Vector((0,0,.02)),end],.042,bark,[1,.8,.42])
for cluster in range(15):
 angle=math.tau*cluster/15+rng.uniform(-.18,.18);rad=rng.uniform(.20,.43);end=Vector((math.cos(angle)*rad,math.sin(angle)*rad*.75,rng.uniform(1.53,1.83)));root=min(primary_ends,key=lambda p:(p-end).length).copy();mid=root.lerp(end,.55)+Vector((0,0,.035));curve('Treant_crown_branch',[root,mid,end],.012,bark,[1.4,.75,.12])
 for twig in range(9):
  t=.45+twig*.065;start=root.lerp(end,t);az=angle+(1 if twig%2 else -1)*rng.uniform(.6,1.6);tip=start+Vector((math.cos(az)*rng.uniform(.045,.10),math.sin(az)*rng.uniform(.04,.09),rng.uniform(.015,.07)));curve('Treant_leaf_twig',[start,start.lerp(tip,.5)+Vector((0,0,.008)),tip],.003,bark,[1,.6,.05])
  for j in range(4):
   along=.3+j*.22;origin=start.lerp(tip,along);direction=Vector((math.cos(az+(j%2*2-1)*.8),math.sin(az+(j%2*2-1)*.8),rng.uniform(-1.2,.7)));leaf(origin,direction,rng.uniform(.045,.075),rng.uniform(-1.5,1.5))
me=bpy.data.meshes.new('Individual_curved_lobed_leaves');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob)
for m in leafmats:me.materials.append(m)
for p,i in zip(me.polygons,mats):p.material_index=i;p.use_smooth=True
solid=ob.modifiers.new('Leaf_lamina_thickness','SOLIDIFY');solid.thickness=.00018
scene=bpy.context.scene;scene.view_settings.exposure=0;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.location=(0,-6,1.2);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
for ob in scene.objects:
 if ob.type=='LIGHT' and ob not in set(coll.all_objects):ob.data.energy*=.4
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':args.revision,'status':'author_preview_not_accepted','source':'r01/inspection/m1_r01.blend','changes':['Removed fused upper crown above 1.37 m','Connected branches, petioles and modelled lobed maple leaves','Nonmetallic bark and darker brown reflectance','Varied crown height and reduced leaf specular response'],'leaf_count':leaf_count,'remaining':['Finger separation and arm length','Thick lichen geometry','Eye socket depth','Close-up bark and leaf detail still require independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
