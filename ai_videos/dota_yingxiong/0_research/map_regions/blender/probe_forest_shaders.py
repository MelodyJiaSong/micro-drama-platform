from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v019.blend'))
def scan(nt,depth=0):
 if depth>5:return []
 return [{'name':n.name,'type':n.type,'group':n.node_tree.name if n.type=='GROUP' and n.node_tree else None,'nested':scan(n.node_tree,depth+1) if n.type=='GROUP' and n.node_tree else []} for n in nt.nodes]
data={}
for ob in bpy.data.collections['LIB_Tree_5'].objects:
 if ob.type=='MESH':
  for mat in ob.data.materials:data[mat.name]=scan(mat.node_tree)
(OUT/'forest_shader_probe.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print(json.dumps(data),flush=True)
