"""Correct dry-soil reflection after a same-camera no-specular diagnostic."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v031.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v030.blend'));mat=bpy.data.materials['Continuous_ground'];nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED')
prior={'specular_ior_level':bs.inputs['Specular IOR Level'].default_value,'ior':bs.inputs['IOR'].default_value};bs.inputs['IOR'].default_value=1.42
def calc(op,a,b):
 q=n.new('ShaderNodeMath');q.operation=op
 for socket,value in zip(q.inputs,[a,b]):
  if isinstance(value,(int,float)):socket.default_value=value
  else:l.new(value,socket)
 return q.outputs[0]
shore=n.new('ShaderNodeAttribute');shore.attribute_name='Actual_shore_distance_mask';geo=n.new('ShaderNodeNewGeometry');xyz=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],xyz.inputs[0]);wet=n.new('ShaderNodeMapRange');wet.clamp=True;wet.inputs['From Min'].default_value=-6.85;wet.inputs['From Max'].default_value=-6.10;wet.inputs['To Min'].default_value=1;wet.inputs['To Max'].default_value=0;l.new(xyz.outputs['Z'],wet.inputs['Value']);moist=calc('MULTIPLY',wet.outputs[0],shore.outputs['Fac']);paving=n.new('ShaderNodeAttribute');paving.attribute_name='Paving'
spec=calc('ADD',.10,calc('ADD',calc('MULTIPLY',moist,.30),calc('MULTIPLY',paving.outputs['Fac'],.10)));l.new(spec,bs.inputs['Specular IOR Level']);rough=calc('SUBTRACT',.94,calc('ADD',calc('MULTIPLY',moist,.60),calc('MULTIPLY',paving.outputs['Fac'],.13)));l.new(rough,bs.inputs['Roughness'])
if bs.inputs.get('Diffuse Roughness'):bs.inputs['Diffuse Roughness'].default_value=.35
# Earlier darkening compensated for the washed-out reflection. Restore a modest
# diffuse ash reflectance now that the reflection is independently controlled.
ash=next(q for q in n if q.type=='HUE_SAT');prior['ash_value']=ash.inputs['Value'].default_value;ash.inputs['Value'].default_value=.24;ash.inputs['Saturation'].default_value=.40
normal=bs.inputs['Normal'].links[0].from_socket if bs.inputs['Normal'].is_linked else None;grain=n.new('ShaderNodeTexNoise');grain.inputs['Scale'].default_value=110;grain.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],grain.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.20;bump.inputs['Distance'].default_value=.0025;l.new(grain.outputs['Fac'],bump.inputs['Height'])
if normal:l.new(normal,bump.inputs['Normal'])
l.new(bump.outputs[0],bs.inputs['Normal']);scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V031 MATERIAL TRIAL; independently unaccepted';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report=json.loads((OUT/'environment_v030_report.json').read_text());report.update(file=dest.name,source='environment_v030.blend',status='candidate_pending_author_view',reflectance_change={'diagnosis':'ground_reflectance_v030/no_specular.png versus unchanged v030 Scourge_Base: broad pale reflection hides diffuse soil variation','prior':prior,'dry_specular_ior_level':.10,'wet_addition':.30,'paving_addition':.10,'ior':1.42,'dry_roughness':.94,'wet_roughness_min':.34,'ash_value':.24,'micrograin_bump_distance_m':.0025},terrain_navigation_and_water_unchanged=True);(OUT/'environment_v031_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Scourge_Base','River_Eye_Level','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v031_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
