"""Match scanned boulder tones to embedded strata and remove perched local clutter."""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v039.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v038.blend'))
changed=[]
for cname in ['RIVER_SCAN_boulder_01','RIVER_SCAN_coast_rocks_02']:
 collection=bpy.data.collections.get(cname)
 if not collection:continue
 for ob in collection.objects:
  if ob.type!='MESH':continue
  for i,old in enumerate(list(ob.data.materials)):
   mat=old.copy();mat.name=old.name+'_River_weathered';ob.data.materials[i]=mat;nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');source=bs.inputs['Base Color'].links[0].from_socket
   tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.35,.42,.43,1);l.new(source,tint.inputs[1])
   geo=n.new('ShaderNodeNewGeometry');xyz=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],xyz.inputs[0]);dry=n.new('ShaderNodeMapRange');dry.clamp=True;dry.interpolation_type='SMOOTHSTEP';dry.inputs['From Min'].default_value=-10.85;dry.inputs['From Max'].default_value=-10.15;l.new(xyz.outputs['Z'],dry.inputs[0])
   wet=n.new('ShaderNodeMapRange');wet.inputs['To Min'].default_value=.48;wet.inputs['To Max'].default_value=1;l.new(dry.outputs[0],wet.inputs[0]);multiply=n.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1;l.new(tint.outputs[0],multiply.inputs[1]);l.new(wet.outputs[0],multiply.inputs[2]);l.new(multiply.outputs[0],bs.inputs['Base Color'])
   rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.30;rough.inputs['To Max'].default_value=.82;l.new(dry.outputs[0],rough.inputs[0]);l.new(rough.outputs[0],bs.inputs['Roughness']);changed.append(mat.name)
report=json.loads((OUT/'environment_v038_report.json').read_text());hidden=[]
for ob in bpy.data.collections['17_River_bank_detail'].objects:
 if not ob.instance_collection or not ob.instance_collection.name.startswith('RIVER_SCAN_'):continue
 for row in report['patches']:
  if math.hypot(ob.location.x-row['anchor'][0],ob.location.y-row['anchor'][1])<4.5 and ob.location.z>row['z_range'][0]+1.3:
   ob.hide_render=True;ob.hide_viewport=True;hidden.append(ob.name);break
scene=bpy.context.scene;scene['production_status']='LOCAL_RIVER_ROCK_MATERIAL_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v039_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v038.blend','status':'local_author_trial_not_full_map_coverage','changed_materials':changed,'hidden_perched_boulder_instances':hidden,'remaining':['Only the 62 earlier local scan patches exist','Cliff coverage and repetition','Navigation collision verification for exposed triangles','Upper pools have no new wet-rock material transition']},indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.use_border=False
camera=bpy.data.objects['River_Eye_Level'];scene.camera=camera
scene.render.filepath=str(OUT/'environment_v039_River_Eye_Level.png');bpy.ops.render.render(write_still=True)
close=json.loads((OUT/'environment_v038_close_cameras.json').read_text())[0];camera.location=close['camera'];look_at(camera,Vector(close['target']));camera.data.type='PERSP';camera.data.lens=42
scene.render.filepath=str(OUT/'environment_v039_Rock_River_Close.png');bpy.ops.render.render(write_still=True)
