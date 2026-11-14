"""Use measured bark luminance and feathered soil to finish r39 root contacts."""
from pathlib import Path
import bpy,json,sys,numpy as np,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['r40','r41'],default='r40');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('background/*/bg23_*/model_3d'));out=folder/args.revision;out.mkdir(exist_ok=True)
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r39/authoring.blend'));coll=bpy.data.collections['ASSET_bg23'];mat=bpy.data.materials['Tileable_root_bark_actual_scale'];nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and n.image and '_diff_' in n.image.name);pixels=np.empty(len(tex.image.pixels),np.float32);tex.image.pixels.foreach_get(pixels);rgb=pixels.reshape(-1,4)[::8,:3]
decoded=args.revision=='r41' and not tex.image.is_float and tex.image.colorspace_settings.name=='sRGB'
if decoded:rgb=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
luminance=rgb@np.array([.2126,.7152,.0722]);lo,hi=np.quantile(luminance,[.05,.95]);assert hi>lo;gray=nt.nodes.new('ShaderNodeRGBToBW');nt.links.new(tex.outputs['Color'],gray.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=float(lo);ramp.color_ramp.elements[0].color=(.12,.105,.075,1);ramp.color_ramp.elements[1].position=float(hi);ramp.color_ramp.elements[1].color=(.38,.33,.24,1);nt.links.new(gray.outputs[0],ramp.inputs[0]);nt.links.new(ramp.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.84;bs.inputs['Specular IOR Level'].default_value=.16
for n in nt.nodes:
 if n.type=='BUMP':n.inputs['Distance'].default_value=.002;n.inputs['Strength'].default_value=.65
 if n.type=='NORMAL_MAP':n.inputs['Strength'].default_value=.30
feeders=sorted((o for o in coll.objects if o.type=='CURVE' and not o.hide_render and o.name.startswith('Fine_feeder_root')),key=lambda o:o.name);kept=0
for i,ob in enumerate(feeders):
 if i%3:ob.hide_render=True;ob.hide_viewport=True;continue
 kept+=1
 for spline in ob.data.splines:
  points=spline.bezier_points if spline.type=='BEZIER' else spline.points
  for j,p in enumerate(points):
   t=j/max(1,len(points)-1);delta=.06*max(0,(t-.35)/.65)**2;p.co.z-=delta
   if spline.type=='BEZIER':p.handle_left.z-=delta;p.handle_right.z-=delta
soil=bpy.data.materials['Localized_root_soil'];nt=soil.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='Root_soil_edge_fade';nt.links.new(attr.outputs['Fac'],bs.inputs['Alpha']);soil.surface_render_method='DITHERED';mounds=0
for ob in coll.objects:
 if ob.hide_render or not ob.name.startswith('Small_irregular_root_soil_hummock'):continue
 me=ob.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);center=co[:,:2].mean(0);radius=np.linalg.norm(co[:,:2]-center,axis=1);scale=np.quantile(radius,.95);t=np.clip((radius/scale-.25)/.60,0,1);fade=1-t*t*(3-2*t);a=me.attributes.new('Root_soil_edge_fade','FLOAT','POINT');a.data.foreach_set('value',fade.astype(np.float32));mounds+=1
ferns=sorted((o for o in coll.objects if not o.hide_render and o.name.startswith('Irregular_fern_root_margin')),key=lambda o:o.name)
for i,ob in enumerate(ferns):
 if i%3==0:ob.scale*=1.25
report=json.loads((folder/'r39/authoring.json').read_text());report.update(revision=args.revision,source='r39',status='author_trial_pending_view',root_surface={'actual_diffuse_luminance_5_95':list(map(float,[lo,hi])),'srgb_byte_samples_decoded_to_linear':decoded,'linear_bark_colour_range':[[.12,.105,.075],[.38,.33,.24]],'bump_depth_m':.002,'fine_feeders_retained':kept,'fine_feeders_hidden':len(feeders)-kept,'feeder_tips_lowered_m':.06,'soil_patches_with_continuous_opacity_fade':mounds},remaining=['Pale living root appearance','Ground transition and fern overlap','Independent multi-angle review']);scene=bpy.context.scene;scene['production_status']='ROOT_SURFACE_AND_GROUND_BLEND_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'));(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('ROOT_GROUND_BLEND_SAVED',json.dumps(report['root_surface']),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('root_detail',(6,-7,3),(1.25,-.9,.35),3.8),('perspective_preview',(9,-14,7.5),(0,0,2.5),6.9)]:
 scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
