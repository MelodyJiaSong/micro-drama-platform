from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/anatomy_sources'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb_merchant_source.blend'));o=next(o for o in bpy.context.scene.objects if o.type=='MESH');ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
# Read shape-key evaluated positions without the mask (helper landmarks must stay).
for m in o.modifiers:m.show_viewport=False
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();coords=[v.co for v in me.vertices];report={}
for name in ['joint-head','joint-head-2','joint-neck','joint-jaw','joint-mouth','joint-l-eye','joint-r-eye','helper-l-eye','helper-upper-teeth','helper-lower-teeth']:
    gi=o.vertex_groups[name].index;ids=[v.index for v in o.data.vertices if any(g.group==gi and g.weight>.1 for g in v.groups)];vv=[coords[i] for i in ids];report[name]={'n':len(vv),'center':[sum(v[j] for v in vv)/len(vv) for j in range(3)],'bounds':[[min(v[j] for v in vv),max(v[j] for v in vv)] for j in range(3)]}
(OUT/'landmarks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
