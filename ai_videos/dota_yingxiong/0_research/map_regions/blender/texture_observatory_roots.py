"""Use tileable bark at real scale, longitudinal UVs and visible feeder roots."""
from pathlib import Path
import bpy,json,sys,math,random
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at,material
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('background/*/bg23_*/model_3d'));out=folder/'r26';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r25/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];parent=bpy.data.objects['Asset_metre_calibration'];rng=random.Random(2326)
mat=material('Tileable_root_bark_actual_scale',(.09,.075,.045),.88);nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=.14
uv=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs[3].default_value=3;l.new(uv.outputs['UV'],scale.inputs[0])
textures={}
for tag,suffix in [('color','diff_4k.jpg'),('height','disp_4k.png'),('rough','rough_4k.jpg')]:
 node=n.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(WORLD/'background/map_3d/environment_sources/bark_brown_02'/('bark_brown_02_'+suffix)),check_existing=True);l.new(scale.outputs[0],node.inputs['Vector']);textures[tag]=node
 if tag!='color':node.image.colorspace_settings.name='Non-Color'
tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.24,.28,.23,1);l.new(textures['color'].outputs['Color'],tint.inputs[1])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=12;noise.inputs['Detail'].default_value=3;l.new(uv.outputs['Object'],noise.inputs['Vector']);mask=n.new('ShaderNodeMapRange');mask.inputs['From Min'].default_value=.56;mask.inputs['From Max'].default_value=.73;l.new(noise.outputs['Fac'],mask.inputs[0]);moss=n.new('ShaderNodeMixRGB');moss.inputs[2].default_value=(.024,.037,.009,1);l.new(mask.outputs[0],moss.inputs[0]);l.new(tint.outputs[0],moss.inputs[1]);l.new(moss.outputs[0],bs.inputs['Base Color']);l.new(textures['rough'].outputs['Color'],bs.inputs['Roughness'])
bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.005;bump.inputs['Strength'].default_value=.8;l.new(textures['height'].outputs['Color'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
roots=[];feeders=[]
for ob in coll.objects:
 if not ob.name.startswith(('Woven_pale_primary_root','Connected_crossing_rootlet','Interwoven_circumferential_root')):continue
 me=ob.data;me.materials.clear();me.materials.append(mat);count=len(me.vertices)//14;centers=[sum((me.vertices[j*14+k].co for k in range(14)),Vector())/14 for j in range(count)];lengths=[0.]
 for j,c in enumerate(centers):
  if j:lengths.append(lengths[-1]+(c-centers[j-1]).length)
  for k in range(14):
   v=me.vertices[j*14+k];v.co=c+(v.co-c)*(1+.12*math.sin(k*2.3+j*.4)+.07*math.sin(j*1.7));v.co.z-=.012
 for face in me.polygons:
  ks=[me.loops[li].vertex_index%14 for li in face.loop_indices];seam=0 in ks and 13 in ks
  for li in face.loop_indices:
   vi=me.loops[li].vertex_index;j,k=divmod(vi,14);radius=(me.vertices[j*14].co-centers[j]).length
   me.uv_layers.active.data[li].uv=((14 if seam and k==0 else k)/14*math.tau*radius,lengths[j])
 me.update();roots.append(ob)
 if ob.name.startswith('Woven_pale_primary_root'):
  for j in [25,40,55,65]:
   c=centers[j];d=(centers[min(j+3,count-1)]-c).normalized();side=Vector((-d.y,d.x,0))*rng.choice([-1,1]);points=[]
   for step in range(21):
    t=step/20;p=c+(d*.19+side*.25)*t+side*(.03*math.sin(t*8));p.z=c.z*(1-t)-.035*t+.016*math.sin(t*math.pi);points.append(p)
   feeders.append(points)
for points in feeders:
 cu=bpy.data.curves.new('Fine_feeder_root','CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=.010;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for j,(p,c) in enumerate(zip(sp.points,points)):p.co=(*c,1);p.radius=(1-j/(len(points)-1))**.7+.10
 ob=bpy.data.objects.new('Fine_feeder_root',cu);coll.objects.link(ob);ob.parent=parent;cu.materials.append(mat)
# Low irregular soil collar covers the buried ends, without crossing the entrance.
soil=material('Root_collar_damp_soil',(.025,.022,.012),.97);sn=soil.node_tree.nodes;sl=soil.node_tree.links;sb=sn.get('Principled BSDF');noise=sn.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=55;noise.inputs['Detail'].default_value=5;bp=sn.new('ShaderNodeBump');bp.inputs['Distance'].default_value=.018;sl.new(noise.outputs['Fac'],bp.inputs['Height']);sl.new(bp.outputs[0],sb.inputs['Normal'])
verts=[];faces=[]
for i in range(257):
 a=i/256*math.tau;wall=2.39/math.cos((a+math.pi/8)%(math.pi/4)-math.pi/8)
 for j in range(9):
  t=j/8;r=wall-.05+t*(.92+.14*math.sin(a*13)+.07*math.cos(a*27));z=-.035+.052*math.sin(t*math.pi)**.6+.009*math.sin(a*37+t*9)*math.sin(t*math.pi)
  if math.sin(a)<-.92:z=-.12
  verts.append((r*math.cos(a),r*math.sin(a),z))
for i in range(256):
 for j in range(8):k=i*9+j;faces.append((k,k+1,k+10,k+9))
me=bpy.data.meshes.new('Irregular_root_soil_collar');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(me.name,me);coll.objects.link(ob);ob.parent=parent;me.materials.append(soil)
for face in me.polygons:face.use_smooth=True
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'bg23','revision':'r26','source':'r25','status':'author_preview_not_accepted','changes':['Replace dead tree atlas with tileable scanned bark, physically scaled longitudinal UVs and corrected seam','Geometric bark roughness and moss variation','Fine feeder roots and damp soil transition'],'root_meshes':len(roots),'feeder_roots':len(feeders)},indent=2),encoding='utf-8')
scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=3.8;look_at(scene.camera,(1.25,-.9,.35));scene.render.filepath=str(out/'root_detail.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(9,-14,7.5);scene.camera.data.ortho_scale=6.7;look_at(scene.camera,(0,0,2.4));scene.render.filepath=str(out/'perspective_preview.png');bpy.ops.render.render(write_still=True)
