"""Trial: close the perforated reconstruction and transfer baked source appearance."""
from pathlib import Path
import bpy,bmesh,json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m21_Polar_Furbolg/model_3d'));out=folder/'r11';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r10/authoring.blend'));coll=bpy.data.collections['ASSET_m21'];source=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));source.name='Archive_original_perforated_furbolg';me=source.data
# Bake actual shader colour in Blender's scene-linear pipeline; avoid guessing
# whether image.pixels needs an sRGB transfer or sampling across UV seams.
color=me.color_attributes.new(name='Baked_source_albedo',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=color
original_materials=list(me.materials)
for i,original in enumerate(original_materials):
 mat=original.copy();me.materials[i]=mat;nt=mat.node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(bs.inputs['Base Color'].links[0].from_socket,em.inputs['Color']);nt.links.new(em.outputs[0],next(q for q in nt.nodes if q.type=='OUTPUT_MATERIAL').inputs['Surface'])
bpy.ops.object.select_all(action='DESELECT');source.select_set(True);bpy.context.view_layer.objects.active=source;scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.bake.target='VERTEX_COLORS';bpy.ops.object.bake(type='EMIT');print('SOURCE_COLOR_BAKED',len(color.data),flush=True)
me.materials.clear()
for mat in original_materials:me.materials.append(mat)
# The second colour layer carries the authored leather coverage for shading only.
mask=me.color_attributes.new(name='Transferred_leather_mask',type='FLOAT_COLOR',domain='CORNER');indices=np.empty(len(me.loops),np.int32);me.loops.foreach_get('vertex_index',indices);coverage=np.empty(len(me.vertices),np.float32);me.attributes['LeatherCoverage'].data.foreach_get('value',coverage);rgba=np.ones((len(indices),4),np.float32);rgba[:,:3]=coverage[indices,None];mask.data.foreach_set('color',rgba.ravel())
body=source.copy();body.data=me.copy();body.name='Closed_furbolg_surface';coll.objects.link(body);source.hide_render=True;source.hide_viewport=True;bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
solid=body.modifiers.new('Close_thin_reconstruction_shell','SOLIDIFY');solid.thickness=.010;solid.offset=-.5;solid.use_quality_normals=True;bpy.ops.object.modifier_apply(modifier=solid.name);print('SHELL_CLOSED',flush=True)
remesh=body.modifiers.new('Voxel_surface_union_4mm','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.004;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name);smooth=body.modifiers.new('Reduce_reconstruction_surface_fins','SMOOTH');smooth.factor=.45;smooth.iterations=4;bpy.ops.object.modifier_apply(modifier=smooth.name);print('SURFACE_REBUILT',len(body.data.polygons),flush=True)
for name in ['Baked_source_albedo','Transferred_leather_mask']:
 if not body.data.color_attributes.get(name):body.data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='CORNER')
transfer=body.modifiers.new('Transfer_source_colours_by_nearest_surface','DATA_TRANSFER');transfer.object=source;transfer.use_loop_data=True;transfer.data_types_loops={'COLOR_CORNER'};transfer.loop_mapping='POLYINTERP_NEAREST';transfer.layers_vcol_loop_select_src='ALL';transfer.layers_vcol_loop_select_dst='NAME';bpy.ops.object.modifier_apply(modifier=transfer.name)
values=np.empty(len(body.data.color_attributes['Baked_source_albedo'].data)*4,np.float32);body.data.color_attributes['Baked_source_albedo'].data.foreach_get('color',values);assert np.max(values.reshape(-1,4)[:,:3])>.05,'Colour transfer empty'
mat=bpy.data.materials.new('Transferred_original_furbolg_surface_colour');mat.use_nodes=True;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=n.get('Principled BSDF');a=n.new('ShaderNodeVertexColor');a.layer_name='Baked_source_albedo';l.new(a.outputs['Color'],bs.inputs['Base Color']);a=n.new('ShaderNodeVertexColor');a.layer_name='Transferred_leather_mask';rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.83;rough.inputs['To Max'].default_value=.59;l.new(a.outputs['Color'],rough.inputs['Value']);l.new(rough.outputs[0],bs.inputs['Roughness']);bs.inputs['Specular IOR Level'].default_value=.2;body.data.materials.clear();body.data.materials.append(mat)
bm=bmesh.new();bm.from_mesh(body.data);topology={'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)};bm.free()
scene['production_status']='AUTHOR_TRIAL_NOT_ACCEPTED';scene.render.bake.target='IMAGE_TEXTURES';scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m21','revision':'r11','source':'r10','status':'author_trial_not_accepted','changes':['Bake actual source shader colour to linear corner attributes','10mm closed shell followed by 4mm voxel union and four smoothing iterations','Nearest-surface colour and leather-mask transfer; original groom retained'],'topology':topology,'remaining':['Colour transfer fidelity','Head, mouth and hair-root contacts','Cape holes and silhouette','All prior proportion blockers remain until checked']},indent=2),encoding='utf-8');print('COLOR_TRANSFER_TRIAL_SAVED',flush=True)
for name,loc,target,scale in [('author_preview',(6,-7,3),(0,0,1.15),2.9),('face_detail',(.5,-3,1.8),(0,-.40,1.61),.72)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
