"""Restore the original 4K texture sampling after geometric repair, retaining r11 tone."""
from pathlib import Path
import bpy,json,sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r12');parser.add_argument('--uv-method',choices=['builtin','chunked'],default='builtin');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m26_*/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r11/authoring.blend'));body=bpy.data.objects['Closed_lizard_surface_3mm'];source=bpy.data.objects['Archive_r07_lizard_before_closed_surface']
for uv in source.data.uv_layers:
 if not body.data.uv_layers.get(uv.name):body.data.uv_layers.new(name=uv.name)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
if args.uv_method=='chunked':
 from transfer_uv_in_chunks import transfer_uv
 uv_report=transfer_uv(source,body,out)
else:
 transfer=body.modifiers.new('Recover_source_UV_after_surface_repair','DATA_TRANSFER');transfer.object=source;transfer.use_loop_data=True;transfer.data_types_loops={'UV'};transfer.loop_mapping='POLYINTERP_NEAREST';transfer.layers_uv_select_src='ALL';transfer.layers_uv_select_dst='NAME';bpy.ops.object.modifier_apply(modifier=transfer.name);uv_report={'method':'Blender builtin nearest polygon UV interpolation'}
mat=source.data.materials[0].copy();mat.name='Repaired_lizard_original_4K_sampling';nt=mat.node_tree;n,l=nt.nodes,nt.links;bs=next(q for q in n if q.type=='BSDF_PRINCIPLED');colour=bs.inputs['Base Color'].links[0].from_socket
sep=n.new('ShaderNodeSeparateColor');sep.mode='HSV';l.new(colour,sep.inputs[0]);mask=n.new('ShaderNodeMapRange');mask.clamp=True;mask.inputs['From Min'].default_value=.25;mask.inputs['From Max'].default_value=.55;l.new(sep.outputs[1],mask.inputs[0]);skin=n.new('ShaderNodeHueSaturation');skin.inputs['Saturation'].default_value=.80;skin.inputs['Value'].default_value=.78;l.new(colour,skin.inputs['Color']);bone=n.new('ShaderNodeHueSaturation');bone.inputs['Saturation'].default_value=.55;bone.inputs['Value'].default_value=.97;l.new(colour,bone.inputs['Color']);mix=n.new('ShaderNodeMixRGB');l.new(mask.outputs[0],mix.inputs[0]);l.new(bone.outputs[0],mix.inputs[1]);l.new(skin.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],bs.inputs['Base Color']);bs.inputs['Metallic'].default_value=0;bs.inputs['Specular IOR Level'].default_value=.15
geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180;noise.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],noise.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.0008;bump.inputs['Strength'].default_value=.35;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);body.data.materials.clear();body.data.materials.append(mat)
scene=bpy.context.scene;scene['production_status']='4K_UV_REPROJECTION_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));report=json.loads((folder/'r11/authoring.json').read_text());report.update(revision=args.revision,source='r11',status='author_trial_pending_view',texture_recovery={'source':'Archive_r07_lizard_before_closed_surface','method':uv_report,'albedo_size':[4096,4096],'roughness':'Original material texture graph restored','micro_bump_m':.0008,'geometry_changed':False},remaining=['Texture seams on repaired cavities','Pitted spike silhouettes','Skin detail and source fidelity','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('4K_UV_RESTORED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('back_detail',(1,-4,4),(.1,0,1.8),2.3),('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9),('author_preview',(6,-8,4.3),(0,0,1.2),5.8)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
