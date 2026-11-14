"""Repair r04 material discontinuity and detached cloth remnants before review."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'));folder=next(WORLD.glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r05';out.mkdir(exist_ok=True);scan=WORLD/'background/map_3d/environment_sources/brown_leather'
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r04/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];cloth=bpy.data.objects['Reconstructed_leather_cape_shell'];body=max((o for o in coll.objects if o.type=='MESH' and o!=cloth),key=lambda o:len(o.data.polygons))
bm=bmesh.new();bm.from_mesh(cloth.data);unseen=set(bm.verts);groups=[]
while unseen:
 first=unseen.pop();group=[first];pending=[first]
 while pending:
  v=pending.pop()
  for edge in v.link_edges:
   other=edge.other_vert(v)
   if other in unseen:unseen.remove(other);pending.append(other);group.append(other)
 groups.append(group)
groups.sort(key=len,reverse=True);total=sum(map(len,groups));removed=0
for group in groups[1:]:
 if len(group)<max(1000,total*.01):bmesh.ops.delete(bm,geom=group,context='VERTS');removed+=len(group)
bm.to_mesh(cloth.data);bm.free();cloth.data.update();print('CLOTH_COMPONENTS',len(groups),'REMOVED_VERTS',removed,flush=True)
bpy.ops.object.select_all(action='DESELECT');cloth.select_set(True);bpy.context.view_layer.objects.active=cloth;mod=cloth.modifiers.new('Reduce_reconstruction_lumps','SMOOTH');mod.factor=.70;mod.iterations=30;bpy.ops.object.modifier_apply(modifier=mod.name)
def leather_nodes(mat):
 nt=mat.node_tree;n,l=nt.nodes,nt.links;coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=2.5;l.new(coord.outputs['Object'],mapping.inputs[0]);maps={}
 for key,pattern in [('color','*albedo*jpg'),('rough','*rough*jpg'),('height','*disp*png')]:
  tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(next(scan.glob(pattern))),check_existing=True);tex.projection='BOX';tex.projection_blend=.25;l.new(mapping.outputs[0],tex.inputs['Vector']);maps[key]=tex.outputs['Color']
 tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.10,.085,.065,1);l.new(maps['color'],tint.inputs[1]);rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.74;rough.inputs['To Max'].default_value=.94;l.new(maps['rough'],rough.inputs['Value']);return tint.outputs[0],rough.outputs[0],maps['height']
mat=cloth.data.materials[0];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');color,rough,height=leather_nodes(mat);nt.links.new(color,bs.inputs['Base Color']);nt.links.new(rough,bs.inputs['Roughness']);bs.inputs['Specular IOR Level'].default_value=.16
# Match the retained lower cape strip to the rebuilt shell, using the existing surface mask.
mat=body.data.materials[0];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(n for n in n if n.type=='BSDF_PRINCIPLED');old=bs.inputs['Base Color'].links[0].from_socket;color,rough,height=leather_nodes(mat);attr=n.new('ShaderNodeAttribute');attr.attribute_name='LeatherCoverage';mask=n.new('ShaderNodeMapRange');mask.clamp=True;mask.interpolation_type='SMOOTHSTEP';mask.inputs['From Min'].default_value=.05;mask.inputs['From Max'].default_value=.50;l.new(attr.outputs['Fac'],mask.inputs['Value']);mix=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],mix.inputs[0]);l.new(old,mix.inputs[1]);l.new(color,mix.inputs[2]);l.new(mix.outputs[0],bs.inputs['Base Color'])
roughmix=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],roughmix.inputs[0]);l.new(rough,roughmix.inputs[2])
if bs.inputs['Roughness'].is_linked:l.new(bs.inputs['Roughness'].links[0].from_socket,roughmix.inputs[1])
else:roughmix.inputs[1].default_value=(*([bs.inputs['Roughness'].default_value]*3),1)
l.new(roughmix.outputs[0],bs.inputs['Roughness'])
wood=bpy.data.materials['Weathered_solid_wood_poles'];nt=wood.node_tree;bs=nt.nodes.get('Principled BSDF');source=bs.inputs['Base Color'].links[0].from_socket;tint=nt.nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.12,.09,.06,1);nt.links.new(source,tint.inputs[1]);nt.links.new(tint.outputs[0],bs.inputs['Base Color']);bs.inputs['Specular IOR Level'].default_value=.12
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(6,-7,3);scene.camera.data.ortho_scale=2.9;look_at(scene.camera,(0,0,1.15));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r05','source':'r04','status':'author_preview_not_accepted','changes':['Remove detached cape fragments','Smooth remeshed reconstruction lumps','Shared dark matte scanned leather across both cape sections','Dark weathered pole colour'],'removed_cape_vertices':removed,'remaining':['Cape/body boundary and smoothness','All-angle author inspection','Independent review']},indent=2),encoding='utf-8');print('CAPE_SURFACE_SAVED',flush=True)
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.location=(3,4,3.2);scene.camera.data.ortho_scale=1.5;look_at(scene.camera,(0,.1,1.8));scene.render.filepath=str(out/'roof_poles_preview.png');bpy.ops.render.render(write_still=True)
