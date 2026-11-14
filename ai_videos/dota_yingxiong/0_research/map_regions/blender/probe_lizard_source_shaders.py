from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'r11/authoring.blend'))
source=bpy.data.objects['Archive_r07_lizard_before_closed_surface'];report={'mesh_vertices':len(source.data.vertices),'uv_layers':[uv.name for uv in source.data.uv_layers],'materials':[]}
for mat in source.data.materials:
 row={'name':mat.name,'textures':[],'shader_inputs':{}}
 for node in mat.node_tree.nodes:
  if node.type=='TEX_IMAGE' and node.image:row['textures'].append({'name':node.name,'image':node.image.name,'colorspace':node.image.colorspace_settings.name,'size':list(node.image.size)})
  if node.type=='BSDF_PRINCIPLED':row['shader_inputs']={s.name:([{'node':l.from_node.name,'socket':l.from_socket.name} for l in s.links] if s.is_linked else str(s.default_value)) for s in node.inputs if s.name in ['Base Color','Normal','Roughness','Metallic']}
 report['materials'].append(row)
(folder/'r11/source_shader_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
