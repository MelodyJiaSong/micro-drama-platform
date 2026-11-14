"""Isolate authored/canonical cliff contributions in a narrow overhead render crop."""
from pathlib import Path
import bpy,json,collections
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v022.blend'));report={}
for name in ['04_Environment_Details','07_Cliff_Relief']:
 coll=bpy.data.collections.get(name)
 if coll:report[name]={'objects':len(coll.objects),'instance_collections':dict(collections.Counter(o.instance_collection.name if o.instance_collection else o.type for o in coll.objects))}
(OUT/'cliff_source_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene=bpy.context.scene;scene.camera=bpy.data.objects['Map_Overview'];scene.cycles.device='CPU';scene.cycles.samples=12;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1000;scene.render.resolution_y=750;scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=0;scene.render.border_max_x=1;scene.render.border_min_y=.75;scene.render.border_max_y=1
for variant in ['all','without_authored_cliff_rocks','without_authored_and_canonical_props']:
 if variant!='all':bpy.data.collections['07_Cliff_Relief'].hide_render=True
 if variant=='without_authored_and_canonical_props':bpy.data.collections['04_Environment_Details'].hide_render=True
 scene.render.filepath=str(OUT/('cliff_source_'+variant+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',variant,flush=True)
