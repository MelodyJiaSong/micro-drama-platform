"""Read-only geometry evidence for the merchant's raised platform anchor."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];W=next(ROOT.glob('2_*'));p=next(W.glob('background/*/bg12_*/model_3d/r08/inspection/bg12_r08.blend'))
bpy.ops.wm.open_mainfile(filepath=str(p));coll=bpy.data.collections['ASSET_bg12'];rows=[]
for ob in coll.all_objects:
 if ob.hide_render:continue
 bounds=[ob.matrix_world@Vector(v) for v in ob.bound_box]
 rows.append({'name':ob.name,'type':ob.type,'min':[min(v[i] for v in bounds) for i in range(3)],'max':[max(v[i] for v in bounds) for i in range(3)],'materials':[m.name for m in getattr(ob.data,'materials',[]) if m]})
surface=bpy.data.objects['geometry_0'];inverse=surface.matrix_world.inverted();rays=[]
for x in [.5,1,1.5,2,2.5,3]:
 for y in [-2.5,-2,-1.5,-1]:
  hit,point,n,index=surface.ray_cast(inverse@Vector((x,y,3.2)),inverse.to_3x3()@Vector((0,0,-1)))
  if hit:rays.append({'xy':[x,y],'hit':list(surface.matrix_world@point),'normal':list((surface.matrix_world.to_3x3().inverted().transposed()@n).normalized())})
report={'objects':rows,'platform_rays':rays,'camera':{'location':list(bpy.context.scene.camera.location),'matrix':[list(v) for v in bpy.context.scene.camera.matrix_world]}}
(p.parent/'platform_anchor_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
