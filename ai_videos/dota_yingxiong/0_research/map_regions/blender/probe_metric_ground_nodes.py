"""Record elevation-dependent ground shader nodes before adapting water height."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v032.blend'))
nodes=[]
for n in bpy.data.materials['Continuous_ground'].node_tree.nodes:
 if n.type not in ['MAP_RANGE','ATTRIBUTE','TEX_IMAGE']:continue
 nodes.append({'name':n.name,'type':n.type,'attribute':getattr(n,'attribute_name',None),'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,'inputs':{s.name:({'node':s.links[0].from_node.name,'socket':s.links[0].from_socket.name} if s.is_linked else float(s.default_value) if isinstance(getattr(s,'default_value',None),(int,float)) else None) for s in n.inputs if s.enabled}})
(OUT/'metric_ground_shader_probe.json').write_text(json.dumps(nodes,indent=2),encoding='utf-8')
print(json.dumps([n for n in nodes if n['type']=='MAP_RANGE']),flush=True)
