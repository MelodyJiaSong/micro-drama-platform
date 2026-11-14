"""Conservatively remove every scan triangle whose XY bounds touch protected cells."""
from pathlib import Path
import bpy,json,numpy as np,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent));from inspect_model import look_at
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d';dest=OUT/'environment_v040.blend'
if dest.exists():raise FileExistsError(dest)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v039.blend'));fields=np.load(OUT/'cliff_embedding_fields.npz');z=fields['z'];protected=(fields['codes']&17)!=0;integral=np.pad(protected.astype(np.int64).cumsum(0).cumsum(1),((1,0),(1,0)))
def sample(xy):
 u,v=np.clip(((xy+409.6)/.8).T,0,1024);i,j=np.minimum(u.astype(int),1023),np.minimum(v.astype(int),1023);a,b=u-i,v-j
 return z[j,i]*(1-a)*(1-b)+z[j,i+1]*a*(1-b)+z[j+1,i]*(1-a)*b+z[j+1,i+1]*a*b
def overlaps(tri):
 low=np.clip(np.floor((tri[:,:,:2].min(1)+409.6)/.8).astype(int)-1,0,1024);high=np.clip(np.ceil((tri[:,:,:2].max(1)+409.6)/.8).astype(int)+1,0,1024);x0,y0=low.T;x1,y1=(high+1).T
 return (integral[y1,x1]-integral[y0,x1]-integral[y1,x0]+integral[y0,x0])>0
rows=[]
for ob in list(bpy.data.collections['19_Embedded_scan_cliff_trial'].objects):
 old=ob.data;old.calc_loop_triangles();co=np.empty(len(old.vertices)*3,np.float32);old.vertices.foreach_get('co',co);co=co.reshape(-1,3);ids=np.empty(len(old.loop_triangles)*3,np.int32);old.loop_triangles.foreach_get('vertices',ids);ids=ids.reshape(-1,3);loops=np.empty(len(old.loop_triangles)*3,np.int32);old.loop_triangles.foreach_get('loops',loops);loops=loops.reshape(-1,3);unsafe=overlaps(co[ids]);safe=ids[~unsafe]
 if not len(safe):ob.hide_render=True;rows.append({'object':ob.name,'hidden_empty':True,'removed_triangles':len(ids)});continue
 used=np.unique(safe);remap=np.full(len(co),-1,np.int32);remap[used]=np.arange(len(used));faces=remap[safe];vertices=co[used].copy();edges=np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]);edges.sort(1);unique,count=np.unique(edges,axis=0,return_counts=True);boundary=np.unique(unique[count==1]);ground=sample(vertices[boundary,:2]);vertices[boundary,2]=np.minimum(vertices[boundary,2],ground-.06)
 assert not overlaps(vertices[faces]).any()
 mesh=bpy.data.meshes.new(old.name+'_Navigation_clipped');mesh.from_pydata(vertices.tolist(),[],faces.tolist());mesh.update()
 for mat in old.materials:mesh.materials.append(mat)
 for layer in old.uv_layers:
  uv=np.empty(len(old.loops)*2,np.float32);layer.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);new=mesh.uv_layers.new(name=layer.name);new.data.foreach_set('uv',uv[loops[~unsafe]].reshape(-1))
 for p in mesh.polygons:p.use_smooth=True
 ob.data=mesh;rows.append({'object':ob.name,'original_triangles':len(ids),'retained_triangles':len(faces),'removed_triangles':int(unsafe.sum()),'buried_boundary_vertices':len(boundary),'projected_protected_aabb_overlaps_after':0})
scene=bpy.context.scene;scene['production_status']='LOCAL_CLIFF_NAVIGATION_CLIPPED_AUTHOR_TRIAL';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(dest));report={'file':dest.name,'source':'environment_v039.blend','status':'local_author_trial_pending_visual_check','scope':'Same local 62 patches, no map-wide expansion','method':'Remove complete triangles when their projected bounds, expanded by one 0.8m terrain-grid step, intersect any walk/ramp cell; then lower new open boundaries by at least 6cm below terrain without XY motion. Remaining triangle projected bounds all disjoint from protected grid.','removed_triangles':sum(r['removed_triangles'] for r in rows),'remaining_triangles':sum(r.get('retained_triangles',0) for r in rows),'patches':rows,'limitations':['Conservative clipping may remove more rock than necessary','Original environment objects are outside this new-scan check','Visual seams and shoreline must still be reviewed']};(OUT/'environment_v040_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('CLIFF_NAVIGATION_CLIPPED',report['removed_triangles'],report['remaining_triangles'],flush=True)
scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=6;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.use_simplify=True;scene.cycles.texture_limit_render='2048';scene.render.use_border=False
camera=bpy.data.objects['River_Eye_Level'];scene.camera=camera;scene.render.filepath=str(OUT/'environment_v040_River_Eye_Level.png');bpy.ops.render.render(write_still=True)
close=json.loads((OUT/'environment_v038_close_cameras.json').read_text())[0];camera.location=close['camera'];look_at(camera,Vector(close['target']));camera.data.type='PERSP';camera.data.lens=42;scene.render.filepath=str(OUT/'environment_v040_Rock_River_Close.png');bpy.ops.render.render(write_still=True)
