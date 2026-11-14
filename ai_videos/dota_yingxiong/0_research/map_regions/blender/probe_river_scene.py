from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v016.blend'))
result={'objects':[],'materials':[],'cameras':{}}
for o in bpy.data.objects:
 if any(s in o.name.lower() for s in ['water','river','bank','outer_land','atmosphere']):
  result['objects'].append({'name':o.name,'type':o.type,'location':list(o.location),'scale':list(o.scale),'dimensions':list(o.dimensions),'materials':[m.name for m in o.data.materials] if o.type=='MESH' else [],'hidden':o.hide_render})
for m in bpy.data.materials:
 if 'water' not in m.name.lower():continue
 result['materials'].append({'name':m.name,'nodes':[{'name':n.name,'type':n.type,'inputs':{s.name:str(s.default_value) for s in n.inputs if hasattr(s,'default_value') and not s.is_linked}} for n in m.node_tree.nodes]})
for name in ['Mid_River','River_Eye_Level']:
 o=bpy.data.objects.get(name)
 if o:result['cameras'][name]={'location':list(o.location),'rotation':list(o.rotation_euler)}
(OUT/'river_scene_probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('PROBE_DONE',flush=True)
