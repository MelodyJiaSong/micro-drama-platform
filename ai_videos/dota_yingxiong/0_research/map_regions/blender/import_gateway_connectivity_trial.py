"""Apply repaired connectivity while retaining source UVs, materials and hair masks."""
from pathlib import Path
import bpy,json,numpy as np,sys,argparse
from mathutils import kdtree,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r08',choices=['r08','r09']);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=Path(__file__).resolve().parents[3];folder=next(next(ROOT.glob('2_*')).glob('characters/*/m303_*/model_3d'));out=folder/args.revision
if (out/'authoring.blend').exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(folder/'r07/authoring.blend'))
body=bpy.data.objects['Gateway_merchant_body'];source=body.copy();source.data=body.data.copy();source.name='Archive_gateway_r07_before_connectivity';bpy.data.collections['ASSET_m303'].objects.link(source)
data=np.load(out/'repaired_geometry.npz');mesh=bpy.data.meshes.new('Gateway_repaired_connectivity');mesh.from_pydata(data['vertices'].tolist(),[],data['faces'].tolist());mesh.update()
for mat in body.data.materials:mesh.materials.append(mat)
body.data=mesh
for poly in mesh.polygons:poly.use_smooth=True
for layer in source.data.uv_layers:mesh.uv_layers.new(name=layer.name)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
transfer=body.modifiers.new('Preserve_source_UV_charts','DATA_TRANSFER');transfer.object=source;transfer.use_loop_data=True;transfer.data_types_loops={'UV'};transfer.loop_mapping='POLYINTERP_NEAREST';transfer.layers_uv_select_src='ALL';transfer.layers_uv_select_dst='NAME';bpy.ops.object.modifier_apply(modifier=transfer.name)
print('UV_TRANSFERRED',flush=True)
tree=kdtree.KDTree(len(source.data.vertices))
for v in source.data.vertices:tree.insert(v.co,v.index)
tree.balance();indices=np.empty(len(mesh.vertices),np.int32);distances=np.empty(len(mesh.vertices),np.float32)
for v in mesh.vertices:
    _,indices[v.index],distances[v.index]=tree.find(v.co)
attributes=[]
for attribute in source.data.attributes:
    if attribute.domain!='POINT' or attribute.data_type!='FLOAT' or attribute.name.startswith('.'):continue
    values=np.empty(len(source.data.vertices),np.float32);attribute.data.foreach_get('value',values);new=mesh.attributes.new(attribute.name,'FLOAT','POINT');new.data.foreach_set('value',values[indices]);attributes.append(attribute.name)
source.hide_render=True;source.hide_viewport=True
probes=[]
for name,x,z in [('forehead',.0038,1.757),('chin',-.00228,1.6392),('nose_cheek',-.0399,1.6905),('left_collar',-.0988,1.5442),('right_collar',.0836,1.5366)]:
    hit,p,n,index=body.ray_cast(Vector((x,-2,z)),Vector((0,1,0)));probes.append({'name':name,'hit':hit,'position':list(p),'normal':list(n)})
scene=bpy.context.scene;scene['production_status']='CONNECTIVITY_REPAIR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'authoring.blend'))
report=json.loads((out/'connectivity_repair.json').read_text());report.update(asset_id='m303',revision=args.revision,status='author_trial_pending_view',uv_transfer='Nearest source polygon interpolation in Blender; existing source retained hidden',transferred_float_point_attributes=attributes,nearest_source_vertex_distance_quantiles_m=np.quantile(distances,[.5,.9,.99,1]).tolist(),measured_hole_ray_checks=probes)
(out/'authoring.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('SAVED',json.dumps(probes),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.render.threads_mode='FIXED';scene.render.threads=6
for name,loc,target,scale in [('face_detail',(0,-2,1.7),(0,0,1.7),.38),('face_side',(1.3,-2,1.7),(0,0,1.7),.38),('author_preview',(4,-6,2),(0,0,.925),2.37)]:
    scene.camera.location=loc;look_at(scene.camera,target);scene.camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
