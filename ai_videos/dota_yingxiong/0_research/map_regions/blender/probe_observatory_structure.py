from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));bpy.ops.wm.open_mainfile(filepath=str(folder/'r18/inspection/bg23_r18.blend'));coll=bpy.data.collections['ASSET_bg23'];report=[]
for o in coll.objects:
    if not o.hide_render and ('obelisk' in o.name.lower() or o.name.startswith('Question_mark')):report.append({'name':o.name,'type':o.type,'location':list(o.location),'bounds':[[min((o.matrix_world@__import__('mathutils').Vector(c))[i] for c in o.bound_box),max((o.matrix_world@__import__('mathutils').Vector(c))[i] for c in o.bound_box)] for i in range(3)]})
(folder/'r18/structure_probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
