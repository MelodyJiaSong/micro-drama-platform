"""Place bone roots inside the lower bronze sleeves, avoiding exposed flat caps."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg26_*/model_3d'));out=folder/'r12';out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r11/authoring.blend'));coll=bpy.data.collections['ASSET_bg26'];ribs=[o for o in coll.objects if o.name.startswith('Continuous_structural_bronze_rib')]
for claw in [o for o in coll.objects if o.name.startswith('Large_outward_basal_bone_claw')]:
 p=claw.data.splines[0].bezier_points;rib=min(ribs,key=lambda o:(o.data.splines[0].bezier_points[0].co-p[0].co).length);a,b=rib.data.splines[0].bezier_points[:2];t=(1.55-a.co.z)/(b.co.z-a.co.z);p[0].co=a.co.lerp(b.co,t);p[0].radius=.45;p[1].radius=.94;p[2].radius=.52;p[3].radius=.025
scene=bpy.context.scene;scene.cycles.samples=48;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps({'asset_id':'bg26','revision':'r12','source':'r11','status':'author_preview_not_accepted','changes':['Seated narrow bone roots inside lower bronze sleeves'],'remaining':['Full multi-angle and independent inspection','Crystal fissure and surface weathering realism']},indent=2),encoding='utf-8');scene.render.filepath=str(out/'tower_preview.png');bpy.ops.render.render(write_still=True)
