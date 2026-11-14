"""Restore ogre skin, worn triangular markings and short upward lower tusks."""
from pathlib import Path
import bpy,bmesh,numpy as np,json,sys,math,random,argparse
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('--revision',default='r05');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m16_Ogre/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m16_r01.blend'));coll=bpy.data.collections['ASSET_m16'];body=max((o for o in coll.all_objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));bpy.context.view_layer.update();body.data.transform(body.matrix_world);body.parent=None;body.matrix_world=Matrix.Identity(4);me=body.data
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);co=v[vi.reshape(-1,3)].mean(1);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1)
base=me.materials[0];im=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pix=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pix);pix=pix.reshape(im.size[1],im.size[0],4);rgb=pix[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]

def matcopy(name,tint,rough):
 m=base.copy();m.name=name;nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);nt.links.new(source,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
 for key,value in [('Metallic',0),('Roughness',rough)]:
  for link in list(bs.inputs[key].links):nt.links.remove(link)
  bs.inputs[key].default_value=value
 me.materials.append(m);return len(me.materials)-1,m,mix.outputs[0]

skinidx,skin,source=matcopy('Ogre_weathered_red_brown_skin',(.52,.27,.18),.68);furidx,fur,_=matcopy('Ogre_old_dark_brown_hide',(.50,.32,.18),.88)
nt=skin.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Subsurface Weight'].default_value=.04;bs.inputs['Subsurface Scale'].default_value=.009;bs.inputs['Specular IOR Level'].default_value=.25
tc=n.new('ShaderNodeTexCoord');split=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],split.inputs[0]);X,Y,Z=[split.outputs[k] for k in ['X','Y','Z']]
def mathnode(op,a,b=0):
 node=n.new('ShaderNodeMath');node.operation=op
 for socket,value in zip(node.inputs,[a,b]):
  if isinstance(value,(int,float)):socket.default_value=value
  else:l.new(value,socket)
 return node.outputs[0]
def window(socket,lo,hi,edge=.03):
 a=n.new('ShaderNodeMapRange');a.interpolation_type='SMOOTHSTEP';a.clamp=True;a.inputs['From Min'].default_value=lo;a.inputs['From Max'].default_value=lo+edge;l.new(socket,a.inputs['Value'])
 b=n.new('ShaderNodeMapRange');b.interpolation_type='SMOOTHSTEP';b.clamp=True;b.inputs['From Min'].default_value=hi-edge;b.inputs['From Max'].default_value=hi;b.inputs['To Min'].default_value=1;b.inputs['To Max'].default_value=0;l.new(socket,b.inputs['Value']);return mathnode('MULTIPLY',a.outputs[0],b.outputs[0])
front=window(Y,-2,.42,.08);central=window(X,-.50,.53,.09);front=mathnode('MULTIPLY',front,central)
chestzone=window(Z,1.88,2.30,.10);bellyzone=window(Z,1.32,1.93,.10);clean=mathnode('MULTIPLY',front,mathnode('MAXIMUM',chestzone,bellyzone))
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=12;noise.inputs['Detail'].default_value=4;l.new(tc.outputs['Object'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.09,.018,.007,1);ramp.color_ramp.elements[1].color=(.17,.055,.024,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);mix=n.new('ShaderNodeMixRGB');l.new(clean,mix.inputs[0]);l.new(source,mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2]);skincolor=mix.outputs[0]
warp=mathnode('MULTIPLY',mathnode('SUBTRACT',noise.outputs['Fac'],.5),.035);Xw=mathnode('ADD',X,warp);fraction=mathnode('FRACT',mathnode('DIVIDE',mathnode('ADD',Xw,.64),.17));triangle=mathnode('SUBTRACT',1,mathnode('ABSOLUTE',mathnode('SUBTRACT',mathnode('MULTIPLY',fraction,2),1)));triheight=mathnode('MULTIPLY',triangle,.15);xx=mathnode('MULTIPLY',X,X)
chestbase=mathnode('ADD',mathnode('ADD',2.14,warp),mathnode('MULTIPLY',xx,.34));bellybase=mathnode('ADD',mathnode('ADD',1.47,warp),mathnode('MULTIPLY',xx,.45))
chest=mathnode('MULTIPLY',mathnode('LESS_THAN',Z,chestbase),mathnode('GREATER_THAN',Z,mathnode('SUBTRACT',chestbase,triheight)))
belly=mathnode('MULTIPLY',mathnode('GREATER_THAN',Z,bellybase),mathnode('LESS_THAN',Z,mathnode('ADD',bellybase,triheight)))
tattoo=mathnode('MULTIPLY',front,mathnode('MAXIMUM',chest,belly));wear=n.new('ShaderNodeTexNoise');wear.inputs['Scale'].default_value=180;wear.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],wear.inputs['Vector']);tattoo=mathnode('MULTIPLY',tattoo,mathnode('GREATER_THAN',wear.outputs['Fac'],.42));mix=n.new('ShaderNodeMixRGB');l.new(tattoo,mix.inputs[0]);l.new(skincolor,mix.inputs[1]);mix.inputs[2].default_value=(.006,.004,.003,1);skincolor=mix.outputs[0]
freckle=n.new('ShaderNodeTexNoise');freckle.inputs['Scale'].default_value=100;freckle.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],freckle.inputs['Vector']);spot=mathnode('GREATER_THAN',freckle.outputs['Fac'],.66);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';l.new(spot,mix.inputs[0]);l.new(skincolor,mix.inputs[1]);mix.inputs[2].default_value=(.38,.32,.27,1);l.new(mix.outputs[0],bs.inputs['Base Color'])
pore=n.new('ShaderNodeTexNoise');pore.inputs['Scale'].default_value=1100;pore.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],pore.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.00065;bump.inputs['Strength'].default_value=.34;l.new(pore.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
x,y,z=co.T;r,g,b=rgb.T;labels=np.full(len(co),skinidx,np.int32);me.polygons.foreach_set('material_index',labels)
root=np.array([-.30,.26,2.530]);tip=np.array([-.393,.175,2.565]);axis=tip-root;t=np.clip(((v-root)@axis)/(axis@axis),0,1);closest=root+t[:,None]*axis;distance=np.linalg.norm(v-closest,axis=1);weight=np.clip((.042-distance)/.007,0,1)*np.clip((t-.08)/.23,0,1);target_axis=np.array([-.016,-.042,.062]);rotation=np.array(Vector(axis).rotation_difference(Vector(target_axis)).to_matrix());perp=v-closest;target=root+t[:,None]*target_axis+(perp@rotation.T)*.88;v+=(target-v)*weight[:,None];me.vertices.foreach_set('co',v.ravel());me.update();deformed=int((weight>.001).sum())
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))

