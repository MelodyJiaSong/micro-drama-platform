"""Round blocked bank contours and replace abstract cliff blocks with scanned rock."""
from pathlib import Path
import bpy,json,base64,math,random,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v021.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v020.blend'))
terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2];before=z.copy();x,y=co[:,:,0],co[:,:,1]
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512);ix=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ix[:,None],ix[None,:]];protected=(codes&(1|16))!=0
blur=before.copy()
for _ in range(64):
 p=np.pad(blur,1,mode='edge');blur=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
gy,gx=np.gradient(before,.8);slope=np.hypot(gx,gy)
bank=np.clip((before+10)/2,0,1)*np.clip((-1-before)/2,0,1)*np.clip(slope/.3,0,1)*(~protected)
z[:]+=np.clip(blur-before,-1.2,1.2)*bank
rough=(.22*np.sin(x*.23+np.sin(y*.17)*1.8)*np.cos(y*.19-x*.08)+.10*np.sin(y*.51+x*.37))
z[:]+=rough*(~protected)*np.clip((before+6.5)/2,0,1)*np.clip(1-slope,0,1)
terrain.vertices.foreach_set('co',co.ravel());terrain.update();assert np.max(np.abs(z-before)[protected])==0
def height(px,py,arr=z):
 u,v=np.clip((px+409.6)/.8,0,1023.999),np.clip((py+409.6)/.8,0,1023.999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);a,b=u-i,v-j
 return (arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b
grounded=0
for cname in ['02_Forest','03_Asset_Placement','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','16_Forest_understorey','17_River_bank_detail']:
 coll=bpy.data.collections.get(cname)
 if not coll:continue
 for ob in coll.objects:
  px,py=ob.location[:2];ob.location.z+=float(height(px,py)-height(px,py,before));grounded+=1
point_objects=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or not ob.modifiers or not any(m.type=='NODES' for m in ob.modifiers):continue
 if len(ob.data.polygons) or len(ob.data.vertices)<1000:continue
 points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3)
 # Existing scatter point clouds are in map coordinates, with identity transforms.
 if ob.matrix_world!=bpy.data.objects['Terrain_683d'].matrix_world:continue
 points[:,2]+=height(points[:,0],points[:,1])-height(points[:,0],points[:,1],before);ob.data.vertices.foreach_set('co',points.ravel());ob.data.update();point_objects.append(ob.name)
rng=random.Random(29121);proto=bpy.data.collections['RIVER_SCAN_boulder_01'];replaced=0
for ob in bpy.data.collections['07_Cliff_Relief'].objects:
 if ob.instance_collection==proto:continue
 ob.instance_collection=proto;s=rng.uniform(.8,1.6);ob.scale=(s*rng.uniform(.85,1.3),s*rng.uniform(.65,1.1),s*rng.uniform(.9,1.45));ob.rotation_euler=(rng.uniform(-.6,.6),rng.uniform(-.5,.5),rng.uniform(0,math.tau));ob.location.z=float(height(*ob.location[:2]))-rng.uniform(.45,.8);replaced+=1
# Reduce the pale road halo using the existing canonical paving mask.
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.65;noise.inputs['Detail'].default_value=4;l.new(geo.outputs['Position'],noise.inputs['Vector']);road_changes=0
for node in list(n):
 if node.type=='ATTRIBUTE' and node.attribute_name=='Paving':
  targets=[link.to_socket for link in node.outputs['Fac'].links]
  wav=n.new('ShaderNodeMapRange');wav.inputs['To Min'].default_value=-.10;wav.inputs['To Max'].default_value=.10;l.new(noise.outputs['Fac'],wav.inputs['Value']);add=n.new('ShaderNodeMath');add.operation='ADD';l.new(node.outputs['Fac'],add.inputs[0]);l.new(wav.outputs[0],add.inputs[1]);edge=n.new('ShaderNodeMapRange');edge.clamp=True;edge.interpolation_type='SMOOTHSTEP';edge.inputs['From Min'].default_value=.23;edge.inputs['From Max'].default_value=.68;l.new(add.outputs[0],edge.inputs['Value'])
  for target in targets:l.new(edge.outputs[0],target)
 if node.type=='MIX_RGB' and node.blend_type=='MULTIPLY' and node.inputs[1].is_linked:
  tex=node.inputs[1].links[0].from_node
  if tex.type=='TEX_IMAGE' and tex.image and 'white_sandstone' in tex.image.name:node.inputs[2].default_value=(.15,.145,.125,1);road_changes+=1
assert road_changes==1,road_changes
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V021 CANDIDATE; blocked bank contour repair and scanned cliffs require review'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'file':dest.name,'source':'environment_v020.blend','status':'candidate_pending_visual_review','protected_walk_ramp_height_change_m':float(np.max(np.abs(z-before)[protected])),'blocked_surface_max_change_m':float(np.max(np.abs(z-before))),'bank_vertices_modified':int(np.count_nonzero(bank)),'replaced_abstract_cliff_instances':replaced,'regrounded_objects':grounded,'regrounded_point_clouds':point_objects,'canonical_xy_unchanged':True,'remaining':['Macro river silhouette','Cliff appearance and gaps','Road borders','Independent review']}
(OUT/'environment_v021_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['Mid_River','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_v021_{name}.png');bpy.ops.render.render(write_still=True)
