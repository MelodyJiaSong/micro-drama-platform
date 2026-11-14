"""Limit wet mud to actual shoreline distance instead of every low-elevation terrace."""
from pathlib import Path
import bpy,numpy as np,json
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v022.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v021.blend'));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2];level=float(bpy.data.objects['River_surface'].data.vertices[0].co.z)
# Bounded chamfer distance: only the first 8 metres can affect this shader.
distance=np.where(z<level,0,100).astype(np.float32)
for _ in range(12):
 p=np.pad(distance,1,mode='edge');distance=np.minimum.reduce([distance,p[:-2,1:-1]+.8,p[2:,1:-1]+.8,p[1:-1,:-2]+.8,p[1:-1,2:]+.8,p[:-2,:-2]+1.13137,p[:-2,2:]+1.13137,p[2:,:-2]+1.13137,p[2:,2:]+1.13137])
mask=np.clip((5-distance)/3.5,0,1);mask=mask*mask*(3-2*mask)
a=me.attributes.new('Actual_shore_distance_mask','FLOAT','POINT');a.data.foreach_set('value',mask.astype(np.float32).ravel())
wet=me.attributes.get('RiverWetness')
if wet:
 values=np.empty(len(me.vertices),np.float32);wet.data.foreach_get('value',values);values*=np.clip((2.5-distance.ravel())/2,0,1);wet.data.foreach_set('value',values)
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;attr=n.new('ShaderNodeAttribute');attr.attribute_name='Actual_shore_distance_mask';changed=[]
for ramp in list(n):
 if ramp.type!='MAP_RANGE' or abs(ramp.inputs['From Min'].default_value-(level+1.1))>.01 or abs(ramp.inputs['From Max'].default_value-(level+4.2))>.01:continue
 for target in list(ramp.outputs[0].links):
  masknode=target.to_node
  if masknode.type!='MATH' or masknode.operation!='SUBTRACT':continue
  outputs=[link.to_socket for link in masknode.outputs[0].links];multiply=n.new('ShaderNodeMath');multiply.operation='MULTIPLY';l.new(masknode.outputs[0],multiply.inputs[0]);l.new(attr.outputs['Fac'],multiply.inputs[1])
  for socket in outputs:l.new(multiply.outputs[0],socket)
  changed.append({'height_mask_node':masknode.name,'downstream_inputs':len(outputs)})
assert len(changed)==1,changed
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V022 CANDIDATE; biome restoration outside narrow river bank requires review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v022_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v021.blend','status':'candidate_pending_visual_review','diagnosis':'Old bank shader keyed only on elevation, covering low terraces far from water and obscuring grass/blight materials','bank_mud_max_distance_from_water_m':5,'wet_soil_max_distance_from_water_m':2.5,'shader_branches':changed,'geometry_and_navigation_changed':False},indent=2),encoding='utf-8');print('SAVED',dest,flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v022_{name}.png');bpy.ops.render.render(write_still=True)
