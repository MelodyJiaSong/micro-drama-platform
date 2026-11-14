"""Task-local dielectric material trial, retaining geometry and base-colour evidence."""
from pathlib import Path
import bpy,json,sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
p=argparse.ArgumentParser();p.add_argument('asset',choices=['m26','m303']);p.add_argument('--source',required=True);p.add_argument('--revision',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob(f'characters/*/{args.asset}_*/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
source=folder/args.source/'authoring.blend'
if not source.exists():source=folder/args.source/'inspection'/f'{args.asset}_{args.source}.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));coll=bpy.data.collections['ASSET_'+args.asset];body=max((o for o in coll.all_objects if o.type=='MESH' and not o.hide_render),key=lambda o:len(o.data.polygons));changes=[]
for mat in body.data.materials:
 nt=mat.node_tree;bs=next(q for q in nt.nodes if q.type=='BSDF_PRINCIPLED');changes.append({'material':mat.name,'prior_metallic_link':bs.inputs['Metallic'].links[0].from_node.name if bs.inputs['Metallic'].is_linked else None,'prior_specular':bs.inputs['Specular IOR Level'].default_value})
 for link in list(bs.inputs['Metallic'].links):nt.links.remove(link)
 bs.inputs['Metallic'].default_value=0;bs.inputs['Specular IOR Level'].default_value=.28;bs.inputs['IOR'].default_value=1.45
 if bs.inputs['Roughness'].is_linked:
  source_roughness=bs.inputs['Roughness'].links[0].from_socket;remap=nt.nodes.new('ShaderNodeMapRange');remap.clamp=True;remap.inputs['To Min'].default_value=.48;remap.inputs['To Max'].default_value=.88;nt.links.new(source_roughness,remap.inputs['Value']);nt.links.new(remap.outputs[0],bs.inputs['Roughness'])
scene=bpy.context.scene;scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=1000;scene['production_status']='ORGANIC_PBR_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
prior=folder/args.source/'authoring.json';report=json.loads(prior.read_text()) if prior.exists() else {'asset_id':args.asset};report.update(revision=args.revision,source=args.source,status='author_trial_pending_view',dielectric_correction={'evidence':'pbr_channel_diagnosis.json','changes':changes,'metallic':0,'specular_ior_level':.28,'ior':1.45,'roughness_remap':[.48,.88],'scope':'Organic body; m303 belt buckle still requires a separately masked metal assignment. No geometry or base-colour change.'},remaining=['Geometry and texture blockers remain','Evaluate against unchanged-lighting source','Independent review']);(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('DIELECTRIC_TRIAL_SAVED',flush=True)
views=[('head_detail',(5,-3,2.4),(1.65,0,1.05),1.9),('author_preview',(6,-8,4.3),(0,0,1.2),5.8)] if args.asset=='m26' else [('face_detail',(0,-2,1.70),(0,0,1.70),.38),('author_preview',(4,-6,2.0),(0,0,.925),2.37)]
for name,loc,target,scale in views:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
