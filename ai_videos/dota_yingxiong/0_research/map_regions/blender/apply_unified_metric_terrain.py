"""Apply metric height trial and reground scenery without changing XY layout."""
from pathlib import Path
import bpy,json,numpy as np,sys,argparse
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='v032',choices=['v032','v033']);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
revision=args.revision;source='v031' if revision=='v032' else 'v032'
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/f'environment_{revision}.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/f'environment_{source}.blend'));terrain=bpy.data.objects['Terrain_683d'];me=terrain.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);before=co[:,:,2].copy();data=np.load(OUT/f'metric_terrain_{revision}.npz');z=data['heights'];waterheight=data['water_mean_heights'];co[:,:,2]=z;me.vertices.foreach_set('co',co.ravel());me.update()
def height(x,y,array):
 u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);a,b=u-i,v-j;return (array[j,i]*(1-a)+array[j,i+1]*a)*(1-b)+(array[j+1,i]*(1-a)+array[j+1,i+1]*a)*b
delta=z-before;regrounded=0
for name in ['02_Forest','03_Asset_Placement','04_Environment_Details','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','16_Forest_understorey','17_River_bank_detail']:
 coll=bpy.data.collections.get(name)
 if coll:
  for ob in coll.objects:ob.location.z+=float(height(ob.location.x,ob.location.y,delta));regrounded+=1
clouds=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or not any(m.type=='NODES' for m in ob.modifiers) or len(ob.data.polygons) or len(ob.data.vertices)<1000 or ob.matrix_world!=terrain.matrix_world:continue
 points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3);points[:,2]+=height(points[:,0],points[:,1],delta);ob.data.vertices.foreach_set('co',points.ravel());ob.data.update();clouds.append(ob.name)
j,i=np.nonzero(data['water_cells']);a=j*1025+i;faces=np.column_stack((a,a+1,a+1026,a+1025));unique,inverse=np.unique(faces,return_inverse=True);jj,ii=np.divmod(unique,1025);x=-409.6+ii*.8;y=-409.6+jj*.8;waves=.018*np.sin((x*.62+y*.78)*2.5)+.009*np.sin((x*.85-y*.53)*5.1)+.004*np.sin(x*9.2+y*7.1);verts=np.column_stack((x,y,waterheight[jj,ii]+waves));water=bpy.data.objects['River_surface'];mesh=bpy.data.meshes.new('W3E_bounded_metric_water_levels');mesh.from_pydata(verts.tolist(),[],inverse.reshape(-1,4).tolist());mesh.materials.append(bpy.data.materials['River_water']);water.data=mesh;water.matrix_world.identity()
for p in mesh.polygons:p.use_smooth=True
distance=np.where(z<waterheight,0,100).astype(np.float32)
for _ in range(12):
 p=np.pad(distance,1,mode='edge');distance=np.minimum.reduce([distance,p[:-2,1:-1]+.8,p[2:,1:-1]+.8,p[1:-1,:-2]+.8,p[1:-1,2:]+.8,p[:-2,:-2]+1.13137,p[:-2,2:]+1.13137,p[2:,:-2]+1.13137,p[2:,2:]+1.13137])
mask=np.clip((5-distance)/3.5,0,1);mask=mask*mask*(3-2*mask);me.attributes['Actual_shore_distance_mask'].data.foreach_set('value',mask.ravel());gy,gx=np.gradient(z,.8);me.attributes['Rock'].data.foreach_set('value',np.clip((np.hypot(gx,gy)-.3)*1.3,0,1).astype(np.float32).ravel())
camera=bpy.data.objects['River_Eye_Level'];direction=camera.matrix_world.to_quaternion()@Vector((0,0,-1));target=None
if direction.z<-.01:
 old_water=-6.8 if revision=='v032' else -10.88
 t=(old_water-camera.location.z)/direction.z;target=camera.location+direction*t
 if abs(target.x)<409.6 and abs(target.y)<409.6:target.z=float(height(target.x,target.y,waterheight))
 else:target=None
camera.location.z+=float(height(camera.location.x,camera.location.y,delta))
if target is not None:look_at(camera,target)
shader_changes=[]
if revision=='v033':
 attr=me.attributes.get('Height_above_local_water') or me.attributes.new('Height_above_local_water','FLOAT','POINT');attr.data.foreach_set('value',(z-waterheight).astype(np.float32).ravel())
 nt=bpy.data.materials['Continuous_ground'].node_tree;node=nt.nodes.new('ShaderNodeAttribute');node.attribute_name='Height_above_local_water'
 for name in ['Map Range.001','Map Range.003','Map Range.008']:
  ramp=nt.nodes[name];original=[ramp.inputs['From Min'].default_value,ramp.inputs['From Max'].default_value];assert all(-8<v<-2 for v in original),(name,original)
  for socket in ['From Min','From Max']:ramp.inputs[socket].default_value+=6.8
  nt.links.new(node.outputs['Fac'],ramp.inputs['Value']);shader_changes.append({'node':name,'old_absolute_range_m':original,'new_local_relative_range_m':[ramp.inputs['From Min'].default_value,ramp.inputs['From Max'].default_value]})
scene=bpy.context.scene;scene['vertical_game_units_per_m']=20.;scene['production_status']=f'METRIC_TERRAIN_{revision}_AUTHOR_TRIAL_NOT_ACCEPTED';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report=json.loads((OUT/f'metric_terrain_{revision}_prepare.json').read_text());report.update(file=dest.name,regrounded_objects=regrounded,regrounded_clouds=clouds,water_vertices=len(verts),water_faces=len(faces),local_water_shader_changes=shader_changes,source_special_high_water_vertex={'grid_xy':[117,17],'world_xy':[6784,-6016],'water_m':-4.48,'source_ground_m':-12.8,'context':'Single flagged depressed tilepoint surrounded by dry ground at zero; neighbouring stored water levels also -4.48. Retained only in bounded local water geometry.'});(OUT/f'environment_{revision}_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('METRIC_ENVIRONMENT_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['River_Eye_Level','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_{revision}_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
