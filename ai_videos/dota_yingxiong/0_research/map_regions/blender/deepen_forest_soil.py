"""Earth reflectance and spatially varied grass clump scale; no terrain movement."""
from pathlib import Path
import bpy,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v015.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v014.blend'));nt=bpy.data.materials['Continuous_ground'].node_tree;changed=[]
for n in nt.nodes:
 if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY' and n.inputs[1].is_linked:
  source=n.inputs[1].links[0].from_node
  if source.type=='TEX_IMAGE' and source.image and source.image.name in ['grass_ground_diff_2k.jpg','leafy_grass_diff_2k.jpg']:
   changed.append({'node':n.name,'old_factor':n.inputs[0].default_value,'old_tint':list(n.inputs[2].default_value)})
   n.inputs[0].default_value=1;n.inputs[2].default_value=(.26,.23,.17,1)
assert len(changed)==2,changed
ob=bpy.data.objects['Living_ground_grass'];me=ob.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
sc=np.empty(len(me.vertices)*3,np.float32);me.attributes['clump_scale'].data.foreach_get('vector',sc);sc=sc.reshape(-1,3)
x,y=co[:,0],co[:,1];patch=np.clip(.5+.3*np.sin(x*.82+y*.37)*np.sin(y*.63-x*.25)+.2*np.sin(x*.23-y*.44),0,1)
rng=np.random.default_rng(15015);factor=.24+1.05*patch+rng.uniform(-.08,.08,len(x));sc*=factor[:,None];me.attributes['clump_scale'].data.foreach_set('vector',sc.ravel());me.update()
scene=bpy.context.scene;scene.camera=bpy.data.objects['Sentinel_Merchant_Ground_Eye'];scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=1000
scene['production_status']='ENVIRONMENT V015 CANDIDATE; earth reflectance and spatial grass variation awaiting review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v015_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v014.blend','status':'candidate_pending_visual_inspection','changes':changed,'terrain_and_navigation_changed':False,'vegetation_change':'Spatially correlated clump-scale variation; point anchors unchanged','scale_factor_range':[float(factor.min()),float(factor.max())]},indent=2),encoding='utf-8')
scene.render.filepath=str(OUT/'environment_v015_Merchant_Ground.png');bpy.ops.render.render(write_still=True)
