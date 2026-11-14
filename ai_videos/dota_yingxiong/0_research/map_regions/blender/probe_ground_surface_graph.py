from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v025.blend'))
def trace(socket,depth=0):
 if depth>24:return 'depth_limit'
 if not socket.is_linked:
  v=getattr(socket,'default_value',None)
  return list(v) if hasattr(v,'__len__') and not isinstance(v,str) else v
 q=socket.links[0].from_node
 return {'name':q.name,'type':q.type,'image':q.image.name if q.type=='TEX_IMAGE' and q.image else None,'attribute':q.attribute_name if q.type=='ATTRIBUTE' else None,'operation':getattr(q,'operation',getattr(q,'blend_type',None)),'inputs':{f'{i}:{s.name}':trace(s,depth+1) for i,s in enumerate(q.inputs) if s.enabled and s.name not in ['Normal','Alpha']}}
report={}
for name in ['Continuous_ground','River_water']:
 mat=bpy.data.materials[name];bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');report[name]={k:trace(bs.inputs[k]) for k in ['Base Color','Roughness','Metallic','Transmission Weight']}
report['view']={'exposure':bpy.context.scene.view_settings.exposure,'look':bpy.context.scene.view_settings.look}
(OUT/'surface_graph_probe_v025.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SURFACE_GRAPH_SAVED',flush=True)
