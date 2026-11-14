"""Smooth the diagnosed stepped terrain border, preserving all walk/ramp heights."""
from pathlib import Path
import bpy,bmesh,json,base64,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v023.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v022.blend'));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2];before=z.copy();x,y=co[:,:,0],co[:,:,1]
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512);ix=np.minimum(np.arange(1025)//2,511);codes=cells[::-1][ix[:,None],ix[None,:]];protected=(codes&(1|16))!=0
edge=np.clip((np.maximum(np.abs(x),np.abs(y))-374)/22,0,1);edge=edge*edge*(3-2*edge);blur=z.copy()
for _ in range(256):
 p=np.pad(blur,1,mode='edge');blur=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
z[:]+=(blur-z)*edge*(~protected);me.vertices.foreach_set('co',co.ravel());me.update();assert np.max(np.abs(z-before)[protected])==0
gy,gx=np.gradient(z,.8);me.attributes['Rock'].data.foreach_set('value',np.clip((np.hypot(gx,gy)-.35)*1.4,0,1).astype(np.float32).ravel())
def height(px,py,arr=z):
 u,v=np.clip((px+409.6)/.8,0,1023.999),np.clip((py+409.6)/.8,0,1023.999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);a,b=u-i,v-j
 return (arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b
for name in ['02_Forest','03_Asset_Placement','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','16_Forest_understorey','17_River_bank_detail']:
 coll=bpy.data.collections.get(name)
 if not coll:continue
 for ob in coll.objects:
  px,py=ob.location[:2];ob.location.z+=float(height(px,py)-height(px,py,before))
grass=bpy.data.objects['Living_ground_grass'].data;points=np.empty(len(grass.vertices)*3,np.float32);grass.vertices.foreach_get('co',points);points=points.reshape(-1,3);points[:,2]+=height(points[:,0],points[:,1])-height(points[:,0],points[:,1],before);grass.vertices.foreach_set('co',points.ravel());grass.update()
# Continue the new height across the existing outside apron; avoid a seam at 409.6m.
outer=bpy.data.objects['Continuous_outer_land'].data;points=np.empty(len(outer.vertices)*3,np.float32);outer.vertices.foreach_get('co',points);points=points.reshape(-1,3);radius=np.max(np.abs(points[:,:2]),axis=1);weight=np.clip(1-(radius-409.6)/120,0,1);points[:,2]+=(height(points[:,0],points[:,1])-height(points[:,0],points[:,1],before))*weight;outer.vertices.foreach_set('co',points.ravel());outer.update();bm=bmesh.new();bm.from_mesh(outer);tree=BVHTree.FromBMesh(bm);bm.free()
for ob in bpy.data.collections['14_Distant_Landscape'].objects:
 if ob.instance_type!='COLLECTION':continue
 px,py=ob.location[:2];hit,normal,face,distance=tree.ray_cast(Vector((px,py,150)),Vector((0,0,-1)))
 if hit is not None:ob.location.z=hit.z
nt=bpy.data.materials['Continuous_ground'].node_tree;n,l=nt.nodes,nt.links;tinted=[]
for attr in list(n):
 if attr.type!='ATTRIBUTE' or attr.attribute_name!='Rock':continue
 for link in list(attr.outputs['Fac'].links):
  mix=link.to_node
  if mix.type!='MIX_RGB' or not mix.inputs[2].is_linked:continue
  source=mix.inputs[2].links[0].from_socket;tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.42,.46,.38,1);l.new(source,tint.inputs[1]);l.new(tint.outputs[0],mix.inputs[2]);tinted.append(mix.name)
assert tinted,'Ground cliff shader branch not found'
scene=bpy.context.scene;scene['production_status']='ENVIRONMENT V023 CANDIDATE; diagnosed terrain boundary smoothing pending review';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
(OUT/'environment_v023_report.json').write_text(json.dumps({'file':dest.name,'source':'environment_v022.blend','status':'candidate_pending_visual_review','diagnosis_evidence':'cliff_source_* renders and cliff_ray_probe.json: northern bright blocks mostly Terrain_683d, not authored rock instances','border_start_m':374,'smoothing_iterations':256,'protected_walk_ramp_height_change_m':float(np.max(np.abs(z-before)[protected])),'max_blocked_border_height_change_m':float(np.max(np.abs(z-before))),'border_protected_fraction':float(protected[edge>0].mean()),'canonical_xy_unchanged':True,'cliff_shader_tinted':tinted,'remaining':['Boundary continuity','Blocked border appearance','Full map independent review']},indent=2),encoding='utf-8');print('BOUNDARY_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=8;scene.camera=bpy.data.objects['Map_Overview'];scene.render.resolution_x=1200;scene.render.resolution_y=900
scene.cycles.samples=24;scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=0;scene.render.border_max_x=1;scene.render.border_min_y=.75;scene.render.border_max_y=1;scene.render.filepath=str(OUT/'environment_v023_Northern_edge.png');bpy.ops.render.render(write_still=True)
scene.render.use_border=False;scene.render.use_crop_to_border=False;scene.cycles.samples=48;scene.render.filepath=str(OUT/'environment_v023_Map_Overview.png');bpy.ops.render.render(write_still=True)
