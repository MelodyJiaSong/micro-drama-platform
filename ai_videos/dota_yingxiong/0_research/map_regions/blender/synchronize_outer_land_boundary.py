"""Match the outer landscape to current metric terrain and all ground attributes."""
from pathlib import Path
import bpy,bmesh,json,numpy as np,sys,argparse
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';parser=argparse.ArgumentParser();parser.add_argument('--source',choices=['v033','v034'],default='v034');parser.add_argument('--revision',choices=['v035','v036'],default='v035');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);dest=OUT/f'environment_{args.revision}.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/f'environment_{args.source}.blend'));terrain=bpy.data.objects['Terrain_683d'].data;co=np.empty(len(terrain.vertices)*3,np.float32);terrain.vertices.foreach_get('co',co);co=co.reshape(1025,1025,3);z=co[:,:,2];old=bpy.data.objects['Continuous_outer_land'];oldco=np.empty(len(old.data.vertices)*3,np.float32);old.data.vertices.foreach_get('co',oldco);oldco=oldco.reshape(-1,3)
def sample(arr,x,y):
 u,v=np.clip((x+409.6)/.8,0,1024),np.clip((y+409.6)/.8,0,1024);i,j=np.minimum(u.astype(int),1023),np.minimum(v.astype(int),1023);a,b=u-i,v-j;return (arr[j,i]*(1-a)+arr[j,i+1]*a)*(1-b)+(arr[j+1,i]*(1-a)+arr[j+1,i+1]*a)*b
edgeold=oldco[np.max(np.abs(oldco[:,:2]),axis=1)<409.601];old_seam=np.abs(edgeold[:,2]-sample(z,edgeold[:,0],edgeold[:,1]));old_tree=BVHTree.FromPolygons(oldco.tolist(),[list(p.vertices) for p in old.data.polygons],all_triangles=False)
steps=1024;rings=61;u=-1+np.arange(steps)*2/steps;unit=np.concatenate([np.column_stack((u,np.full(steps,-1))),np.column_stack((np.ones(steps),u)),np.column_stack((-u,np.ones(steps))),np.column_stack((-np.ones(steps),-u))]);radius=409.6+np.arange(rings)*10;xy=(radius[:,None,None]*unit[None,:,:]).reshape(-1,2);x,y=xy.T;distance=np.repeat(radius-409.6,4*steps);blend=np.clip(distance/120,0,1);blend=blend*blend*(3-2*blend);edgeheight=sample(z,x,y);previous=np.empty(len(x),np.float32)
for i,(px,py) in enumerate(xy):
 hit,normal,face,d=old_tree.ray_cast(Vector((float(px),float(py),150)),Vector((0,0,-1)))
 previous[i]=hit.z if hit is not None else float(10+18*np.sin(px*.006)*np.cos(py*.009)+9*np.sin((px+py)*.013))
stride=4*steps
def perimeter_smooth(values):
 grid=values.reshape(rings,stride);frequency=np.fft.rfftfreq(stride);sigma=np.minimum((radius-409.6)*.8,35)/(2*radius/steps);kernel=np.exp(-2*np.pi**2*sigma[:,None]**2*frequency[None,:]**2);result=np.fft.irfft(np.fft.rfft(grid,axis=1)*kernel,n=stride,axis=1);result[0]=grid[0];return result.ravel()
