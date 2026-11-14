"""Use the real assembly path to inspect the canonical Thunder Lizard camp."""
from pathlib import Path
from argparse import Namespace
import bpy,json,sys,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));import assemble_map;from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';name='camp_K8_RAO_v001.blend';assemble_map.main(Namespace(environment='environment_v031.blend',output=name,draft=True,only_assets=['m26'],camp_overrides=['K8=RAO']))
camp=bpy.data.collections['10_Neutral_Camps'];units=[o for o in camp.objects if o.get('camp')=='K8'];assert len(units)==3
# An object-linked material override keeps source meshes and the large variant
# unchanged, while providing the card's smaller grey-green variant.
source=units[0].instance_collection;variant=bpy.data.collections.new('VARIANT_m26_small_grey');variant.instance_offset=source.instance_offset;mapping={};mats={}
for ob in source.all_objects:
 if ob.hide_render:continue
 copy=ob.copy();variant.objects.link(copy);mapping[ob]=copy
for ob,copy in mapping.items():
 copy.parent=mapping.get(ob.parent);copy.matrix_world=ob.matrix_world
 for slot in copy.material_slots:
  mat=slot.material
  if not mat:continue
  if mat not in mats:
   new=mat.copy();new.name='Small_lizard_grey_'+mat.name
   for node in new.node_tree.nodes:
    if node.type=='HUE_SAT':node.inputs['Hue'].default_value=.5;node.inputs['Saturation'].default_value=.12;node.inputs['Value'].default_value=.90
   mats[mat]=new
  slot.link='OBJECT';slot.material=mats[mat]
for ob in units:
 if ob.get('rawcode')=='n0LD':ob.instance_collection=variant;ob['variant_status']='small_grey_material_author_preview_not_accepted'
center=sum((o.location for o in units),Vector())/len(units);scene=bpy.context.scene;scene['production_status']='CANONICAL_CAMP_DIAGNOSTIC_NOT_ACCEPTED';camera=bpy.data.cameras.new('Thunder_lizard_camp_camera');ob=bpy.data.objects.new('Thunder_lizard_camp_camera',camera);scene.collection.objects.link(ob);ob.location=center+Vector((14,-19,10));look_at(ob,center+Vector((0,0,1)));camera.lens=48;scene.camera=ob
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/name));report=json.loads((OUT/'camp_K8_RAO_v001_report.json').read_text(encoding='utf-8'));report['small_variant_material']='Object-linked copy, skin hue saturation .12; colour and contact remain author-preview-only';report['camera']=list(ob.location);(OUT/'camp_K8_RAO_v001_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.filepath=str(OUT/'camp_K8_RAO_v001.png');bpy.ops.render.render(write_still=True);print('CAMP_PREVIEW_SAVED',flush=True)
