"""Reduce r22's excessive pale coverage and broad white leaf reflections."""
from pathlib import Path
import bpy,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m1_Treant/model_3d'));out=folder/'r23';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r22/authoring.blend'));coll=bpy.data.collections['ASSET_m1'];body=max((o for o in coll.objects if o.type=='MESH'),key=lambda o:len(o.data.polygons));changed=[]
replacements={(.39,.57):(.505,.545),(.38,.57):(.525,.57),(.53,.67):(.42,.58),(.35,.55):(.37,.55)}
for node in body.data.materials[0].node_tree.nodes:
 if node.type=='MAP_RANGE':
  pair=(round(node.inputs['From Min'].default_value,3),round(node.inputs['From Max'].default_value,3))
  if pair in replacements:
   lo,hi=replacements[pair];node.inputs['From Min'].default_value=lo;node.inputs['From Max'].default_value=hi;changed.append([node.name,pair,(lo,hi)])
 elif node.type=='MIX_RGB':
  color=node.inputs[2].default_value
  if abs(color[0]-.26)<.001 and abs(color[1]-.29)<.001:node.inputs[2].default_value=(.18,.21,.17,1)
assert len(changed)==4,changed
for mat in [m for m in bpy.data.materials if m.name.startswith('Scanned_dark_living_maple')]:
 for node in mat.node_tree.nodes:
  if node.type=='BSDF_PRINCIPLED':node.inputs['Coat Weight'].default_value=0;node.inputs['Specular IOR Level'].default_value=.065;node.inputs['Roughness'].default_value=.68
  elif node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.65
scene=bpy.context.scene;scene.cycles.samples=64;scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera.location=(0,-6,1.25);scene.camera.data.ortho_scale=2.25;look_at(scene.camera,(0,0,.95));scene['production_status']='AUTHOR_PREVIEW_NOT_ACCEPTED'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'asset_id':'m1','revision':'r23','source':'r22','status':'author_preview_not_accepted','changes':['Crisp scattered pale lichen rather than continuous pale wash','More dark green moss','Reduce broad white leaf coat reflections'],'mask_changes':changed,'remaining':['Crown anatomy and head separation','Leaf/branch transitions','Independent review']},indent=2),encoding='utf-8')
scene.render.filepath=str(out/'author_preview.png');bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale=.9;scene.camera.location=(.4,-3,1.9);look_at(scene.camera,(0,0,1.55));scene.render.filepath=str(out/'crown_detail.png');bpy.ops.render.render(write_still=True)
