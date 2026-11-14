"""Conservative projected bounds audit plus seven surface samples per local scan triangle."""
from pathlib import Path
import bpy,json,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=next(ROOT.glob('2_*'))/'background/map_3d'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'environment_v039.blend'));fields=np.load(OUT/'cliff_embedding_fields.npz');z=fields['z'];codes=fields['codes'];protected=(codes&17)!=0;integral=np.pad(protected.astype(np.int64).cumsum(0).cumsum(1),((1,0),(1,0)))
def sample(xy):
 u,v=np.clip(((xy+409.6)/.8).T,0,1024);i,j=np.minimum(u.astype(int),1023),np.minimum(v.astype(int),1023);a,b=u-i,v-j
 return z[j,i]*(1-a)*(1-b)+z[j,i+1]*a*(1-b)+z[j+1,i]*(1-a)*b+z[j+1,i+1]*a*b
rows=[]
for ob in bpy.data.collections['19_Embedded_scan_cliff_trial'].objects:
 me=ob.data;me.calc_loop_triangles();co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);ids=np.empty(len(me.loop_triangles)*3,np.int32);me.loop_triangles.foreach_get('vertices',ids);tri=co[ids.reshape(-1,3)]
 low=np.clip(np.floor((tri[:,:,:2].min(1)+409.6)/.8).astype(int)-1,0,1024);high=np.clip(np.ceil((tri[:,:,:2].max(1)+409.6)/.8).astype(int)+1,0,1024);x0,y0=low.T;x1,y1=(high+1).T;overlap=(integral[y1,x1]-integral[y0,x1]-integral[y1,x0]+integral[y0,x0])>0
 suspect=tri[overlap];max_above=-1e9;exposed_protected=0
 for weights in [(1,0,0),(0,1,0),(0,0,1),(.5,.5,0),(.5,0,.5),(0,.5,.5),(1/3,1/3,1/3)]:
  p=np.einsum('ijk,j->ik',suspect,np.array(weights));height=p[:,2]-sample(p[:,:2]);ij=np.clip(((p[:,:2]+409.6)/.8).astype(int),0,1024);mask=protected[ij[:,1],ij[:,0]]
  if mask.any():max_above=max(max_above,float(height[mask].max()));exposed_protected+=int(np.count_nonzero(mask&(height>.005)))
 rows.append({'object':ob.name,'triangles':len(tri),'triangles_with_conservative_protected_bbox':int(overlap.sum()),'exposed_protected_surface_samples':exposed_protected,'max_protected_sample_above_terrain_m':None if max_above<-1e8 else max_above})
report={'file':'environment_v039.blend','status':'diagnostic_not_collision_acceptance','method':'Triangle XY bounds expanded by one 0.8m grid step against protected-cell integral image; vertices, edge midpoints and centroid tested against terrain where bounds overlap. Seven samples do not prove complete triangle clipping.','patches':rows,'total_triangles':sum(r['triangles'] for r in rows),'conservative_potential_triangles':sum(r['triangles_with_conservative_protected_bbox'] for r in rows),'exposed_protected_surface_samples':sum(r['exposed_protected_surface_samples'] for r in rows)}
(OUT/'environment_v039_navigation_diagnostic.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='patches'}),flush=True)
