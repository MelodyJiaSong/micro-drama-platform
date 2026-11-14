"""Create a local anatomy source for repairing generated humanoid faces."""
from pathlib import Path
import bpy,sys,json,importlib,addon_utils
ADDON=Path('C:/Users/light/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/blender_org/mpfb')
addon_utils.enable('bl_ext.blender_org.mpfb',default_set=True)
HumanService=importlib.import_module('bl_ext.blender_org.mpfb.services.humanservice').HumanService
TargetService=importlib.import_module('bl_ext.blender_org.mpfb.services.targetservice').TargetService
for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
macro=TargetService.get_default_macro_info_dict();macro.update(gender=1,age=.82,muscle=.7,weight=.68)
macro['race']={'asian':0,'caucasian':1,'african':0}
human=HumanService.create_human(macro_detail_dict=macro)
human.name='Merchant_anatomy_source_M P F B'.replace(' ','')
for target,weight in [('head/head-scale-horiz-incr',.45),('head/head-round',.35),('head/head-scale-vert-decr',.25)]:
    TargetService.load_target(human,str(ADDON/'data/targets'/(target+'.target.gz')),weight=weight)
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d/anatomy_sources';OUT.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb_merchant_source.blend'))
coords=[human.matrix_world@v.co for v in human.data.vertices]
report={'source_addon':str(ADDON),'vertices':len(coords),'bounds':[[min(c[i] for c in coords),max(c[i] for c in coords)] for i in range(3)],'vertex_groups':[g.name for g in human.vertex_groups],'macro':macro,'status':'anatomy_source_not_asset'}
(OUT/'mpfb_probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
