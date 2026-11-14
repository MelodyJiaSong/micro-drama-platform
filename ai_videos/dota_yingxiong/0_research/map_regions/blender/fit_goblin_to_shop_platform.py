"""Inspect the separate goblin on the building's measured wooden platform."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];W=next(ROOT.glob('2_*'));OUT=W/'background/map_3d';dest=OUT/'side_shop_merchant_fit_v001.blend'
if dest.exists():raise FileExistsError(dest)
shop=next(W.glob('background/*/bg12_*/model_3d/r08/inspection/bg12_r08.blend'));merchant=next(W.glob('characters/*/m309_*/model_3d/r01/inspection/m309_r01.blend'))
bpy.ops.wm.open_mainfile(filepath=str(shop))
with bpy.data.libraries.load(str(merchant),link=True) as (src,dst):dst.collections=['ASSET_m309']
coll=bpy.data.collections.new('SHOP_MERCHANT_PLACEMENT');bpy.context.scene.collection.children.link(coll);ob=bpy.data.objects.new('m309_on_right_shop_platform',None);coll.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=dst.collections[0];ob.location=(1.5,-1.05,2.805);ob['asset_id']='m309';ob['source']='m309 asset card: right raised platform of bg12; original game embeds merchant in building mesh';ob['status']='local_anchor_trial_pending_contact_view'
scene=bpy.context.scene;scene['production_status']='SHOP_PLATFORM_CONTACT_TRIAL_NOT_ACCEPTED';bpy.ops.wm.save_as_mainfile(filepath=str(dest))
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('overview',(7,-15,8),(0,0,3.4),9),('contact',(4,-8,5),(1.5,-1,3.15),2.3)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=scale;scene.render.filepath=str(OUT/f'side_shop_merchant_fit_v001_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
(OUT/'side_shop_merchant_anchor_v001.json').write_text(json.dumps({'status':'author_view_pending_not_accepted','host_asset':'bg12','host_revision':'r08','merchant_asset':'m309','merchant_revision':'r01','local_position':list(ob.location),'facing':'-Y source assumption pending visual check','placement_source':'m309 asset card and bg12 platform ray hits','merchant_original_coordinate':'Embedded in original building; use host instance transform, no invented independent game coordinate','remaining':['Foot contact and roof/wall clearance','Merchant appearance remains independently failed','Apply to both u010 side shop instances after anchor inspection']},indent=2),encoding='utf-8')
