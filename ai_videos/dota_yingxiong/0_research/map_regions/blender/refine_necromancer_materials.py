"""Separate robe, trim, skin and beard response on the grounded necromancer."""
from pathlib import Path
import bpy,json,math,random,sys,numpy as np,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r05');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m5_Necromancer/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r03/authoring.blend'));coll=bpy.data.collections['ASSET_m5'];body=next(o for o in coll.objects if o.type=='MESH');bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);me=body.data
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);tri=vi.reshape(-1,3);co=v[tri].mean(1);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1)
base=me.materials[0];im=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);rgb=pix[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]
def variant(name,tint,rough,metal=0):
 m=base.copy();m.name=name;nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(source,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
 for key,val in [('Metallic',metal),('Roughness',rough)]:
  for link in list(bs.inputs[key].links):nt.links.remove(link)
  bs.inputs[key].default_value=val
 me.materials.append(m);return len(me.materials)-1,m
robe,robe_mat=variant('Necromancer_old_violet_wool',(.78,.17,1.0),.93);gold,gold_mat=variant('Necromancer_tarnished_gold_trim',(.75,.48,.16),.58,.6);skin,skin_mat=variant('Necromancer_living_aged_skin',(.65,.46,.40),.7)
nt=robe_mat.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Sheen Weight'].default_value=.18;noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=350;noise.inputs['Detail'].default_value=2;bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0005;bump.inputs['Strength'].default_value=.35;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal'])
bs=skin_mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.10;bs.inputs['Subsurface Scale'].default_value=.008
nt=skin_mat.node_tree;tc=nt.nodes.new('ShaderNodeTexCoord');split=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tc.outputs['Object'],split.inputs[0]);absolute=nt.nodes.new('ShaderNodeMath');absolute.operation='ABSOLUTE';nt.links.new(split.outputs['X'],absolute.inputs[0]);factors=[]
for socket,lo,hi,a,b in [(split.outputs['Z'],1.64,1.67,0,1),(split.outputs['Z'],1.76,1.79,1,0),(absolute.outputs[0],.070,.095,1,0),(split.outputs['Y'],-.09,-.06,1,0)]:
 node=nt.nodes.new('ShaderNodeMapRange');node.interpolation_type='SMOOTHSTEP';node.clamp=True;nt.links.new(socket,node.inputs['Value']);node.inputs['From Min'].default_value=lo;node.inputs['From Max'].default_value=hi;node.inputs['To Min'].default_value=a;node.inputs['To Max'].default_value=b;factors.append(node.outputs['Result'])
factor=factors[0]
for socket in factors[1:]:node=nt.nodes.new('ShaderNodeMath');node.operation='MULTIPLY';nt.links.new(factor,node.inputs[0]);nt.links.new(socket,node.inputs[1]);factor=node.outputs[0]
tint=next(n for n in nt.nodes if n.type=='MIX_RGB');nt.links.new(factor,tint.inputs[0])
x,y,z=co.T;r,g,b=rgb.T;labels=np.zeros(len(co),np.int32);robe_mask=(r>g*1.05)&(b>g*1.04)&(z<1.59)&(z>.12)&(rgb.mean(1)<.57);labels[robe_mask]=robe;gold_mask=(r>g*1.18)&(g>b*1.10)&(z<1.35)&(z>.13)&(np.abs(x)>.12)&(np.abs(x)<.25)&(y<-.10)&(rgb.mean(1)<.50);labels[gold_mask]=gold;skin_mask=(z>1.64)&(z<1.79)&(np.abs(x)<.095)&(y<-.06);labels[skin_mask]=skin;me.polygons.foreach_set('material_index',labels);me.update()
def simple(name,color,rough=.75):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
hairmat=simple('Necromancer_fine_grey_white_beard',(.30,.29,.26),.85);rng=random.Random(504)
def front(x,z):
 hit,pos,n,face=body.ray_cast(Vector((x,-3,z)),Vector((0,1,0)));return float(pos.y-.0018) if hit else -.18
for i in range(650):
 xx=rng.uniform(-.075,.075);top=1.625+rng.uniform(-.02,.025)+max(0,abs(xx)-.04)*1.5;bottom=rng.uniform(1.17,1.27)+abs(xx)*.5;cu=bpy.data.curves.new('Fine_beard_fibre','CURVE');cu.dimensions='3D';cu.resolution_u=3;cu.bevel_depth=rng.uniform(.00022,.00048);cu.bevel_resolution=1;sp=cu.splines.new('BEZIER');sp.bezier_points.add(4)
 for j,p in enumerate(sp.bezier_points):
  t=j/4;px=xx*(1-.75*t)+math.sin(t*math.pi*2+i)*.003;pz=top*(1-t)+bottom*t;p.co=(px,front(px,pz)-rng.uniform(.001,.004),pz);p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=1-t*.94
 ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob);cu.materials.append(hairmat)
eye=simple('Necromancer_dim_violet_eye_glow',(.06,.005,.12),.4);bs=eye.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(.28,.015,.7,1);bs.inputs['Emission Strength'].default_value=1.2;eyes=[]
for side in [-1,1]:
 px=side*.050;pz=1.750;py=front(px,pz)-.002;bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=(px,py,pz));ob=bpy.context.object
 for c in list(ob.users_collection):c.objects.unlink(ob)
 coll.objects.link(ob);ob.name='Violet_eye_glow_candidate';ob.scale=(.0055,.002,.0035);ob.data.materials.append(eye);eyes.append(list(ob.location))
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m5','revision':args.revision,'source':'r03','status':'author_preview_not_accepted','changes':['Violet wool and restricted old gold trim separated from grey cloak','Soft skin-mask boundaries','650 separate beard fibres with cheek origins','Eye glow moved upward into the eye region'],'material_face_counts':{'robe':int(robe_mask.sum()),'gold':int(gold_mask.sum()),'skin':int(skin_mask.sum())},'eye_trial_positions':eyes,'remaining':['Verify face and eye placement','Cloak and bone-chain geometry','Trim coverage and hand detail','Independent full review']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.45;scene.camera.location=(0,-3,1.73);look_at(scene.camera,(0,-.08,1.69));scene.render.filepath=str(out/'face_preview.png');bpy.ops.render.render(write_still=True)
