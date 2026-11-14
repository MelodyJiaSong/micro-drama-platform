"""Keep detailed native wood and replace fused foliage with curved serrated leaves."""
from pathlib import Path
import argparse,sys,json,math,random
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inspect_model import look_at

p=argparse.ArgumentParser();p.add_argument('--revision',default='r10');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r09/authoring.blend'))
coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons))
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new();bm.from_mesh(body.data)
remove=[v for v in bm.verts if v.co.z>1.60 or (v.co.z>1.37 and math.hypot(v.co.x,v.co.y)>.18) or (v.co.z>1.29 and math.hypot(v.co.x,v.co.y)>.27)]
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(body.data);bm.free();body.data.update()
if body.data.has_custom_normals:body.data.normals_split_custom_set([(0,0,0)]*len(body.data.loops))
mat=body.data.materials[0];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket
tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=.28;tint.inputs[2].default_value=(.72,.46,.25,1);nt.links.new(old,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color'])

def material(name,col,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*col,1);bs.inputs['Roughness'].default_value=rough;return m

bark=material('Connected_branch_rough_brown_bark',(.026,.016,.008),.82)
nt=bark.node_tree;bs=nt.nodes.get('Principled BSDF');tc=nt.nodes.new('ShaderNodeTexCoord');scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(85,85,8);nt.links.new(tc.outputs['Object'],scale.inputs[0]);noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=4;nt.links.new(scale.outputs[0],noise.inputs[0]);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0015;bump.inputs['Strength'].default_value=.6;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
leafmats=[]
for i,col in enumerate([(.014,.034,.005),(.023,.045,.007),(.022,.009,.026),(.010,.022,.004),(.035,.026,.009)]):
 m=material('Living_maple_lamina_'+str(i),col,.44);leafmats.append(m);nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.035;bs.inputs['Subsurface Scale'].default_value=.001;bs.inputs['Coat Weight'].default_value=.06;bs.inputs['Coat Roughness'].default_value=.3
 tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=24;noise.inputs['Detail'].default_value=4;nt.links.new(tc.outputs['UV'],noise.inputs['Vector']);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.4 for x in col],1);ramp.color_ramp.elements[1].color=(*[x*1.8 for x in col],1);nt.links.new(noise.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00016;bump.inputs['Strength'].default_value=.22;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
veinmat=material('Maple_petioles_and_raised_veins',(.030,.043,.010),.62)

def curve(name,pts,radius,mat,radii=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=1;cu.resolution_u=2;cu.use_fill_caps=True;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for i,(point,co) in enumerate(zip(sp.points,pts)):point.co=(*co,1);point.radius=radii[i] if radii else 1
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob

rng=random.Random(1029);verts=[];faces=[];uvs=[];mats=[];count=0
outline=[(0,0),(-.20,.10),(-.44,.05),(-.36,.24),(-.65,.38),(-.39,.42),(-.50,.70),(-.23,.60),(-.21,.88),(0,1.14),(.21,.88),(.23,.60),(.50,.70),(.39,.42),(.65,.38),(.36,.24),(.44,.05),(.20,.10)]
boundary=[]
for i,a in enumerate(outline):
 b=outline[(i+1)%len(outline)]
 for j in range(6):
  t=j/6;x=a[0]*(1-t)+b[0]*t;y=a[1]*(1-t)+b[1]*t
  if j%2 and i not in (0,17):x*=1.025;y=.43+(y-.43)*1.025
  boundary.append((x,y))

def leaf(origin,direction,width,roll):
 global count
 origin=Vector(origin);long=Vector(direction).normalized();side=long.cross(Vector((0,0,1)))
 if side.length<.01:side=Vector((1,0,0))
 side.normalize();normal=side.cross(long).normalized();side,normal=side*math.cos(roll)+normal*math.sin(roll),-side*math.sin(roll)+normal*math.cos(roll)
 curl=rng.uniform(-.25,.25);warp=rng.uniform(-.13,.13)
 def pos(x,y):return origin+width*(side*x+long*y+normal*(.055*math.sin(math.pi*y)+curl*x*x+warp*x*y))
 start=len(verts);verts.append(tuple(pos(0,.43)));uvs.append((.5,.43/1.14));N=len(boundary);rings=5
 for r in range(1,rings+1):
  f=r/rings
  for x,y in boundary:
   px=x*f;py=.43+(y-.43)*f;verts.append(tuple(pos(px,py)));uvs.append((px/1.3+.5,py/1.14))
 mi=rng.choices(range(5),[4,3,3,3,1])[0]
 for j in range(N):faces.append((start,start+1+j,start+1+(j+1)%N));mats.append(mi)
 for r in range(rings-1):
  inner=start+1+r*N;outer=inner+N
  for j in range(N):faces.append((inner+j,outer+j,outer+(j+1)%N,inner+(j+1)%N));mats.append(mi)
 curve('Leaf_petiole',[origin-long*width*.12,origin,pos(0,.43),pos(0,1.1)],.00019,veinmat,[1.2,1,.65,.10])
 for x,y in [(-.64,.38),(-.49,.70),(.49,.70),(.64,.38)]:curve('Leaf_primary_vein',[pos(0,.18),pos(x*.45,.18+(y-.18)*.45)+normal*.00010,pos(x,y)],.00011,veinmat,[1,.65,.08])
 count+=1

centers=[(-.26,-.025,1.67),(-.065,.035,1.76),(.17,.06,1.78),(.31,-.035,1.55),(-.37,.04,1.47),(.035,-.16,1.60),(.015,.18,1.65)]
for ci,coords in enumerate(centers):
 center=Vector(coords);root=Vector((coords[0]*.24,coords[1]*.24,1.43));mid=root.lerp(center,.5);curve('Native_crown_branch',[root,mid,center],.026,bark,[1,.60,.18])
 for k in range(28):
  theta=k*2.399963+rng.uniform(-.12,.12);h=rng.uniform(-.11,.09);rad=rng.uniform(.045,.13);tip=center+Vector((math.cos(theta)*rad,math.sin(theta)*rad*.85,h));start=mid.lerp(center,rng.uniform(.5,1));curve('Attached_foliage_twig',[start,start.lerp(tip,.55),tip],.0028,bark,[1,.62,.12])
  for j in range(4):
   origin=start.lerp(tip,.35+j*.21);az=theta+(1 if j%2 else -1)*rng.uniform(.45,1.5);direction=(math.cos(az),math.sin(az),rng.uniform(-1.5,.9));leaf(origin,direction,rng.uniform(.045,.082),rng.uniform(-1.0,1.0))
me=bpy.data.meshes.new('Separate_serrated_curved_maple_leaves');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob)
for m in leafmats:me.materials.append(m)
uv=me.uv_layers.new(name='Leaf_local_coordinates')
for poly,mi in zip(me.polygons,mats):
 poly.material_index=mi;poly.use_smooth=True
 for li in poly.loop_indices:uv.data[li].uv=uvs[me.loops[li].vertex_index]
solid=ob.modifiers.new('Thin_leaf_surface','SOLIDIFY');solid.thickness=.00009
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':args.revision,'source':'r09','status':'author_preview_not_accepted','changes':['Preserved detailed source trunk, roots, arms and head','Replaced fused crown with seven connected volumetric branch clusters','Individual serrated, curved, veined green and purple maple leaves'],'leaf_count':count,'remaining':['Author visual check','Source torso texture distortion','Arm and finger proportions','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.57));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
