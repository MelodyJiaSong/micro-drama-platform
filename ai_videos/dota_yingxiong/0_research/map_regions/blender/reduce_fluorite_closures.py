"""Replace zero-density Principled Volume with its emission-only equivalent."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r08';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'))
nt=bpy.data.materials['Tower_faceted_fluorite_shell'].node_tree;vol=next(n for n in nt.nodes if n.type=='PRINCIPLED_VOLUME')
assert not vol.inputs['Density'].is_linked and vol.inputs['Density'].default_value==0
assert not vol.inputs['Blackbody Intensity'].is_linked and vol.inputs['Blackbody Intensity'].default_value==0
em=nt.nodes.new('ShaderNodeEmission');em.name='Mineral_volume_emission_only';em.inputs['Color'].default_value=vol.inputs['Emission Color'].default_value
if vol.inputs['Emission Strength'].is_linked:nt.links.new(vol.inputs['Emission Strength'].links[0].from_socket,em.inputs['Strength'])
else:em.inputs['Strength'].default_value=vol.inputs['Emission Strength'].default_value
for link in list(vol.outputs[0].links):nt.links.new(em.outputs[0],link.to_socket)
nt.nodes.remove(vol)
scene=bpy.context.scene;scene.render.filepath=str(out/'tower_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
(out/'authoring.json').write_text(json.dumps({'revision':'r08','source':'r07','status':'author_preview_pending','changes':['Replaced zero-density, zero-blackbody Principled Volume by volume Emission shader','Absorption, surface refraction, emission colour and strength field preserved'],'reason':'r07 renderer reported conservative closure count 76 > 64','remaining':['Verify appearance and renderer warning, then independent review']},indent=2),encoding='utf-8');bpy.ops.render.render(write_still=True)
