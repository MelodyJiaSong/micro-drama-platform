"""Apply the constrained bank trial and replace isolated upright stone fins with rubble."""
from pathlib import Path
import bpy,numpy as np,json,random,math,base64,argparse,sys
from mathutils import Vector
parser=argparse.ArgumentParser();parser.add_argument('--revision',default='v027');parser.add_argument('--source',default='environment_v026.blend');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);assert args.revision in ['v027','v028','v029'];assert Path(args.source).name==args.source
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/f'environment_{args.revision}.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/args.source));me=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);before=co[:,:,2].copy();z=np.load(OUT/f'bank_sculpt_{args.revision}_heights.npy');co[:,:,2]=z;me.vertices.foreach_set('co',co.ravel());me.update()
def height(x,y,arr=z):
 u,v=np.clip((x+409.6)/.8,0,1023.999),np.clip((y+409.6)/.8,0,1023.999);i,j=np.asarray(u,dtype=int),np.asarray(v,dtype=int);a,b=u-i,v-j;return (arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b
regrounded=0
for cname in ['02_Forest','03_Asset_Placement','04_Environment_Details','06_Undergrowth','07_Cliff_Relief','08_Meadow_Growth','09_Ground_Stones','13_Fallen_Timber','16_Forest_understorey','17_River_bank_detail']:
 coll=bpy.data.collections.get(cname)
 if not coll:continue
 for ob in coll.objects:
  px,py=ob.location[:2];ob.location.z+=float(height(px,py)-height(px,py,before));regrounded+=1
clouds=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or not any(m.type=='NODES' for m in ob.modifiers) or len(ob.data.polygons) or len(ob.data.vertices)<1000:continue
 if ob.matrix_world!=bpy.data.objects['Terrain_683d'].matrix_world:continue
 points=np.empty(len(ob.data.vertices)*3,np.float32);ob.data.vertices.foreach_get('co',points);points=points.reshape(-1,3);points[:,2]+=height(points[:,0],points[:,1])-height(points[:,0],points[:,1],before);ob.data.vertices.foreach_set('co',points.ravel());ob.data.update();clouds.append(ob.name)
# Recompute the local wet-bank masks against the modified bed.
distance=np.where(z<-6.8,0,100).astype(np.float32)
for _ in range(12):
 p=np.pad(distance,1,mode='edge');distance=np.minimum.reduce([distance,p[:-2,1:-1]+.8,p[2:,1:-1]+.8,p[1:-1,:-2]+.8,p[1:-1,2:]+.8,p[:-2,:-2]+1.13137,p[:-2,2:]+1.13137,p[2:,:-2]+1.13137,p[2:,2:]+1.13137])
mask=np.clip((5-distance)/3.5,0,1);mask=mask*mask*(3-2*mask);me.attributes['Actual_shore_distance_mask'].data.foreach_set('value',mask.ravel())
gy,gx=np.gradient(z,.8)
if me.attributes.get('Rock'):me.attributes['Rock'].data.foreach_set('value',np.clip((np.hypot(gx,gy)-.3)*1.3,0,1).astype(np.float32).ravel())
# The ray probe confirmed three conspicuous fins are grounded, single-piece
# scanned cliff faces scaled down. Use rounded rubble for this decorative layer.
proto=bpy.data.collections['RIVER_SCAN_boulder_01'];corners=[]
for src in proto.all_objects:
 if src.type=='MESH':corners.extend(tuple(src.matrix_world@Vector(c)-proto.instance_offset) for c in src.bound_box)
bounds=np.array(corners);span=float(np.max(np.ptp(bounds,axis=0)));rng=random.Random(27027);changed=hidden=0
grid=json.loads((ROOT/'0_research/map_regions/navigation/grid.json').read_text());cells=np.frombuffer(base64.b64decode(grid['cells_base64']),np.uint8).reshape(512,512)
for ob in bpy.data.collections['09_Ground_Stones'].objects:
 if args.revision!='v027':break
 if ob.instance_type!='COLLECTION':continue
 x,y=ob.location[:2];code=int(cells[int(np.clip((409.6-y)/1.6,0,511)),int(np.clip((x+409.6)/1.6,0,511))]);cluster=(math.sin(x*.067+math.sin(y*.031)*2)+math.sin(y*.073-x*.029))*.25+.5
 if rng.random()>.12+.55*cluster:ob.hide_render=True;hidden+=1;continue
 size=rng.uniform(.035,.085) if code&(1|16) else rng.uniform(.13,.43);s=size/span;ob.instance_collection=proto;ob.scale=(s*rng.uniform(.8,1.2),s*rng.uniform(.8,1.2),s*.60);ob.rotation_euler=(rng.uniform(-.5,.5),rng.uniform(-.5,.5),rng.uniform(0,math.tau));ob.location.z=float(height(x,y))-size*.16;changed+=1
scene=bpy.context.scene;scene['production_status']=f'ENVIRONMENT {args.revision} AUTHOR TRIAL; bank silhouette and contacts unaccepted';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report=json.loads((OUT/f'bank_sculpt_{args.revision}_prepare.json').read_text());report.update(file=dest.name,regrounded_objects=regrounded,regrounded_clouds=clouds,replaced_decorative_stone_instances=changed,hidden_grid_stones=hidden,mean_water_level_m=-6.800000190734863)
(OUT/f'environment_{args.revision}_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('BANK_SCULPT_SAVED',flush=True)
scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
for name in ['River_Eye_Level','Map_Overview']:
 scene.camera=bpy.data.objects[name];scene.render.filepath=str(OUT/f'environment_{args.revision}_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
