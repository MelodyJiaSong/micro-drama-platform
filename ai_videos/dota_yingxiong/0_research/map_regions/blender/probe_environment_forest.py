from pathlib import Path
import bpy,json,collections
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v024.blend'))
rows=[]
for i in range(8):
 c=bpy.data.collections.get(f'LIB_Tree_{i}')
 if not c:continue
 objects=[]
 for o in c.objects:
  mats=[]
  if o.type=='MESH':
   counts=collections.Counter(p.material_index for p in o.data.polygons)
   mats=[{'index':j,'name':m.name if m else None,'faces':counts[j]} for j,m in enumerate(o.data.materials)]
  objects.append({'name':o.name,'type':o.type,'dimensions':list(o.dimensions),'materials':mats})
 anchors=[o for o in bpy.data.collections['02_Forest'].objects if o.instance_collection==c]
 rows.append({'collection':c.name,'objects':objects,'anchor_count':len(anchors),'scale_range':[[min(o.scale[j] for o in anchors),max(o.scale[j] for o in anchors)] for j in range(3)] if anchors else [],'sample_positions':[list(o.location) for o in anchors[:3]]})
(OUT/'forest_geometry_probe_v024.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows),flush=True)