def simple(name,color,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;return m
bone=simple('Short_lower_tusk_old_ivory',(.37,.29,.18),.56);scar=simple('Ogre_old_healed_scars',(.18,.069,.041),.72)
me.materials.append(bone);face_t=np.clip(((co-root)@axis)/(axis@axis),0,1);face_dist=np.linalg.norm(co-(root+face_t[:,None]*axis),axis=1);labels[(face_dist<.036)&(face_t>.18)]=len(me.materials)-1;me.polygons.foreach_set('material_index',labels)
def front_y(x,z):
 hit,pt,normal,index=body.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
 if not hit:raise RuntimeError(f'No skin surface at {x},{z}')
 return pt.y,normal
def curve(name,points,radius,material,radii):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=8;cu.bevel_depth=radius;cu.bevel_resolution=3;cu.use_fill_caps=True;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co,r in zip(sp.bezier_points,points,radii):p.co=co;p.radius=r;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(material);return ob
tusks=[]
for x,z,side in []:
 yy,normal=front_y(x,z);root=Vector((x,yy+.018,z-.016));points=[root,Vector((x+side*.010,yy-.019,z)),Vector((x+side*.012,yy-.025,z+.026)),Vector((x+side*.003,yy-.017,z+.052))];curve('Short_upturned_lower_tusk',points,.016,bone,[1,.85,.49,.025]);tusks.append([list(p) for p in points])
rng=random.Random(1602);scarcount=0
for cx,cz,angle,length in [(-.72,1.45,.3,.14),(-.66,1.56,.25,.10),(.77,1.48,-.3,.16),(.77,1.60,-.2,.10),(-.35,.68,.3,.13),(.43,.75,-.4,.17),(.43,.83,-.35,.10)]:
 points=[]
 for i in range(7):
  t=i/6-.5;xx=cx+t*length;zz=cz+t*length*angle+rng.uniform(-.003,.003)
  hit,pt,norm,index=body.ray_cast(Vector((xx,-3,zz)),Vector((0,1,0)))
  if not hit:break
  points.append(tuple(pt+norm*.0007))
 if len(points)==7:curve('Healed_irregular_skin_scar',points,.0015,scar,[.05,.6,1,.8,.9,.5,.05]);scarcount+=1
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.camera.data.ortho_scale=3.7;scene.camera.location=(0,-8,1.8);look_at(scene.camera,(0,0,1.45));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m16','revision':args.revision,'source':'r01','status':'author_preview_not_accepted','changes':['Continuous warm nonmetallic response without polygon colour-classification seams','Smaller irregular worn triangle markings; abdomen band raised','Existing long tusk shortened and curved upward by local deformation; no faces deleted','Surface-fitted fine healed scars'],'tusk_vertices_deformed':deformed,'faces_deleted':0,'scar_count':scarcount,'tusk_paths':tusks,'remaining':['Author visual validation of masks and tusk placement','Geometry holes and head proportions','Independent multi-view review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=1.30;scene.camera.location=(0,-4,2.5);look_at(scene.camera,(0,0,2.5));scene.render.filepath=str(out/'face_detail.png');bpy.ops.render.render(write_still=True)
