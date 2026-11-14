"""Keep the preserved source geometry; remove nonphysical metallic wood response."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r09';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r08/inspection/m1_r08.blend'));coll=bpy.data.collections['ASSET_m1'];materials={slot.material for o in coll.objects if o.type=='MESH' for slot in o.material_slots}
for mat in materials:
 nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF')
 for key,value in [('Metallic',0),('Roughness',.82)]:
  for link in list(bs.inputs[key].links):nt.links.remove(link)
  bs.inputs[key].default_value=value
 old=bs.inputs['Base Color'].links[0].from_socket;hue=nt.nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=1.25;hue.inputs['Value'].default_value=.8;nt.links.new(old,hue.inputs['Color']);nt.links.new(hue.outputs['Color'],bs.inputs['Base Color'])
for ob in bpy.context.scene.objects:
 if ob.type=='LIGHT' and ob not in set(coll.all_objects):ob.data.energy*=.4
scene=bpy.context.scene;scene.cycles.samples=48;scene.cycles.device='CPU';scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r09','source':'r08','status':'author_preview_not_accepted','changes':['Preserved 2.79M-face non-remeshed geometry','Nonmetallic rough wood and foliage','Mild saturation and value adjustment','Studio power 40% of baseline'],'geometry_changed':False,'remaining':['Source shape, leaf identity and physical topology still require full review']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
