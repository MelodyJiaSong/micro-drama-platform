from pathlib import Path
import bpy,json,collections
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'))
used={s.material for o in bpy.context.scene.objects if not o.hide_render for s in o.material_slots if s.material}
for m in used:
 if not m.use_nodes:continue
 print(json.dumps({'material':m.name,'nodes':dict(collections.Counter(n.type for n in m.node_tree.nodes)),'outputs':[(n.name,[(l.from_node.name,l.from_socket.name,l.to_socket.name) for l in m.node_tree.links if l.to_node==n]) for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL']}),flush=True)