height=edgeheight*(1-blend)+previous*blend
if args.revision=='v036':height=perimeter_smooth(height)
vertices=np.column_stack((x,y,height));a=np.arange((rings-1)*stride).reshape(rings-1,stride);nexta=(np.arange(stride)+1)%stride+np.arange(rings-1)[:,None]*stride;faces=np.stack((a,a+stride,nexta+stride,nexta),axis=-1).reshape(-1,4);mesh=bpy.data.meshes.new('Metric_continuous_outer_land');mesh.from_pydata(vertices.tolist(),[],faces.tolist());mesh.materials.append(bpy.data.materials['Continuous_ground']);old.data=mesh
for p in mesh.polygons:p.use_smooth=True
biome=np.clip((x+y+80)/160,0,1);attribute_reports={}
for attr in terrain.attributes:
 if attr.domain!='POINT' or attr.data_type!='FLOAT' or attr.name.startswith('.'):continue
 values=np.empty(len(terrain.vertices),np.float32);attr.data.foreach_get('value',values);edgevalues=sample(values.reshape(1025,1025),x,y)
 if attr.name=='Grass':far=np.ones(len(x))
 elif attr.name=='Blight':far=biome
 elif attr.name=='ForestFloor':far=np.full(len(x),.08)
 elif attr.name=='Height_above_local_water':far=height+10.88
 else:far=np.zeros(len(x))
 material_blend=np.clip(distance/50,0,1) if args.revision=='v036' else blend;material_blend=material_blend*material_blend*(3-2*material_blend) if args.revision=='v036' else material_blend;values=edgevalues*(1-material_blend)+far*material_blend
 if args.revision=='v036':values=perimeter_smooth(values)
 new=mesh.attributes.new(attr.name,'FLOAT','POINT');new.data.foreach_set('value',values.astype(np.float32));attribute_reports[attr.name]={'boundary_max_delta':float(np.max(np.abs(values[:stride]-edgevalues[:stride])))}
bm=bmesh.new();bm.from_mesh(mesh);tree=BVHTree.FromBMesh(bm);bm.free();moved=0
for ob in bpy.data.collections['14_Distant_Landscape'].objects:
 if ob.instance_type!='COLLECTION':continue
 px,py=ob.location[:2];hit,normal,face,d=tree.ray_cast(Vector((px,py,150)),Vector((0,0,-1)))
 if hit is not None:ob.location.z=hit.z;moved+=1
seam=np.abs(height[:stride]-sample(z,x[:stride],y[:stride]));assert seam.max()<1e-5
report={'file':dest.name,'source':f'environment_{args.source}.blend','status':'author_trial_pending_view','diagnosis':'Metric terrain edits updated Terrain_683d but left Continuous_outer_land at old heights and without new local-water/source-soil attributes','old_boundary_vertex_max_gap_m':float(old_seam.max()),'old_boundary_vertex_median_gap_m':float(np.median(old_seam)),'new_boundary_sample_max_gap_m':float(seam.max()),'boundary_samples':stride,'outer_vertices':len(vertices),'outer_faces':len(faces),'transition_width_m':120,'attributes':attribute_reports,'outer_trees_regrounded':moved,'playable_terrain_unchanged':True,'remaining':['Visual edge continuity','Boundary cliffs inside playable region remain separate issue','Independent review']}
report['extension_smoothing']='Distance-growing cyclic Gaussian along perimeter; 0m at seam, max35m; material transition50m' if args.revision=='v036' else 'none';scene=bpy.context.scene;scene['production_status']='OUTER_BOUNDARY_CONTINUITY_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));(OUT/f'environment_{args.revision}_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('BOUNDARY_SYNCHRONIZED',json.dumps(report),flush=True)
scene.camera=bpy.data.objects['Map_Overview'];scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.debug_use_compact_bvh=True;scene.render.use_simplify=True;scene.cycles.texture_limit_render='1024';scene.render.threads_mode='FIXED';scene.render.threads=8;scene.render.resolution_x=1200;scene.render.resolution_y=900
scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=0;scene.render.border_max_x=1;scene.render.border_min_y=.75;scene.render.border_max_y=1;scene.render.filepath=str(OUT/f'environment_{args.revision}_Northern_edge.png');bpy.ops.render.render(write_still=True)
scene.render.use_border=False;scene.render.use_crop_to_border=False;scene.render.filepath=str(OUT/f'environment_{args.revision}_Map_Overview.png');bpy.ops.render.render(write_still=True);print('OUTER_BOUNDARY_VIEWS_RENDERED',flush=True)
