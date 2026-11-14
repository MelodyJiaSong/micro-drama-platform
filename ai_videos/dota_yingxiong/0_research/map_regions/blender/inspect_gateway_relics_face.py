"""Head-scale render and geometry evidence before editing the human merchant."""
from pathlib import Path
import bpy,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_Gateway_Relics/model_3d'));out=folder/'face_diagnosis_r01';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r01/inspection/m303_r01.blend'));scene=bpy.context.scene;scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=1000;camera=scene.camera;camera.data.type='ORTHO';camera.data.ortho_scale=.38
rows=[{'name':o.name,'type':o.type,'matrix':list(map(list,o.matrix_world)),'dimensions':list(o.dimensions),'faces':len(o.data.polygons) if o.type=='MESH' else None,'materials':[s.material.name for s in o.material_slots if s.material]} for o in bpy.data.collections['ASSET_m303'].all_objects]
(out/'scene.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for name,loc in [('front',(0,-2,1.70)),('side',(1.3,-2,1.70))]:
 camera.location=loc;look_at(camera,(0,0,1.70));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
