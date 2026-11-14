"""Build real leaf meshes from the scanned opacity silhouette, retaining source maps."""
from pathlib import Path
import bpy,numpy as np,json,math,random,sys
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m1_Treant/model_3d'));out=folder/'r13';out.mkdir(exist_ok=True);scan=WORLD/'background/map_3d/environment_sources/LeafSet027'
if (out/'authoring.blend').exists():raise FileExistsError(out)
provenance=json.loads((scan/'provenance.json').read_text(encoding='utf-8'));assert provenance['license']=='CC0'
bpy.ops.wm.open_mainfile(filepath=str(folder/'r12/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];old=bpy.data.objects['Separate_serrated_curved_maple_leaves'];coords=np.empty(len(old.data.vertices)*3,np.float32);old.data.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3)
images={}
for key in ['Color','NormalGL','Roughness','Opacity','Displacement','Scattering']:
 im=bpy.data.images.load(str(scan/f'LeafSet027_4K-PNG_{key}.png'),check_existing=True)
 if key not in ['Color','Scattering']:im.colorspace_settings.name='Non-Color'
 images[key]=im
def pixels(im):
 data=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(data);return data.reshape(im.size[1],im.size[0],4)[:,:,0]
opacity=pixels(images['Opacity']);displacement=pixels(images['Displacement']);H,W=opacity.shape
def sample(data,u,v):return float(data[int(np.clip(v*H,0,H-1)),int(np.clip(u*W,0,W-1))])
center=np.array([.500,.530]);assert sample(opacity,*center)>.9
outline=[]
for j in range(256):
 direction=np.array([math.cos(j*math.tau/256),math.sin(j*math.tau/256)]);last=center
 for radius in np.arange(.0004,.19,.0004):
  uv=center+direction*radius
  if uv[1]<.438 or sample(opacity,*uv)<.5:break
  last=uv
 outline.append(last)
materials=[]
for i,tint in enumerate([(.045,.080,.055),(.045,.070,.060),(.065,.065,.080)]):
 mat=bpy.data.materials.new(f'Scanned_dark_living_maple_{i}');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.58;bs.inputs['Specular IOR Level'].default_value=.22;bs.inputs['Subsurface Weight'].default_value=.035;bs.inputs['Subsurface Scale'].default_value=.0005
 color=n.new('ShaderNodeTexImage');color.image=images['Color'];mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(*tint,1);l.new(color.outputs['Color'],mix.inputs[1]);l.new(mix.outputs[0],bs.inputs['Base Color'])
 normal=n.new('ShaderNodeTexImage');normal.image=images['NormalGL'];normalmap=n.new('ShaderNodeNormalMap');normalmap.inputs['Strength'].default_value=.8;l.new(normal.outputs['Color'],normalmap.inputs['Color']);l.new(normalmap.outputs[0],bs.inputs['Normal'])
 rough=n.new('ShaderNodeTexImage');rough.image=images['Roughness'];remap=n.new('ShaderNodeMapRange');remap.inputs['To Min'].default_value=.42;remap.inputs['To Max'].default_value=.72;l.new(rough.outputs['Color'],remap.inputs['Value']);l.new(remap.outputs['Result'],bs.inputs['Roughness'])
 translucent=n.new('ShaderNodeBsdfTranslucent');l.new(mix.outputs[0],translucent.inputs['Color']);mixshader=n.new('ShaderNodeMixShader');mixshader.inputs[0].default_value=.16;l.new(bs.outputs[0],mixshader.inputs[1]);l.new(translucent.outputs[0],mixshader.inputs[2]);l.new(mixshader.outputs[0],n.get('Material Output').inputs['Surface']);materials.append(mat)
meshes=[]
for variant in range(6):
 verts=[];uvs=[];faces=[];rings=8;curl=(variant-2.5)*.07
 def point(uv):
  x=(uv[0]-.50)/.21;y=(uv[1]-.438)/.21;z=.045*math.sin(y*math.pi)+curl*x*x+.018*math.sin(x*9+y*4)+(sample(displacement,*uv)-.5)*.024;return (x,y,z)
 verts.append(point(center));uvs.append(center)
 for r in range(1,rings+1):
  for edge in outline:
   uv=center+(edge-center)*(r/rings);verts.append(point(uv));uvs.append(uv)
 for j in range(256):faces.append((0,1+j,1+(j+1)%256))
 for r in range(rings-1):
  inner=1+r*256;outer=inner+256
  for j in range(256):faces.append((inner+j,outer+j,outer+(j+1)%256,inner+(j+1)%256))
 me=bpy.data.meshes.new(f'Scanned_maple_curvature_{variant}');me.from_pydata(verts,[],faces);me.materials.append(materials[variant%3]);uvlayer=me.uv_layers.new(name='Original_scan_UV')
 for poly in me.polygons:
  poly.use_smooth=True
  for li in poly.loop_indices:uvlayer.data[li].uv=uvs[me.loops[li].vertex_index]
 me.update();meshes.append(me)
rng=random.Random(1313);stride=541;assert len(coords)%stride==0;count=len(coords)//stride
for i in range(count):
 start=i*stride;edge=start+1+4*108;origin=Vector(coords[edge]);tip=Vector(coords[edge+54]);left=Vector(coords[edge+24]);right=Vector(coords[edge+84]);long=(tip-origin).normalized();side=(right-left).normalized();normal=side.cross(long).normalized();side=long.cross(normal).normalized();width=(tip-origin).length/1.14
 ob=bpy.data.objects.new(f'Scanned_maple_leaf_{i:04d}',meshes[i%6]);coll.objects.link(ob);ob.location=origin;ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Matrix((side,long,normal)).transposed().to_quaternion();ob.scale=(width,)*3
 # Preserve the attachment point while varying the scanned blade curvature.
for ob in list(coll.objects):
 if ob.name.startswith('Leaf_primary_vein'):bpy.data.objects.remove(ob,do_unlink=True)
 elif ob.name.startswith('Leaf_petiole') and ob.type=='CURVE':ob.data.bevel_depth=.00065
bpy.data.objects.remove(old,do_unlink=True)
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r13','source':'r12','status':'author_preview_not_accepted','changes':['Scanned maple lamina outlines converted to real meshes; no alpha billboards','Original 4K leaf albedo, roughness and normal maps','Physical scanned displacement, varied curvature and translucent response','Thicker connected petioles'],'leaf_count':count,'source_provenance':str((scan/'provenance.json').relative_to(ROOT)),'remaining':['Author visual check','Native head and trunk defects','Crown transition','Full independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.57));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
