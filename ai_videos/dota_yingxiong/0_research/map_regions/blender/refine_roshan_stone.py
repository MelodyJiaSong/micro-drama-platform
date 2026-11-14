"""Purple fractured stone, faceted amethyst spines and the orange facial fissure."""
from pathlib import Path
import bpy,bmesh,json,math,random,sys,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m7_Roshan/model_3d'));out=folder/'r02';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m7_r01.blend'));coll=bpy.data.collections['ASSET_m7'];body=next(o for o in coll.objects if o.type=='MESH');bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);me=body.data
v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);vi=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',vi);co=v[vi.reshape(-1,3)].mean(1);uv=np.empty(len(me.loops)*2,np.float32);me.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2).mean(1);base=me.materials[0];im=next(n.image for n in base.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');pixels=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pixels);pixels=pixels.reshape(im.size[1],im.size[0],4);rgb=pixels[(uv[:,1]*im.size[1]).astype(int).clip(0,im.size[1]-1),(uv[:,0]*im.size[0]).astype(int).clip(0,im.size[0]-1),:3]
mat=base.copy();mat.name='Roshan_deep_violet_weathered_stone';nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket;mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.55,.16,.70,1);nt.links.new(source,mix.inputs[1]);nt.links.new(mix.outputs[0],bs.inputs['Base Color'])
for key,val in [('Metallic',0),('Roughness',.86)]:
 for link in list(bs.inputs[key].links):nt.links.remove(link)
 bs.inputs[key].default_value=val
tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=35;noise.inputs['Detail'].default_value=5;nt.links.new(tc.outputs['Object'],noise.inputs['Vector']);bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.016;bump.inputs['Strength'].default_value=.65;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],bs.inputs['Normal']);me.materials[0]=mat
crystal=bpy.data.materials.new('Roshan_amethyst_fracture_crystal');crystal.use_nodes=True;p=crystal.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.035,.004,.065,1);p.inputs['Roughness'].default_value=.24;p.inputs['Transmission Weight'].default_value=.18;p.inputs['IOR'].default_value=1.54;me.materials.append(crystal)
mask=(rgb[:,2]>rgb[:,0]*1.25)&(rgb[:,2]>rgb[:,1]*1.5)&(rgb.mean(1)<.55);me.polygons.foreach_set('material_index',mask.astype(np.int32));upper=mask&(co[:,2]>3.48);selected=co[upper]
# Select separated spine groups in XY, preserving their asymmetric placement.
centers=[]
if len(selected):
 centers=[selected[selected[:,2].argmax()]]
 for _ in range(11):
  dist=np.min(np.linalg.norm(selected[:,None,:2]-np.asarray(centers)[None,:,:2],axis=2),axis=1);idx=int(dist.argmax())
  if dist[idx]<.23:break
  centers.append(selected[idx])
 centers=np.asarray(centers)
 for _ in range(12):
  labels=np.linalg.norm(selected[:,None,:2]-centers[None,:,:2],axis=2).argmin(1)
  for i in range(len(centers)):
   if np.any(labels==i):centers[i]=selected[labels==i].mean(0)
bm=bmesh.new();bm.from_mesh(me);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in np.flatnonzero(upper)],context='FACES');bm.to_mesh(me);bm.free();me.update()
if me.has_custom_normals:me.normals_split_custom_set([(0,0,0)]*len(me.loops))
# Fine geometric fracture relief leaves contact points fixed.
group=body.vertex_groups.new(name='Rock_weathering_above_contact');indices=[i for i,vert in enumerate(me.vertices) if vert.co.z>.16];group.add(indices,1,'REPLACE');tex=bpy.data.textures.new('Roshan_physical_rock_fracture',type='CLOUDS');tex.noise_scale=.095;tex.noise_depth=2;dis=body.modifiers.new('Chipped_stone_surface','DISPLACE');dis.texture=tex;dis.texture_coords='GLOBAL';dis.strength=.038;dis.mid_level=.5;dis.vertex_group=group.name;bpy.ops.object.modifier_apply(modifier=dis.name)
rng=random.Random(702);spines=[]
for i,c in enumerate(centers):
 points=selected[labels==i];bottom=float(np.quantile(points[:,2],.08))-.10;top=min(4.4,float(points[:,2].max())+rng.uniform(.08,.22));height=top-bottom
 if height<.16:continue
 radius=rng.uniform(.10,.18);axis=Vector((float(c[0])*.07,.18,1)).normalized();origin=Vector((float(c[0]),float(c[1]),bottom));basis=axis.to_track_quat('Z','Y').to_matrix();verts=[];faces=[];n=6
 for z,rr in [(0,radius),(height*.66,radius*.68)]:
  for j in range(n):a=j*math.tau/n;local=Vector((math.cos(a)*rr,math.sin(a)*rr,z));verts.append(tuple(origin+basis@local))
 verts.append(tuple(origin+axis*height));faces.append(tuple(range(n-1,-1,-1)))
 for j in range(n):faces.append((j,(j+1)%n,n+(j+1)%n,n+j));faces.append((n+j,n+(j+1)%n,2*n))
 data=bpy.data.meshes.new('Closed_faceted_amethyst_spine');data.from_pydata(verts,[],faces);data.materials.append(crystal);ob=bpy.data.objects.new(data.name,data);coll.objects.link(ob);spines.append({'base':list(origin),'height':height})
# Place the glowing fissure along the actual front surface of the head.
glow=bpy.data.materials.new('Roshan_orange_face_fissure');glow.use_nodes=True;nt=glow.node_tree;nt.nodes.clear();em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(1,.12,.003,1);em.inputs['Strength'].default_value=9;output=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(em.outputs[0],output.inputs['Surface']);cu=bpy.data.curves.new('Orange_head_fissure','CURVE');cu.dimensions='3D';cu.bevel_depth=.009;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(20);fissure=[]
for j,p in enumerate(sp.points):
 x=-.27+.54*j/20;z=3.27+.018*math.sin(j*.9);hit,pos,normal,face=body.ray_cast(Vector((x,-8,z)),Vector((0,1,0)))
 if not hit:raise RuntimeError('Face fissure ray missed')
 p.co=(x,pos.y-.008,z,1);p.radius=.5+.5*math.sin(math.pi*j/20);fissure.append([x,pos.y-.008,z])
ob=bpy.data.objects.new(cu.name,cu);coll.objects.link(ob);cu.materials.append(glow)
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m7','revision':'r02','source':'r01','status':'author_preview_not_accepted','changes':['Nonmetallic saturated violet stone','Fine physical fracture relief above contact points','Separate faceted amethyst spine geometry','Orange face fissure geometry'],'spines':spines,'replaced_spine_faces':int(upper.sum()),'fissure_points':fissure,'remaining':['Confirm facial fissure sits in the head seam','Stone feet and side cavities','All-view independent inspection']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
