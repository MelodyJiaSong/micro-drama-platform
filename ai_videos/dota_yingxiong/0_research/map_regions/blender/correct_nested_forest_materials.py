"""Tint actual nested leaf BSDFs in isolated copies and restore dark blighted soil."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v020.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v019.blend'))
changed=[]
def tint_tree(nt,path):
 for node in list(nt.nodes):
  if node.type=='GROUP' and node.node_tree:
   node.node_tree=node.node_tree.copy();node.node_tree.name='Blighted_'+node.node_tree.name;tint_tree(node.node_tree,path+'/'+node.name)
  elif node.type in ['BSDF_PRINCIPLED','BSDF_TRANSLUCENT','BSDF_DIFFUSE']:
   socket=node.inputs.get('Base Color') or node.inputs.get('Color')
   if socket is None:continue
   mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.10,.16,.075,1)
   if socket.is_linked:nt.links.new(socket.links[0].from_socket,mix.inputs[1])
   else:mix.inputs[1].default_value=socket.default_value
   nt.links.new(mix.outputs[0],socket);changed.append(path+'/'+node.name)
for mat in list(bpy.data.materials):
 if mat.name.startswith('Dark_forest_') and any(word in mat.name.lower() for word in ['leaf','leaves','foliage']):tint_tree(mat.node_tree,mat.name)
assert changed,'No actual leaf shading nodes changed'
ground=[]
for node in bpy.data.materials['Continuous_ground'].node_tree.nodes:
 if node.type=='HUE_SAT' and abs(node.inputs['Saturation'].default_value-.25)<.01 and node.inputs['Value'].default_value<.4:
  ground.append({'node':node.name,'old_value':node.inputs['Value'].default_value});node.inputs['Value'].default_value=.075
assert ground,'Blight shader branch missing'
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V020 CANDIDATE; nested leaf tint and blight require visual review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v020_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v019.blend','status':'candidate_pending_visual_review','nested_leaf_shader_paths':changed,'blight_nodes':ground,'shared_source_groups_changed':False,'geometry_and_navigation_changed':False},indent=2),encoding='utf-8');print('SAVED',dest,flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v020_{name}.png');bpy.ops.render.render(write_still=True)
