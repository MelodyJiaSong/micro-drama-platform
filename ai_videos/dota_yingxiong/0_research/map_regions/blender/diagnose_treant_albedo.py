"""Compare exported albedo with illuminated appearance; preserve the source asset."""
from pathlib import Path
import bpy,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];WORLD=next(ROOT.glob('2_*'))
folder=next((WORLD/'characters').glob('*/m1_Treant'))/'model_3d/r01'
out=folder/'diagnostics';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(folder/'inspection/m1_r01.blend'))
scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=32
scene.render.resolution_x=800;scene.render.resolution_y=800
materials={};images={}
for obj in bpy.data.collections['ASSET_m1'].all_objects:
 for slot in obj.material_slots:
  mat=slot.material
  if not mat or not mat.use_nodes or mat.name in materials:continue
  nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if not bs:continue
  materials[mat.name]={'values':{k:('linked' if bs.inputs[k].is_linked else bs.inputs[k].default_value) for k in ['Metallic','Roughness','IOR','Emission Strength']},'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in nt.links]}
  for n in nt.nodes:
   if n.type!='TEX_IMAGE' or not n.image:continue
   im=n.image
   if im.name in images:continue
   a=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(a);a=a.reshape(-1,4)
   images[im.name]={'size':list(im.size),'colorspace':im.colorspace_settings.name,'rgb_quantiles':np.quantile(a[:,:3],[.1,.5,.9],axis=0).tolist()}
scene.view_settings.exposure=-2
scene.render.filepath=str(out/'studio_minus_two_stops.png');bpy.ops.render.render(write_still=True)
scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard'
for name in materials:
 nt=bpy.data.materials[name].node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
 em=nt.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1
 if bs.inputs['Base Color'].is_linked:nt.links.new(bs.inputs['Base Color'].links[0].from_socket,em.inputs['Color'])
 else:em.inputs['Color'].default_value=bs.inputs['Base Color'].default_value
 nt.links.new(em.outputs[0],output.inputs['Surface'])
scene.render.filepath=str(out/'exported_base_color_unlit.png');bpy.ops.render.render(write_still=True)
(out/'albedo_probe.json').write_text(json.dumps({'source':'r01/inspection/m1_r01.blend','materials':materials,'images':images,'status':'diagnostic_only_no_acceptance'},indent=2),encoding='utf-8')
