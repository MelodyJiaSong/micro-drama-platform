"""Balance cyan light, soft short fibres, and a sparse fading wake."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m306_*/model_3d'));out=folder/'r17';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r16/authoring.blend'));coll=bpy.data.collections['ASSET_m306'];center=Vector((0,0,1))
for ob in coll.objects:
 if ob.hide_render:continue
 if ob.name=='Six_curving_light_fibres':
  ob.data.bevel_depth=.00018
  for s in ob.data.splines:
   for p in s.points:p.co=(*(center+(Vector(p.co[:3])-center)*.72),1)
  nt=ob.data.materials[0].node_tree;nt.nodes.get('Emission').inputs[0].default_value=(.12,.65,1,1)
  fade=next(n for n in nt.nodes if n.type=='MAP_RANGE');fade.inputs['From Max'].default_value=.21;fade.inputs['To Min'].default_value=40
 elif ob.name=='Visible_organic_Fuzz':
  ob.data.bevel_depth=.00011
  for s in ob.data.splines:
   for p in s.points:p.co=(*(center+(Vector(p.co[:3])-center)*1.35),1)
  em=ob.data.materials[0].node_tree.nodes.get('Emission');em.inputs[0].default_value=(.13,.65,1,1);em.inputs[1].default_value=19
 elif ob.name=='Tapered_particle_wake':
  attr=ob.data.attributes['DustFade'];colors=np.empty(len(attr.data)*4,np.float32);attr.data.foreach_get('color',colors);colors=colors.reshape(-1,4);colors[:,:3]*=(.25,.8,1);attr.data.foreach_set('color',colors.ravel());ob.data.materials[0].node_tree.nodes.get('Emission').inputs[1].default_value=10
 elif ob.name=='Soft_particle_wake_volume':
  for n in ob.data.materials[0].node_tree.nodes:
   if n.type=='PRINCIPLED_VOLUME':n.inputs['Emission Color'].default_value=(.10,.62,1,1)
   if n.type=='MATH' and n.operation=='MULTIPLY' and not n.inputs[1].is_linked and abs(n.inputs[1].default_value-28)<.01:n.inputs[1].default_value=10
 if ob.type=='LIGHT':ob.data.color=(.30,.78,1)
for n in bpy.data.materials['Cyan_atmospheric_fringe'].node_tree.nodes:
 if n.type=='PRINCIPLED_VOLUME':n.inputs['Emission Color'].default_value=(.12,.65,1,1)
scene=bpy.context.scene;glare=next(n for n in scene.compositing_node_group.nodes if n.type=='GLARE');glare.inputs['Threshold'].default_value=.35;glare.inputs['Strength'].default_value=1.1;glare.inputs['Size'].default_value=.28
scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera.data.ortho_scale=.72;scene.camera.location=(1.1,-1.6,1.25);look_at(scene.camera,(0,.05,1))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'revision':'r17','status':'author_preview_pending','source':'r16','changes':['Long fibres shortened to 72 percent, short fuzz extended to 135 percent','Cyan emission retained in outer filaments and dust','Less luminous continuous tail volume; optical bloom applied consistently'],'main_filaments':6,'short_fuzz_filaments':600,'dust_particles':1900,'tail_length_m':.38,'remaining':['All-view appearance and translated-instance checks pending']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'close_preview.png');bpy.ops.render.render(write_still=True)
