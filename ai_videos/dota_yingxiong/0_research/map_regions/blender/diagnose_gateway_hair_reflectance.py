"""Read shader evidence and isolate emitted base colour in an unsaved control."""
from pathlib import Path
import bpy,json,numpy as np,sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d/r04'))
bpy.ops.wm.open_mainfile(filepath=str(folder/'authoring.blend'));body=bpy.data.objects['Gateway_merchant_body'];rows=[]
for mat in body.data.materials:
 bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');rows.append({'material':mat.name,'inputs':{i.name:{'value':list(i.default_value) if hasattr(i.default_value,'__len__') else i.default_value,'linked':i.is_linked} for i in bs.inputs if hasattr(i,'default_value') and i.name in ['Base Color','Roughness','Metallic','Specular IOR Level','Subsurface Weight','Coat Weight','Sheen Weight']}})
values=np.empty(len(body.data.vertices),np.float32);body.data.attributes['ScalpHair'].data.foreach_get('value',values);co=np.empty(len(values)*3,np.float32);body.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);mask=co[:,2]>1.81
report={'body_materials':rows,'scalp_mask_on_high_head_quantiles':np.quantile(values[mask],[0,.1,.5,.9,1]).tolist(),'control':'Emit actual base colour for all asset materials; source blend unchanged'}
(folder/'hair_reflectance_diagnosis.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
mats={m for ob in bpy.data.collections['ASSET_m303'].all_objects if not ob.hide_render for m in getattr(ob.data,'materials',[]) if m}
for mat in mats:
 nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if not bs:continue
 em=nt.nodes.new('ShaderNodeEmission')
 if bs.inputs['Base Color'].is_linked:nt.links.new(bs.inputs['Base Color'].links[0].from_socket,em.inputs[0])
 else:em.inputs[0].default_value=bs.inputs['Base Color'].default_value
 nt.links.new(em.outputs[0],next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL').inputs['Surface'])
scene=bpy.context.scene;scene.camera.location=(0,-2,1.70);look_at(scene.camera,(0,0,1.70));scene.camera.data.ortho_scale=.38;scene.render.resolution_x=scene.render.resolution_y=700;scene.cycles.device='CPU';scene.cycles.samples=8;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.filepath=str(folder/'hair_albedo_control.png');bpy.ops.render.render(write_still=True)
